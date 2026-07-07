# AGENTS.md – AI-Assisted Project Rules
- Use FastAPI dependency injection for all services.
- Keep API keys in .env, never frontend.
- All Setu calls go through SetuClient with retries.
- Validate files on backend (type, size).
- Use structured logging with request IDs.
- Follow repository and service pattern.
- Write tests for each endpoint.
