
# Northstar AI - Cached Authorization Demo

from access_control import documents, employees
from document_retrieval import knowledge_base
from permission_cache import PermissionCache
from session_auth import get_authenticated_username

# Simulates an authoritative employee role directory.
# In production, this would be a trusted service.
directory = employees.copy()

cache = PermissionCache(
    role_provider=lambda username: directory.get(username),
    ttl_seconds=300
)


def retrieve_with_fresh_permissions(
    session_token, document_name
):
    username = get_authenticated_username(session_token)

    if username is None:
        return "Access denied: Invalid session."

    # Refresh role when the authorization cache expires.
    role = cache.get_role(username)

    if role is None:
        return "Access denied: Role unavailable."

    document = documents.get(document_name)

    if document is None:
        return "Document unavailable or access denied."

    if role not in document["allowed_roles"]:
        return "Access denied: Insufficient permissions."

    return knowledge_base.get(
        document_name,
        "Document content unavailable."
    )
