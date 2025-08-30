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
      <div class="inline-block align-bottom bg-white dark:bg-gray-900 rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-5xl sm:w-full">
        <!-- Header -->
        <div class="bg-white dark:bg-gray-900 px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white" id="modal-title">
              Screenshots - Run #{{ run.id.slice(-6) }}
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
          <!-- Screenshots Grid -->
          <div v-if="run.screenshots && run.screenshots.length > 0" class="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div 
              v-for="(screenshot, index) in run.screenshots" 
              :key="index"
              class="relative group cursor-pointer"
              @click="selectedScreenshot = screenshot"
            >
              <div class="aspect-video bg-gray-100 dark:bg-gray-800 rounded-lg overflow-hidden border border-gray-200 dark:border-gray-700">
                <img 
                  :src="screenshot" 
                  :alt="`Screenshot ${index + 1}`"
                  class="w-full h-full object-cover"
                  loading="lazy"
                />
                <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-all duration-200 flex items-center justify-center">
                  <Eye class="h-6 w-6 text-white opacity-0 group-hover:opacity-100 transition-opacity duration-200" />
                </div>
              </div>
              <p class="mt-2 text-xs text-gray-500 dark:text-gray-400 text-center">
                Screenshot {{ index + 1 }}
              </p>
            </div>
          </div>

          <!-- Empty State -->
          <div v-else class="text-center py-12">
            <Camera class="h-16 w-16 text-gray-300 mx-auto mb-4" />
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">
              No Screenshots Available
            </h3>
            <p class="text-gray-500 dark:text-gray-400">
              This run didn't capture any screenshots.
            </p>
          </div>
        </div>

        <!-- Footer -->
        <div class="bg-gray-50 dark:bg-gray-800 px-6 py-3 flex justify-between">
          <div class="text-sm text-gray-500 dark:text-gray-400">
            {{ run.screenshots?.length || 0 }} screenshot(s)
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

    <!-- Full-size Screenshot Modal -->
    <div 
      v-if="selectedScreenshot"
      class="fixed inset-0 z-60 flex items-center justify-center bg-black bg-opacity-90"
      @click="selectedScreenshot = null"
    >
      <div class="relative max-w-full max-h-full p-4">
        <img 
          :src="selectedScreenshot" 
          alt="Full size screenshot"
          class="max-w-full max-h-full object-contain"
        />
        <button 
          @click="selectedScreenshot = null"
          class="absolute top-4 right-4 text-white hover:text-gray-300 bg-black bg-opacity-50 rounded-full p-2"
        >
          <X class="h-6 w-6" />
        </button>
        
        <!-- Navigation arrows (if multiple screenshots) -->
        <div v-if="run.screenshots && run.screenshots.length > 1" class="absolute inset-y-0 left-4 flex items-center">
          <button 
            @click.stop="navigateScreenshot(-1)"
            class="text-white hover:text-gray-300 bg-black bg-opacity-50 rounded-full p-2"
          >
            <ChevronLeft class="h-6 w-6" />
          </button>
        </div>
        
        <div v-if="run.screenshots && run.screenshots.length > 1" class="absolute inset-y-0 right-4 flex items-center">
          <button 
            @click.stop="navigateScreenshot(1)"
            class="text-white hover:text-gray-300 bg-black bg-opacity-50 rounded-full p-2"
          >
            <ChevronRight class="h-6 w-6" />
          </button>
        </div>

        <!-- Screenshot counter -->
        <div class="absolute bottom-4 left-1/2 transform -translate-x-1/2 text-white bg-black bg-opacity-50 px-3 py-1 rounded-full text-sm">
          {{ currentScreenshotIndex + 1 }} / {{ run.screenshots?.length || 0 }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { X, Camera, Eye, ChevronLeft, ChevronRight } from 'lucide-vue-next'
import type { RunHistory } from '~/types/automation'

interface Props {
  run: RunHistory
  isOpen: boolean
}

interface Emits {
  (e: 'close'): void
}

const props = defineProps<Props>()
defineEmits<Emits>()

const selectedScreenshot = ref<string | null>(null)

const currentScreenshotIndex = computed(() => {
  if (!selectedScreenshot.value || !props.run.screenshots) return 0
  return props.run.screenshots.indexOf(selectedScreenshot.value)
})

const navigateScreenshot = (direction: number) => {
  if (!props.run.screenshots || props.run.screenshots.length === 0) return
  
  const currentIndex = currentScreenshotIndex.value
  let newIndex = currentIndex + direction
  
  // Wrap around
  if (newIndex < 0) {
    newIndex = props.run.screenshots.length - 1
  } else if (newIndex >= props.run.screenshots.length) {
    newIndex = 0
  }
  
  selectedScreenshot.value = props.run.screenshots[newIndex]
}

// Handle keyboard navigation
const handleKeydown = (event: KeyboardEvent) => {
  if (!selectedScreenshot.value) return
  
  switch (event.key) {
    case 'Escape':
      selectedScreenshot.value = null
      break
    case 'ArrowLeft':
      navigateScreenshot(-1)
      break
    case 'ArrowRight':
      navigateScreenshot(1)
      break
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
/* Ensure modal appears above everything */
.z-60 {
  z-index: 1100;
}

/* Smooth transitions */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 200ms;
}

.transition-opacity {
  transition-property: opacity;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 200ms;
}

/* Image hover effects */
.group:hover img {
  transform: scale(1.05);
  transition: transform 0.2s ease;
}

/* Ensure images don't exceed container */
img {
  transition: transform 0.2s ease;
}

/* Full-screen image styling */
.max-w-full {
  max-width: calc(100vw - 2rem);
}

.max-h-full {
  max-height: calc(100vh - 2rem);
}
</style>
