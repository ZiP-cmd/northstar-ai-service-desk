
# Northstar AI - SQLite Approval Integration Tests

import sqlite3
import pytest

import fresh_authorization
import ticket_approval

from permission_cache import PermissionCache
from session_auth import (
    active_sessions,
    create_demo_session
)
from sqlite_ticket_approval import (
    approve_ticket_to_database,
    propose_ticket
)


@pytest.fixture
def approval_db_setup(tmp_path, monkeypatch):
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

    database = tmp_path / "approval_test.db"

    yield roles, database

    active_sessions.clear()
    ticket_approval.pending_tickets.clear()


def test_approved_ticket_saved_to_sqlite(approval_db_setup):
    roles, database = approval_db_setup
    token = create_demo_session("james")

    proposal, error = propose_ticket(
        token, "VPN connection problem"
    )
    assert error is None

    ticket, error = approve_ticket_to_database(
        token,
        proposal["proposal_id"],
        db_path=database
    )

    assert error is None
    assert ticket["employee"] == "james"

    with sqlite3.connect(database) as conn:
        count = conn.execute(
            "SELECT COUNT(*) FROM tickets"
        ).fetchone()[0]

    assert count == 1


def test_wrong_session_cannot_save_ticket(approval_db_setup):
    roles, database = approval_db_setup

    james = create_demo_session("james")
    sarah = create_demo_session("sarah")

    proposal, error = propose_ticket(
        james, "VPN connection problem"
    )
    assert error is None

    ticket, error = approve_ticket_to_database(
        sarah,
        proposal["proposal_id"],
        db_path=database
    )

    assert ticket is None
    assert error == "Access denied: Wrong session."
    assert not database.exists()


def test_repeated_approval_creates_no_duplicate(
    approval_db_setup
):
    roles, database = approval_db_setup
    token = create_demo_session("james")

    proposal, error = propose_ticket(
        token, "VPN connection problem"
    )
    assert error is None

    first, first_error = approve_ticket_to_database(
        token, proposal["proposal_id"], db_path=database
    )
    second, second_error = approve_ticket_to_database(
        token, proposal["proposal_id"], db_path=database
    )

    assert first_error is None
    assert first is not None
    assert second is None
    assert second_error == "Proposal invalid or already used."

    with sqlite3.connect(database) as conn:
        count = conn.execute(
            "SELECT COUNT(*) FROM tickets"
        ).fetchone()[0]

    assert count == 1
