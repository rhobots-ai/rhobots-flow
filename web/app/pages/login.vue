<template>
  <div class="min-h-screen flex items-center justify-center p-6 bg-gradient-to-br from-gray-50 to-primary-50/30 dark:from-gray-900 dark:to-gray-800">
    <div class="w-full max-w-md">
      <AuthLogin />
    </div>
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia"

const userStore = useUserStore()
const { isLoggedIn } = storeToRefs(userStore)

// Page meta
definePageMeta({
  layout: false // Use no layout for login page
})

// Redirect if already logged in
onMounted(() => {
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
