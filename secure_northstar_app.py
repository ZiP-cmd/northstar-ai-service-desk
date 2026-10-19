
# Northstar AI - Session-Bound Service Desk Demo

from session_auth import (
    create_demo_session,
    end_session
)
from secure_service import (
    get_document,
    submit_support_ticket
)
from mock_claude import mock_claude_response


def ask_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()

        if answer in ("yes", "no"):
            return answer == "yes"

        print("Please enter yes or no.")


def main():
    print("\nNORTHSTAR AI - SECURE SERVICE DESK DEMO")
    print("Mock session mode - not real SSO\n")

    # Simulation of a completed authentication event.
    # This must NOT be exposed as a public login endpoint.
    username = input(
        "Select demo employee: "
    ).strip().lower()

    try:
        token = create_demo_session(username)
    except ValueError:
        print("Unknown demo employee.")
        return

    try:
        document = input(
            "Enter document name: "
        ).strip()

        question = input(
            "Describe your IT question: "
        ).strip()

        if not question:
            print("Question cannot be empty.")
            return

        content, error = get_document(token, document)

        if error:
            print("\n", error)
            return

        response = mock_claude_response(
            question, content
        )

        print("\nNORTHSTAR AI RESPONSE:")
        print(response)

        resolved = ask_yes_no(
            "\nWas your issue resolved? (yes/no): "
        )

        if resolved:
            print("Support session completed.")
            return

        print("\nProposed ticket:")
        print("Issue:", question)

        confirmed = ask_yes_no(
            "Create this ticket? (yes/no): "
        )

        ticket, error = submit_support_ticket(
            token,
            question,
            confirmed=confirmed
        )

        if error:
            print(error)
            return

        print("\nSupport ticket created!")
        print("Ticket ID:", ticket["ticket_id"])
        print("Employee:", ticket["employee"])
        print("Status:", ticket["status"])

    finally:
        end_session(token)


if __name__ == "__main__":
    main()
