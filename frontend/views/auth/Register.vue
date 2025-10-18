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
            <input
              type="text"
              id="first_name"
              v-model="form.first_name"
              placeholder="Enter your first name"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>

          <div>
            <label class="block text-gray-700 text-sm font-medium mb-2" for="last_name">
              Last Name
            </label>
            <input
              type="text"
              id="last_name"
              v-model="form.last_name"
              placeholder="Enter your last name"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>
        </div>

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

        <div>
          <label class="block text-gray-700 text-sm font-medium mb-2" for="organization_name">
            Organization Name
          </label>
          <input
            type="text"
            id="organization_name"
            v-model="form.organization_name"
            placeholder="Enter organization name"
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
            Creating...
          </span>
          <span v-else>Create Organization</span>
        </button>
      </form>

      <!-- Messages -->
      <div v-if="successMessage" class="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
        <p class="text-green-600 text-center font-medium">{{ successMessage }}</p>
      </div>
      
      <div v-if="errorMessage" class="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
        <p class="text-red-600 text-center font-medium">{{ errorMessage }}</p>
      </div>

      <!-- Back to Home -->
      <div class="mt-6 text-center">
        <router-link 
          to="/" 
          class="text-blue-600 hover:text-blue-800 text-sm font-medium transition duration-300"
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

const router = useRouter()

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
    const response = await axios.post('organizations/', { ...form })
    successMessage.value = `Organization "${response.data.organization_name}" created successfully!`

    // Reset form
    Object.keys(form).forEach(key => (form[key] = ''))

    // Optional: Redirect to a dashboard or login page after success
    setTimeout(() => {
      // router.push('/dashboard') // Uncomment when you have a dashboard
    }, 2000)

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