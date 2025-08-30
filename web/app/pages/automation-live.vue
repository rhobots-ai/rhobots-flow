<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <div class="max-w-7xl mx-auto p-6">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-gray-100">
          Live Browser Automation
        </h1>
        <p class="mt-2 text-lg text-gray-600 dark:text-gray-400">
          Watch and interact with automation in real-time using VNC streaming
        </p>
      </div>

      <!-- Control Panel -->
      <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm mb-6">
        <div class="p-6">
          <div class="flex items-center justify-between mb-6">
            <div class="flex items-center gap-4">
              <button 
                @click="startAutomation" 
                :disabled="isBusy"
                class="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
              >
                {{ isBusy ? 'Running...' : 'Start Live Automation' }}
              </button>
              
              <button 
                v-if="isPaused" 
                @click="resumeAutomation"
                class="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium flex items-center gap-2"
              >
                <Play class="h-4 w-4" />
                Resume Automation
              </button>
              
              <button 
                v-if="isConnected" 
                @click="stopAutomation"
                class="px-4 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-medium"
              >
                Stop
              </button>
            </div>
            
            <div class="flex items-center gap-4">
              <!-- Connection Status -->
              <div class="flex items-center gap-2">
                <div 
                  :class="[
                    'w-3 h-3 rounded-full',
                    isConnected ? 'bg-green-500 animate-pulse' : 'bg-gray-400'
                  ]"
                ></div>
                <span class="text-sm text-gray-600 dark:text-gray-400">
                  {{ isConnected ? 'Connected' : 'Disconnected' }}
                </span>
              </div>
              
              <!-- Browser Health -->
              <button 
                @click="checkBrowserHealth"
                class="px-3 py-2 text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
              >
                Health Check
              </button>
            </div>
          </div>
          
          <!-- Status Display -->
          <div 
            class="p-4 rounded-lg text-sm font-medium"
            :class="statusClass"
          >
            <div class="flex items-center gap-2">
              <div 
                v-if="statusType === 'running'"
                class="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin"
              ></div>
              <div 
                v-else-if="statusType === 'paused'"
                class="w-2 h-2 bg-current rounded-full animate-pulse"
              ></div>
              <strong>Status:</strong> {{ statusMessage }}
            </div>
          </div>
        </div>
      </div>

      <!-- VNC Viewer Container -->
      <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm overflow-hidden">
        <div class="border-b border-gray-200 dark:border-gray-700 px-6 py-4">
          <div class="flex items-center justify-between">
            <h2 class="text-lg font-medium text-gray-900 dark:text-gray-100">
              Browser Viewport
            </h2>
            
            <div class="flex items-center gap-3">
              <!-- VNC Controls -->
              <div class="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400">
                <Monitor class="h-4 w-4" />
                <span>Live VNC Stream</span>
              </div>
              
              <!-- Interactive Mode Indicator -->
              <div 
                v-if="isPaused"
                class="flex items-center gap-2 px-3 py-1 bg-green-100 dark:bg-green-900/20 text-green-800 dark:text-green-200 rounded-full text-sm font-medium"
              >
                <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                Interactive Mode
              </div>
            </div>
          </div>
        </div>
        
        <!-- VNC Canvas Container -->
        <div class="relative bg-black" style="height: 600px;">
          <!-- VNC Canvas -->
          <div 
            id="vnc-canvas" 
            class="w-full h-full"
            :class="{ 
              'cursor-crosshair': isPaused,
              'cursor-not-allowed': !isPaused && isConnected 
            }"
          ></div>
          
          <!-- Loading Overlay -->
          <div 
            v-if="isConnecting"
            class="absolute inset-0 bg-black bg-opacity-80 flex items-center justify-center z-10"
          >
            <div class="text-center text-white">
              <div class="w-8 h-8 border-2 border-white border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
              <p class="text-lg font-medium">{{ statusMessage }}</p>
              <p class="text-sm text-gray-300 mt-2">Establishing VNC connection...</p>
            </div>
          </div>
          
          <!-- Error Overlay -->
          <div 
            v-if="errorMessage"
            class="absolute inset-0 bg-red-900 bg-opacity-80 flex items-center justify-center z-10"
          >
            <div class="text-center text-white max-w-md">
              <AlertCircle class="h-12 w-12 mx-auto mb-4 text-red-300" />
              <h3 class="text-lg font-medium mb-2">Connection Error</h3>
              <p class="text-sm text-red-100 mb-4">{{ errorMessage }}</p>
              <button 
                @click="retryConnection"
                class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
              >
                Retry Connection
              </button>
            </div>
          </div>
          
          <!-- Empty State -->
          <div 
            v-if="!isConnected && !isConnecting && !errorMessage"
            class="absolute inset-0 bg-gray-100 dark:bg-gray-800 flex items-center justify-center"
          >
            <div class="text-center max-w-md">
              <Monitor class="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">
                Live Browser Automation
              </h3>
              <p class="text-gray-600 dark:text-gray-400 mb-6">
                Click "Start Live Automation" to begin. You'll see a live view of the browser and can interact during pause points.
              </p>
              <div class="grid grid-cols-3 gap-4 text-sm text-gray-500 dark:text-gray-400">
                <div class="flex flex-col items-center">
                  <Eye class="h-6 w-6 mb-2" />
                  <span>Real-time View</span>
                </div>
                <div class="flex flex-col items-center">
                  <Mouse class="h-6 w-6 mb-2" />
                  <span>Interactive Control</span>
                </div>
                <div class="flex flex-col items-center">
                  <Shield class="h-6 w-6 mb-2" />
                  <span>Secure Streaming</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Debug Panel (Development Only) -->
      <div 
        v-if="showDebugPanel"
        class="mt-6 bg-gray-100 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4"
      >
        <h3 class="text-sm font-medium text-gray-900 dark:text-gray-100 mb-3">Debug Information</h3>
        <div class="grid grid-cols-2 gap-4 text-sm">
          <div>
            <strong>Session ID:</strong> {{ sessionId }}
          </div>
          <div>
            <strong>VNC URL:</strong> ws://{{ process.client ? window.location?.host : 'localhost:3000' }}/vnc
          </div>
          <div>
            <strong>WebSocket URL:</strong> ws://{{ process.client ? window.location?.host : 'localhost:3000' }}/ws/automation/{{ sessionId }}/
          </div>
          <div>
            <strong>Browser Status:</strong> {{ browserHealth?.status || 'Unknown' }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { v4 as uuidv4 } from 'uuid'
import { 
  Play, Monitor, Eye, Mouse, Shield, AlertCircle
} from 'lucide-vue-next'

// Page metadata
definePageMeta({
  layout: 'default',
  middleware: 'auth'
})

// State
const sessionId = ref(uuidv4())
const statusMessage = ref('Ready to start automation')
const statusType = ref('idle')
const isPaused = ref(false)
const isConnecting = ref(false)
const isConnected = ref(false)
const errorMessage = ref('')
const showDebugPanel = ref(process.dev)
const browserHealth = ref(null)

// WebSocket and VNC connections
const automationSocket = ref<WebSocket | null>(null)
const vncClient = ref<any>(null)

// Computed
const isBusy = computed(() => ['connecting', 'running'].includes(statusType.value))

const statusClass = computed(() => {
  const baseClasses = 'px-4 py-3 rounded-lg'
  switch (statusType.value) {
    case 'idle':
      return `${baseClasses} bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200`
    case 'connecting':
    case 'running':
      return `${baseClasses} bg-blue-100 dark:bg-blue-900/20 text-blue-800 dark:text-blue-200`
    case 'paused':
      return `${baseClasses} bg-yellow-100 dark:bg-yellow-900/20 text-yellow-800 dark:text-yellow-200`
    case 'completed':
      return `${baseClasses} bg-green-100 dark:bg-green-900/20 text-green-800 dark:text-green-200`
    case 'error':
      return `${baseClasses} bg-red-100 dark:bg-red-900/20 text-red-800 dark:text-red-200`
    default:
      return `${baseClasses} bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200`
  }
})

// VNC Connection
const connectVNC = async () => {
  try {
    console.log('Establishing VNC connection...')
    
    const { default: RFB } = await import('@novnc/novnc/core/rfb')
    const vncCanvas = document.getElementById('vnc-canvas')
    
    if (!vncCanvas) {
      throw new Error('VNC canvas element not found')
    }
    
    vncCanvas.innerHTML = ''
    const vncUrl = `ws://${window.location.host}/vnc`
    
    vncClient.value = new RFB(vncCanvas, vncUrl, {
      scaleViewport: true,
      resizeSession: false,
      showDotCursor: true,
      background: '#000000'
    })
    
    // VNC event handlers
    vncClient.value.addEventListener('connect', () => {
      console.log('VNC connected successfully')
      isConnected.value = true
      errorMessage.value = ''
    })
    
    vncClient.value.addEventListener('disconnect', () => {
      console.log('VNC disconnected')
      isConnected.value = false
    })
    
    vncClient.value.addEventListener('securityfailure', (e: any) => {
      console.error('VNC security failure:', e.detail)
      throw new Error('VNC authentication failed')
    })
    
  } catch (error: any) {
    console.error('VNC connection error:', error)
    errorMessage.value = `Failed to establish VNC connection: ${error.message}`
    isConnected.value = false
    throw error
  }
}

// WebSocket Connection
const connectWebSocket = () => {
  if (automationSocket.value) {
    automationSocket.value.close()
  }
  
  const wsUrl = `ws://${window.location.host}/ws/automation/${sessionId.value}/`
  console.log(`Connecting to automation WebSocket: ${wsUrl}`)
  
  automationSocket.value = new WebSocket(wsUrl)
  
  automationSocket.value.onopen = () => {
    console.log('Automation WebSocket connected')
  }
  
  automationSocket.value.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)
      console.log('WebSocket message:', data)
      
      if (data.type === 'status_update') {
        handleStatusUpdate(data.status, data.message)
      }
    } catch (error) {
      console.error('Error parsing WebSocket message:', error)
    }
  }
  
  automationSocket.value.onerror = (error) => {
    console.error('WebSocket error:', error)
    errorMessage.value = 'WebSocket connection failed'
  }
  
  automationSocket.value.onclose = () => {
    console.log('WebSocket connection closed')
  }
}

// Status Handler
const handleStatusUpdate = (status: string, message: string) => {
  console.log(`Status update: ${status} - ${message}`)
  
  statusType.value = status
  statusMessage.value = message
  
  switch (status) {
    case 'paused':
      isPaused.value = true
      break
    case 'running':
    case 'completed':
      isPaused.value = false
      break
    case 'error':
      isPaused.value = false
      errorMessage.value = message
      break
  }
}

// Actions
const startAutomation = async () => {
  try {
    sessionId.value = uuidv4()
    statusType.value = 'connecting'
    statusMessage.value = 'Starting automation...'
    isConnecting.value = true
    errorMessage.value = ''
    
    // Connect VNC first
    await connectVNC()
    
    // Connect WebSocket
    connectWebSocket()
    
    // Start automation via API
    const { $fetch } = useNuxtApp()
    await $fetch('/api/system/automations/start/', {
      method: 'POST',
      body: { sessionId: sessionId.value }
    })
    
    statusMessage.value = 'Automation started successfully'
    
  } catch (error: any) {
    console.error('Failed to start automation:', error)
    errorMessage.value = error.message || 'Failed to start automation'
    statusType.value = 'error'
    statusMessage.value = 'Failed to start automation'
  } finally {
    isConnecting.value = false
  }
}

const resumeAutomation = () => {
  if (automationSocket.value?.readyState === WebSocket.OPEN) {
    automationSocket.value.send(JSON.stringify({ command: 'resume' }))
    isPaused.value = false
    statusMessage.value = 'Resuming automation...'
  }
}

const stopAutomation = async () => {
  try {
    const { $fetch } = useNuxtApp()
    await $fetch('/api/system/automations/stop/', {
      method: 'POST',
      body: { sessionId: sessionId.value }
    })
  } catch (error) {
    console.error('Failed to stop automation:', error)
  }
  
  cleanup()
}

const checkBrowserHealth = async () => {
  try {
    const { $fetch } = useNuxtApp()
    const health = await $fetch('/api/system/browser/health/')
    browserHealth.value = health
    console.log('Browser health:', health)
  } catch (error) {
    console.error('Browser health check failed:', error)
  }
}

const retryConnection = () => {
  errorMessage.value = ''
  startAutomation()
}

const cleanup = () => {
  if (vncClient.value) {
    try {
      vncClient.value.disconnect()
    } catch (error) {
      console.warn('Error disconnecting VNC:', error)
    }
  }
  
  if (automationSocket.value) {
    automationSocket.value.close()
  }
  
  isConnected.value = false
  isPaused.value = false
  statusType.value = 'idle'
  statusMessage.value = 'Ready to start automation'
}

// Lifecycle
onMounted(() => {
  // Check browser health on load
  checkBrowserHealth()
})

onUnmounted(() => {
  cleanup()
})
</script>

<style scoped>
/* VNC Canvas Styling */
#vnc-canvas {
  background: #000;
}

#vnc-canvas canvas {
  width: 100% !important;
  height: 100% !important;
  object-fit: contain;
}
</style>
