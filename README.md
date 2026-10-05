# HelioSL

**Agentic AI renewable-energy intelligence and decision support for Sri Lanka**

HelioSL brings electricity consumption, rooftop-solar generation, bill import,
weather context, trusted local knowledge, financial planning, and explainable AI
into one secure web application for households and businesses.

> HelioSL is a decision-support and academic research system. It does not replace
> a qualified electrical professional, solar engineer, financial adviser, utility,
> or regulator. Planning outputs are estimates based on the supplied assumptions;
> they are not quotations, guarantees, or claims about current Sri Lankan tariffs.

## Contents

- [Why HelioSL](#why-heliosl)
- [Product capabilities](#product-capabilities)
- [How HelioSL AI works](#how-heliosl-ai-works)
- [Technology](#technology)
- [Repository structure](#repository-structure)
- [Quick start](#quick-start)
- [Demo accounts](#demo-accounts)
- [Knowledge ingestion](#knowledge-ingestion)
- [API and application URLs](#api-and-application-urls)
- [Testing](#testing)
- [Evaluation](#evaluation)
- [Security and Responsible AI](#security-and-responsible-ai)
- [Known limitations](#known-limitations)
- [Academic context](#academic-context)

## Why HelioSL

Energy information is commonly split across electricity bills, inverter portals,
weather services, regulatory documents, and installer proposals. HelioSL turns
that fragmented information into a traceable workflow that helps a user:

- understand electricity-consumption and solar-generation trends;
- import a text-based electricity bill and confirm extracted values;
- explore solar capacity and financial scenarios without hidden assumptions;
- ask natural-language questions grounded in personal records and trusted sources;
- see which specialist agents, sources, safety checks, and limitations shaped an
  answer; and
- keep household and business records isolated behind authenticated `/me`
  endpoints.

## Product capabilities

### Public experience

- Business-level landing page describing the problem and product value.
- First-visit Solar Path Finder using a selected city, never live location.
- Preliminary scheme direction, capacity band, next step, and provider-discovery
  guidance.
- Guided Get Started flow, responsive registration, and responsive login.

### Authenticated workspace

- **Overview** — integrated user, energy, solar, trend, alert, weather, and tips
  summary.
- **Energy** — energy profile and monthly consumption history.
- **Import Bill** — authenticated PDF, TXT, or CSV extraction with confidence,
  warnings, editable results, and explicit confirmation before saving.
- **Solar** — system details and monthly generation records.
- **Solar Planner** — energy and financial scenario calculations with household,
  business, and custom assumptions.
- **HelioSL AI** — persistent, scrollable conversation with live agent execution,
  suggested follow-up questions, sources, confidence, safety notes, and traces.
- **Settings** — user profile review and update.
- **Upgrade** — Alpha, Home Pro, and Business Pro product concepts for future
  commercialization.

The bill importer does not retain the original uploaded file. The initial release
supports text-based documents; scanned-image bills require a future OCR stage.

## How HelioSL AI works

```text
Authenticated question
        |
        v
Prompt injection guard
        |
        v
NLP intent and entity extraction
        |
        v
Orchestrator selects specialist agents
        |
        v
Energy -> Weather -> Knowledge -> Financial
        |
        v
Grounded response synthesis
        |
        v
Safety and verification
        |
        v
Confidence assessment + privacy redaction
        |
        v
Final answer, sources, notes, and execution trace
```

The workflow visits a predictable sequence, but unselected agents are skipped.
Progress is streamed to the frontend with Server-Sent Events.

| Component | Responsibility |
| --- | --- |
| NLP pipeline | Detects intent and extracts location, capacity, and energy values. |
| Orchestrator | Chooses only the agents required for the detected task. |
| Energy Intelligence Agent | Analyses the signed-in user's consumption and generation history. |
| Weather Intelligence Agent | Adds location-based environmental context without claiming causation. |
| Knowledge Retrieval Agent | Retrieves trusted Sri Lankan evidence from PostgreSQL and pgvector. |
| Financial Planning Agent | Calculates estimates only when the required inputs are available. |
| Safety and Verification Agent | Blocks unsafe electrical guidance and flags unsupported or overconfident claims. |

## Technology

| Layer | Main technologies |
| --- | --- |
| Frontend | Next.js 16, React 19, TypeScript, Tailwind CSS |
| Backend | FastAPI, Python, Pydantic, SQLAlchemy, Alembic |
| Database | PostgreSQL 16 with pgvector |
| AI workflow | LangGraph, local Ollama generation and embeddings |
| Retrieval | PDF extraction, chunking, vector embeddings, metadata-aware retrieval |
| Authentication | JWT, Argon2 password hashing, authenticated user-scoped services |
| Streaming | Server-Sent Events |
| Testing | Pytest, frontend linting, production build, evaluation datasets |

## Repository structure

```text
HelioSL/
├── backend/
│   ├── alembic/               # Database migrations
│   ├── app/
│   │   ├── agents/            # Orchestrator and specialist agents
│   │   ├── api/routes/        # Versioned FastAPI endpoints
│   │   ├── core/              # Configuration and database setup
│   │   ├── llm/               # Local LLM integration
│   │   ├── models/            # SQLAlchemy models
│   │   ├── nlp/               # Intent and entity extraction
│   │   ├── rag/               # Chunking, embeddings, and retrieval
│   │   ├── schemas/           # API request and response models
│   │   ├── security/          # Auth, guards, redaction, rate limits, headers
│   │   └── services/          # Application services
│   ├── evaluation/            # Datasets, evaluators, benchmarks, results
│   ├── knowledge/             # Authoritative documents and metadata
│   ├── scripts/               # Knowledge ingestion and synthetic seed data
│   └── tests/                 # Backend unit and integration tests
├── frontend/
│   ├── public/                # Static assets and synthetic sample bills
│   └── src/
│       ├── app/               # Next.js routes
│       ├── components/        # Shared UI and agent-flow components
│       ├── lib/               # API and authentication helpers
│       ├── services/          # Typed backend clients
│       └── types/             # TypeScript contracts
├── docs/                      # Demo and product-flow documentation
└── docker-compose.yml         # Local pgvector-enabled PostgreSQL
```

## Quick start

### Prerequisites

- Git
- Docker Desktop with Docker Compose
- Python 3.11 or later
- Node.js 20 or later and npm
- [Ollama](https://ollama.com/) for local AI and embeddings

The project has been developed with newer Python versions as well, but Python 3.11+
is the supported baseline.

### 1. Clone the project

```bash
git clone https://github.com/inthiiii/HelioSL.git
cd HelioSL
```

### 2. Start PostgreSQL with pgvector

```bash
docker compose up -d
docker compose ps
```

The development database is exposed on `localhost:5432` with the credentials in
`docker-compose.yml`. Do not reuse development credentials in production.

### 3. Configure and run the backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Set at least these values in `backend/.env`:

```env
DATABASE_URL=postgresql+psycopg2://heliosl:heliosl@localhost:5432/heliosl
FRONTEND_ORIGIN=http://localhost:3000
SECRET_KEY=replace-with-a-long-random-development-secret

LLM_PROVIDER=ollama
LLM_MODEL=llama3.2
OLLAMA_BASE_URL=http://127.0.0.1:11434
EMBEDDING_MODEL=nomic-embed-text
```

Never commit `backend/.env` or a real secret. Generate an appropriate secret for
each deployed environment.

Apply the schema and start the API:

```bash
alembic upgrade head
python -m uvicorn app.main:app --reload
```

Verify:

- API root: <http://127.0.0.1:8000/>
- Health: <http://127.0.0.1:8000/api/v1/health>
- Swagger: <http://127.0.0.1:8000/docs>

### 4. Configure Ollama

In another terminal:

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
ollama list
```

Keep Ollama running while using HelioSL AI, document ingestion, or retrieval
evaluation. Core energy, solar, bill, integration, and planning features do not
depend on a generated LLM answer.

### 5. Configure and run the frontend

```bash
cd frontend
npm install
```

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

Then start the application:

```bash
npm run dev
```

Open <http://localhost:3000>.

## Demo accounts

All demo identities and records are synthetic and intended only for development,
academic evaluation, and product demonstrations.

Load the primary household and business datasets:

```bash
cd backend
source .venv/bin/activate
python -m scripts.seed_demo_data
```

Load the extended Space Industries dataset separately:

```bash
python -m scripts.seed_space_industries
```

| Persona | Email | Password | Profile |
| --- | --- | --- | --- |
| Household | `household.demo@heliosl.lk` | `DemoHouse123!` | Colombo, 5 kW, 9 months |
| Business | `business.demo@heliosl.lk` | `DemoBiz123!` | Gampaha, 20 kW, 9 months |
| Space Industries | `spaceindustries@gmail.com` | `SpaceIndustries123` | Gampaha, 75 kW, 18 months |

The `.lk` demo addresses are intentional. Older `.local` addresses fail strict API
email validation with HTTP 422. See [`docs/DEMO_SCENARIOS.md`](docs/DEMO_SCENARIOS.md)
for expected trends, questions, and responsible-use guidance.

## Knowledge ingestion

Official documents belong in `backend/knowledge/documents/`, with a corresponding
entry in `backend/knowledge/metadata.json`. Metadata records source authority,
publication details, document type, and source URL.

With PostgreSQL, migrations, and Ollama running:

```bash
cd backend
source .venv/bin/activate
python scripts/ingest_knowledge.py
```

The pipeline extracts PDF text, cleans it, creates overlapping chunks, generates
embeddings with the configured model, and stores chunks and metadata in PostgreSQL
with pgvector. The vector dimension must match the configured embedding model.

Only documents that HelioSL is permitted to store and use should be added. Source
metadata must be reviewed instead of inferred from filenames.

## API and application URLs

### Frontend routes

| Route | Purpose |
| --- | --- |
| `/` | Landing page and visitor Solar Path Finder |
| `/get-started` | Guided value and registration introduction |
| `/register` | Account registration |
| `/login` | Authentication |
| `/dashboard` | Integrated overview |
| `/energy` | Consumption profile and records |
| `/energy/bills` | Electricity-bill import and confirmation |
| `/solar` | Solar system and generation records |
| `/planning` | Solar and financial scenarios |
| `/assistant` | HelioSL AI and live agent flow |
| `/settings` | Profile management |

### API groups

- `/api/v1/auth` — registration, login, current-user profile, profile update
- `/api/v1/energy/me` — user-scoped energy profile and consumption
- `/api/v1/energy/me/bills` — authenticated bill extraction
- `/api/v1/solar/me` — user-scoped solar system and generation
- `/api/v1/analytics/summary` — current-user energy intelligence
- `/api/v1/integration/summary` — integrated dashboard state
- `/api/v1/planning` — scenario and comparison calculations
- `/api/v1/knowledge/search` — protected retrieval testing
- `/api/v1/assistant/analyze` — basic NLP and LLM path
- `/api/v1/assistant/agentic` — complete multi-agent response
- `/api/v1/assistant/agentic/stream` — live execution events and final answer
- `/api/v1/health` — application and database health

Use Swagger at <http://127.0.0.1:8000/docs> to inspect the current contracts and
authorize protected requests with a JWT.

## Testing

### Backend

Run the complete suite, not only the most recently changed tests:

```bash
cd backend
source .venv/bin/activate
pytest -v
```

Tests cover models, health, NLP, orchestration, agents, planning, integration,
bill extraction, privacy, audit logging, prompt security, source trust, rate
limiting, retrieval, safety, and user-data isolation.

### Frontend

```bash
cd frontend
npm run lint
npm run build
```

### Manual end-to-end check

1. Start PostgreSQL, Ollama, the backend, and the frontend.
2. Seed the synthetic accounts.
3. Sign in as the household user and inspect Overview, Energy, Import Bill, Solar,
   Solar Planner, HelioSL AI, and Settings.
4. Sign out, sign in as a business user, and verify that business values replace
   household values.
5. Confirm that user-scoped endpoints cannot retrieve another account's records.
6. Test a normal energy question and a prompt-injection request.
7. Confirm sources, confidence, safety notes, traces, and skipped agents in the AI
   transparency panel.

## Evaluation

HelioSL includes reproducible datasets and scripts under `backend/evaluation/`.
From the activated backend environment, run:

```bash
PYTHONPATH=. python evaluation/evaluate_nlp.py
PYTHONPATH=. python evaluation/evaluate_routing.py
PYTHONPATH=. python evaluation/evaluate_retrieval.py
PYTHONPATH=. python evaluation/evaluate_answer_quality.py
PYTHONPATH=. python evaluation/benchmark_performance.py
PYTHONPATH=. python evaluation/evaluate_demo_scenarios.py
PYTHONPATH=. python evaluation/generate_report.py
```

The protected API benchmark requires the backend, database, Ollama, and a seeded
household account:

```bash
PYTHONPATH=. python evaluation/benchmark_api.py
```

Tracked outputs are written to `backend/evaluation/results/`. Retrieval evaluation
also includes a manual relevance sheet for defensible Precision@K assessment.
Answer quality is human-scored for correctness, groundedness, safety,
transparency, and relevance; it is not presented as an invented AI accuracy score.

## Security and Responsible AI

Implemented controls include:

- Argon2 password hashing and JWT authentication;
- current-user data access through `/me` endpoints;
- direct prompt-injection detection on assistant routes, including streaming;
- trusted-organization checks and indirect prompt-injection filtering for RAG;
- email and token redaction in user-sensitive generated output;
- rate limiting for expensive AI endpoints;
- security response headers;
- minimal audit events that exclude passwords, tokens, and complete prompts;
- source display and conservative confidence labels;
- missing-data, financial-uncertainty, and unsupported-knowledge warnings;
- detection and blocking of unsafe electrical guidance; and
- explicit separation of user inputs, retrieved facts, demo assumptions, and
  calculated estimates.

For production, add TLS, managed secret storage, refresh-token/session revocation,
centralized monitoring, encrypted backups, malware scanning for uploads, a formal
retention policy, and an independent security review.

## Known limitations

- Weather observations are contextual evidence and cannot establish the cause of a
  historical generation change.
- Bill import currently supports text-based PDF, TXT, and CSV files; scanned bills
  need OCR.
- Financial outputs depend on verified tariff, export, cost, yield, roof, shading,
  and scheme inputs.
- The demo planning presets are synthetic and are not current market claims.
- Local Ollama response time and answer quality depend on the machine and model.
- Knowledge quality depends on authorized, current, correctly labelled documents.
- The provider-discovery experience is preliminary guidance, not an endorsement,
  quotation, or engineering design.
- Confidence labels are conservative evidence indicators, not calibrated
  probabilities.

## Academic context

HelioSL was developed for the **Information Retrieval and Web Analytics** module as
an academic project exploring full-stack development, information retrieval,
agentic workflows, renewable-energy decision support, security, privacy, and
Responsible AI.

## License and permitted use

No open-source license is currently declared in this repository. Copyright remains
with the project contributors. Contact the repository owner before copying,
redistributing, or using the software or included documents outside the permitted
academic context.
