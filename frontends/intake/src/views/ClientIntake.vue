<script setup>
import { computed, onMounted, onUnmounted, reactive, ref, watch } from 'vue';
import { intakeApi } from '../api/intake.js';
import { TEST_TYPES, TEST_TYPES_BY_VALUE } from '../data/test_types.js';
import ArchetypeCard from '../components/ArchetypeCard.vue';
import ListBuilder from '../components/ListBuilder.vue';
import KeyValueBuilder from '../components/KeyValueBuilder.vue';
import IntakeSubmitted from './IntakeSubmitted.vue';

const props = defineProps({
  intakeId: { type: String, required: true },
});

const loading = ref(true);
const error = ref(null);
const saving = ref(false);
const savedAt = ref(null);
const submitting = ref(false);
const submitErrors = ref([]);

// Local state of the intake — mirrors the backend shape. Only fields we
// touch are PATCHed; auto-save is debounced.
const form = reactive({
  company_name: '',
  contact_name: '',
  contact_email: '',
  contact_role: '',
  test_type_preference: '',
  test_title: '',
  test_objective: '',
  decision_context: '',
  test_type_specific: {},
  product_name: '',
  product_description: '',
  launch_timing: '',
  brand_positioning: '',
  key_competitors: [],
  markets: [],
  key_facts_global: {},
  target_audience_description: '',
  desired_archetypes: [],
  must_include_archetypes: [],
  must_exclude_archetypes: [],
  audience_size_hint: 80,
  hypotheses: [],
  success_metrics: [],
  expected_risks: '',
  variants: [],
  client_logo_url: '',
  client_primary_color: '',
  sensitive_topics_to_avoid: '',
  legal_constraints: '',
  reference_urls: [],
});

const status = ref('draft');
const remoteIntake = ref(null); // full last-synced intake

const selectedTestType = computed(
  () => TEST_TYPES_BY_VALUE[form.test_type_preference] || null
);

const savingLabel = computed(() => {
  if (saving.value) return 'Guardando…';
  if (savedAt.value) {
    const h = savedAt.value.getHours().toString().padStart(2, '0');
    const m = savedAt.value.getMinutes().toString().padStart(2, '0');
    return `Guardado a las ${h}:${m}`;
  }
  return '';
});

const canSubmit = computed(() => {
  return (
    form.company_name.trim() &&
    form.contact_name.trim() &&
    form.contact_email.trim() &&
    form.test_type_preference &&
    form.test_title.trim() &&
    form.test_objective.trim().length > 50 &&
    form.product_description.trim().length > 100 &&
    form.desired_archetypes.length >= 4 &&
    form.variants.length >= 1
  );
});

const validationHint = computed(() => {
  if (canSubmit.value) return 'Listo para enviar.';
  const missing = [];
  if (!form.company_name.trim()) missing.push('empresa');
  if (!form.contact_email.trim()) missing.push('email');
  if (!form.test_type_preference) missing.push('tipo de test');
  if (form.test_objective.trim().length <= 50) missing.push('objetivo (≥50 palabras)');
  if (form.desired_archetypes.length < 4) missing.push('≥4 arquetipos');
  if (form.variants.length < 1) missing.push('≥1 variante');
  return `Faltan: ${missing.join(', ')}`;
});

// ---- Load ----
onMounted(async () => {
  try {
    const intake = await intakeApi.get(props.intakeId);
    applyRemote(intake);
  } catch (err) {
    error.value = err?.response?.data?.detail ?? err.message ?? 'No se pudo cargar el intake';
  } finally {
    loading.value = false;
  }
});

function applyRemote(intake) {
  remoteIntake.value = intake;
  status.value = intake.status;
  for (const key of Object.keys(form)) {
    if (key in intake && intake[key] !== null && intake[key] !== undefined) {
      form[key] = intake[key];
    }
  }
}

// ---- Auto-save (debounced) ----
let saveTimer = null;
const PATCH_DEBOUNCE_MS = 1500;
let suppressAutoSave = true; // skip initial load

watch(
  () => ({ ...form }),
  () => {
    if (suppressAutoSave) return;
    if (status.value !== 'draft' && status.value !== 'rejected') return;
    clearTimeout(saveTimer);
    saveTimer = setTimeout(() => doSave(), PATCH_DEBOUNCE_MS);
  },
  { deep: true }
);

// Skip the first reactive trigger that fires from applyRemote.
onMounted(() => {
  setTimeout(() => { suppressAutoSave = false; }, 500);
});

async function doSave() {
  if (saving.value) return;
  saving.value = true;
  try {
    const payload = buildPatch();
    const updated = await intakeApi.patch(props.intakeId, payload);
    applyRemote(updated);
    savedAt.value = new Date();
  } catch (err) {
    console.error('auto-save error', err);
  } finally {
    saving.value = false;
  }
}

function buildPatch() {
  // Send all fields; backend merges (exclude_none at its side).
  return {
    company_name: form.company_name,
    contact_name: form.contact_name,
    contact_email: form.contact_email,
    contact_role: form.contact_role,
    test_type_preference: form.test_type_preference,
    test_title: form.test_title,
    test_objective: form.test_objective,
    decision_context: form.decision_context,
    test_type_specific: form.test_type_specific,
    product_name: form.product_name,
    product_description: form.product_description,
    launch_timing: form.launch_timing,
    brand_positioning: form.brand_positioning,
    key_competitors: form.key_competitors,
    markets: form.markets,
    key_facts_global: form.key_facts_global,
    target_audience_description: form.target_audience_description,
    desired_archetypes: form.desired_archetypes,
    must_include_archetypes: form.must_include_archetypes,
    must_exclude_archetypes: form.must_exclude_archetypes,
    audience_size_hint: form.audience_size_hint,
    hypotheses: form.hypotheses,
    success_metrics: form.success_metrics,
    expected_risks: form.expected_risks,
    variants: form.variants,
    client_logo_url: form.client_logo_url,
    client_primary_color: form.client_primary_color,
    sensitive_topics_to_avoid: form.sensitive_topics_to_avoid,
    legal_constraints: form.legal_constraints,
    reference_urls: form.reference_urls,
  };
}

onUnmounted(() => { clearTimeout(saveTimer); });

// ---- Archetypes ----
function addArchetype() {
  form.desired_archetypes = [...form.desired_archetypes, { name: '', short_label: '' }];
}
function updateArchetype(i, updated) {
  const next = [...form.desired_archetypes];
  next[i] = updated;
  form.desired_archetypes = next;
}
function removeArchetype(i) {
  const next = [...form.desired_archetypes];
  next.splice(i, 1);
  form.desired_archetypes = next;
}

// ---- Variants ----
function addVariant() {
  form.variants = [...form.variants, { name: '', description: '' }];
}
function updateVariantField(i, field, value) {
  const next = [...form.variants];
  next[i] = { ...next[i], [field]: value };
  form.variants = next;
}
function removeVariant(i) {
  const next = [...form.variants];
  next.splice(i, 1);
  form.variants = next;
}

// ---- Submit ----
async function saveNow() {
  clearTimeout(saveTimer);
  await doSave();
}

async function submitIntake() {
  if (!canSubmit.value || submitting.value) return;
  submitting.value = true;
  submitErrors.value = [];
  try {
    // Force final save first
    await doSave();
    const result = await intakeApi.submit(props.intakeId);
    if (result.ok) {
      status.value = result.data.status;
      // Reload the full intake for the submitted state
      const intake = await intakeApi.get(props.intakeId);
      applyRemote(intake);
    } else {
      submitErrors.value = result.errors;
    }
  } catch (err) {
    submitErrors.value = [err?.message ?? 'Error desconocido'];
  } finally {
    submitting.value = false;
  }
}

const isSubmitted = computed(
  () => status.value === 'submitted' || status.value === 'approved' || status.value === 'completed'
);
</script>

<template>
  <div class="intake-page">
    <!-- Hero -->
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
      <div v-if="loading" class="sharpz-info-box">Cargando intake…</div>
      <div v-else-if="error" class="sharpz-error-box">{{ error }}</div>

      <IntakeSubmitted v-else-if="isSubmitted" :intake="remoteIntake" />

      <template v-else>
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
              <label>Email *</label>
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
            El tipo de test determina qué preguntas te vamos a hacer y cómo estructuramos las variantes.
          </p>

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
              <input v-model="form.test_title" placeholder="ej. McAllister Burger · Pricing AR Q2 2026" />
            </div>
          </div>
        </section>

        <!-- 03 Qué querés aprender -->
        <section v-if="form.test_type_preference" class="intake-section">
          <div class="intake-section-head">
            <span class="intake-section-num">03</span>
            <h2>Qué querés aprender</h2>
          </div>
          <div class="intake-field">
            <label>¿Qué querés aprender con este test? *</label>
            <textarea
              v-model="form.test_objective"
              rows="3"
              placeholder="Describí en 3-5 oraciones qué pregunta concreta querés responder."
            />
            <div class="intake-help">Mínimo 50 palabras. Entre más específico, mejor el reporte.</div>
          </div>
          <div class="intake-field">
            <label>¿Qué decisión vas a tomar con el resultado?</label>
            <textarea
              v-model="form.decision_context"
              rows="2"
              placeholder="ej. decidir si lanzamos en Q2 o pivoteamos al framing B"
            />
          </div>
        </section>

        <!-- 04 Producto / marca -->
        <section v-if="form.test_type_preference" class="intake-section">
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
            <textarea
              v-model="form.product_description"
              rows="4"
              placeholder="Qué es, para quién, qué problema resuelve, qué lo hace diferente."
            />
            <div class="intake-help">Mínimo 100 caracteres.</div>
          </div>
          <div class="intake-field">
            <label>¿Cómo se percibe la marca hoy?</label>
            <textarea v-model="form.brand_positioning" rows="3" />
          </div>
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
          <div class="intake-field">
            <label>Hechos clave globales</label>
            <KeyValueBuilder
              v-model="form.key_facts_global"
              key-placeholder="ej. launch_date"
              value-placeholder="ej. Nov 2027"
            />
          </div>
        </section>

        <!-- 05 Audiencia -->
        <section v-if="form.test_type_preference" class="intake-section">
          <div class="intake-section-head">
            <span class="intake-section-num">05</span>
            <h2>A quién querés testear</h2>
          </div>
          <div class="intake-field">
            <label>Descripción general del buyer / audiencia *</label>
            <textarea
              v-model="form.target_audience_description"
              rows="3"
              placeholder="Un párrafo sobre la audiencia central. Demografía, intereses, contexto."
            />
          </div>
          <div class="intake-field">
            <label>Arquetipos que querés ver representados (mín 4)</label>
            <div class="archetype-list">
              <ArchetypeCard
                v-for="(a, i) in form.desired_archetypes"
                :key="i"
                :archetype="a"
                :index="i"
                :start-open="!a.name"
                @update="(u) => updateArchetype(i, u)"
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
              <ListBuilder
                v-model="form.must_include_archetypes"
                item-placeholder="ej. Al menos 3 mujeres > 50 años"
              />
            </div>
            <div class="intake-field">
              <label>Must exclude</label>
              <ListBuilder v-model="form.must_exclude_archetypes" />
            </div>
          </div>
          <div class="intake-field" style="max-width: 260px;">
            <label>Tamaño de audiencia (cant. agentes)</label>
            <input type="number" v-model.number="form.audience_size_hint" min="20" max="2000" placeholder="80" />
            <div class="intake-help">
              Default 80. Máximo depende del test_type (hasta 2000 para survey/forecast).
            </div>
          </div>
        </section>

        <!-- 06 Hipótesis y éxito -->
        <section v-if="form.test_type_preference" class="intake-section">
          <div class="intake-section-head">
            <span class="intake-section-num">06</span>
            <h2>Hipótesis y éxito</h2>
          </div>
          <div class="intake-field">
            <label>Hipótesis que estás testeando</label>
            <ListBuilder v-model="form.hypotheses" item-placeholder="ej. LP institucionales van a objetar la fee structure" />
          </div>
          <div class="intake-field">
            <label>Métricas de éxito</label>
            <ListBuilder v-model="form.success_metrics" item-placeholder="ej. ≥60% intent-to-follow-up" />
          </div>
          <div class="intake-field">
            <label>Riesgos o temas sensibles a anticipar</label>
            <textarea v-model="form.expected_risks" rows="2" />
          </div>
        </section>

        <!-- 07 Variantes -->
        <section v-if="form.test_type_preference" class="intake-section">
          <div class="intake-section-head">
            <span class="intake-section-num">07</span>
            <h2>Variantes a comparar</h2>
          </div>
          <p class="intake-section-sub">
            Mínimo 1, máximo 5 dependiendo del test_type. Las variantes se corren sobre la misma audiencia.
          </p>
          <div v-for="(v, i) in form.variants" :key="i" class="intake-variant">
            <div class="intake-variant-head">
              <h3>
                Variante {{ String.fromCharCode(65 + i) }}
                <span v-if="v.name" class="variant-name-inline">· {{ v.name }}</span>
              </h3>
              <button @click="removeVariant(i)" class="intake-remove" type="button">
                × Eliminar
              </button>
            </div>
            <div class="intake-field">
              <label>Nombre de la variante *</label>
              <input
                :value="v.name"
                @input="updateVariantField(i, 'name', $event.target.value)"
                placeholder="ej. $19.900 ARS"
              />
            </div>
            <div class="intake-field">
              <label>Descripción / rationale *</label>
              <textarea
                :value="v.description"
                @input="updateVariantField(i, 'description', $event.target.value)"
                rows="3"
              />
            </div>
          </div>
          <button @click="addVariant" class="intake-add" type="button">
            + Agregar variante
          </button>
        </section>

        <!-- 08 Branding -->
        <section v-if="form.test_type_preference" class="intake-section">
          <div class="intake-section-head">
            <span class="intake-section-num">08</span>
            <h2>Branding & restricciones</h2>
          </div>
          <div class="intake-grid-2">
            <div class="intake-field">
              <label>Logo URL (opcional)</label>
              <input v-model="form.client_logo_url" placeholder="https://..." />
              <div class="intake-help">Aparece arriba del deliverable.</div>
            </div>
            <div class="intake-field">
              <label>Color primario (hex)</label>
              <input v-model="form.client_primary_color" placeholder="#FFC72C" />
              <div class="intake-help">Afecta brand tag + links + winner chip del reporte.</div>
            </div>
          </div>
          <div class="intake-field">
            <label>Temas sensibles a evitar</label>
            <textarea v-model="form.sensitive_topics_to_avoid" rows="2" />
          </div>
          <div class="intake-field">
            <label>Restricciones legales / NDA</label>
            <textarea v-model="form.legal_constraints" rows="2" />
          </div>
          <div class="intake-field">
            <label>URLs de referencia</label>
            <ListBuilder v-model="form.reference_urls" item-placeholder="https://..." />
          </div>
        </section>

        <!-- Footer: save + submit -->
        <footer class="intake-footer">
          <div class="intake-footer-status">{{ validationHint }}</div>
          <div class="intake-footer-actions">
            <button @click="saveNow" :disabled="saving" class="sharpz-btn" type="button">
              {{ saving ? 'Guardando…' : 'Guardar borrador' }}
            </button>
            <button
              @click="submitIntake"
              :disabled="!canSubmit || submitting"
              class="sharpz-btn sharpz-btn-accent"
              type="button"
            >
              {{ submitting ? 'Enviando…' : 'Enviar intake' }}
            </button>
          </div>
        </footer>

        <div v-if="submitErrors.length" class="sharpz-error-box" style="margin-top: 20px;">
          <strong>No pudimos enviarlo todavía:</strong>
          <ul style="margin: 8px 0 0; padding-left: 20px;">
            <li v-for="(err, i) in submitErrors" :key="i">{{ err }}</li>
          </ul>
        </div>
      </template>
    </main>
  </div>
</template>

<style scoped>
.intake-page {
  min-height: 100vh;
  background: #0a0a0a;
  color: #fff;
  font-family: 'Space Grotesk', sans-serif;
}
.intake-hero {
  padding: 80px 24px 56px;
  border-bottom: 1px solid #1f1f1f;
}
.intake-hero-inner { max-width: 860px; margin: 0 auto; }
.intake-brand-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  letter-spacing: 0.28em;
  text-transform: uppercase;
  color: #999;
  margin-bottom: 24px;
}
.intake-hero h1 {
  font-size: clamp(2.25rem, 5.5vw, 3.75rem);
  font-weight: 700;
  letter-spacing: -0.03em;
  line-height: 1.05;
  margin: 0 0 20px;
  background: linear-gradient(180deg, #fff 0%, #888 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.intake-hero-lead {
  font-size: 17px;
  line-height: 1.6;
  color: #999;
  margin: 0 0 28px;
  max-width: 640px;
  font-weight: 300;
}
.intake-id {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: #666;
  border-top: 1px solid #1f1f1f;
  padding-top: 16px;
  letter-spacing: 0.04em;
}
.intake-id code {
  background: #141414;
  padding: 3px 10px;
  border-radius: 3px;
  border: 1px solid #2a2a2a;
  color: #e0e0e0;
  margin: 0 6px;
}
.intake-save-hint { margin-left: 12px; color: #666; font-style: italic; }

.intake-main { max-width: 860px; margin: 0 auto; padding: 40px 24px 96px; }

.intake-section {
  background: #141414;
  border: 1px solid #1f1f1f;
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
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  color: #666;
  letter-spacing: 0.18em;
}
.intake-section h2 {
  font-size: 26px;
  margin: 0;
  font-weight: 600;
  letter-spacing: -0.02em;
  color: #fff;
}
.intake-section-sub {
  font-size: 14px;
  color: #999;
  margin: 0 0 32px;
  max-width: 680px;
  line-height: 1.6;
  font-weight: 300;
}

.intake-field { margin-bottom: 22px; }
.intake-field label {
  display: block;
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: #999;
  margin-bottom: 8px;
}
.intake-field input,
.intake-field textarea,
.intake-field select {
  width: 100%;
  font-family: inherit;
  font-size: 15px;
  padding: 11px 14px;
  border: 1px solid #2a2a2a;
  border-radius: 4px;
  background: #0a0a0a;
  color: #fff;
  transition: border-color 0.15s, background 0.15s;
}
.intake-field input:focus,
.intake-field textarea:focus,
.intake-field select:focus {
  outline: none;
  border-color: #e0e0e0;
  background: #141414;
}
.intake-field textarea { resize: vertical; min-height: 72px; font-family: inherit; line-height: 1.5; }
.intake-help {
  font-size: 12px;
  color: #666;
  margin: 6px 0 10px;
  line-height: 1.55;
  font-weight: 300;
}

.intake-grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
@media (max-width: 640px) { .intake-grid-2 { grid-template-columns: 1fr; } }

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
  border: 1px solid #2a2a2a;
  border-radius: 6px;
  background: #0a0a0a;
  cursor: pointer;
  transition: all 0.15s;
}
.test-type-card:hover {
  border-color: #666;
  background: #1f1f1f;
}
.test-type-card.selected {
  border-color: #e0e0e0;
  background: #1f1f1f;
}
.test-type-card input[type="radio"] {
  margin-top: 4px;
  accent-color: #e0e0e0;
  flex-shrink: 0;
  width: auto;
}
.test-type-label strong {
  display: block;
  font-size: 14px;
  color: #fff;
  margin-bottom: 4px;
  font-weight: 600;
}
.test-type-desc {
  font-size: 12px;
  color: #999;
  margin-bottom: 6px;
  line-height: 1.5;
  font-weight: 300;
}
.test-type-shape {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  color: #888;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.intake-variant {
  border: 1px solid #2a2a2a;
  border-radius: 6px;
  padding: 24px;
  margin-bottom: 16px;
  background: #0a0a0a;
}
.intake-variant-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 14px;
  border-bottom: 1px solid #1f1f1f;
}
.intake-variant-head h3 { font-size: 15px; font-weight: 600; margin: 0; }
.variant-name-inline { color: #999; font-weight: 400; margin-left: 4px; }

.intake-remove {
  background: transparent;
  border: 1px solid transparent;
  color: #d46060;
  font-size: 11px;
  cursor: pointer;
  padding: 4px 10px;
  border-radius: 3px;
}
.intake-remove:hover {
  border-color: #d46060;
  background: rgba(212, 96, 96, 0.08);
}

.intake-add {
  width: 100%;
  padding: 14px;
  border: 1px dashed #444;
  background: transparent;
  color: #999;
  cursor: pointer;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.15s;
}
.intake-add:hover {
  border-color: #e0e0e0;
  color: #e0e0e0;
  background: #1f1f1f;
}

.intake-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 28px 0 0;
  gap: 16px;
  flex-wrap: wrap;
  border-top: 1px solid #1f1f1f;
  margin-top: 8px;
}
.intake-footer-status {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: #999;
  letter-spacing: 0.04em;
}
.intake-footer-actions { display: flex; gap: 10px; }

.sharpz-btn {
  padding: 11px 22px;
  border-radius: 4px;
  border: 1px solid #2a2a2a;
  background: transparent;
  color: #fff;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s;
}
.sharpz-btn:hover {
  border-color: #666;
  background: #1f1f1f;
}
.sharpz-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.sharpz-btn-accent {
  background: #e0e0e0;
  color: #0a0a0a;
  border-color: #e0e0e0;
  font-weight: 600;
}
.sharpz-btn-accent:hover {
  background: #fff;
  border-color: #fff;
}

.sharpz-error-box {
  background: rgba(212, 96, 96, 0.08);
  color: #d46060;
  border: 1px solid rgba(212, 96, 96, 0.3);
  border-radius: 4px;
  padding: 12px 16px;
  margin-bottom: 20px;
  font-size: 13px;
}
.sharpz-info-box {
  background: #141414;
  color: #999;
  border: 1px solid #1f1f1f;
  border-radius: 4px;
  padding: 20px;
  font-size: 14px;
  text-align: center;
}

@media (max-width: 640px) {
  .intake-hero { padding: 48px 20px 32px; }
  .intake-section { padding: 28px 20px; }
  .intake-main { padding: 24px 16px 80px; }
  .test-type-grid { grid-template-columns: 1fr; }
}
</style>
