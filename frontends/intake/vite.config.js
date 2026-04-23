import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

// Sharpz Intake Vue SPA.
// Dev: http://localhost:5173/intake/new
// Build: dist/ served by backend at sharpzanalytics.com/intake/:id
export default defineConfig({
  plugins: [vue()],
  base: '/intake/',
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
});
