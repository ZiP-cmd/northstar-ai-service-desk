
# Northstar AI - Local Portfolio Demo
# Mock authentication and simulated AI responses.

import streamlit as st

from session_auth import (
    create_demo_session,
    end_session
)
from secure_service import get_document
from mock_claude import mock_claude_response
from sqlite_ticket_approval import (
    propose_ticket,
    approve_ticket_to_database
)


st.set_page_config(
    page_title="Northstar AI Service Desk",
    page_icon="🛡️",
    layout="centered"
)

st.title("🛡️ Northstar AI Service Desk")
st.caption(
    "Portfolio demonstration | Simulated identity "
    "| Mock AI | Local SQLite storage"
)

st.warning(
    "Development demonstration only. "
    "Not connected to real corporate SSO or Claude."
)

employees = ["james", "sarah", "michelle"]

employee = st.selectbox(
    "Select demo employee",
    employees
)

# Keep a session bound to the selected demo employee.
if st.session_state.get("employee") != employee:
    old_token = st.session_state.get("token")

    if old_token:
        end_session(old_token)

    st.session_state.employee = employee
    st.session_state.token = create_demo_session(employee)
    st.session_state.proposal = None
    st.session_state.response = None

st.subheader("Company knowledge base")

document = st.selectbox(
    "Choose a document",
    ["vpn_guide", "it_policy", "salary_report"]
)

question = st.text_area(
    "Describe your question or IT issue",
    placeholder="My VPN isn't connecting..."
)

if st.button("Ask Northstar", type="primary"):
    st.session_state.proposal = None
    st.session_state.response = None

    if not question.strip():
        st.error("Please enter a question.")
    else:
        content, error = get_document(
            st.session_state.token,
            document
        )

        if error:
            st.error(error)
        else:
            answer = mock_claude_response(
                question, content
            )

            st.session_state.response = answer
            st.session_state.issue = question.strip()
            st.success("Authorized document retrieved.")

if st.session_state.get("response"):
    st.subheader("Northstar response")
    st.info(st.session_state.response)

    if st.button("My issue is unresolved"):
        proposal, error = propose_ticket(
            st.session_state.token,
            st.session_state.issue
        )

        if error:
            st.error(error)
        else:
            st.session_state.proposal = proposal

if st.session_state.get("proposal"):
    proposal = st.session_state.proposal

    st.subheader("Support ticket preview")
    st.write("Employee:", proposal["employee"])
    st.write("Issue:", proposal["issue"])

    if st.button("Approve and create ticket"):
        ticket, error = approve_ticket_to_database(
            st.session_state.token,
            proposal["proposal_id"]
        )

        if error:
            st.error(error)
        else:
            st.success(
                f"Ticket created: {ticket['ticket_id']}"
            )

        st.session_state.proposal = None
