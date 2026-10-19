
# Northstar AI - Mock IT Ticket System

import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from access_control import employees


# Location of our local ticket database
TICKET_FILE = Path(__file__).with_name("tickets.json")


def create_ticket(username, issue):
    """
    Create a support ticket for a recognized employee.

    Prototype storage function.
    Real applications must enforce authenticated
    identity and authorization in the service layer.
    """

    if username not in employees:
        return None, "Unknown employee."

    if not isinstance(issue, str) or not issue.strip():
        return None, "Issue description cannot be empty."

    # Create the ticket
    ticket = {
        "ticket_id": "NST-" + uuid4().hex[:12].upper(),
        "employee": username,
        "issue": issue.strip(),
        "status": "Open",
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    # Load existing tickets
    if TICKET_FILE.exists():
        with TICKET_FILE.open("r", encoding="utf-8") as file:
            tickets = json.load(file)
    else:
        tickets = []

    # Add our new ticket
    tickets.append(ticket)

    # Save updated records
    with TICKET_FILE.open("w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4)

    return ticket, None


if __name__ == "__main__":
    print("Northstar AI - Ticket System")
    print("Run the secure ticket approval demo to create a ticket.")
