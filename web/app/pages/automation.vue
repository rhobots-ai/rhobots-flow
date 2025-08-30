<template>
  <div class="flex h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Left Sidebar Panel -->
    <div class="w-80 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col">
      <!-- Header with New Task Button -->
      <div class="p-4 border-b border-gray-200 dark:border-gray-700">
        <div class="flex items-center justify-between mb-4">
          <h1 class="text-xl font-semibold text-gray-900 dark:text-white">Automation Tasks</h1>
          <button 
            @click="showCreateModal = true"
            class="p-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
            title="Create New Task"
          >
            <Plus class="h-4 w-4" />
          </button>
        </div>
        
        <!-- Search/Filter -->
        <div class="space-y-3">
          <div class="relative">
            <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input 
              v-model="searchQuery"
              type="text" 
              placeholder="Search tasks..."
              class="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>
          
          <!-- Status Filter -->
          <select 
            v-model="filterStatus"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="all">All Tasks</option>
            <option value="draft">Draft</option>
            <option value="ready">Ready</option>
            <option value="running">Running</option>
            <option value="completed">Completed</option>
            <option value="failed">Failed</option>
            <option value="paused">Paused</option>
          </select>
        </div>
      </div>

      <!-- Task List -->
      <div class="flex-1 overflow-y-auto p-4 space-y-3">
        <div v-if="isLoading" class="flex items-center justify-center py-8">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        </div>
        
        <div v-else-if="filteredTasks.length === 0" class="text-center py-8 text-gray-500 dark:text-gray-400">
          <FileX class="h-12 w-12 mx-auto mb-3 opacity-50" />
          <p>No tasks found</p>
          <button 
            @click="showCreateModal = true"
            class="mt-2 text-primary-600 dark:text-primary-400 hover:underline text-sm"
          >
            Create your first task
          </button>
        </div>
        
        <AutomationTaskCard 
          v-for="task in filteredTasks" 
          :key="task.id"
          :task="task"
          :is-active="selectedTask?.id === task.id"
          @select="selectTask"
          @edit="editTask"
          @duplicate="duplicateTask"
          @delete="deleteTask"
        />
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col">
      <!-- Top Bar -->
      <div class="h-16 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 flex items-center justify-between">
        <div v-if="selectedTask" class="flex items-center gap-4">
          <div>
            <h2 class="text-lg font-semibold text-gray-900 dark:text-white">{{ selectedTask.name }}</h2>
            <p class="text-sm text-gray-500">
              Last run: {{ selectedTask.lastRun ? formatDate(selectedTask.lastRun) : 'Never' }}
            </p>
          </div>
        </div>
        
        <div v-else class="flex items-center text-gray-500 dark:text-gray-400">
          <FileQuestion class="h-5 w-5 mr-2" />
          <span>Select a task to get started</span>
        </div>
        
        <div v-if="selectedTask" class="flex items-center gap-3">
          <AutomationTaskStatusBadge :status="selectedTask.status" />
          <button 
            v-if="!isRunning"
            @click="runTask"
            :disabled="selectedTask.status === 'draft'"
            class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <Play class="h-4 w-4 mr-2 inline" />
            Run Automation
          </button>
          <button 
            v-else
            @click="stopTask"
            class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
          >
            <Square class="h-4 w-4 mr-2 inline" />
            Stop
          </button>
        </div>
      </div>

      <!-- Main Workflow Area -->
      <div v-if="selectedTask" class="flex-1 flex">
        <!-- Workflow Configuration -->
        <div class="w-96 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 overflow-y-auto">
          <AutomationWorkflowConfig :task="selectedTask" @update="updateTask" />
        </div>

        <!-- Browser Viewport + History -->
        <div class="flex-1 flex flex-col">
          <!-- Browser Viewport -->
          <div class="flex-1 bg-gray-100 dark:bg-gray-900 p-4">
            <AutomationBrowserViewport 
              :task="selectedTask" 
              :is-running="isRunning"
              :session-id="currentSessionId"
            />
          </div>
          
          <!-- Run History Panel -->
          <div class="h-48 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
            <AutomationRunHistoryPanel :task="selectedTask" />
          </div>
        </div>
      </div>
      
      <!-- Empty State -->
      <div v-else class="flex-1 flex items-center justify-center bg-gray-50 dark:bg-gray-900">
        <div class="text-center">
          <Bot class="h-24 w-24 text-gray-300 dark:text-gray-600 mx-auto mb-6" />
          <h3 class="text-xl font-medium text-gray-900 dark:text-gray-100 mb-2">
            Welcome to Automation Studio
          </h3>
          <p class="text-gray-500 dark:text-gray-400 mb-6 max-w-md">
            Create and manage your automation workflows. Select a task from the sidebar or create a new one to get started.
          </p>
          <button 
            @click="showCreateModal = true"
            class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            <Plus class="h-4 w-4 mr-2 inline" />
            Create Your First Task
          </button>
        </div>
      </div>
    </div>

    <!-- Create/Edit Task Modal -->
    <AutomationTaskModal
      v-if="showCreateModal || showEditModal"
      :task="editingTask"
      :is-open="showCreateModal || showEditModal"
      @close="closeModals"
      @save="handleTaskSave"
    />
  </div>
</template>

<script setup lang="ts">
import { 
  Plus, Search, FileX, FileQuestion, Play, Square, Bot
} from 'lucide-vue-next'
import { useAutomationStore } from '~/stores/automation'
import type { AutomationTask, TaskStatus } from '~/types/automation'

// Meta
definePageMeta({
  layout: 'minimum'
})

useHead({
  title: 'Automation Studio - Rhobots Flow'
})

// Store
const automationStore = useAutomationStore()
const { 
  filteredTasks, 
  selectedTask, 
  isRunning, 
  isLoading, 
  currentSessionId 
} = storeToRefs(automationStore)

// Local state
const showCreateModal = ref(false)
const showEditModal = ref(false)
const editingTask = ref<AutomationTask | null>(null)

// Computed
const searchQuery = computed({
  get: () => automationStore.searchQuery,
  set: (value: string) => automationStore.setSearchQuery(value)
})

const filterStatus = computed({
  get: () => automationStore.filterStatus,
  set: (value: TaskStatus | 'all') => automationStore.setFilterStatus(value)
})

// Methods
const selectTask = (task: AutomationTask) => {
  automationStore.selectTask(task)
}

const editTask = (task: AutomationTask) => {
  editingTask.value = task
  showEditModal.value = true
}

const duplicateTask = async (task: AutomationTask) => {
  try {
    await automationStore.duplicateTask(task.id)
    // Show success notification
  } catch (error) {
    console.error('Failed to duplicate task:', error)
    // Show error notification
  }
}

const deleteTask = async (task: AutomationTask) => {
  if (confirm(`Are you sure you want to delete "${task.name}"?`)) {
    try {
      await automationStore.deleteTask(task.id)
      // Show success notification
    } catch (error) {
      console.error('Failed to delete task:', error)
      // Show error notification
    }
  }
}

const runTask = async () => {
  if (!selectedTask.value) return
  
  try {
    await automationStore.runTask(selectedTask.value.id)
    // Show success notification
  } catch (error) {
    console.error('Failed to run task:', error)
    // Show error notification
  }
}

const stopTask = async () => {
  if (!selectedTask.value) return
  
  try {
    await automationStore.stopTask(selectedTask.value.id)
    // Show success notification
  } catch (error) {
    console.error('Failed to stop task:', error)
    // Show error notification
  }
}

const updateTask = async (updates: Partial<AutomationTask>) => {
  if (!selectedTask.value) return
  
  try {
    await automationStore.updateTask(selectedTask.value.id, updates)
  } catch (error) {
    console.error('Failed to update task:', error)
  }
}

const closeModals = () => {
  showCreateModal.value = false
  showEditModal.value = false
  editingTask.value = null
}

const handleTaskSave = async (taskData: any) => {
  try {
    if (editingTask.value) {
      await automationStore.updateTask(editingTask.value.id, taskData)
    } else {
      const newTask = await automationStore.createTask(taskData)
      automationStore.selectTask(newTask)
    }
    closeModals()
    // Show success notification
  } catch (error) {
    console.error('Failed to save task:', error)
    // Show error notification
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString()
}

// Lifecycle
onMounted(() => {
  automationStore.fetchTasks()
})
</script>

<style scoped>
/* Custom scrollbar for task list */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background-color: rgba(0, 0, 0, 0.3);
}

/* Dark mode scrollbar */
.dark .overflow-y-auto::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.2);
}

.dark .overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background-color: rgba(255, 255, 255, 0.3);
}
</style>
