<template>
  <div 
    v-if="isOpen"
    class="fixed inset-0 z-50 overflow-y-auto"
    aria-labelledby="modal-title"
    role="dialog"
    aria-modal="true"
  >
    <!-- Background overlay -->
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <div 
        class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
        aria-hidden="true"
        @click="$emit('close')"
      ></div>

      <!-- Modal content -->
      <div class="inline-block align-bottom bg-white dark:bg-gray-900 rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-3xl sm:w-full">
        <!-- Header -->
        <div class="bg-white dark:bg-gray-900 px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <h3 class="text-lg font-medium text-gray-900 dark:text-white" id="modal-title">
                Run Details #{{ run.id.slice(-6) }}
              </h3>
              <AutomationRunStatusBadge :status="run.status" />
            </div>
            <button 
              @click="$emit('close')"
              class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
            >
              <X class="h-5 w-5" />
            </button>
          </div>
        </div>

        <!-- Content -->
        <div class="bg-white dark:bg-gray-900">
          <!-- Run Info -->
          <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <div class="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span class="font-medium text-gray-500 dark:text-gray-400">Started:</span>
                <span class="ml-2 text-gray-900 dark:text-white">{{ formatDate(run.startTime) }}</span>
              </div>
              <div v-if="run.endTime">
                <span class="font-medium text-gray-500 dark:text-gray-400">Ended:</span>
                <span class="ml-2 text-gray-900 dark:text-white">{{ formatDate(run.endTime) }}</span>
              </div>
              <div v-if="run.duration">
                <span class="font-medium text-gray-500 dark:text-gray-400">Duration:</span>
                <span class="ml-2 text-gray-900 dark:text-white">{{ run.duration }}</span>
              </div>
              <div>
                <span class="font-medium text-gray-500 dark:text-gray-400">Screenshots:</span>
                <span class="ml-2 text-gray-900 dark:text-white">{{ run.screenshots?.length || 0 }}</span>
              </div>
            </div>
          </div>

          <!-- Error Details -->
          <div v-if="run.error" class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <h4 class="font-medium text-red-600 dark:text-red-400 mb-2">Error Details</h4>
            <div class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-3">
              <p class="text-sm text-red-700 dark:text-red-300">{{ run.error }}</p>
            </div>
          </div>

          <!-- Logs -->
          <div class="px-6 py-4">
            <h4 class="font-medium text-gray-900 dark:text-white mb-3">Execution Logs</h4>
            <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4 max-h-64 overflow-y-auto">
              <div v-if="run.logs && run.logs.length > 0" class="space-y-1">
                <div 
                  v-for="log in run.logs" 
                  :key="log.id"
                  class="flex items-start gap-3 text-sm font-mono"
                >
                  <span class="text-xs text-gray-500 dark:text-gray-400 flex-shrink-0">
                    {{ formatTime(log.timestamp) }}
                  </span>
                  <span 
                    class="flex-shrink-0 w-12 text-xs font-medium"
                    :class="getLogLevelClass(log.level)"
                  >
                    {{ log.level.toUpperCase() }}
                  </span>
                  <span class="text-gray-700 dark:text-gray-300">{{ log.message }}</span>
                </div>
              </div>
              <div v-else class="text-center py-4 text-gray-500 dark:text-gray-400">
                <FileText class="h-8 w-8 mx-auto mb-2 opacity-50" />
                <p class="text-sm">No logs available</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="bg-gray-50 dark:bg-gray-800 px-6 py-3 flex justify-between">
          <div class="flex items-center gap-2">
            <button 
              v-if="run.screenshots && run.screenshots.length > 0"
              @click="viewScreenshots"
              class="px-3 py-1 text-sm border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded hover:bg-gray-50 dark:hover:bg-gray-700"
            >
              <Camera class="h-4 w-4 mr-1 inline" />
              View Screenshots
            </button>
          </div>
          <button 
            @click="$emit('close')"
            class="px-4 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { X, FileText, Camera } from 'lucide-vue-next'
import type { RunHistory, LogLevel } from '~/types/automation'

interface Props {
  run: RunHistory
  isOpen: boolean
}

interface Emits {
  (e: 'close'): void
  (e: 'view-screenshots'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleString()
}

const formatTime = (dateString: string): string => {
  return new Date(dateString).toLocaleTimeString()
}

const getLogLevelClass = (level: LogLevel): string => {
  switch (level) {
    case 'error':
      return 'text-red-600 dark:text-red-400'
    case 'warn':
      return 'text-amber-600 dark:text-amber-400'
    case 'info':
      return 'text-blue-600 dark:text-blue-400'
    case 'debug':
      return 'text-gray-500 dark:text-gray-400'
    default:
      return 'text-gray-600 dark:text-gray-300'
  }
}

const viewScreenshots = () => {
  emit('view-screenshots')
}
</script>

<style scoped>
/* Custom scrollbar for logs */
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
