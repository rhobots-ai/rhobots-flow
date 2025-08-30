<template>
  <div class="space-y-2">
    <!-- Text Input -->
    <input 
      v-if="field.type === 'text_input'"
      :type="getInputType()"
      v-model="localValue"
      :placeholder="field.label"
      :required="field.required"
      class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
      @input="handleUpdate"
      @blur="validateField"
    />
    
    <!-- URL Input -->
    <input 
      v-else-if="field.type === 'url_input'"
      type="url"
      v-model="localValue"
      :placeholder="field.label || 'https://example.com'"
      :required="field.required"
      class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
      @input="handleUpdate"
      @blur="validateField"
    />
    
    <!-- Number Input -->
    <input 
      v-else-if="field.type === 'number_input'"
      type="number"
      v-model.number="localValue"
      :placeholder="field.label"
      :required="field.required"
      class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
      @input="handleUpdate"
      @blur="validateField"
    />
    
    <!-- Select Dropdown -->
    <select 
      v-else-if="field.type === 'select' && field.options"
      v-model="localValue"
      :required="field.required"
      class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
      @change="handleUpdate"
    >
      <option value="">{{ field.placeholder || `Choose ${field.label}...` }}</option>
      <option v-for="option in field.options" :key="option" :value="option">
        {{ option }}
      </option>
    </select>
    
    <!-- File Upload -->
    <div v-else-if="field.type === 'file'">
      <AutomationFileUploadDropzone
        :accept="getFileAcceptTypes()"
        :value="localValue"
        @upload="handleFileUpload"
        @remove="handleFileRemove"
      />
    </div>
    
    <!-- Textarea for long text -->
    <textarea 
      v-else-if="field.type === 'textarea'"
      v-model="localValue"
      :placeholder="field.placeholder || field.label"
      :required="field.required"
      rows="3"
      class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
      @input="handleUpdate"
      @blur="validateField"
    />
    
    <!-- Email Input -->
    <input 
      v-else-if="field.type === 'email'"
      type="email"
      v-model="localValue"
      :placeholder="field.placeholder || 'user@example.com'"
      :required="field.required"
      class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
      @input="handleUpdate"
      @blur="validateField"
    />
    
    <!-- Password Input -->
    <div v-else-if="field.type === 'password'" class="relative">
      <input 
        :type="showPassword ? 'text' : 'password'"
        v-model="localValue"
        :placeholder="field.placeholder || 'Enter password'"
        :required="field.required"
        class="w-full px-3 py-2 pr-10 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        @input="handleUpdate"
        @blur="validateField"
      />
      <button
        type="button"
        @click="showPassword = !showPassword"
        class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
      >
        <Eye v-if="!showPassword" class="h-4 w-4" />
        <EyeOff v-else class="h-4 w-4" />
      </button>
    </div>
    
    <!-- Validation Errors -->
    <div v-if="validationError" class="flex items-center gap-2 text-red-600 dark:text-red-400 text-sm">
      <AlertCircle class="h-4 w-4" />
      <span>{{ validationError }}</span>
    </div>
    
    <!-- Help Text -->
    <p v-if="field.helpText" class="text-xs text-gray-500 dark:text-gray-400">
      {{ field.helpText }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { AlertCircle, Eye, EyeOff } from 'lucide-vue-next'
import type { DynamicField, ValidationRule } from '~/types/automation'

interface Props {
  field: DynamicField
}

interface Emits {
  (e: 'update', value: any): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

// Local state
const localValue = ref(props.field.value || '')
const validationError = ref<string>('')
const showPassword = ref(false)

// Watch for external value changes
watch(() => props.field.value, (newValue) => {
  localValue.value = newValue || ''
  validationError.value = ''
}, { immediate: true })

// Methods
const handleUpdate = () => {
  emit('update', localValue.value)
  validationError.value = ''
}

const handleFileUpload = (file: File) => {
  localValue.value = file
  emit('update', file)
}

const handleFileRemove = () => {
  localValue.value = null
  emit('update', null)
}

const getInputType = (): string => {
  // Determine input type based on field label/name
  const label = props.field.label.toLowerCase()
  
  if (label.includes('email')) return 'email'
  if (label.includes('password') || label.includes('secret')) return 'password'
  if (label.includes('phone') || label.includes('tel')) return 'tel'
  if (label.includes('url') || label.includes('website') || label.includes('link')) return 'url'
  if (label.includes('number') || label.includes('count') || label.includes('quantity')) return 'number'
  
  return 'text'
}

const getFileAcceptTypes = (): string[] => {
  const label = props.field.label.toLowerCase()
  
  if (label.includes('excel') || label.includes('spreadsheet')) {
    return ['.xlsx', '.xls', '.csv']
  }
  if (label.includes('image') || label.includes('photo')) {
    return ['.jpg', '.jpeg', '.png', '.gif']
  }
  if (label.includes('pdf')) {
    return ['.pdf']
  }
  if (label.includes('document')) {
    return ['.doc', '.docx', '.txt', '.pdf']
  }
  
  return ['.txt', '.pdf', '.doc', '.docx', '.xlsx', '.csv']
}

const validateField = () => {
  if (!props.field.validation) return
  
  for (const rule of props.field.validation) {
    const error = validateRule(rule, localValue.value)
    if (error) {
      validationError.value = error
      return
    }
  }
  
  validationError.value = ''
}

const validateRule = (rule: ValidationRule, value: any): string => {
  switch (rule.type) {
    case 'required':
      if (!value || (typeof value === 'string' && value.trim() === '')) {
        return rule.message || 'This field is required'
      }
      break
      
    case 'minLength':
      if (typeof value === 'string' && value.length < rule.value) {
        return rule.message || `Minimum length is ${rule.value} characters`
      }
      break
      
    case 'maxLength':
      if (typeof value === 'string' && value.length > rule.value) {
        return rule.message || `Maximum length is ${rule.value} characters`
      }
      break
      
    case 'pattern':
      if (typeof value === 'string' && !new RegExp(rule.value).test(value)) {
        return rule.message || 'Invalid format'
      }
      break
      
    case 'email':
      if (typeof value === 'string') {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        if (!emailRegex.test(value)) {
          return rule.message || 'Please enter a valid email address'
        }
      }
      break
      
    case 'url':
      if (typeof value === 'string') {
        try {
          new URL(value)
        } catch {
          return rule.message || 'Please enter a valid URL'
        }
      }
      break
  }
  
  return ''
}

// Auto-validate when component mounts if field has a value
onMounted(() => {
  if (props.field.value) {
    nextTick(() => {
      validateField()
    })
  }
})
</script>

<style scoped>
/* Ensure consistent input styling */
input, select, textarea {
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

input:focus, select:focus, textarea:focus {
  outline: none;
}

/* Error state styling */
input:invalid, select:invalid, textarea:invalid {
  border-color: #ef4444;
}

/* Password toggle button positioning */
.relative input[type="password"], 
.relative input[type="text"] {
  padding-right: 2.5rem;
}
</style>
