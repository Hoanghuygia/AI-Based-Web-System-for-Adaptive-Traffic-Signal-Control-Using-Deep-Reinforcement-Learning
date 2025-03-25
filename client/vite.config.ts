import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@src': path.resolve(__dirname,'./src'),
      '@assets': path.resolve(__dirname, './src/assets'),
      '@components': path.resolve(__dirname, './src/components'),
      '@uitl': path.resolve(__dirname, './src/uitl'),
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
        target: 'http://your-api-server.com/users', // Khi frontend gọi /api/users, request sẽ được đổi thành http://your-api-server.com/users.
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
});
