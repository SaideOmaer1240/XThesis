import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist', // Gera a pasta de build correta
  },
  server: {
    historyApiFallback: true, // Garante que rotas sejam tratadas corretamente
  }
});

