<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="bg-white p-8 rounded-xl shadow-2xl w-full max-w-md border border-gray-100">
      <!-- Header -->
      <div class="text-center mb-8">
        <div class="mx-auto w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mb-4">
          <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </div>
        <h1 class="text-3xl font-bold text-gray-900 mb-2">Welcome Back</h1>
        <p class="text-gray-600">Sign in to your TrackTools account</p>
      </div>

      <!-- General Error Alert -->
      <div v-if="errors.general" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
        <div class="flex items-center">
          <svg class="w-5 h-5 text-red-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p class="text-sm text-red-800">{{ errors.general }}</p>
        </div>
      </div>

      <!-- Login Form -->
      <form @submit.prevent="handleLogin" class="space-y-6" novalidate>
        <!-- Email Field -->
        <BaseInput v-model="form.email" label="Email Address" type="email" placeholder="Enter your email address"
          :error="errors.email" :disabled="loading" required size="lg" autocomplete="email"
          @blur="validateField('email')" @input="clearError('email')" />

        <!-- Password Field -->
        <div class="relative">
          <BaseInput v-model="form.password" label="Password" :type="showPassword ? 'text' : 'password'"
            placeholder="Enter your password" :error="errors.password" :disabled="loading" required size="lg"
            autocomplete="current-password" @blur="validateField('password')" @input="clearError('password')" />
          <!-- Password Toggle -->
          <button type="button" @click="togglePasswordVisibility"
            class="absolute right-3 top-9 text-gray-500 hover:text-gray-700 focus:outline-none focus:text-gray-700 transition-colors"
            :disabled="loading" tabindex="-1">
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
            <input id="remember-me" v-model="form.rememberMe" type="checkbox"
              class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded" :disabled="loading" />
            <label for="remember-me" class="ml-2 block text-sm text-gray-700">
              Remember me
            </label>
          </div>
          <router-link to="/forgot-password"
            class="text-sm text-blue-600 hover:text-blue-800 font-medium transition duration-300">
            Forgot password?
          </router-link>
        </div>

        <!-- Submit Button -->
        <Button type="submit" variant="primary" size="lg" fullWidth :loading="loading" loadingText="Signing in..."
          label="Sign In" :disabled="!isFormValid"
          class="bg-blue-600 hover:bg-blue-700 text-white shadow-lg hover:shadow-xl transition-all duration-200 transform hover:-translate-y-0.5" />
      </form>

      <!-- Links -->
      <div class="mt-8 text-center space-y-3">
        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-300"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-2 bg-white text-gray-500">New to TrackTools?</span>
          </div>
        </div>

        <p class="text-gray-600 text-sm">
          <router-link to="/register"
            class="text-blue-600 hover:text-blue-800 font-medium transition duration-300 inline-flex items-center">
            Create your organization
            <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </router-link>
        </p>

        <router-link to="/"
          class="inline-flex items-center text-gray-500 hover:text-gray-700 text-sm font-medium transition duration-300">
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
/* Gradient background animation */
.min-h-screen {
  background: linear-gradient(-45deg, #f8fafc, #e2e8f0, #cbd5e1, #f1f5f9);
  background-size: 400% 400%;
  animation: gradientShift 15s ease infinite;
}

@keyframes gradientShift {
  0% {
    background-position: 0% 50%;
  }

  50% {
    background-position: 100% 50%;
  }

  100% {
    background-position: 0% 50%;
  }
}

/* Enhanced focus states */
.form-input:focus {
  transform: translateY(-1px);
  box-shadow: 0 10px 25px rgba(59, 130, 246, 0.15);
}

/* Button hover effects */
.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
}

/* Loading spinner */
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

/* Error shake animation */
.error-shake {
  animation: shake 0.5s ease-in-out;
}

@keyframes shake {

  0%,
  100% {
    transform: translateX(0);
  }

  25% {
    transform: translateX(-5px);
  }

  75% {
    transform: translateX(5px);
  }
}

/* Smooth transitions */
.transition-all {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Custom checkbox styling */
input[type="checkbox"]:checked {
  background-image: url("data:image/svg+xml,%3csvg viewBox='0 0 16 16' fill='white' xmlns='http://www.w3.org/2000/svg'%3e%3cpath d='m13.854 3.646-7.5 7.5a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6 10.293l7.146-7.147a.5.5 0 0 1 .708.708z'/%3e%3c/svg%3e");
}

/* Enhanced card styling */
.card-shadow {
  box-shadow:
    0 10px 15px -3px rgba(0, 0, 0, 0.1),
    0 4px 6px -2px rgba(0, 0, 0, 0.05),
    0 0 0 1px rgba(0, 0, 0, 0.05);
}

/* Link hover effects */
a {
  position: relative;
  transition: color 0.3s ease;
}

a:hover {
  transform: translateY(-1px);
}

/* Icon animations */
.icon-hover:hover {
  transform: scale(1.1);
  transition: transform 0.2s ease;
}

/* Form field animation */
.form-group {
  position: relative;
}

.form-group input:focus+label,
.form-group input:not(:placeholder-shown)+label {
  transform: translateY(-1.5rem) scale(0.875);
  color: #3b82f6;
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .card-shadow {
    margin: 1rem;
    border-radius: 1rem;
  }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .min-h-screen {
    background: linear-gradient(-45deg, #1e293b, #334155, #475569, #1e293b);
  }
}

/* Accessibility improvements */
@media (prefers-reduced-motion: reduce) {
  .min-h-screen {
    animation: none;
  }

  .transition-all {
    transition: none;
  }

  .btn-primary:hover {
    transform: none;
  }
}
</style>