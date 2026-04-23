<script setup>
import { computed } from 'vue';

const props = defineProps({
  modelValue: { type: Object, default: () => ({}) },
  keyLabel: { type: String, default: 'Clave' },
  valueLabel: { type: String, default: 'Valor' },
  keyPlaceholder: { type: String, default: '' },
  valuePlaceholder: { type: String, default: '' },
});
const emit = defineEmits(['update:modelValue']);

const rowsWithPhantom = computed(() => {
  const rows = Object.entries(props.modelValue || {}).map(([k, v]) => ({
    key: k, value: v, phantom: false,
  }));
  rows.push({ key: '', value: '', phantom: true });
  return rows;
});

function updateRow(i, field, value) {
  const entries = Object.entries(props.modelValue || {});
  if (i < entries.length) {
    const next = Object.fromEntries(entries);
    if (field === 'key') {
      const oldKey = entries[i][0];
      const oldValue = entries[i][1];
      delete next[oldKey];
      if (value.trim() !== '') next[value] = oldValue;
    } else {
      next[entries[i][0]] = value;
    }
    emit('update:modelValue', next);
  } else {
    // phantom row — promote when user types a non-empty key
    if (field === 'key' && value.trim() !== '') {
      const next = Object.fromEntries(entries);
      next[value] = '';
      emit('update:modelValue', next);
    } else if (field === 'value' && value.trim() !== '') {
      const next = Object.fromEntries(entries);
      next[''] = value;
      emit('update:modelValue', next);
    }
  }
}

function removeRow(i) {
  const entries = Object.entries(props.modelValue || {});
  entries.splice(i, 1);
  emit('update:modelValue', Object.fromEntries(entries));
}
</script>

<template>
  <div class="kv-builder">
    <div class="kv-header">
      <div class="kv-col-key">{{ keyLabel }}</div>
      <div class="kv-col-value">{{ valueLabel }}</div>
      <div class="kv-col-actions" />
    </div>
    <div
      v-for="(row, i) in rowsWithPhantom"
      :key="i"
      class="kv-row"
      :class="{ 'kv-row-phantom': row.phantom }"
    >
      <input
        :value="row.key"
        @input="updateRow(i, 'key', $event.target.value)"
        class="kv-input kv-col-key"
        :placeholder="keyPlaceholder"
      />
      <input
        :value="row.value"
        @input="updateRow(i, 'value', $event.target.value)"
        class="kv-input kv-col-value"
        :placeholder="valuePlaceholder"
      />
      <button
        v-if="!row.phantom"
        @click="removeRow(i)"
        class="kv-remove"
        type="button"
      >×</button>
      <span v-else class="kv-add-hint">(empezá a escribir)</span>
    </div>
  </div>
</template>

<style scoped>
.kv-builder {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.kv-header, .kv-row {
  display: grid;
  grid-template-columns: 1fr 1.6fr 40px;
  gap: 8px;
  align-items: center;
}
.kv-header {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: #666;
  margin-bottom: 2px;
}
.kv-input {
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  padding: 9px 12px;
  border: 1px solid #2a2a2a;
  border-radius: 3px;
  background: #0a0a0a;
  color: #fff;
  transition: border-color 0.15s;
}
.kv-input:focus {
  outline: none;
  border-color: #e0e0e0;
}
.kv-row-phantom .kv-input {
  background: transparent;
  border-style: dashed;
  color: #999;
}
.kv-remove {
  background: transparent;
  border: 1px solid transparent;
  color: #d46060;
  cursor: pointer;
  border-radius: 3px;
  padding: 4px 8px;
}
.kv-remove:hover {
  border-color: #d46060;
  background: rgba(212, 96, 96, 0.08);
}
.kv-add-hint {
  font-size: 10px;
  color: #666;
  font-style: italic;
  grid-column: 3 / 4;
}
</style>
