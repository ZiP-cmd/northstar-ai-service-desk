
# Northstar AI - Automated Secure Service Tests

import json
import pytest

import fresh_authorization
import secure_service
import ticket_system

from permission_cache import PermissionCache
from session_auth import (
    active_sessions,
    create_demo_session,
    end_session
)


@pytest.fixture
def service_setup(tmp_path, monkeypatch):
    """
    Create isolated test sessions, roles,
    permission cache, and ticket storage.
    """

    active_sessions.clear()

    roles = {
        "james": "employee",
        "sarah": "it_support",
        "michelle": "hr_manager"
    }

    cache = PermissionCache(
        role_provider=lambda user: roles.get(user),
        ttl_seconds=300
    )

    # Use our test authorization cache
    monkeypatch.setattr(
        fresh_authorization,
        "cache",
        cache
    )

    # Save test tickets in a temporary location
    ticket_file = tmp_path / "tickets.json"

    monkeypatch.setattr(
        ticket_system,
        "TICKET_FILE",
        ticket_file
    )

    yield roles, ticket_file

    active_sessions.clear()


# TEST 1: Authorized document retrieval

def test_authorized_document_access(service_setup):
    token = create_demo_session("james")

    content, error = secure_service.get_document(
        token,
        "vpn_guide"
    )

    assert error is None
    assert isinstance(content, str)
    assert "approved VPN application" in content


# TEST 2: Restricted document retrieval

def test_restricted_document_denied(service_setup):
    token = create_demo_session("sarah")

    content, error = secure_service.get_document(
        token,
        "salary_report"
    )

    assert content is None
    assert error == (
        "Access denied: Insufficient permissions."
    )


# TEST 3: Invalid session cannot create tickets

def test_invalid_session_cannot_create_ticket(service_setup):
    roles, ticket_file = service_setup

    ticket, error = secure_service.submit_support_ticket(
        "invalid-session",
        "VPN issue",
        confirmed=True
    )

    assert ticket is None
    assert error == "Access denied: Invalid session."
    assert not ticket_file.exists()


# TEST 4: Ticket creation requires confirmation

def test_ticket_requires_confirmation(service_setup):
    roles, ticket_file = service_setup

    token = create_demo_session("james")

    ticket, error = secure_service.submit_support_ticket(
        token,
        "VPN issue",
        confirmed=False
    )

    assert ticket is None
    assert error == "Ticket creation not confirmed."
    assert not ticket_file.exists()


# TEST 5: Ticket uses authenticated session identity

def test_ticket_uses_session_identity(service_setup):
    roles, ticket_file = service_setup

    token = create_demo_session("sarah")

    ticket, error = secure_service.submit_support_ticket(
        token,
        "Cannot access company VPN",
        confirmed=True
    )

    assert error is None
    assert ticket["employee"] == "sarah"

    saved = json.loads(
        ticket_file.read_text(encoding="utf-8")
    )

    assert len(saved) == 1
    assert saved[0]["employee"] == "sarah"


# TEST 6: Logged-out sessions cannot create tickets

def test_revoked_session_cannot_create_ticket(service_setup):
    roles, ticket_file = service_setup

    token = create_demo_session("james")
    end_session(token)

    ticket, error = secure_service.submit_support_ticket(
        token,
        "VPN issue",
        confirmed=True
    )

    assert ticket is None
    assert error == "Access denied: Invalid session."
    assert not ticket_file.exists()


# TEST 7: Unauthorized roles cannot create tickets

def test_unknown_role_cannot_create_ticket(service_setup):
    roles, ticket_file = service_setup

    token = create_demo_session("james")

    # Simulate a role change
    roles["james"] = "unrecognized_role"

    ticket, error = secure_service.submit_support_ticket(
        token,
        "VPN issue",
        confirmed=True
    )

    assert ticket is None
    assert error == (
        "Access denied: Insufficient permissions."
    )
    assert not ticket_file.exists()
