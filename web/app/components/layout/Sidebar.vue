<template>
  <div
    class="fixed top-0 left-0 h-full w-64 bg-white dark:bg-gray-800 transform transition-transform duration-500 ease-in-out z-20"
    :class="isSidebarOpen ? 'translate-x-0' : '-translate-x-full'">
    <div class="flex flex-col h-full overflow-hidden">
      <div class="flex items-center justify-between border-b border-gray-100 dark:border-gray-700">
        <NuxtLink to="/" class="flex items-center">
          <div class="p-3">
            <img :src="isDark ? '/images/icon-dark.svg' : '/images/icon-light.svg'" alt="Logo" class="h-6" />
          </div>
        </NuxtLink>
        <button class="p-2 mr-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          @click="$emit('update:isSidebarOpen', false)">
          <PanelLeftClose class="h-5 w-5 text-gray-500 dark:text-gray-400" />
        </button>
      </div>

      <nav class="flex flex-col h-[calc(100%-10rem)] mt-4">
        <div class="px-4">
          <NuxtLink to="/" class="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors"
            :class="$route.path === '/' ? 'bg-primary-50 dark:bg-primary-900/50 text-primary-700 dark:text-primary-400' : 'text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800'"
            @click="handleClose">
            <Home class="h-5 w-5" />
            Home
          </NuxtLink>

          <!-- Sample Link -->
          <NuxtLink to="/ui-reference"
            class="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors mt-1"
            :class="$route.path.startsWith('/sample') ? 'bg-primary-50 dark:bg-primary-900/50 text-primary-700 dark:text-primary-400' : 'text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800'"
            @click="handleClose">
            <Layout class="h-5 w-5" />
            UI Reference
          </NuxtLink>
        </div>
      </nav>

      <div v-if="isLoggedIn" class="p-4 border-t border-gray-100 dark:border-gray-800">
        <LayoutProfileMenu :is-dark="isDark" @update:is-dark="$emit('update:isDark', $event)" @close="handleClose" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useWindowSize } from '@vueuse/core'
import { Layout, PanelLeftClose, Home } from 'lucide-vue-next'
import { storeToRefs } from 'pinia'
import { computed, ref } from 'vue'
import { useUserStore } from '~/stores/user'

const props = defineProps<{
  isSidebarOpen: boolean
  isDark: boolean
  isWhiteLabeled?: boolean
}>()

const userStore = useUserStore()

const { isLoggedIn } = storeToRefs(userStore)

const showMenu = ref(false)
const menuPosition = ref({ x: 0, y: 0 })

const openMenu = (event: MouseEvent) => {
  event.preventDefault()
  menuPosition.value = { x: event.clientX, y: event.clientY }
  showMenu.value = true

  // Add click outside listener
  nextTick(() => {
    document.addEventListener('click', closeMenu)
  })
}

const closeMenu = () => {
  showMenu.value = false
  document.removeEventListener('click', closeMenu)
}

onUnmounted(() => {
  document.removeEventListener('click', closeMenu)
})

const emit = defineEmits<{
  (e: 'update:isSidebarOpen', value: boolean): void
  (e: 'update:isDark', value: boolean): void
}>()

const { width } = useWindowSize()
const isMobile = computed(() => width.value < 1024)

const handleClose = () => {
  if (isMobile.value) {
    emit('update:isSidebarOpen', false)
  }
}

// Format timestamp
const formatTime = (timestamp: string | number) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMins / 60)

  // If a message is from today, show relative time
  if (date.toDateString() === now.toDateString()) {
    if (diffMins < 1) return 'just now'
    if (diffMins === 1) return '1 min ago'
    if (diffMins < 60) return `${diffMins} mins ago`
    if (diffHours === 1) return '1 hour ago'
    return `${diffHours} hours ago`
  }

  // For older messages, show full date and time
  return date.toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>