<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { intakeApi } from '../api/intake.js';

const router = useRouter();
const error = ref(null);

onMounted(async () => {
  try {
    const intake = await intakeApi.create();
    router.replace({ name: 'intake', params: { intakeId: intake.id } });
  } catch (err) {
    console.error(err);
    error.value = err?.response?.data?.detail ?? err.message ?? 'Error creando intake';
  }
});
</script>

<template>
  <div class="intake-page">
    <div class="intake-loading">
      <div class="intake-brand-tag">Sharpz Analytics · Client Intake</div>
      <h1 v-if="!error">Preparando tu intake…</h1>
      <h1 v-else>No pudimos crear el intake</h1>
      <p v-if="error" class="intake-loading-error">{{ error }}</p>
      <p v-else class="intake-loading-hint">Se guarda automáticamente mientras completas.</p>
    </div>
  </div>
</template>

<style scoped>
.intake-page {
  min-height: 100vh;
  background: #0a0a0a;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  font-family: 'Space Grotesk', sans-serif;
}
.intake-loading { max-width: 520px; text-align: center; }
.intake-brand-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  letter-spacing: 0.28em;
  text-transform: uppercase;
  color: #888;
  margin-bottom: 24px;
}
h1 {
  font-size: 32px;
  font-weight: 600;
  letter-spacing: -0.02em;
  margin: 0 0 16px;
  background: linear-gradient(180deg, #fff 0%, #888 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.intake-loading-hint { color: #888; font-weight: 300; }
.intake-loading-error {
  color: #d46060;
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  margin-top: 16px;
}
</style>
