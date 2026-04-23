<script setup>
import { computed } from 'vue';

const props = defineProps({
  modelValue: { type: Array, default: () => [] },
  itemPlaceholder: { type: String, default: '' },
  addHint: { type: String, default: '(empezá a escribir para agregar)' },
});
const emit = defineEmits(['update:modelValue']);

const rowsWithPhantom = computed(() => {
  const rows = (props.modelValue || []).map((v) => ({ value: v, phantom: false }));
  rows.push({ value: '', phantom: true });
  return rows;
});

function updateRow(i, value) {
  const next = [...props.modelValue];
  if (i < next.length) {
    next[i] = value;
  } else if (value.trim() !== '') {
    next.push(value); // promoted from phantom
  }
  emit('update:modelValue', next);
}

function removeRow(i) {
  const next = [...props.modelValue];
  next.splice(i, 1);
  emit('update:modelValue', next);
}

function focusNext(evt) {
  const inputs = Array.from(evt.target.closest('.list-builder').querySelectorAll('input'));
  const idx = inputs.indexOf(evt.target);
  if (idx >= 0 && idx + 1 < inputs.length) inputs[idx + 1].focus();
}
</script>

<template>
  <div class="list-builder">
    <div
      v-for="(row, i) in rowsWithPhantom"
      :key="i"
      class="list-row"
      :class="{ 'list-row-phantom': row.phantom }"
    >
      <span class="list-bullet">{{ row.phantom ? '+' : i + 1 }}</span>
      <input
        :value="row.value"
        @input="updateRow(i, $event.target.value)"
        @keyup.enter="focusNext"
        class="list-input"
        :placeholder="row.phantom ? addHint : itemPlaceholder"
      />
      <button v-if="!row.phantom" @click="removeRow(i)" class="list-remove" type="button">
        ×
      </button>
      <span v-else class="list-filler" />
    </div>
  </div>
</template>

<style scoped>
.list-builder {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.list-row { display: flex; gap: 10px; align-items: center; }
.list-bullet {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  color: #666;
  width: 22px;
  text-align: right;
  flex-shrink: 0;
}
.list-input {
  flex: 1;
  font-size: 14px;
  padding: 9px 12px;
  border: 1px solid #2a2a2a;
  border-radius: 3px;
  background: #0a0a0a;
  color: #fff;
  font-family: inherit;
  transition: border-color 0.15s;
}
.list-input:focus {
  outline: none;
  border-color: #e0e0e0;
}
.list-row-phantom .list-input {
  background: transparent;
  border-style: dashed;
  font-style: italic;
  color: #999;
}
.list-remove {
  background: transparent;
  border: 1px solid transparent;
  color: #d46060;
  font-size: 16px;
  cursor: pointer;
  padding: 2px 8px;
  border-radius: 3px;
  width: 28px;
}
.list-remove:hover {
  border-color: #d46060;
  background: rgba(212, 96, 96, 0.08);
}
.list-filler { width: 28px; display: inline-block; }
</style>
