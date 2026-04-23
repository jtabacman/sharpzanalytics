# Sharpz Analytics — Intake Form Design

> Código del diseño del intake form actual (`intake.sharpzanalytics.com`, hosted en Vercel).
> Vue 3 SPA con modo `VITE_PUBLIC_MODE=true` (oculta el resto del dashboard operator).
>
> **Design language:** mismo dark theme que la landing (`#0a0a0a` + Space Grotesk + JetBrains Mono + acentos `#e0e0e0`) pero tighter, más form-focused. Secciones numeradas tipo informe. Cards colapsables. Auto-save.
>
> **Structure:** una vista grande (`ClientIntake.vue`) que compone 4 componentes reutilizables (`ArchetypeCard`, `ListBuilder`, `KeyValueBuilder`, `SchemaField`). Diseño tokens en `tokens.css` global (usado también en reportes).

---

## Archivo 1/6 · Design tokens globales (`tokens.css`)

> **Nota importante:** Este archivo de tokens se diseñó originalmente para los REPORTES (viewer PDF/HTML de deliverables) con un ethos "FT × McKinsey × Stratechery" — serif, cream paper, terracotta accents. El intake form en cambio usa el dark theme de la landing. Hay dos design languages coexistiendo en el proyecto:
> - **tokens.css** → reportes/deliverables (light, serif, authoritative)
> - **intake inline vars** → forms/landing (dark, sans, operator-tech)
>
> Para V2 conviene decidir si mantener dual-theme o unificar. Por ahora se mantiene.

```css
/* ==========================================================================
   SHARPZ DESIGN TOKENS
   Synthetic audiences for strategic clarity

   Ethos: "Quiet authority" — FT x McKinsey x Stratechery
   Use these variables everywhere. No hardcoded colors or fonts in components.
   ========================================================================== */

:root {
  /* ------ COLORS · Primary Palette -------------------------------------- */
  --sharpz-ink:          #0A0E27;   /* Deep Navy - main text */
  --sharpz-ink-soft:     #1F2441;   /* Slightly lighter for body */
  --sharpz-canvas:       #FAF9F6;   /* Warm off-white - background */
  --sharpz-paper:        #FFFFFF;   /* Pure white for cards/content */

  /* ------ COLORS · Accent ---------------------------------------------- */
  --sharpz-accent-warm:  #B85C38;   /* Terracotta - highlights, quotes */
  --sharpz-accent-warm-soft: #E8CFC4; /* Terracotta tinted for bg hints */
  --sharpz-accent-cool:  #1E40AF;   /* Deep Blue - interactive links */
  --sharpz-accent-cool-hover: #1E3A8A;

  /* ------ COLORS · Neutrals -------------------------------------------- */
  --sharpz-gray-100:     #F4F2ED;   /* subtle backgrounds */
  --sharpz-gray-200:     #E5E1D8;   /* grid lines, dividers */
  --sharpz-gray-400:     #A8A29A;   /* disabled, muted */
  --sharpz-gray-500:     #6B7280;   /* meta info, timestamps */
  --sharpz-gray-700:     #374151;   /* secondary text */

  /* ------ COLORS · Semantic -------------------------------------------- */
  --sharpz-success:      #166534;
  --sharpz-success-bg:   #DCFCE7;
  --sharpz-warning:      #92400E;
  --sharpz-warning-bg:   #FEF3C7;
  --sharpz-danger:       #991B1B;
  --sharpz-danger-bg:    #FEE2E2;

  /* ------ TYPOGRAPHY · Font families ----------------------------------- */
  --sharpz-font-ui: "Inter", "Inter Display", -apple-system, BlinkMacSystemFont,
                    "Segoe UI", sans-serif;
  --sharpz-font-serif: "GT Sectra", "Tiempos Text", "Charter",
                       "Iowan Old Style", Georgia, serif;
  --sharpz-font-mono: "JetBrains Mono", "SF Mono", Menlo, Consolas, monospace;

  /* ------ TYPOGRAPHY · Sizes ------------------------------------------- */
  --sharpz-text-xs:      0.75rem;    /* 12px */
  --sharpz-text-sm:      0.875rem;   /* 14px */
  --sharpz-text-base:    1rem;       /* 16px */
  --sharpz-text-lg:      1.125rem;   /* 18px */
  --sharpz-text-xl:      1.25rem;    /* 20px */
  --sharpz-text-2xl:     1.5rem;     /* 24px */
  --sharpz-text-3xl:     1.875rem;   /* 30px */
  --sharpz-text-4xl:     2.5rem;     /* 40px */
  --sharpz-text-5xl:     3.5rem;     /* 56px */

  /* ------ TYPOGRAPHY · Weights ----------------------------------------- */
  --sharpz-weight-regular:  400;
  --sharpz-weight-medium:   500;
  --sharpz-weight-semibold: 600;
  --sharpz-weight-bold:     700;

  /* ------ TYPOGRAPHY · Line height ------------------------------------- */
  --sharpz-leading-tight:   1.25;
  --sharpz-leading-snug:    1.375;
  --sharpz-leading-normal:  1.5;
  --sharpz-leading-relaxed: 1.625;
  --sharpz-leading-loose:   1.75;  /* serif body ideal */

  /* ------ SPACING ------------------------------------------------------ */
  --sharpz-space-0:   0;
  --sharpz-space-1:   0.25rem;
  --sharpz-space-2:   0.5rem;
  --sharpz-space-3:   0.75rem;
  --sharpz-space-4:   1rem;
  --sharpz-space-5:   1.25rem;
  --sharpz-space-6:   1.5rem;
  --sharpz-space-8:   2rem;
  --sharpz-space-10:  2.5rem;
  --sharpz-space-12:  3rem;
  --sharpz-space-16:  4rem;
  --sharpz-space-20:  5rem;
  --sharpz-space-24:  6rem;

  /* ------ LAYOUT · Widths ---------------------------------------------- */
  --sharpz-width-narrow:    560px;
  --sharpz-width-reading:   720px;
  --sharpz-width-content:   960px;
  --sharpz-width-wide:     1200px;

  /* ------ BORDERS & RADII ---------------------------------------------- */
  --sharpz-border-width:    1px;
  --sharpz-border-color:    var(--sharpz-gray-200);
  --sharpz-radius-none:     0;
  --sharpz-radius-sm:       2px;
  --sharpz-radius-md:       4px;
  --sharpz-radius-lg:       8px;

  /* ------ SHADOWS (used very sparingly) -------------------------------- */
  --sharpz-shadow-subtle:   0 1px 2px 0 rgba(10, 14, 39, 0.04);
  --sharpz-shadow-paper:    0 1px 3px 0 rgba(10, 14, 39, 0.08),
                            0 1px 2px 0 rgba(10, 14, 39, 0.04);

  /* ------ TRANSITIONS -------------------------------------------------- */
  --sharpz-transition-fast:   100ms cubic-bezier(0.4, 0, 0.2, 1);
  --sharpz-transition-normal: 200ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* Report body styling (serif, terracotta quotes) */
.sharpz-report-body {
  font-family: var(--sharpz-font-serif);
  font-size: var(--sharpz-text-lg);
  line-height: var(--sharpz-leading-loose);
  color: var(--sharpz-ink-soft);
  max-width: var(--sharpz-width-reading);
  margin: 0 auto;
  padding: var(--sharpz-space-12) var(--sharpz-space-6);
}

.sharpz-report-body blockquote {
  border-left: 3px solid var(--sharpz-accent-warm);  /* Terracotta */
  padding-left: var(--sharpz-space-5);
  margin: var(--sharpz-space-8) 0;
  font-style: italic;
  color: var(--sharpz-gray-700);
}
```

---

## Archivo 2/6 · `ClientIntake.vue` — template (la vista principal)

El intake se compone de **9 secciones numeradas** (01 al 09), con auto-save + estado "submitted" al final. Cada sección es una card `.intake-section` con head (num + título) + sub + fields.

**Structure (9 secciones):**
01. Quién nos escribe (contacto empresa)
02. Qué tipo de test (grid de 15 test_types como radio cards)
03. Qué querés aprender (objetivo + decisión)
04. Tu producto, tu marca
05. Escenario (solo para test_types `scenario_plus_responses`)
06. Audiencia (buyer + archetypes array)
07. Hipótesis y éxito
08. Variantes a comparar (N variants dinámicas según schema)
09. Branding & restricciones

```vue
<template>
  <div class="intake-page">
    <!-- HERO -->
    <header class="intake-hero">
      <div class="intake-hero-inner">
        <div class="intake-brand-tag">Sharpz Analytics · Client Intake</div>
        <h1>Contanos qué querés testear</h1>
        <p class="intake-hero-lead">
          Este formulario captura todo lo que necesitamos para correr una
          simulación con tu audiencia sintética y compararte N variantes antes
          de ir a mercado. Completalo a tu ritmo — se guarda automáticamente.
        </p>
        <div v-if="intakeId" class="intake-id">
          <strong>Tu intake ID:</strong>
          <code>{{ intakeId }}</code>
          <span class="intake-save-hint">{{ savingLabel }}</span>
        </div>
      </div>
    </header>

    <main class="intake-main">
      <div v-if="error" class="sharpz-error-box">{{ error }}</div>

      <!-- Submitted state -->
      <div v-if="submitted" class="intake-submitted-card">
        <h2>✓ Intake enviado</h2>
        <p>
          Tu intake quedó en cola de revisión.
          Nos contactamos a <strong>{{ form.contact_email }}</strong>
          con cronograma y confirmación.
        </p>
        <p><strong>ID de referencia:</strong> <code>{{ intakeId }}</code></p>
      </div>

      <template v-if="!submitted">

      <!-- 01 Quién nos escribe -->
      <section class="intake-section">
        <div class="intake-section-head">
          <span class="intake-section-num">01</span>
          <h2>Quién nos escribe</h2>
        </div>
        <p class="intake-section-sub">
          Datos del contacto comercial. Los usamos para coordinar el test;
          nunca aparecen en el reporte.
        </p>
        <div class="intake-grid-2">
          <div class="intake-field">
            <label>Empresa o agencia *</label>
            <input v-model="form.company_name" placeholder="ej. Sony Interactive Entertainment" />
          </div>
          <div class="intake-field">
            <label>Tu nombre *</label>
            <input v-model="form.contact_name" placeholder="Nombre y apellido" />
          </div>
          <div class="intake-field">
            <label>Email</label>
            <input v-model="form.contact_email" type="email" placeholder="nombre@empresa.com" />
          </div>
          <div class="intake-field">
            <label>Rol</label>
            <input v-model="form.contact_role" placeholder="Ej: Head of Pricing" />
          </div>
        </div>
      </section>

      <!-- 02 Tipo de test -->
      <section class="intake-section">
        <div class="intake-section-head">
          <span class="intake-section-num">02</span>
          <h2>Qué tipo de test necesitás</h2>
        </div>
        <p class="intake-section-sub">
          El tipo de test determina qué preguntas te vamos a hacer y cómo
          estructuramos las variantes.
        </p>

        <!-- Grid de test_type cards con radio selection -->
        <div class="test-type-grid">
          <label
            v-for="t in TEST_TYPES"
            :key="t.value"
            class="test-type-card"
            :class="{ selected: form.test_type_preference === t.value }"
          >
            <input type="radio" :value="t.value" v-model="form.test_type_preference" />
            <div class="test-type-label">
              <strong>{{ t.label }}</strong>
              <div class="test-type-desc">{{ t.desc }}</div>
              <div class="test-type-shape">{{ t.shape }}</div>
            </div>
          </label>
        </div>

        <div v-if="form.test_type_preference" class="intake-grid-2" style="margin-top: 24px;">
          <div class="intake-field">
            <label>Título corto del test *</label>
            <input v-model="form.test_title" :placeholder="testTitlePlaceholder" />
          </div>
        </div>
      </section>

      <!-- 03 Objetivo + Campos contextuales DINÁMICOS según test_type -->
      <section class="intake-section" v-if="form.test_type_preference">
        <div class="intake-section-head">
          <span class="intake-section-num">03</span>
          <h2>Qué querés aprender</h2>
        </div>

        <div class="intake-field">
          <label>¿Qué querés aprender con este test? *</label>
          <textarea v-model="form.test_objective" rows="3" :placeholder="objectivePlaceholder"></textarea>
        </div>

        <div class="intake-field">
          <label>¿Qué decisión vas a tomar con el resultado?</label>
          <textarea v-model="form.decision_context" rows="2" :placeholder="decisionPlaceholder"></textarea>
        </div>

        <!-- Campos contextuales dinámicos — renderiza lo que el schema del test_type pide -->
        <div v-if="schema.context_fields?.length" class="schema-section-contextual">
          <div class="schema-section-label">Contexto específico de este tipo de test</div>
          <SchemaField
            v-for="f in schema.context_fields"
            :key="f.id"
            :field="f"
            :model-value="form.test_type_specific[f.id]"
            @update:model-value="setTypeSpecific(f.id, $event)"
          />
        </div>
      </section>

      <!-- 04 Producto / marca -->
      <section class="intake-section" v-if="form.test_type_preference">
        <div class="intake-section-head">
          <span class="intake-section-num">04</span>
          <h2>Tu producto, tu marca</h2>
        </div>

        <div class="intake-grid-2">
          <div class="intake-field">
            <label>Producto en foco</label>
            <input v-model="form.product_name" placeholder="ej. PlayStation 6" />
          </div>
          <div class="intake-field">
            <label>Timing de lanzamiento</label>
            <input v-model="form.launch_timing" placeholder="ej. Nov 2027, Q4 2026" />
          </div>
        </div>

        <div class="intake-field">
          <label>Descripción del producto *</label>
          <textarea v-model="form.product_description" rows="4" placeholder="Qué es, para quién..."></textarea>
        </div>

        <div class="intake-field">
          <label>¿Cómo se percibe la marca hoy?</label>
          <textarea v-model="form.brand_positioning" rows="3"></textarea>
        </div>

        <!-- Usa ListBuilder (componente aparte) -->
        <div class="intake-grid-2">
          <div class="intake-field">
            <label>Competencia principal</label>
            <ListBuilder v-model="form.key_competitors" item-placeholder="ej. Microsoft Xbox" />
          </div>
          <div class="intake-field">
            <label>Mercados objetivo</label>
            <ListBuilder v-model="form.markets" item-placeholder="ej. US, UK, JP, MX, BR" />
          </div>
        </div>

        <!-- Usa KeyValueBuilder -->
        <div class="intake-field">
          <label>Hechos clave globales</label>
          <KeyValueBuilder
            v-model="form.key_facts_global"
            key-placeholder="ej. launch_date"
            value-placeholder="ej. Nov 2027"
          />
        </div>
      </section>

      <!-- 06 Audiencia (array de ArchetypeCard dinámicos) -->
      <section class="intake-section" v-if="form.test_type_preference">
        <div class="intake-section-head">
          <span class="intake-section-num">{{ isScenarioMode ? '06' : '05' }}</span>
          <h2>A quién querés testear</h2>
        </div>

        <div class="intake-field">
          <label>Descripción general del buyer / audiencia *</label>
          <textarea v-model="form.target_audience_description" rows="3"></textarea>
        </div>

        <div class="intake-field">
          <label>Arquetipos que querés ver representados</label>
          <div class="archetype-list">
            <ArchetypeCard
              v-for="(a, i) in form.desired_archetypes"
              :key="i"
              :archetype="a"
              :index="i"
              :start-open="!a.name"
              @update="updateArchetype(i, $event)"
              @remove="removeArchetype(i)"
            />
          </div>
          <button @click="addArchetype" class="intake-add" type="button">
            + Agregar arquetipo
          </button>
        </div>

        <div class="intake-grid-2">
          <div class="intake-field">
            <label>Must include</label>
            <ListBuilder v-model="form.must_include_archetypes" item-placeholder="ej. Al menos 3 mujeres > 50 años" />
          </div>
          <div class="intake-field">
            <label>Must exclude</label>
            <ListBuilder v-model="form.must_exclude_archetypes" />
          </div>
        </div>

        <div class="intake-field" style="max-width: 260px;">
          <label>Tamaño de audiencia (cant. agentes)</label>
          <input type="number" v-model.number="form.audience_size_hint" min="20" max="200" placeholder="80" />
          <div class="intake-help">Default 80. Máximo 200.</div>
        </div>
      </section>

      <!-- 08 Variantes (array de variants con SchemaField dinámicos por test_type) -->
      <section class="intake-section" v-if="form.test_type_preference">
        <div class="intake-section-head">
          <span class="intake-section-num">08</span>
          <h2>{{ schema.variant_noun_plural }} a comparar</h2>
        </div>
        <p class="intake-section-sub">
          {{ schema.variant_helper }}
          Mínimo {{ schema.variant_min }}, máximo {{ schema.variant_max }}.
        </p>

        <div v-for="(v, i) in form.variants" :key="i" class="intake-variant">
          <div class="intake-variant-head">
            <h3>
              {{ schema.variant_noun }} {{ String.fromCharCode(65 + i) }}
              <span v-if="v.name" class="variant-name-inline">· {{ v.name }}</span>
            </h3>
            <button
              v-if="form.variants.length > schema.variant_min"
              @click="removeVariant(i)"
              class="intake-remove"
            >× Eliminar</button>
          </div>

          <SchemaField
            v-for="f in schema.variant_fields"
            :key="f.id"
            :field="f"
            :model-value="getVariantField(i, f)"
            @update:model-value="setVariantField(i, f, $event)"
          />

          <div class="intake-field">
            <label>Descripción / rationale *</label>
            <textarea :value="v.description" @input="setVariantDesc(i, $event.target.value)" rows="3"></textarea>
          </div>
        </div>

        <button v-if="form.variants.length < schema.variant_max" @click="addVariant" class="intake-add">
          + Agregar {{ schema.variant_noun.toLowerCase() }}
        </button>
      </section>

      <!-- Footer con auto-save status + submit buttons -->
      <footer class="intake-footer">
        <div class="intake-footer-status">{{ validationHint }}</div>
        <div class="intake-footer-actions">
          <button @click="saveNow" :disabled="saving" class="sharpz-btn">
            {{ saving ? 'Guardando…' : 'Guardar borrador' }}
          </button>
          <button @click="submitIntake" :disabled="!canSubmit || submitting" class="sharpz-btn sharpz-btn-accent">
            {{ submitting ? 'Enviando…' : 'Enviar intake' }}
          </button>
        </div>
      </footer>
      </template>
    </main>
  </div>
</template>
```

---

## Archivo 3/6 · `ClientIntake.vue` — styles

```css
/* ═══════════════════════════════════════════════════════════════════
   Sharpz Analytics — Client Intake (dark theme, coherente con landing)

   Design language: mismo stack que sharpzanalytics.com:
   - fondo #0a0a0a con grays escalonados
   - Space Grotesk para UI/titulares, JetBrains Mono para IDs/tags
   - acentos blanco-off (#e0e0e0), sin colores saturados
   - mucho whitespace, bordes sutiles (1px en gray-3)

   Las CSS custom properties están scoped al .intake-page y se
   cascadean por DOM a los sub-componentes.
   ═══════════════════════════════════════════════════════════════════ */

@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

.intake-page {
  --bg: #0a0a0a;
  --fg: #ffffff;
  --gray-1: #141414;
  --gray-2: #1f1f1f;
  --gray-3: #2a2a2a;
  --gray-4: #444444;
  --gray-5: #666666;
  --gray-6: #999999;
  --accent: #e0e0e0;
  --accent-dim: #888888;
  --danger: #d46060;

  min-height: 100vh;
  background: var(--bg);
  color: var(--fg);
  font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
  -webkit-font-smoothing: antialiased;
}

/* Hero */
.intake-hero {
  background: var(--bg);
  color: var(--fg);
  padding: 80px 24px 56px;
  border-bottom: 1px solid var(--gray-2);
}
.intake-hero-inner { max-width: 860px; margin: 0 auto; }

.intake-brand-tag {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 11px;
  letter-spacing: 0.28em;
  text-transform: uppercase;
  color: var(--gray-6);
  margin-bottom: 24px;
}

.intake-hero h1 {
  font-size: clamp(2.25rem, 5.5vw, 3.75rem);
  font-weight: 700;
  letter-spacing: -0.03em;
  line-height: 1.05;
  margin: 0 0 20px;
  background: linear-gradient(180deg, #ffffff 0%, #888888 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.intake-hero-lead {
  font-size: 17px;
  line-height: 1.6;
  color: var(--gray-6);
  margin: 0 0 28px;
  max-width: 640px;
  font-weight: 300;
}

.intake-id {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 11px;
  color: var(--gray-5);
  border-top: 1px solid var(--gray-2);
  padding-top: 16px;
  letter-spacing: 0.04em;
}
.intake-id code {
  background: var(--gray-1);
  padding: 3px 10px;
  border-radius: 3px;
  border: 1px solid var(--gray-3);
  color: var(--accent);
  margin: 0 6px;
}

/* Main layout */
.intake-main { max-width: 860px; margin: 0 auto; padding: 40px 24px 96px; }

.intake-section {
  background: var(--gray-1);
  border: 1px solid var(--gray-2);
  border-radius: 8px;
  padding: 40px 36px;
  margin-bottom: 24px;
}
.intake-section-head {
  display: flex;
  align-items: baseline;
  gap: 16px;
  margin-bottom: 12px;
}
.intake-section-num {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 12px;
  color: var(--gray-5);
  letter-spacing: 0.18em;
}
.intake-section h2 {
  font-size: 26px;
  margin: 0;
  font-weight: 600;
  letter-spacing: -0.02em;
  color: var(--fg);
}
.intake-section-sub {
  font-size: 14px;
  color: var(--gray-6);
  margin: 0 0 32px;
  max-width: 680px;
  line-height: 1.6;
  font-weight: 300;
}

/* Fields */
.intake-field { margin-bottom: 22px; }
.intake-field label {
  display: block;
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 10px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: var(--gray-6);
  margin-bottom: 8px;
}
.intake-field input,
.intake-field textarea,
.intake-field select {
  width: 100%;
  font-family: inherit;
  font-size: 15px;
  padding: 11px 14px;
  border: 1px solid var(--gray-3);
  border-radius: 4px;
  background: var(--bg);
  color: var(--fg);
  transition: border-color 0.15s, background 0.15s;
}
.intake-field input:focus,
.intake-field textarea:focus,
.intake-field select:focus {
  outline: none;
  border-color: var(--accent);
  background: var(--gray-1);
}
.intake-field textarea {
  resize: vertical;
  min-height: 72px;
  font-family: inherit;
  line-height: 1.5;
}
.intake-field select {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%23999' stroke-width='2'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 14px center;
  padding-right: 40px;
  cursor: pointer;
}
.intake-help {
  font-size: 12px;
  color: var(--gray-5);
  margin: 6px 0 10px;
  line-height: 1.55;
  font-weight: 300;
}

.intake-grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
@media (max-width: 640px) { .intake-grid-2 { grid-template-columns: 1fr; } }

/* Test type selector cards */
.test-type-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-top: 8px;
}
.test-type-card {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 18px;
  border: 1px solid var(--gray-3);
  border-radius: 6px;
  background: var(--bg);
  cursor: pointer;
  transition: all 0.15s;
}
.test-type-card:hover {
  border-color: var(--gray-5);
  background: var(--gray-2);
}
.test-type-card.selected {
  border-color: var(--accent);
  background: var(--gray-2);
}
.test-type-card input[type="radio"] {
  margin-top: 4px;
  accent-color: var(--accent);
  flex-shrink: 0;
}
.test-type-label strong {
  display: block;
  font-size: 14px;
  color: var(--fg);
  margin-bottom: 4px;
  font-weight: 600;
}
.test-type-desc {
  font-size: 12px;
  color: var(--gray-6);
  margin-bottom: 6px;
  line-height: 1.5;
  font-weight: 300;
}
.test-type-shape {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 10px;
  color: var(--accent-dim);
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

/* Schema contextual section (dinámica por test_type) */
.schema-section-contextual {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px dashed var(--gray-3);
}
.schema-section-label {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  color: var(--gray-5);
  margin-bottom: 16px;
}

/* Variants */
.intake-variant {
  border: 1px solid var(--gray-3);
  border-radius: 6px;
  padding: 24px;
  margin-bottom: 16px;
  background: var(--bg);
}
.intake-variant-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--gray-2);
}

.intake-remove {
  background: transparent;
  border: 1px solid transparent;
  color: var(--danger);
  font-size: 11px;
  cursor: pointer;
  padding: 4px 10px;
  border-radius: 3px;
}
.intake-remove:hover {
  border-color: var(--danger);
  background: rgba(212, 96, 96, 0.08);
}

/* Add button (dashed border, expands on hover) */
.intake-add {
  width: 100%;
  padding: 14px;
  border: 1px dashed var(--gray-4);
  background: transparent;
  color: var(--gray-6);
  cursor: pointer;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.15s;
}
.intake-add:hover {
  border-color: var(--accent);
  color: var(--accent);
  background: var(--gray-2);
}

/* Footer */
.intake-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 28px 0 0;
  gap: 16px;
  flex-wrap: wrap;
  border-top: 1px solid var(--gray-2);
  margin-top: 8px;
}

/* Submitted state (replaces form after submit) */
.intake-submitted-card {
  background: var(--gray-1);
  border: 1px solid var(--gray-2);
  border-radius: 8px;
  padding: 72px 48px;
  text-align: center;
}
.intake-submitted-card h2 {
  font-size: 36px;
  margin: 0 0 20px;
  color: var(--fg);
  font-weight: 600;
}
.intake-submitted-card p {
  font-size: 15px;
  color: var(--gray-6);
  line-height: 1.7;
  max-width: 480px;
  margin: 0 auto 12px;
  font-weight: 300;
}

/* Buttons */
.sharpz-btn {
  padding: 11px 22px;
  border-radius: 4px;
  border: 1px solid var(--gray-3);
  background: transparent;
  color: var(--fg);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s;
}
.sharpz-btn:hover {
  border-color: var(--gray-5);
  background: var(--gray-2);
}
.sharpz-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.sharpz-btn-accent {
  background: var(--accent);
  color: var(--bg);
  border-color: var(--accent);
  font-weight: 600;
}
.sharpz-btn-accent:hover {
  background: var(--fg);
  border-color: var(--fg);
}

/* Error box */
.sharpz-error-box {
  background: rgba(212, 96, 96, 0.08);
  color: var(--danger);
  border: 1px solid rgba(212, 96, 96, 0.3);
  border-radius: 4px;
  padding: 12px 16px;
  margin-bottom: 20px;
  font-size: 13px;
}

/* Mobile */
@media (max-width: 640px) {
  .intake-hero { padding: 48px 20px 32px; }
  .intake-section { padding: 28px 20px; }
  .intake-main { padding: 24px 16px 80px; }
  .test-type-grid { grid-template-columns: 1fr; }
}
```

---

## Archivo 4/6 · `ArchetypeCard.vue` — editor de archetypes colapsables

**Comportamiento:** cada ArchetypeCard se expande/colapsa al clickear el header. Muestra preview con nombre + bits clave (age/location/role/vocal). Expandido: form completo con secciones de Identidad / Demografía / Psicografía / Relación con categoría / Voz / Rol en test.

```vue
<template>
  <div class="archetype-card" :class="{ 'is-open': expanded }">
    <!-- Header / collapsed summary -->
    <div class="archetype-head" @click="expanded = !expanded">
      <div class="archetype-idx">{{ String.fromCharCode(65 + index) }}</div>
      <div class="archetype-summary">
        <strong v-if="a.name">{{ a.name }}</strong>
        <span v-else class="archetype-empty">Arquetipo sin nombre</span>
        <div v-if="previewBits.length" class="archetype-preview">
          {{ previewBits.join(' · ') }}
        </div>
      </div>
      <div class="archetype-actions">
        <button @click.stop="$emit('remove')" class="archetype-remove-btn">×</button>
        <span class="archetype-chevron">{{ expanded ? '▾' : '▸' }}</span>
      </div>
    </div>

    <!-- Expanded body: 5 logical sections -->
    <div v-if="expanded" class="archetype-body">

      <div class="archetype-section-label">Identidad</div>
      <div class="archetype-grid-2">
        <div class="archetype-field">
          <label>Nombre / alias *</label>
          <input :value="a.name" @input="update('name', $event.target.value)" />
        </div>
        <div class="archetype-field">
          <label>Etiqueta corta</label>
          <input :value="a.short_label" @input="update('short_label', $event.target.value)" />
        </div>
      </div>

      <div class="archetype-section-label">Demografía</div>
      <div class="archetype-grid-3">
        <!-- Edad, Género, Ubicación, Ocupación, Income -->
      </div>

      <div class="archetype-section-label">Psicografía</div>
      <!-- Motivaciones, Frustraciones, Valores -->

      <div class="archetype-section-label">Relación con tu categoría / marca</div>
      <!-- Historia, brand_affinity select, price_sensitivity select -->

      <div class="archetype-section-label">Voz del arquetipo</div>
      <div class="archetype-field">
        <label>Cita arquetípica</label>
        <input :value="a.archetypal_quote"
          placeholder='"Para mí PlayStation no es una consola, es identidad"' />
      </div>

      <div class="archetype-section-label">Rol en el test</div>
      <div class="archetype-grid-2">
        <!-- Role select: hardcore/mainstream/skeptic/advocate/laggard/influencer -->
        <!-- must_be_vocal checkbox -->
      </div>
    </div>
  </div>
</template>
```

**Styles signature:**
```css
.archetype-card {
  border: 1px solid var(--gray-3);
  border-radius: 6px;
  background: var(--bg);
  margin-bottom: 10px;
  overflow: hidden;
  transition: border-color 0.15s, background 0.15s;
}
.archetype-card.is-open {
  border-color: var(--accent);
  background: var(--gray-2);
}

.archetype-idx {
  /* Letter badge A/B/C in circle */
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: var(--accent);
  color: var(--bg);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 12px;
  font-family: 'JetBrains Mono', monospace;
}
.archetype-card.is-open .archetype-idx {
  background: var(--fg);
}

.archetype-section-label {
  /* Small caps divider label */
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  color: var(--gray-5);
  margin: 22px 0 10px 0;
}

/* Fields follow same pattern as .intake-field but smaller */
.archetype-field input, textarea, select {
  font-size: 13px;      /* vs 15px en intake-field */
  padding: 9px 12px;    /* vs 11px 14px */
  border-radius: 3px;   /* vs 4px */
  background: var(--gray-1);
}
```

---

## Archivo 5/6 · `ListBuilder.vue` — editor row-by-row de List<string>

**Comportamiento:** cada item es su propio input. Enter avanza al siguiente. Phantom row al final (placeholder: "empezá a escribir para agregar") se vuelve real cuando escribís. Eliminar con ×.

```vue
<template>
  <div class="list-builder">
    <div v-for="(row, i) in rowsWithPhantom" :key="i" class="list-row" :class="{ 'list-row-phantom': row.phantom }">
      <span class="list-bullet">{{ row.phantom ? '+' : i + 1 }}</span>
      <input
        :value="row.value"
        @input="updateRow(i, $event.target.value)"
        @keyup.enter="focusNext($event)"
        class="list-input"
        :placeholder="row.phantom ? addHint : itemPlaceholder"
      />
      <button v-if="!row.phantom" @click="removeRow(i)" class="list-remove">×</button>
      <span v-else class="list-filler"></span>
    </div>
  </div>
</template>
```

**Styles signature:**
```css
.list-builder {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.list-row {
  display: flex;
  gap: 10px;
  align-items: center;
}
.list-bullet {
  /* Numbered pseudo-gutter on the left */
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  color: var(--gray-5);
  width: 22px;
  text-align: right;
  flex-shrink: 0;
}
.list-input {
  flex: 1;
  font-size: 14px;
  padding: 9px 12px;
  border: 1px solid var(--gray-3);
  border-radius: 3px;
  background: var(--bg);
  color: var(--fg);
}
.list-row-phantom .list-input {
  background: transparent;
  border-style: dashed;
  font-style: italic;
  color: var(--gray-6);
}
```

---

## Archivo 6/6 · `KeyValueBuilder.vue` + `SchemaField.vue`

### KeyValueBuilder (edita Dict<string, string>)

**Comportamiento:** grid de 2 columnas (Clave | Valor) + header con labels + remove por row. Phantom row al final para add rápido. Usado en `key_facts_global`.

```vue
<template>
  <div class="kv-builder">
    <div class="kv-header" v-if="rows.length > 0 || allowEmpty">
      <div class="kv-col-key">{{ keyLabel }}</div>
      <div class="kv-col-value">{{ valueLabel }}</div>
      <div class="kv-col-actions"></div>
    </div>
    <div v-for="(row, i) in rowsWithPhantom" :key="i" class="kv-row" :class="{ 'kv-row-phantom': row.phantom }">
      <input :value="row.key"   class="kv-input kv-col-key"   :placeholder="keyPlaceholder" />
      <input :value="row.value" class="kv-input kv-col-value" :placeholder="valuePlaceholder" />
      <button v-if="!row.phantom" @click="removeRow(i)" class="kv-remove">×</button>
      <span v-else class="kv-add-hint">(empezá a escribir para agregar)</span>
    </div>
  </div>
</template>
```

**Styles signature:**
```css
.kv-builder {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.kv-header, .kv-row {
  display: grid;
  grid-template-columns: 1fr 1.6fr 40px; /* key más angosto, value más ancho */
  gap: 8px;
}
.kv-header {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: var(--gray-5);
  margin-bottom: 2px;
}
.kv-input {
  font-family: 'JetBrains Mono', monospace; /* diff from regular field — monospace para datos */
  font-size: 13px;
  padding: 9px 12px;
  border: 1px solid var(--gray-3);
  border-radius: 3px;
  background: var(--bg);
  color: var(--fg);
}
.kv-row-phantom .kv-input {
  background: transparent;
  border-style: dashed;
  color: var(--gray-6);
}
```

### SchemaField (router de tipos dinámicos según schema del backend)

Recibe un `field` del backend con `{id, label, type, placeholder, hint, required, options}` donde `type ∈ {string, text, select, number, multiline_list, urls_list, key_value_dict}` y renderiza el input apropiado. Es el "dynamic form generator" para campos contextuales por test_type.

```vue
<template>
  <div class="schema-field">
    <label class="schema-label">
      {{ field.label }}
      <span v-if="field.required" class="schema-required">*</span>
    </label>

    <input    v-if="field.type === 'string'"       type="text" />
    <textarea v-else-if="field.type === 'text'"    rows="3" />
    <select   v-else-if="field.type === 'select'">
      <option v-for="opt in field.options" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
    </select>
    <input    v-else-if="field.type === 'number'"  type="number" />
    <ListBuilder      v-else-if="field.type === 'multiline_list'" />
    <ListBuilder      v-else-if="field.type === 'urls_list'" />
    <KeyValueBuilder  v-else-if="field.type === 'key_value_dict'" />
    <input    v-else type="text" /> <!-- fallback -->

    <div v-if="field.hint" class="schema-hint">{{ field.hint }}</div>
  </div>
</template>
```

**Styles signature:**
```css
.schema-field { margin-bottom: 22px; }
.schema-label {
  display: block;
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: var(--gray-6);
  margin-bottom: 8px;
}
.schema-required {
  color: var(--accent);
  margin-left: 4px;
  font-weight: 700;
}
.schema-input, .schema-textarea, .schema-select {
  /* Igual que .intake-field input */
  width: 100%;
  font-size: 15px;
  padding: 11px 14px;
  border: 1px solid var(--gray-3);
  border-radius: 4px;
  background: var(--bg);
  color: var(--fg);
}
```

---

## Resumen del design language del intake (para V2 replicate o rethink)

**Ethos:** Form denso pero respiración. "Serious but approachable." Operator-tech aesthetic (mucho mono-space) sobre dark theme heredado de la landing.

**Paleta del intake (inline vars, distinto de tokens.css de reportes):**
- `#0a0a0a` bg
- `#141414` gray-1 (section cards)
- `#1f1f1f` gray-2 (inner highlights)
- `#2a2a2a` gray-3 (borders)
- `#666666` / `#999999` gray-5 / gray-6 (text secondary)
- `#e0e0e0` accent (borders activos, CTA hover)
- `#d46060` danger (remove buttons)

**Tipografía:**
- `Space Grotesk` para UI text (body 15px, h2 26px, h1 48-60px)
- `JetBrains Mono` para **labels** (10-11px, uppercase, letter-spacing 0.18em), IDs, tags, numbered bullets
- Weight 300 para body text (muy fino, lujoso), 600 para headers

**Patterns clave:**
- **Sections numeradas 01-09** con "section-num" en mono-space + h2 serif-weight
- **Cards (`.intake-section`)** con bg gray-1 + border gray-2 + padding 40-36 + margin-bottom 24
- **Labels en uppercase mono-space 10px** (no estándar, es la firma del design)
- **Inputs con focus → border accent + bg gray-1**
- **Grids 2-cols** que colapsan a 1-col en mobile (640px)
- **Dashed borders** para "add new" buttons y phantom rows
- **CTAs:** `sharpz-btn` (outline) y `sharpz-btn-accent` (white solid, bold)
- **Dynamic fields:** SchemaField renderiza campos del schema del backend (polimórfico)
- **Collapsable cards** (ArchetypeCard) con A/B/C index badge + chevron

**Responsive:** max-width 860px en desktop, grid 2-col → 1-col a 640px, padding ajustado en mobile.

**Bounce from the form:**
- Auto-save con indicador textual ("Guardando…" / "Guardado a las 14:23")
- Intake ID visible en el hero (`code` styled)
- Footer sticky con validation hint + save + submit buttons
- Submitted state reemplaza todo con una card success centrada

---

## Nota sobre integración con backend V2

El intake form actualmente hace auto-save cada N segundos via `PATCH /api/sharpz/intakes/:id` y submitea con `POST /api/sharpz/intakes/:id/submit`. El schema que envía:

```typescript
{
  // Section 01
  company_name: string
  contact_name: string
  contact_email: string
  contact_role: string

  // Section 02
  test_type_preference: string  // one of the 15 test_types
  test_title: string

  // Section 03
  test_objective: string
  decision_context: string
  test_type_specific: Record<string, any>  // dynamic por test_type

  // Section 04
  product_name: string
  product_description: string
  launch_timing: string
  brand_positioning: string
  key_competitors: string[]
  markets: string[]
  key_facts_global: Record<string, string>

  // Section 05 (conditional — solo scenario mode)
  scenario: Record<string, any>

  // Section 06
  target_audience_description: string
  desired_archetypes: Archetype[]  // see ArchetypeCard
  must_include_archetypes: string[]
  must_exclude_archetypes: string[]
  audience_size_hint: number

  // Section 07
  hypotheses: string[]
  success_metrics: string[]
  expected_risks: string

  // Section 08
  variants: Variant[]  // dynamic fields por test_type

  // Section 09
  client_logo_url: string
  client_primary_color: string  // hex
  sensitive_topics_to_avoid: string
  legal_constraints: string
  reference_urls: string[]
}
```

El backend V2 debe ser API-compatible con este payload para que el intake existente siga funcionando sin re-deploy del frontend.
