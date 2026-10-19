
# Northstar AI - Session Security Demonstration

from session_auth import (
    create_demo_session,
    end_session
)
from secure_retrieval import secure_retrieve


# Simulate a successful login for Sarah.
# This is a trusted TEST FIXTURE, not real SSO.
sarah_session = create_demo_session("sarah")

print("\nTEST 1: Sarah requests confidential HR data")
print(secure_retrieve(sarah_session, "salary_report"))

print("\nTEST 2: Sarah requests the VPN guide")
print(secure_retrieve(sarah_session, "vpn_guide"))

print("\nTEST 3: Invalid session attempts retrieval")
print(secure_retrieve("invalid-session", "salary_report"))

print("\nTEST 4: Sarah logs out")
end_session(sarah_session)

print(secure_retrieve(sarah_session, "vpn_guide"))
