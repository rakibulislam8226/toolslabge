<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-800 mb-2">Create Organization</h1>
        <p class="text-gray-600">Start your journey with BaseTrack</p>
      </div>

      <!-- Registration Form -->
      <form @submit.prevent="createOrganization" class="space-y-6">
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-gray-700 text-sm font-medium mb-2" for="first_name">
              First Name
            </label>
            <input type="text" id="first_name" v-model="form.first_name" placeholder="Enter your first name"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required />
          </div>

          <div>
            <label class="block text-gray-700 text-sm font-medium mb-2" for="last_name">
              Last Name
            </label>
            <input type="text" id="last_name" v-model="form.last_name" placeholder="Enter your last name"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required />
          </div>
        </div>

        <div>
          <label class="block text-gray-700 text-sm font-medium mb-2" for="email">
            Email Address
          </label>
          <input type="email" id="email" v-model="form.email" placeholder="Enter your email"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            required />
        </div>

        <div>
          <label class="block text-gray-700 text-sm font-medium mb-2" for="password">
            Password
          </label>
          <input type="password" id="password" v-model="form.password" placeholder="Enter your password"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            required />
        </div>

        <div>
          <label class="block text-gray-700 text-sm font-medium mb-2" for="organization_name">
            Organization Name
          </label>
          <input type="text" id="organization_name" v-model="form.organization_name"
            placeholder="Enter organization name"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            required />
        </div>

        <Button type="submit" variant="primary" size="md" fullWidth :loading="loading" loadingText="Creating..."
          label="Create Organization" />
      </form>

      <!-- Messages -->
      <div v-if="successMessage" class="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
        <p class="text-green-600 text-center font-medium">{{ successMessage }}</p>
      </div>

      <div v-if="errorMessage" class="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
        <p class="text-red-600 text-center font-medium">{{ errorMessage }}</p>
      </div>
      <div class="mt-6 text-center space-y-2">
        <p class="text-gray-600 text-sm">
          Already have an account?
          <router-link to="/login"
            class="text-blue-600 hover:text-blue-800 text-sm font-medium transition duration-300">
            ← Back to Login
          </router-link>
        </p>

        <router-link to="/" class="text-blue-600 hover:text-blue-800 text-sm font-medium transition duration-300">
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
import Button from '@/components/Button.vue'

const router = useRouter()
const { login } = useAuth()

const form = reactive({
  first_name: '',
  last_name: '',
  email: '',
  password: '',
  organization_name: ''
})

const loading = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

const createOrganization = async () => {
  successMessage.value = ''
  errorMessage.value = ''
  loading.value = true

  try {
    const response = await axios.post('organizations/register/', { ...form })
    successMessage.value = response.data.data.detail || response.data.message || 'Organization created successfully!'

    // Handle authentication tokens if provided
    if (response.data.access && response.data.refresh) {
      // Login the user with tokens
      login({
        access: response.data.access,
        refresh: response.data.refresh
      }, response.data.user || null)

      // Show success message briefly then redirect to dashboard
      setTimeout(() => {
        router.push('/dashboard') // Redirect to dashboard after login
      }, 1500)
    } else if (response.data.data?.access && response.data.data?.refresh) {
      // Handle nested token structure
      login({
        access: response.data.data.access,
        refresh: response.data.data.refresh
      }, response.data.data.user || null)

      setTimeout(() => {
        router.push('/dashboard')
      }, 1500)
    } else {
      // No tokens provided, just show success message
      // Reset form
      Object.keys(form).forEach(key => (form[key] = ''))
    }

  } catch (error) {
    if (error.response?.data?.detail) {
      errorMessage.value = error.response.data.detail
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