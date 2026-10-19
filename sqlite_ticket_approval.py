
# Northstar AI - SQLite Ticket Approval Integration
# Local development prototype

from datetime import datetime, timezone

import fresh_authorization
from session_auth import get_authenticated_username
from ticket_approval import (
    propose_ticket,
    pending_tickets,
    approval_lock
)
from idempotent_tickets import create_ticket_once


ALLOWED_ROLES = {
    "employee",
    "it_support",
    "hr_manager"
}


def approve_ticket_to_database(
    session_token, proposal_id, db_path=None
):
    # Resolve identity from the mock server session.
    username = get_authenticated_username(session_token)

    if username is None:
        return None, "Access denied: Invalid session."

    # Validate current cached authorization.
    role = fresh_authorization.cache.get_role(username)

    if role not in ALLOWED_ROLES:
        return None, "Access denied: Insufficient permissions."

    with approval_lock:
        proposal = pending_tickets.get(proposal_id)

        if proposal is None:
            return None, "Proposal invalid or already used."

        # Approval must belong to the same session.
        if (
            proposal["session_token"] != session_token
            or proposal["username"] != username
        ):
            return None, "Access denied: Wrong session."

        if datetime.now(timezone.utc) >= proposal["expires_at"]:
            del pending_tickets[proposal_id]
            return None, "Proposal expired."

        # Use the stored proposal details, not new
        # client-provided ticket information.
        try:
            ticket, created = create_ticket_once(
                proposal_id,
                username,
                proposal["issue"],
                db_path=db_path
            )
        except Exception:
            # Preserve proposal for an authorized retry.
            # Log this failure in a production service.
            return None, "Ticket storage failed."

        # Consume approval after successful persistence.
        del pending_tickets[proposal_id]

        return ticket, None
