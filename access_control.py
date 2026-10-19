
# Northstar AI - Access Control Prototype

# Fictional employees and their assigned roles
employees = {
    "james": "employee",
    "sarah": "it_support",
    "michelle": "hr_manager"
}

# Document classifications and permitted roles
documents = {
    "vpn_guide": {
        "allowed_roles": ["employee", "it_support", "hr_manager"]
    },
    "it_policy": {
        "allowed_roles": ["employee", "it_support", "hr_manager"]
    },
    "salary_report": {
        "allowed_roles": ["hr_manager"]
    }
}


def check_access(username, document_name):
    # Simulates looking up an authenticated user.
    # Production systems must validate identity through
    # a trusted authentication provider.
    role = employees.get(username)

    if role is None:
        return "Access denied: Unknown user."

    document = documents.get(document_name)

    if document is None:
        return "Document not found."

    if role not in document["allowed_roles"]:
        return "Access denied: Insufficient permissions."

    return "Access granted."


if __name__ == "__main__":
    print(check_access("james", "salary_report"))
    print(check_access("michelle", "salary_report"))
    print(check_access("james", "vpn_guide"))
