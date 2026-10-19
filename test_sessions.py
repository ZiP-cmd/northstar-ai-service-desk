
import pytest

from session_auth import (
    active_sessions,
    create_demo_session,
    end_session
)
from secure_retrieval import secure_retrieve


@pytest.fixture(autouse=True)
def clear_sessions():
    active_sessions.clear()
    yield
    active_sessions.clear()


def test_valid_session_allows_permitted_document():
    token = create_demo_session("sarah")
    result = secure_retrieve(token, "vpn_guide")

    assert "company VPN" in result


def test_valid_session_enforces_permissions():
    token = create_demo_session("sarah")
    result = secure_retrieve(token, "salary_report")

    assert result == (
        "Access denied: Insufficient permissions."
    )


def test_invalid_session_denied():
    result = secure_retrieve(
        "fake-session", "vpn_guide"
    )

    assert result == "Access denied: Invalid session."


def test_logged_out_session_denied():
    token = create_demo_session("sarah")
    end_session(token)

    result = secure_retrieve(token, "vpn_guide")

    assert result == "Access denied: Invalid session."
