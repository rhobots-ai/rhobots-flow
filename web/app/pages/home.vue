<template>
  <div class="h-[calc(100vh-4rem)] flex items-center justify-center p-6">
    <div class="w-full max-w-2xl mx-auto">
      <!-- Welcome Message -->
      <div class="text-center mb-8">
        <h1 class="text-3xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
          Welcome to Rhobots Flow
        </h1>
        <p class="mt-6 text-xl md:text-4xl text-gray-600 dark:text-gray-300">
          This is a template for a Rhobots app.
        </p>
        <div class="mt-6 flex flex-wrap items-center justify-center gap-3">
          <div
              class="flex items-center gap-2 px-2 py-2 rounded-full bg-gradient-to-r from-primary-50 to-purple-50 dark:from-primary-900/30 dark:to-purple-900/30 border border-primary-200/50 dark:border-primary-700/50 text-primary-700 dark:text-primary-300 text-sm font-medium hover:shadow-lg hover:shadow-primary-500/20 dark:hover:shadow-primary-500/10 transition-all duration-300">
            <Sparkles class="h-4 w-4"/>
            <span class="text-xs">{{ highlights[0] }}</span>
          </div>
          <div
              class="flex items-center gap-2 px-2 py-2 rounded-full bg-gradient-to-r from-emerald-50 to-teal-50 dark:from-emerald-900/30 dark:to-teal-900/30 border border-emerald-200/50 dark:border-emerald-700/50 text-emerald-700 dark:text-emerald-300 text-sm font-medium hover:shadow-lg hover:shadow-emerald-500/20 dark:hover:shadow-emerald-500/10 transition-all duration-300">
            <BookOpen class="h-4 w-4"/>
            <span class="text-xs">{{ highlights[1] }}</span>
          </div>
          <div
              class="flex items-center gap-2 px-2 py-2 rounded-full bg-gradient-to-r from-purple-50 to-indigo-50 dark:from-purple-900/30 dark:to-indigo-900/30 border border-purple-200/50 dark:border-purple-700/50 text-purple-700 dark:text-purple-300 text-sm font-medium hover:shadow-lg hover:shadow-purple-500/20 dark:hover:shadow-purple-500/10 transition-all duration-300">
            <Brain class="h-4 w-4"/>
            <span class="text-xs">{{ highlights[2] }}</span>
          </div>
        </div>
      </div>

      <!-- Welcome message for logged-in users -->
      <div v-if="userStore.profile" class="text-center">
        <p class="text-lg text-gray-600 dark:text-gray-300">
          Welcome back, {{ userStore.fullName || userStore.profile.email }}!
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { BookOpen, Brain, Sparkles } from 'lucide-vue-next'
import { storeToRefs } from "pinia"

// Store
const userStore = useUserStore()
const { isLoggedIn } = storeToRefs(userStore)
const highlights = ref(['Feature 1', 'Feature 2', 'Feature 3'])

// Page meta
definePageMeta({
  layout: 'default',
  middleware: 'auth' // This will be created next
})

// Redirect if not logged in
onMounted(() => {
  if (!isLoggedIn.value) {
    navigateTo('/login')
  }
})

// Lifecycle
onMounted(() => {
  // Initialize any required data
})
</script>
