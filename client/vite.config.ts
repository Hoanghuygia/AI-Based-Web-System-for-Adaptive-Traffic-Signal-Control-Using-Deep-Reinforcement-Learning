import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname,'./src')
    }
  },
  server: {
    port: 5173,
    open: true,
    proxy: {
      '/apiv1': {
        target: 'http://api.twitter.com',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/apiv1/, '')
      }
    }
  }
});
