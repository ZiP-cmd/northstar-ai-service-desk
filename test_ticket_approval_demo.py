
# Northstar AI - Secure Ticket Approval Demonstration

from session_auth import create_demo_session, end_session
from ticket_approval import propose_ticket, approve_ticket


def main():

    print("\n===================================")
    print(" NORTHSTAR AI - TICKET APPROVAL")
    print("       SECURE DEMO MODE")
    print("===================================\n")

    # Step 1: Create a simulated employee session
    token = create_demo_session("james")

    try:
        # Step 2: Propose a support ticket
        proposal, error = propose_ticket(
            token,
            "VPN connection not working"
        )

        if error:
            print("Proposal error:", error)
            return

        # Step 3: Display ticket details
        print("Ticket preview:")
        print("Employee:", proposal["employee"])
        print("Issue:", proposal["issue"])

        # Step 4: Request employee approval
        answer = input(
            "\nApprove this ticket? (yes/no): "
        ).strip().lower()

        if answer != "yes":
            print("\nTicket not created.")
            return

        # Step 5: Approve the proposed ticket
        ticket, error = approve_ticket(
            token,
            proposal["proposal_id"]
        )

        if error:
            print("\nApproval error:", error)
            return

        print("\nSupport ticket created successfully!")
        print("Ticket ID:", ticket["ticket_id"])
        print("Employee:", ticket["employee"])
        print("Status:", ticket["status"])

        # Step 6: Test duplicate approval protection
        print("\nTesting duplicate approval protection...")

        second_ticket, second_error = approve_ticket(
            token,
            proposal["proposal_id"]
        )

        print("Second approval result:", second_error)

    finally:
        # Step 7: End the simulated session
        end_session(token)
        print("\nDemo session ended.")


if __name__ == "__main__":
    main()
