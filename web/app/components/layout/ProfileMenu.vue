<template>
  <div class="relative">
    <ClientOnly>
      <button
          ref="menuRef"
          class="w-full flex items-center gap-2 px-4 py-3 rounded-xl text-sm font-medium bg-white/10 backdrop-blur-sm border border-white/20 text-white/90 hover:bg-white/20 hover:border-white/30 transition-all duration-300 shadow-lg"
          @click="isOpen = !isOpen"
      >
        <div class="relative h-8 w-8 rounded-full overflow-hidden bg-white/20 backdrop-blur-sm flex items-center justify-center ring-2 ring-white/30">
          <img
              v-if="profile?.imageUrl"
              :src="profile.imageUrl"
              :alt="fullName"
              class="h-full w-full object-cover rounded-full"
          />
          <User v-else class="h-4 w-4 text-white"/>
        </div>
        
        <div class="flex-1 text-left">
          <div class="text-white font-medium">{{ fullName }}</div>
          <div class="inline-flex items-center">
            <span v-if="isPro" class="px-2 py-0.5 rounded-full text-xs font-medium bg-white/20 backdrop-blur-sm border border-white/30 text-white inline-flex items-center gap-1">
              <Sparkles class="h-3 w-3" />
              Pro
            </span>
            <span v-else class="px-2 py-0.5 rounded-full text-xs font-medium bg-white/10 backdrop-blur-sm border border-white/20 text-white/80 inline-flex items-center gap-1">
              Free
            </span>
          </div>
        </div>

        <ChevronUp
            class="h-4 w-4 text-white/80 transition-transform"
            :class="{ 'rotate-180': !isOpen }"
        />
      </button>
    </ClientOnly>

    <!-- Dropdown Menu -->
    <div
        v-show="isOpen"
        class="absolute bottom-full left-0 right-0 mb-2 bg-white/10 backdrop-blur-2xl border border-white/20 rounded-xl shadow-2xl overflow-hidden"
    >
      <div class="py-1 space-y-1">
        <!-- Account Section -->
        <div>
          <NuxtLink
              to="/account"
              class="flex items-center gap-2 px-4 py-2 text-sm text-white/90 hover:bg-white/10 hover:text-white transition-all duration-300"
              @click="handleClose"
          >
            <Settings class="h-4 w-4"/>
            Account
          </NuxtLink>
        </div>

        <!-- Settings Section -->
        <div class="border-t border-white/20 pt-1">
          <LayoutThemeToggle :is-dark="isDark" @update:is-dark="$emit('update:isDark', $event)" />
          <button
              class="w-full flex items-center gap-2 px-4 py-2 text-sm text-red-300 hover:bg-white/10 hover:text-red-200 transition-all duration-300"
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