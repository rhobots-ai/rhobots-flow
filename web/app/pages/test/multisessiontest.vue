<template>
  <div>
    <!-- Render MultiSessionTest component -->
    <MultiSessionTest />
  </div>
</template>

<script setup>
// Import the original MultiSessionTest component via the @auto alias
import MultiSessionTest from '@auto/components/MultiSessionTest.vue'

// Page metadata
definePageMeta({
  title: 'Multi-Session Test',
  layout: 'legacy'
})
</script>
