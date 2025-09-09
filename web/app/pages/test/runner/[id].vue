<template>
  <div>
    <!-- Render original AutomationRunner component verbatim, passing route param as prop -->
    <AutomationRunner :task-id="route.params.id" />
  </div>
</template>

<script setup>
// Import the copied original component via the @auto alias
import AutomationRunner from '@auto/components/AutomationRunner.vue'
const route = useRoute()
</script>
