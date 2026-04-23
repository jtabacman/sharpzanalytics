# Sharpz V2 Backend

FastAPI async pipeline engine. Reads DNA YAMLs + venue YAMLs and executes the 8-stage simulation pipeline.

## Quick start (dev)

```bash
# From repo root
cd backend

# 1. Copy env template
cp .env.example .env.local
# Fill in: OPENROUTER_API_KEY, SHARPZ_SYNC_KEY (generate random), JWT_SECRET (generate random)

# 2. Start dependencies (Postgres + Redis)
docker compose up -d

# 3. Install deps (uv recommended)
uv sync

# 4. Run dev server
uv run uvicorn sharpz.main:app --reload --host 0.0.0.0 --port 8000

# 5. Verify
curl http://localhost:8000/health
# {"status":"ok","version":"0.1.0","env":"development"}
```

## Structure (planned)

```
backend/
├── pyproject.toml
├── docker-compose.yml
├── .env.example
├── src/sharpz/
│   ├── __init__.py
│   ├── config.py           # pydantic-settings
│   ├── main.py             # FastAPI entry
│   ├── db.py               # SQLModel async session
│   ├── models/             # DB models (Intake, Test, Environment, Persona, Action, Report, ...)
│   ├── api/                # FastAPI routers
│   │   ├── intakes.py
│   │   ├── tests.py
│   │   ├── operator.py
│   │   └── deliverables.py
│   ├── pipeline/           # 8 stages + QA reviews
│   │   ├── orchestrator.py
│   │   ├── stage_1_intake.py
│   │   ├── stage_2_environment.py
│   │   ├── stage_3_variants.py
│   │   ├── stage_4_simulation.py
│   │   ├── stage_5_interviews.py
│   │   ├── stage_6_narratives.py
│   │   ├── stage_7_judge.py
│   │   ├── stage_8_publish.py
│   │   └── qa_review.py
│   ├── dna/                # DNA YAML loader + validator
│   ├── venues/             # venue module loader + pluggable behaviors
│   ├── llm/                # OpenRouter client + cost tracker + tier router
│   ├── local_infer/        # GPU local (NER, embeddings, quote similarity)
│   ├── notifications/      # email + operator alerts
│   └── deliverable/        # Jinja2 renderer for /report/{project_id}
├── tests/
├── migrations/             # alembic
└── scripts/
```

## Status

- **Skeleton**: pyproject.toml, docker-compose, env template, config module, FastAPI hello-world. ✓
- **Next**: SQLModel models + Intake API (Stage 1) following `docs/intake-api-contract.md`.

## Dev conventions

- Python 3.12+
- Package manager: `uv`
- Lint + format: `ruff`
- Type check: `pyright --strict`
- Tests: `pytest --asyncio-mode=auto`

## Production deploy (v1+)

- Cloudflare Tunnel from WSL2 for v0 with external clients
- Migrate to Fly.io / Railway / DO App Platform when scaling
