<template>
  <BaseModal
    :is-open="isOpen"
    title="Edit Member Role"
    size="md"
    @close="handleClose"
  >
    <form @submit.prevent="handleSubmit" class="space-y-6">
      <!-- Member Info Display -->
      <div class="bg-gray-50 rounded-lg p-4">
        <div class="flex items-center">
          <div class="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
            {{ getInitials(member?.user) }}
          </div>
          <div class="ml-3">
            <div class="font-medium text-gray-900">
              <span v-if="member?.user_name">
                {{ member.user_name }}
              </span>
              <span v-else>{{ member?.user_email }}</span>
            </div>
            <div class="text-sm text-gray-500">{{ member?.user_email }}</div>
            <div class="text-xs text-gray-400">
              Current role: <span class="font-medium capitalize">{{ member?.role }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Role Selection -->
      <div>
        <label for="role" class="block text-sm font-medium text-gray-700 mb-2">
          New Role <span class="text-red-500">*</span>
        </label>
        <select
          id="role"
          v-model="form.role"
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          :class="{ 'border-red-500': errors.role }"
        >
          <option value="manager">Manager</option>
          <option value="contributor">Contributor</option>
          <option value="viewer">Viewer</option>
        </select>
        <p class="mt-1 text-xs text-gray-500">
          <span v-if="form.role === 'manager'">Can manage project settings, members, and all tasks</span>
          <span v-else-if="form.role === 'contributor'">Can create and edit tasks, collaborate on project</span>
          <span v-else-if="form.role === 'viewer'">Can view project details and tasks (read-only access)</span>
          <span v-else>Select a role to see permissions</span>
        </p>
        <p v-if="errors.role" class="mt-1 text-sm text-red-600">
          {{ errors.role[0] }}
        </p>
      </div>

      <!-- Error Message -->
      <div v-if="generalError" class="bg-red-50 border border-red-200 rounded-lg p-4">
        <div class="flex">
          <svg class="w-5 h-5 text-red-400 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <div>
            <h3 class="text-sm font-medium text-red-800">Error updating member</h3>
            <div class="mt-1 text-sm text-red-700">{{ generalError }}</div>
          </div>
        </div>
      </div>
    </form>

    <template #footer>
      <div class="flex justify-end space-x-3">
        <button
          type="button"
          @click="handleClose"
          class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
          :disabled="loading"
        >
          Cancel
        </button>
        <button
          type="submit"
          @click="handleSubmit"
          class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
          :disabled="loading || !form.role || form.role === member?.role"
        >
          <svg v-if="loading" class="w-4 h-4 mr-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" class="opacity-25"></circle>
            <path fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" class="opacity-75"></path>
          </svg>
          {{ loading ? 'Updating...' : 'Update Role' }}
        </button>
      </div>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, reactive, watch, inject } from 'vue'
import BaseModal from './BaseModal.vue'
import axios from "@/plugins/axiosConfig.js"

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  member: {
    type: Object,
    default: null
  },
  projectId: {
    type: [String, Number],
    required: true
  }
})

const emit = defineEmits(['close', 'updated'])

// Form data
const form = reactive({
  role: ''
})

// State
const loading = ref(false)
const errors = ref({})
const generalError = ref('')
const $toast = inject("toast");

// Watch for member changes to populate form
watch(() => props.member, (newMember) => {
  if (newMember) {
    form.role = newMember.role || ''
  }
}, { immediate: true })

// Reset form when modal opens/closes
watch(() => props.isOpen, (isOpen) => {
  if (isOpen && props.member) {
    form.role = props.member.role || ''
    errors.value = {}
    generalError.value = ''
  }
})

// Helper function to get initials
const getInitials = (user) => {
  if (!user) return 'U'
  if (user.first_name && user.last_name) {
    return `${user.first_name.charAt(0)}${user.last_name.charAt(0)}`.toUpperCase()
  } else if (user.email) {
    return user.email.charAt(0).toUpperCase()
  }
  return 'U'
}

// Handle form submission
const handleSubmit = async () => {
  if (loading.value || !props.member) return

  loading.value = true
  errors.value = {}
  generalError.value = ''

  try {
    // Validate required fields
    if (!form.role) {
      errors.value.role = ['Please select a role']
      return
    }
    
    if (form.role === props.member.role) {
      generalError.value = 'Please select a different role to update'
      return
    }

    // Prepare form data
    const formData = {
      role: form.role
    }

    const response = await axios.patch(`projects/${props.projectId}/members/${props.member.id}/`, formData)
    
    // Success - emit updated event with member data
    const updatedMember = response.data.data || response.data
    $toast.success(response.data.message || 'Project member updated successfully')
    emit('updated', updatedMember)
    
  } catch (err) {
    console.error('Failed to update project member:', err)
    console.error('Error response data:', err.response?.data)
    console.error('Error status:', err.response?.status)
    
    if (err.response?.status === 400 && err.response?.data) {
      // Handle validation errors
      const responseData = err.response.data
      
      if (responseData.data?.errors && Array.isArray(responseData.data.errors)) {
        const errorObj = {}
        responseData.data.errors.forEach(errorItem => {
          Object.keys(errorItem).forEach(field => {
            errorObj[field] = [errorItem[field]]
          })
        })
        errors.value = errorObj
      } else if (responseData.errors) {
        errors.value = responseData.errors
      } else if (responseData.message) {
        generalError.value = responseData.message
      } else {
        generalError.value = 'Validation failed. Please check your input.'
      }
    } else if (err.response?.status === 401) {
      generalError.value = 'You are not authorized to update project members'
    } else if (err.response?.status === 404) {
      generalError.value = 'Member not found'
    } else if (err.response?.data?.message) {
      generalError.value = err.response.data.message
    } else {
      generalError.value = 'Failed to update project member. Please try again.'
    }
  } finally {
    loading.value = false
  }
}

// Handle modal close
const handleClose = () => {
  if (!loading.value) {
    emit('close')
  }
}
</script>

<style scoped>
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