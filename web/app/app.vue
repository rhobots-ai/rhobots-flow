<template>
  <NuxtLoadingIndicator/>
  <NuxtLayout>
    <NuxtPage/>
  </NuxtLayout>
</template>

<script setup lang="ts">
import {useUserStore} from "./stores/user";
import {useAuthClient} from "./composables/useAuthClient";

const isLoading = ref<boolean>(true)

const forceLogOut = async (signOutFromAuth: boolean) => {
  if (signOutFromAuth) {
    const {signOut} = useAuthClient()
    await signOut()
  }

  const userStore = useUserStore()
  userStore.clearProfile()
}

const updateSession = async () => {
  try {
    const {getSession, setJwtToken} = useAuthClient()

    await setJwtToken()

    // Get session data
    const session = await getSession({fetchOptions: {credentials: 'include'}})

    if (session.data) {
      const userStore = useUserStore()
      userStore.setProfile({
        ...session.data.user,
      })
    }
  } catch (e: any) {
    await forceLogOut(e.status !== 401)
  }
}

onMounted(async () => {
  await updateSession()
  isLoading.value = false
});

useHead({
  title: 'App Template',
  meta: [
    {
      name: 'description',
      content: 'App Template'
    }
  ]
})

useSeoMeta({
  title: 'App Template',
  description: 'App Template',
  ogTitle: 'App Template',
  ogDescription: 'App Template',
  ogImage: 'https://rhobots.ai/images/og-image.png',
  ogUrl: 'https://rhobots.ai',
  ogType: 'website',
  twitterCard: 'summary_large_image',
  twitterTitle: 'App Template',
  twitterDescription: 'App Template',
  twitterImage: 'https://rhobots.ai/images/og-image.png',
  robots: 'index, follow',
});
</script>