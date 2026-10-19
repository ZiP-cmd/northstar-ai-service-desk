
# Northstar AI - Database Idempotency Tests

import sqlite3
import pytest

from idempotent_tickets import create_ticket_once


def test_first_approval_creates_ticket(tmp_path):
    database = tmp_path / "test.db"

    ticket, created = create_ticket_once(
        "proposal-123",
        "james",
        "VPN not connecting",
        db_path=database
    )

    assert created is True
    assert ticket["employee"] == "james"
    assert ticket["status"] == "Open"


def test_retry_returns_same_ticket(tmp_path):
    database = tmp_path / "test.db"

    first, first_created = create_ticket_once(
        "proposal-123", "james",
        "VPN not connecting", db_path=database
    )

    second, second_created = create_ticket_once(
        "proposal-123", "james",
        "VPN not connecting", db_path=database
    )

    assert first_created is True
    assert second_created is False
    assert first["ticket_id"] == second["ticket_id"]

    with sqlite3.connect(database) as conn:
        count = conn.execute(
            "SELECT COUNT(*) FROM tickets"
        ).fetchone()[0]

    assert count == 1


def test_same_id_cannot_change_employee(tmp_path):
    database = tmp_path / "test.db"

    create_ticket_once(
        "proposal-123", "james",
        "VPN not connecting", db_path=database
    )

    with pytest.raises(ValueError):
        create_ticket_once(
            "proposal-123", "sarah",
            "VPN not connecting", db_path=database
        )


def test_same_id_cannot_change_issue(tmp_path):
    database = tmp_path / "test.db"

    create_ticket_once(
        "proposal-123", "james",
        "VPN not connecting", db_path=database
    )

    with pytest.raises(ValueError):
        create_ticket_once(
            "proposal-123", "james",
            "Different issue", db_path=database
        )
