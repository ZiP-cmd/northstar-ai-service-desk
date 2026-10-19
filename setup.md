# Northstar AI — Installation and Setup

## Requirements

- Python 3.15 (version used in local development)
- Git
- Windows PowerShell for the commands below

## Installation

Clone the repository:

```powershell
git clone YOUR_REPOSITORY_URL
cd northstar-ai-service-desk
```

Create a virtual environment:

```powershell
py -3.15 -m venv .venv
```

Install dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Run the automated tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/ -v
```

Launch the web interface:

```powershell
.\.venv\Scripts\python.exe -m streamlit run portfolio_app.py --server.address 127.0.0.1
```

Open the local address displayed by Streamlit.

## Demo Accounts

The local prototype provides fictional employee identities:

- `james` — Employee
- `sarah` — IT Support
- `michelle` — HR Manager

Employee selection is simulated authentication and must not be used as a real sign-in system.

## Example Workflow

Select James, retrieve the VPN instructions, indicate the issue remains unresolved, review the ticket proposal, and approve ticket creation.

The application uses simulated AI responses rather than the live Claude API.

## Notes

SQLite databases are created locally and are excluded from version control. This prototype is intended for local demonstration only.
