<script setup>
defineProps({
  intake: { type: Object, required: true },
});
</script>

<template>
  <div class="intake-submitted-card">
    <h2>✓ Intake enviado</h2>
    <p>
      Tu intake quedó en cola de revisión. Nos contactamos a
      <strong>{{ intake.contact_email }}</strong>
      con cronograma y confirmación.
    </p>
    <p><strong>ID de referencia:</strong> <code>{{ intake.id }}</code></p>
    <p class="note">
      Podés volver a este link para ver el estado cuando quieras.
    </p>
  </div>
</template>

<style scoped>
.intake-submitted-card {
  background: #141414;
  border: 1px solid #1f1f1f;
  border-radius: 8px;
  padding: 72px 48px;
  text-align: center;
}
h2 {
  font-size: 36px;
  margin: 0 0 20px;
  color: #fff;
  font-weight: 600;
}
p {
  font-size: 15px;
  color: #999;
  line-height: 1.7;
  max-width: 480px;
  margin: 0 auto 12px;
  font-weight: 300;
}
code {
  background: #0a0a0a;
  padding: 3px 10px;
  border-radius: 3px;
  border: 1px solid #2a2a2a;
  color: #e0e0e0;
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
}
.note {
  margin-top: 32px;
  font-size: 12px;
  color: #666;
  font-style: italic;
}
</style>
