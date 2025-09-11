<template>
  <div class="relative w-full h-full bg-black">
    <div :id="`vnc-screen-${uniqueId}`" class="absolute inset-0 w-full h-full"></div>

    <div v-if="connectionStatus"
         :class="statusClasses"
         class="absolute top-4 right-4 px-3 py-1 rounded text-sm">
      {{ connectionStatus }}
    </div>

    <div v-if="scriptCompleted"
         class="absolute top-4 left-4 bg-green-500 text-white px-3 py-1 rounded text-sm font-medium">
      ✓ Manual Control Active
    </div>

    <div v-if="isPaused"
         class="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex gap-2">
      <button @click="resume"
              class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
        Resume Automation
      </button>
    </div>

    <div v-if="isConnecting"
         class="absolute inset-0 bg-black bg-opacity-75 flex items-center justify-center">
      <div class="text-white text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
        <p>Connecting to browser...</p>
      </div>
    </div>
  </div>
  </template>

<script setup>
import { ref, onUnmounted, watch, computed, onMounted } from 'vue'
import { useSessionManager } from '@/app/composables/useSessionManager'

// Lazy-loaded noVNC (client-only)
let RFB = null
const loadRFB = async () => {
  if (!RFB && import.meta.client) {
    const mod = await import('@novnc/novnc/lib/rfb.js')
    RFB = mod.default || mod
  }
}

const props = defineProps({
  sessionId: String,
  isRunning: Boolean
})

const emit = defineEmits(['resume'])

const uniqueId = ref((typeof crypto !== 'undefined' && crypto.randomUUID) ? crypto.randomUUID() : `id-${Date.now()}-${Math.random().toString(36).slice(2)}`)
const vnc = ref(null)
const connectionStatus = ref('')
const isConnecting = ref(false)
const isPaused = ref(false)
const scriptCompleted = ref(false)
const sessionInfo = ref(null)

// Compute view-only: allow interaction when paused or after completion
const isViewOnly = computed(() => {
  return props.isRunning && !isPaused.value && !scriptCompleted.value
})

const statusClasses = computed(() => {
  const base = 'px-3 py-1 rounded text-sm font-medium'
  if (connectionStatus.value === 'Connected' || connectionStatus.value === 'Manual Control Active') {
    return `${base} bg-green-500 text-white`
  } else if (connectionStatus.value === 'Connecting...' || connectionStatus.value === 'connecting') {
    return `${base} bg-yellow-500 text-white`
  } else {
    return `${base} bg-red-500 text-white`
  }
})

const sm = useSessionManager()

const connectVNC = async (session) => {
  try {
    if (!import.meta.client) return
    await loadRFB()
    if (!RFB) return

    isConnecting.value = true
    connectionStatus.value = 'Connecting...'

    const screen = document.getElementById(`vnc-screen-${uniqueId.value}`)
    if (!screen) return
    if (vnc.value) vnc.value.disconnect()

    const url = session?.vnc_url || `ws://localhost:${session.web_port}/websockify`
    vnc.value = new RFB(screen, url, {
      shared: true,
      // Input policy: disable input while automation runs; enable for manual control
      viewOnly: isViewOnly.value,
      focusOnClick: true,
      // Make local clicks map correctly to remote by scaling instead of clipping
      scaleViewport: true,
      clipViewport: false,
      dragViewport: false,
      // Resize remote session to client size (helps full-window click mapping and cursor alignment)
      resizeSession: true,
      // Enable all input methods
      touchButton: 1,
      // CURSOR VISIBILITY: Critical settings for mouse cursor display
      showDotCursor: true,        // Show dot cursor when no local cursor
      localCursor: true,          // Use local cursor when possible
      cursorURIs: [],             // Use default cursor shapes
      credentials: { password: session?.password || '' }
    })

    vnc.value.addEventListener('connect', () => {
      connectionStatus.value = 'Connected'
      isConnecting.value = false
      // ensure interactive settings are applied post-connect
      try {
        vnc.value.scaleViewport = true
        vnc.value.clipViewport = false
        vnc.value.viewOnly = isViewOnly.value
        vnc.value.focus()
        // focus canvas to receive inputs
        const canvas = screen.querySelector('canvas')
        if (canvas) {
          canvas.style.pointerEvents = 'auto'
          canvas.style.cursor = 'default'
          canvas.style.touchAction = 'none'
          canvas.tabIndex = 0
          canvas.focus()
          console.log('VNC Canvas configured for input:', { 
            viewOnly: vnc.value.viewOnly, 
            allowInput: !isViewOnly.value,
            canvasTabIndex: canvas.tabIndex 
          })
        }
      } catch (e) {
        console.error('Error setting VNC properties:', e)
      }
    })

    vnc.value.addEventListener('disconnect', () => {
      connectionStatus.value = 'Disconnected'
      isConnecting.value = false
    })

    vnc.value.addEventListener('credentialsrequired', () => {
      vnc.value.sendCredentials({ password: session?.password || '' })
    })
  } catch (error) {
    console.error('VNC connection error:', error)
    connectionStatus.value = 'Connection failed'
    isConnecting.value = false
  }
}

const ensureSessionAndConnect = async () => {
  try {
    if (!props.sessionId) return
    // Use automation sessionId as the session manager user_id to reuse the engine-allocated session
    sessionInfo.value = await sm.createSession(props.sessionId)
    await connectVNC(sessionInfo.value)
  } catch (e) {
    console.warn('Failed to create/reuse VNC session for automation sessionId:', e)
  }
}

const disconnectVNC = () => {
  if (vnc.value) {
    vnc.value.disconnect()
    vnc.value = null
  }
}

const resume = () => {
  isPaused.value = false
  emit('resume')
}

watch(() => props.isRunning, (newVal) => {
  if (newVal) {
    scriptCompleted.value = false
    isPaused.value = false
    setTimeout(() => ensureSessionAndConnect(), 1000)
  } else if (!scriptCompleted.value) {
    // Keep VNC connected when automation stops to allow manual control
    // Do not disconnect here; switch viewOnly off via watcher below
  }
})

// apply viewOnly updates
watch(isViewOnly, (newVal) => {
  if (!vnc.value) return
  
  // Toggle view-only mode
  vnc.value.viewOnly = newVal
  
  if (!newVal) {
    // Manual control is now active - ensure canvas can receive input
    setTimeout(() => {
      try {
        vnc.value.focus()
        const screen = document.getElementById(`vnc-screen-${uniqueId.value}`)
        const canvas = screen ? screen.querySelector('canvas') : null
        if (canvas) {
          canvas.tabIndex = 0
          canvas.focus()
          canvas.style.pointerEvents = 'auto'
          canvas.style.cursor = 'default'
          canvas.style.touchAction = 'none'
          // Force a click event to ensure focus
          canvas.click()
          console.log('Manual control activated - Canvas focused for input:', {
            viewOnly: vnc.value.viewOnly,
            canvasTabIndex: canvas.tabIndex,
            pointerEvents: canvas.style.pointerEvents
          })
        }
      } catch (e) {
        console.error('Error activating manual control:', e)
      }
    }, 500) // Small delay to ensure VNC is ready
  }
})

// Handle WebSocket messages (status)
watch(() => props.sessionId, (newVal) => {
  if (!import.meta.client) return
  if (newVal) {
    // For development, connect directly to automation backend on port 8000
    const wsScheme = location.protocol === 'https:' ? 'wss' : 'ws'
    const hostname = location.hostname
    const wsUrl = `${wsScheme}://${hostname}:8000/ws/${newVal}`

    const ws = new WebSocket(wsUrl)
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.type === 'status') {
        switch (data.status) {
          case 'paused':
            isPaused.value = true
            break
          case 'completed':
            scriptCompleted.value = true
            isPaused.value = false
            connectionStatus.value = 'Manual Control Active'
            break
          case 'running':
            isPaused.value = false
            scriptCompleted.value = false
            break
          case 'stopped':
          case 'error':
            isPaused.value = false
            scriptCompleted.value = false
            break
        }
      }
    }
  }
})

onMounted(() => {
  if (props.sessionId && props.isRunning) {
    ensureSessionAndConnect()
  }
})

onUnmounted(() => {
  disconnectVNC()
})
</script>

<style scoped>
/* Allow noVNC to size canvas naturally to avoid cursor offset while preserving interaction */
:deep(canvas) {
  max-width: 100%;
  max-height: 100%;
  pointer-events: auto !important;
  cursor: default !important;
  user-select: none !important;
}
</style>
