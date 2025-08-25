<template>
  <div class="bg-gradient-to-br from-gray-50 to-primary-50/30 dark:from-gray-900 dark:to-gray-800">
    <div class="flex items-center justify-center p-6">
      <div class="w-full max-w-md">
        <div class="bg-white/50 dark:bg-gray-900/50 backdrop-blur-sm rounded-xl shadow-lg border border-gray-200/50 dark:border-gray-700/50 p-6">
          <div class="text-center mb-8">
            <h1 class="text-2xl font-semibold text-gray-900 dark:text-white">Welcome to App Template</h1>
            <p class="mt-2 text-sm text-gray-600 dark:text-gray-300">
              This is a template for a Rhobots app.
            </p>
          </div>

          <!-- Auth Forms -->
          <AuthForms @success="handleAuthSuccess" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {storeToRefs} from "pinia";

const userStore = useUserStore()
const {isLoggedIn} = storeToRefs(userStore)

const handleAuthSuccess = () => {
  navigateTo('/home')
}

onMounted(() => {
  watch(() => isLoggedIn.value, (currentIsSignedIn) => {
    if (currentIsSignedIn) {
      navigateTo('/home')
    }
  }, {immediate: true})
})
</script>