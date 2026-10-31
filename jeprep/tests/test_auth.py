import pytest

from app.auth import has_perm, roles_from_groups, safe_next, setup_oauth
from app.config import Settings

OKTA = {"OKTA_ISSUER": "https://acme.okta.com", "OKTA_CLIENT_ID": "cid", "OKTA_CLIENT_SECRET": "sec", "SECRET_KEY": "k" * 40}


@pytest.fixture
def okta_settings(tmp_path):
    return Settings.from_env({**OKTA, "DATA_DIR": str(tmp_path)})


def test_okta_groups_map_to_roles(okta_settings):
    assert roles_from_groups(["Everyone", "JE-Reviewer"], okta_settings) == ["reviewer"]
    assert roles_from_groups(["JE-Preparer", "JE-Admin"], okta_settings) == ["admin", "preparer"]
    assert roles_from_groups("JE-Admin", okta_settings) == ["admin"]          # a single group arrives as a string


def test_no_matching_group_means_no_access(okta_settings):
    assert roles_from_groups(["Everyone", "Finance"], okta_settings) == []
    assert roles_from_groups(None, okta_settings) == []


def test_group_names_are_configurable(tmp_path):
    s = Settings.from_env({**OKTA, "DATA_DIR": str(tmp_path), "OKTA_GROUP_REVIEWER": "Firm-JE-Approvers"})
    assert roles_from_groups(["Firm-JE-Approvers"], s) == ["reviewer"]
    assert roles_from_groups(["JE-Reviewer"], s) == []


def test_oidc_client_is_registered_for_okta_with_pkce(okta_settings):
    oauth = setup_oauth(okta_settings)
    client = oauth.create_client("okta")
    assert client._server_metadata_url == "https://acme.okta.com/.well-known/openid-configuration"
    assert client.client_kwargs["scope"] == "openid profile email groups"
    assert client.client_kwargs["code_challenge_method"] == "S256"


def test_no_oidc_client_without_okta_settings(tmp_path):
    assert setup_oauth(Settings.from_env({"DEMO_MODE": "true", "DATA_DIR": str(tmp_path)})) is None


def test_permissions_by_role():
    user = lambda *roles: {"email": "x@y", "roles": list(roles)}  # noqa: E731
    assert has_perm(user("preparer"), "job.work") and not has_perm(user("preparer"), "export.approve")
    assert has_perm(user("reviewer"), "export.approve") and has_perm(user("reviewer"), "mapping.approve")
    assert not has_perm(user("reviewer"), "audit.view") and not has_perm(user("admin"), "job.create")
    assert has_perm(user("admin"), "audit.view") and has_perm(user("admin"), "admin.clients")
    assert not has_perm(None, "job.work") and not has_perm(user(), "job.work")


@pytest.mark.parametrize("raw,expected", [
    ("/jobs/3/preview", "/jobs/3/preview"), ("//evil.example", "/"), ("https://evil.example", "/"),
    ("/\\evil.example", "/"), ("", "/"), (None, "/"), ("/ok?x=1", "/ok?x=1"),
])
def test_safe_next_blocks_open_redirects(raw, expected):
    assert safe_next(raw) == expected
