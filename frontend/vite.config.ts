import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Adjust the proxy so that `/api`... hits the backend on port 8000
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://localhost:8000'
    }
  }
});
