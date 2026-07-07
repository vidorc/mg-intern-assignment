.PHONY: run migrate test lint

run:
	cd backend && uvicorn app.main:app --reload --port 8000 &
	cd frontend && npm run dev

migrate:
	cd backend && alembic upgrade head

test:
	cd backend && pytest

lint:
	cd backend && ruff check .
	cd frontend && npm run lint

docker-up:
	docker compose up -d
