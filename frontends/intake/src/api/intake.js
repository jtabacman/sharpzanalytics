import axios from 'axios';

// In dev Vite proxies /api to http://localhost:8000. In prod same origin.
const client = axios.create({
  baseURL: '',
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
});

export const intakeApi = {
  async create() {
    const res = await client.post('/api/intakes', {});
    return res.data;
  },

  async get(intakeId) {
    const res = await client.get(`/api/intakes/${intakeId}`);
    return res.data;
  },

  async patch(intakeId, partialUpdates) {
    const res = await client.patch(`/api/intakes/${intakeId}`, partialUpdates);
    return res.data;
  },

  async submit(intakeId) {
    try {
      const res = await client.post(`/api/intakes/${intakeId}/submit`);
      return { ok: true, data: res.data };
    } catch (err) {
      if (err.response?.status === 400) {
        return { ok: false, errors: err.response.data?.detail?.errors ?? [] };
      }
      throw err;
    }
  },
};
