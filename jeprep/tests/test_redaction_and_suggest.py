"""Privacy tests for the model path: names/IDs must never leave the process."""
import json
from types import SimpleNamespace

import pytest

from app.parsing import parse_report
from app.redaction import build_model_payload, restore
from app.suggest import MOCK_LABEL, normalize_ai_lines, response_schema, suggest_mapping
from tests.conftest import csv_bytes, make_client

NAMES = ["Avery Stone", "Blake Rivera", "Casey Nguyen", "Drew Okafor", "Emery Walsh"]
IDS = ["77310", "77311", "77312", "77313", "77314"]
SSNS = ["123-45-6789", "987-65-4321", "111-22-3333", "222-33-4444", "333-44-5555"]

HEADERS = ["Legal Name", "Badge", "SSN", "Dept", "Notes", "Check Date", "Base Comp", "Housing Allowance",
           "Total Earnings", "Disbursed Amount", "Soc Sec / Medicare (Org)"]


def new_layout_report():
    rows = []
    for i, (n, badge, ssn) in enumerate(zip(NAMES, IDS, SSNS)):
        base, housing = 1000 + 100 * i, 50 * (i + 1)
        # free text that mentions people: repeated for most rows so it is not caught as a unique-per-row column
        note = f"Check issued to {NAMES[0]} re: {SSNS[0]} jsmith0@example.org" if i < 4 else "n/a"
        rows.append([n, badge, ssn, ["Ministry", "Office"][i % 2], note, "10/31/2026",
                     f"{base}.00", f"{housing}.00", f"{base + housing}.00", f"{base - 100}.00", f"{base * 0.0765:.2f}"])
    return parse_report(csv_bytes(HEADERS, rows), ".csv")


def flat(obj) -> str:
    return json.dumps(obj)


def test_payload_contains_no_names_ids_ssns_or_emails():
    result = build_model_payload(new_layout_report())
    text = flat(result.payload)
    for secret in NAMES + IDS + SSNS + ["jsmith0@example.org", "example.org"]:
        assert secret not in text, secret
    assert len(result.payload["sample_rows"]) == 3
    assert result.values_redacted > 0


def test_tokens_replace_values_and_are_consistent():
    result = build_model_payload(new_layout_report())
    row0 = result.payload["sample_rows"][0]
    assert row0["Legal Name"] == "EMP_001"
    assert row0["Badge"].startswith("ID_")           # numeric-only ID column caught by the heuristic
    assert row0["SSN"].startswith("ID_")
    assert row0["Notes"].startswith("Check issued to EMP_001")   # names inside free text are scrubbed too
    assert result.token_map["EMP_001"] == "Avery Stone"


def test_non_identifying_columns_survive_redaction():
    row0 = build_model_payload(new_layout_report()).payload["sample_rows"][0]
    assert row0["Dept"] == "Ministry"
    assert row0["Base Comp"] == "1000.00"
    assert row0["Check Date"] == "10/31/2026"


def test_token_map_only_holds_tokens_that_were_sent():
    result = build_model_payload(new_layout_report())
    assert "EMP_005" not in result.token_map     # employee 5 is not in the 3-row sample
    assert all(t in flat(result.payload) for t in result.token_map)


def test_restore_puts_real_values_back():
    assert restore("EMP_001 looks odd", {"EMP_001": "Avery Stone"}) == "Avery Stone looks odd"
    assert restore("EMP_999 unknown", {}) == "EMP_999 unknown"


# ---------------------------------------------------------------- suggest_mapping()
def stub_client(response=None, raises=None, stop_reason="end_turn"):
    calls = []

    def create(**kwargs):
        calls.append(kwargs)
        if raises:
            raise raises
        text = json.dumps(response)
        return SimpleNamespace(stop_reason=stop_reason, content=[SimpleNamespace(type="text", text=text)])

    return SimpleNamespace(messages=SimpleNamespace(create=create)), calls


def ai_line(col, **kw):
    base = dict(source_column=col, role="ignore", line_type="", side="", gl_account="", offset_account="", entity="",
                fund="", memo="", confidence=0.9, rationale="because")
    base.update(kw)
    return base


def test_no_api_key_falls_back_to_a_clearly_labelled_mock(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    s = suggest_mapping(new_layout_report(), make_client())
    assert s.source == "mock" and s.notice == MOCK_LABEL and "no AI model was called" in s.notice
    assert all(l.origin == "mock" for l in s.lines)
    assert all(l.reviewed is False for l in s.lines)           # never pre-approved


def test_mock_covers_every_column_and_finds_the_subtotal(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    report = new_layout_report()
    lines = {l.source_column: l for l in suggest_mapping(report, make_client()).lines}
    assert set(lines) == set(report.headers)
    assert lines["Total Earnings"].role == "ignore"            # = Base Comp + Housing Allowance, would double count
    assert lines["Base Comp"].role == "amount" and lines["Housing Allowance"].role == "amount"
    assert lines["Disbursed Amount"].role == "amount" and lines["Disbursed Amount"].gl_account == "1010"
    assert lines["Soc Sec / Medicare (Org)"].offset_account == "2120"
    assert lines["Legal Name"].role == "employee_name"


def test_claude_path_sends_only_redacted_data(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    report, client = new_layout_report(), make_client()
    resp = {"lines": [ai_line("Legal Name", role="employee_name"),
                      ai_line("Base Comp", role="amount", line_type="expense", side="debit", gl_account="6010",
                              entity="PARISH", fund="UNR", rationale="Base pay for EMP_001 and others")]}
    stub, calls = stub_client(resp)
    s = suggest_mapping(report, client, api_key="sk-test", anthropic_client=stub, model="claude-test")
    assert s.source == "claude" and s.model == "claude-test"
    request_text = json.dumps(calls[0], default=str)
    for secret in NAMES + IDS + SSNS + ["jsmith0@example.org"]:
        assert secret not in request_text, secret
    assert "EMP_001" in request_text and "6010" in request_text      # tokens and the chart ARE sent
    assert calls[0]["output_config"]["format"]["type"] == "json_schema"
    # the rationale had a token in it: it is restored locally, after the response
    base = next(l for l in s.lines if l.source_column == "Base Comp")
    assert "Avery Stone" in base.rationale
    assert all(l.reviewed is False and l.origin == "ai" for l in s.lines)


def test_model_output_is_validated_against_the_clients_chart():
    report, client = new_layout_report(), make_client()
    raw = [ai_line("Base Comp", role="amount", line_type="expense", side="debit", gl_account="9999",
                   offset_account="8888", entity="NOPE", fund="NOPE"),
           ai_line("Legal Name", role="bogus-role")]
    lines = {l.source_column: l for l in normalize_ai_lines(raw, report, client, {}, "ai")}
    base = lines["Base Comp"]
    assert base.gl_account == "" and base.offset_account == ""           # unknown accounts are cleared
    assert base.entity == "PARISH" and base.fund == "UNR"                # defaults, not the invented values
    assert "not in the chart" in base.rationale
    assert lines["Legal Name"].role == ""                                # unknown role -> unassigned
    assert lines["Check Date"].rationale.startswith("The suggestion did not cover")


def test_amount_role_on_a_text_column_is_cleared():
    report, client = new_layout_report(), make_client()
    raw = [ai_line("Dept", role="amount", line_type="expense", side="debit", gl_account="6010", entity="PARISH", fund="UNR")]
    line = next(l for l in normalize_ai_lines(raw, report, client, {}, "ai") if l.source_column == "Dept")
    assert line.role == "" and line.gl_account == ""


@pytest.mark.parametrize("kwargs", [
    dict(raises=RuntimeError("boom")),
    dict(response={"lines": []}, stop_reason="refusal"),
    dict(response={"lines": []}, stop_reason="max_tokens"),
])
def test_api_failure_falls_back_to_labelled_mock_and_does_not_leak_errors(kwargs):
    stub, _ = stub_client(**kwargs)
    s = suggest_mapping(new_layout_report(), make_client(), api_key="sk-test", anthropic_client=stub)
    assert s.source == "mock" and "MOCK SUGGESTION" in s.notice


def test_schema_only_allows_the_clients_own_accounts_entities_and_funds():
    schema = response_schema(make_client(multi=True))
    props = schema["properties"]["lines"]["items"]["properties"]
    assert "6010" in props["gl_account"]["enum"] and "9999" not in props["gl_account"]["enum"]
    assert set(props["entity"]["enum"]) == {"", "PARISH", "SCHOOL", "STORE"}
    assert schema["additionalProperties"] is False
