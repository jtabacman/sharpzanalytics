<script setup>
import { computed, ref } from 'vue';

const props = defineProps({
  archetype: { type: Object, required: true },
  index: { type: Number, required: true },
  startOpen: { type: Boolean, default: false },
});
const emit = defineEmits(['update', 'remove']);

const expanded = ref(props.startOpen);
const a = computed(() => props.archetype || {});

function update(field, value) {
  emit('update', { ...a.value, [field]: value });
}

const letter = computed(() => String.fromCharCode(65 + props.index));
const previewBits = computed(() =>
  [a.value.age_range, a.value.location, a.value.occupation, a.value.role]
    .filter((x) => x && String(x).trim().length > 0)
);
</script>

<template>
  <div class="archetype-card" :class="{ 'is-open': expanded }">
    <!-- Header / collapsed summary -->
    <div class="archetype-head" @click="expanded = !expanded">
      <div class="archetype-idx">{{ letter }}</div>
      <div class="archetype-summary">
        <strong v-if="a.name">{{ a.name }}</strong>
        <span v-else class="archetype-empty">Arquetipo sin nombre</span>
        <div v-if="previewBits.length" class="archetype-preview">
          {{ previewBits.join(' · ') }}
        </div>
      </div>
      <div class="archetype-actions">
        <button @click.stop="$emit('remove')" class="archetype-remove-btn" type="button">×</button>
        <span class="archetype-chevron">{{ expanded ? '▾' : '▸' }}</span>
      </div>
    </div>

    <!-- Expanded body: 5 logical sections -->
    <div v-if="expanded" class="archetype-body">
      <div class="archetype-section-label">Identidad</div>
      <div class="archetype-grid-2">
        <div class="archetype-field">
          <label>Nombre / alias *</label>
          <input :value="a.name || ''" @input="update('name', $event.target.value)" placeholder="ej. TIAA-Nuveen agri lead" />
        </div>
        <div class="archetype-field">
          <label>Etiqueta corta</label>
          <input :value="a.short_label || ''" @input="update('short_label', $event.target.value)" placeholder="ej. TIAA" />
        </div>
      </div>

      <div class="archetype-section-label">Demografía</div>
      <div class="archetype-grid-3">
        <div class="archetype-field">
          <label>Edad / rango</label>
          <input :value="a.age_range || ''" @input="update('age_range', $event.target.value)" placeholder="ej. 45-55" />
        </div>
        <div class="archetype-field">
          <label>Ubicación</label>
          <input :value="a.location || ''" @input="update('location', $event.target.value)" placeholder="ej. NY, US" />
        </div>
        <div class="archetype-field">
          <label>Ocupación</label>
          <input :value="a.occupation || ''" @input="update('occupation', $event.target.value)" placeholder="ej. Senior PM" />
        </div>
        <div class="archetype-field">
          <label>Género</label>
          <input :value="a.gender || ''" @input="update('gender', $event.target.value)" />
        </div>
        <div class="archetype-field">
          <label>Income level</label>
          <input :value="a.income_level || ''" @input="update('income_level', $event.target.value)" />
        </div>
      </div>

      <div class="archetype-section-label">Psicografía</div>
      <div class="archetype-field">
        <label>Motivaciones</label>
        <textarea :value="a.motivations || ''" @input="update('motivations', $event.target.value)" rows="2" />
      </div>
      <div class="archetype-field">
        <label>Frustraciones</label>
        <textarea :value="a.frustrations || ''" @input="update('frustrations', $event.target.value)" rows="2" />
      </div>
      <div class="archetype-field">
        <label>Valores</label>
        <textarea :value="a.values || ''" @input="update('values', $event.target.value)" rows="2" />
      </div>

      <div class="archetype-section-label">Relación con categoría / marca</div>
      <div class="archetype-field">
        <label>Historia con la categoría</label>
        <textarea :value="a.category_history || ''" @input="update('category_history', $event.target.value)" rows="2" />
      </div>
      <div class="archetype-grid-2">
        <div class="archetype-field">
          <label>Brand affinity</label>
          <select :value="a.brand_affinity || ''" @change="update('brand_affinity', $event.target.value)">
            <option value="">—</option>
            <option value="advocate">advocate</option>
            <option value="user">user</option>
            <option value="lapsed">lapsed</option>
            <option value="aware">aware</option>
            <option value="unaware">unaware</option>
          </select>
        </div>
        <div class="archetype-field">
          <label>Price sensitivity</label>
          <select :value="a.price_sensitivity || ''" @change="update('price_sensitivity', $event.target.value)">
            <option value="">—</option>
            <option value="low">low</option>
            <option value="medium">medium</option>
            <option value="high">high</option>
          </select>
        </div>
      </div>

      <div class="archetype-section-label">Voz del arquetipo</div>
      <div class="archetype-field">
        <label>Cita arquetípica</label>
        <input
          :value="a.archetypal_quote || ''"
          @input="update('archetypal_quote', $event.target.value)"
          placeholder='ej. "Fee transparency es la primera pregunta que hago"'
        />
      </div>

      <div class="archetype-section-label">Rol en el test</div>
      <div class="archetype-grid-2">
        <div class="archetype-field">
          <label>Rol</label>
          <select :value="a.role || ''" @change="update('role', $event.target.value)">
            <option value="">—</option>
            <option value="hardcore">hardcore</option>
            <option value="mainstream">mainstream</option>
            <option value="skeptic">skeptic</option>
            <option value="advocate">advocate</option>
            <option value="laggard">laggard</option>
            <option value="influencer">influencer</option>
          </select>
        </div>
        <div class="archetype-field">
          <label>Must be vocal</label>
          <input
            type="checkbox"
            :checked="!!a.must_be_vocal"
            @change="update('must_be_vocal', $event.target.checked)"
            style="width:auto;"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.archetype-card {
  border: 1px solid #2a2a2a;
  border-radius: 6px;
  background: #0a0a0a;
  margin-bottom: 10px;
  overflow: hidden;
  transition: border-color 0.15s, background 0.15s;
}
.archetype-card.is-open {
  border-color: #e0e0e0;
  background: #1f1f1f;
}

.archetype-head {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  cursor: pointer;
  user-select: none;
}
.archetype-idx {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: #e0e0e0;
  color: #0a0a0a;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 12px;
  font-family: 'JetBrains Mono', monospace;
  flex-shrink: 0;
}
.archetype-card.is-open .archetype-idx { background: #fff; }

.archetype-summary { flex: 1; min-width: 0; }
.archetype-summary strong { font-size: 14px; color: #fff; font-weight: 600; display: block; }
.archetype-empty { color: #888; font-style: italic; font-size: 14px; }
.archetype-preview {
  font-size: 11px;
  color: #888;
  margin-top: 3px;
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: 0.02em;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.archetype-actions { display: flex; align-items: center; gap: 8px; }
.archetype-remove-btn {
  background: transparent;
  border: 1px solid transparent;
  color: #d46060;
  font-size: 16px;
  cursor: pointer;
  padding: 2px 8px;
  border-radius: 3px;
  width: 28px;
}
.archetype-remove-btn:hover {
  border-color: #d46060;
  background: rgba(212, 96, 96, 0.08);
}
.archetype-chevron { color: #888; font-size: 12px; }

.archetype-body {
  padding: 4px 16px 20px;
  border-top: 1px solid #2a2a2a;
}
.archetype-section-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  color: #666;
  margin: 22px 0 10px;
}
.archetype-grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.archetype-grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
@media (max-width: 640px) {
  .archetype-grid-2, .archetype-grid-3 { grid-template-columns: 1fr; }
}
.archetype-field { margin-bottom: 14px; }
.archetype-field label {
  display: block;
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: #888;
  margin-bottom: 6px;
}
.archetype-field input,
.archetype-field textarea,
.archetype-field select {
  width: 100%;
  font-family: inherit;
  font-size: 13px;
  padding: 9px 12px;
  border: 1px solid #2a2a2a;
  border-radius: 3px;
  background: #141414;
  color: #fff;
  transition: border-color 0.15s;
}
.archetype-field input:focus,
.archetype-field textarea:focus,
.archetype-field select:focus {
  outline: none;
  border-color: #e0e0e0;
}
.archetype-field textarea { resize: vertical; line-height: 1.5; }
.archetype-field select {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 24 24' fill='none' stroke='%23999' stroke-width='2'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 12px center;
  padding-right: 32px;
  cursor: pointer;
}
</style>
