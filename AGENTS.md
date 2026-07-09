# AGENTS.md – AI‑Assisted Development Rules
- All Setu API calls go through the backend.
- Use async/await for all I/O.
- Validate file type/size on backend before proxying.
- Database operations use SQLAlchemy 2.0 async syntax.
- Manage environment variables via Pydantic Settings.
