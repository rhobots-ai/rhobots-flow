<template>
  <span 
    class="inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium transition-colors"
    :class="badgeClasses"
  >
    <component :is="statusIcon" :class="iconSize" />
    {{ statusText }}
  </span>
</template>

<script setup lang="ts">
import { 
  Clock, Play, CheckCircle2, XCircle, Square
} from 'lucide-vue-next'
import type { RunStatus } from '~/types/automation'

interface Props {
  status: RunStatus
  size?: 'sm' | 'md'
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md'
})

const iconSize = computed(() => {
  return props.size === 'sm' ? 'h-3 w-3' : 'h-4 w-4'
})

const statusConfig = computed(() => {
  switch (props.status) {
    case 'pending':
      return {
        icon: Clock,
        text: 'Pending',
        classes: 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300'
      }
    case 'running':
      return {
        icon: Play,
        text: 'Running',
        classes: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300'
      }
    case 'completed':
      return {
        icon: CheckCircle2,
        text: 'Completed',
        classes: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300'
      }
    case 'failed':
      return {
        icon: XCircle,
        text: 'Failed',
        classes: 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300'
      }
    case 'cancelled':
      return {
        icon: Square,
        text: 'Cancelled',
        classes: 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300'
      }
    default:
      return {
        icon: Clock,
        text: 'Unknown',
        classes: 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300'
      }
  }
})

const statusIcon = computed(() => statusConfig.value.icon)
const statusText = computed(() => statusConfig.value.text)
const badgeClasses = computed(() => statusConfig.value.classes)
</script>

<style scoped>
/* Add subtle animation for running status */
.bg-blue-100 .h-3,
.bg-blue-100 .h-4 {
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
  .dark .bg-blue-900\/30 .h-3,
  .dark .bg-blue-900\/30 .h-4 {
    animation: spin 2s linear infinite;
  }
}
</style>
