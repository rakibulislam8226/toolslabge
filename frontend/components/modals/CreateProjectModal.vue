<template>
  <BaseModal
    :is-open="isOpen"
    title="Create New Project"
    size="lg"
    @close="handleClose"
  >
    <form @submit.prevent="handleSubmit" class="space-y-6">
      <!-- Project Name -->
      <div>
        <label for="name" class="block text-sm font-medium text-gray-700 mb-2">
          Project Name <span class="text-red-500">*</span>
        </label>
        <input
          id="name"
          v-model="form.name"
          type="text"
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          :class="{ 'border-red-500': errors.name }"
          placeholder="Enter project name"
        />
        <p v-if="errors.name" class="mt-1 text-sm text-red-600">
          {{ errors.name[0] }}
        </p>
      </div>

      <!-- Project Description -->
      <div>
        <label for="description" class="block text-sm font-medium text-gray-700 mb-2">
          Description
        </label>
        <textarea
          id="description"
          v-model="form.description"
          rows="4"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          :class="{ 'border-red-500': errors.description }"
          placeholder="Describe your project (optional)"
        ></textarea>
        <p v-if="errors.description" class="mt-1 text-sm text-red-600">
          {{ errors.description[0] }}
        </p>
      </div>

      <!-- Project Dates -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label for="start_date" class="block text-sm font-medium text-gray-700 mb-2">
            Start Date
          </label>
          <input
            id="start_date"
            v-model="form.start_date"
            type="date"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            :class="{ 'border-red-500': errors.start_date }"
          />
          <p v-if="errors.start_date" class="mt-1 text-sm text-red-600">
            {{ errors.start_date[0] }}
          </p>
        </div>

        <div>
          <label for="end_date" class="block text-sm font-medium text-gray-700 mb-2">
            End Date
          </label>
          <input
            id="end_date"
            v-model="form.end_date"
            type="date"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            :class="{ 'border-red-500': errors.end_date }"
            :min="form.start_date"
          />
          <p v-if="errors.end_date" class="mt-1 text-sm text-red-600">
            {{ errors.end_date[0] }}
          </p>
        </div>
      </div>

      <!-- Project Status -->
      <div>
        <label for="status" class="block text-sm font-medium text-gray-700 mb-2">
          Status
        </label>
        <select
          id="status"
          v-model="form.status"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          :class="{ 'border-red-500': errors.status }"
        >
          <option value="active">Active</option>
          <option value="on_hold">On Hold</option>
          <option value="completed">Completed</option>
          <option value="archived">Archived</option>
        </select>
        <p v-if="errors.status" class="mt-1 text-sm text-red-600">
          {{ errors.status[0] }}
        </p>
      </div>

      <!-- Error Message -->
      <div v-if="generalError" class="bg-red-50 border border-red-200 rounded-lg p-4">
        <div class="flex">
          <svg class="w-5 h-5 text-red-400 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <div>
            <h3 class="text-sm font-medium text-red-800">Error creating project</h3>
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
          :disabled="loading"
        >
          <svg v-if="loading" class="w-4 h-4 mr-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" class="opacity-25"></circle>
            <path fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" class="opacity-75"></path>
          </svg>
          {{ loading ? 'Creating...' : 'Create Project' }}
        </button>
      </div>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import BaseModal from './BaseModal.vue'
import axios from "@/plugins/axiosConfig.js"

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'created'])

// Form data
const form = reactive({
  name: '',
  description: '',
  start_date: '',
  end_date: '',
  status: 'active',
  organization: null
})

// State
const loading = ref(false)
const errors = ref({})
const generalError = ref('')
const userOrganizations = ref([])

// Reset form when modal opens/closes
watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    resetForm()
    fetchOrganizations()
  }
})

// Reset form to initial state
const resetForm = () => {
  form.name = ''
  form.description = ''
  form.start_date = ''
  form.end_date = ''
  form.status = 'active'
  // Keep the organization auto-selected
  errors.value = {}
  generalError.value = ''
}

// Fetch user's organizations and auto-select
const fetchOrganizations = async () => {
  try {
    const response = await axios.get('users/my-info/')
    const userInfo = response.data.data || response.data
    const organizations = userInfo.organizations || []
    
    // Transform and store organizations data
    userOrganizations.value = organizations.map(org => ({
      id: org.organization_id,
      name: org.organization_name,
      slug: org.organization_slug
    }))
    
    // Auto-select the first organization (or the only one)
    if (userOrganizations.value.length > 0) {
      form.organization = userOrganizations.value[0].id
    }
  } catch (err) {
    console.error('Failed to fetch organizations:', err)
    generalError.value = 'Failed to load organization information'
  }
}

// Handle form submission
const handleSubmit = async () => {
  if (loading.value) return

  loading.value = true
  errors.value = {}
  generalError.value = ''

  try {
    // Prepare form data
    const formData = {
      name: form.name.trim(),
      description: form.description.trim() || null,
      start_date: form.start_date || null,
      end_date: form.end_date || null,
      status: form.status,
      organization: form.organization
    }

    // Remove empty fields
    Object.keys(formData).forEach(key => {
      if (formData[key] === '' || formData[key] === null) {
        delete formData[key]
      }
    })

    const response = await axios.post('projects/', formData)
    
    // Success - emit created event with new project data
    emit('created', response.data.data || response.data)
    handleClose()
    
  } catch (err) {
    console.error('Failed to create project:', err)
    
    if (err.response?.status === 400 && err.response?.data) {
      // Handle validation errors based on your API response structure
      const responseData = err.response.data
      
      if (responseData.data?.errors && Array.isArray(responseData.data.errors)) {
        // Handle the specific API response structure with errors array
        const errorObj = {}
        responseData.data.errors.forEach(errorItem => {
          Object.keys(errorItem).forEach(field => {
            errorObj[field] = [errorItem[field]]
          })
        })
        errors.value = errorObj
      } else if (responseData.errors) {
        // Handle direct errors object
        errors.value = responseData.errors
      } else if (responseData.message) {
        generalError.value = responseData.message
      } else {
        generalError.value = 'Validation failed. Please check your input.'
      }
    } else if (err.response?.status === 401) {
      generalError.value = 'You are not authorized to create projects'
    } else if (err.response?.data?.message) {
      generalError.value = err.response.data.message
    } else {
      generalError.value = 'Failed to create project. Please try again.'
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