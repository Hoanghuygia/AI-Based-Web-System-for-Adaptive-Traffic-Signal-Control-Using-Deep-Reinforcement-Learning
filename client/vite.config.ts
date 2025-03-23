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
        target: 'http://your-api-server.com/users', // Khi frontend gọi /apiv1/users, request sẽ được đổi thành http://your-api-server.com/users.
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/apiv1/, '')
      }
    }
  }
});
