<template>
  <div class="automation-workspace min-h-screen bg-zinc-50">
    <!-- Tab Navigation -->
    <div class="bg-white border-b border-zinc-200 shadow-sm">
      <div class="px-6 py-4">
        <div class="flex items-center justify-between">
          <div class="flex space-x-1">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              :class="[
                'flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200',
                activeTab === tab.id
                  ? 'bg-blue-100 text-blue-700 border border-blue-200'
                  : 'text-zinc-600 hover:text-zinc-900 hover:bg-zinc-100'
              ]"
              @click="setActiveTab(tab.id)"
            >
              <component :is="tab.icon" class="w-4 h-4" />
              {{ tab.label }}
              <span v-if="tab.badge" class="ml-1 px-1.5 py-0.5 text-xs bg-blue-200 text-blue-800 rounded-full">
                {{ tab.badge }}
              </span>
            </button>
          </div>
          
          <!-- Quick Actions -->
          <div class="flex items-center gap-2">
            <button
              v-if="activeTab === 'dashboard'"
              @click="refreshDashboard"
              class="p-2 text-zinc-500 hover:text-zinc-700 hover:bg-zinc-100 rounded-lg transition-colors"
              title="Refresh Dashboard"
            >
              <RefreshCw class="w-4 h-4" />
            </button>
            <button
              v-if="activeTab === 'runner' && currentTaskId"
              @click="openRunnerInNewTab"
              class="p-2 text-zinc-500 hover:text-zinc-700 hover:bg-zinc-100 rounded-lg transition-colors"
              title="Open in New Tab"
            >
              <ExternalLink class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Tab Content -->
    <div class="tab-content">
      <div v-if="activeTab === 'dashboard'" class="h-full">
        <Suspense>
          <MainDashboard />
          <template #fallback>
            <div class="flex items-center justify-center h-full">
              <div class="text-center">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-2"></div>
                <p class="text-zinc-600">Loading Dashboard...</p>
              </div>
            </div>
          </template>
        </Suspense>
      </div>
      
      <div v-else-if="activeTab === 'tigervnc'" class="h-full">
        <Suspense>
          <TestTigerVNC />
          <template #fallback>
            <div class="flex items-center justify-center h-full">
              <div class="text-center">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-2"></div>
                <p class="text-zinc-600">Loading TigerVNC Test...</p>
              </div>
            </div>
          </template>
        </Suspense>
      </div>
      
      <div v-else-if="activeTab === 'multisession'" class="h-full">
        <Suspense>
          <MultiSessionTest />
          <template #fallback>
            <div class="flex items-center justify-center h-full">
              <div class="text-center">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-2"></div>
                <p class="text-zinc-600">Loading Multi-Session Test...</p>
              </div>
            </div>
          </template>
        </Suspense>
      </div>
      
      <div v-else-if="activeTab === 'builder'" class="h-full">
        <Suspense>
          <TaskBuilder />
          <template #fallback>
            <div class="flex items-center justify-center h-full">
              <div class="text-center">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-2"></div>
                <p class="text-zinc-600">Loading Task Builder...</p>
              </div>
            </div>
          </template>
        </Suspense>
      </div>
      
      <div v-else-if="activeTab === 'runner'" class="h-full">
        <Suspense>
          <TaskSelector 
            v-if="!currentTaskId || currentTaskId === 'select'"
            @task-selected="handleTaskSelected"
          />
          <AutomationRunner 
            v-else
            :task-id="currentTaskId" 
            @task-completed="handleTaskCompleted"
          />
          <template #fallback>
            <div class="flex items-center justify-center h-full">
              <div class="text-center">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-2"></div>
                <p class="text-zinc-600">Loading Task Runner...</p>
              </div>
            </div>
          </template>
        </Suspense>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { 
  Monitor, 
  TestTube, 
  Users, 
  Wrench, 
  PlayCircle,
  RefreshCw,
  ExternalLink
} from 'lucide-vue-next'

// Import components dynamically to avoid circular dependencies
const MainDashboard = defineAsyncComponent(() => import('@auto/components/MainDashboard.vue'))
const TestTigerVNC = defineAsyncComponent(() => import('@auto/components/TestTigerVNC.vue'))
const MultiSessionTest = defineAsyncComponent(() => import('@auto/components/MultiSessionTest.vue'))
const TaskBuilder = defineAsyncComponent(() => import('@auto/components/TaskBuilder.vue'))
const AutomationRunner = defineAsyncComponent(() => import('@auto/components/AutomationRunner.vue'))
const TaskSelector = defineAsyncComponent(() => import('~/components/automation/TaskSelector.vue'))

// Tab configuration
const tabs = ref([
  {
    id: 'dashboard',
    label: 'Dashboard',
    icon: Monitor,
    description: 'Main automation dashboard'
  },
  {
    id: 'tigervnc',
    label: 'TigerVNC Test',
    icon: TestTube,
    description: 'Test TigerVNC connection'
  },
  {
    id: 'multisession',
    label: 'Multi-Session',
    icon: Users,
    description: 'Multi-session testing'
  },
  {
    id: 'builder',
    label: 'Task Builder',
    icon: Wrench,
    description: 'Create and edit automation tasks'
  },
  {
    id: 'runner',
    label: 'Task Runner',
    icon: PlayCircle,
    description: 'Execute automation tasks',
    badge: 'Live'
  }
])

// Active tab state
const activeTab = ref('dashboard')
const currentTaskId = ref(null)

// Tab management
const setActiveTab = (tabId) => {
  activeTab.value = tabId
  
  // Handle special cases
  if (tabId === 'runner' && !currentTaskId.value) {
    // If no task selected, show task selection
    currentTaskId.value = 'select'
  }
}

// Actions
const refreshDashboard = () => {
  // Trigger dashboard refresh
  console.log('Refreshing dashboard...')
}

const openRunnerInNewTab = () => {
  if (currentTaskId.value && currentTaskId.value !== 'select') {
    window.open(`/test/runner/${currentTaskId.value}`, '_blank')
  }
}

// Task selection handlers
const handleTaskSelected = (taskId) => {
  currentTaskId.value = taskId
}

const handleTaskCompleted = () => {
  // Reset to task selection after completion
  currentTaskId.value = 'select'
}

// Initialize
onMounted(() => {
  // Check if we have a task ID from URL params
  const route = useRoute()
  if (route.query.taskId) {
    currentTaskId.value = route.query.taskId
    activeTab.value = 'runner'
  }
})

// Expose methods for parent components
defineExpose({
  setActiveTab,
  currentTaskId
})
</script>

<style scoped>
.automation-workspace {
  height: calc(100vh - 3rem); /* Account for app bar */
}

.tab-content {
  height: calc(100% - 4rem); /* Account for tab navigation */
  overflow: auto;
}

/* Smooth transitions */
.tab-content > div {
  animation: fadeIn 0.2s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Active tab indicator */
button[class*="bg-blue-100"] {
  position: relative;
}

button[class*="bg-blue-100"]::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 2px;
  background: #3b82f6;
  border-radius: 1px;
}
</style>
