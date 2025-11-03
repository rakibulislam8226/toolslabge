<template>
  <BaseModal :is-open="isOpen" title="Add Project Member" size="xl" @close="handleClose">
    <form @submit.prevent="handleSubmit" class="space-y-6">
      <!-- User Selection -->
      <div>
        <label for="user" class="block text-base font-medium text-gray-700 mb-3">
          Team Member <span class="text-red-500">*</span>
        </label>
        <div class="relative">
          <BaseInput v-model="userSearch" placeholder="Search for an organization member..." required
            :error="fieldErrors.user" @focus="showUserDropdown = true" @input="handleUserSearch" />
          <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
            <svg v-if="loadingUsers" class="w-4 h-4 animate-spin text-gray-400" fill="none" stroke="currentColor"
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

          <!-- User Dropdown -->
          <div v-if="showUserDropdown && (filteredUsers.length > 0 || userSearch.length > 0)"
            class="absolute z-10 w-full mt-1 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg shadow-lg max-h-60 overflow-y-auto">
            <div v-if="loadingUsers" class="p-3 text-center text-gray-500 dark:text-gray-400">
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
            <div v-else-if="filteredUsers.length === 0" class="p-3 text-center text-gray-500 dark:text-gray-400">
              No members found
            </div>
            <div v-else>
              <button v-for="user in filteredUsers" :key="user.id" type="button" @click="selectUser(user)"
                class="w-full px-3 py-2 text-left hover:bg-blue-50 dark:hover:bg-blue-900/20 hover:border-l-4 hover:border-blue-500 dark:hover:border-blue-400 focus:bg-blue-50 dark:focus:bg-blue-900/20 focus:border-l-4 focus:border-blue-500 dark:focus:border-blue-400 focus:outline-none flex items-center cursor-pointer transition-all duration-200 ease-in-out">
                <div class="flex-1">
                  <div
                    class="font-medium text-gray-900 dark:text-gray-100 hover:text-blue-900 dark:hover:text-blue-300 transition-colors duration-200 text-base">
                    <span v-if="user.user.first_name && user.user.last_name">
                      {{ user.user.first_name }} {{ user.user.last_name }}
                    </span>
                    <span v-else>{{ user.user.email }}</span>
                  </div>
                  <div class="text-sm text-gray-500 dark:text-gray-400">{{ user.user.email }}</div>
                  <div class="text-sm text-blue-600 dark:text-blue-400 capitalize">{{ user.role }} in organization</div>
                </div>
              </button>
            </div>
          </div>
        </div>

        <!-- Selected User Display -->
        <div v-if="selectedUser"
          class="mt-3 p-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-700 rounded-lg">
          <div class="flex items-center justify-between">
            <div>
              <div class="font-medium text-blue-900 dark:text-blue-300 text-base">
                <span v-if="selectedUser.user.first_name && selectedUser.user.last_name">
                  {{ selectedUser.user.first_name }} {{ selectedUser.user.last_name }}
                </span>
                <span v-else>{{ selectedUser.user.email }}</span>
              </div>
              <div class="text-sm text-blue-700 dark:text-blue-400">{{ selectedUser.user.email }}</div>
              <div class="text-sm text-blue-600 dark:text-blue-400 capitalize">{{ selectedUser.role }} in organization
              </div>
            </div>
            <button type="button" @click="clearUser"
              class="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 transition-colors duration-200">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Role Selection -->
      <div>
        <BaseSelect v-model="form.role" label="Project Role" :options="roleOptions" required
          :error="fieldErrors.role" />
        <p class="mt-2 text-sm text-gray-500">
          <span v-if="form.role === 'manager'">Can manage project settings, members, and all tasks</span>
          <span v-else-if="form.role === 'contributor'">Can create and edit tasks, collaborate on project</span>
          <span v-else-if="form.role === 'viewer'">Can view project details and tasks (read-only access)</span>
          <span v-else>Select a role to see permissions</span>
        </p>
      </div>

    </form>

    <template #footer>
      <div class="flex justify-end space-x-3">
        <button type="button" @click="handleClose"
          class="px-5 py-3 text-base font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
          :disabled="loading">
          Cancel
        </button>
        <button type="submit" @click="handleSubmit"
          class="px-5 py-3 text-base font-medium text-white bg-blue-600 border border-transparent rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed flex items-center cursor-pointer"
          :disabled="loading || !selectedUser || !form.role">
          <svg v-if="loading" class="w-5 h-5 mr-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" class="opacity-25"></circle>
            <path fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              class="opacity-75"></path>
          </svg>
          {{ loading ? 'Adding...' : 'Add Member' }}
        </button>
      </div>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, reactive, watch, computed, inject } from 'vue'
import BaseModal from './BaseModal.vue'
import axios from "@/plugins/axiosConfig.js"
import { BaseInput, BaseSelect } from '@/components/forms'

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
  },
  projectSlug: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['close', 'added'])
const $toast = inject("toast")

// Role options
const roleOptions = [
  { value: 'contributor', label: 'Contributor' },
  { value: 'manager', label: 'Manager' },
  { value: 'viewer', label: 'Viewer' }
]

// Form data
const form = reactive({
  user_id: null,
  role: 'contributor'
})

// State
const loading = ref(false)
const fieldErrors = ref({})

// User search state
const organizationUsers = ref([])
const loadingUsers = ref(false)
const userSearch = ref('')
const selectedUser = ref(null)
const showUserDropdown = ref(false)

// Computed property for filtered users
const filteredUsers = computed(() => {
  if (!userSearch.value.trim()) {
    return organizationUsers.value
  }

  const search = userSearch.value.toLowerCase()
  return organizationUsers.value.filter(user => {
    const fullName = user.user.first_name && user.user.last_name
      ? `${user.user.first_name} ${user.user.last_name}`.toLowerCase()
      : ''
    const email = user.user.email.toLowerCase()
    return fullName.includes(search) || email.includes(search)
  })
})

// Reset form when modal opens/closes
watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    resetForm()
    fetchOrganizationUsers()
  }
})

// Close dropdown when clicking outside
watch(() => showUserDropdown.value, (isOpen) => {
  if (isOpen) {
    const handleClickOutside = (event) => {
      const dropdown = event.target.closest('.relative')
      if (!dropdown) {
        showUserDropdown.value = false
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
  form.user_id = null
  form.role = 'contributor'
  userSearch.value = ''
  selectedUser.value = null
  showUserDropdown.value = false
  fieldErrors.value = {}
}

// Fetch organization users
const fetchOrganizationUsers = async () => {
  try {
    loadingUsers.value = true
    const response = await axios.get('organizations/members/')
    organizationUsers.value = response.data.data || []
  } catch (err) {
    organizationUsers.value = []
  } finally {
    loadingUsers.value = false
  }
}

// Debounced user search
const debouncedFetchUsers = debounce(fetchOrganizationUsers, 300)

// Handle user search input
const handleUserSearch = () => {
  showUserDropdown.value = true
  if (organizationUsers.value.length === 0 && !loadingUsers.value) {
    debouncedFetchUsers()
  }
}

// Select a user
const selectUser = (user) => {
  console.log('Selecting user:', user)
  selectedUser.value = user
  form.user_id = user.user.id
  console.log('Set form.user_id to:', form.user_id)
  userSearch.value = user.user.first_name && user.user.last_name
    ? `${user.user.first_name} ${user.user.last_name}`
    : user.user.email
  showUserDropdown.value = false
}

// Clear selected user
const clearUser = () => {
  selectedUser.value = null
  form.user_id = null
  userSearch.value = ''
  showUserDropdown.value = false
}

// Handle form submission
const handleSubmit = async () => {
  if (loading.value) return

  loading.value = true
  fieldErrors.value = {}

  try {
    if (!selectedUser.value) {
      fieldErrors.value.user = 'Please select a team member'
      return
    }

    if (!form.user_id) {
      fieldErrors.value.user = 'User ID is missing'
      console.error('form.user_id is null or undefined:', form.user_id)
      return
    }

    const formData = {
      user: form.user_id,
      role: form.role
    }

    console.log('Sending formData:', formData)
    console.log('Selected user:', selectedUser.value)

    const response = await axios.post(`projects/${props.projectSlug}/members/`, formData)
    const newMember = response.data.data || response.data

    $toast?.success('Member added successfully')
    emit('added', newMember)
    handleClose()
  } catch (err) {
    const responseData = err.response?.data

    if (responseData?.message) {
      $toast?.error(responseData.message)
    }

    if (responseData?.data?.errors && Array.isArray(responseData.data.errors)) {
      responseData.data.errors.forEach(errorItem => {
        Object.assign(fieldErrors.value, errorItem)
      })
    } else if (responseData?.errors) {
      Object.assign(fieldErrors.value, responseData.errors)
    } else if (!responseData?.message) {
      $toast?.error('Failed to add member')
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