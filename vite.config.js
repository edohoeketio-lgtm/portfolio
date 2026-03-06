import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  server: {
    port: 3000,
    open: true,
  },
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        clips: resolve(__dirname, 'pages/clips/index.html'),
        ghost: resolve(__dirname, 'pages/ghost/index.html'),
      }
    }
  }
});
