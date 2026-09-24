# CodeMentor AI & SAP S/4HANA Guided Learning Platform

Production-grade, dual-curriculum AI engineering platform:
1. **160-Day Python & DSA Curriculum**: 16 foundational and advanced topics (14 core curriculum sections), 178 curated LeetCode-style algorithmic challenges across 5 difficulty tiers (148 mapped directly to daily practice), Socratic AI Teacher, pgvector semantic memory, and zero-trust sandbox execution.
2. **100-Day Enterprise SAP S/4HANA & ABAP Cloud Curriculum**: 9 architectural phases, 100 authored daily lessons with 8-step pedagogical structures, 33 interactive enterprise business missions, ECC-to-S/4HANA architectural shifts, In-Memory HANA, ACDOCA Universal Journal, MATDOC, CDS views & VDM, Clean Core extensibility, ABAP RESTful Application Programming (RAP), and final Enterprise Capstone defense.

```
Next.js 15 (App Router)  ──HTTP (Cookies)──▶  FastAPI (Backend)  ──▶  Zero-Trust Sandbox
                                                  │
                                                  ├──▶  PostgreSQL 16 + pgvector (Vector RAG)
                                                  ├──▶  Redis 7 (Distributed Rate Limiting)
                                                  ├──▶  SAP Curriculum Knowledge Engine (DAG)
                                                  └──▶  LLM Services (Nemotron / Claude / GPT)
```

---

## Architecture & Technology Stack

- **Frontend**: Next.js 15.5 (15 App Router pages, React 19, TypeScript strict mode, Tailwind CSS, Monaco Editor).
- **Backend**: FastAPI (57 OpenAPI route paths, 59 HTTP operations), SQLAlchemy 2.0, Pydantic v2, Alembic migrations.
- **Databases**:
  - **PostgreSQL 16 + pgvector**: Relational data, user progression, dual-mode enterprise state, and vector embeddings for semantic review memory.
  - **Redis 7**: Distributed sliding-window rate limiting on execution, AI tutor chats, and problem generation.
- **Authentication**: Server-authoritative HttpOnly JWT session cookies (`access_token`) with SameSite=Lax protection and CSRF mitigation. Optional Bearer header supported for programmatic API clients.
- **Code Execution Sandbox**: Subprocess isolation with cross-platform memory tracking (RSS/working set), CPU deadlines, network namespace isolation (`unshare -n`), and output streaming capped at 64 KiB.

---

## Local Development Setup

### 1. Infrastructure Services (Docker)

```bash
docker compose up -d                      # PostgreSQL 16 (port 5433) + Redis 7 (port 6379)
```

*Note: PostgreSQL is exposed on host port `5433` (mapped from container port `5432`) to prevent collisions with existing system PostgreSQL instances.*

### 2. Backend (FastAPI)

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env

# Run database migrations and seed data
python -m alembic upgrade head
python -m app.seed                        # Seeds 16 topics, 178 practice problems
uvicorn app.main:app --reload             # http://localhost:8000/docs
```

### 3. Frontend (Next.js)

```bash
cd frontend
npm install
cp .env.local.example .env.local          # BACKEND_URL=http://localhost:8000
npm run dev                               # http://localhost:3000
```

---

## Curriculum Overview

### 1. Python & DSA Masterclass (160 Days)
- **Topics (16)**: Arrays & Hashing, Two Pointers, Strings, Stacks & Queues, Binary Search, Graphs & Trees, Python Basics, Linked Lists, Trees & BST, Heaps & Priority Queues, Searching & Sorting, Hashing, Greedy Algorithms, Dynamic Programming, Bit Manipulation, Advanced DSA & Capstone.
- **Problem Distribution (178)**: Tier 1 (35), Tier 2 (56), Tier 3 (48), Tier 4 (29), Tier 5 (10). 148 problems are mapped to daily practice; the remainder serve adaptive difficulty remediation.
- **Server-Authoritative Progression**: Progress is recorded day-by-day. Solving a practice problem credits only the intended, accessible day without pre-marking future locked days.
- **Pedagogical Experience**: 4-part daily lessons with interactive code sandboxes, Socratic AI Teacher guidance, and adaptive LeetCode-style problem recommendations.

### 2. SAP S/4HANA & ABAP Cloud Enterprise Track (100 Days)
- **Phase 1 (Days 1–8)**: Enterprise ERP Foundations & Architecture.
- **Phase 2 (Days 9–22)**: S/4HANA Core Innovations (In-Memory HANA, ACDOCA, MATDOC, Business Partner / CVI, CTS Landscapes).
- **Phase 3 (Days 23–44)**: Core End-to-End Business Processes (P2P, O2C, Record-to-Report, Inventory, Manufacturing).
- **Phase 4 (Days 45–54)**: Core Data Services (CDS) & Virtual Data Models (VDM).
- **Phase 5 (Days 55–64)**: SAP Fiori & Modern User Experience (Fiori Elements, SAPUI5, Flexible Programming Model).
- **Phase 6 (Days 65–76)**: S/4HANA Cloud & Clean Core Extensibility (Key-User, On-Stack Developer Extensibility, Side-by-Side BTP).
- **Phase 7 (Days 77–89)**: ABAP RESTful Application Programming Model (RAP) (Managed, Unmanaged, Draft, Determinations, Validations, Actions).
- **Phase 8 (Days 90–95)**: Enterprise Integration & Business Technology Platform (BTP) (Integration Suite, Event Mesh, Cloud Connector).
- **Phase 9 (Days 96–100)**: Full Enterprise Capstone Project & Architectural Defense (Nova Manufacturing Corp digital twin).
- **Missions (33)**: Interactive multi-step business missions across Phases 1–4 testing realistic enterprise ERP configuration and code.

---

## Test Suites & Quality Gates

The codebase enforces strict end-to-end verification gates:

### Backend Testing (Pytest)
```bash
cd backend
# Run full unit and integration test suite
$env:TEST_DATABASE_URL="postgresql+psycopg://codementor:codementor@localhost:5433/codementor"
python -m pytest tests -q                 # 368 tests passing (0 failed, 0 skipped)
```

Key test modules:
- `tests/test_sap_metadata_consistency.py`: Asserts zero discrepancies between curriculum manifest and authored lessons across all 100 days.
- `tests/test_sandbox.py`: Zero-trust code execution, 64 KiB output truncation, Win32 Job Object / POSIX rlimit enforcement, and RSS physical memory bounds (19 tests).
- `tests/test_batch4_adversarial.py`: Anti-abuse rate limits, open redirect validation, and problem generation truthfulness.
- `tests/test_sap_progression_gating.py`: Server-authoritative milestone unlock rules and diagnostic placement waivers.
- `tests/test_cookie_cors_production.py`: HttpOnly cookie transport, CSRF protection, and CORS production validation.

### Frontend Verification
```bash
cd frontend
npx tsc --noEmit                          # Strict TypeScript typechecking (0 errors)
npm run build                             # Next.js 15 production static page optimization (15 routes generated)
```

### End-to-End Browser Testing (Playwright)
```bash
cd frontend
# Run Playwright tests against production build (17 tests total across 2 suites)
npm run start                             # Runs built frontend on port 3000
npx playwright test e2e/codementor-integration.spec.ts   # 8 tests passing
npx playwright test e2e/sap-ux-gating.spec.ts            # 9 tests passing
```

---

## Production Deployment

- **Backend**: Containerized FastAPI service on Render / Railway / AWS ECS. Set `ENVIRONMENT=production`, configure managed PostgreSQL + Redis URLs, and ensure `CORS_ORIGINS` points strictly to the frontend origin.
- **Frontend**: Next.js App Router deployed on Vercel or containerized with standalone output. Set `BACKEND_URL` to route API proxy requests safely with HttpOnly cookie support.

