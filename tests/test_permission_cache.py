
# Northstar AI - Permission Cache Security Tests

import pytest

from permission_cache import PermissionCache
from session_auth import active_sessions, create_demo_session
import fresh_authorization


@pytest.fixture
def revocation_setup(monkeypatch):
    """
    Create a test environment with simulated roles
    and a controllable clock.
    """

    current_time = [0.0]

    roles = {
        "michelle": "hr_manager",
        "sarah": "it_support"
    }

    cache = PermissionCache(
        role_provider=lambda username: roles.get(username),
        ttl_seconds=300,
        clock=lambda: current_time[0]
    )

    # Replace the real module's cache with our test cache
    monkeypatch.setattr(
        fresh_authorization,
        "cache",
        cache
    )

    active_sessions.clear()

    yield roles, current_time

    active_sessions.clear()


# TEST 1: HR manager initially has access

def test_hr_manager_initially_has_access(revocation_setup):

    token = create_demo_session("michelle")

    result = fresh_authorization.retrieve_with_fresh_permissions(
        token,
        "salary_report"
    )

    assert "confidential hr salary information" in result.lower()


# TEST 2: Permissions expire and refresh

def test_permissions_expire_and_are_refreshed(revocation_setup):

    roles, current_time = revocation_setup

    token = create_demo_session("michelle")

    # Populate the cache while Michelle is HR manager
    fresh_authorization.retrieve_with_fresh_permissions(
        token,
        "salary_report"
    )

    # HR revokes Michelle's privileged role
    roles["michelle"] = "employee"

    # At 299 seconds, the old cached role is valid
    current_time[0] = 299

    result_before = (
        fresh_authorization.retrieve_with_fresh_permissions(
            token,
            "salary_report"
        )
    )

    assert "confidential hr salary information" in result_before.lower()

    # At 300 seconds, the cached role expires
    current_time[0] = 300

    result_after = (
        fresh_authorization.retrieve_with_fresh_permissions(
            token,
            "salary_report"
        )
    )

    assert result_after == (
        "Access denied: Insufficient permissions."
    )


# TEST 3: Invalid sessions are rejected

def test_invalid_session_is_rejected(revocation_setup):

    result = fresh_authorization.retrieve_with_fresh_permissions(
        "invalid-session",
        "salary_report"
    )

    assert result == "Access denied: Invalid session."


# TEST 4: Missing roles are denied

def test_unknown_role_denied(revocation_setup):

    roles, current_time = revocation_setup

    roles.pop("michelle")

    token = create_demo_session("michelle")

    result = fresh_authorization.retrieve_with_fresh_permissions(
        token,
        "salary_report"
    )

    assert result == "Access denied: Role unavailable."
