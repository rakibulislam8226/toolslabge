<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click="handleOverlayClick">
    <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
      <!-- Modal Header -->
      <div class="flex items-center justify-between mb-6">
        <h3 class="text-lg font-semibold text-gray-900">Invite Team Member</h3>
        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-gray-600 focus:outline-none"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>

      <!-- Form -->
      <form @submit.prevent="sendInvitation">
        <!-- Email Field -->
        <div class="mb-4">
          <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
            Email Address
          </label>
          <input
            v-model="form.email"
            type="email"
            id="email"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            :class="{ 'border-red-500': errors.email }"
            placeholder="Enter email address"
          />
          <p v-if="errors.email" class="mt-1 text-sm text-red-600">{{ errors.email }}</p>
        </div>

        <!-- Role Field -->
        <div class="mb-6">
          <label for="role" class="block text-sm font-medium text-gray-700 mb-2">
            Role
          </label>
          <select
            v-model="form.role"
            id="role"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            :class="{ 'border-red-500': errors.role }"
          >
            <option value="">Select a role</option>
            <option 
              v-for="role in availableRoles" 
              :key="role.value" 
              :value="role.value"
            >
              {{ role.label }}
            </option>
          </select>
          <p v-if="errors.role" class="mt-1 text-sm text-red-600">{{ errors.role }}</p>
        </div>

        <!-- Action Buttons -->
        <div class="flex justify-end space-x-3">
          <button
            type="button"
            @click="$emit('close')"
            class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            :disabled="loading"
          >
            Cancel
          </button>
          <button
            type="submit"
            class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="loading"
          >
            <span v-if="loading" class="flex items-center">
              <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Sending...
            </span>
            <span v-else>Send Invitation</span>
          </button>
        </div>
      </form>

      <!-- Success Message -->
      <div v-if="successMessage" class="mt-4 p-4 bg-green-50 border border-green-200 rounded-md">
        <div class="flex">
          <svg class="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <p class="ml-2 text-sm text-green-700">{{ successMessage }}</p>
        </div>
      </div>

      <!-- Error Message -->
      <div v-if="errorMessage" class="mt-4 p-4 bg-red-50 border border-red-200 rounded-md">
        <div class="flex">
          <svg class="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <p class="ml-2 text-sm text-red-700">{{ errorMessage }}</p>
        </div>
      </div>

      <!-- Debug Info (temporary) -->
      <div class="mt-4 p-3 bg-gray-100 border rounded-md text-xs">
        <p><strong>Debug Info:</strong></p>
        <p>User exists: {{ !!user }}</p>
        <p>Organization ID: {{ organizationId }}</p>
        <p>User has data: {{ !!user?.data }}</p>
        <p>User.data organizations: {{ user?.data?.organizations?.length || 0 }}</p>
        <p>User organizations: {{ user?.organizations?.length || 0 }}</p>
        <p>User.data org memberships: {{ user?.data?.organization_memberships?.length || 0 }}</p>
        <p>User org memberships: {{ user?.organization_memberships?.length || 0 }}</p>
        <div class="mt-2 p-2 bg-white rounded text-xs max-h-20 overflow-y-auto">
          <p><strong>Full user data:</strong></p>
          <pre>{{ JSON.stringify(user, null, 2) }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuth } from '@/composables/useAuth.js'
import axios from '@/plugins/axiosConfig.js'

const emit = defineEmits(['close', 'invited'])
const { user, fetchUserProfile } = useAuth()

const loading = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

const form = ref({
  email: '',
  role: ''
})

const errors = ref({})

// Get current organization ID from user data
const organizationId = computed(() => {
  console.log('Computing organizationId, user.value:', user.value)
  
  // Try multiple possible paths for organization data
  // First check if user data has the API response structure
  if (user.value?.data?.organizations?.[0]?.organization_id) {
    console.log('Found org ID via data.organizations path:', user.value.data.organizations[0].organization_id)
    return user.value.data.organizations[0].organization_id
  }
  
  if (user.value?.organizations?.[0]?.organization_id) {
    console.log('Found org ID via organizations path:', user.value.organizations[0].organization_id)
    return user.value.organizations[0].organization_id
  }
  
  if (user.value?.data?.organization_memberships?.[0]?.organization_id) {
    console.log('Found org ID via data.organization_memberships path:', user.value.data.organization_memberships[0].organization_id)
    return user.value.data.organization_memberships[0].organization_id
  }
  
  if (user.value?.organization_memberships?.[0]?.organization_id) {
    console.log('Found org ID via organization_memberships path:', user.value.organization_memberships[0].organization_id)
    return user.value.organization_memberships[0].organization_id
  }
  
  // Check if organization data is directly on the user
  if (user.value?.organization_id) {
    console.log('Found org ID directly on user:', user.value.organization_id)
    return user.value.organization_id
  }
  
  if (user.value?.data?.organization_id) {
    console.log('Found org ID directly on user.data:', user.value.data.organization_id)
    return user.value.data.organization_id
  }
  
  console.log('No organization ID found in user data')
  console.log('Available user data keys:', Object.keys(user.value || {}))
  if (user.value?.data) {
    console.log('Available user.data keys:', Object.keys(user.value.data || {}))
  }
  return null
})

// Available roles based on the backend choices
const availableRoles = [
  { value: 'member', label: 'Member' },
  { value: 'manager', label: 'Manager' },
  { value: 'admin', label: 'Admin' },
  { value: 'owner', label: 'Owner' }
]

const sendInvitation = async () => {
  try {
    loading.value = true
    errors.value = {}
    errorMessage.value = ''
    successMessage.value = ''

    // Check if we need to fetch user profile data
    if (!organizationId.value) {
      console.log('Organization ID not found, fetching user profile...')
      await fetchUserProfile()
    }

    // Validate form
    if (!organizationId.value) {
      errorMessage.value = 'Organization not found. Please refresh and try again.'
      return
    }
    if (!form.value.email) {
      errors.value.email = 'Email is required'
      return
    }
    if (!form.value.role) {
      errors.value.role = 'Role is required'
      return
    }

    // Debug: Log the user data and organization ID
    console.log('Full user data:', user.value)
    console.log('Organization ID:', organizationId.value)
    console.log('Sending invitation:', { email: form.value.email, role: form.value.role })

    // Send invitation to backend
    const response = await axios.post(`organizations/${organizationId.value}/invite/`, {
      email: form.value.email,
      role: form.value.role
    })

    successMessage.value = response.data.detail || 'Invitation sent successfully!'
    
    // Emit the invitation data to parent component
    emit('invited', {
      email: form.value.email,
      role: form.value.role,
      created_at: new Date().toISOString()
    })

    // Reset form
    form.value = {
      email: '',
      role: ''
    }

    // Close modal after 2 seconds
    setTimeout(() => {
      emit('close')
    }, 2000)

  } catch (error) {
    console.error('Failed to send invitation:', error)
    
    if (error.response?.data) {
      // Handle validation errors
      if (error.response.data.email) {
        errors.value.email = Array.isArray(error.response.data.email) 
          ? error.response.data.email[0] 
          : error.response.data.email
      }
      if (error.response.data.role) {
        errors.value.role = Array.isArray(error.response.data.role) 
          ? error.response.data.role[0] 
          : error.response.data.role
      }
      if (error.response.data.detail) {
        errorMessage.value = error.response.data.detail
      } else if (error.response.data.non_field_errors) {
        errorMessage.value = Array.isArray(error.response.data.non_field_errors)
          ? error.response.data.non_field_errors[0]
          : error.response.data.non_field_errors
      } else {
        errorMessage.value = 'Failed to send invitation. Please try again.'
      }
    } else {
      errorMessage.value = 'Failed to send invitation. Please try again.'
    }
  } finally {
    loading.value = false
  }
}

const handleOverlayClick = (event) => {
  if (event.target === event.currentTarget) {
    emit('close')
  }
}

// Fetch user profile on mount if organization data is missing
onMounted(async () => {
  if (!organizationId.value) {
    console.log('Modal mounted: Organization ID not found, fetching user profile...')
    await fetchUserProfile()
  }
})
</script>