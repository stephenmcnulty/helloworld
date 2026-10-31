import pytest

from app.auth import clean_identity, has_perm, safe_next


def test_identity_is_trimmed_lowercased_and_collapsed():
    who, problems = clean_identity("  Dana \t  Lee\n", "  Dana.Lee@Example.ORG ", "reviewer")
    assert problems == [] and who == {"name": "Dana Lee", "email": "dana.lee@example.org", "role": "reviewer"}


def test_control_characters_are_stripped_from_names():
    who, _ = clean_identity("Dana\x00\x1b[31m Lee", "d@example.org", "preparer")
    assert "\x00" not in who["name"] and "\x1b" not in who["name"]


@pytest.mark.parametrize("name,email,role", [
    ("", "a@b.co", "preparer"), ("A", "", "preparer"), ("A", "a@b", "preparer"), ("A", "a@b.co", ""), ("A", "a@b.co", "root"),
    ("A", "a b@c.co", "preparer"), ("A", "a@@b.co", "preparer"), ("A", "<a>@b.co", "preparer"), ("A" * 81, "a@b.co", "preparer"),
    ("A", "a" * 250 + "@b.co", "preparer"),
])
def test_bad_identities_are_rejected(name, email, role):
    who, problems = clean_identity(name, email, role)
    assert who is None and problems


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
