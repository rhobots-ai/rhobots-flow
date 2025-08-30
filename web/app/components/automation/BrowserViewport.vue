<template>
  <div class="h-full flex flex-col bg-white dark:bg-gray-800 rounded-lg overflow-hidden border border-gray-200 dark:border-gray-700">
    <!-- Browser Chrome -->
    <div class="flex items-center gap-2 p-3 bg-gray-100 dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
      <!-- Window Controls -->
      <div class="flex items-center gap-1.5">
        <div class="w-3 h-3 rounded-full bg-red-500"></div>
        <div class="w-3 h-3 rounded-full bg-yellow-500"></div>
        <div class="w-3 h-3 rounded-full bg-green-500"></div>
      </div>
      
      <!-- Address Bar -->
      <div class="flex-1 mx-4">
        <div class="flex items-center bg-white dark:bg-gray-700 rounded-lg px-3 py-1.5 border border-gray-300 dark:border-gray-600">
          <Lock v-if="isSecure" class="h-3 w-3 text-green-600 dark:text-green-400 mr-2" />
          <Globe v-else class="h-3 w-3 text-gray-400 mr-2" />
          <input 
            type="text" 
            :value="currentUrl"
            readonly
            class="flex-1 text-xs bg-transparent border-none outline-none text-gray-600 dark:text-gray-300"
          />
        </div>
      </div>
      
      <!-- Browser Controls -->
      <div class="flex items-center gap-1">
        <button 
          @click="refresh"
          :disabled="!isRunning"
          class="p-1.5 hover:bg-gray-200 dark:hover:bg-gray-700 rounded disabled:opacity-50 disabled:cursor-not-allowed"
          title="Refresh"
        >
          <RefreshCw class="h-4 w-4 text-gray-600 dark:text-gray-400" />
        </button>
        
        <button 
          @click="toggleFullscreen"
          class="p-1.5 hover:bg-gray-200 dark:hover:bg-gray-700 rounded"
          title="Toggle Fullscreen"
        >
          <Maximize2 class="h-4 w-4 text-gray-600 dark:text-gray-400" />
        </button>
        
        <button 
          @click="takeScreenshot"
          :disabled="!isRunning"
          class="p-1.5 hover:bg-gray-200 dark:hover:bg-gray-700 rounded disabled:opacity-50 disabled:cursor-not-allowed"
          title="Take Screenshot"
        >
          <Camera class="h-4 w-4 text-gray-600 dark:text-gray-400" />
        </button>
      </div>
    </div>

    <!-- Browser Content Area -->
    <div class="flex-1 relative bg-white dark:bg-gray-900">
      <!-- Live Browser View -->
      <div v-if="isRunning && sessionId" class="h-full w-full">
        <!-- VNC/WebRTC Stream Container -->
        <div 
          ref="browserContainer"
          class="h-full w-full relative cursor-pointer"
          @click="handleClick"
          @mousemove="handleMouseMove"
        >
          <!-- VNC Canvas for live browser view -->
          <div 
            v-if="task.id === 'task_test'"
            id="vnc-canvas" 
            class="h-full w-full bg-black"
            :class="{ 'pointer-events-auto': canInteract, 'pointer-events-none': !canInteract }"
          ></div>
          
          <!-- Simulated view for other tasks -->
          <iframe
            v-else-if="simulatedUrl"
            :src="simulatedUrl"
            class="w-full h-full border-none"
            sandbox="allow-same-origin allow-scripts allow-forms"
            loading="lazy"
          />
          
          <!-- Loading overlay -->
          <div 
            v-if="isConnecting"
            class="absolute inset-0 bg-white dark:bg-gray-900 flex items-center justify-center z-10"
          >
            <div class="text-center">
              <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto mb-4"></div>
              <p class="text-sm text-gray-600 dark:text-gray-400">
                {{ task.id === 'task_test' ? 'Connecting to live browser...' : 'Connecting to browser...' }}
              </p>
            </div>
          </div>
          
          <!-- Interactive Control Indicators for Test Task -->
          <div 
            v-if="task.id === 'task_test' && canInteract"
            class="absolute top-4 left-4 bg-primary-600 text-white px-4 py-2 rounded-lg shadow-lg z-20"
          >
            <div class="flex items-center gap-2">
              <div class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
              <span class="text-sm font-medium">Interactive Mode - You can control the browser</span>
            </div>
          </div>
          
          <!-- Resume Button for Interactive Mode -->
          <div 
            v-if="task.id === 'task_test' && canInteract"
            class="absolute bottom-4 right-4 z-20"
          >
            <button 
              @click="resumeAutomation"
              class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 shadow-lg transition-colors flex items-center gap-2"
            >
              <Play class="h-4 w-4" />
              Resume Automation
            </button>
          </div>
          
          <!-- Interaction overlay -->
          <div 
            v-if="isRunning && !isConnecting"
            class="absolute inset-0 pointer-events-none"
          >
            <!-- Show current step indicator -->
            <div 
              v-if="currentStep"
              class="absolute top-4 left-4 bg-black/75 text-white px-3 py-2 rounded-lg text-sm font-medium"
            >
              Step {{ currentStep.order }}: {{ currentStep.description }}
            </div>
            
            <!-- Show interaction hints -->
            <div 
              v-if="highlightElement"
              class="absolute border-2 border-red-500 bg-red-500/20 rounded"
              :style="highlightElement"
            ></div>
          </div>
        </div>
      </div>
      
      <!-- Empty State -->
      <div v-else-if="!isRunning" class="h-full flex items-center justify-center bg-gray-50 dark:bg-gray-900">
        <div class="text-center max-w-md">
          <Monitor class="h-20 w-20 text-gray-300 dark:text-gray-600 mx-auto mb-6" />
          <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">
            Browser Viewport
          </h3>
          <p class="text-gray-500 dark:text-gray-400 mb-6">
            The live browser session will appear here when you run an automation. 
            You can interact with the page in real-time.
          </p>
          <div class="flex items-center justify-center gap-4 text-sm text-gray-400">
            <div class="flex items-center gap-2">
              <Mouse class="h-4 w-4" />
              <span>Click to interact</span>
            </div>
            <div class="flex items-center gap-2">
              <Eye class="h-4 w-4" />
              <span>Live view</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Error State -->
      <div v-else-if="connectionError" class="h-full flex items-center justify-center bg-gray-50 dark:bg-gray-900">
        <div class="text-center max-w-md">
          <AlertCircle class="h-16 w-16 text-red-400 mx-auto mb-4" />
          <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">
            Connection Failed
          </h3>
          <p class="text-gray-500 dark:text-gray-400 mb-6">
            {{ connectionError }}
          </p>
          <button 
            @click="reconnect"
            class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
          >
            Try Again
          </button>
        </div>
      </div>
    </div>
    
    <!-- Status Bar -->
    <div class="flex items-center justify-between px-3 py-2 bg-gray-50 dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 text-xs">
      <div class="flex items-center gap-4 text-gray-500 dark:text-gray-400">
        <span v-if="isRunning" class="flex items-center gap-1">
          <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          Live
        </span>
        <span v-if="sessionId">Session: {{ sessionId.slice(-8) }}</span>
        <span v-if="currentUrl">{{ getDomain(currentUrl) }}</span>
      </div>
      
      <div class="flex items-center gap-4 text-gray-500 dark:text-gray-400">
        <span v-if="viewport.width && viewport.height">
          {{ viewport.width }}×{{ viewport.height }}
        </span>
        <span v-if="isRunning && executionTime">
          {{ formatExecutionTime(executionTime) }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { 
  Globe, Lock, RefreshCw, Maximize2, Camera, Monitor, 
  Mouse, Eye, AlertCircle, Play
} from 'lucide-vue-next'
import type { AutomationTask, AutomationStep } from '~/types/automation'
import { StepAction, StepType } from '~/types/automation'
import type RFB from '@novnc/novnc/lib/rfb.js';

interface Props {
  task: AutomationTask
  isRunning: boolean
  sessionId: string | null
}

interface Emits {
  (e: 'interact', data: { x: number, y: number, type: 'click' | 'move' }): void
  (e: 'screenshot' | 'refresh'): void
  (e: 'completed' | 'error', data: { message: string }): void
  (e: 'statusChange', status: string): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

// State
const browserContainer = ref<HTMLElement>()
const currentUrl = ref('about:blank')
const isConnecting = ref(false)
const connectionError = ref<string>('')
const currentStep = ref<AutomationStep | null>(null)
const highlightElement = ref<{ top: string, left: string, width: string, height: string } | null>(null)
const viewport = ref({ width: 0, height: 0 })
const executionTime = ref(0)
const simulatedUrl = ref<string>('')
const canInteract = ref(false)
const vncClient = ref<RFB | null>(null)
const automationSocket = ref<WebSocket | null>(null)

// Computed
const isSecure = computed(() => currentUrl.value.startsWith('https://'))

// Methods
const handleClick = (event: MouseEvent) => {
  if (!props.isRunning) return
  
  const rect = browserContainer.value?.getBoundingClientRect()
  if (!rect) return
  
  const x = event.clientX - rect.left
  const y = event.clientY - rect.top
  
  emit('interact', { x, y, type: 'click' })
}

const handleMouseMove = (event: MouseEvent) => {
  if (!props.isRunning) return
  
  const rect = browserContainer.value?.getBoundingClientRect()
  if (!rect) return
  
  const x = event.clientX - rect.left
  const y = event.clientY - rect.top
  
  emit('interact', { x, y, type: 'move' })
}

const refresh = () => {
  emit('refresh')
}

const takeScreenshot = () => {
  emit('screenshot')
}

const toggleFullscreen = () => {
  if (!document.fullscreenElement) {
    browserContainer.value?.requestFullscreen()
  } else {
    document.exitFullscreen()
  }
}

const reconnect = () => {
  connectionError.value = ''
  connectToBrowser()
}

const connectToBrowser = async () => {
  if (!props.sessionId) return
  
  isConnecting.value = true
  connectionError.value = ''
  
  try {
    if (props.task.id === 'task_test') {
      // For the test task, establish VNC connection
      await connectVNC()
      // Setup WebSocket for automation control
      setupAutomationWebSocket()
    } else {
      // Simulate connection for demo tasks
      await new Promise(resolve => setTimeout(resolve, 2000))
      simulatedUrl.value = 'https://example.com'
    }
    
    currentUrl.value = 'https://angularformadd.netlify.app/'
    viewport.value = { width: 1920, height: 1080 }
    
  } catch (error: unknown) {
    console.error('Browser connection error:', error)
    connectionError.value = 'Failed to connect to browser session'
  } finally {
    isConnecting.value = false
  }
}

const connectVNC = async () => {
  try {
    console.log('Establishing VNC connection...')
    
    // Dynamic import of noVNC to avoid SSR issues
    const { default: RFB } = await import('@novnc/novnc/lib/rfb.js')
    
    const vncCanvas = document.getElementById('vnc-canvas')
    if (!vncCanvas) {
      throw new Error('VNC canvas element not found')
    }
    
    // Clear any existing content
    vncCanvas.innerHTML = ''
    
    // VNC connection URL - proxied through Nuxt dev server
    const vncUrl = `ws://${window.location.host}/vnc`
    
    console.log(`Connecting to VNC at: ${vncUrl}`)
    
    // Create RFB connection
    vncClient.value = new RFB(vncCanvas, vncUrl, {
      scaleViewport: true,
      resizeSession: false,
      showDotCursor: true,
      background: '#000000'
    })
    
    // Set up VNC event handlers
    const client = vncClient.value
    client.addEventListener('connect', () => {
      console.log('VNC connected successfully')
      currentUrl.value = 'https://angularformadd.netlify.app/'
    })
    
    client.addEventListener('disconnect', () => {
      console.log('VNC disconnected')
    })
    
    client.addEventListener('securityfailure', (e: CustomEvent) => {
      console.error('VNC security failure:', e.detail)
      throw new Error('VNC authentication failed')
    })
    
    // Wait for connection to establish
    await new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        reject(new Error('VNC connection timeout'))
      }, 10000) // 10 second timeout
      
      client.addEventListener('connect', () => {
        clearTimeout(timeout)
        resolve(true)
      })
      
      client.addEventListener('disconnect', () => {
        clearTimeout(timeout)
        reject(new Error('VNC connection failed'))
      })
    })
    
    console.log('VNC connection established for test task')
  } catch (error: unknown) {
    console.error('VNC connection error:', error)
    const errorMessage = error instanceof Error ? error.message : 'Unknown error'
    throw new Error(`Failed to establish VNC connection: ${errorMessage}`)
  }
}

const setupAutomationWebSocket = () => {
  if (!props.sessionId) return
  
  try {
    // Use proxied WebSocket connection through Nuxt dev server
    const wsUrl = `ws://${window.location.host}/ws/automation/${props.sessionId}/`
    
    console.log(`Connecting to automation WebSocket at: ${wsUrl}`)
    
    automationSocket.value = new WebSocket(wsUrl)
    
    automationSocket.value.onopen = () => {
      console.log('Automation WebSocket connected')
    }
    
    automationSocket.value.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        console.log('WebSocket message received:', data)
        
        if (data.type === 'status_update') {
          handleAutomationStatus(data.status, data.message, data.step_info)
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error)
      }
    }
    
    automationSocket.value.onerror = (error) => {
      console.error('WebSocket error:', error)
    }
    
    automationSocket.value.onclose = (event) => {
      console.log('WebSocket connection closed:', event.code, event.reason)
    }
    
  } catch (error) {
    console.error('WebSocket setup failed:', error)
  }
}

const handleAutomationStatus = (status: string, message: string, stepInfo?: AutomationStep) => {
  console.log(`Automation Status: ${status} - ${message}`)
  
  // Update connection status based on automation status
  switch (status) {
    case 'connecting':
      isConnecting.value = true
      connectionError.value = ''
      break
      
    case 'connected':
      isConnecting.value = false
      connectionError.value = ''
      break
      
    case 'running':
      isConnecting.value = false
      canInteract.value = false
      connectionError.value = ''
      if (stepInfo) {
        currentStep.value = stepInfo
      }
      break
      
    case 'paused':
      isConnecting.value = false
      canInteract.value = true
      connectionError.value = ''
      // Create interactive pause step
      currentStep.value = {
        id: 'interactive_step',
        type: StepType.CUSTOM,
        action: StepAction.INTERACTIVE_PAUSE,
        description: message || 'Interact with the form and click Resume when ready',
        order: 3
      }
      break
      
    case 'completed':
      isConnecting.value = false
      canInteract.value = false
      connectionError.value = ''
      currentStep.value = null
      // Emit completion event
      emit('completed', { message })
      break
      
    case 'error':
      isConnecting.value = false
      canInteract.value = false
      connectionError.value = message || 'An error occurred during automation'
      currentStep.value = null
      // Emit error event
      emit('error', { message: connectionError.value })
      break
      
    case 'disconnected':
      isConnecting.value = false
      canInteract.value = false
      currentStep.value = null
      break
      
    default:
      console.warn(`Unknown automation status: ${status}`)
  }
}

const resumeAutomation = () => {
  console.log('Resume automation button clicked')
  
  if (automationSocket.value && automationSocket.value.readyState === WebSocket.OPEN) {
    try {
      const resumeCommand = JSON.stringify({ command: 'resume' })
      automationSocket.value.send(resumeCommand)
      console.log('Resume command sent via WebSocket')
      
      // Immediately update UI state
      canInteract.value = false
      currentStep.value = {
        id: 'resuming_step',
        type: StepType.CUSTOM,
        action: StepAction.EXECUTE_SCRIPT, // Use a valid action
        description: 'Resuming automation...',
        order: 4
      }
      
    } catch (error) {
      console.error('Failed to send resume command:', error)
      connectionError.value = 'Failed to resume automation'
    }
  } else {
    console.warn('WebSocket not connected, cannot send resume command')
    connectionError.value = 'WebSocket connection lost. Please refresh and try again.'
  }
}

const getDomain = (url: string): string => {
  try {
    return new URL(url).hostname
  } catch {
    return url
  }
}

const formatExecutionTime = (seconds: number): string => {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return minutes > 0 
    ? `${minutes}m ${remainingSeconds}s`
    : `${remainingSeconds}s`
}

// Watchers
watch(() => props.sessionId, (newSessionId) => {
  if (newSessionId && props.isRunning) {
    connectToBrowser()
  }
})

watch(() => props.isRunning, (isRunning) => {
  if (isRunning && props.sessionId) {
    connectToBrowser()
    // Start execution timer
    const startTime = Date.now()
    const timer = setInterval(() => {
      executionTime.value = Math.floor((Date.now() - startTime) / 1000)
    }, 1000)
    
    // Clean up timer when component unmounts or stops running
    onUnmounted(() => clearInterval(timer))
    watch(() => props.isRunning, (stillRunning) => {
      if (!stillRunning) clearInterval(timer)
    })
  } else {
    simulatedUrl.value = ''
    currentUrl.value = 'about:blank'
    executionTime.value = 0
  }
})

// Listen for step updates (would come from WebSocket in real implementation)
const listenForStepUpdates = () => {
  if (!props.isRunning || props.task.steps.length === 0) return
  
  if (props.task.id === 'task_test') {
    // For test task, simulate the interactive flow
    let stepIndex = 0
    const stepTimer = setInterval(() => {
      if (stepIndex < props.task.steps.length) {
        const step = props.task.steps[stepIndex]
        if (step) {
          currentStep.value = step
          
          // Handle interactive pause
          if (step.action === StepAction.INTERACTIVE_PAUSE) {
            setTimeout(() => {
              canInteract.value = true
            }, 2000) // Give time for navigation
          }
        }
        
        stepIndex++
      } else {
        clearInterval(stepTimer)
        currentStep.value = null
      }
    }, 3000)
    
    // Clean up
    onUnmounted(() => clearInterval(stepTimer))
    watch(() => props.isRunning, (stillRunning) => {
      if (!stillRunning) {
        clearInterval(stepTimer)
        currentStep.value = null
        canInteract.value = false
      }
    })
  } else {
    // Simulate step updates for other tasks
    let stepIndex = 0
    const stepTimer = setInterval(() => {
      if (stepIndex < props.task.steps.length) {
        const step = props.task.steps[stepIndex]
        if (step) {
          currentStep.value = step
          
          // Simulate element highlighting
          if (step.selector) {
            highlightElement.value = {
              top: '20%',
              left: '30%',
              width: '200px',
              height: '40px'
            }
            
            setTimeout(() => {
              highlightElement.value = null
            }, 2000)
          }
        }
        stepIndex++
      } else {
        clearInterval(stepTimer)
        currentStep.value = null
      }
    }, 3000)
    
    // Clean up
    onUnmounted(() => clearInterval(stepTimer))
    watch(() => props.isRunning, (stillRunning) => {
      if (!stillRunning) {
        clearInterval(stepTimer)
        currentStep.value = null
        highlightElement.value = null
      }
    })
  }
}

// Lifecycle
onMounted(() => {
  if (props.isRunning && props.sessionId) {
    connectToBrowser()
    listenForStepUpdates()
  }
})

onUnmounted(() => {
  // Clean up connections
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
  
  // Reset state
  canInteract.value = false
  currentStep.value = null
})
</script>

<style scoped>
/* Smooth transitions */
.transition-all {
  transition: all 0.2s ease;
}

/* Fullscreen styles */
:fullscreen {
  background: black;
}

/* Animation for live indicator */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Highlight animation */
@keyframes highlight {
  0%, 100% {
    opacity: 0.6;
  }
  50% {
    opacity: 0.9;
  }
}

.highlight-element {
  animation: highlight 1s ease-in-out infinite;
}

/* Ensure iframe responsiveness */
iframe {
  min-height: 100%;
}
</style>
