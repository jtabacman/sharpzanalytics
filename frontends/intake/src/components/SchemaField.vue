<script setup>
import ListBuilder from './ListBuilder.vue';
import KeyValueBuilder from './KeyValueBuilder.vue';

const props = defineProps({
  field: { type: Object, required: true }, // { id, label, type, placeholder, hint, required, options }
  modelValue: null,
});
const emit = defineEmits(['update:modelValue']);

function onInput(evt) {
  emit('update:modelValue', evt.target.value);
}

function onNumberInput(evt) {
  const v = evt.target.value === '' ? null : Number(evt.target.value);
  emit('update:modelValue', v);
}
</script>

<template>
  <div class="schema-field">
    <label class="schema-label">
      {{ field.label }}
      <span v-if="field.required" class="schema-required">*</span>
    </label>

    <input
      v-if="field.type === 'string'"
      type="text"
      class="schema-input"
      :value="modelValue || ''"
      :placeholder="field.placeholder || ''"
      @input="onInput"
    />
    <textarea
      v-else-if="field.type === 'text'"
      class="schema-textarea"
      rows="3"
      :value="modelValue || ''"
      :placeholder="field.placeholder || ''"
      @input="onInput"
    />
    <select
      v-else-if="field.type === 'select'"
      class="schema-select"
      :value="modelValue || ''"
      @change="onInput"
    >
      <option value="" disabled>Seleccioná…</option>
      <option v-for="opt in field.options" :key="opt.value" :value="opt.value">
        {{ opt.label }}
      </option>
    </select>
    <input
      v-else-if="field.type === 'number'"
      type="number"
      class="schema-input"
      :value="modelValue ?? ''"
      :placeholder="field.placeholder || ''"
      @input="onNumberInput"
    />
    <ListBuilder
      v-else-if="field.type === 'multiline_list' || field.type === 'urls_list'"
      :model-value="modelValue || []"
      :item-placeholder="field.placeholder || ''"
      @update:model-value="(v) => emit('update:modelValue', v)"
    />
    <KeyValueBuilder
      v-else-if="field.type === 'key_value_dict'"
      :model-value="modelValue || {}"
      @update:model-value="(v) => emit('update:modelValue', v)"
    />
    <input
      v-else
      type="text"
      class="schema-input"
      :value="modelValue || ''"
      :placeholder="field.placeholder || ''"
      @input="onInput"
    />

    <div v-if="field.hint" class="schema-hint">{{ field.hint }}</div>
  </div>
</template>

<style scoped>
.schema-field { margin-bottom: 22px; }
.schema-label {
  display: block;
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: #999;
  margin-bottom: 8px;
}
.schema-required { color: #e0e0e0; margin-left: 4px; font-weight: 700; }
.schema-input, .schema-textarea, .schema-select {
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
.schema-input:focus, .schema-textarea:focus, .schema-select:focus {
  outline: none;
  border-color: #e0e0e0;
  background: #141414;
}
.schema-textarea { resize: vertical; min-height: 72px; line-height: 1.5; }
.schema-select {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%23999' stroke-width='2'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 14px center;
  padding-right: 40px;
  cursor: pointer;
}
.schema-hint {
  font-size: 12px;
  color: #666;
  margin: 6px 0 0;
  line-height: 1.5;
  font-weight: 300;
}
</style>
