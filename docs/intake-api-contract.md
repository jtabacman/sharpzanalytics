# Intake API Contract — Sharpz V2 backend ↔ frontend

> **Status:** v0.1 — derivado del intake Vue SPA existente (`intake.sharpzanalytics.com`).
> **Binding:** este contrato es la fuente de verdad. Backend V2 debe implementar exactamente esta shape para que el intake existente siga funcionando sin rewrite.
> **Modificaciones permitidas:** sí, pero cada cambio requiere actualizar intake Vue también. Preferimos aditivos (campos nuevos opcionales) sobre breaking changes.

---

## 1. Endpoints

| Método | Path | Propósito | Auth |
|---|---|---|---|
| `POST` | `/api/intakes` | Crear intake nuevo (devuelve `intake_id`) | Session cookie o anonymous |
| `GET` | `/api/intakes/:id` | Leer intake (para resume) | Session o signed token |
| `PATCH` | `/api/intakes/:id` | Auto-save (parcial) | Session o shared key |
| `POST` | `/api/intakes/:id/submit` | Finalizar y enviar a queue del operador | Session |
| `GET` | `/api/intakes?status=submitted` | Listado para operador | `X-Sharpz-Sync-Key` |

### Shared secrets

- `X-Sharpz-Sync-Key` — header obligatorio para endpoints operator (`GET /api/intakes`, operator list). Valor: env `SHARPZ_SYNC_KEY`.

---

## 2. Estados del Intake

```
draft (auto-saved, can edit) → submitted (locked, in queue) → approved (pipeline running) → completed
                                                           └→ rejected (operator sent feedback)
```

- **draft**: estado default post-POST. Auto-save funciona.
- **submitted**: inmutable. Frontend muestra "submitted card".
- **approved**: operador disparó pipeline. El Test associated tiene su propio estado.
- **rejected**: operador devolvió con razón. El cliente puede editar (se desbloquea a draft) y re-submitear.
- **completed**: el test asociado completó y el deliverable está disponible.

---

## 3. Schema completo del payload

### 3.1 TypeScript (autoritativo, usado por frontend Vue)

```typescript
type IntakeStatus = "draft" | "submitted" | "approved" | "rejected" | "completed";

interface Archetype {
  // Identity
  name: string;
  short_label: string;
  // Demographics
  age_range?: string;
  gender?: string;
  location?: string;
  occupation?: string;
  income_level?: string;
  // Psychographics
  motivations?: string;
  frustrations?: string;
  values?: string;
  // Category relationship
  category_history?: string;
  brand_affinity?: "advocate" | "user" | "lapsed" | "aware" | "unaware";
  price_sensitivity?: "low" | "medium" | "high";
  // Voice
  archetypal_quote?: string;
  // Role in test
  role?: "hardcore" | "mainstream" | "skeptic" | "advocate" | "laggard" | "influencer";
  must_be_vocal?: boolean;
}

interface Variant {
  name: string;
  description: string;
  // Dynamic fields per test_type (ex: price_point for pricing_test)
  [key: string]: any;
}

interface Intake {
  // System-managed
  id: string;                       // server-assigned UUID on POST
  status: IntakeStatus;
  created_at: string;               // ISO 8601
  updated_at: string;
  submitted_at: string | null;

  // Section 01 — Who writes
  company_name: string;
  contact_name: string;
  contact_email: string;
  contact_role: string;

  // Section 02 — Test type
  test_type_preference: string;     // one of the 15 test_types
  test_title: string;

  // Section 03 — Objective
  test_objective: string;
  decision_context: string;
  test_type_specific: Record<string, any>;  // dynamic by test_type

  // Section 04 — Product / brand
  product_name: string;
  product_description: string;
  launch_timing: string;
  brand_positioning: string;
  key_competitors: string[];
  markets: string[];
  key_facts_global: Record<string, string>;

  // Section 05 — Scenario (conditional, only scenario_plus_responses types)
  scenario: Record<string, any>;

  // Section 06 — Audience
  target_audience_description: string;
  desired_archetypes: Archetype[];
  must_include_archetypes: string[];
  must_exclude_archetypes: string[];
  audience_size_hint: number;       // default 80, max 200 (UI) — backend enforces DNA limits

  // Section 07 — Hypotheses / success
  hypotheses: string[];
  success_metrics: string[];
  expected_risks: string;

  // Section 08 — Variants (array size per test_type DNA)
  variants: Variant[];

  // Section 09 — Branding / constraints
  client_logo_url: string;
  client_primary_color: string;     // hex
  sensitive_topics_to_avoid: string;
  legal_constraints: string;
  reference_urls: string[];

  // Tier (from payment step if integrated)
  tier_selected?: "economy" | "pro" | "premium" | "ultra";
  payment_status?: "pending" | "paid" | "refunded";
  stripe_session_id?: string;
}
```

### 3.2 Pydantic (backend V2 source of truth)

```python
from datetime import datetime
from enum import Enum
from typing import Any
from pydantic import BaseModel, EmailStr, Field, HttpUrl


class IntakeStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"


class BrandAffinity(str, Enum):
    ADVOCATE = "advocate"
    USER = "user"
    LAPSED = "lapsed"
    AWARE = "aware"
    UNAWARE = "unaware"


class PriceSensitivity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ArchetypeRole(str, Enum):
    HARDCORE = "hardcore"
    MAINSTREAM = "mainstream"
    SKEPTIC = "skeptic"
    ADVOCATE = "advocate"
    LAGGARD = "laggard"
    INFLUENCER = "influencer"


class Tier(str, Enum):
    ECONOMY = "economy"
    PRO = "pro"
    PREMIUM = "premium"
    ULTRA = "ultra"


class Archetype(BaseModel):
    name: str
    short_label: str = ""
    age_range: str | None = None
    gender: str | None = None
    location: str | None = None
    occupation: str | None = None
    income_level: str | None = None
    motivations: str | None = None
    frustrations: str | None = None
    values: str | None = None
    category_history: str | None = None
    brand_affinity: BrandAffinity | None = None
    price_sensitivity: PriceSensitivity | None = None
    archetypal_quote: str | None = None
    role: ArchetypeRole | None = None
    must_be_vocal: bool = False


class Variant(BaseModel):
    name: str
    description: str = ""
    # Dynamic fields per test_type validated against DNA.variant_fields
    model_config = {"extra": "allow"}


class Intake(BaseModel):
    id: str
    status: IntakeStatus = IntakeStatus.DRAFT
    created_at: datetime
    updated_at: datetime
    submitted_at: datetime | None = None

    # Section 01
    company_name: str = ""
    contact_name: str = ""
    contact_email: EmailStr | str = ""    # allow str for drafts
    contact_role: str = ""

    # Section 02
    test_type_preference: str = ""
    test_title: str = ""

    # Section 03
    test_objective: str = ""
    decision_context: str = ""
    test_type_specific: dict[str, Any] = Field(default_factory=dict)

    # Section 04
    product_name: str = ""
    product_description: str = ""
    launch_timing: str = ""
    brand_positioning: str = ""
    key_competitors: list[str] = Field(default_factory=list)
    markets: list[str] = Field(default_factory=list)
    key_facts_global: dict[str, str] = Field(default_factory=dict)

    # Section 05
    scenario: dict[str, Any] = Field(default_factory=dict)

    # Section 06
    target_audience_description: str = ""
    desired_archetypes: list[Archetype] = Field(default_factory=list)
    must_include_archetypes: list[str] = Field(default_factory=list)
    must_exclude_archetypes: list[str] = Field(default_factory=list)
    audience_size_hint: int = 80

    # Section 07
    hypotheses: list[str] = Field(default_factory=list)
    success_metrics: list[str] = Field(default_factory=list)
    expected_risks: str = ""

    # Section 08
    variants: list[Variant] = Field(default_factory=list)

    # Section 09
    client_logo_url: str = ""
    client_primary_color: str = ""
    sensitive_topics_to_avoid: str = ""
    legal_constraints: str = ""
    reference_urls: list[str] = Field(default_factory=list)

    # Tier & payment (optional, nullable until paid)
    tier_selected: Tier | None = None
    payment_status: str | None = None
    stripe_session_id: str | None = None
```

---

## 4. Validation rules (backend enforces on submit)

Un intake en estado `draft` acepta cualquier shape parcial (auto-save tolerant). En `submit` el backend valida:

### 4.1 Required fields (submission-blocking)

- `company_name` non-empty
- `contact_name` non-empty
- `contact_email` valid email
- `test_type_preference` ∈ lista de 15 test_types activos
- `test_title` non-empty, ≤ 120 chars
- `test_objective` ≥ 50 chars (no briefs vacíos)
- `product_description` ≥ 100 chars
- `desired_archetypes` array con `count ≥ DNA.panel.anchors_spec.count.min` (según test_type)
- `variants` array con `count ≥ DNA.variant_min`

### 4.2 DNA-driven validation

Para cada test_type, la DNA declara `anchors_spec.count.min/max` + `variant_min/max`:

```python
async def validate_intake_submit(intake: Intake) -> list[str]:
    """Returns list of validation errors. Empty = OK to submit."""
    errors = []
    dna = await load_dna(intake.test_type_preference)
    if not dna:
        errors.append(f"Unknown test_type: {intake.test_type_preference}")
        return errors

    # Archetypes count
    min_anchors = dna.panel.anchors_spec.count.min
    max_anchors = dna.panel.anchors_spec.count.max
    n = len(intake.desired_archetypes)
    if n < min_anchors:
        errors.append(f"Need ≥ {min_anchors} archetypes (got {n})")
    if n > max_anchors:
        errors.append(f"Max {max_anchors} archetypes (got {n})")

    # Variants count
    if len(intake.variants) < dna.variant_min:
        errors.append(f"Need ≥ {dna.variant_min} variants")

    # Stimulus check (for test_types that require file upload)
    if dna.stimulus.required_fields and not intake.test_type_specific.get("stimulus_url"):
        errors.append("Estímulo (PDF/video/image) es obligatorio")

    # Audience size hint vs DNA
    if intake.audience_size_hint > dna.simulation.panel_size.max:
        errors.append(f"Panel size > DNA max ({dna.simulation.panel_size.max})")

    return errors
```

### 4.3 Detección de conflictos obvios

- Archetypes genéricos tipo "consumers" → warning pidiendo más especificidad
- Tier mismatch con complejidad del test → suggestion de upgrade/downgrade
- Locale inconsistency (intake en español + product_description en inglés) → warning

---

## 5. Auto-save semantics

- **Trigger:** on-blur de cualquier campo + debounced 30s interval
- **Endpoint:** `PATCH /api/intakes/:id` con body partial (solo los campos modificados)
- **Response:** `{ updated_at: ISO, status: "draft" }`
- **UI feedback:** "Guardado a las HH:MM" indicator en el hero del form
- **Conflict resolution:** last-write-wins (no optimistic locking en v0). Improbable que dos sesiones editen el mismo intake simultáneo.
- **Rate limit backend:** max 1 PATCH / 2s per intake_id para evitar thrashing.

---

## 6. Submission flow (`POST /api/intakes/:id/submit`)

```
1. Backend valida con validate_intake_submit()
   └─ Si errors → 400 con {errors: [...]}, frontend muestra list
2. Si OK:
   a. Backend marca status=submitted, submitted_at=now
   b. Backend crea un Test record (DNA snapshot embebido)
   c. Backend notifica operador (webhook Slack o email)
   d. Si Stripe integrado y unpaid → redirect a Checkout session
3. Backend response: { id, status, submitted_at, test_id, next_action }
   └─ next_action ∈ {"await_payment", "await_operator_approval", "approved"}
```

---

## 7. Operator workflow integration

El control panel (`control.sharpzanalytics.com`) consume:

- `GET /api/intakes?status=submitted` — queue
- `GET /api/intakes/:id` — full detail
- `POST /api/intakes/:id/approve` → dispara Stage 2 pipeline
- `POST /api/intakes/:id/reject` con body `{reason: str}` → vuelve a draft y notifica cliente
- `PATCH /api/intakes/:id/override` → operador puede editar archetypes, tier, etc.

Todos requieren `X-Sharpz-Sync-Key` header.

---

## 8. Migration notes (del intake actual al V2)

El intake Vue SPA actual hace POSTs al endpoint de Vercel serverless (`/api/sharpz/intakes/...`) que persiste en Vercel KV. V2 reemplaza Vercel KV con Postgres.

**Estrategia de corte:**

1. V2 backend implementa TODOS los endpoints de sección 1 con misma shape
2. Variable env del intake Vue: `VITE_API_URL` — cambiamos de `/api/sharpz` (Vercel serverless) a `https://backend.sharpzanalytics.com/api` (backend V2)
3. Intakes activos en Vercel KV al momento del corte → se migran con script one-off (`scripts/migrate_kv_to_postgres.py`)
4. Rebuild + redeploy del intake con nuevo API_URL

Sin rewrite del Vue SPA. El cliente no nota el cambio.

---

## 9. Open items

1. **Stripe integration** — ¿está ya en el intake o lo agregamos backend-side en `/submit`?
2. **Email notifications** — ¿qué sender usamos? Resend, Postmark, SES? (no bloquea v0 — podemos logear en el operador y notificar manual)
3. **File upload** — el intake upload PDF/video/image. ¿Vercel Blob, R2, S3? La URL termina en `test_type_specific.stimulus_url` pero el endpoint de upload es aparte.
4. **Rate limits + abuse protection** — intake es público-ish. Necesita Captcha o rate limit por IP al menos.

---

**Fin v0.1.** Backend V2 implementa este contrato en Paso 4 del plan maestro. Cualquier desviación se documenta acá antes de escribir código.
