<template>
  <div>
    <!-- Render the original Home component -->
    <Home />
  </div>
</template>

<script setup>
// Import the copied original component via the @auto alias
import Home from '@auto/components/Home.vue'

// Page metadata
definePageMeta({
  title: 'Automation Home',
  layout: 'default'
})
</script>
