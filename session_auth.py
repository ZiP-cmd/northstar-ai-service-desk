
# Northstar AI - Mock Server-Side Session Management
# Educational prototype, NOT production authentication.

import secrets
from access_control import employees

# In-memory server-side sessions.
# Real applications need a secure persistent session store.
active_sessions = {}


def create_demo_session(username):
    """
    Simulates a successfully authenticated login.
    WARNING: Does not verify an employee's identity.
    Never expose this function as a public login endpoint.
    """
    if username not in employees:
        raise ValueError("Unknown employee.")

    token = secrets.token_urlsafe(32)
    active_sessions[token] = username

    return token


def get_authenticated_username(session_token):
    """
    Look up the identity bound to a session token.
    Reject missing or unrecognized sessions.
    """
    if not isinstance(session_token, str):
        return None

    return active_sessions.get(session_token)


def end_session(session_token):
    """Invalidate a demo session."""
    active_sessions.pop(session_token, None)
