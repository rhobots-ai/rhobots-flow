<template>
  <div>
    <!-- Render the original MainDashboard component -->
    <MainDashboard />
  </div>
</template>

<script setup>
// Import the copied original component via the @auto alias
import MainDashboard from '@auto/components/MainDashboard.vue'

// Page metadata
definePageMeta({
  title: 'Automation Dashboard',
  layout: 'default'
})
</script>
