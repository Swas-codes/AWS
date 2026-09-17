# LaunchLens Backend

AI-powered pre-launch customer discovery backend built with FastAPI, PostgreSQL, Redis, and integrated with n8n + OpenClaw for agentic research.

## Architecture

```
React Frontend → FastAPI Backend → PostgreSQL + Redis → n8n → OpenClaw
```

### FastAPI (this project)
- REST API, validation, auth, database operations
- Deterministic lead scoring
- Callback ingestion from n8n/OpenClaw

### n8n (orchestration layer)
- Workflow orchestration, API integrations, retries, scheduling

### OpenClaw (research/agent layer)
- Research planning, search strategy, reasoning, signal extraction

## Setup

### Prerequisites
- Python 3.12+
- PostgreSQL (or use SQLite for local dev)
- Redis (optional — graceful degradation)

### Installation

```bash
cd backend

# Create virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

**Required:** `DATABASE_URL` must be explicitly set. No silent fallback.

```env
# PostgreSQL (recommended)
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/launchlens

# SQLite (for local development)
DATABASE_URL=sqlite:///./launchlens.db
```

### Database

```bash
# Run migrations
alembic upgrade head

# Generate new migration after model changes
alembic revision --autogenerate -m "description"
```

### Run

```bash
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

## API Endpoints

### Health
| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check (API + DB + Redis) |

### Products
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/products/` | Create product |
| GET | `/api/products/` | List products |
| GET | `/api/products/{id}` | Get product |
| PUT | `/api/products/{id}` | Update product |
| DELETE | `/api/products/{id}` | Delete product |

### Research
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/research/` | Trigger research (async) |
| GET | `/api/research/` | List research runs |
| GET | `/api/research/{id}` | Poll status + progress |
| POST | `/api/research/{id}/callback` | n8n/OpenClaw callback (secured) |
| GET | `/api/research/{id}/leads` | Leads for a run |
| GET | `/api/research/{id}/segments` | Segments for a run |
| GET | `/api/research/{id}/report` | Research report |

### Leads
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/leads/` | List leads (filter: min_score, segment, source) |
| GET | `/api/leads/{id}` | Get lead with evidence |
| POST | `/api/leads/` | Create lead manually |
| POST | `/api/leads/{id}/evidence` | Add evidence to lead |

### Segments
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/segments/` | List segments |
| GET | `/api/segments/{id}` | Get segment |
| POST | `/api/segments/` | Create segment manually |

## Testing

```bash
pytest tests/ -v
```

## Database Schema

```
Product → ResearchRun → Lead → Evidence
                      → Segment
                      → ResearchReport
```

## Scoring

Deterministic weighted scoring (OpenClaw extracts → FastAPI computes):

```
overall_score = 0.35 × problem_fit
              + 0.25 × intent_level
              + 0.20 × persona_fit
              + 0.20 × evidence_strength
```
