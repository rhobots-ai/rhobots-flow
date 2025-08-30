<template>
  <div 
    class="rounded-full flex items-center justify-center transition-colors"
    :class="[iconContainerClasses, sizeClasses]"
  >
    <component :is="statusIcon" :class="iconSizeClasses" />
  </div>
</template>

<script setup lang="ts">
import { 
  Clock, Play, CheckCircle2, XCircle, Square
} from 'lucide-vue-next'
import type { RunStatus } from '~/types/automation'

interface Props {
  status: RunStatus
  size?: 'xs' | 'sm' | 'md' | 'lg'
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md'
})

const sizeClasses = computed(() => {
  switch (props.size) {
    case 'xs':
      return 'w-4 h-4'
    case 'sm':
      return 'w-6 h-6'
    case 'md':
      return 'w-8 h-8'
    case 'lg':
      return 'w-10 h-10'
    default:
      return 'w-8 h-8'
  }
})

const iconSizeClasses = computed(() => {
  switch (props.size) {
    case 'xs':
      return 'h-2 w-2'
    case 'sm':
      return 'h-3 w-3'
    case 'md':
      return 'h-4 w-4'
    case 'lg':
      return 'h-5 w-5'
    default:
      return 'h-4 w-4'
  }
})

const statusConfig = computed(() => {
  switch (props.status) {
    case 'pending':
      return {
        icon: Clock,
        containerClasses: 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400'
      }
    case 'running':
      return {
        icon: Play,
        containerClasses: 'bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400'
      }
    case 'completed':
      return {
        icon: CheckCircle2,
        containerClasses: 'bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400'
      }
    case 'failed':
      return {
        icon: XCircle,
        containerClasses: 'bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400'
      }
    case 'cancelled':
      return {
        icon: Square,
        containerClasses: 'bg-amber-100 text-amber-600 dark:bg-amber-900/30 dark:text-amber-400'
      }
    default:
      return {
        icon: Clock,
        containerClasses: 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400'
      }
  }
})

const statusIcon = computed(() => statusConfig.value.icon)
const iconContainerClasses = computed(() => statusConfig.value.containerClasses)
</script>

<style scoped>
/* Add subtle animation for running status */
.bg-blue-100 .h-2,
.bg-blue-100 .h-3,
.bg-blue-100 .h-4,
.bg-blue-100 .h-5 {
  animation: spin 2s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Dark mode adjustments */
@media (prefers-color-scheme: dark) {
  .dark .bg-blue-900\/30 .h-2,
  .dark .bg-blue-900\/30 .h-3,
  .dark .bg-blue-900\/30 .h-4,
  .dark .bg-blue-900\/30 .h-5 {
    animation: spin 2s linear infinite;
  }
}
</style>
