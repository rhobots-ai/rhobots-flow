// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  css: ['~/assets/css/main.css'],
  vite: {
    plugins: [
      tailwindcss(),
    ],
    optimizeDeps: {
      exclude: ['@novnc/novnc']
    },
    server: {
      proxy: {
        // Proxy VNC WebSocket connections to the playwright-vnc container
        '/vnc': {
          target: 'ws://playwright-vnc:7900',
          ws: true,
          changeOrigin: true,
          secure: false
        },
        // Proxy WebSocket connections to Django backend
        '/ws': {
          target: 'ws://backend:8000',
          ws: true,
          changeOrigin: true,
          secure: false
        }
      }
    }
  },
  modules: [
    '@nuxt/eslint',
    '@nuxt/image',
    '@nuxt/scripts',
    '@nuxt/test-utils',
    '@nuxt/ui',
    '@pinia/nuxt'
  ],
  app: {
    pageTransition: {name: 'page', mode: 'out-in'}
  },
  runtimeConfig: {
    public: {
      appBaseUrl: process.env.NUXT_PUBLIC_APP_BASE_URL,
      apiScheme: process.env.NUXT_PUBLIC_API_SCHEME,
      apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URL,
      authBaseUrl: process.env.NUXT_PUBLIC_AUTH_BASE_URL,
    },
  }
})