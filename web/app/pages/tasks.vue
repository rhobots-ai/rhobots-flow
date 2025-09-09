<template>
  <div>
    <!-- Render original TaskList component verbatim -->
    <TaskList />
  </div>
</template>

<script setup>
// Import the copied original component via the @auto alias
import TaskList from '@auto/components/TaskList.vue'

// Page metadata
definePageMeta({
  title: 'Task Management',
  layout: 'legacy'
})
</script>
