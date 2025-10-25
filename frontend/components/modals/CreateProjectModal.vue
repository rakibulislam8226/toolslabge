<template>
  <BaseModal :is-open="isOpen" title="Create New Project" size="xxl" @close="handleClose">
    <form @submit.prevent="handleSubmit" class="space-y-6">
      <!-- Project Name -->
      <BaseInput v-model="form.name" label="Project Name" placeholder="Enter project name" required
        :error="fieldErrors.name" />

      <!-- Project Description -->
      <BaseTextarea v-model="form.description" label="Description" placeholder="Describe your project (optional)"
        :rows="4" :error="fieldErrors.description" />

      <!-- Project Dates -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <BaseDatePicker v-model="form.start_date" label="Start Date" placeholder="Select start date"
          :enable-time="false" date-format="Y-m-d" alt-format="F j, Y" :error="fieldErrors.start_date" />

        <BaseDatePicker v-model="form.end_date" label="End Date" placeholder="Select end date" :enable-time="false"
          date-format="Y-m-d" alt-format="F j, Y" :error="fieldErrors.end_date" />
      </div>

      <!-- Project Manager -->
      <div>
        <label for="manager" class="block text-sm font-medium text-gray-700 mb-2">
          Project Manager
        </label>
        <div class="relative">
          <BaseInput v-model="managerSearch" placeholder="Search for a team member..." :error="fieldErrors.manager_id"
            @focus="showManagerDropdown = true" @input="handleManagerSearch" />
          <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
            <svg v-if="loadingMembers" class="w-4 h-4 animate-spin text-gray-400" fill="none" stroke="currentColor"
              viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" class="opacity-25"></circle>
              <path fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                class="opacity-75"></path>
            </svg>
            <svg v-else class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
          </div>

          <!-- Manager Dropdown -->
          <div v-if="showManagerDropdown && (filteredMembers.length > 0 || managerSearch.length > 0)"
            class="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-y-auto">
            <div v-if="loadingMembers" class="p-3 text-center text-gray-500">
              <div class="flex items-center justify-center">
                <svg class="w-4 h-4 animate-spin mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" class="opacity-25"></circle>
                  <path fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    class="opacity-75"></path>
                </svg>
                Loading members...
              </div>
            </div>
            <div v-else-if="filteredMembers.length === 0" class="p-3 text-center text-gray-500">
              No members found
            </div>
            <div v-else>
              <button v-for="member in filteredMembers" :key="member.id" type="button" @click="selectManager(member)"
                class="w-full px-3 py-2 text-left hover:bg-gray-50 focus:bg-gray-50 focus:outline-none flex items-center">
                <div class="flex-1">
                  <div class="font-medium text-gray-900">
                    {{ member.user.first_name }} {{ member.user.last_name }}
                  </div>
                  <div class="text-sm text-gray-500">{{ member.user.email }}</div>
                  <div class="text-xs text-blue-600 capitalize">{{ member.role }}</div>
                </div>
              </button>
            </div>
          </div>
        </div>

        <!-- Selected Manager Display -->
        <div v-if="selectedManager" class="mt-2 p-2 bg-blue-50 border border-blue-200 rounded-lg">
          <div class="flex items-center justify-between">
            <div>
              <div class="font-medium text-blue-900">
                {{ selectedManager.user.first_name }} {{ selectedManager.user.last_name }}
              </div>
              <div class="text-sm text-blue-700">{{ selectedManager.user.email }}</div>
              <div class="text-xs text-blue-600 capitalize">{{ selectedManager.role }}</div>
            </div>
            <button type="button" @click="clearManager" class="text-blue-600 hover:text-blue-800">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Project Status -->
      <BaseSelect v-model="form.status" label="Status" :options="statusOptions" :error="fieldErrors.status" />

      <!-- Error Message -->
      <div v-if="generalError" class="bg-red-50 border border-red-200 rounded-lg p-4">
        <div class="flex">
          <svg class="w-5 h-5 text-red-400 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
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
        <button type="button" @click="handleClose"
          class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
          :disabled="loading">
          Cancel
        </button>
        <button type="submit" @click="handleSubmit"
          class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
          :disabled="loading">
          <svg v-if="loading" class="w-4 h-4 mr-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" class="opacity-25"></circle>
            <path fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              class="opacity-75"></path>
          </svg>
          {{ loading ? 'Creating...' : 'Create Project' }}
        </button>
      </div>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, reactive, watch, computed, inject } from 'vue'
import BaseModal from './BaseModal.vue'
import axios from "@/plugins/axiosConfig.js"
import { BaseInput, BaseTextarea, BaseSelect, BaseDatePicker } from '@/components/forms'

// Debounce utility function
function debounce(func, wait) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'created'])
const $toast = inject("toast")

// Status options
const statusOptions = [
  { value: 'active', label: 'Active' },
  { value: 'on_hold', label: 'On Hold' },
  { value: 'completed', label: 'Completed' },
  { value: 'archived', label: 'Archived' }
]

// Form data
const form = reactive({
  name: '',
  description: '',
  start_date: '',
  end_date: '',
  status: 'active',
  manager_id: null
})

// State
const loading = ref(false)
const fieldErrors = ref({})
const generalError = ref('')

// Manager search state
const members = ref([])
const loadingMembers = ref(false)
const managerSearch = ref('')
const selectedManager = ref(null)
const showManagerDropdown = ref(false)

// Computed property for filtered members
const filteredMembers = computed(() => {
  if (!managerSearch.value.trim()) {
    return members.value
  }

  const search = managerSearch.value.toLowerCase()
  return members.value.filter(member => {
    const fullName = `${member.user.first_name} ${member.user.last_name}`.toLowerCase()
    const email = member.user.email.toLowerCase()
    return fullName.includes(search) || email.includes(search)
  })
})

// Reset form when modal opens/closes
watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    resetForm()
    fetchMembers()
  }
})

// Close dropdown when clicking outside
watch(() => showManagerDropdown.value, (isOpen) => {
  if (isOpen) {
    // Add click outside listener
    const handleClickOutside = (event) => {
      const dropdown = event.target.closest('.relative')
      if (!dropdown) {
        showManagerDropdown.value = false
        document.removeEventListener('click', handleClickOutside)
      }
    }

    setTimeout(() => {
      document.addEventListener('click', handleClickOutside)
    }, 100)
  }
})

// Reset form to initial state
const resetForm = () => {
  form.name = ''
  form.description = ''
  form.start_date = ''
  form.end_date = ''
  form.status = 'active'
  form.manager_id = null
  managerSearch.value = ''
  selectedManager.value = null
  showManagerDropdown.value = false
  fieldErrors.value = {}
  generalError.value = ''
}

// Fetch organization members
const fetchMembers = async () => {
  try {
    loadingMembers.value = true
    const response = await axios.get('organizations/members/')
    members.value = response.data.data || []
  } catch (err) {
    members.value = []
  } finally {
    loadingMembers.value = false
  }
}

// Debounced member search
const debouncedFetchMembers = debounce(fetchMembers, 300)

// Handle manager search input
const handleManagerSearch = () => {
  showManagerDropdown.value = true
  if (members.value.length === 0 && !loadingMembers.value) {
    debouncedFetchMembers()
  }
}

// Select a manager
const selectManager = (member) => {
  selectedManager.value = member
  form.manager_id = member.id
  managerSearch.value = `${member.user.first_name} ${member.user.last_name}`
  showManagerDropdown.value = false
}

// Clear selected manager
const clearManager = () => {
  selectedManager.value = null
  form.manager_id = null
  managerSearch.value = ''
  showManagerDropdown.value = false
}

// Handle form submission
const handleSubmit = async () => {
  if (loading.value) return

  loading.value = true
  fieldErrors.value = {}
  generalError.value = ''

  try {
    const formData = {
      name: form.name.trim(),
      description: form.description.trim() || null,
      start_date: form.start_date || null,
      end_date: form.end_date || null,
      status: form.status,
      manager_id: form.manager_id
    }

    // Remove empty fields
    Object.keys(formData).forEach(key => {
      if (formData[key] === '' || formData[key] === null) {
        delete formData[key]
      }
    })

    const response = await axios.post('projects/', formData)
    const newProject = response.data.data || response.data

    $toast?.success('Project created successfully')
    emit('created', newProject)
    handleClose()
  } catch (err) {
    const responseData = err.response?.data

    if (responseData?.message) {
      $toast?.error(responseData.message)
      generalError.value = responseData.message
    }

    if (responseData?.data?.errors && Array.isArray(responseData.data.errors)) {
      responseData.data.errors.forEach(errorItem => {
        Object.assign(fieldErrors.value, errorItem)
      })
    } else if (responseData?.errors) {
      Object.assign(fieldErrors.value, responseData.errors)
    } else if (!responseData?.message) {
      generalError.value = 'Failed to create project. Please try again.'
      $toast?.error('Failed to create project')
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