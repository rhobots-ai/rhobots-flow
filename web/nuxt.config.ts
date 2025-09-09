// https://nuxt.com/docs/api/configuration/nuxt-config
import { defineNuxtConfig } from 'nuxt/config';
import { fileURLToPath } from 'node:url';
import tsconfigPaths from 'vite-tsconfig-paths';
import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  css: [fileURLToPath(new URL('./app/assets/css/main.css', import.meta.url))],
  vite: {
    plugins: [tsconfigPaths(), tailwindcss()],
    resolve: {
      alias: {
        '@auto': fileURLToPath(new URL('./app/automation/src', import.meta.url)),
      },
    },
    server: {
      proxy: {
        '/api/test-browser': {
          target: 'http://automation:8000',
          changeOrigin: true
        },
        '/api/health': {
          target: 'http://automation:8000',
          changeOrigin: true
        },
        '/api/automation': {
          target: 'http://automation:8000',
          changeOrigin: true
        },
        '/api/tasks': {
          target: 'http://automation:8000',
          changeOrigin: true
        },
        '/api/sessions': {
          target: 'http://automation:8001',
          changeOrigin: true
        },
        '/api/files': {
          target: 'http://automation:8000',
          changeOrigin: true
        },
        '/api': {
          target: `${process.env.NUXT_PUBLIC_API_SCHEME || 'http'}://${process.env.NUXT_PUBLIC_API_BASE_URL || 'localhost:8004'}`,
          changeOrigin: true
        },
        '/ws': {
          target: `${process.env.NUXT_PUBLIC_API_SCHEME || 'http'}://${process.env.NUXT_PUBLIC_API_BASE_URL || 'localhost:8004'}`,
          ws: true,
          changeOrigin: true
        },
        '/ws/automation': {
          target: 'http://automation:8000',
          ws: true,
          changeOrigin: true,
          rewrite: (path: string) => path.replace(/^\/ws\/automation/, '/ws')
        }
      }
    },
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
