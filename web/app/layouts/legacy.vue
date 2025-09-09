<template>
  <div class="min-h-screen bg-zinc-100">
    <!-- Legacy Header -->
    <header class="bg-white border-b border-zinc-200 shadow-sm">
      <div class="px-6 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <NuxtLink to="/automation" class="flex items-center gap-2 text-blue-600 hover:text-blue-700">
              <ArrowLeft class="w-4 h-4" />
              <span class="text-sm font-medium">Back to Dashboard</span>
            </NuxtLink>
            <div class="w-px h-6 bg-zinc-200" />
            <h1 class="text-xl font-semibold text-zinc-900">
              {{ pageTitle }}
            </h1>
          </div>
          
          <!-- Legacy Navigation -->
          <nav class="flex items-center gap-1">
            <NuxtLink
              to="/test"
              class="px-3 py-2 text-sm font-medium rounded-lg transition-colors"
              :class="$route.path === '/test' ? 'bg-blue-100 text-blue-700' : 'text-zinc-600 hover:text-zinc-900 hover:bg-zinc-100'"
            >
              TigerVNC Test
            </NuxtLink>
            <NuxtLink
              to="/test/multisessiontest"
              class="px-3 py-2 text-sm font-medium rounded-lg transition-colors"
              :class="$route.path === '/test/multisessiontest' ? 'bg-blue-100 text-blue-700' : 'text-zinc-600 hover:text-zinc-900 hover:bg-zinc-100'"
            >
              Multi-Session
            </NuxtLink>
            <NuxtLink
              to="/tasks"
              class="px-3 py-2 text-sm font-medium rounded-lg transition-colors"
              :class="$route.path === '/tasks' ? 'bg-blue-100 text-blue-700' : 'text-zinc-600 hover:text-zinc-900 hover:bg-zinc-100'"
            >
              Tasks
            </NuxtLink>
            <NuxtLink
              to="/test/builder"
              class="px-3 py-2 text-sm font-medium rounded-lg transition-colors"
              :class="$route.path === '/test/builder' ? 'bg-blue-100 text-blue-700' : 'text-zinc-600 hover:text-zinc-900 hover:bg-zinc-100'"
            >
              Builder
            </NuxtLink>
          </nav>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1">
      <slot />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { ArrowLeft } from 'lucide-vue-next'

const route = useRoute()

// Compute page title based on route
const pageTitle = computed(() => {
  const titles = {
    '/test': 'TigerVNC Test Harness',
    '/test/multisessiontest': 'Multi-Session Test',
    '/test/builder': 'Task Builder',
    '/tasks': 'Task Management'
  }
  
  // Handle dynamic routes like /test/runner/[id]
  if (route.path.startsWith('/test/runner/')) {
    return 'Task Runner'
  }
  
  return titles[route.path] || 'Test Environment'
})
</script>

<style scoped>
/* Legacy layout specific styles */
.min-h-screen {
  min-height: 100vh;
}

/* Ensure proper spacing and typography matches auto-flow */
main {
  background-color: #f9fafb; /* zinc-50 */
}

/* Active navigation item indicator */
.bg-blue-100 {
  position: relative;
}

.bg-blue-100::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  right: 0;
  height: 2px;
  background-color: #3b82f6;
  border-radius: 1px;
}
</style>
