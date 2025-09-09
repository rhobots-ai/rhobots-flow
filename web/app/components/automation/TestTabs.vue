<template>
  <div class="automation-workspace">
    <div class="flex border-b mb-4">
      <button
        v-for="subTest in testTabs"
        :key="subTest.id"
        :class="[
          'px-4 py-2',
          activeTestTab === subTest.id ? 'border-b-2 border-blue-500 text-blue-500' : 'text-gray-500'
        ]"
        @click="activeTestTab = subTest.id"
      >
        {{ subTest.label }}
      </button>
    </div>

    <!-- TigerVNC Test Tab -->
    <div v-if="activeTestTab === 'tigervnc'" class="h-full">
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
    <div v-else-if="activeTestTab === 'multisession'" class="h-full">
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
    <div v-else-if="activeTestTab === 'builder'" class="h-full">
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
    <div v-else-if="activeTestTab === 'runner'" class="h-full">
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
</template>

<script setup>
import { ref, onMounted, defineAsyncComponent } from 'vue'

const TestTigerVNC = defineAsyncComponent(() => import('@auto/components/TestTigerVNC.vue'))
const MultiSessionTest = defineAsyncComponent(() => import('@auto/components/MultiSessionTest.vue'))
const TaskBuilder = defineAsyncComponent(() => import('@auto/components/TaskBuilder.vue'))
const AutomationRunner = defineAsyncComponent(() => import('@auto/components/AutomationRunner.vue'))
const TaskSelector = defineAsyncComponent(() => import('~/components/automation/TaskSelector.vue'))

const testTabs = ref([
  { id: 'tigervnc', label: 'TigerVNC Test' },
  { id: 'multisession', label: 'Multi-Session' },
  { id: 'builder', label: 'Task Builder' },
  { id: 'runner', label: 'Task Runner' }
])

const activeTestTab = ref('tigervnc')
const currentTaskId = ref(null)

const handleTaskSelected = (taskId) => {
  currentTaskId.value = taskId
}

const handleTaskCompleted = () => {
  currentTaskId.value = 'select'
}

onMounted(() => {
  const route = useRoute()
  if (route.query.taskId) {
    currentTaskId.value = route.query.taskId
    activeTestTab.value = 'runner'
  }
})
</script>

<style scoped>
.automation-workspace {
  height: calc(100vh - 6rem);
}
</style>
