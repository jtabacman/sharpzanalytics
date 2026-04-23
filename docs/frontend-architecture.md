# Frontend Architecture — Sharpz V2

> **Status:** v0.1 — working draft.
> **Decisión:** unificar los 4 frontends bajo `sharpzanalytics.com` (+ `control.` subdomain) con DNS en Hostinger.
> **Assets existentes:** landing Netlify, intake Vercel Vue SPA, admin Vue offline. Los portamos/reusamos sin rewrite.

---

## 1. Los 4 frontends del producto

| # | Superficie | URL | Propósito | Quién accede |
|---|---|---|---|---|
| 1 | **Landing** | `sharpzanalytics.com` | Marketing, CTAs, operator login entry | Público |
| 2 | **Intake form** | `sharpzanalytics.com/intake/{intake_id}` | Cliente completa brief + estímulo + paga | Cliente con sesión |
| 3 | **Control panel** | `control.sharpzanalytics.com` | Operador revisa intakes, aprueba, dispara tests, monitorea | Operador (Julian) |
| 4 | **Deliverable** | `sharpzanalytics.com/report/{project_id}` | Cliente ve reporte HTML interactivo | Cliente (link único) |

### Diferencias vs estructura actual

| Actual | Nuevo | Razón |
|---|---|---|
| `intake.sharpzanalytics.com` | `sharpzanalytics.com/intake/{id}` | Unificación bajo dominio raíz + URL con ID para auto-save persistente |
| (sin admin deploy) | `control.sharpzanalytics.com` | Re-deploy del admin Vue en subdomain |
| (sin deliverable hosting) | `sharpzanalytics.com/report/{project_id}` | Deliverable como ruta del root |

### Nota sobre el prefijo `/report/`

Julian pidió originalmente `sharpzanalytics.com/{project_id}` sin prefijo. **Recomendamos prefijo `/report/`** por 2 razones:

1. **Evita colisión con rutas futuras** de la landing (`/about`, `/services`, `/pricing`).
2. **Separa el namespace de IDs** — si mañana queremos `/about`, no hay ambiguity con un project_id llamado "about".

Alternativa si el prefijo molesta estéticamente: usar IDs con patrón reconocible (ej. UUIDs o prefix `sh_xxx`) + regex en el router. Frágil, no recomendado.

---

## 2. Hosting + DNS (Hostinger como DNS manager)

### Asumpciones

- Julian tiene `sharpzanalytics.com` comprado en Hostinger
- Hostinger es el DNS manager (no necesariamente el host)
- Queremos mantener la landing Netlify existente + intake Vue existente (evitar rewrites)

### Routing strategy recomendada

**Opción A — Netlify como "frontend router" (recomendada para v0):**

```
DNS @ CNAME → Netlify
DNS control CNAME → Vercel (admin SPA) o backend

Netlify _redirects:
  /intake/*     → backend (Cloudflare Tunnel URL)     200
  /report/*     → backend                              200
  /api/*        → backend                              200
  /*            → /index.html                          200
```

Ventajas:
- Un solo DNS record para `@`
- Netlify decide routing via `_redirects` file
- La landing static sigue sirviendo como está
- Backend se expone solo por las rutas que necesita
- Plan free de Netlify lo soporta

Desventajas:
- Si Netlify cae, cae todo
- Latency extra (request pasa por Netlify → backend)

**Opción B — Cloudflare como edge proxy:**

```
DNS @ A → Cloudflare
Cloudflare Workers:
  / → Netlify origin
  /intake/* → backend origin
  /report/* → backend origin
Cloudflare Workers:
  control.* → Vercel/backend
```

Ventajas:
- Latency mínima (Cloudflare edge en todo el mundo)
- Rules más flexibles
- DDoS protection gratis
- Logs agregados

Desventajas:
- Setup más complejo
- Cloudflare Workers puede tener cost en volumen alto (free tier cubre 100k req/día)

**Decisión recomendada v0:** Opción A (Netlify). Migrar a Opción B si escalamos.

### DNS records concretos (Hostinger)

```
Type   Name      Value                                       TTL
────────────────────────────────────────────────────────────────
A      @         <Netlify IP>          (o ALIAS a apex CNAME) 300
CNAME  www       sharpzanalytics.com                          300
CNAME  control   <Vercel / backend URL>                       300
```

El subdomain `intake.*` del setup actual se deprecia — se redirige a `/intake` del root vía Netlify redirect 301 para preservar links viejos si existen.

---

## 3. Estructura del repo `frontends/`

```
frontends/
├── landing/                    # sharpzanalytics.com — HTML static + Three.js
│   ├── index.html
│   ├── assets/
│   │   ├── css/
│   │   ├── js/hero-graph.js    # Three.js graph 3D
│   │   └── fonts/
│   ├── login/                  # /login/ operator entry
│   │   └── index.html
│   └── _redirects              # Netlify routing rules
│
├── intake/                     # /intake/{intake_id} — Vue 3 SPA
│   ├── src/
│   │   ├── views/ClientIntake.vue
│   │   ├── components/
│   │   │   ├── ArchetypeCard.vue
│   │   │   ├── ListBuilder.vue
│   │   │   ├── KeyValueBuilder.vue
│   │   │   └── SchemaField.vue
│   │   ├── api/intake.js       # calls to backend
│   │   └── main.js
│   ├── public/tokens.css       # global design tokens
│   ├── vite.config.js
│   └── package.json
│
├── control/                    # control.sharpzanalytics.com — Vue SPA admin
│   ├── src/                    # importado del /MiroFish/frontend/ original
│   └── package.json
│
└── deliverable-template/       # backend render target
    ├── base.html.j2            # Jinja2 template del deliverable
    ├── report.css
    └── interactive.js          # click en agent → persona modal
```

### Decisión: monorepo unificado

Los 4 frontends viven en ESTE repo (`sharpzanalytics`). Rationale:
- Un solo lugar para operar releases
- Compartir design tokens (`tokens.css` global)
- CI/CD unificado
- Deploy coordinado (si el backend cambia un API contract, los frontends dependientes se actualizan en el mismo PR)

Los deploys siguen siendo independientes por frontend (cada uno a su host), pero el código está junto.

---

## 4. Design system — dual theme

El producto tiene **dos ethos visuales distintos** que coexisten:

### Theme A — "Operator-tech dark" (landing + intake + control)

- Paleta: `#0a0a0a` canvas, grays escalonados, accent `#e0e0e0`
- Fonts: `Space Grotesk` (UI), `JetBrains Mono` (tags/IDs)
- Signature: section numbers "01 / Services", gradient text, monospace labels uppercase
- Feel: quiet authority, Bloomberg terminal minimal

Ver `docs/landing-design.md` para paleta + patterns completos.

### Theme B — "Report serif authority" (deliverable)

- Paleta: `#FAF9F6` canvas (warm off-white), `#0A0E27` ink, `#B85C38` terracotta accent
- Fonts: `Inter` (UI), `GT Sectra` / Georgia (body serif), `JetBrains Mono` (meta)
- Signature: serif body con line-height 1.75, terracotta blockquote borders
- Feel: FT × McKinsey × Stratechery — printed authority

Ver `docs/intake-design.md` sección 1 (tokens.css) para paleta completa.

### Decisión sobre coexistencia

**Mantener ambos themes** — tienen funciones distintas:
- Theme A es "operator UI" — denso, informacional, dark
- Theme B es "deliverable" — reading experience, light, serif

NO unificar en uno solo. La decisión ya está en el design existente y funciona.

---

## 5. Flujo end-to-end con los 4 frontends

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  1. Cliente visita sharpzanalytics.com                       │
│     (landing static Netlify, Three.js hero)                  │
│              │                                               │
│              ├─ click "Request a test"                       │
│              ▼                                               │
│  2. Backend POST /api/intakes → crea intake_id               │
│     Redirect → sharpzanalytics.com/intake/{intake_id}        │
│              │                                               │
│              ▼                                               │
│  3. Intake Vue SPA carga estado por GET /api/intakes/{id}    │
│     Cliente llena 9 secciones                                │
│     Auto-save cada N segundos: PATCH /api/intakes/{id}       │
│              │                                               │
│              ├─ submit                                       │
│              ▼                                               │
│  4. POST /api/intakes/{id}/submit                            │
│     → backend marca submitted, notifica operador             │
│     Intake muestra "submitted" state                         │
│                                                              │
│  ─── OPERATOR PATH ──────────────────────────────────────    │
│                                                              │
│  5. Operador abre control.sharpzanalytics.com                │
│     Ve queue de intakes pending                              │
│     Aprueba + dispara pipeline                               │
│              │                                               │
│              ▼                                               │
│  6. Backend ejecuta 8 stages con QA reviews                  │
│     Real-time monitoring en control panel                    │
│              │                                               │
│              ▼                                               │
│  7. Stage 8: render HTML del deliverable                     │
│     Upload a R2 o servido directo desde backend              │
│     URL: sharpzanalytics.com/report/{project_id}             │
│     Email al cliente con link                                │
│                                                              │
│  ─── CLIENT PATH ────────────────────────────────────────    │
│                                                              │
│  8. Cliente abre el link                                     │
│     Backend sirve HTML renderizado del template serif        │
│     Click en personas → modal con persona full + sim actions │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 6. Integraciones y autenticación

### Intake (client-facing)

- **Auth:** session token en cookie + intake_id en URL (doble check backend)
- **Auto-save:** PATCH cada 30s o on-blur de cada sección
- **Upload:** estimulo (PDF/video/image) directo a blob storage via signed URL del backend
- **Pago:** Stripe Checkout session creada por backend, redirect al pago, webhook confirma

### Control panel (operator-facing)

- **Auth:** API key del operador (password-equivalent) + session cookie en cada request
- **Scope:** todos los intakes + todos los tests + cost tracker + alerts feed

### Deliverable (client-facing, link único)

- **Auth:** signed URL con JWT embedded (expires 90 días) o magic link per cliente
- **Anonymous view:** NO. El deliverable NUNCA es público — siempre requiere el link con token válido
- **Optional share:** cliente puede generar links adicionales con scope limitado para su equipo

### API secrets crosswiring

| Frontend | Backend secret | Uso |
|---|---|---|
| Intake | `X-Sharpz-Sync-Key` (shared secret) | Auth para auto-save endpoint |
| Control | `OPERATOR_API_KEY` + JWT session | Auth operator |
| Deliverable | JWT signed URL | Validation per request |
| Landing | ninguno (static) | N/A |

---

## 7. Deploy targets propuestos

| Frontend | Primary | Rationale | Fallback |
|---|---|---|---|
| Landing | **Netlify** | Existente, static + redirects built-in | Vercel |
| Intake | **Backend sirve SPA** | Compila Vue a static + backend Jinja wrap con intake_id | Vercel con redirect |
| Control | **Vercel** | Privado por auth, separate deploy | Backend sirve |
| Deliverable | **Backend Jinja** | Render dinámico por project_id desde DB | Static pre-render + R2 |

Ver sección 2 para DNS routing.

---

## 8. Open questions para cerrar con Julian

1. **Prefijo `/report/` vs `/{project_id}` sin prefijo**: mi recomendación es `/report/`. ¿OK?

2. **Control panel — re-deploy del código Vue existente en `/MiroFish/frontend/`** (que está offline) vs **rewrite desde cero en React/Svelte**: recomiendo reuse del código Vue actual. Rewrite es 1-2 semanas extra sin ganancia visible.

3. **Stripe integration**: ¿ya está integrada en el intake actual, o hay que agregarla? El doc del intake no la menciona explícitamente.

4. **Auth flow del intake — login antes o después del form?** Mirando el código Vue, parece que no hay login pre-form (el intake_id basta). ¿Validamos email via magic-link al submittear o dejamos open submission + approval manual del operador?

5. **Deliverable sharing — signed URLs vs public link**: mi recomendación signed URLs. ¿El cliente pide alguna vez un link público?

6. **Branding per cliente en deliverable**: el doc menciona `client_logo_url` y `client_primary_color` en el payload. ¿Confirmamos que el deliverable template usa esto o quitamos del schema?

---

**Fin v0.1.** Siguiente paso después de resolver open questions: setup de Hostinger DNS + Netlify deploy + estructura concreta de `frontends/` con código importado.
