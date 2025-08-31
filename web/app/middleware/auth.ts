export default defineNuxtRouteMiddleware((to, from) => {
  // Temporarily disable all auth checks for testing
  return
  
  const userStore = useUserStore()
  
  // If user is not logged in, redirect to login page
  if (!userStore.isLoggedIn) {
    return navigateTo('/login')
  }
})
