<template>
  <div class="automation-workspace min-h-screen bg-zinc-50 dark:bg-zinc-950">
    <!-- Tab Navigation -->
    <div class="bg-white dark:bg-zinc-900 border-b border-zinc-200 dark:border-zinc-800 shadow-sm">
      <div class="px-6 py-4">
        <div class="flex items-center justify-between">
          <div class="flex space-x-1">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              :class="[
                'flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200',
                activeTab === tab.id
                  ? 'bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-700'
                  : 'text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-zinc-800'
              ]"
              @click="setActiveTab(tab.id)"
            >
              <component :is="tab.icon" class="w-4 h-4" />
              {{ tab.label }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Tab Content -->
    <div class="tab-content p-6">
      <!-- Dashboard Tab -->
      <div v-if="activeTab === 'dashboard'" class="h-full">
        <Suspense>
          <HomeDashboard />
          <template #fallback>
            <div class="flex items-center justify-center h-full">
              <div class="text-center">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-2" />
                <p class="text-zinc-600 dark:text-zinc-400">Loading Dashboard...</p>
              </div>
            </div>
          </template>
        </Suspense>
      </div>

      <!-- Workspace Tab -->
      <div v-else-if="activeTab === 'workspace'" class="h-full">
        <Suspense>
          <MainDashboard />
          <template #fallback>
            <div class="flex items-center justify-center h-full">
              <div class="text-center">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-2" />
                <p class="text-zinc-600 dark:text-zinc-400">Loading Workspace...</p>
              </div>
            </div>
          </template>
        </Suspense>
      </div>

      <!-- TigerVNC Test Tab -->
      <div v-else-if="activeTab === 'tigervnc'" class="h-full">
        <Suspense>
          <TestTigerVNC />
          <template #fallback>
            <div class="flex items-center justify-center h-full">
              <div class="text-center">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-2" />
                <p class="text-zinc-600 dark:text-zinc-400">Loading TigerVNC Test...</p>
              </div>
            </div>
          </template>
        </Suspense>
      </div>

      <!-- Multi-Session Test Tab -->
      <div v-else-if="activeTab === 'multisession'" class="h-full">
        <Suspense>
          <MultiSessionTest />
          <template #fallback>
            <div class="flex items-center justify-center h-full">
              <div class="text-center">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-2" />
                <p class="text-zinc-600 dark:text-zinc-400">Loading Multi-Session Test...</p>
              </div>
            </div>
          </template>
        </Suspense>
      </div>

      <!-- Task Builder Tab -->
      <div v-else-if="activeTab === 'builder'" class="h-full">
        <Suspense>
          <TaskBuilder />
          <template #fallback>
            <div class="flex items-center justify-center h-full">
              <div class="text-center">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-2" />
                <p class="text-zinc-600 dark:text-zinc-400">Loading Task Builder...</p>
              </div>
            </div>
          </template>
        </Suspense>
      </div>

      <!-- Task Runner Tab -->
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
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-2" />
                <p class="text-zinc-600 dark:text-zinc-400">Loading Task Runner...</p>
              </div>
            </div>
          </template>
        </Suspense>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { 
  Monitor, 
  TestTube, 
  Users, 
  Wrench, 
  PlayCircle
} from 'lucide-vue-next'

// Import components dynamically to avoid circular dependencies
const HomeDashboard = defineAsyncComponent(() => import('~/components/automation/HomeDashboard.vue'))
const MainDashboard = defineAsyncComponent(() => import('~/components/automation/MainDashboard.vue'))
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
    id: 'workspace',
    label: 'Workspace',
    icon: Monitor,
    description: 'Full automation workspace with task list, CSV upload, and live automation view'
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
    description: 'Execute automation tasks'
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
</script>

<style scoped>
.automation-workspace {
  height: calc(100vh - 3rem);
}

.tab-content {
  height: calc(100% - 4rem);
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
