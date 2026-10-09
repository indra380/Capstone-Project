# Project 15 Stack and Technologies

## Project Context
Project 15 is Project Management: The AI Project Manager.
The system must support planning, resource allocation, progress tracking, risk assessment, communication, and supervisor orchestration.

## 1. Recommended Primary Stack

### Frontend
- Framework: Next.js 14 (React + App Router)
- Language: TypeScript
- UI: Tailwind CSS + shadcn/ui
- Data Fetching: TanStack Query
- Form Handling: React Hook Form + Zod

Why:
- Fast development and clean component architecture.
- Type safety across UI and API contracts.
- Strong dashboard and admin panel support.

### Backend
- Framework: FastAPI (Python)
- Language: Python 3.11+
- API Style: REST (with optional WebSocket for live status)
- Validation: Pydantic v2
- Background Jobs: Celery + Redis (or FastAPI BackgroundTasks for MVP)

Why:
- Excellent for AI-heavy services and structured outputs.
- Fast API development with built-in docs and validation.
- Easy integration with orchestration and LLM layers.

### AI Orchestration and LLM Layer
- Orchestration: LangGraph
- LLM SDK: LangChain
- Model Provider: OpenAI API (GPT-4.1 or newer equivalent available in your org)
- Prompt Management: Versioned prompt templates in repo
- Output Reliability: Structured JSON outputs + schema validation + retry policy

Why:
- LangGraph fits supervisor-style multi-feature workflows.
- Clear state transitions for planning to communication lifecycle.
- Better control over deterministic execution and observability.

### Data and Storage
- Primary Database: Supabase Postgres
- ORM/Query: SQLModel or SQLAlchemy
- Optional Vector Store: pgvector (inside Supabase)
- Caching and Queue: Redis

Why:
- Strong relational modeling for projects, tasks, risks, and reports.
- Easy managed database + authentication options.
- pgvector enables future retrieval-based enhancements.

### Authentication and Authorization
- Auth: Supabase Auth or Auth0
- Authorization: RBAC (Project Manager, Team Lead, Team Member, Stakeholder)
- Session: JWT with role claims

Why:
- Secure access control aligned with governance requirements.
- Straightforward integration with web and API layers.

### Notifications and Communication
- Email: SendGrid or Resend
- Team Notifications: Slack API or Microsoft Teams webhook
- Scheduler: APScheduler / Celery beat

Why:
- Supports automated daily and weekly updates.
- Enables risk and blocker escalation workflows.

## 2. Development and Quality Tooling

### Code Quality
- Python Lint/Format: Ruff + Black
- Type Checking: mypy
- TS Lint/Format: ESLint + Prettier
- Commit Quality: Conventional Commits + pre-commit hooks

### Testing
- Backend Tests: Pytest
- Frontend Tests: Vitest + React Testing Library
- API Contract Tests: Schemathesis or Postman collections
- End-to-End Tests: Playwright

### Observability
- Logging: Structured JSON logging (loguru or standard logging formatter)
- Monitoring: OpenTelemetry + Grafana/Prometheus (or Sentry for MVP)
- Audit Logs: Database table for critical actions and AI overrides

## 3. Deployment and Environment

### Environments
- Local: Docker Compose (API, UI, Redis, worker)
- Staging: Cloud deployment for UAT
- Production: Managed cloud environment

### Hosting Options
- Frontend: Vercel
- Backend: Render, Railway, or Azure App Service
- Database: Supabase managed Postgres
- Redis: Upstash Redis or managed Redis service

### CI/CD
- GitHub Actions pipeline:
  - Lint and test
  - Build frontend and backend
  - Run migration checks
  - Deploy to staging/production with approval gates

## 4. Security and Governance Stack
- Secrets: Environment variables via secure secret manager
- Encryption: TLS in transit, provider encryption at rest
- Access Controls: RBAC and protected admin routes
- Compliance Support:
  - Audit trail for AI recommendations and manual overrides
  - Report snapshot retention
  - Access log visibility

## 5. Technology Mapping to Core Features
- Planning Feature: FastAPI + LangGraph + OpenAI + Postgres
- Resource Allocation Feature: Python rules engine + Postgres + Redis cache
- Progress Tracking Feature: FastAPI + WebSocket/REST + Postgres
- Risk Assessment Feature: LangGraph node + scoring heuristics + Postgres
- Communication Feature: Scheduler + LLM summary + SendGrid/Slack
- Supervisor Feature: LangGraph state machine + centralized orchestration logs

## 6. MVP vs Stretch Technology Scope

### MVP (Must Have)
- Next.js + FastAPI
- LangGraph + OpenAI
- Supabase Postgres
- Basic RBAC
- Email/Slack notifications
- Pytest/Vitest basic coverage

### Stretch (If Time Allows)
- pgvector for historical retrieval
- Advanced observability dashboards
- Calendar integration
- Scenario simulation for risk forecasting

## 7. Final Recommendation for Capstone
Use this stack for fastest reliable delivery in 15 days:
- Next.js + TypeScript for frontend
- FastAPI + Python for backend
- LangGraph + OpenAI for orchestration and AI features
- Supabase Postgres for persistence
- Redis for queue and cache
- SendGrid/Slack for communications
- GitHub Actions for CI/CD

This combination balances speed, clarity, production readiness, and strong demo capability for the final capstone presentation.
