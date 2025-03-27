import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'node:path';
import tsconfigPaths from 'vite-tsconfig-paths';
import { createStyleImportPlugin, AntdResolve } from 'vite-plugin-style-import';

export default defineConfig({
  plugins: [
    react(),
    tsconfigPaths(),
    createStyleImportPlugin({
      resolves: [AntdResolve()]
    })
  ],
  resolve: {
    alias: {
      '@src': path.resolve(__dirname, './src'),
      '@assets': path.resolve(__dirname, './src/assets'),
      '@components': path.resolve(__dirname, './src/components'),
      '@util': path.resolve(__dirname, './src/util'),
      '@pages': path.resolve(__dirname, './src/pages'),
      '@locale': path.resolve(__dirname, './src/locale'),
      '@mock': path.resolve(__dirname, './mock')
    }
  },
  server: {
    port: 5173,
    open: true,
    proxy: {
      '/api': {
        target: 'http://your-api-server.com',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
});
