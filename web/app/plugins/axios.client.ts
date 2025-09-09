import axios from 'axios'

export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()
  const scheme = (config.public.apiScheme || 'http') as string
  const host = (config.public.apiBaseUrl || 'localhost:8000') as string

  // Build baseURL like http://localhost:8000 in production, but use relative in dev to leverage Vite proxy
  const isDev = import.meta.dev
  const baseURL = isDev ? '' : `${scheme}://${host}`

  // Set global axios defaults so copied components using axios work without changes
  axios.defaults.baseURL = baseURL
  axios.defaults.withCredentials = false
  axios.defaults.headers.common['Accept'] = 'application/json'
  // Leave Authorization header management to existing auth/client if needed

  if (import.meta.client) {
    // Optional: simple debug log
    console.debug('[axios] baseURL set to', baseURL || '(relative)')
  }
})
