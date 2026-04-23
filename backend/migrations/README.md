# Alembic migrations

Async migrations para Postgres via `asyncpg`.

## Crear migration nueva

```bash
# Desde backend/
uv run alembic revision --autogenerate -m "descripción corta"
```

Alembic compara `SQLModel.metadata` contra la DB actual y genera la diff.
Antes de correr, asegurate que `sharpz.models` esté importando todos los models
en `env.py`.

## Aplicar migrations

```bash
# upgrade a último
uv run alembic upgrade head

# downgrade 1 paso
uv run alembic downgrade -1

# ver estado actual
uv run alembic current

# ver history
uv run alembic history
```

## Convención

- Cada revision tiene un nombre descriptivo (ej. `001_initial_schema`, `002_add_pattern_table`)
- `downgrade()` DEBE ser implementado (no empty) para poder rollback
- Migrations production-destructive (DROP TABLE, DROP COLUMN con data) requieren coordinación manual — no autogenerate ciegamente

## Estado

- `versions/` vacía — la primera migration se crea en Stage 1 (m1) con todos los models iniciales
