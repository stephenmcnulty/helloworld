"""Build the single-file browser walkthrough from the REAL demo data and engine.

    python artifact/build.py                       -> artifact/journal-entry-prep.html
    python artifact/build.py --expected out.json   -> also write Python-engine results used by verify_engine.js

The page re-implements the engine in JavaScript so it can run with no server. To keep the two from
drifting, `verify_engine.js` replays the cases below through the JS engine and compares the output
(including the exact export CSV bytes) with what the Python engine produces.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from dataclasses import replace
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from app.demo import generate as gen  # noqa: E402
from app.demo.seed import demo_clients  # noqa: E402
from app.exporters import export_journal  # noqa: E402
from app.journal import build_journal  # noqa: E402
from app.parsing import parse_report  # noqa: E402
from app.redaction import build_model_payload  # noqa: E402
from app.rules import propose_from_rules  # noqa: E402
from app.suggest import mock_lines  # noqa: E402
from app.validation import run_checks  # noqa: E402

CLIENTS = {c.id: c for c in demo_clients()}


def holy_cross_csv() -> str:
    """The Excel sample, expressed as CSV (title rows included) because the page can't read .xlsx."""
    rows = [gen.standard_row(e, gen.compute_pay(e), "10/15/2026") for e in gen.employees_for("holy-cross-school")]
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(["Holy Cross School - Payroll Register"])
    w.writerow(["Pay period 10/01/2026 - 10/15/2026 (synthetic demo data)"])
    w.writerow([])
    w.writerow(gen.STANDARD_HEADERS)
    w.writerows(rows)
    w.writerow(gen.totals_row(rows, 4))
    return buf.getvalue()


def file_texts() -> dict[str, str]:
    out = {}
    for name, data in gen.sample_bytes().items():
        out[name] = data.decode("utf-8") if name.endswith(".csv") else holy_cross_csv()
    out["holy-cross-school_payroll_2026-10-15.xlsx"] = holy_cross_csv()
    return out


def client_json(c) -> dict:
    return {
        "id": c.id, "name": c.name, "description": c.description, "dueFrom": c.due_from_account, "dueTo": c.due_to_account,
        "entities": [{"code": e.code, "name": e.name, "pct": float(e.alloc_pct), "paying": e.is_paying, "fund": e.default_fund}
                     for e in c.entities],
        "funds": c.funds,
        "accounts": [{"no": a.account_no, "name": a.name, "category": a.category} for a in c.accounts.values()],
    }


def saved_mappings() -> list[dict]:
    """The two approved versions seeded for Our Lady of Grace (same construction as app/demo/seed.py)."""
    cfg = CLIENTS["our-lady-grace"]
    report = parse_report(gen.standard_csv("our-lady-grace"), ".csv")
    base = [replace(l, origin="saved", reviewed=True, rationale="") for l in propose_from_rules(report, cfg)]
    v1 = [replace(l, gl_account="6030") if l.source_column == "Employer 403(b) Match" else l for l in base]
    return [
        {"clientId": cfg.id, "version": 1, "note": "initial mapping", "decidedBy": "rhea.reviewer@demo.example",
         "lines": [l.to_dict() for l in v1]},
        {"clientId": cfg.id, "version": 2, "note": "corrected employer 403(b) match account", "decidedBy": "rhea.reviewer@demo.example",
         "lines": [l.to_dict() for l in base]},
    ]


def demo_data() -> dict:
    texts = file_texts()
    return {
        "clients": [client_json(c) for c in CLIENTS.values()],
        "files": [{"filename": s.filename, "clientId": s.client_id, "title": s.title, "description": s.description,
                   "start": s.period_start.isoformat(), "end": s.period_end.isoformat(), "csv": texts[s.filename]}
                  for s in gen.SAMPLE_FILES],
        "saved": saved_mappings(),
    }


# (case name, client, file, target, start, end, allocate, how the mapping is produced)
CASES = [
    ("olg-saved-allocated", "our-lady-grace", "our-lady-grace_payroll_2026-10-15.csv", "intacct", "2026-10-01", "2026-10-15", True, "saved2"),
    ("olg-saved-plain-qbo", "our-lady-grace", "our-lady-grace_payroll_2026-10-15.csv", "qbo", "2026-10-01", "2026-10-15", False, "saved2"),
    ("olg-saved-v1", "our-lady-grace", "our-lady-grace_payroll_2026-10-15.csv", "intacct", "2026-10-01", "2026-10-15", True, "saved1"),
    ("stbrigid-rules-qbo", "st-brigid", "st-brigid_payroll_2026-10-15.csv", "qbo", "2026-10-01", "2026-10-15", False, "rules"),
    ("holycross-title-rows", "holy-cross-school", "holy-cross-school_payroll_2026-10-15.xlsx", "intacct", "2026-10-01", "2026-10-15", False, "rules"),
    ("olg-newlayout-mock-allocated", "our-lady-grace", "our-lady-grace_payroll_2026-10-31_NEW-LAYOUT.csv", "intacct", "2026-10-16", "2026-10-31", True, "mock"),
    ("olg-newlayout-mock-plain-qbo", "our-lady-grace", "our-lady-grace_payroll_2026-10-31_NEW-LAYOUT.csv", "qbo", "2026-10-16", "2026-10-31", False, "mock"),
    ("olg-broken", "our-lady-grace", "our-lady-grace_payroll_2026-10-15_BROKEN.csv", "intacct", "2026-10-01", "2026-10-15", False, "rules"),
    ("olg-wrong-period", "our-lady-grace", "our-lady-grace_payroll_2026-10-15.csv", "intacct", "2026-11-01", "2026-11-15", False, "saved2"),
]


def expected_cases() -> list[dict]:
    texts, saved = file_texts(), {m["version"]: m for m in saved_mappings()}
    out = []
    for name, cid, fname, target, start, end, allocate, how in CASES:
        client, report = CLIENTS[cid], parse_report(texts[fname].encode(), ".csv")
        from app.domain import MappingLine

        if how == "rules":
            lines = propose_from_rules(report, client)
        elif how == "mock":
            lines = mock_lines(report, client)
        else:
            lines = [MappingLine.from_dict(d) for d in saved[int(how[-1])]["lines"]]
        s, e = date.fromisoformat(start), date.fromisoformat(end)
        j = build_journal(report, lines, client, period_start=s, period_end=e, allocate=allocate, target=target)
        checks, tie = run_checks(report, lines, client, j, s, e)
        exported = export_journal(j).content.decode() if all(c.status != "fail" for c in checks) else None
        payload = build_model_payload(report)
        out.append({
            "name": name, "clientId": cid, "file": fname, "target": target, "start": start, "end": end, "allocate": allocate,
            "how": how, "headers": report.headers, "signature_headers": sorted(report.headers),
            "mapping": [l.to_dict() for l in lines],
            "lines": [[l.line_no, l.account_no, l.entity, l.fund, str(l.debit), str(l.credit), l.memo, l.kind] for l in j.lines],
            "checks": [[c.id, c.status, c.detail] for c in checks],
            "tie": [[r.column, str(r.source_total), None if r.stated_total is None else str(r.stated_total),
                     str(r.journal_amount), r.note] for r in tie],
            "reference": j.reference, "description": j.description, "debits": str(j.total_debits), "credits": str(j.total_credits),
            "csv": exported, "payload_rows": payload.payload["sample_rows"], "columns_redacted": payload.columns_redacted,
        })
    return out


def build(out_path: Path) -> None:
    template = (HERE / "template.html").read_text(encoding="utf-8")
    marker = "/*DATA*/"
    assert marker in template, "template is missing the /*DATA*/ marker"
    blob = json.dumps(demo_data(), separators=(",", ":")).replace("</", "<\\/")
    out_path.write_text(template.replace(marker, f"const DEMO = {blob};"), encoding="utf-8")
    print(f"wrote {out_path} ({out_path.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(HERE / "journal-entry-prep.html"))
    ap.add_argument("--expected", help="write Python engine results for verify_engine.js")
    args = ap.parse_args()
    build(Path(args.out))
    if args.expected:
        Path(args.expected).write_text(json.dumps(expected_cases()), encoding="utf-8")
        print(f"wrote {args.expected} ({len(CASES)} cases)")
