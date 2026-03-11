import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  base: '/wc/',
  server: {
    proxy: {
      '/wc/api': {
        target: 'http://localhost:5035',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/wc\/api/, '/api')
      }
    }
  }
})