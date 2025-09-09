<template>
  <div class="px-4 py-6 sm:px-0">
    <!-- Hero Section -->
    <div class="text-center mb-12">
      <h1 class="text-4xl font-bold text-zinc-900 dark:text-zinc-100 mb-4">
        Browser Automation Studio
      </h1>
      <p class="text-xl text-zinc-600 dark:text-zinc-400 max-w-3xl mx-auto">
        Create, manage, and execute browser automation tasks with real-time visual feedback through VNC integration.
      </p>
    </div>

    <!-- Feature Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
      <div class="bg-white dark:bg-zinc-900 rounded-lg p-6 border border-zinc-200 dark:border-zinc-800 shadow-sm">
        <div class="text-blue-600 mb-4">
          <Monitor class="w-12 h-12" />
        </div>
        <h3 class="text-xl font-semibold text-zinc-900 dark:text-zinc-100 mb-2">Visual Automation</h3>
        <p class="text-zinc-600 dark:text-zinc-400">
          Watch your automation tasks execute in real-time through our integrated VNC viewer.
        </p>
      </div>

      <div class="bg-white dark:bg-zinc-900 rounded-lg p-6 border border-zinc-200 dark:border-zinc-800 shadow-sm">
        <div class="text-green-600 mb-4">
          <Settings class="w-12 h-12" />
        </div>
        <h3 class="text-xl font-semibold text-zinc-900 dark:text-zinc-100 mb-2">Task Builder</h3>
        <p class="text-zinc-600 dark:text-zinc-400">
          Create complex automation workflows with our intuitive step-by-step builder.
        </p>
      </div>

      <div class="bg-white dark:bg-zinc-900 rounded-lg p-6 border border-zinc-200 dark:border-zinc-800 shadow-sm">
        <div class="text-purple-600 mb-4">
          <FileText class="w-12 h-12" />
        </div>
        <h3 class="text-xl font-semibold text-zinc-900 dark:text-zinc-100 mb-2">File Integration</h3>
        <p class="text-zinc-600 dark:text-zinc-400">
          Upload Excel, CSV, and other files to provide data for your automation tasks.
        </p>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="text-center">
      <h2 class="text-2xl font-bold text-zinc-900 dark:text-zinc-100 mb-6">Quick Actions</h2>
      <div class="flex justify-center space-x-4 mb-4">
        <NuxtLink
          to="/test/builder"
          class="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-semibold transition-colors"
        >
          Create New Task
        </NuxtLink>
        <NuxtLink
          to="/tasks"
          class="bg-zinc-100 dark:bg-zinc-800 hover:bg-zinc-200 dark:hover:bg-zinc-700 text-zinc-900 dark:text-zinc-100 px-8 py-3 rounded-lg font-semibold transition-colors border border-zinc-200 dark:border-zinc-700"
        >
          View All Tasks
        </NuxtLink>
      </div>
      
      <!-- Test Actions -->
      <div class="flex justify-center space-x-4">
        <button
          :disabled="browserTesting"
          class="bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white px-6 py-2 rounded-lg font-semibold transition-colors"
          @click="testBrowser"
        >
          {{ browserTesting ? 'Testing...' : 'Test Browser + VNC' }}
        </button>
        <button
          class="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded-lg font-semibold transition-colors"
          @click="openVNC"
        >
          Open VNC Viewer
        </button>
      </div>

      <!-- Test Results -->
      <div v-if="testResult" class="mt-4 p-4 rounded-lg max-w-md mx-auto" :class="testResult.status === 'success' ? 'bg-green-100 text-green-800 dark:bg-green-950 dark:text-green-300' : 'bg-red-100 text-red-800 dark:bg-rose-950 dark:text-rose-300'">
        <p>{{ testResult.message }}</p>
      </div>
    </div>

    <!-- System Status -->
    <div class="mt-12 bg-white dark:bg-zinc-900 rounded-lg p-6 border border-zinc-200 dark:border-zinc-800 shadow-sm">
      <h3 class="text-lg font-semibold text-zinc-900 dark:text-zinc-100 mb-4">System Status</h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="text-center">
          <div class="text-2xl font-bold" :class="systemStatus.backend ? 'text-green-600' : 'text-red-600'">
            {{ systemStatus.backend ? '✓' : '✗' }}
          </div>
          <div class="text-sm text-zinc-600 dark:text-zinc-400">Backend</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold" :class="systemStatus.database ? 'text-green-600' : 'text-red-600'">
            {{ systemStatus.database ? '✓' : '✗' }}
          </div>
          <div class="text-sm text-zinc-600 dark:text-zinc-400">Database</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold" :class="systemStatus.vnc ? 'text-green-600' : 'text-red-600'">
            {{ systemStatus.vnc ? '✓' : '✗' }}
          </div>
          <div class="text-sm text-zinc-600 dark:text-zinc-400">VNC Server</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-blue-600">{{ systemStatus.timezone || 'Unknown' }}</div>
          <div class="text-sm text-zinc-600 dark:text-zinc-400">Timezone</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Monitor, Settings, FileText } from 'lucide-vue-next'

const systemStatus = ref({
  backend: false,
  database: false,
  vnc: false,
  timezone: 'Unknown'
})

const browserTesting = ref(false)
const testResult = ref(null)

const checkSystemStatus = async () => {
  try {
    const response = await $fetch('/api/health/')
    systemStatus.value = {
      backend: response.backend || true,
      database: response.database || true, 
      vnc: response.vnc || true,
      timezone: response.timezone || 'UTC'
    }
  } catch (error) {
    console.error('Health check failed:', error)
    systemStatus.value = {
      backend: false,
      database: false,
      vnc: false,
      timezone: 'Unknown'
    }
  }
}

const testBrowser = async () => {
  browserTesting.value = true
  testResult.value = null
  try {
    // First, try simple test endpoint
    const healthResponse = await $fetch('/api/test-browser')
    if (healthResponse.status === 'success') {
      // Now create a session and test actual browser
      const sessionManager = useSessionManager()
      const session = await sessionManager.createSession('test-user')
      
      // Give session time to initialize
      await new Promise(resolve => setTimeout(resolve, 3000))
      
      // Test browser in the session
      await sessionManager.testBrowser(session.session_id, 'https://rhobots.ai')
      
      testResult.value = {
        status: 'success',
        message: `Browser test successful! Session ${session.session_id.substring(0, 8)} created and browser launched.`
      }
      
      // Clean up session after a delay
      setTimeout(async () => {
        try {
          await sessionManager.destroySession(session.session_id)
        } catch (e) {
          console.warn('Failed to cleanup test session:', e)
        }
      }, 30000) // 30 seconds
      
    } else {
      testResult.value = healthResponse
    }
  } catch (error) {
    console.error('Browser test failed:', error)
    testResult.value = { 
      status: 'error', 
      message: 'Failed to test browser: ' + (error.data?.detail || error.message)
    }
  } finally {
    browserTesting.value = false
  }
}

const openVNC = () => {
  // Open VNC viewer in new tab
  const vncUrl = `${window.location.protocol}//${window.location.hostname}:7900/vnc.html`
  window.open(vncUrl, '_blank')
}

onMounted(() => {
  checkSystemStatus()
})
</script>

<style scoped>
/* Add any specific styling for the home dashboard */
.transition-colors {
  transition: color 0.2s ease, background-color 0.2s ease;
}

/* Animation for test results */
.bg-green-100, .bg-red-100 {
  animation: fadeIn 0.3s ease-in-out;
}

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
</style>
