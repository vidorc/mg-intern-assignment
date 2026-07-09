🚀 MG eSign – Full‑Stack Setu eSign Integration

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-16.2+-black.svg?logo=next.js&logoColor=white)](https://nextjs.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3-blue.svg?logo=sqlite&logoColor=white)](https://sqlite.org/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production‑grade demo integrating **Setu’s Aadhaar eSign APIs** through a secure backend proxy. Built with **FastAPI**, **Next.js 16**, **SQLite**, and **Docker**. This project was developed as part of the **Mango Giraffe SDE Intern Assignment** and demonstrates clean architecture, security best practices, and polished UI/UX.

---

## 📑 Table of Contents
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [API Endpoints](#-api-endpoints)
- [Project Structure](#-project-structure)
- [Documentation](#-documentation)
- [UI/UX Highlights](#-uiux-highlights)
- [Security](#-security)
- [Deployment](#-deployment)
- [AI‑Assisted Workflow](#-ai-assisted-workflow)
- [Future Improvements](#-future-improvements)
- [License](#-license)

---

## 🧱 Architecture

```
Browser (Next.js) → Backend (FastAPI) → Setu eSign APIs (simulated via Mock)
                          ↓
                    SQLite (or PostgreSQL)
```

- **Frontend:** Next.js 16 (App Router), Tailwind CSS, shadcn/ui, Sonner, React Hook Form + Zod
- **Backend:** FastAPI (async), SQLAlchemy 2.0 (async), Alembic, Pydantic, tenacity, slowapi
- **Database:** SQLite (development) → PostgreSQL (production) via Neon
- **External Service:** Setu eSign sandbox (mock client used when sandbox credentials unavailable)

The backend acts as a secure proxy – all Setu API keys stay server‑side in `.env`. The frontend never communicates directly with Setu.

---

## ⚡ Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- (Optional) Docker & Docker Compose

### 1. Clone the repository
```bash
git clone https://github.com/vidorc/mg-intern-assignment.git
cd mg-intern-assignment
```

### 2. Backend setup
```bash
cd backend
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # Fill in your Setu sandbox credentials (or leave defaults for mock)
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend setup
```bash
cd frontend
npm install
npm run dev
```

### 4. Open your browser
- Frontend: [http://localhost:3000](http://localhost:3000)
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Health check: [http://localhost:8000/api/health](http://localhost:8000/api/health)

> **Note:** The project includes a **Mock Setu Client** so you can test the full flow without real sandbox credentials. To use the real Setu API, fill in the actual keys in `backend/.env` and remove the mock client from `app/clients/setu_client.py`.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/upload-contract` | Upload a PDF, create a signature request |
| `GET` | `/api/signature-status/{signature_id}` | Get the current signature status |
| `GET` | `/api/download/{signature_id}` | Download the signed PDF |
| `GET` | `/api/signatures` | List recent signature requests (for dropdown) |
| `GET` | `/api/health` | Basic health check |
| `GET` | `/api/ready` | Database connectivity check |
| `GET` | `/api/live` | Setu connectivity check (mock always returns true) |

All responses follow a consistent structure:
```json
{
  "success": true,
  "message": "Operation completed",
  "data": { ... }
}
```

---

## 📁 Project Structure

```
mg-intern-assignment/
├── backend/
│   ├── app/
│   │   ├── api/                 # Route handlers
│   │   ├── clients/             # Setu API client (mock or real)
│   │   ├── core/                # Config, exceptions, logging, middleware
│   │   ├── db/                  # Async SQLAlchemy engine & session
│   │   ├── models/              # SQLAlchemy ORM models
│   │   ├── repositories/        # Database access layer
│   │   ├── schemas/             # Pydantic request/response schemas
│   │   ├── services/            # Business logic
│   │   └── utils/               # Rate limiting, helpers
│   ├── alembic/                 # Database migrations
│   ├── tests/                   # pytest tests
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/                 # Next.js App Router pages
│   │   ├── components/          # shadcn/ui components, navbar, theme provider
│   │   └── lib/                 # API helper, utility functions
│   └── ...
├── docs/                        # PRD, Architecture, ADRs
├── postman/                     # Postman collection
├── docker-compose.yml
├── Makefile
├── AGENTS.md                    # AI‑assisted development rules
├── CLAUDE.md                    # Project context for AI tools
└── README.md
```

---

## 📚 Documentation

- 📖 [Product Requirements Document (PRD)](docs/PRD.md)
- 🏗 [Architecture Document](docs/ARCHITECTURE.md)
- 📋 [Architecture Decision Records (ADRs)](docs/DECISIONS.md)
- 🤖 [AI‑Assisted Development Rules](AGENTS.md)
- 🧠 [Project Context for AI](CLAUDE.md)

---

## 🎨 UI/UX Highlights

- **Dark mode** toggle (using `next-themes`)
- **Drag‑and‑drop** PDF upload with file type & size validation
- **Progress bar** & **spinner** during API calls
- **Real‑time polling** (status checks every 5 seconds)
- **Previous requests dropdown** (fetched from database)
- **Friendly error states** (e.g., "Signature Not Found" with icon)
- **Toast notifications** for success/error feedback
- **Responsive design** (mobile‑friendly)

---

## 🔒 Security

- **All Setu API calls happen server‑side** – the frontend never sees API keys.
- **File validation** on the backend (type: PDF, size: <5 MB).
- **Rate limiting** on the upload endpoint (5 requests per minute).
- **CORS** restricted to the frontend origin.
- **Structured JSON logging** with request‑IDs for audit trails.

### Secrets Management in Production
For local development, Setu API keys are stored in a `.env` file (excluded from Git). In a production environment, these secrets would be injected at runtime using a managed secrets store such as **AWS Secrets Manager**, **Google Cloud Secret Manager**, or **HashiCorp Vault**. The application would retrieve them during startup, ensuring credentials are never exposed in configuration files or environment dumps.

---

## 🚀 Deployment

| Component | Platform | Notes |
|-----------|----------|-------|
| Frontend  | **Vercel** | Set `NEXT_PUBLIC_API_URL` to backend URL |
| Backend   | **Railway / Render** | Set `DATABASE_URL` and Setu keys in environment variables |
| Database  | **Neon (PostgreSQL)** | For production; SQLite file used for local demo |

---

## 🤖 AI‑Assisted Workflow

This project was built with the help of **AI tools** (Claude, Gemini, Cursor). The following practices were followed:

- **AGENTS.md** defines coding standards and architecture rules for AI assistants.
- **CLAUDE.md** provides project context so AI can quickly resume work.
- **PROMPTS.md** (coming soon) documents actual prompts and manual adjustments.
- All AI‑generated code was reviewed, tested, and understood before inclusion – no unedited code was submitted.

---

## 🔮 Future Improvements

- [ ] Webhook support for real‑time status updates (replace polling)
- [ ] Authentication & multi‑user support
- [ ] Background workers (Celery) for async upload processing
- [ ] Redis caching for frequent status checks
- [ ] Comprehensive integration tests with mocked Setu API
- [ ] CI/CD pipeline with automated testing and deployment

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

Built with ❤️ for the Mango Giraffe SDE Intern Assignment.
```
