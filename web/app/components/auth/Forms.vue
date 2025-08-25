<template>
  <div class="w-full">
    <!-- Tabs -->
    <div class="flex border-b border-white/20 mb-8">
      <button
          class="flex-1 px-4 py-3 text-sm font-medium transition-all duration-300 relative text-center"
          :class="activeTab === 'signin' ? 'text-white' : 'text-white/60 hover:text-white/80'"
          @click="activeTab = 'signin'"
      >
        Sign In
        <div
            class="absolute bottom-0 left-0 right-0 h-0.5 bg-white transform origin-left transition-transform duration-300"
            :class="activeTab === 'signin' ? 'scale-x-100' : 'scale-x-0'"
        />
      </button>
      <button
          class="flex-1 px-4 py-3 text-sm font-medium transition-all duration-300 relative text-center"
          :class="activeTab === 'signup' ? 'text-white' : 'text-white/60 hover:text-white/80'"
          @click="activeTab = 'signup'"
      >
        Sign Up
        <div
            class="absolute bottom-0 left-0 right-0 h-0.5 bg-white transform origin-left transition-transform duration-300"
            :class="activeTab === 'signup' ? 'scale-x-100' : 'scale-x-0'"
        />
      </button>
    </div>

    <!-- Sign In Form -->
    <form v-if="activeTab === 'signin'" @submit.prevent="handleSignIn" class="space-y-6">
      <!-- Email -->
      <div>
        <label for="signin-email" class="block text-sm font-medium text-white/90 mb-2">
          Email Address
        </label>
        <input
            id="signin-email"
            autocomplete="email"
            v-model="signInForm.email"
            type="email"
            required
            class="w-full px-4 py-3 rounded-xl bg-white/10 backdrop-blur-sm border border-white/20 text-white placeholder-white/60 focus:bg-white/15 focus:border-white/40 focus:ring-0 focus:outline-none transition-all duration-300"
            :class="{ 'border-red-400 bg-red-500/10': formErrors.email }"
            placeholder="Enter your email"
        />
        <p v-if="formErrors.email" class="mt-2 text-xs text-red-300">{{ formErrors.email }}</p>
      </div>

      <!-- Password -->
      <div>
        <div class="flex items-center justify-between mb-2">
          <label for="signin-password" class="block text-sm font-medium text-white/90">
            Password
          </label>
          <button
              type="button"
              class="text-xs text-white/70 hover:text-white transition-colors underline underline-offset-2"
              @click="showForgotPassword = true"
          >
            Forgot password?
          </button>
        </div>
        <div class="relative">
          <input
              id="signin-password"
              autocomplete="current-password"
              v-model="signInForm.password"
              :type="showPassword ? 'text' : 'password'"
              required
              class="w-full px-4 py-3 rounded-xl bg-white/10 backdrop-blur-sm border border-white/20 text-white placeholder-white/60 focus:bg-white/15 focus:border-white/40 focus:ring-0 focus:outline-none transition-all duration-300 pr-12"
              :class="{ 'border-red-400 bg-red-500/10': formErrors.password }"
              placeholder="Enter your password"
          />
          <button
              type="button"
              class="absolute inset-y-0 right-0 pr-4 flex items-center text-white/60 hover:text-white transition-colors"
              @click="showPassword = !showPassword"
          >
            <Eye v-if="showPassword" class="h-5 w-5"/>
            <EyeOff v-else class="h-5 w-5"/>
          </button>
        </div>
        <p v-if="formErrors.password" class="mt-2 text-xs text-red-300">{{ formErrors.password }}</p>
      </div>

      <!-- Remember Me -->
      <div class="flex items-center">
        <input
            id="remember-me"
            v-model="signInForm.rememberMe"
            type="checkbox"
            class="h-4 w-4 rounded border-white/20 bg-white/10 text-white focus:ring-white/20 focus:ring-offset-0"
        />
        <label for="remember-me" class="ml-3 block text-sm text-white/80">
          Remember me for 30 days
        </label>
      </div>

      <!-- Error Message -->
      <div v-if="authError" class="p-4 rounded-xl bg-red-500/10 backdrop-blur-sm border border-red-400/20 text-red-300 text-sm">
        {{ authError }}
      </div>

      <!-- Signup Success Message -->
      <div v-if="signUpSuccess" class="p-4 rounded-xl bg-green-500/10 backdrop-blur-sm border border-green-400/20 text-green-300 text-sm">
        <div class="flex items-start gap-3">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mt-0.5 flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
          </svg>
          <div>
            <p class="font-medium">Account created successfully!</p>
            <p class="text-xs mt-1 text-green-300/80">Please check your email to verify your account before signing in.</p>
          </div>
        </div>
      </div>

      <!-- Submit Button -->
      <button
          type="submit"
          class="w-full px-6 py-3 rounded-xl bg-white/20 backdrop-blur-sm border border-white/30 text-white font-medium hover:bg-white/30 hover:border-white/40 transition-all duration-300 flex items-center justify-center shadow-lg hover:shadow-xl transform hover:scale-[1.02]"
          :disabled="isLoading"
      >
        <Loader2 v-if="isLoading" class="h-5 w-5 mr-2 animate-spin"/>
        {{ isLoading ? 'Signing In...' : 'Sign In' }}
      </button>

      <!-- Social Login Divider -->
      <div class="relative my-8">
        <div class="absolute inset-0 flex items-center">
          <div class="w-full border-t border-white/20"></div>
        </div>
        <div class="relative flex justify-center text-sm">
          <span class="px-4 bg-white/5 backdrop-blur-sm text-white/70 rounded-full">Or continue with</span>
        </div>
      </div>

      <!-- Social Login Buttons -->
      <div class="grid grid-cols-1 gap-3">
        <AuthSocial/>
      </div>
    </form>

    <!-- Sign Up Form -->
    <form v-if="activeTab === 'signup'" @submit.prevent="handleSignUp" class="space-y-6">
      <!-- Full Name -->
      <div>
        <label for="signup-name" class="block text-sm font-medium text-white/90 mb-2">
          Full Name
        </label>
        <input
            id="signup-name"
            v-model="signUpForm.name"
            type="text"
            required
            class="w-full px-4 py-3 rounded-xl bg-white/10 backdrop-blur-sm border border-white/20 text-white placeholder-white/60 focus:bg-white/15 focus:border-white/40 focus:ring-0 focus:outline-none transition-all duration-300"
            :class="{ 'border-red-400 bg-red-500/10': formErrors.name }"
            placeholder="Enter your full name"
        />
        <p v-if="formErrors.name" class="mt-2 text-xs text-red-300">{{ formErrors.name }}</p>
      </div>

      <!-- Email -->
      <div>
        <label for="signup-email" class="block text-sm font-medium text-white/90 mb-2">
          Email Address
        </label>
        <input
            id="signup-email"
            v-model="signUpForm.email"
            type="email"
            required
            class="w-full px-4 py-3 rounded-xl bg-white/10 backdrop-blur-sm border border-white/20 text-white placeholder-white/60 focus:bg-white/15 focus:border-white/40 focus:ring-0 focus:outline-none transition-all duration-300"
            :class="{ 'border-red-400 bg-red-500/10': formErrors.email }"
            placeholder="Enter your email address"
        />
        <p v-if="formErrors.email" class="mt-2 text-xs text-red-300">{{ formErrors.email }}</p>
      </div>

      <!-- Password -->
      <div>
        <label for="signup-password" class="block text-sm font-medium text-white/90 mb-2">
          Password
        </label>
        <div class="relative">
          <input
              id="signup-password"
              v-model="signUpForm.password"
              :type="showPassword ? 'text' : 'password'"
              required
              class="w-full px-4 py-3 rounded-xl bg-white/10 backdrop-blur-sm border border-white/20 text-white placeholder-white/60 focus:bg-white/15 focus:border-white/40 focus:ring-0 focus:outline-none transition-all duration-300 pr-12"
              :class="{ 'border-red-400 bg-red-500/10': formErrors.password }"
              placeholder="Create a strong password"
          />
          <button
              type="button"
              class="absolute inset-y-0 right-0 pr-4 flex items-center text-white/60 hover:text-white transition-colors"
              @click="showPassword = !showPassword"
          >
            <Eye v-if="showPassword" class="h-5 w-5"/>
            <EyeOff v-else class="h-5 w-5"/>
          </button>
        </div>
        <p v-if="formErrors.password" class="mt-2 text-xs text-red-300">{{ formErrors.password }}</p>
      </div>

      <!-- Password Strength Indicator -->
      <div v-if="signUpForm.password" class="space-y-3">
        <div class="flex items-center gap-3">
          <div class="h-2 flex-1 rounded-full bg-white/20 overflow-hidden">
            <div
                class="h-full transition-all duration-500 rounded-full"
                :class="[
                passwordStrength === 'weak' ? 'w-1/3 bg-red-400' :
                passwordStrength === 'medium' ? 'w-2/3 bg-yellow-400' :
                'w-full bg-green-400'
              ]"
            ></div>
          </div>
          <span class="text-sm font-medium" :class="[
            passwordStrength === 'weak' ? 'text-red-300' :
            passwordStrength === 'medium' ? 'text-yellow-300' :
            'text-green-300'
          ]">
            {{ passwordStrength === 'weak' ? 'Weak' : passwordStrength === 'medium' ? 'Medium' : 'Strong' }}
          </span>
        </div>
        <ul class="text-xs space-y-2 text-white/70">
          <li class="flex items-center gap-2">
            <Check v-if="passwordCriteria.length" class="h-3 w-3 text-green-400"/>
            <X v-else class="h-3 w-3 text-red-400"/>
            At least 8 characters
          </li>
          <li class="flex items-center gap-2">
            <Check v-if="passwordCriteria.uppercase" class="h-3 w-3 text-green-400"/>
            <X v-else class="h-3 w-3 text-red-400"/>
            Contains uppercase letter
          </li>
          <li class="flex items-center gap-2">
            <Check v-if="passwordCriteria.number" class="h-3 w-3 text-green-400"/>
            <X v-else class="h-3 w-3 text-red-400"/>
            Contains number
          </li>
        </ul>
      </div>

      <!-- Error Message -->
      <div v-if="authError" class="p-4 rounded-xl bg-red-500/10 backdrop-blur-sm border border-red-400/20 text-red-300 text-sm">
        {{ authError }}
      </div>

      <!-- Submit Button -->
      <button
          type="submit"
          class="w-full px-6 py-3 rounded-xl bg-white/20 backdrop-blur-sm border border-white/30 text-white font-medium hover:bg-white/30 hover:border-white/40 transition-all duration-300 flex items-center justify-center shadow-lg hover:shadow-xl transform hover:scale-[1.02]"
          :disabled="isLoading"
      >
        <Loader2 v-if="isLoading" class="h-5 w-5 mr-2 animate-spin"/>
        {{ isLoading ? 'Creating Account...' : 'Create Account' }}
      </button>

      <!-- Social Login Divider -->
      <div class="relative my-8">
        <div class="absolute inset-0 flex items-center">
          <div class="w-full border-t border-white/20"></div>
        </div>
        <div class="relative flex justify-center text-sm">
          <span class="px-4 bg-white/5 backdrop-blur-sm text-white/70 rounded-full">Or continue with</span>
        </div>
      </div>

      <!-- Social Login Buttons -->
      <div class="grid grid-cols-1 gap-3">
        <AuthSocial/>
      </div>

      <!-- Terms Agreement -->
      <p class="text-xs text-center text-white/60 leading-relaxed">
        By signing up, you agree to our
        <NuxtLink to="/terms" class="text-white/80 hover:text-white underline underline-offset-2">Terms of Service</NuxtLink>
        and
        <NuxtLink to="/privacy" class="text-white/80 hover:text-white underline underline-offset-2">Privacy Policy</NuxtLink>
      </p>
    </form>
  </div>

  <!-- Forgot Password Dialog -->
  <TransitionRoot appear :show="showForgotPassword" as="template">
    <Dialog as="div" @close="showForgotPassword = false" class="relative z-50">
      <TransitionChild
          as="template"
          enter="duration-300 ease-out"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="duration-200 ease-in"
          leave-from="opacity-100"
          leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-black/30 backdrop-blur-sm"/>
      </TransitionChild>

      <div class="fixed inset-0 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4">
          <TransitionChild
              as="template"
              enter="duration-300 ease-out"
              enter-from="opacity-0 scale-95"
              enter-to="opacity-100 scale-100"
              leave="duration-200 ease-in"
              leave-from="opacity-100 scale-100"
              leave-to="opacity-0 scale-95"
          >
            <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white/10 backdrop-blur-2xl border border-white/20 p-8 shadow-2xl transition-all">
              <div class="flex justify-between items-center mb-6">
                <DialogTitle as="h3" class="text-xl font-semibold text-white">
                  Reset Password
                </DialogTitle>
                <button
                    type="button"
                    class="text-white/60 hover:text-white transition-colors"
                    @click="showForgotPassword = false"
                >
                  <X class="h-6 w-6"/>
                </button>
              </div>

              <form @submit.prevent="handleForgotPassword" class="space-y-6">
                <p class="text-sm text-white/80 leading-relaxed">
                  Enter your email address and we'll send you a secure link to reset your password.
                </p>

                <!-- Email -->
                <div>
                  <label for="reset-email" class="block text-sm font-medium text-white/90 mb-2">
                    Email Address
                  </label>
                  <input
                      id="reset-email"
                      v-model="forgotPasswordEmail"
                      type="email"
                      required
                      class="w-full px-4 py-3 rounded-xl bg-white/10 backdrop-blur-sm border border-white/20 text-white placeholder-white/60 focus:bg-white/15 focus:border-white/40 focus:ring-0 focus:outline-none transition-all duration-300"
                      placeholder="Enter your email address"
                  />
                </div>

                <!-- Success Message -->
                <div v-if="resetEmailSent" class="p-4 rounded-xl bg-green-500/10 backdrop-blur-sm border border-green-400/20 text-green-300 text-sm">
                  <div class="flex items-center gap-2">
                    <Check class="h-4 w-4"/>
                    <span>Password reset link sent! Please check your email.</span>
                  </div>
                </div>

                <!-- Submit Button -->
                <div class="flex justify-end gap-3">
                  <button
                      type="button"
                      class="px-5 py-2.5 rounded-xl text-white/70 text-sm font-medium hover:text-white hover:bg-white/10 transition-all duration-300"
                      @click="showForgotPassword = false"
                  >
                    Cancel
                  </button>
                  <button
                      type="submit"
                      class="px-5 py-2.5 rounded-xl bg-white/20 backdrop-blur-sm border border-white/30 text-white text-sm font-medium hover:bg-white/30 hover:border-white/40 transition-all duration-300 flex items-center shadow-lg"
                      :disabled="isLoading || resetEmailSent"
                  >
                    <Loader2 v-if="isLoading" class="h-4 w-4 mr-2 animate-spin"/>
                    {{ resetEmailSent ? 'Sent' : 'Send Reset Link' }}
                  </button>
                </div>
              </form>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup lang="ts">
import {computed, ref, watch} from 'vue'
import {Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot} from '@headlessui/vue'
import {Check, Eye, EyeOff, Loader2, X} from 'lucide-vue-next'

const props = defineProps<{
  initialTab?: 'signin' | 'signup'
}>()

const emit = defineEmits<{
  (e: 'success'): void
}>()

const isDark = ref(false)
const callbackURL = ref('')
const activeTab = ref(props.initialTab || 'signin')
const showPassword = ref(false)
const isLoading = ref(false)
const authError = ref('')
const signUpSuccess = ref<boolean>(false)
const showForgotPassword = ref(false)
const forgotPasswordEmail = ref('')
const resetEmailSent = ref(false)

// Form data
const signInForm = ref({
  email: '',
  password: '',
  rememberMe: false
})

const signUpForm = ref({
  name: '',
  email: '',
  password: ''
})

// Form validation
const formErrors = ref({
  name: '',
  email: '',
  password: ''
})

// Password strength
const passwordCriteria = computed(() => {
  const password = signUpForm.value.password
  return {
    length: password.length >= 8,
    uppercase: /[A-Z]/.test(password),
    number: /[0-9]/.test(password)
  }
})

const passwordStrength = computed(() => {
  const criteria = passwordCriteria.value
  const score = Object.values(criteria).filter(Boolean).length

  if (score <= 1) return 'weak'
  if (score === 2) return 'medium'
  return 'strong'
})

// Watch for prop changes
watch(() => props.initialTab, (newTab) => {
  if (newTab) {
    activeTab.value = newTab
  }
})

onMounted(() => {
  // Set callback URL
  callbackURL.value = 'http://localhost:3000/auth'
  
  // Update isDark based on current document class
  isDark.value = document.documentElement.classList.contains('dark')
  
  // Watch for theme changes
  const observer = new MutationObserver(() => {
    isDark.value = document.documentElement.classList.contains('dark')
  })
  
  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['class']
  })
  
  // Cleanup observer on unmount
  onUnmounted(() => {
    observer.disconnect()
  })
})

// Auth client
const {signIn, signUp} = useAuthClient()

// Handle sign in
const handleSignIn = async () => {
  // Reset errors
  authError.value = ''
  signUpSuccess.value = false
  formErrors.value = {name: '', email: '', password: ''}

  // Validate form
  if (!validateEmail(signInForm.value.email)) {
    formErrors.value.email = 'Please enter a valid email address'
    return
  }

  isLoading.value = true

  try {
    const {error} = await signIn.email({
      email: signInForm.value.email,
      password: signInForm.value.password,
      rememberMe: signInForm.value.rememberMe,
      callbackURL: callbackURL.value
    })

    if (error) throw error

    emit('success')
  } catch (error: any) {
    authError.value = error.message
  } finally {
    isLoading.value = false
  }
}

// Handle sign up
const handleSignUp = async () => {
  // Reset errors
  authError.value = ''
  signUpSuccess.value = false
  formErrors.value = {name: '', email: '', password: ''}

  // Validate form
  if (signUpForm.value.name.length < 2) {
    formErrors.value.name = 'Name must be at least 2 characters'
    return
  }

  if (!validateEmail(signUpForm.value.email)) {
    formErrors.value.email = 'Please enter a valid email address'
    return
  }

  if (signUpForm.value.password.length < 8) {
    formErrors.value.password = 'Password must be at least 8 characters'
    return
  }

  isLoading.value = true

  try {
    const {error} = await signUp.email({
      email: signUpForm.value.email,
      password: signUpForm.value.password,
      name: signUpForm.value.name,
      callbackURL: callbackURL.value
    })

    if (error) throw error

    // Show a success message
    authError.value = ''

    // Create success alert
    activeTab.value = 'signin'
    signUpSuccess.value = true

    // Pre-fill the email in the sign-in form
    signInForm.value.email = signUpForm.value.email

    // Reset sign-up form
    signUpForm.value = {
      name: '',
      email: '',
      password: ''
    }
  } catch (error: any) {
    authError.value = error.message
  } finally {
    isLoading.value = false
  }
}

// Handle forgot password
const handleForgotPassword = async () => {
  if (!validateEmail(forgotPasswordEmail.value)) {
    return
  }

  isLoading.value = true

  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    resetEmailSent.value = true

    // Close dialog after 3 seconds
    setTimeout(() => {
      showForgotPassword.value = false
      resetEmailSent.value = false
      forgotPasswordEmail.value = ''
    }, 10000)
  } catch (error) {
    console.error('Forgot password error:', error)
  } finally {
    isLoading.value = false
  }
}

// Validate email
const validateEmail = (email: string) => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}
</script>
