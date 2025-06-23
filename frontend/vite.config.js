import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    host: "0.0.0.0",
    port: 3000,
      hmr: {
        host : "backend",
        protocol: "ws",  // Assure-toi qu'il utilise WebSocket
        clientPort: 3000
      },
      proxy: {
        '/api/us': {
          target: 'http://backend_us:8084',
          changeOrigin: true,
          secure: false,
          rewrite: path => path.replace(/^\/api/, '')
        },
        '/api/fr': {
          target: 'http://backend_fr:8084',
          changeOrigin: true,
          secure: false,
          rewrite: path => path.replace(/^\/api/, '')
        },
        '/api/ch_fr': {
          target: 'http://backend_ch_fr:8084',
          changeOrigin: true,
          secure: false,
          rewrite: path => path.replace(/^\/api/, '')
        },
        '/api/ch_en': {
          target: 'http://backend_ch_en:8084',
          changeOrigin: true,
          secure: false,
          rewrite: path => path.replace(/^\/api/, '')
        },
        '/api/ch_de': {
          target: 'http://backend_ch_de:8084',
          changeOrigin: true,
          secure: false,
          rewrite: path => path.replace(/^\/api/, '')
        }
      }
    }
  }
)
