from access_control import check_access


def test_employee_can_access_vpn_guide():
    result = check_access("james", "vpn_guide")
    assert result == "Access granted."


def test_employee_cannot_access_salary_report():
    result = check_access("james", "salary_report")
    assert result == "Access denied: Insufficient permissions."


def test_hr_manager_can_access_salary_report():
    result = check_access("michelle", "salary_report")
    assert result == "Access granted."


def test_unknown_user_is_denied():
    result = check_access("unknown", "salary_report")
    assert result == "Access denied: Unknown user."


def test_unknown_document():
    result = check_access("james", "secret_document")
    assert result == "Document not found."
