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
      <div class="inline-block align-bottom bg-white dark:bg-gray-900 rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full">
        <!-- Header -->
        <div class="bg-white dark:bg-gray-900 px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white" id="modal-title">
              Automation Steps Editor
            </h3>
            <button 
              @click="$emit('close')"
              class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
            >
              <X class="h-5 w-5" />
            </button>
          </div>
        </div>

        <!-- Content -->
        <div class="bg-white dark:bg-gray-900 px-6 py-4">
          <div class="text-center py-12">
            <Wrench class="h-16 w-16 text-gray-300 mx-auto mb-4" />
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">
              Steps Editor Coming Soon
            </h3>
            <p class="text-gray-500 dark:text-gray-400">
              The visual steps editor is under development. For now, steps can be configured through the API.
            </p>
          </div>
        </div>

        <!-- Footer -->
        <div class="bg-gray-50 dark:bg-gray-800 px-6 py-3 flex justify-end">
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
import { X, Wrench } from 'lucide-vue-next'
import type { AutomationStep } from '~/types/automation'

interface Props {
  steps: AutomationStep[]
  isOpen: boolean
}

interface Emits {
  (e: 'close'): void
  (e: 'save', steps: AutomationStep[]): void
}

defineProps<Props>()
defineEmits<Emits>()
</script>
