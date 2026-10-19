Northstar AI — GitHub Publication Checklist
Before first commit
- [ ] Back up the working project.
- [ ] Make sure secure_service.py is application code and tests/test_secure_service.py contains tests.
- [ ] Include README, SETUP.md, requirements.txt, docs/IMPLEMENTATION_CASE_STUDY.md, and sanitized screenshots.
- [ ] Review dependencies in requirements.txt; keep a tested, reproducible version set.
- [ ] Confirm .gitignore excludes .venv/, .env, .env.*, __pycache__/, .pytest_cache/, *.pyc, *.db, *.db-shm, *.db-wal, tickets.json, and .streamlit/secrets.toml (allow .env.example if intended).
- [ ] Check staged files manually for tokens, secrets, personal information, and real ticket data.
- [ ] Reproduce tests and Streamlit startup in a fresh clone using documented commands.
- [ ] Run all unit/integration tests and retain the test summary as evidence.
Git commands (run locally in repository root)
</> powershell
git --version
git status
git init -b main                 # only if not already a Git repository
git add .
git diff --cached --stat
git diff --cached --name-only
# Review the actual staged file contents for secrets before the next step.
git commit -m "Prepare Northstar AI portfolio release"
Create a private, empty GitHub repository named northstar-ai-service-desk without auto-generating a README. Then use your actual GitHub repository URL:
</> powershell
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
If origin already exists, use git remote -v to inspect it rather than adding it again. Review the repository on GitHub, then change visibility to public only after the security review.
Validation evidence to publish
- [ ] New pytest output or CI results, accurate test count and date.
- [ ] Four sanitized UI screenshots with captions.
- [ ] Clear disclosure of mock AI and mock SSO.
- [ ] A short screen recording of the demo.
- [ ] Known limitations and realistic production roadmap.
