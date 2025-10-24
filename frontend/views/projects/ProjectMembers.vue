<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-24">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      <span class="ml-3 text-gray-600">Loading project members...</span>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
      <div class="bg-red-50 border border-red-200 rounded-lg p-4 sm:p-6 text-center">
        <svg class="w-10 h-10 sm:w-12 sm:h-12 text-red-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <h3 class="text-base sm:text-lg font-semibold text-red-800 mb-2">Failed to load project members</h3>
        <p class="text-sm sm:text-base text-red-600 mb-4">{{ error }}</p>
        <div class="flex flex-col sm:flex-row items-center justify-center space-y-2 sm:space-y-0 sm:space-x-3">
          <button
            @click="fetchMembers"
            class="w-full sm:w-auto bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition duration-300 text-sm sm:text-base"
          >
            Try Again
          </button>
          <button
            @click="goBack"
            class="w-full sm:w-auto bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition duration-300 text-sm sm:text-base"
          >
            Back to Project
          </button>
        </div>
      </div>
    </div>

    <!-- Project Members Content -->
    <div v-else class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
      <!-- Header Section -->
      <div class="bg-white rounded-lg shadow-sm border mb-6 md:mb-8">
        <div class="px-4 sm:px-6 py-4 sm:py-6 border-b border-gray-200">
          <div class="space-y-4 lg:space-y-0 lg:flex lg:items-start lg:justify-between">
            <div class="flex-1">
              <!-- Breadcrumb -->
              <nav class="mb-4">
                <ol class="flex flex-wrap items-center space-x-1 sm:space-x-2 text-xs sm:text-sm text-gray-500">
                  <li>
                    <router-link to="/projects" class="hover:text-blue-600 transition duration-300">
                      Projects
                    </router-link>
                  </li>
                  <li>
                    <svg class="w-3 h-3 sm:w-4 sm:h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                    </svg>
                  </li>
                  <li>
                    <button @click="goBack" class="hover:text-blue-600 transition duration-300 truncate max-w-[120px] sm:max-w-none">
                      {{ projectName }}
                    </button>
                  </li>
                  <li>
                    <svg class="w-3 h-3 sm:w-4 sm:h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                    </svg>
                  </li>
                  <li class="text-gray-900 font-medium">Members</li>
                </ol>
              </nav>

              <!-- Page Title -->
              <div class="mb-4">
                <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 mb-2 lg:mb-0">Project Members</h1>
                <span class="text-sm sm:text-lg text-gray-600 block lg:inline">{{ projectName }}</span>
              </div>

              <p class="text-sm sm:text-base text-gray-600">
                Manage project team members and their roles
              </p>
            </div>

            <!-- Action Buttons -->
            <div class="flex items-center justify-end lg:ml-6">
              <button
                @click="showAddMemberModal = true"
                class="bg-blue-600 text-white px-3 sm:px-4 py-2 rounded-lg hover:bg-blue-700 transition duration-300 flex items-center text-sm sm:text-base"
              >
                <svg class="w-4 h-4 mr-1 sm:mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                </svg>
                <span class="hidden sm:inline">Add Member</span>
                <span class="sm:hidden">Add</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Members Stats -->
        <div class="px-4 sm:px-6 py-4 sm:py-6">
          <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
            <div class="text-center">
              <div class="w-10 h-10 sm:w-12 sm:h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-2">
                <svg class="w-5 h-5 sm:w-6 sm:h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-2.239"></path>
                </svg>
              </div>
              <p class="text-xl sm:text-2xl font-bold text-gray-900">{{ members.length }}</p>
              <p class="text-xs sm:text-sm text-gray-600">Total Members</p>
            </div>

            <div class="text-center">
              <div class="w-10 h-10 sm:w-12 sm:h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-2">
                <svg class="w-5 h-5 sm:w-6 sm:h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.25-4.5v16.5h-16.5V7.5"></path>
                </svg>
              </div>
              <p class="text-xl sm:text-2xl font-bold text-gray-900">{{ getManagersCount() }}</p>
              <p class="text-xs sm:text-sm text-gray-600">Managers</p>
            </div>

            <div class="text-center">
              <div class="w-10 h-10 sm:w-12 sm:h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-2">
                <svg class="w-5 h-5 sm:w-6 sm:h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
              </div>
              <p class="text-xl sm:text-2xl font-bold text-gray-900">{{ getContributorsCount() }}</p>
              <p class="text-xs sm:text-sm text-gray-600">Contributors</p>
            </div>

            <div class="text-center">
              <div class="w-10 h-10 sm:w-12 sm:h-12 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-2">
                <svg class="w-5 h-5 sm:w-6 sm:h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                </svg>
              </div>
              <p class="text-xl sm:text-2xl font-bold text-gray-900">{{ getViewersCount() }}</p>
              <p class="text-xs sm:text-sm text-gray-600">Viewers</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Members List -->
      <div class="bg-white rounded-lg shadow-sm border">
        <div class="px-4 sm:px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg sm:text-xl font-semibold text-gray-900">Team Members</h2>
        </div>

        <div v-if="members.length === 0" class="text-center py-8 sm:py-12 px-4">
          <svg class="w-12 h-12 sm:w-16 sm:h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-2.239"></path>
          </svg>
          <h3 class="text-lg sm:text-xl font-semibold text-gray-900 mb-2">No members yet</h3>
          <p class="text-sm sm:text-base text-gray-600 mb-6 max-w-sm mx-auto">Add team members to start collaborating on this project</p>
          <button
            @click="showAddMemberModal = true"
            class="bg-blue-600 text-white px-4 sm:px-6 py-2 sm:py-3 rounded-lg font-semibold hover:bg-blue-700 transition duration-300 inline-flex items-center text-sm sm:text-base"
          >
            <svg class="w-4 h-4 sm:w-5 sm:h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
            </svg>
            Add First Member
          </button>
        </div>

        <div v-else class="divide-y divide-gray-200">
          <div
            v-for="member in members"
            :key="member.id"
            class="px-4 sm:px-6 py-4 hover:bg-gray-50 transition duration-300"
          >
            <div class="flex flex-col sm:flex-row sm:items-center justify-between space-y-3 sm:space-y-0">
              <div class="flex items-center min-w-0 flex-1">
                <!-- Avatar -->
                <div class="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white font-semibold mr-3 flex-shrink-0">
                  {{ getInitials(member.user) }}
                </div>

                <!-- User Info -->
                <div class="min-w-0 flex-1">
                  <div class="font-medium text-gray-900 text-sm sm:text-base truncate">
                    <span v-if="member.user_name">
                      {{ member.user_name }}
                    </span>
                    <span v-else>{{ member.user_email }}</span>
                  </div>
                  <div class="text-xs sm:text-sm text-gray-500 truncate">{{ member.user_email }}</div>
                  <div class="text-xs text-gray-400">
                    Joined {{ formatDate(member.created_at) }}
                  </div>
                </div>
              </div>

              <!-- Role and Actions -->
              <div class="flex items-center justify-between sm:justify-end space-x-3 flex-shrink-0">
                <span 
                  :class="getRoleBadgeClass(member.role)"
                  class="px-2 py-1 text-xs font-medium rounded-full"
                >
                  {{ formatRole(member.role) }}
                </span>

                <div class="flex items-center space-x-1">
                  <button
                    @click="editMember(member)"
                    class="text-blue-600 hover:text-blue-800 p-1 rounded"
                    title="Edit role"
                  >
                    <svg class="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                    </svg>
                  </button>
                  <button
                    @click="removeMember(member)"
                    class="text-red-600 hover:text-red-800 p-1 rounded"
                    title="Remove member"
                  >
                    <svg class="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Member Modal -->
    <AddProjectMemberModal
      :is-open="showAddMemberModal"
      :project-id="projectId"
      @close="closeAddMemberModal"
      @added="onMemberAdded"
    />

    <!-- Edit Member Modal -->
    <EditProjectMemberModal
      v-if="editingMember"
      :is-open="showEditMemberModal"
      :member="editingMember"
      :project-id="projectId"
      @close="showEditMemberModal = false"
      @updated="handleMemberUpdated"
    />

    <!-- Remove Member Confirmation Modal -->
    <ConfirmModal
      :is-open="showRemoveModal"
      title="Remove Member"
      :message="`Are you sure you want to remove ${removingMember?.user_name ? removingMember.user_name : removingMember?.user_email} from this project?`"
      confirm-text="Remove"
      confirm-class="bg-red-600 hover:bg-red-700 focus:ring-red-500"
      @confirm="confirmRemoveMember"
      @cancel="showRemoveModal = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from "@/plugins/axiosConfig.js"
import { extractIdFromSlug } from "@/utils/slugUtils.js"
import AddProjectMemberModal from '@/components/modals/AddProjectMemberModal.vue'
import EditProjectMemberModal from '@/components/modals/EditProjectMemberModal.vue'
import ConfirmModal from '@/components/modals/ConfirmModal.vue'

const router = useRouter()
const route = useRoute()

// Reactive data
const members = ref([])
const loading = ref(true)
const error = ref('')
const showAddMemberModal = ref(false)
const projectName = ref('')

// Get project slug from route
const projectSlug = computed(() => route.params.slug)

// Extract project ID from slug for API calls
const projectId = computed(() => {
  const slug = projectSlug.value
  return extractIdFromSlug(slug)
})

// Fetch project members from API
const fetchMembers = async () => {
  try {
    loading.value = true
    error.value = ''
    
    const id = projectId.value
    if (!id) {
      error.value = 'Invalid project URL - could not extract project ID'
      return
    }
    
    const response = await axios.get(`projects/${id}/members/`)
    members.value = response.data.data || response.data || []

    // Also fetch project name for breadcrumb
    try {
      const projectResponse = await axios.get(`projects/${id}/`)
      const projectData = projectResponse.data.data || projectResponse.data
      projectName.value = projectData.name || 'Unknown Project'
    } catch (err) {
      console.error('Failed to fetch project name:', err)
      projectName.value = 'Project'
    }

  } catch (err) {
    console.error('Failed to fetch project members:', err)
    if (err.response?.status === 404) {
      error.value = 'Project not found'
    } else if (err.response?.status === 401) {
      error.value = 'You need to login to view project members'
    } else if (err.response?.data?.detail) {
      error.value = err.response.data.detail
    } else {
      error.value = 'Failed to load project members. Please try again.'
    }
  } finally {
    loading.value = false
  }
}

// Helper functions
const getInitials = (user) => {
  if (user.first_name && user.last_name) {
    return `${user.first_name.charAt(0)}${user.last_name.charAt(0)}`.toUpperCase()
  } else if (user.email) {
    return user.email.charAt(0).toUpperCase()
  }
  return 'U'
}

const formatRole = (role) => {
  if (!role) return 'Member'
  return role.charAt(0).toUpperCase() + role.slice(1).replace('_', ' ')
}

const getRoleBadgeClass = (role) => {
  const roleLower = (role || 'contributor').toLowerCase()
  
  switch (roleLower) {
    case 'manager':
      return 'bg-purple-100 text-purple-800'
    case 'contributor':
      return 'bg-blue-100 text-blue-800'
    case 'viewer':
      return 'bg-gray-100 text-gray-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  })
}

// Statistics
const getManagersCount = () => {
  return members.value.filter(member => member.role?.toLowerCase() === 'manager').length
}

const getContributorsCount = () => {
  return members.value.filter(member => member.role?.toLowerCase() === 'contributor').length
}

const getViewersCount = () => {
  return members.value.filter(member => member.role?.toLowerCase() === 'viewer').length
}

// Modal functions
const closeAddMemberModal = () => {
  showAddMemberModal.value = false
}

const onMemberAdded = (newMember) => {
  members.value.push(newMember)
  showAddMemberModal.value = false
}

// Action functions
const goBack = () => {
  const slug = projectSlug.value
  router.push(`/projects/${slug}`)
}

const editMember = (member) => {
  editingMember.value = { ...member }
  showEditMemberModal.value = true
}

const removeMember = (member) => {
  removingMember.value = member
  showRemoveModal.value = true
}

// Additional modal states for edit and remove
const showEditMemberModal = ref(false)
const showRemoveModal = ref(false)
const editingMember = ref(null)
const removingMember = ref(null)

// Handle member updated
const handleMemberUpdated = (updatedMember) => {
  const index = members.value.findIndex(m => m.id === updatedMember.id)
  if (index !== -1) {
    members.value[index] = updatedMember
  }
  showEditMemberModal.value = false
  editingMember.value = null
}

// Confirm member removal
const confirmRemoveMember = async () => {
  if (!removingMember.value) return
  
  try {
    await axios.delete(`projects/${projectId.value}/members/${removingMember.value.id}/`)
    
    // Remove from local state
    members.value = members.value.filter(m => m.id !== removingMember.value.id)
    
    showRemoveModal.value = false
    removingMember.value = null
    
  } catch (err) {
    console.error('Failed to remove member:', err)
    error.value = 'Failed to remove member'
  }
}

// Fetch members on component mount
onMounted(() => {
  fetchMembers()
})
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