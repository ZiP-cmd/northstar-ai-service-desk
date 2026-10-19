
# Northstar AI - Free Mock Claude Integration

from access_control import check_access
from document_retrieval import retrieve_document


def mock_claude_response(question, context):
    """
    Simulates an AI response using authorized
    document content. No API key required.
    """

    if not question.strip():
        return "Please enter a question."

    return (
        "[MOCK AI RESPONSE - NOT REAL CLAUDE]\n\n"
        "Based on the authorized company document:\n\n"
        f"{context}\n\n"
        "This is a simulated response for testing."
    )


def ask_northstar(username, document_name, question):

    # Validate access before retrieval
    access = check_access(username, document_name)

    if access != "Access granted.":
        return access

    # Retrieve authorized information
    context = retrieve_document(username, document_name)

    if context == "Document content unavailable.":
        return context

    # Use our free simulated response
    return mock_claude_response(question, context)


if __name__ == "__main__":

    print("\nNorthstar AI - Free Development Mode\n")

    username = input("Employee username: ").strip().lower()
    document = input("Document name: ").strip()
    question = input("Your question: ").strip()

    result = ask_northstar(username, document, question)

    print("\nNorthstar AI:\n", result)
