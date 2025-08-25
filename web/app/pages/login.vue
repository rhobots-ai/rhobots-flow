<template>
  <div class="min-h-screen flex items-center justify-center p-6 bg-gradient-to-br from-gray-50 to-primary-50/30 dark:from-gray-900 dark:to-gray-800">
    <!-- Theme Toggle -->
    <div class="absolute top-4 right-4">
      <button
          @click="toggleTheme"
          class="p-2 rounded-lg bg-white/20 dark:bg-gray-800/20 backdrop-blur-sm border border-gray-200/50 dark:border-gray-700/50 text-gray-600 dark:text-gray-300 hover:bg-white/30 dark:hover:bg-gray-800/30 transition-colors"
          :title="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
      >
        <Sun v-if="isDark" class="h-5 w-5"/>
        <Moon v-else class="h-5 w-5"/>
      </button>
    </div>

    <div class="w-full max-w-md">
      <AuthLogin />
    </div>
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia"
import { Sun, Moon } from 'lucide-vue-next'

const userStore = useUserStore()
const { isLoggedIn } = storeToRefs(userStore)

const isDark = ref(false)

// Page meta
definePageMeta({
  layout: false // Use no layout for login page
})

// Theme toggle function
const toggleTheme = () => {
  isDark.value = !isDark.value
  if (isDark.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}

// Initialize theme since we're not using a layout
onMounted(() => {
  // Check for saved theme preference or system preference
  const savedTheme = localStorage.getItem('theme')
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches

  isDark.value = savedTheme === 'dark' || (!savedTheme && prefersDark)
  if (isDark.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }

  // Initialize color palette
  const { setColorPalette } = useTheme()
  const savedPalette = localStorage.getItem('colorPalette')
  if (savedPalette) {
    setColorPalette(savedPalette)
  }

  // Redirect if already logged in
  if (isLoggedIn.value) {
    navigateTo('/home')
  }
  
  // Watch for login state changes
  watch(() => isLoggedIn.value, (newIsLoggedIn) => {
    if (newIsLoggedIn) {
      navigateTo('/home')
    }
  })
})
</script>
