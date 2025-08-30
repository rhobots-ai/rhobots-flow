<template>
  <div class="p-6 space-y-6 h-full overflow-y-auto">
    <!-- Prerequisites Section -->
    <div>
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Prerequisites</h3>
        <button 
          @click="addPrerequisite"
          class="p-1 text-primary-600 dark:text-primary-400 hover:bg-primary-50 dark:hover:bg-primary-900/20 rounded"
          title="Add Prerequisite"
        >
          <Plus class="h-4 w-4" />
        </button>
      </div>
      
      <div class="space-y-4">
        <!-- File Upload Section -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Excel/CSV File Upload
          </label>
          <AutomationFileUploadDropzone 
            :accept="['.xlsx', '.xls', '.csv']"
            @upload="handleFileUpload"
            :value="uploadedFile"
          />
        </div>
        
        <!-- Dynamic Prerequisites -->
        <div v-for="(prerequisite, index) in task.prerequisites" :key="prerequisite.id" class="space-y-2">
          <div class="flex items-center justify-between">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
              {{ prerequisite.label }}
              <span v-if="prerequisite.required" class="text-red-500">*</span>
            </label>
            <button 
              @click="removePrerequisite(index)"
              class="p-1 text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded"
              title="Remove"
            >
              <X class="h-3 w-3" />
            </button>
          </div>
          
          <AutomationDynamicField 
            :field="prerequisite"
            @update="(value) => updatePrerequisite(index, value)"
          />
        </div>
        
        <!-- Add Common Prerequisites -->
        <div class="border-t border-gray-200 dark:border-gray-700 pt-4">
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">Quick Add:</p>
          <div class="flex flex-wrap gap-2">
            <button 
              @click="addCommonPrerequisite('url')"
              class="px-3 py-1 text-xs bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700"
            >
              Website URL
            </button>
            <button 
              @click="addCommonPrerequisite('credentials')"
              class="px-3 py-1 text-xs bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700"
            >
              Login Credentials
            </button>
            <button 
              @click="addCommonPrerequisite('text')"
              class="px-3 py-1 text-xs bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700"
            >
              Text Input
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Automation Steps -->
    <div>
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Automation Steps</h3>
        <button 
          @click="showStepsEditor = true"
          class="px-3 py-1 text-sm bg-primary-600 text-white rounded-lg hover:bg-primary-700"
        >
          <Edit3 class="h-4 w-4 mr-1 inline" />
          Edit Steps
        </button>
      </div>
      
      <div class="space-y-2">
        <div 
          v-for="(step, index) in task.steps" 
          :key="step.id"
          class="flex items-center gap-3 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg"
        >
          <div class="flex-shrink-0 w-6 h-6 bg-primary-100 dark:bg-primary-900/50 text-primary-600 dark:text-primary-400 rounded-full flex items-center justify-center text-xs font-medium">
            {{ index + 1 }}
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium text-gray-900 dark:text-white truncate">
              {{ formatStepDescription(step) }}
            </p>
            <p class="text-xs text-gray-500 dark:text-gray-400">
              {{ step.type }} • {{ step.action }}
            </p>
          </div>
          <component :is="getStepIcon(step.type)" class="h-4 w-4 text-gray-400" />
        </div>
        
        <div v-if="task.steps.length === 0" class="text-center py-6 text-gray-500 dark:text-gray-400">
          <Zap class="h-8 w-8 mx-auto mb-2 opacity-50" />
          <p class="text-sm">No automation steps defined</p>
          <button 
            @click="showStepsEditor = true"
            class="mt-2 text-primary-600 dark:text-primary-400 hover:underline text-sm"
          >
            Add your first step
          </button>
        </div>
      </div>
    </div>

    <!-- Run Settings -->
    <div>
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Run Settings</h3>
      <div class="space-y-3">
        <label class="flex items-center">
          <input 
            type="checkbox" 
            v-model="localSettings.headless"
            @change="updateSettings"
            class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
          />
          <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">Headless mode</span>
          <span class="ml-1 text-xs text-gray-500">(run without visible browser)</span>
        </label>
        
        <label class="flex items-center">
          <input 
            type="checkbox" 
            v-model="localSettings.takeScreenshots"
            @change="updateSettings"
            class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
          />
          <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">Take screenshots</span>
          <span class="ml-1 text-xs text-gray-500">(capture key moments)</span>
        </label>
        
        <div class="space-y-2">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
            Timeout (seconds)
          </label>
          <input 
            type="number" 
            v-model.number="localSettings.timeout"
            @change="updateSettings"
            min="5"
            max="300"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg"
          />
        </div>
        
        <div class="space-y-2">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
            Retry Attempts
          </label>
          <input 
            type="number" 
            v-model.number="localSettings.retryAttempts"
            @change="updateSettings"
            min="0"
            max="5"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg"
          />
        </div>
        
        <div class="space-y-2">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
            Wait Between Steps (ms)
          </label>
          <input 
            type="number" 
            v-model.number="localSettings.waitBetweenSteps"
            @change="updateSettings"
            min="0"
            max="10000"
            step="100"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg"
          />
        </div>
      </div>
    </div>

    <!-- Steps Editor Modal -->
    <AutomationStepsEditor
      v-if="showStepsEditor"
      :steps="task.steps"
      :is-open="showStepsEditor"
      @close="showStepsEditor = false"
      @save="updateSteps"
    />
  </div>
</template>

<script setup lang="ts">
import { 
  Plus, X, Edit3, Zap, Mouse, Type, Navigation, Clock, 
  Camera, Download, Code, Eye
} from 'lucide-vue-next'
import type { 
  AutomationTask, 
  AutomationStep, 
  Prerequisite, 
  TaskSettings,
  StepType,
  PrerequisiteType
} from '~/types/automation'

interface Props {
  task: AutomationTask
}

interface Emits {
  (e: 'update', updates: Partial<AutomationTask>): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

// Local state
const showStepsEditor = ref(false)
const uploadedFile = ref<File | null>(null)
const localSettings = ref<TaskSettings>({ ...props.task.settings })

// Watch for task changes
watch(() => props.task.settings, (newSettings) => {
  localSettings.value = { ...newSettings }
}, { deep: true })

// Methods
const handleFileUpload = (file: File) => {
  uploadedFile.value = file
  // You can emit an update or handle the file upload here
}

const addPrerequisite = () => {
  const newPrerequisite: Prerequisite = {
    id: `prereq_${Date.now()}`,
    type: 'text_input' as PrerequisiteType,
    label: 'New Requirement',
    required: false
  }
  
  emit('update', {
    prerequisites: [...props.task.prerequisites, newPrerequisite]
  })
}

const removePrerequisite = (index: number) => {
  const prerequisites = [...props.task.prerequisites]
  prerequisites.splice(index, 1)
  emit('update', { prerequisites })
}

const updatePrerequisite = (index: number, updates: Partial<Prerequisite>) => {
  const prerequisites = [...props.task.prerequisites]
  prerequisites[index] = { ...prerequisites[index], ...updates }
  emit('update', { prerequisites })
}

const addCommonPrerequisite = (type: 'url' | 'credentials' | 'text') => {
  const commonPrerequisites = {
    url: {
      type: 'url_input' as PrerequisiteType,
      label: 'Website URL',
      required: true,
      validation: [
        { type: 'required' as const, message: 'URL is required' },
        { type: 'url' as const, message: 'Please enter a valid URL' }
      ]
    },
    credentials: {
      type: 'text_input' as PrerequisiteType,
      label: 'Login Credentials',
      required: true
    },
    text: {
      type: 'text_input' as PrerequisiteType,
      label: 'Text Input',
      required: false
    }
  }
  
  const prerequisite: Prerequisite = {
    id: `prereq_${Date.now()}`,
    ...commonPrerequisites[type]
  }
  
  emit('update', {
    prerequisites: [...props.task.prerequisites, prerequisite]
  })
}

const updateSettings = () => {
  emit('update', {
    settings: { ...localSettings.value }
  })
}

const updateSteps = (steps: AutomationStep[]) => {
  emit('update', { steps })
  showStepsEditor.value = false
}

const formatStepDescription = (step: AutomationStep): string => {
  if (step.description) return step.description
  
  switch (step.action) {
    case 'navigate_to':
      return `Navigate to ${step.value || 'URL'}`
    case 'click_element':
      return `Click ${step.selector || 'element'}`
    case 'type_text':
      return `Type "${step.value || 'text'}" into ${step.selector || 'element'}`
    case 'wait_for_element':
      return `Wait for ${step.selector || 'element'}`
    case 'take_screenshot':
      return 'Take screenshot'
    default:
      return `${step.type} action`
  }
}

const getStepIcon = (stepType: StepType) => {
  const icons = {
    navigate: Navigation,
    click: Mouse,
    type: Type,
    wait: Clock,
    scroll: Eye,
    screenshot: Camera,
    extract: Download,
    custom: Code
  }
  return icons[stepType] || Code
}
</script>

<style scoped>
/* Custom scrollbar for the config panel */
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
