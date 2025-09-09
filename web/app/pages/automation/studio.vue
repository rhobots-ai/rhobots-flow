<template>
  <div>
    <!-- Render the original TaskBuilder component -->
    <TaskBuilder />
  </div>
</template>

<script setup>
// Import the copied original component via the @auto alias
import TaskBuilder from '@auto/components/TaskBuilder.vue'

// Page metadata
definePageMeta({
  title: 'Automation Studio',
  layout: 'default'
})
</script>
