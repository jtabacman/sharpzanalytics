# Repo structure — Sharpz Analytics

> **Ownership:** operador (Julian) + build Claude. Cualquier cambio de estructura pasa por esta doc.

## Top-level layout

```
sharpzanalytics/
├── backend/           # FastAPI app + pipeline engine (Python 3.12 + uv)
├── dna/               # test_type YAMLs — 1 archivo por test_type
├── venues/            # interaction surface YAMLs — 1 archivo por venue
├── prompts/           # prompts YAML (port de MiroFish 75 YAMLs)
│   ├── shared/        # prompts compartidos (one_pager, qa_reviewer_base)
│   └── <test_type>/   # prompts específicos per test_type
├── docs/              # documentación arquitectónica
├── scripts/           # dev tooling, data migrations, ops helpers
├── tests/             # pytest suite
└── migrations/        # alembic DB migrations
```

## Qué vive fuera de este repo

| Asset | Ubicación | Notas |
|---|---|---|
| Landing (`sharpzanalytics.com`) | Netlify | Static HTML, repo propio |
| Intake form (`intake.sharpzanalytics.com`) | Vercel, `sharpz-intake` project | Vue SPA + Python serverless en `api/`, Vercel KV (Redis) |
| Admin panel | Offline actualmente | Vue, pendiente re-deploy |
| MiroFish (prototipo anterior) | Mac de Julian | Fuente de 75 YAMLs de prompts portables |
| Business brief | Local de Julian (`sharpz_business_brief.md`) | Contexto producto |

## Convenciones

### Python

- Version: **3.12+**
- Package manager: **uv** (10-100× faster than pip/poetry)
- Lint + format: **ruff** (single tool)
- Type check: **pyright strict**
- Tests: **pytest + pytest-asyncio**

### Naming

- Test_type IDs: `snake_case` (ej. `investor_pitch`)
- Venue IDs: `snake_case` (ej. `pitch_meeting`)
- DNA filenames: `dna/<test_type_id>.yaml`
- Venue filenames: `venues/<venue_id>.yaml`
- Prompt filenames: `prompts/<test_type_id>/<stage>.yaml`

### Commits

- Conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`
- Referencia a issues cuando aplica: `feat(pipeline): add stage 4 orchestration (#12)`
- Sign-off en commits que tocan producción: trailer `Co-Authored-By:` cuando asistió Claude

### Branching

v0 (equipo de 1, velocidad > proceso):
- `main` es la rama activa
- Feature branches opcional para cambios grandes (> 500 líneas o múltiples días)
- Tags para milestones: `m0-complete`, `m1-complete`

v1+ (cuando crezca el equipo):
- `main` protegida
- PR + review obligatorio
- CI gates antes de merge

## Secretos y env vars

- `.env.local` — dev local (gitignored)
- `.env.example` — template comprometido
- Producción: secrets manager del host (Fly/Railway/DO) — nunca en repo
- Nunca committear: API keys (OpenRouter, Anthropic, OpenAI), DB credentials, Stripe webhook secrets, JWT keys

## Archivos que nunca entran al repo

- Stimulus subidos por clientes (PDFs de pitches, assets de creatividades)
- Deliverables renderizados
- Sim logs (event sourced, en DB o blob)
- Uploads de cualquier tipo

Ver `.gitignore` para la lista completa.
