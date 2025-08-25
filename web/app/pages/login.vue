<template>
  <div class="min-h-screen relative overflow-hidden flex items-center justify-center">
    <!-- Video Background -->
    <video
        ref="videoRef"
        class="absolute inset-0 w-full h-full object-cover"
        autoplay
        muted
        loop
        playsinline
        :class="{ 'opacity-0': !videoLoaded }"
        @loadeddata="onVideoLoaded"
        @error="onVideoError"
    >
      <source src="https://videos.pexels.com/video-files/8084496/8084496-uhd_2560_1440_25fps.mp4" type="video/mp4">
      Your browser does not support the video tag.
    </video>

    <!-- Fallback Background -->
    <div 
        class="absolute inset-0 bg-gradient-to-br from-blue-600 via-purple-700 to-indigo-800"
        :class="{ 'opacity-0': videoLoaded, 'opacity-100': !videoLoaded }"
    ></div>

    <!-- Dark Overlay for Better Contrast -->
    <div class="absolute inset-0 bg-black/40 dark:bg-black/60"></div>

    <!-- Animated Particles -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="particle particle-1"></div>
      <div class="particle particle-2"></div>
      <div class="particle particle-3"></div>
      <div class="particle particle-4"></div>
      <div class="particle particle-5"></div>
    </div>

    <!-- Theme Toggle -->
    <button
        @click="toggleTheme"
        class="absolute top-6 right-6 z-30 p-3 rounded-full bg-white/10 backdrop-blur-md border border-white/20 text-white hover:bg-white/20 transition-all duration-300 shadow-lg hover:shadow-xl"
        :title="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
    >
      <Sun v-if="isDark" class="h-5 w-5"/>
      <Moon v-else class="h-5 w-5"/>
    </button>

    <!-- Main Content -->
    <div class="relative z-20 w-full max-w-lg mx-auto px-6 py-6">
      <!-- Logo/Brand Section -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-20 h-20 bg-white/10 backdrop-blur-md rounded-3xl mb-6 border border-white/20 shadow-2xl">
          <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
          </svg>
        </div>
        <h1 class="text-5xl font-bold text-white mb-3 tracking-tight">
          Welcome Back
        </h1>
        <p class="text-xl text-white/90 font-light">
          Sign in to continue your journey
        </p>
      </div>

      <!-- Login Card -->
      <div class="bg-white/10 backdrop-blur-2xl border border-white/20 rounded-3xl shadow-2xl p-8 transition-all duration-300 hover:bg-white/15">
        <AuthLogin />
      </div>

      <!-- Bottom Links -->
      <div class="text-center mt-8">
        <p class="text-white/70 text-sm">
          Don't have an account? 
          <a href="#" class="text-white font-medium hover:text-white/80 transition-colors underline underline-offset-2">
            Sign up here
          </a>
        </p>
      </div>
    </div>

    <!-- Video Controls (Optional) -->
    <button
        @click="toggleVideo"
        class="absolute bottom-6 right-6 z-30 p-2 rounded-full bg-white/10 backdrop-blur-md border border-white/20 text-white hover:bg-white/20 transition-all duration-300"
        title="Toggle video playback"
    >
      <Pause v-if="isVideoPlaying" class="h-4 w-4"/>
      <Play v-else class="h-4 w-4"/>
    </button>
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia"
import { Sun, Moon, Play, Pause } from 'lucide-vue-next'

const userStore = useUserStore()
const { isLoggedIn } = storeToRefs(userStore)

const isDark = ref(false)
const videoRef = ref<HTMLVideoElement>()
const videoLoaded = ref(false)
const isVideoPlaying = ref(true)

// Page meta
definePageMeta({
  layout: false // Use no layout for login page
})

// Video functions
const onVideoLoaded = () => {
  videoLoaded.value = true
}

const onVideoError = () => {
  videoLoaded.value = false
  console.warn('Video failed to load, using fallback background')
}

const toggleVideo = () => {
  if (videoRef.value) {
    if (isVideoPlaying.value) {
      videoRef.value.pause()
    } else {
      videoRef.value.play()
    }
    isVideoPlaying.value = !isVideoPlaying.value
  }
}

// Theme toggle function
const toggleTheme = () => {
  isDark.value = !isDark.value
  if (isDark.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}

// Initialize theme since we're not using a layout
onMounted(() => {
  // Check for saved theme preference or system preference
  const savedTheme = localStorage.getItem('theme')
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches

  isDark.value = savedTheme === 'dark' || (!savedTheme && prefersDark)
  if (isDark.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }

  // Initialize color palette
  const { setColorPalette } = useTheme()
  const savedPalette = localStorage.getItem('colorPalette')
  if (savedPalette) {
    setColorPalette(savedPalette)
  }

  // Redirect if already logged in
  if (isLoggedIn.value) {
    navigateTo('/home')
  }
  
  // Watch for login state changes
  watch(() => isLoggedIn.value, (newIsLoggedIn) => {
    if (newIsLoggedIn) {
      navigateTo('/home')
    }
  })
})
</script>

<style scoped>
/* Enhanced backdrop blur effects */
.backdrop-blur-md {
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.backdrop-blur-2xl {
  backdrop-filter: blur(40px);
  -webkit-backdrop-filter: blur(40px);
}

/* Video background styling */
video {
  transition: opacity 0.5s ease-in-out;
}

/* Animated particles */
.particle {
  position: absolute;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  pointer-events: none;
}

.particle-1 {
  width: 4px;
  height: 4px;
  top: 20%;
  left: 10%;
  animation: float-particle 8s ease-in-out infinite;
}

.particle-2 {
  width: 6px;
  height: 6px;
  top: 60%;
  left: 80%;
  animation: float-particle 10s ease-in-out infinite 2s;
}

.particle-3 {
  width: 3px;
  height: 3px;
  top: 30%;
  right: 20%;
  animation: float-particle 12s ease-in-out infinite 1s;
}

.particle-4 {
  width: 5px;
  height: 5px;
  bottom: 40%;
  left: 70%;
  animation: float-particle 9s ease-in-out infinite 3s;
}

.particle-5 {
  width: 4px;
  height: 4px;
  bottom: 20%;
  right: 10%;
  animation: float-particle 11s ease-in-out infinite 0.5s;
}

@keyframes float-particle {
  0%, 100% {
    transform: translateY(0px) translateX(0px);
    opacity: 0.3;
  }
  25% {
    transform: translateY(-20px) translateX(10px);
    opacity: 0.8;
  }
  50% {
    transform: translateY(-40px) translateX(-5px);
    opacity: 0.5;
  }
  75% {
    transform: translateY(-20px) translateX(-10px);
    opacity: 0.9;
  }
}

/* Login card hover effect */
.bg-white\/10:hover {
  background-color: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
}

/* Button hover effects */
button:hover {
  transform: translateY(-1px);
}

/* Text glow effect for better readability */
.text-white {
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

/* Smooth transitions */
* {
  transition: all 0.3s ease;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .text-5xl {
    font-size: 2.5rem;
    line-height: 1.2;
  }
  
  .text-xl {
    font-size: 1.125rem;
  }
  
  .w-20.h-20 {
    width: 4rem;
    height: 4rem;
  }
  
  .w-10.h-10 {
    width: 2rem;
    height: 2rem;
  }
  
  .p-8 {
    padding: 1.5rem;
  }
  
  .max-w-lg {
    max-width: 20rem;
  }
}

@media (max-width: 480px) {
  .text-5xl {
    font-size: 2rem;
  }
  
  .p-8 {
    padding: 1rem;
  }
  
  .px-6 {
    padding-left: 1rem;
    padding-right: 1rem;
  }
}

/* Performance optimizations */
.particle {
  will-change: transform, opacity;
}

video {
  will-change: opacity;
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
  
  .text-white {
    color: #fff;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
  }
}
</style>
