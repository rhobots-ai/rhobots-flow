// https://nuxt.com/docs/api/configuration/nuxt-config
import { defineNuxtConfig } from 'nuxt/config';
import { fileURLToPath } from 'node:url';
import tsconfigPaths from 'vite-tsconfig-paths';

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  css: [fileURLToPath(new URL('./app/assets/css/main.css', import.meta.url))],
  postcss: {
    plugins: {
      '@tailwindcss/postcss': {},
      autoprefixer: {}
    }
  },
  vite: {
    plugins: [tsconfigPaths()],
    resolve: {
      alias: {
        '@auto': fileURLToPath(new URL('./app/automation/src', import.meta.url)),
      },
    },
    server: {
      proxy: {
        '/api': {
          target: `${process.env.NUXT_PUBLIC_API_SCHEME || 'http'}://${process.env.NUXT_PUBLIC_API_BASE_URL || 'localhost:8000'}`,
          changeOrigin: true
        },
        '/ws': {
          target: `${process.env.NUXT_PUBLIC_API_SCHEME || 'http'}://${process.env.NUXT_PUBLIC_API_BASE_URL || 'localhost:8000'}`,
          ws: true,
          changeOrigin: true
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
