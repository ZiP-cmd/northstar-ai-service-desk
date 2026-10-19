
# Northstar AI - Integrated Service Desk
# Free development version: no Claude API key required.

from access_control import employees, documents, check_access
from document_retrieval import retrieve_document
from mock_claude import mock_claude_response
from ticket_system import create_ticket


def get_available_documents(username):
    """Return documents allowed for this employee."""

    role = employees.get(username)

    if role is None:
        return []

    return [
        name
        for name, settings in documents.items()
        if role in settings["allowed_roles"]
    ]


def ask_yes_no(prompt):
    """Require an explicit yes or no answer."""

    while True:
        answer = input(prompt).strip().lower()

        if answer in ("yes", "no"):
            return answer

        print("Please enter yes or no.")


def start_service_desk():
    print("\n=================================")
    print(" NORTHSTAR AI - IT SERVICE DESK")
    print("       MOCK DEVELOPMENT MODE")
    print("=================================\n")

    # Step 1: Identify the employee
    # This is a demo lookup, NOT real authentication.
    username = input(
        "Enter employee username: "
    ).strip().lower()

    if username not in employees:
        print("Access denied: Unknown employee.")
        return

    print(f"\nWelcome, {username.title()}!")

    # Step 2: Show authorized documents
    available = get_available_documents(username)

    if not available:
        print("No documents available.")
        return

    print("\nAvailable support documents:")

    for name in available:
        print(f" - {name}")

    # Step 3: Choose a support document
    document_name = input(
        "\nEnter document name: "
    ).strip()

    if document_name not in available:
        print("Document unavailable or access denied.")
        return

    # Authorize the specific document again
    if check_access(username, document_name) != "Access granted.":
        print("Access denied.")
        return

    # Step 4: Get the employee's question
    question = input(
        "\nDescribe your issue or question: "
    ).strip()

    if not question:
        print("Question cannot be empty.")
        return

    # Step 5: Retrieve authorized information
    context = retrieve_document(username, document_name)

    if context in (
        "Access denied: Unknown user.",
        "Access denied: Insufficient permissions.",
        "Document not found.",
        "Document content unavailable."
    ):
        print(context)
        return

    # Step 6: Simulate the AI response
    response = mock_claude_response(question, context)

    print("\nNORTHSTAR AI RESPONSE:")
    print("-----------------------------")
    print(response)

    # Step 7: Determine whether the issue is resolved
    resolved = ask_yes_no(
        "\nDid this resolve your issue? (yes/no): "
    )

    if resolved == "yes":
        print("\nGlad we could help!")
        print("Support session completed.")
        return

    # Step 8: Offer ticket escalation
    print("\nWe can create an IT support ticket.")

    issue = question

    print("\nTicket preview:")
    print("Employee:", username)
    print("Issue:", issue)

    confirm = ask_yes_no(
        "\nCreate support ticket? (yes/no): "
    )

    if confirm != "yes":
        print("\nTicket creation cancelled.")
        return

    # Step 9: Create the ticket
    ticket, error = create_ticket(username, issue)

    if error:
        print("Ticket creation failed:", error)
        return

    print("\nSUPPORT TICKET CREATED")
    print("-----------------------------")
    print("Ticket ID:", ticket["ticket_id"])
    print("Status:", ticket["status"])
    print("Employee:", ticket["employee"])

    print("\nYour request has been saved.")


if __name__ == "__main__":
    start_service_desk()
