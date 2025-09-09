<template>
  <div>
    <!-- Render the original TaskBuilder component -->
    <ClientOnly>
      <TaskBuilder />
      <template #fallback>
        <div class="flex items-center justify-center h-64">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      </template>
    </ClientOnly>
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
