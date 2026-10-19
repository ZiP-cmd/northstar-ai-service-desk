
# Northstar AI - Secure Service Layer
# Educational prototype using mock authentication.

from session_auth import get_authenticated_username
import fresh_authorization
import ticket_system


ALLOWED_TICKET_ROLES = {
    "employee",
    "it_support",
    "hr_manager"
}


def get_document(session_token, document_name):
    """
    Retrieve a document using session-bound identity
    and the permission-aware retrieval system.

    Returns:
        (document_content, error)
    """

    username = get_authenticated_username(session_token)

    if username is None:
        return None, "Access denied: Invalid session."

    result = (
        fresh_authorization.retrieve_with_fresh_permissions(
            session_token,
            document_name
        )
    )

    if result.startswith((
        "Access denied:",
        "Document unavailable or access denied.",
        "Document content unavailable."
    )):
        return None, result

    return result, None


def submit_support_ticket(
    session_token,
    issue,
    confirmed=False
):
    """
    Create a support ticket using session identity,
    current role authorization, and confirmation.

    Returns:
        (ticket, error)
    """

    # Step 1: Verify session identity
    username = get_authenticated_username(session_token)

    if username is None:
        return None, "Access denied: Invalid session."

    # Step 2: Check authorization
    role = fresh_authorization.cache.get_role(username)

    if role not in ALLOWED_TICKET_ROLES:
        return None, "Access denied: Insufficient permissions."

    # Step 3: Validate issue
    if not isinstance(issue, str) or not issue.strip():
        return None, "Issue description cannot be empty."

    # Step 4: Require confirmation
    if confirmed is not True:
        return None, "Ticket creation not confirmed."

    # Step 5: Create ticket under the session identity
    return ticket_system.create_ticket(username, issue)
