<template>
  <div 
    class="relative border-2 border-dashed rounded-lg p-6 transition-colors"
    :class="[
      isDragActive 
        ? 'border-primary-400 bg-primary-50 dark:bg-primary-900/20 dark:border-primary-500' 
        : 'border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500',
      { 'cursor-not-allowed opacity-50': disabled }
    ]"
    @drop="handleDrop"
    @dragover="handleDragOver"
    @dragenter="handleDragEnter"
    @dragleave="handleDragLeave"
    @click="!disabled && fileInput?.click()"
  >
    <input
      ref="fileInput"
      type="file"
      :accept="accept.join(',')"
      :multiple="multiple"
      :disabled="disabled"
      class="hidden"
      @change="handleFileSelect"
    />
    
    <!-- Upload State -->
    <div v-if="!value && !isUploading" class="text-center">
      <Upload class="h-12 w-12 text-gray-400 mx-auto mb-4" />
      <div class="space-y-2">
        <p class="text-sm font-medium text-gray-900 dark:text-white">
          Drop your files here, or 
          <span class="text-primary-600 dark:text-primary-400 cursor-pointer hover:underline">
            browse
          </span>
        </p>
        <p class="text-xs text-gray-500 dark:text-gray-400">
          Supports: {{ accept.join(', ') }}
          <span v-if="maxSize">(Max: {{ formatFileSize(maxSize) }})</span>
        </p>
      </div>
    </div>
    
    <!-- Uploading State -->
    <div v-else-if="isUploading" class="text-center">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto mb-4"></div>
      <p class="text-sm text-gray-600 dark:text-gray-400">Uploading...</p>
      <div v-if="uploadProgress > 0" class="mt-3">
        <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
          <div 
            class="bg-primary-600 h-2 rounded-full transition-all duration-300"
            :style="{ width: uploadProgress + '%' }"
          ></div>
        </div>
        <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">{{ uploadProgress }}%</p>
      </div>
    </div>
    
    <!-- File Uploaded State -->
    <div v-else-if="value" class="flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="p-2 bg-green-100 dark:bg-green-900/30 rounded-lg">
          <component :is="getFileIcon(value.name)" class="h-5 w-5 text-green-600 dark:text-green-400" />
        </div>
        <div class="min-w-0 flex-1">
          <p class="text-sm font-medium text-gray-900 dark:text-white truncate">
            {{ value.name }}
          </p>
          <p class="text-xs text-gray-500 dark:text-gray-400">
            {{ formatFileSize(value.size) }} • {{ formatDate(value.lastModified) }}
          </p>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <button
          @click.stop="handlePreview"
          class="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
          title="Preview"
        >
          <Eye class="h-4 w-4" />
        </button>
        <button
          @click.stop="handleRemove"
          class="p-1 text-gray-400 hover:text-red-600 dark:hover:text-red-400"
          title="Remove"
        >
          <X class="h-4 w-4" />
        </button>
      </div>
    </div>
    
    <!-- Error State -->
    <div v-if="error" class="mt-3 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
      <div class="flex items-center gap-2">
        <AlertCircle class="h-4 w-4 text-red-600 dark:text-red-400" />
        <p class="text-sm text-red-600 dark:text-red-400">{{ error }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { 
  Upload, Eye, X, AlertCircle, FileText, 
  FileSpreadsheet, File, Image 
} from 'lucide-vue-next'

interface Props {
  accept: string[]
  multiple?: boolean
  maxSize?: number // in bytes
  value?: File | null
  disabled?: boolean
}

interface Emits {
  (e: 'upload', file: File): void
  (e: 'remove'): void
  (e: 'preview', file: File): void
}

const props = withDefaults(defineProps<Props>(), {
  multiple: false,
  disabled: false
})

const emit = defineEmits<Emits>()

// State
const fileInput = ref<HTMLInputElement>()
const isDragActive = ref(false)
const isUploading = ref(false)
const uploadProgress = ref(0)
const error = ref<string>('')

// Methods
const handleDragEnter = (e: DragEvent) => {
  e.preventDefault()
  if (!props.disabled) {
    isDragActive.value = true
  }
}

const handleDragOver = (e: DragEvent) => {
  e.preventDefault()
}

const handleDragLeave = (e: DragEvent) => {
  e.preventDefault()
  // Only set to false if we're leaving the dropzone entirely
  if (!e.currentTarget?.contains(e.relatedTarget as Node)) {
    isDragActive.value = false
  }
}

const handleDrop = (e: DragEvent) => {
  e.preventDefault()
  isDragActive.value = false
  
  if (props.disabled) return
  
  const files = Array.from(e.dataTransfer?.files || [])
  if (files.length > 0) {
    handleFiles(files)
  }
}

const handleFileSelect = (e: Event) => {
  const target = e.target as HTMLInputElement
  const files = Array.from(target.files || [])
  if (files.length > 0) {
    handleFiles(files)
  }
}

const handleFiles = async (files: File[]) => {
  error.value = ''
  
  const file = files[0] // Take first file for single upload
  
  // Validate file type
  const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase()
  if (!props.accept.includes(fileExtension)) {
    error.value = `File type not supported. Please upload: ${props.accept.join(', ')}`
    return
  }
  
  // Validate file size
  if (props.maxSize && file.size > props.maxSize) {
    error.value = `File too large. Maximum size: ${formatFileSize(props.maxSize)}`
    return
  }
  
  // Simulate upload progress
  isUploading.value = true
  uploadProgress.value = 0
  
  try {
    // Simulate upload with progress
    for (let i = 0; i <= 100; i += 10) {
      uploadProgress.value = i
      await new Promise(resolve => setTimeout(resolve, 50))
    }
    
    emit('upload', file)
  } catch (err) {
    error.value = 'Upload failed. Please try again.'
  } finally {
    isUploading.value = false
    uploadProgress.value = 0
  }
}

const handleRemove = () => {
  error.value = ''
  emit('remove')
  
  // Clear the input
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const handlePreview = () => {
  if (props.value) {
    emit('preview', props.value)
  }
}

const getFileIcon = (fileName: string) => {
  const extension = fileName.split('.').pop()?.toLowerCase()
  
  switch (extension) {
    case 'xlsx':
    case 'xls':
    case 'csv':
      return FileSpreadsheet
    case 'txt':
    case 'md':
      return FileText
    case 'jpg':
    case 'jpeg':
    case 'png':
    case 'gif':
      return Image
    default:
      return File
  }
}

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes'
  
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const formatDate = (timestamp: number): string => {
  return new Date(timestamp).toLocaleDateString()
}
</script>

<style scoped>
/* Smooth transitions for drag states */
.transition-colors {
  transition-property: color, background-color, border-color;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

/* Cursor styles */
.cursor-pointer {
  cursor: pointer;
}

.cursor-not-allowed {
  cursor: not-allowed;
}

/* Animation for upload progress */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
