<template>
  <div>
    <!-- Render the MainDashboard with integrated tabs -->
    <AutomationTabsSimple />
  </div>
</template>

<script setup>
// Import the simpler tabbed automation component to avoid timeout issues
import AutomationTabsSimple from '~/components/automation/AutomationTabsSimple.vue'

// Page metadata
definePageMeta({
  title: 'Automation Dashboard',
  layout: 'default'
})
</script>
