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
      <div class="inline-block align-bottom bg-white dark:bg-gray-900 rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full">
        <!-- Header -->
        <div class="bg-white dark:bg-gray-900 px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white" id="modal-title">
              {{ isEditing ? 'Edit Task' : 'Create New Task' }}
            </h3>
            <button 
              @click="$emit('close')"
              class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
            >
              <X class="h-5 w-5" />
            </button>
          </div>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="bg-white dark:bg-gray-900">
          <div class="px-6 py-4 space-y-6 max-h-96 overflow-y-auto">
            <!-- Basic Info -->
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Task Name *
                </label>
                <input 
                  v-model="formData.name"
                  type="text" 
                  required
                  placeholder="Enter task name..."
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Description
                </label>
                <textarea 
                  v-model="formData.description"
                  rows="3"
                  placeholder="Describe what this automation does..."
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                ></textarea>
              </div>
            </div>

            <!-- Quick Setup -->
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                Quick Setup
              </label>
              <div class="grid grid-cols-2 gap-3">
                <button 
                  type="button"
                  @click="applyTemplate('data-entry')"
                  class="p-3 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 text-left"
                >
                  <div class="flex items-center gap-2 mb-1">
                    <FileSpreadsheet class="h-4 w-4 text-primary-600 dark:text-primary-400" />
                    <span class="text-sm font-medium text-gray-900 dark:text-white">Data Entry</span>
                  </div>
                  <p class="text-xs text-gray-500 dark:text-gray-400">Excel to web form automation</p>
                </button>

                <button 
                  type="button"
                  @click="applyTemplate('web-scraping')"
                  class="p-3 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 text-left"
                >
                  <div class="flex items-center gap-2 mb-1">
                    <Globe class="h-4 w-4 text-primary-600 dark:text-primary-400" />
                    <span class="text-sm font-medium text-gray-900 dark:text-white">Web Scraping</span>
                  </div>
                  <p class="text-xs text-gray-500 dark:text-gray-400">Extract data from websites</p>
                </button>

                <button 
                  type="button"
                  @click="applyTemplate('form-filling')"
                  class="p-3 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 text-left"
                >
                  <div class="flex items-center gap-2 mb-1">
                    <Edit3 class="h-4 w-4 text-primary-600 dark:text-primary-400" />
                    <span class="text-sm font-medium text-gray-900 dark:text-white">Form Filling</span>
                  </div>
                  <p class="text-xs text-gray-500 dark:text-gray-400">Automated form completion</p>
                </button>

                <button 
                  type="button"
                  @click="applyTemplate('live-test')"
                  class="p-3 border border-primary-200 dark:border-primary-700 bg-primary-50 dark:bg-primary-900/20 rounded-lg hover:bg-primary-100 dark:hover:bg-primary-900/30 text-left"
                >
                  <div class="flex items-center gap-2 mb-1">
                    <Monitor class="h-4 w-4 text-primary-600 dark:text-primary-400" />
                    <span class="text-sm font-medium text-gray-900 dark:text-white">Live Browser Test</span>
                  </div>
                  <p class="text-xs text-gray-500 dark:text-gray-400">Interactive test with VNC streaming</p>
                </button>

                <button 
                  type="button"
                  @click="applyTemplate('custom')"
                  class="p-3 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 text-left"
                >
                  <div class="flex items-center gap-2 mb-1">
                    <Wrench class="h-4 w-4 text-primary-600 dark:text-primary-400" />
                    <span class="text-sm font-medium text-gray-900 dark:text-white">Custom</span>
                  </div>
                  <p class="text-xs text-gray-500 dark:text-gray-400">Build from scratch</p>
                </button>
              </div>
            </div>

            <!-- Initial Prerequisites -->
            <div v-if="formData.prerequisites.length > 0">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                Prerequisites
              </label>
              <div class="space-y-3">
                <div 
                  v-for="(prerequisite, index) in formData.prerequisites" 
                  :key="index"
                  class="flex items-center gap-3 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg"
                >
                  <component :is="getPrerequisiteIcon(prerequisite.type)" class="h-4 w-4 text-gray-500" />
                  <div class="flex-1">
                    <input 
                      v-model="prerequisite.label"
                      type="text" 
                      placeholder="Prerequisite name..."
                      class="w-full px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
                    />
                  </div>
                  <label class="flex items-center">
                    <input 
                      v-model="prerequisite.required"
                      type="checkbox"
                      class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                    />
                    <span class="ml-1 text-xs text-gray-500 dark:text-gray-400">Required</span>
                  </label>
                  <button 
                    type="button"
                    @click="removePrerequisite(index)"
                    class="p-1 text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded"
                  >
                    <X class="h-3 w-3" />
                  </button>
                </div>
              </div>
            </div>

            <!-- Settings -->
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                Settings
              </label>
              <div class="space-y-3">
                <label class="flex items-center">
                  <input 
                    v-model="formData.settings.headless"
                    type="checkbox"
                    class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                  />
                  <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">Run in headless mode</span>
                </label>

                <label class="flex items-center">
                  <input 
                    v-model="formData.settings.takeScreenshots"
                    type="checkbox"
                    class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                  />
                  <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">Take screenshots</span>
                </label>

                <div class="grid grid-cols-2 gap-3">
                  <div>
                    <label class="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Timeout (seconds)
                    </label>
                    <input 
                      v-model.number="formData.settings.timeout"
                      type="number"
                      min="5"
                      max="300"
                      class="w-full px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                    />
                  </div>

                  <div>
                    <label class="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Retry Attempts
                    </label>
                    <input 
                      v-model.number="formData.settings.retryAttempts"
                      type="number"
                      min="0"
                      max="5"
                      class="w-full px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Footer -->
          <div class="bg-gray-50 dark:bg-gray-800 px-6 py-3 flex justify-end gap-3">
            <button 
              type="button"
              @click="$emit('close')"
              class="px-4 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700"
            >
              Cancel
            </button>
            <button 
              type="submit"
              :disabled="!formData.name.trim()"
              class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ isEditing ? 'Update Task' : 'Create Task' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { 
  X, FileSpreadsheet, Globe, Edit3, Wrench, Upload, Type, Link, Hash, Monitor 
} from 'lucide-vue-next'
import type { 
  AutomationTask, 
  CreateTaskData, 
  TaskSettings,
  Prerequisite,
  PrerequisiteType 
} from '~/types/automation'

interface Props {
  task?: AutomationTask | null
  isOpen: boolean
}

interface Emits {
  (e: 'close'): void
  (e: 'save', data: CreateTaskData): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

// Computed
const isEditing = computed(() => !!props.task)

// Form data
const formData = ref<CreateTaskData>({
  name: '',
  description: '',
  prerequisites: [],
  steps: [],
  settings: {
    headless: false,
    takeScreenshots: true,
    timeout: 30,
    retryAttempts: 3,
    waitBetweenSteps: 1000
  }
})

// Watch for task changes
watch(() => props.task, (newTask) => {
  if (newTask) {
    formData.value = {
      name: newTask.name,
      description: newTask.description,
      prerequisites: newTask.prerequisites.map(p => ({ ...p })),
      steps: newTask.steps.map(s => ({ ...s })),
      settings: { ...newTask.settings }
    }
  } else {
    resetForm()
  }
}, { immediate: true })

// Methods
const resetForm = () => {
  formData.value = {
    name: '',
    description: '',
    prerequisites: [],
    steps: [],
    settings: {
      headless: false,
      takeScreenshots: true,
      timeout: 30,
      retryAttempts: 3,
      waitBetweenSteps: 1000
    }
  }
}

const applyTemplate = (templateType: string) => {
  const templates = {
    'data-entry': {
      description: 'Automates data entry from Excel files to web forms',
      prerequisites: [
        {
          type: 'file_upload' as PrerequisiteType,
          label: 'Excel File',
          required: true
        },
        {
          type: 'url_input' as PrerequisiteType,
          label: 'Target Website URL',
          required: true
        }
      ]
    },
    'web-scraping': {
      description: 'Extracts data from websites and saves to Excel',
      prerequisites: [
        {
          type: 'url_input' as PrerequisiteType,
          label: 'Website URL',
          required: true
        },
        {
          type: 'text_input' as PrerequisiteType,
          label: 'CSS Selectors',
          required: false
        }
      ]
    },
    'form-filling': {
      description: 'Automatically fills out web forms with provided data',
      prerequisites: [
        {
          type: 'url_input' as PrerequisiteType,
          label: 'Form URL',
          required: true
        },
        {
          type: 'file_upload' as PrerequisiteType,
          label: 'Data File (CSV/Excel)',
          required: false
        }
      ]
    },
    'live-test': {
      description: 'Interactive test automation with live browser view using Playwright + VNC streaming',
      prerequisites: []
    },
    'custom': {
      description: 'Custom automation workflow',
      prerequisites: []
    }
  }

  const template = templates[templateType as keyof typeof templates]
  if (template) {
    formData.value.description = template.description
    formData.value.prerequisites = template.prerequisites.map((p, index) => ({
      ...p,
      id: `prereq_${Date.now()}_${index}`
    }))
  }
}

const removePrerequisite = (index: number) => {
  formData.value.prerequisites.splice(index, 1)
}

const getPrerequisiteIcon = (type: PrerequisiteType) => {
  const icons = {
    file_upload: Upload,
    text_input: Type,
    url_input: Link,
    number_input: Hash,
    select: Edit3
  }
  return icons[type] || Type
}

const handleSubmit = () => {
  emit('save', { ...formData.value })
}

// Handle escape key
const handleEscape = (event: KeyboardEvent) => {
  if (event.key === 'Escape') {
    emit('close')
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleEscape)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscape)
})
</script>

<style scoped>
/* Ensure modal appears above everything */
.fixed {
  z-index: 1000;
}

/* Smooth transitions */
.transition-opacity {
  transition-property: opacity;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

/* Ensure form scrolls properly */
.max-h-96 {
  max-height: 24rem;
}

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
