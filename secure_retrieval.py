
# Northstar AI - Session-Bound Document Retrieval

from access_control import check_access
from document_retrieval import retrieve_document
from session_auth import get_authenticated_username


def secure_retrieve(session_token, document_name):
    # Derive identity from our mock server session.
    username = get_authenticated_username(session_token)

    if username is None:
        return "Access denied: Invalid session."

    # Do not accept a username from the document request.
    decision = check_access(username, document_name)

    if decision != "Access granted.":
        return decision

    return retrieve_document(username, document_name)
