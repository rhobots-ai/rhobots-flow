<template>
  <div>
    <!-- Render original TaskBuilder component verbatim -->
    <TaskBuilder />
  </div>
</template>

<script setup>
// Import the copied original component via the @auto alias
import TaskBuilder from '@auto/components/TaskBuilder.vue'
</script>
