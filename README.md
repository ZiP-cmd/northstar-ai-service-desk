# Northstar AI — Intelligent IT Service Desk

**A security-focused AI service desk implementation prototype**

## Project Overview

Northstar AI is a Python-based service desk prototype designed for a fictional organization with 250 employees.

The project demonstrates how an enterprise could integrate AI-assisted knowledge retrieval with role-based access control, IT ticket automation, and employee approval workflows.

The solution includes an interactive Streamlit interface, simulated AI responses, mock employee sessions, and SQLite-backed ticket storage.

**Development status:** Functional local prototype. Not production-ready.

## Business Problem

Northstar Technologies faces repetitive IT support requests, fragmented documentation, and manual ticket escalation.

The proposed solution aims to improve access to IT guidance while enforcing information-access rules and requiring approval before performing support actions.

These are intended business benefits, not measured production outcomes.

## Key Features

- Role-based document access for employees, IT support, and HR managers
- Permission-aware retrieval of fictional company documentation
- Mock AI responses for testing without paid API access
- Simulated session-bound employee identity
- Authorization cache with expiration and refresh behavior
- Support ticket proposals and employee confirmation
- SQLite ticket storage with unique idempotency keys
- Streamlit demonstration interface
- Automated security and integration tests

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Web interface |
| pytest | Automated testing |
| SQLite | Transactional ticket storage |
| Mock AI backend | Simulated assistant responses |

## Example Demonstration Scenarios

**Scenario 1: Authorized retrieval**

James requests VPN instructions. Northstar verifies his role and returns the authorized document.

**Scenario 2: Restricted information**

Sarah, an IT support employee, requests confidential HR information. Northstar rejects the request.

**Scenario 3: HR authorization**

Michelle, an HR manager, accesses documentation permitted to her assigned role.

**Scenario 4: Support ticket escalation**

James reports an unresolved VPN issue, reviews a ticket proposal, approves it, and receives a generated ticket ID.

## Testing

The project has previously reported 30 passing automated tests covering authorization, session handling, permission-cache expiration, ticket approval, and database idempotency.

Four Streamlit user acceptance scenarios have also passed.

Test execution and results should be independently reproducible using the repository setup instructions.

## Security Architecture

The prototype demonstrates several important security principles:

- Authorization occurs before restricted document content is returned.
- Backend services derive employee identity from simulated session records rather than accepting a username for each request.
- Ticket proposals are bound to a session and contain server-stored issue details.
- Ticket storage uses a unique proposal ID to prevent duplicate database records.

## Known Limitations

- Authentication is simulated; real corporate SSO has not been integrated.
- The application does not currently use the live Claude API.
- Document retrieval is based on a small fictional knowledge base rather than production semantic search.
- Ticket proposals are held in application memory.
- The approval workflow does not yet provide crash-safe distributed recovery.
- The prototype has not undergone a production security assessment.

## Future Enhancements

- Corporate SSO integration
- Live Claude API integration
- Secure retrieval-augmented generation
- Persistent, transactionally managed ticket approval records
- Audit logging and operational monitoring
- Deployment configuration and continuous integration

## Project Purpose

This portfolio project demonstrates an end-to-end implementation process: translating business requirements into technical components, designing security controls, integrating application services, testing workflows, and documenting implementation limitations.

**All employee accounts, documents, and company scenarios are fictional.**

### Reproducibility Validation

Northstar AI was cloned from its GitHub repository into a separate directory and installed in a fresh Python virtual environment.

The automated test suite completed successfully:

- **30 tests passed**
- **0 test failures**
- **Execution time:** 2.34 seconds
- **Environment:** Windows, Python 3.15.0

One non-failing pytest warning occurred when writing temporary cache files. The application test results were unaffected.

This validation demonstrates that the automated test environment can be reproduced from the repository and its dependency configuration.
