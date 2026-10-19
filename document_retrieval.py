
from access_control import employees, documents, check_access

# Simulated company knowledge base
knowledge_base = {
    "vpn_guide": (
        "To connect to Northstar's VPN, open the approved VPN "
        "application and sign in using your company credentials."
    ),
    "it_policy": (
        "Employees must use company-approved software and "
        "report suspicious emails to the IT department."
    ),
    "salary_report": (
        "Confidential HR salary information. "
        "Access is restricted to authorized HR personnel."
    )
}


def retrieve_document(username, document_name):
    # Check permissions BEFORE retrieving content
    access_result = check_access(username, document_name)

    if access_result != "Access granted.":
        return access_result

    return knowledge_base.get(document_name, "Document not found.")


print("\nJames requests the VPN guide:")
print(retrieve_document("james", "vpn_guide"))

print("\nSarah requests the salary report:")
print(retrieve_document("sarah", "salary_report"))

print("\nMichelle requests the salary report:")
print(retrieve_document("michelle", "salary_report"))
