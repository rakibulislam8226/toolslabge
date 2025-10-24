<template>
  <BaseModal :is-open="isOpen" title="Add Project Member" size="lg" @close="handleClose">
    <form @submit.prevent="handleSubmit" class="space-y-6">
      <!-- User Selection -->
      <div>
        <label for="user" class="block text-sm font-medium text-gray-700 mb-2">
          Team Member <span class="text-red-500">*</span>
        </label>
        <div class="relative">
          <input id="user" v-model="userSearch" type="text" required
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent pr-10"
            :class="{ 'border-red-500': errors.user }" placeholder="Search for an organization member..."
            @focus="showUserDropdown = true" @input="handleUserSearch" />
          <div class="absolute inset-y-0 right-0 flex items-center pr-3">
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
            class="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-y-auto">
            <div v-if="loadingUsers" class="p-3 text-center text-gray-500">
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
            <div v-else-if="filteredUsers.length === 0" class="p-3 text-center text-gray-500">
              No members found
            </div>
            <div v-else>
              <button v-for="user in filteredUsers" :key="user.id" type="button" @click="selectUser(user)"
                class="w-full px-3 py-2 text-left hover:bg-gray-50 focus:bg-gray-50 focus:outline-none flex items-center">
                <div class="flex-1">
                  <div class="font-medium text-gray-900">
                    <span v-if="user.user.first_name && user.user.last_name">
                      {{ user.user.first_name }} {{ user.user.last_name }}
                    </span>
                    <span v-else>{{ user.user.email }}</span>
                  </div>
                  <div class="text-sm text-gray-500">{{ user.user.email }}</div>
                  <div class="text-xs text-blue-600 capitalize">{{ user.role }} in organization</div>
                </div>
              </button>
            </div>
          </div>
        </div>

        <!-- Selected User Display -->
        <div v-if="selectedUser" class="mt-2 p-2 bg-blue-50 border border-blue-200 rounded-lg">
          <div class="flex items-center justify-between">
            <div>
              <div class="font-medium text-blue-900">
                <span v-if="selectedUser.user.first_name && selectedUser.user.last_name">
                  {{ selectedUser.user.first_name }} {{ selectedUser.user.last_name }}
                </span>
                <span v-else>{{ selectedUser.user.email }}</span>
              </div>
              <div class="text-sm text-blue-700">{{ selectedUser.user.email }}</div>
              <div class="text-xs text-blue-600 capitalize">{{ selectedUser.role }} in organization</div>
            </div>
            <button type="button" @click="clearUser" class="text-blue-600 hover:text-blue-800">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
        </div>

        <p v-if="errors.user" class="mt-1 text-sm text-red-600">
          {{ errors.user[0] }}
        </p>
      </div>

      <!-- Role Selection -->
      <div>
        <label for="role" class="block text-sm font-medium text-gray-700 mb-2">
          Project Role <span class="text-red-500">*</span>
        </label>
        <select id="role" v-model="form.role" required
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          :class="{ 'border-red-500': errors.role }">
          <option value="contributor">Contributor</option>
          <option value="manager">Manager</option>
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
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <div>
            <h3 class="text-sm font-medium text-red-800">Error adding member</h3>
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
          :disabled="loading || !selectedUser || !form.role">
          <svg v-if="loading" class="w-4 h-4 mr-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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

const $toast = inject('toast')

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
  projectId: {
    type: [String, Number],
    required: true
  }
})

const emit = defineEmits(['close', 'added'])

// Form data
const form = reactive({
  user: null,
  role: ''
})

// State
const loading = ref(false)
const errors = ref({})
const generalError = ref('')

// User search state
const orgMembers = ref([])
const loadingUsers = ref(false)
const userSearch = ref('')
const selectedUser = ref(null)
const showUserDropdown = ref(false)

// Computed property for filtered users
const filteredUsers = computed(() => {
  if (!userSearch.value.trim()) {
    return orgMembers.value
  }

  const search = userSearch.value.toLowerCase()
  return orgMembers.value.filter(member => {
    const fullName = `${member.user.first_name} ${member.user.last_name}`.toLowerCase()
    const email = member.user.email.toLowerCase()
    return fullName.includes(search) || email.includes(search)
  })
})

// Reset form when modal opens/closes
watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    resetForm()
    fetchOrgMembers()
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
  form.user = null
  form.role = 'contributor'
  userSearch.value = ''
  selectedUser.value = null
  showUserDropdown.value = false
  errors.value = {}
  generalError.value = ''
}

// Fetch organization members
const fetchOrgMembers = async () => {
  try {
    loadingUsers.value = true
    const response = await axios.get('organizations/members/')
    orgMembers.value = response.data.data || []
  } catch (err) {
    console.error('Failed to fetch organization members:', err)
    generalError.value = 'Failed to load organization members'
  } finally {
    loadingUsers.value = false
  }
}

// Debounced member search
const debouncedFetchMembers = debounce(fetchOrgMembers, 300)

// Handle user search input
const handleUserSearch = () => {
  showUserDropdown.value = true
  if (orgMembers.value.length === 0 && !loadingUsers.value) {
    debouncedFetchMembers()
  }
}

// Select a user
const selectUser = (member) => {
  selectedUser.value = member
  form.user = member.user.id
  userSearch.value = member.user.first_name && member.user.last_name
    ? `${member.user.first_name} ${member.user.last_name}`
    : member.user.email
  showUserDropdown.value = false
}

// Clear selected user
const clearUser = () => {
  selectedUser.value = null
  form.user = null
  userSearch.value = ''
  showUserDropdown.value = false
}

// Handle form submission
const handleSubmit = async () => {
  if (loading.value) return

  loading.value = true
  errors.value = {}
  generalError.value = ''

  try {
    // Validate required fields
    if (!selectedUser.value) {
      errors.value.user = ['Please select a user']
      return
    }

    if (!form.role) {
      errors.value.role = ['Please select a role']
      return
    }

    // Prepare form data
    const formData = {
      user: form.user,
      role: form.role
    }

    const response = await axios.post(`projects/${props.projectId}/members/`, formData)

    // Success - emit added event with new member data
    emit('added', response.data.data || response.data)
    $toast.success(response.data.message || 'Project member added successfully')
    handleClose()

  } catch (err) {
    console.error('Failed to add project member:', err)

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
      generalError.value = 'You are not authorized to add project members'
    } else if (err.response?.data?.message) {
      generalError.value = err.response.data.message
    } else {
      generalError.value = 'Failed to add project member. Please try again.'
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