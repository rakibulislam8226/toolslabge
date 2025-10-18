<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-800 mb-2">Welcome Back</h1>
        <p class="text-gray-600">Sign in to your BaseTrack account</p>
      </div>

      <!-- Login Form -->
      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label class="block text-gray-700 text-sm font-medium mb-2" for="email">
            Email Address
          </label>
          <input
            type="email"
            id="email"
            v-model="form.email"
            placeholder="Enter your email"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            required
          />
        </div>

        <div>
          <label class="block text-gray-700 text-sm font-medium mb-2" for="password">
            Password
          </label>
          <input
            type="password"
            id="password"
            v-model="form.password"
            placeholder="Enter your password"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            required
          />
        </div>

        <button
          type="submit"
          class="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="loading"
        >
          <span v-if="loading" class="flex items-center justify-center">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Signing in...
          </span>
          <span v-else>Sign In</span>
        </button>
      </form>

      <!-- Messages -->
      <div v-if="successMessage" class="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
        <p class="text-green-600 text-center font-medium">{{ successMessage }}</p>
      </div>
      
      <div v-if="errorMessage" class="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
        <p class="text-red-600 text-center font-medium">{{ errorMessage }}</p>
      </div>

      <!-- Links -->
      <div class="mt-6 text-center space-y-2">
        <p class="text-gray-600 text-sm">
          Don't have an account?
          <router-link 
            to="/register" 
            class="text-blue-600 hover:text-blue-800 font-medium transition duration-300"
          >
            Create Organization
          </router-link>
        </p>
        
        <router-link 
          to="/" 
          class="block text-blue-600 hover:text-blue-800 text-sm font-medium transition duration-300"
        >
          ← Back to Home
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from "@/plugins/axiosConfig.js";
import { useAuth } from "@/composables/useAuth.js";

const router = useRouter()
const { login } = useAuth()

const form = reactive({
  email: '',
  password: ''
})

const loading = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

const handleLogin = async () => {
  successMessage.value = ''
  errorMessage.value = ''
  loading.value = true

  try {
    const response = await axios.post('token/', {
      email: form.email,
      password: form.password
    })

    // Handle successful login - check for tokens in nested data structure
    if (response.data.data?.access && response.data.data?.refresh) {
      // Login with tokens from nested data structure
      login({
        access: response.data.data.access,
        refresh: response.data.data.refresh
      }, response.data.data.user || null)

      successMessage.value = 'Login successful! Redirecting...'

      // Redirect to dashboard
      setTimeout(() => {
        router.push('/dashboard')
      }, 1000)

    } else if (response.data.access && response.data.refresh) {
      // Fallback: Login with tokens from direct structure
      login({
        access: response.data.access,
        refresh: response.data.refresh
      }, response.data.user || null)

      successMessage.value = 'Login successful! Redirecting...'

      setTimeout(() => {
        router.push('/dashboard')
      }, 1000)

    } else {
      errorMessage.value = 'Invalid response from server. Please try again.'
    }

  } catch (error) {
    if (error.response?.status === 401) {
      errorMessage.value = 'Invalid email or password. Please try again.'
    } else if (error.response?.data?.detail) {
      errorMessage.value = error.response.data.detail
    } else if (error.response?.data?.non_field_errors) {
      errorMessage.value = error.response.data.non_field_errors[0]
    } else if (error.response?.data) {
      // Handle field-specific errors
      const errors = Object.values(error.response.data).flat()
      errorMessage.value = errors.join(', ')
    } else {
      errorMessage.value = 'Something went wrong. Please try again.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* Additional styles if needed */
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
</style>