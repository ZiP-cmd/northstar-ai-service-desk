
# Northstar AI - Secure Ticket Approval Prototype

import secrets
import threading
from datetime import datetime, timedelta, timezone

from session_auth import get_authenticated_username
from secure_service import submit_support_ticket


# Server-held pending proposals
pending_tickets = {}

# Prevent simultaneous approvals within this process
approval_lock = threading.Lock()


def propose_ticket(session_token, issue):
    """Save an immutable proposal for employee review."""

    username = get_authenticated_username(session_token)

    if username is None:
        return None, "Access denied: Invalid session."

    if not isinstance(issue, str) or not issue.strip():
        return None, "Issue description cannot be empty."

    proposal_id = secrets.token_urlsafe(24)

    proposal = {
        "username": username,
        "session_token": session_token,
        "issue": issue.strip(),
        "expires_at": (
            datetime.now(timezone.utc) + timedelta(minutes=5)
        )
    }

    with approval_lock:
        pending_tickets[proposal_id] = proposal

    # Return a preview, not the private session token
    return {
        "proposal_id": proposal_id,
        "employee": username,
        "issue": proposal["issue"]
    }, None


def approve_ticket(session_token, proposal_id):
    """Create a ticket from a server-stored proposal."""

    username = get_authenticated_username(session_token)

    if username is None:
        return None, "Access denied: Invalid session."

    with approval_lock:
        proposal = pending_tickets.get(proposal_id)

        if proposal is None:
            return None, "Proposal invalid or already used."

        if (
            proposal["session_token"] != session_token
            or proposal["username"] != username
        ):
            return None, "Access denied: Wrong session."

        if datetime.now(timezone.utc) >= proposal["expires_at"]:
            del pending_tickets[proposal_id]
            return None, "Proposal expired."

        # Consume the proposal before creating the ticket.
        del pending_tickets[proposal_id]

        return submit_support_ticket(
            session_token,
            proposal["issue"],
            confirmed=True
        )
