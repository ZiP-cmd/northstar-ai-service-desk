
# Northstar AI - Automated Security and Integration Tests

import json

import pytest

from access_control import check_access
from document_retrieval import retrieve_document
from ticket_system import create_ticket
import ticket_system
import northstar_app


# SECURITY TESTS

def test_employee_can_access_vpn():
    result = check_access("james", "vpn_guide")
    assert result == "Access granted."


def test_it_support_cannot_access_salary_report():
    result = check_access("sarah", "salary_report")
    assert result == (
        "Access denied: Insufficient permissions."
    )


def test_hr_manager_can_access_salary_report():
    result = check_access("michelle", "salary_report")
    assert result == "Access granted."


def test_unknown_employee_denied():
    result = check_access("unknown_user", "vpn_guide")
    assert result == "Access denied: Unknown user."


# DOCUMENT RETRIEVAL TESTS

def test_authorized_document_retrieval():
    result = retrieve_document("james", "vpn_guide")
    assert " VPN" in result


def test_restricted_document_not_retrieved():
    result = retrieve_document("sarah", "salary_report")
    assert result == (
        "Access denied: Insufficient permissions."
    )
    assert "CONFIDENTIAL:" not in result


# TICKET CREATION TESTS

@pytest.fixture
def isolated_tickets(tmp_path, monkeypatch):
    # Redirect ticket storage to a temporary test file.
    # Real support tickets remain untouched.
    test_file = tmp_path / "tickets.json"
    monkeypatch.setattr(
        ticket_system, "TICKET_FILE", test_file
    )
    return test_file


def test_ticket_created_for_valid_employee(isolated_tickets):
    ticket, error = create_ticket(
        "james", "VPN is not connecting"
    )

    assert error is None
    assert ticket["status"] == "Open"
    assert ticket["ticket_id"].startswith("NST-")

    saved = json.loads(
        isolated_tickets.read_text(encoding="utf-8")
    )
    assert len(saved) == 1
    assert saved[0]["ticket_id"] == ticket["ticket_id"]


def test_unknown_employee_cannot_create_ticket(isolated_tickets):
    ticket, error = create_ticket(
        "unknown_user", "Cannot access VPN"
    )

    assert ticket is None
    assert error == "Unknown employee."
    assert not isolated_tickets.exists()


# END-TO-END WORKFLOW TESTS

def run_app_with_inputs(monkeypatch, answers):
    iterator = iter(answers)
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt="": next(iterator)
    )
    northstar_app.start_service_desk()


def test_resolved_issue_creates_no_ticket(
    isolated_tickets, monkeypatch, capsys
):
    run_app_with_inputs(monkeypatch, [
        "james",
        "vpn_guide",
        "How do I connect to the VPN?",
        "yes",
    ])

    output = capsys.readouterr().out
    assert "Support session completed." in output
    assert not isolated_tickets.exists()


def test_unresolved_issue_requires_confirmation(
    isolated_tickets, monkeypatch, capsys
):
    run_app_with_inputs(monkeypatch, [
        "james",
        "vpn_guide",
        "My VPN is not connecting",
        "no",
        "no",
    ])

    output = capsys.readouterr().out
    assert "Ticket creation cancelled." in output
    assert not isolated_tickets.exists()


def test_approved_ticket_is_saved(
    isolated_tickets, monkeypatch, capsys
):
    run_app_with_inputs(monkeypatch, [
        "james",
        "vpn_guide",
        "My VPN is not connecting",
        "no",
        "yes",
    ])

    output = capsys.readouterr().out
    assert "SUPPORT TICKET CREATED" in output

    saved = json.loads(
        isolated_tickets.read_text(encoding="utf-8")
    )
    assert len(saved) == 1
    assert saved[0]["employee"] == "james"


def test_restricted_request_cannot_create_ticket(
    isolated_tickets, monkeypatch, capsys
):
    run_app_with_inputs(monkeypatch, [
        "sarah",
        "salary_report",
    ])

    output = capsys.readouterr().out
    assert "Document unavailable or access denied." in output
    assert not isolated_tickets.exists()
