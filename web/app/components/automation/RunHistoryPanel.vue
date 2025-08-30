<template>
  <div class="flex flex-col h-full">
    <!-- Header -->
    <div class="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
      <div class="flex items-center gap-3">
        <h3 class="font-medium text-gray-900 dark:text-white">Run History</h3>
        <span 
          v-if="runHistory.length > 0" 
          class="px-2 py-0.5 text-xs bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 rounded-full"
        >
          {{ runHistory.length }}
        </span>
      </div>
      
      <div class="flex items-center gap-2">
        <button 
          @click="refreshHistory"
          :disabled="isLoading"
          class="p-1.5 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 disabled:opacity-50"
          title="Refresh"
        >
          <RefreshCw class="h-4 w-4" :class="{ 'animate-spin': isLoading }" />
        </button>
        
        <button 
          @click="isCollapsed = !isCollapsed"
          class="p-1.5 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800"
          :title="isCollapsed ? 'Expand' : 'Collapse'"
        >
          <ChevronUp v-if="!isCollapsed" class="h-4 w-4" />
          <ChevronDown v-else class="h-4 w-4" />
        </button>
      </div>
    </div>

    <!-- History List -->
    <div 
      v-if="!isCollapsed" 
      class="flex-1 overflow-y-auto"
      :class="{ 'h-0': isCollapsed }"
    >
      <!-- Loading State -->
      <div v-if="isLoading && runHistory.length === 0" class="flex items-center justify-center py-8">
        <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-600"></div>
      </div>
      
      <!-- Empty State -->
      <div v-else-if="runHistory.length === 0" class="flex flex-col items-center justify-center py-8 text-gray-500 dark:text-gray-400">
        <History class="h-12 w-12 mb-3 opacity-50" />
        <p class="text-sm">No execution history</p>
        <p class="text-xs">Run history will appear here</p>
      </div>
      
      <!-- History Items -->
      <div v-else class="divide-y divide-gray-100 dark:divide-gray-700">
        <div 
          v-for="run in runHistory" 
          :key="run.id"
          class="p-3 hover:bg-gray-50 dark:hover:bg-gray-800 cursor-pointer transition-colors"
          @click="selectRun(run)"
        >
          <div class="flex items-start justify-between">
            <!-- Run Info -->
            <div class="flex items-start gap-3 flex-1 min-w-0">
              <AutomationRunStatusIcon :status="run.status" size="sm" />
              
              <div class="min-w-0 flex-1">
                <div class="flex items-center gap-2 mb-1">
                  <p class="text-sm font-medium text-gray-900 dark:text-white">
                    Run #{{ run.id.slice(-6) }}
                  </p>
                  <AutomationRunStatusBadge :status="run.status" size="sm" />
                </div>
                
                <div class="flex items-center gap-3 text-xs text-gray-500 dark:text-gray-400 mb-2">
                  <span class="flex items-center gap-1">
                    <Clock class="h-3 w-3" />
                    {{ formatDate(run.startTime) }}
                  </span>
                  <span v-if="run.duration" class="flex items-center gap-1">
                    <Timer class="h-3 w-3" />
                    {{ run.duration }}
                  </span>
                </div>
                
                <!-- Error Message -->
                <p v-if="run.error" class="text-xs text-red-600 dark:text-red-400 truncate">
                  {{ run.error }}
                </p>
                
                <!-- Progress for running tasks -->
                <div v-if="run.status === 'running'" class="mt-2">
                  <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-1">
                    <div 
                      class="bg-primary-600 h-1 rounded-full transition-all duration-300 animate-pulse"
                      :style="{ width: getRunProgress(run) + '%' }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Actions -->
            <div class="flex items-center gap-1 ml-2">
              <button 
                v-if="run.screenshots && run.screenshots.length > 0"
                @click.stop="viewScreenshots(run)"
                class="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded"
                title="View Screenshots"
              >
                <Camera class="h-3 w-3" />
              </button>
              
              <button 
                @click.stop="viewLogs(run)"
                class="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded"
                title="View Logs"
              >
                <FileText class="h-3 w-3" />
              </button>
              
              <button 
                v-if="run.status === 'running'"
                @click.stop="stopRun(run)"
                class="p-1 text-red-500 hover:text-red-600 rounded"
                title="Stop Run"
              >
                <Square class="h-3 w-3" />
              </button>
              
              <button 
                v-else-if="run.status === 'failed'"
                @click.stop="retryRun(run)"
                class="p-1 text-orange-500 hover:text-orange-600 rounded"
                title="Retry"
              >
                <RotateCcw class="h-3 w-3" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Quick Stats (when collapsed) -->
    <div v-if="isCollapsed && runHistory.length > 0" class="px-4 py-2 border-t border-gray-200 dark:border-gray-700">
      <div class="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
        <span>{{ runHistory.length }} runs</span>
        <div class="flex items-center gap-3">
          <span class="flex items-center gap-1">
            <div class="w-2 h-2 bg-green-500 rounded-full"></div>
            {{ successCount }}
          </span>
          <span class="flex items-center gap-1">
            <div class="w-2 h-2 bg-red-500 rounded-full"></div>
            {{ failureCount }}
          </span>
        </div>
      </div>
    </div>
    
    <!-- Run Details Modal -->
    <AutomationRunDetailsModal
      v-if="selectedRun"
      :run="selectedRun"
      :is-open="!!selectedRun"
      @close="selectedRun = null"
    />
    
    <!-- Screenshots Modal -->
    <AutomationScreenshotsModal
      v-if="screenshotsRun"
      :run="screenshotsRun"
      :is-open="!!screenshotsRun"
      @close="screenshotsRun = null"
    />
  </div>
</template>

<script setup lang="ts">
import { 
  RefreshCw, ChevronUp, ChevronDown, History, Clock, Timer,
  Camera, FileText, Square, RotateCcw
} from 'lucide-vue-next'
import type { AutomationTask, RunHistory, RunStatus } from '~/types/automation'
import { useAutomationStore } from '~/stores/automation'

interface Props {
  task: AutomationTask
}

interface Emits {
  (e: 'stop-run', runId: string): void
  (e: 'retry-run', runId: string): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

// Store
const automationStore = useAutomationStore()

// State
const isCollapsed = ref(false)
const isLoading = ref(false)
const selectedRun = ref<RunHistory | null>(null)
const screenshotsRun = ref<RunHistory | null>(null)

// Computed
const runHistory = computed(() => automationStore.runHistoryForTask(props.task.id))

const successCount = computed(() => 
  runHistory.value.filter(run => run.status === 'completed').length
)

const failureCount = computed(() => 
  runHistory.value.filter(run => run.status === 'failed').length
)

// Methods
const refreshHistory = async () => {
  isLoading.value = true
  try {
    await automationStore.fetchRunHistory(props.task.id)
  } catch (error) {
    console.error('Failed to refresh history:', error)
  } finally {
    isLoading.value = false
  }
}

const selectRun = (run: RunHistory) => {
  selectedRun.value = run
}

const viewScreenshots = (run: RunHistory) => {
  screenshotsRun.value = run
}

const viewLogs = (run: RunHistory) => {
  selectedRun.value = run
  // Could have a separate logs modal or show logs in run details
}

const stopRun = (run: RunHistory) => {
  emit('stop-run', run.id)
}

const retryRun = (run: RunHistory) => {
  emit('retry-run', run.id)
}

const getRunProgress = (run: RunHistory): number => {
  // Calculate progress based on steps completed
  // This would be provided by the backend in a real implementation
  if (run.status === 'running') {
    return Math.floor(Math.random() * 70) + 10 // Simulate progress
  }
  return 0
}

const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffMinutes = Math.floor(diffMs / (1000 * 60))
  const diffHours = Math.floor(diffMinutes / 60)
  const diffDays = Math.floor(diffHours / 24)
  
  if (diffMinutes < 1) {
    return 'Just now'
  } else if (diffMinutes < 60) {
    return `${diffMinutes}m ago`
  } else if (diffHours < 24) {
    return `${diffHours}h ago`
  } else if (diffDays === 1) {
    return 'Yesterday'
  } else if (diffDays < 7) {
    return `${diffDays}d ago`
  } else {
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined
    })
  }
}

// Auto-refresh for running tasks
const autoRefreshInterval = ref<NodeJS.Timeout | null>(null)

const startAutoRefresh = () => {
  if (autoRefreshInterval.value) return
  
  autoRefreshInterval.value = setInterval(() => {
    const hasRunningTasks = runHistory.value.some(run => run.status === 'running')
    if (hasRunningTasks) {
      refreshHistory()
    }
  }, 5000) // Refresh every 5 seconds
}

const stopAutoRefresh = () => {
  if (autoRefreshInterval.value) {
    clearInterval(autoRefreshInterval.value)
    autoRefreshInterval.value = null
  }
}

// Watchers
watch(runHistory, (newHistory) => {
  const hasRunningTasks = newHistory.some(run => run.status === 'running')
  if (hasRunningTasks) {
    startAutoRefresh()
  } else {
    stopAutoRefresh()
  }
}, { immediate: true })

// Lifecycle
onMounted(() => {
  refreshHistory()
})

onUnmounted(() => {
  stopAutoRefresh()
})
</script>

<style scoped>
/* Custom scrollbar for history list */
.overflow-y-auto::-webkit-scrollbar {
  width: 4px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 2px;
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

/* Smooth height transition for collapse */
.transition-height {
  transition: height 0.3s ease-in-out;
}

/* Animation for progress bars */
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
