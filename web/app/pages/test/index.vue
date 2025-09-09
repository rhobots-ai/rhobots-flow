<template>
  <div>
    <!-- Render TestTigerVNC component -->
    <TestTigerVNC />
  </div>
</template>

<script setup>
// Import the original TestTigerVNC component via the @auto alias
import TestTigerVNC from '@auto/components/TestTigerVNC.vue'

// Page metadata
definePageMeta({
  title: 'TigerVNC Test',
  layout: 'legacy'
})
</script>
