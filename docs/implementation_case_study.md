Northstar AI — Implementation Consulting Case Study
Project type: Independent portfolio simulation
Client: Northstar Technologies (fictional, 250 employees)
Role performed: AI implementation consultant / solutions engineer (simulated)
Status: Working local prototype; not production ready
Executive summary
Northstar AI demonstrates how a company could provide employees with role-appropriate IT guidance and escalate unresolved issues into approved support tickets. The prototype combines a Streamlit interface, Python authorization services, a fictional knowledge base, simulated AI responses, session-bound ticket proposals, and SQLite-backed idempotent ticket storage. It was built as an independent portfolio exercise, not as a client engagement or a live Claude deployment.
Client problem and intended outcomes
The fictional IT team handles repetitive VPN and company-policy inquiries and needs a consistent escalation process. The proposed solution aims to make approved guidance easier to find, restrict confidential information, and reduce duplicate or unapproved ticket creation. No actual time savings or resolution-rate improvements have been measured.
Scope and acceptance criteria
ID	Client requirement	Acceptance test
R1	Employees can retrieve permitted guidance	James receives VPN instructions
R2	Restricted HR documents are protected	Sarah is denied the salary report
R3	Authorized HR staff can retrieve HR content	Michelle receives the salary report
R4	Unresolved issues can be escalated	James reviews and approves a ticket proposal
R5	Ticket writes prevent duplicates	Reusing an idempotency key returns an existing SQLite record
R6	Changes do not break known workflows	Automated pytest regression suite


Architecture
1. Interface: Streamlit accepts fictional employee selection and IT questions.
2. Identity simulation: In-memory demo session maps a token to an employee identity; this is not real authentication.
3. Authorization: Role checks occur before retrieval; a TTL-based permission cache models permission refresh.
4. Retrieval and assistant: Python retrieves preselected, authorized sample documents, and a mock responder formats a simulated answer. No real Claude API or production RAG is currently involved.
5. Ticket approval: Server-held, session-bound proposals require confirmation. Proposals are currently stored in process memory.
6. Persistence: SQLite ticket creation uses a unique proposal ID and transaction to avoid duplicate rows for the same request. This database component has been integrated and tested locally.
Key architectural decisions and tradeoffs
Backend authorization rather than prompt-only protection. The application enforces permissions outside the model, so unauthorized content is not intentionally sent to the responder. It does not replace proper production identity verification or secure search indexing.
Mock identity and AI adapters. This avoided API costs during development and allowed testing of integration boundaries. It cannot establish that a live model would produce safe or accurate answers.
Approval separate from ticket creation. A proposal holds the original issue details and is bound to the demo session, reducing the opportunity for last-moment client-side modification. Because proposal state is in memory, server crashes and multi-instance recovery are not yet handled.
SQLite idempotency. A database uniqueness constraint and transaction prevent repeated inserts for the same proposal ID in the local implementation. Production multi-instance operation would require shared durable proposal state, atomic workflow transitions, and a suitably deployed database.
Verification evidence
The project owner reported 30 passing pytest tests and four passing Streamlit user-acceptance tests. The four UI tests covered James's authorized VPN access, Sarah's rejected HR document request, Michelle's authorized HR access, and James's approved support ticket. These results are user-reported local tests; attach fresh terminal output or CI evidence when publishing.
Production-readiness gaps
- Replace demo identity selection with validated corporate SSO and server-managed sessions.
- Integrate live Claude API and test model quality, grounding, prompt injection resilience, latency, and cost.
- Replace exact-document retrieval with permission-filtered search or RAG where justified.
- Persist approval proposals and outcomes transactionally; build crash-safe retries and authorization rechecks.
- Add audit logs, retention controls, secret management, operational monitoring, and security review.
- Validate under concurrent load and verify the full deployment topology.
Proposed business metrics (not measured)
Track percentage of inquiries resolved without escalation, median time to approved guidance, ticket duplication rate, unauthorized-access rejection, employee satisfaction, and cost per successfully resolved inquiry.
Demonstration outline (3–5 minutes)
1. Introduce the fictional IT support problem and success criteria.
2. Show James retrieving authorized VPN instructions.
3. Show Sarah denied access to the HR report and explain server-side authorization.
4. Show Michelle's permitted HR retrieval.
5. Show James reviewing and approving a support ticket; verify the saved database record.
6. Run pytest, show the reported results, and discuss the remaining production gaps.
Portfolio positioning
This exercise demonstrates translating business requirements into a modular implementation, designing permission-aware workflows, troubleshooting Python integration issues, validating behavior with automated and acceptance testing, and documenting the boundaries between a prototype and a production system.
