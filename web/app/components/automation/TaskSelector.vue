<template>
  <div class="p-6">
    <div class="max-w-4xl mx-auto">
      <div class="text-center mb-8">
        <h2 class="text-2xl font-semibold text-zinc-900 mb-2">Select a Task to Run</h2>
        <p class="text-zinc-600">Choose an automation task to execute in the runner</p>
      </div>

      <!-- Task List -->
      <div v-if="loading" class="text-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
        <p class="mt-2 text-zinc-600">Loading tasks...</p>
      </div>

      <div v-else-if="tasks.length === 0" class="text-center py-8">
        <div class="text-zinc-400 mb-4">
          <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        </div>
        <h3 class="text-lg font-medium text-zinc-900 mb-2">No tasks found</h3>
        <p class="text-zinc-600 mb-4">Create your first automation task to get started</p>
        <NuxtLink
          to="/test/builder"
          class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Wrench class="w-4 h-4 mr-2" />
          Create Task
        </NuxtLink>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="task in tasks"
          :key="task.id"
          class="bg-white rounded-lg border border-zinc-200 p-4 hover:shadow-md transition-shadow cursor-pointer"
          @click="selectTask(task.id)"
        >
          <div class="flex items-start justify-between mb-3">
            <h3 class="font-medium text-zinc-900 truncate">{{ task.name }}</h3>
            <span
              :class="getStatusColor(task.status)"
              class="px-2 py-1 text-xs rounded-full"
            >
              {{ task.status || 'ready' }}
            </span>
          </div>
          
          <p class="text-sm text-zinc-600 mb-3 line-clamp-2">
            {{ task.description || 'No description available' }}
          </p>
          
          <div class="flex items-center justify-between text-xs text-zinc-500">
            <span>{{ task.steps?.length || 0 }} steps</span>
            <span>{{ formatDate(task.created_at) }}</span>
          </div>
          
          <div class="mt-3 flex gap-2">
            <button
              @click.stop="selectTask(task.id)"
              class="flex-1 px-3 py-1.5 bg-blue-600 text-white text-sm rounded hover:bg-blue-700 transition-colors"
            >
              Run Task
            </button>
            <button
              @click.stop="editTask(task.id)"
              class="px-3 py-1.5 border border-zinc-300 text-zinc-700 text-sm rounded hover:bg-zinc-50 transition-colors"
            >
              Edit
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Wrench } from 'lucide-vue-next'

const emit = defineEmits(['task-selected'])

const tasks = ref([])
const loading = ref(true)

// Load tasks
const loadTasks = async () => {
  try {
    loading.value = true
    const response = await $fetch('/api/tasks/')
    tasks.value = response
  } catch (error) {
    console.error('Failed to load tasks:', error)
    tasks.value = []
  } finally {
    loading.value = false
  }
}

// Task actions
const selectTask = (taskId) => {
  emit('task-selected', taskId)
}

const editTask = (taskId) => {
  navigateTo(`/test/builder?edit=${taskId}`)
}

// Utility functions
const getStatusColor = (status) => {
  const colors = {
    'draft': 'bg-zinc-100 text-zinc-700',
    'ready': 'bg-blue-100 text-blue-700',
    'running': 'bg-amber-100 text-amber-700',
    'completed': 'bg-emerald-100 text-emerald-700',
    'failed': 'bg-rose-100 text-rose-700'
  }
  return colors[status] || 'bg-zinc-100 text-zinc-700'
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  loadTasks()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
