<template>
  <div 
    class="p-4 rounded-lg border cursor-pointer transition-all duration-200 group"
    :class="[
      isActive 
        ? 'bg-primary-50 border-primary-200 dark:bg-primary-900/20 dark:border-primary-700 shadow-md' 
        : 'bg-white border-gray-200 hover:border-gray-300 hover:shadow-sm dark:bg-gray-800 dark:border-gray-700 dark:hover:border-gray-600'
    ]"
    @click="$emit('select', task)"
  >
    <div class="flex items-start justify-between">
      <div class="flex-1 min-w-0">
        <div class="flex items-center gap-2 mb-2">
          <h3 class="font-medium text-gray-900 dark:text-white truncate">{{ task.name }}</h3>
          <AutomationTaskStatusBadge :status="task.status" size="sm" />
        </div>
        
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-3 line-clamp-2">
          {{ task.description }}
        </p>
        
        <div class="flex items-center justify-between text-xs">
          <div class="flex items-center gap-3 text-gray-500 dark:text-gray-400">
            <span class="flex items-center gap-1">
              <Clock class="h-3 w-3" />
              {{ formatDate(task.updatedAt) }}
            </span>
            <span v-if="task.lastRun" class="flex items-center gap-1">
              <Play class="h-3 w-3" />
              {{ formatDate(task.lastRun) }}
            </span>
          </div>
        </div>
      </div>
      
      <!-- Action Menu -->
      <div class="ml-3 flex-shrink-0 relative">
        <button 
          @click.stop="showMenu = !showMenu"
          class="p-1 rounded-lg opacity-0 group-hover:opacity-100 hover:bg-gray-100 dark:hover:bg-gray-700 transition-all duration-200"
          :class="{ 'opacity-100': showMenu }"
        >
          <MoreVertical class="h-4 w-4 text-gray-500 dark:text-gray-400" />
        </button>
        
        <!-- Dropdown Menu -->
        <div 
          v-if="showMenu"
          v-click-outside="() => showMenu = false"
          class="absolute right-0 top-8 w-48 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg z-50"
        >
          <div class="py-1">
            <button 
              @click.stop="handleEdit"
              class="w-full flex items-center gap-2 px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700"
            >
              <Edit3 class="h-4 w-4" />
              Edit Task
            </button>
            
            <button 
              @click.stop="handleDuplicate"
              class="w-full flex items-center gap-2 px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700"
            >
              <Copy class="h-4 w-4" />
              Duplicate
            </button>
            
            <button 
              v-if="task.status === 'running'"
              @click.stop="handleStop"
              class="w-full flex items-center gap-2 px-3 py-2 text-sm text-orange-600 dark:text-orange-400 hover:bg-orange-50 dark:hover:bg-orange-900/20"
            >
              <Square class="h-4 w-4" />
              Stop Task
            </button>
            
            <button 
              v-else-if="task.status === 'ready'"
              @click.stop="handleRun"
              class="w-full flex items-center gap-2 px-3 py-2 text-sm text-green-600 dark:text-green-400 hover:bg-green-50 dark:hover:bg-green-900/20"
            >
              <Play class="h-4 w-4" />
              Run Task
            </button>
            
            <div class="border-t border-gray-200 dark:border-gray-700 my-1"></div>
            
            <button 
              @click.stop="handleDelete"
              class="w-full flex items-center gap-2 px-3 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20"
            >
              <Trash2 class="h-4 w-4" />
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Progress indicator for running tasks -->
    <div 
      v-if="task.status === 'running'" 
      class="mt-3 w-full bg-gray-200 dark:bg-gray-700 rounded-full h-1"
    >
      <div class="bg-primary-600 h-1 rounded-full animate-pulse" style="width: 45%"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { 
  Clock, Play, MoreVertical, Edit3, Copy, Square, Trash2
} from 'lucide-vue-next'
import type { AutomationTask } from '~/types/automation'

interface Props {
  task: AutomationTask
  isActive: boolean
}

interface Emits {
  (e: 'select', task: AutomationTask): void
  (e: 'edit', task: AutomationTask): void
  (e: 'duplicate', task: AutomationTask): void
  (e: 'delete', task: AutomationTask): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const showMenu = ref(false)

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))
  
  if (diffDays === 0) {
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit' 
    })
  } else if (diffDays === 1) {
    return 'Yesterday'
  } else if (diffDays < 7) {
    return `${diffDays} days ago`
  } else {
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric' 
    })
  }
}

const handleEdit = () => {
  showMenu.value = false
  emit('edit', props.task)
}

const handleDuplicate = () => {
  showMenu.value = false
  emit('duplicate', props.task)
}

const handleDelete = () => {
  showMenu.value = false
  emit('delete', props.task)
}

const handleRun = () => {
  showMenu.value = false
  emit('select', props.task)
  // The parent component will handle running the task
}

const handleStop = () => {
  showMenu.value = false
  // The parent component will handle stopping the task
}

// Click outside directive
const vClickOutside = {
  mounted(el: HTMLElement, binding: any) {
    const clickHandler = (event: Event) => {
      if (!el.contains(event.target as Node)) {
        binding.value()
      }
    }
    el._clickOutsideHandler = clickHandler
    document.addEventListener('click', clickHandler)
  },
  unmounted(el: HTMLElement & { _clickOutsideHandler?: EventListener }) {
    if (el._clickOutsideHandler) {
      document.removeEventListener('click', el._clickOutsideHandler)
      delete el._clickOutsideHandler
    }
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Animation for progress bar */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>
