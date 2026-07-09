# Architecture Decision Records

## ADR-001: Use FastAPI for Backend
**Decision**: FastAPI with Pydantic and async SQLAlchemy.

## ADR-002: Repository Pattern & Dependency Injection
**Decision**: Separate data access, business logic, and API layers.

## ADR-003: Polling over Webhooks
**Decision**: Frontend polls every 5s; simpler deployment.

## ADR-004: Backend Proxy for All Setu Communication
**Decision**: All Setu API keys stay server-side.

## ADR-005: Mock Setu Client When Sandbox Unavailable
**Decision**: Implement a mock client to simulate the full flow.
