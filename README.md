# 🚀 AutoPilot Template

Your AI Command Center starter kit for the AutoPilot Hackathon.

Build an intelligent, multi-agent command center that automates business processes with AI — while keeping humans in the loop for oversight and exception handling.

---

## Quick Start (3 Steps)

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- Git

### 1. Clone & Enter
```bash
git clone <your-repo-url>
cd AutoPilot-Template
```

### 2. Configure Environment
```bash
cp .env.example .env
```
> The defaults work out of the box — `AUTH_BYPASS=true` means no Keycloak setup needed.

### 3. Start Everything
**macOS / Linux:**
```bash
make up
# or
docker compose up --build -d
```

**Windows (PowerShell):**
```powershell
docker compose up --build -d
```

### ✅ You're Running!

| Service | URL | Purpose |
|---------|-----|---------|
| 🖥️ **Frontend** | [http://localhost:3001](http://localhost:3001) | Next.js dashboard |
| ⚙️ **Backend API** | [http://localhost:8001/api/docs](http://localhost:8001/api/docs) | FastAPI Swagger docs |
| 🗄️ **PostgreSQL** | `localhost:5432` | Database (user/password) |

---

## What's Included

### Backend (FastAPI + Python)
- ✅ FastAPI with auto-generated Swagger docs
- ✅ PostgreSQL database with Alembic migrations
- ✅ Auth system with dev-mode bypass (`AUTH_BYPASS=true`)
- ✅ Audit logging middleware (every request logged)
- ✅ Items CRUD API (sample entity)
- ✅ File storage API (local or cloud)
- ✅ Role-based authorization engine

### Frontend (Next.js + React)
- ✅ Premium glassmorphic UI with Framer Motion animations
- ✅ Dashboard with stat cards and activity chart
- ✅ AI Policies page with demo data (5 sample policies)
- ✅ AI Insights page with demo data (patterns, anomalies, actions)
- ✅ AI Manager chat interface
- ✅ Workbench page
- ✅ Admin panel (users, roles)
- ✅ Settings page
- ✅ Command palette (⌘K / Ctrl+K)

### Infrastructure
- ✅ Docker Compose for one-command startup
- ✅ Hot reload in development mode
- ✅ Cross-platform (macOS, Windows, Linux)

---

## What YOU Build

This is a **starter template**. You need to connect these frontend shells to real AI logic:

| Feature | Frontend Status | Your Task |
|---------|----------------|-----------|
| **AI Manager** | ✅ Chat UI ready | Connect to your AI agent orchestration backend |
| **AI Policies** | ✅ Demo data loaded | Build the policy engine that evaluates rules at runtime |
| **AI Insights** | ✅ Demo data loaded | Build the analysis engine that generates insights from your data |
| **Workbench** | ✅ UI shell ready | Build exception routing — when AI fails, send work items here |

See **[`docs/command-center-guide.md`](docs/command-center-guide.md)** for the full architecture guide.

---

## Project Structure

```
AutoPilot-Template/
├── app/                    # Backend (FastAPI)
│   ├── main.py             # App entry point
│   ├── security.py         # Auth + AUTH_BYPASS logic
│   ├── authz.py            # Authorization engine
│   ├── models/             # SQLAlchemy models
│   ├── schemas/            # Pydantic schemas
│   ├── routers/            # API endpoints
│   ├── services/           # Business logic
│   └── core/               # Database, storage
├── frontend/               # Frontend (Next.js)
│   ├── src/app/            # Pages (dashboard, AI, admin, etc.)
│   ├── src/components/     # Reusable UI components
│   └── src/lib/            # API client, utilities
├── alembic/                # Database migrations
├── scripts/                # Seed data, utilities
├── docs/                   # Documentation
│   ├── command-center-guide.md   # ⭐ What to build
│   ├── hackathon-brief.md        # ⭐ Problem statements
│   ├── design-system-template.md # UI patterns
│   └── Audit System Guide.md     # Audit logging
├── docker-compose.yml      # Service orchestration
├── Dockerfile              # Backend container
├── Makefile                # Dev commands
└── .env.example            # Environment config
```

---

## Useful Commands

| Command | Description |
|---------|-------------|
| `make up` | Start all services |
| `make down` | Stop all services |
| `make logs-be` | Tail backend logs |
| `make logs-fe` | Tail frontend logs |
| `make reset-db` | Reset and re-seed database |
| `make migrate-create MSG='...'` | Create a new DB migration |
| `make migrate-up` | Apply pending migrations |
| `make lint` | Lint all code |
| `make test-be` | Run backend tests |

**Windows users** — if `make` isn't available:
```powershell
# Install make via Chocolatey
choco install make

# Or use docker compose directly
docker compose up --build -d
docker compose logs -f backend
docker compose down
```

---

## Key Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `AUTH_BYPASS` | `true` | Skip all auth (dev mode) |
| `AUTH_DEBUG` | `true` | Verbose auth logging |
| `APP_ENV` | `development` | Backend mode |
| `DATABASE_URL` | auto-generated | PostgreSQL connection |
| `FRONTEND_URL` | `http://localhost:3001` | CORS origin |

---

## Documentation

| Document | Purpose |
|----------|---------|
| **[Command Center Guide](docs/command-center-guide.md)** | What is a Command Center, AI Policies, Insights, Manager, Workbench |
| **[Hackathon Brief](docs/hackathon-brief.md)** | Problem statements, judging criteria |
| **[Design System](docs/design-system-template.md)** | UI component patterns, colors, spacing |
| **[Audit System](docs/Audit%20System%20Guide.md)** | Audit logging architecture |

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Backend** | Python 3.12 + FastAPI | API server |
| **Frontend** | Next.js 15 + React 19 | Web dashboard |
| **Database** | PostgreSQL 15 | Persistent storage |
| **ORM** | SQLAlchemy 2 + Alembic | Data modeling + migrations |
| **Auth** | NextAuth.js + JWT | Authentication (bypass-able) |
| **UI** | Tailwind CSS + Framer Motion | Styling + animations |
| **Containers** | Docker + Docker Compose | Development environment |
