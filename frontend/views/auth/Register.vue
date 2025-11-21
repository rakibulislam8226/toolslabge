<template>
  <div
    class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div
      class="bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-xl border border-white/20 w-full max-w-md relative overflow-hidden">
      <!-- Background decoration -->
      <div
        class="absolute -top-10 -right-10 w-20 h-20 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full opacity-20">
      </div>
      <div
        class="absolute -bottom-10 -left-10 w-32 h-32 bg-gradient-to-tr from-indigo-400 to-blue-500 rounded-full opacity-20">
      </div>

      <!-- Header -->
      <div class="text-center mb-8 relative z-10">
        <div
          class="w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full mx-auto mb-4 flex items-center justify-center">
          <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4">
            </path>
          </svg>
        </div>
        <h1 class="text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent mb-2">
          Create Organization
        </h1>
        <p class="text-gray-600">Start your journey with TrackTools</p>
      </div>

      <!-- Registration Form -->
      <form @submit.prevent="handleSubmit" class="space-y-6 relative z-10">
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <BaseInput label="First Name" v-model="form.first_name" placeholder="Enter your first name"
            :error="errors.first_name" size="md" @blur="validateField('first_name')"
            @input="clearError('first_name')" />

          <BaseInput label="Last Name" v-model="form.last_name" placeholder="Enter your last name"
            :error="errors.last_name" size="md" @blur="validateField('last_name')" @input="clearError('last_name')" />
        </div>

        <BaseInput label="Email Address" type="email" v-model="form.email" placeholder="Enter your email address"
          :error="errors.email" size="md" @blur="validateField('email')" @input="clearError('email')" />

        <BaseInput label="Password" type="password" v-model="form.password" placeholder="Create a secure password"
          :error="errors.password" help-text="Password must be at least 8 characters long" size="md"
          @blur="validateField('password')" @input="clearError('password')" />

        <BaseInput label="Organization Name" v-model="form.organization_name" placeholder="Enter your organization name"
          :error="errors.organization_name" size="md" @blur="validateField('organization_name')"
          @input="clearError('organization_name')" />

        <Button type="submit" variant="primary" size="lg" fullWidth :loading="loading"
          loadingText="Creating Organization..." label="Create Organization"
          class="mt-8 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 shadow-lg hover:shadow-xl transition-all duration-200 transform hover:-translate-y-0.5" />
      </form>

      <div class="mt-8 text-center space-y-3 relative z-10">
        <div class="flex items-center justify-center space-x-2">
          <div class="h-px bg-gray-300 flex-1"></div>
          <span class="text-gray-500 text-sm">or</span>
          <div class="h-px bg-gray-300 flex-1"></div>
        </div>

        <p class="text-gray-600 text-sm">
          Already have an account?
          <router-link to="/login"
            class="text-blue-600 hover:text-blue-800 text-sm font-semibold transition duration-300 hover:underline">
            Sign in here
          </router-link>
        </p>

        <router-link to="/"
          class="inline-flex items-center text-gray-500 hover:text-gray-700 text-sm transition duration-300 hover:underline">
          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18">
            </path>
          </svg>
          Back to Home
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, inject } from 'vue'
import { useRouter } from 'vue-router'
import axios from "@/plugins/axiosConfig.js";
import { useAuth } from "@/composables/useAuth.js";
import Button from '@/components/Button.vue'
import { BaseInput } from '@/components/forms'

const router = useRouter()
const { login } = useAuth()
const toast = inject('toast')

// Form data
const form = reactive({
  first_name: '',
  last_name: '',
  email: '',
  password: '',
  organization_name: ''
})

const loading = ref(false)
const errors = ref({})

// Required fields
const requiredFields = ['first_name', 'last_name', 'email', 'password', 'organization_name']

// Field labels for error messages
const fieldLabels = {
  first_name: 'First name',
  last_name: 'Last name',
  email: 'Email address',
  password: 'Password',
  organization_name: 'Organization name'
}

// Validate single field
const validateField = (fieldName) => {
  const value = form[fieldName]?.trim()

  // Required field validation
  if (requiredFields.includes(fieldName) && !value) {
    errors.value[fieldName] = `${fieldLabels[fieldName]} is required`
    return false
  }

  // Email validation
  if (fieldName === 'email' && value) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(value)) {
      errors.value[fieldName] = 'Please enter a valid email address'
      return false
    }
  }

  // Password validation
  if (fieldName === 'password' && value && value.length < 8) {
    errors.value[fieldName] = 'Password must be at least 8 characters long'
    return false
  }

  // Clear error if validation passes
  delete errors.value[fieldName]
  return true
}

// Validate all fields
const validateForm = () => {
  let isValid = true
  requiredFields.forEach(field => {
    if (!validateField(field)) {
      isValid = false
    }
  })
  return isValid
}

// Clear error for specific field
const clearError = (fieldName) => {
  delete errors.value[fieldName]
}

// Handle form submission
const handleSubmit = async () => {
  if (!validateForm()) {
    toast.error('Please fix the errors below and try again.')
    return
  }

  loading.value = true
  errors.value = {}

  try {
    const response = await axios.post('organizations/register/', form)

    toast.success('Organization created successfully! Welcome to TrackTools.')

    // Handle authentication
    const authData = response.data.access ? response.data : response.data.data

    if (authData?.access && authData?.refresh) {
      login({
        access: authData.access,
        refresh: authData.refresh
      }, authData.user || null)

      setTimeout(() => router.push('/dashboard'), 1000)
    } else {
      // Reset form on success
      Object.keys(form).forEach(key => form[key] = '')
      toast.info('Registration successful! Please check your email for verification.')
    }

  } catch (error) {
    console.error('Registration error:', error)

    const errorData = error.response?.data

    if (errorData?.data?.errors) {
      // Handle API error format: { data: { errors: [{ field: "message" }] } }
      errorData.data.errors.forEach(errorObj => {
        Object.assign(errors.value, errorObj)
      })
      toast.error(errorData.message || 'Please fix the errors below and try again.')
    } else if (errorData && typeof errorData === 'object') {
      // Handle standard validation errors
      Object.keys(errorData).forEach(field => {
        const message = Array.isArray(errorData[field]) ? errorData[field][0] : errorData[field]
        if (typeof message === 'string') {
          errors.value[field] = message
        }
      })
      toast.error('Please fix the errors below and try again.')
    } else {
      // Handle general errors
      const message = errorData?.detail || errorData?.message || 'Something went wrong. Please try again.'
      toast.error(message)
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* Custom animations and enhanced styles */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease;
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

/* Enhanced button hover effects */
.group:hover .group-hover\:scale-105 {
  transform: scale(1.05);
}

/* Glassmorphism effect enhancement */
.backdrop-blur-sm {
  backdrop-filter: blur(8px);
}

/* Custom focus states for better accessibility */
.focus-within\:ring-2:focus-within {
  box-shadow: 0 0 0 2px rgb(59 130 246 / 0.5);
}

/* Loading spinner animation */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

/* Gradient text animation */
@keyframes gradient-shift {

  0%,
  100% {
    background-position: 0% 50%;
  }

  50% {
    background-position: 100% 50%;
  }
}

.animate-gradient {
  background-size: 200% 200%;
  animation: gradient-shift 3s ease infinite;
}

/* Form validation styling */
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

/* Enhanced shadow effects */
.shadow-glow {
  box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
}

/* Responsive improvements */
@media (max-width: 640px) {
  .grid-cols-1.sm\:grid-cols-2 {
    grid-template-columns: 1fr;
  }
}

/* Custom scrollbar for better UX */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: rgba(59, 130, 246, 0.3);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(59, 130, 246, 0.5);
}
</style>