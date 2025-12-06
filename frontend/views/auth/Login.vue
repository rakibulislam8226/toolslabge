<template>
  <div
    class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 transition-colors duration-300 bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-gray-900 dark:via-slate-900 dark:to-gray-800">
    <div
      class="p-8 rounded-2xl shadow-xl w-full max-w-md border backdrop-blur-sm transition-all duration-300 bg-white/90 border-gray-200 dark:bg-gray-800/90 dark:border-gray-700">
      <!-- Header -->
      <div class="text-center mb-8">
        <div
          class="mx-auto w-16 h-16 rounded-full flex items-center justify-center mb-4 bg-gradient-to-r from-blue-600 to-indigo-600 dark:from-cyan-500 dark:to-blue-500">
          <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </div>
        <h1
          class="text-3xl font-bold mb-2 bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent dark:from-gray-100 dark:to-gray-300">
          Welcome Back</h1>
        <p class="text-gray-600 dark:text-gray-400">Sign in to your TrackTools account</p>
      </div>

      <!-- General Error Alert -->
      <div v-if="errors.general"
        class="mb-6 p-4 rounded-lg border bg-red-50 border-red-200 dark:bg-red-900/20 dark:border-red-700">
        <div class="flex items-center">
          <svg class="w-5 h-5 text-red-500 mr-2 dark:text-red-400" fill="none" stroke="currentColor"
            viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p class="text-sm text-red-800 dark:text-red-200">{{ errors.general }}</p>
        </div>
      </div>

      <!-- Login Form -->
      <form @submit.prevent=" handleLogin " class="space-y-6" novalidate>
        <!-- Email Field -->
        <BaseInput v-model=" form.email " label="Email Address" type="email" placeholder="Enter your email address"
          :error=" errors.email " :disabled=" loading " required size="lg" autocomplete="email"
          @blur="validateField('email')" @input="clearError('email')" />

        <!-- Password Field -->
        <div class="relative">
          <BaseInput v-model=" form.password " label="Password" :type=" showPassword ? 'text' : 'password' "
            placeholder="Enter your password" :error=" errors.password " :disabled=" loading " required size="lg"
            autocomplete="current-password" @blur="validateField('password')" @input="clearError('password')" />
          <!-- Password Toggle -->
          <button type="button" @click=" togglePasswordVisibility "
            class="absolute right-3 top-9 transition-colors text-gray-500 hover:text-gray-700 focus:outline-none focus:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300 dark:focus:text-gray-300"
            :disabled=" loading " tabindex="-1">
            <svg v-if="showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L8.464 8.464a10.007 10.007 0 00-1.563 3.029M9.878 9.878l.742-.742M21.535 12a10.05 10.05 0 01-2.985 4.825" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3l18 18" />
            </svg>
            <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
          </button>
        </div>

        <!-- Remember Me & Forgot Password -->
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <input id="remember-me" v-model=" form.rememberMe " type="checkbox"
              class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:focus:ring-blue-400"
              :disabled=" loading " />
            <label for="remember-me" class="ml-2 block text-sm text-gray-700 dark:text-gray-300">
              Remember me
            </label>
          </div>
          <router-link to="/forgot-password"
            class="text-sm font-medium transition duration-300 text-blue-600 hover:text-blue-800 dark:text-cyan-400 dark:hover:text-cyan-300">
            Forgot password?
          </router-link>
        </div>

        <!-- Submit Button -->
        <Button type="submit" variant="primary" size="lg" fullWidth :loading=" loading " loadingText="Signing in..."
          label="Sign In" :disabled=" !isFormValid "
          class="shadow-lg hover:shadow-xl transition-all duration-200 transform hover:-translate-y-0.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 dark:from-cyan-500 dark:to-blue-600 dark:hover:from-cyan-600 dark:hover:to-blue-700" />
      </form>

      <!-- Links -->
      <div class="mt-8 text-center space-y-3">
        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-300 dark:border-gray-600"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-2 text-gray-500 dark:text-gray-400 bg-white dark:bg-gray-800">New to TrackTools?</span>
          </div>
        </div>

        <p class="text-sm text-gray-600 dark:text-gray-400">
          <router-link to="/register"
            class="font-medium transition duration-300 inline-flex items-center text-blue-600 hover:text-blue-800 dark:text-cyan-400 dark:hover:text-cyan-300">
            Create your organization
            <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </router-link>
        </p>

        <router-link to="/"
          class="inline-flex items-center text-sm font-medium transition duration-300 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300">
          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Back to Home
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, inject, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from "@/plugins/axiosConfig.js"
import { useAuth } from "@/composables/useAuth.js"
import Button from '@/components/Button.vue'
import { BaseInput } from '@/components/forms'

const router = useRouter()
const { login, isAuthenticated } = useAuth()
const toast = inject('toast')

// State
const loading = ref(false)
const showPassword = ref(false)
const errors = ref({})

// Form data
const form = reactive({
  email: '',
  password: '',
  rememberMe: false
})

// Computed
const isFormValid = computed(() => {
  return form.email && form.password
})

// Utilities
const isValidEmail = (email) => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}

const clearError = (field) => {
  if (errors.value[field]) {
    delete errors.value[field]
  }
}

const validateField = (field) => {
  clearError(field)

  if (field === 'email' && form.email && !isValidEmail(form.email)) {
    errors.value.email = 'Please enter a valid email address'
  }

  if (field === 'password' && !form.password) {
    errors.value.password = 'Password is required'
  }
}

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}

// Main login handler
const handleLogin = async () => {
  if (loading.value || !isFormValid.value) return

  // Clear previous errors
  errors.value = {}
  loading.value = true

  try {
    const response = await axios.post('token/', {
      email: form.email.trim(),
      password: form.password
    })

    // Extract tokens
    const data = response.data.data || response.data
    if (data.access && data.refresh) {
      await login({
        access: data.access,
        refresh: data.refresh
      })

      toast.success('Welcome back!')
      setTimeout(() => router.push('/dashboard'), 1000)
    } else {
      throw new Error('Invalid response format')
    }

  } catch (error) {
    console.error('Login failed:', error)

    // Check if error is due to email not being verified
    if (error.response?.data?.email_not_verified) {
      const userEmail = error.response.data.email || form.email.trim()
      toast.error('Please verify your email address before logging in')
      setTimeout(() => {
        router.push(`/email-verification-required?email=${encodeURIComponent(userEmail)}`)
      }, 2000)
      return
    }

    if (error.response?.status === 401) {
      errors.value.general = 'Invalid email or password'
    } else if (error.response?.data?.detail) {
      errors.value.general = error.response.data.detail
    } else if (error.response?.data?.message) {
      errors.value.general = error.response.data.message
    } else {
      errors.value.general = 'Login failed. Please try again.'
    }

    toast.error(errors.value.general)
  } finally {
    loading.value = false
  }
}

// Lifecycle
onMounted(() => {
  if (isAuthenticated.value) {
    router.push('/dashboard')
  }
})
</script>

<style scoped>
/* Only essential styles that can't be achieved with Tailwind */
</style>