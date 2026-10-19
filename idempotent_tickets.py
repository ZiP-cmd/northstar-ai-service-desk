
# Northstar AI - Idempotent Ticket Storage
# Local SQLite implementation for development

import sqlite3
from pathlib import Path
from uuid import uuid4

DATABASE = Path(__file__).with_name("northstar_tickets.db")


def create_ticket_once(proposal_id, username, issue, db_path=None):
    """
    Create at most one ticket for each proposal ID.

    If the same proposal is submitted again,
    return the previously created ticket.

    Assumes proposal identity, owner, and details
    were already validated by the service layer.
    """

    if not all(
        isinstance(value, str) and value.strip()
        for value in (proposal_id, username, issue)
    ):
        raise ValueError("Invalid ticket details.")

    database = str(db_path or DATABASE)

    with sqlite3.connect(database, timeout=10) as conn:
        conn.row_factory = sqlite3.Row

        conn.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                proposal_id TEXT PRIMARY KEY,
                ticket_id TEXT NOT NULL UNIQUE,
                employee TEXT NOT NULL,
                issue TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Open'
            )
        """)

        # Acquire the write transaction before checking.
        conn.execute("BEGIN IMMEDIATE")

        existing = conn.execute(
            "SELECT * FROM tickets WHERE proposal_id = ?",
            (proposal_id,)
        ).fetchone()

        if existing:
            if (
                existing["employee"] != username
                or existing["issue"] != issue
            ):
                raise ValueError(
                    "Proposal ID reused with different details."
                )

            return dict(existing), False

        ticket_id = "NST-" + uuid4().hex[:12].upper()

        conn.execute(
            """
            INSERT INTO tickets
                (proposal_id, ticket_id, employee, issue)
            VALUES (?, ?, ?, ?)
            """,
            (proposal_id, ticket_id, username, issue)
        )

        ticket = conn.execute(
            "SELECT * FROM tickets WHERE proposal_id = ?",
            (proposal_id,)
        ).fetchone()

        conn.commit()
        return dict(ticket), True
