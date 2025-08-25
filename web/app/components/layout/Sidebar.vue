<template>
  <div
    class="fixed top-0 left-0 h-full w-64 transform transition-transform duration-500 ease-in-out z-20"
    :class="isSidebarOpen ? 'translate-x-0' : '-translate-x-full'">
    
    <!-- Gradient Background -->
    <div class="absolute inset-0 bg-gradient-to-br from-blue-600 via-purple-700 to-indigo-800"></div>
    
    <!-- Dark Overlay for Better Contrast -->
    <div class="absolute inset-0 bg-black/40 dark:bg-black/60"></div>
    
    <!-- Animated Particles -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="particle particle-1"></div>
      <div class="particle particle-2"></div>
      <div class="particle particle-3"></div>
    </div>
    
    <div class="relative flex flex-col h-full overflow-hidden">
      <div class="flex items-center justify-between border-b border-white/20 backdrop-blur-sm">
        <NuxtLink to="/home" class="flex items-center">
          <div class="p-2 m-2 rounded-lg border border-white/20 bg-white/10 backdrop-blur-sm transition-all duration-300">
            <img src="/images/icon-dark.svg" alt="Logo" class="h-6" />
          </div>
        </NuxtLink>
        <button class="p-2 mr-2 rounded-lg cursor-pointer hover:bg-white/10 backdrop-blur-sm transition-all duration-300"
          @click="$emit('update:isSidebarOpen', false)">
          <PanelLeftClose class="h-5 w-5 text-white/80" />
        </button>
      </div>

      <nav class="flex flex-col h-[calc(100%-10rem)] mt-4 overflow-y-auto">
        <div class="px-4 space-y-6">
          <!-- Dynamic Menu Sections -->
          <div v-for="section in visibleSections" :key="section.id" class="space-y-2">
            <!-- Section Label -->
            <div v-if="section.label" class="px-3 py-1 text-xs font-semibold text-white/60 uppercase tracking-wider">
              {{ section.label }}
            </div>
            
            <!-- Menu Items -->
            <div class="space-y-1">
              <template v-for="item in section.items" :key="item.id">
                <!-- Divider -->
                <div v-if="item.divider" class="my-2 border-t border-white/20"></div>
                
                <!-- Regular Menu Item -->
                <NuxtLink 
                  v-else-if="item.path && !item.isExternal"
                  :to="item.path"
                  class="flex items-center gap-2 px-3 py-2 rounded-xl text-sm font-medium transition-all duration-300"
                  :class="isActiveMenuItem(item) ? 'bg-white/20 border-white/30 text-white shadow-lg' : 'text-white/80 hover:text-white'"
                  @click="handleClose">
                  <component v-if="item.icon" :is="item.icon" class="h-5 w-5" />
                  <span>{{ item.label }}</span>
                  <span v-if="item.badge" class="ml-auto px-2 py-0.5 text-xs rounded-full bg-white/20 text-white/90">
                    {{ item.badge }}
                  </span>
                </NuxtLink>
                
                <!-- External Link -->
                <a 
                  v-else-if="item.path && item.isExternal"
                  :href="item.path"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="flex items-center gap-2 px-3 py-2 rounded-xl text-sm font-medium transition-all duration-300 bg-white/10 backdrop-blur-sm border border-white/20 hover:bg-white/20 hover:border-white/30 text-white/80 hover:text-white"
                  @click="handleClose">
                  <component v-if="item.icon" :is="item.icon" class="h-5 w-5" />
                  <span>{{ item.label }}</span>
                  <ExternalLink class="h-4 w-4 ml-auto" />
                </a>
                
                <!-- Clickable Item (no path) -->
                <button 
                  v-else-if="item.onClick"
                  @click="() => { item.onClick?.(); handleClose(); }"
                  class="w-full flex items-center gap-2 px-3 py-2 rounded-xl text-sm font-medium transition-all duration-300 bg-white/10 backdrop-blur-sm border border-white/20 hover:bg-white/20 hover:border-white/30 text-white/80 hover:text-white">
                  <component v-if="item.icon" :is="item.icon" class="h-5 w-5" />
                  <span>{{ item.label }}</span>
                  <span v-if="item.badge" class="ml-auto px-2 py-0.5 text-xs rounded-full bg-white/20 text-white/90">
                    {{ item.badge }}
                  </span>
                </button>
              </template>
            </div>
          </div>
        </div>
      </nav>

      <div v-if="isLoggedIn" class="p-4 border-t border-white/20 backdrop-blur-sm">
        <LayoutProfileMenu :is-dark="isDark" @update:is-dark="$emit('update:isDark', $event)" @close="handleClose" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useWindowSize } from '@vueuse/core'
import { PanelLeftClose, ExternalLink } from 'lucide-vue-next'
import { storeToRefs } from 'pinia'
import { computed, ref } from 'vue'
import { useUserStore } from '~/stores/user'
import { useMenu } from '~/composables/useMenu'

const props = defineProps<{
  isSidebarOpen: boolean
  isDark: boolean
  isWhiteLabeled?: boolean
}>()

const userStore = useUserStore()
const { visibleSections, isActiveMenuItem } = useMenu()

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

<style scoped>
/* Enhanced backdrop blur effects */
.backdrop-blur-sm {
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

/* Animated particles */
.particle {
  position: absolute;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  pointer-events: none;
}

.particle-1 {
  width: 3px;
  height: 3px;
  top: 15%;
  left: 20%;
  animation: float-particle 8s ease-in-out infinite;
}

.particle-2 {
  width: 4px;
  height: 4px;
  top: 50%;
  right: 25%;
  animation: float-particle 10s ease-in-out infinite 2s;
}

.particle-3 {
  width: 2px;
  height: 2px;
  bottom: 30%;
  left: 70%;
  animation: float-particle 12s ease-in-out infinite 1s;
}

@keyframes float-particle {
  0%, 100% {
    transform: translateY(0px) translateX(0px);
    opacity: 0.3;
  }
  25% {
    transform: translateY(-15px) translateX(8px);
    opacity: 0.7;
  }
  50% {
    transform: translateY(-30px) translateX(-4px);
    opacity: 0.4;
  }
  75% {
    transform: translateY(-15px) translateX(-8px);
    opacity: 0.8;
  }
}

/* Glassmorphism hover effects */
.bg-white\/10:hover {
  background-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-1px);
}

/* Text shadow for better readability */
.text-white, .text-white\/80 {
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

/* Smooth transitions */
* {
  transition: all 0.3s ease;
}

/* Performance optimizations */
.particle {
  will-change: transform, opacity;
}

/* Accessibility improvements */
@media (prefers-reduced-motion: reduce) {
  .particle {
    animation: none;
  }
  
  * {
    transition: none;
  }
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  .bg-white\/10 {
    background-color: rgba(255, 255, 255, 0.9);
    color: #000;
  }
  
  .text-white, .text-white\/80 {
    color: #fff;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
  }
}
</style>