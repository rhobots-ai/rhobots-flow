/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './app/**/*.{vue,js,ts}',
    './app/automation/src/**/*.{vue,js,ts}',
    './error.vue'
  ],
  theme: {
    extend: {}
  },
  plugins: [
    '@tailwindcss/forms'
  ]
}
