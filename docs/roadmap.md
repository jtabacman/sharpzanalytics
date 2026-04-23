# Roadmap — Sharpz V2

> Origen: sección 16 del brief producto (`sharpz_business_brief.md`), adaptado con un m0 de arquitectura previa al código.
> Este doc es la fuente de verdad. La tabla del README es resumen.

---

## m0 — Arquitectura declarativa (semana 1) · ✓ done

**Objetivo:** contratos + specs + repo scaffolding. Cero lógica de producción.

**Deliverables:**
- `docs/dna-spec.md` — schema del test_type como YAML declarativo (5 simulation modes, 10 settings, QA review framework)
- `docs/frontend-architecture.md` — URLs unificadas, DNS Hostinger, dual theme design
- `docs/intake-api-contract.md` — TypeScript + Pydantic schema + validation rules
- `docs/landing-design.md`, `docs/intake-design.md`, `docs/deliverable-design.md` — referencias de diseño existentes
- `docs/repo-structure.md` — conventions
- `venues/` — 13/13 YAMLs detallados (pitch_meeting, retail_decision, social_viral, …)
- `dna/` — 3/15 activos (investor_pitch, pricing_test, crisis_response)
- `backend/` — skeleton FastAPI runnable (`/health` responde), pyproject + docker-compose + env + config
- `frontends/` — READMEs con import plans para las 4 superficies

**Criterio de done:** un Claude nuevo puede leer el repo sin contexto y entender producto + arquitectura + próximo paso.

---

## m1 — investor_pitch end-to-end (semana 2-3) · 🟡 in progress

**Objetivo:** pipeline completo de 1 test_type funcionando. Benchmark: caso Invernea (el mismo test que MiroFish corrió mal).

**Deliverables:**
- SQLModel models: `Client`, `Intake`, `Test`, `Environment`, `Persona`, `Variant`, `Simulation`, `Action`, `Interview`, `IndividualReport`, `Report`, `Pattern`
- Alembic migrations inicializadas
- Intake API (Stage 1) compatible con `intake-api-contract.md`
- DNA loader + venue loader + shared prompts placeholder
- LLM router delgado sobre OpenRouter + cost tracker + tier routing
- Stage 2 · environment build (amplify archetypes + extract entities + filter phantoms + generate personas + setup venue)
- Stage 3 · variant authoring (key_facts + initial_posts)
- Stage 4 · simulation para mode `deliberation` (round-by-round en venue pitch_meeting)
- Stage 5 · interviews (top 20% agents)
- Stage 6 · narratives per variant + quote validator
- Stage 7 · executive judge + one-pager con reasoning model
- Stage 8 · deliverable publish (Jinja2 + WeasyPrint PDF + R2 upload)
- QA review LLM post-stage (2, 4, 6, 7) con anti-bias invariants
- Event-sourced log para Stage 4 + snapshots para otras stages
- 1 cliente real disparando end-to-end (o replicando Invernea)

**Tier activado:** Pro únicamente (3 runs)

**Criterio de done:**
- Test completo corre en < 15 min
- Reporte tiene ≥ 5000 palabras + ≥ 15 quotes validadas + winner confidence calibrado
- Deliverable HTML accesible vía signed URL
- QA review logueó correcciones aplicadas
- Compare lado-a-lado con MiroFish Invernea: cero phantoms, cero language drift, cero copy-propagation

**Pendientes conocidos para después:** acceso a Mac para port de 75 YAMLs de MiroFish (los usamos como fuente de prompts); si no, escribimos prompts v1 inicial.

---

## m2 — Expansion horizontal (mes 2-3)

**Objetivo:** plataforma multi-test_type + multi-tier + cross-test learning básico.

**Deliverables:**
- **DNAs restantes (12/15):** creative_test, narrative_framing, brand_sentiment_shift, competitive_response, controversial_launch, product_launch, campaign_planning, churn_analysis, electoral_sentiment, policy_rollout, audience_targeting, b2b_pricing
- **Simulation modes restantes:**
  - `survey_batch` (pricing_test, creative_test, audience_targeting)
  - `forecast` (electoral_sentiment Ultra, policy_rollout)
  - `usage_simulation` (product_launch)
  - `hybrid` (narrative_framing, b2b_pricing, churn_analysis, policy_rollout)
- **Los 4 tiers implementados** (hoy solo Pro): Economy, Pro, Premium, Ultra con model tables distintos
- **Cross-test learning:** pattern extractor post-stage-8 + priors injection en stage-7 del próximo test del mismo cliente+type
- **NER local (GPU WSL2):** gliner-multi para entity validation + bge-m3 para embeddings + quote similarity
- **Real-time streaming al operador** durante sim (WebSocket + panel updates)
- **5-10 clientes reales pagando** (manual payments v0)
- **Operational stability:** error tracking, structured logs, retry policies, dead-letter queue

**Criterio de done:**
- Cada uno de los 15 test_types tiene al menos un test corrido end-to-end
- Los 4 tiers tienen cost cap + model routing verified
- 5+ clientes distintos con tests completados y patterns acumulados
- Pipeline puede correr 10 tests concurrent sin degradación

---

## m3 — Multi-tenant + self-serve (mes 4-6)

**Objetivo:** producto SaaS operable por clientes sin intervención manual.

**Deliverables:**
- **Multi-tenant DB:** workspace_id en todas las tablas + RLS Postgres
- **Auth flow real:** magic-link email + session tokens + rate limits
- **Self-serve intake:** cliente paga con Stripe (v1 real de billing), pipeline arranca solo
- **Admin panel re-deployed** en `control.sharpzanalytics.com` con approval queue + operator actions + cost dashboards
- **Landing pública** con content marketing + case studies + pricing page
- **Multi-modal stimulus** (video + audio + imagen) vía Claude Sonnet vision
- **Agent memory across tests:** Mubadala en test #4 recuerda test #1 con weight decay
- **Operator tools:** live pause + inject mid-sim + weight redistribution
- **SLAs documentados** por tier
- **Refund policy** + support flow básico

**Criterio de done:**
- Cliente nuevo puede firmar, pagar, completar intake y recibir deliverable sin tocar al operador
- Margen 98-99% confirmed (unit economics reales)
- Latency p50 ≤ prometido en cada tier

---

## m4 — Integraciones + moats (mes 7-12)

**Objetivo:** defensibilidad + viralidad.

**Deliverables:**
- **Slack bot** — `/sharpz test pricing for X` dispara flow
- **API pública** con API keys por cliente + OpenAPI spec + Python/JS SDKs
- **Integraciones CRM** (Salesforce, HubSpot) — sync de tests con accounts + opps
- **Marketplace de test_types custom** — clientes publican DNA propios (shared o privados)
- **Benchmarking cross-cliente** (opt-in) — "tu fee structure generó 65% positive intent, el average sector PE agri es 48%"
- **Multi-language panels** — trilingüe ES + EN + AR o LATAM regional
- **Expansion internacional** — multi-currency + país-specific compliance

**Criterio de done:**
- 3+ integraciones productivas con al menos 1 cliente activo en cada
- Marketplace tiene 3+ test_types custom publicados
- Benchmark dataset tiene 20+ tests opt-in per sector

---

## m5+ — Enterprise / research (año 2+)

**Objetivo:** moats profundos + pricing escalable a 6 dígitos.

**Deliverables tentativos:**
- **White-label para agencias** — agencia X revende Sharpz con branding propio
- **Custom enterprise features** — SSO, SCIM, audit log export, compliance reports
- **Research-grade tests** — partnerships con academia, peer review setup
- **Partnerships con consultoras** — McKinsey/Bain/etc resell Sharpz como augmentation
- **Industry-specific verticals** — "Sharpz for Pharma", "Sharpz for Political", con DNA pre-configured

---

## Principios cross-milestone

1. **Decision-first deliverable** — todo termina en "hacer X el lunes 9am"
2. **Transparencia sobre limitaciones** — Apéndice D siempre presente
3. **No "everything is great"** — honestidad > optimismo falso
4. **Quality gates post-each-stage** — fail fast, no silent failures
5. **Single source of truth** — una DB, sin file-state + DB-state inconsistentes
6. **Async + parallel desde día 1** — no serialize lo paralelizable
7. **Operator-in-the-loop** — el operador revisa entre stages hasta m3
8. **Replay** — todo se puede volver a ver, DNAs immutables embebidos

---

## Tiempo + budget assumptions

Julian es **solo founder + operator + builder** en equipo de 1 (hasta m3). Con Claude como builder:
- m0: done (1 sesión intensiva)
- m1: 2-3 semanas estimado
- m2: 2 meses
- m3: 3 meses
- m4+: no estimated hasta post m3

Si aparece un second dev, m2+ acelera ~40%.

## Revisión de este doc

Cada cierre de milestone (done criterion met) → actualizar este doc: mover milestone a ✓ done, agregar aprendizajes/desviaciones, re-estimar siguientes.
