<template>
  <div class="min-h-screen bg-gradient-to-br from-zinc-50 to-primary-50/30 dark:from-zinc-900 dark:to-zinc-800">
    <slot/>
  </div>
</template>

<script setup lang="ts">
const isDark = ref(false)

onMounted(() => {
  // Check for saved theme preference or system preference
  const savedTheme = localStorage.getItem('theme')
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches

  isDark.value = savedTheme === 'dark' || (!savedTheme && prefersDark)
  if (isDark.value) {
    document.documentElement.classList.add('dark')
  }
})
</script>