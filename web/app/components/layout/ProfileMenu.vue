<template>
  <div class="relative">
    <ClientOnly>
      <button
          ref="menuRef"
          class="w-full flex items-center gap-2 px-4 py-3 rounded-lg text-sm font-medium bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
          @click="isOpen = !isOpen"
      >
        <div class="relative h-8 w-8 rounded-full overflow-hidden bg-primary-100 dark:bg-primary-900 flex items-center justify-center ring-2 ring-white dark:ring-gray-900">
          <img
              v-if="profile?.imageUrl"
              :src="profile.imageUrl"
              :alt="fullName"
              class="h-full w-full object-cover rounded-full"
          />
          <User v-else class="h-4 w-4 text-primary-600 dark:text-primary-400"/>
        </div>
        
        <div class="flex-1 text-left">
          <div>{{ fullName }}</div>
          <div class="inline-flex items-center">
            <span v-if="isPro" class="px-2 py-0.5 rounded-full text-xs font-medium bg-primary-50 dark:bg-primary-900/50 text-primary-700 dark:text-primary-400 inline-flex items-center gap-1">
              <Sparkles class="h-3 w-3" />
              Pro
            </span>
            <span v-else class="px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 inline-flex items-center gap-1">
              Free
            </span>
          </div>
        </div>

        <ChevronUp
            class="h-4 w-4 text-gray-500 dark:text-gray-400 transition-transform"
            :class="{ 'rotate-180': !isOpen }"
        />
      </button>
    </ClientOnly>

    <!-- Dropdown Menu -->
    <div
        v-show="isOpen"
        class="absolute bottom-full left-0 right-0 mb-2 bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 shadow-lg overflow-hidden"
    >
      <div class="py-1 space-y-1">
        <!-- Account Section -->
        <div>
          <NuxtLink
              to="/account"
              class="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
              @click="handleClose"
          >
            <Settings class="h-4 w-4"/>
            Account
          </NuxtLink>
        </div>

        <!-- Settings Section -->
        <div class="border-t border-gray-200 dark:border-gray-700 pt-1">
          <LayoutThemeToggle :is-dark="isDark" @update:is-dark="$emit('update:isDark', $event)" />
          <button
              class="w-full flex items-center gap-2 px-4 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-gray-50 dark:hover:bg-gray-800"
              @click="handleLogout"
          >
            <LogOut class="h-4 w-4"/>
            Logout
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import { onClickOutside } from '@vueuse/core'
  import { User, ChevronUp, Settings, LogOut, Sparkles, Users, Settings2, Info, BookOpen } from 'lucide-vue-next'
  import { storeToRefs } from 'pinia'

  const props = defineProps<{
    isDark: boolean
    isLoggedIn?: boolean
  }>()

  const emit = defineEmits<{
    (e: 'close'): void
    (e: 'update:isDark', value: boolean): void
  }>()

  const isOpen = ref(false)
  const menuRef = ref<HTMLElement | null>(null)

  const { signOut } = useAuthClient()
  const userStore = useUserStore()
  const { profile, fullName } = storeToRefs(userStore)

  const isPro = computed(() => true)

  onClickOutside(menuRef, () => {
    if (isOpen.value) {
      handleClose()
    }
  })

  const handleClose = () => {
    isOpen.value = false
    emit('close')
  }

  const handleLogout = async () => {
    await signOut()
    userStore.clearProfile()
    handleClose()
    window.location.href = '/'
  }
</script>