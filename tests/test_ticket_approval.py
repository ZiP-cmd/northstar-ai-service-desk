
# Northstar AI - Ticket Approval Security Tests

from datetime import datetime, timedelta, timezone

import pytest

import ticket_approval
import ticket_system
import fresh_authorization

from permission_cache import PermissionCache
from session_auth import (
    active_sessions,
    create_demo_session,
    end_session
)


@pytest.fixture
def approval_setup(tmp_path, monkeypatch):
    """Create an isolated security test environment."""

    active_sessions.clear()
    ticket_approval.pending_tickets.clear()

    roles = {
        "james": "employee",
        "sarah": "it_support",
        "michelle": "hr_manager"
    }

    test_cache = PermissionCache(
        role_provider=lambda user: roles.get(user),
        ttl_seconds=300
    )

    monkeypatch.setattr(
        fresh_authorization,
        "cache",
        test_cache
    )

    ticket_file = tmp_path / "tickets.json"

    monkeypatch.setattr(
        ticket_system,
        "TICKET_FILE",
        ticket_file
    )

    yield roles, ticket_file

    active_sessions.clear()
    ticket_approval.pending_tickets.clear()


# TEST 1: Employee can approve their own ticket

def test_valid_ticket_approval(approval_setup):
    roles, ticket_file = approval_setup

    token = create_demo_session("james")

    proposal, error = ticket_approval.propose_ticket(
        token, "VPN connection problem"
    )

    assert error is None

    ticket, error = ticket_approval.approve_ticket(
        token, proposal["proposal_id"]
    )

    assert error is None
    assert ticket["employee"] == "james"
    assert ticket_file.exists()


# TEST 2: A proposal cannot be approved twice

def test_duplicate_approval_rejected(approval_setup):
    roles, ticket_file = approval_setup

    token = create_demo_session("james")

    proposal, error = ticket_approval.propose_ticket(
        token, "VPN connection problem"
    )

    first_ticket, first_error = (
        ticket_approval.approve_ticket(
            token, proposal["proposal_id"]
        )
    )

    second_ticket, second_error = (
        ticket_approval.approve_ticket(
            token, proposal["proposal_id"]
        )
    )

    assert first_error is None
    assert first_ticket is not None

    assert second_ticket is None
    assert second_error == "Proposal invalid or already used."


# TEST 3: Another employee cannot approve the proposal

def test_wrong_session_rejected(approval_setup):
    roles, ticket_file = approval_setup

    james_token = create_demo_session("james")
    sarah_token = create_demo_session("sarah")

    proposal, error = ticket_approval.propose_ticket(
        james_token, "VPN connection problem"
    )

    ticket, error = ticket_approval.approve_ticket(
        sarah_token, proposal["proposal_id"]
    )

    assert ticket is None
    assert error == "Access denied: Wrong session."
    assert not ticket_file.exists()


# TEST 4: Expired proposals are rejected

def test_expired_proposal_rejected(approval_setup):
    roles, ticket_file = approval_setup

    token = create_demo_session("james")

    proposal, error = ticket_approval.propose_ticket(
        token, "VPN connection problem"
    )

    proposal_id = proposal["proposal_id"]

    # Simulate expiration without waiting five minutes.
    ticket_approval.pending_tickets[proposal_id][
        "expires_at"
    ] = datetime.now(timezone.utc) - timedelta(seconds=1)

    ticket, error = ticket_approval.approve_ticket(
        token, proposal_id
    )

    assert ticket is None
    assert error == "Proposal expired."
    assert not ticket_file.exists()


# TEST 5: Revoked sessions cannot approve tickets

def test_revoked_session_rejected(approval_setup):
    roles, ticket_file = approval_setup

    token = create_demo_session("james")

    proposal, error = ticket_approval.propose_ticket(
        token, "VPN connection problem"
    )

    end_session(token)

    ticket, error = ticket_approval.approve_ticket(
        token, proposal["proposal_id"]
    )

    assert ticket is None
    assert error == "Access denied: Invalid session."
    assert not ticket_file.exists()


# TEST 6: A revoked role cannot approve tickets

def test_revoked_role_rejected(approval_setup):
    roles, ticket_file = approval_setup

    token = create_demo_session("james")

    proposal, error = ticket_approval.propose_ticket(
        token, "VPN connection problem"
    )

    # Simulate permission revocation before approval.
    roles["james"] = "suspended"

    ticket, error = ticket_approval.approve_ticket(
        token, proposal["proposal_id"]
    )

    assert ticket is None
    assert error == "Access denied: Insufficient permissions."
    assert not ticket_file.exists()
