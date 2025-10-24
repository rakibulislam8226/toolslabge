<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-24">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      <span class="ml-3 text-gray-600">Loading project details...</span>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
        <svg class="w-12 h-12 text-red-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <h3 class="text-lg font-semibold text-red-800 mb-2">Failed to load project</h3>
        <p class="text-red-600 mb-4">{{ error }}</p>
        <div class="space-x-3">
          <button
            @click="fetchProject"
            class="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition duration-300"
          >
            Try Again
          </button>
          <router-link
            to="/projects"
            class="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition duration-300 inline-block"
          >
            Back to Projects
          </router-link>
        </div>
      </div>
    </div>

    <!-- Project Details Content -->
    <div v-else-if="project" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header Section -->
      <div class="bg-white rounded-lg shadow-sm border mb-8">
        <div class="px-6 py-6 border-b border-gray-200">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <!-- Breadcrumb -->
              <nav class="mb-4">
                <ol class="flex items-center space-x-2 text-sm text-gray-500">
                  <li>
                    <router-link to="/projects" class="hover:text-blue-600 transition duration-300">
                      Projects
                    </router-link>
                  </li>
                  <li>
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                    </svg>
                  </li>
                  <li class="text-gray-900 font-medium">{{ project.name }}</li>
                </ol>
              </nav>

              <!-- Project Title and Status -->
              <div class="flex items-center mb-4">
                <h1 class="text-3xl font-bold text-gray-900 mr-4">{{ project.name }}</h1>
                <span 
                  :class="getStatusBadgeClass(project.status)"
                  class="px-3 py-1 text-sm font-medium rounded-full"
                >
                  {{ formatStatus(project.status) }}
                </span>
              </div>

              <!-- Project Description -->
              <p class="text-gray-600 text-lg leading-relaxed">
                {{ project.description || 'No description available for this project.' }}
              </p>
            </div>

            <!-- Action Buttons -->
            <div class="flex items-center space-x-3 ml-6">
              <button
                @click="editProject"
                class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition duration-300 flex items-center"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                </svg>
                Edit Project
              </button>
              <!-- <button
                @click="showDeleteModal = true"
                class="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition duration-300 flex items-center"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                </svg>
                Delete
              </button> -->
            </div>
          </div>
        </div>

        <!-- Project Stats -->
        <div class="px-6 py-6">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
            <!-- Tasks -->
            <div class="text-center">
              <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-2">
                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <p class="text-2xl font-bold text-gray-900">{{ getStaticTasksCount(project) }}</p>
              <p class="text-sm text-gray-600">Tasks</p>
            </div>

            <!-- Members -->
            <div class="text-center">
              <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-2">
                <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-2.239"></path>
                </svg>
              </div>
              <p class="text-2xl font-bold text-gray-900">{{ getStaticMembersCount(project) }}</p>
              <p class="text-sm text-gray-600">Members</p>
            </div>

            <!-- Progress -->
            <div class="text-center">
              <div class="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-2">
                <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                </svg>
              </div>
              <p class="text-2xl font-bold text-gray-900">{{ getStaticProgress(project) }}%</p>
              <p class="text-sm text-gray-600">Complete</p>
            </div>

            <!-- Status Days -->
            <div class="text-center">
              <div class="w-12 h-12 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-2">
                <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <p class="text-2xl font-bold text-gray-900">{{ getDaysRemaining() }}</p>
              <p class="text-sm text-gray-600">{{ getDaysLabel() }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Project Dates and Details -->
      <div class="grid md:grid-cols-2 gap-8 mb-8">
        <!-- Project Timeline -->
        <div class="bg-white rounded-lg shadow-sm border p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-4 flex items-center">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
            </svg>
            Project Timeline
          </h2>
          
          <div class="space-y-4">
            <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span class="text-gray-600">Start Date</span>
              <span class="font-medium text-gray-900">
                {{ project.start_date ? formatDate(project.start_date) : 'Not set' }}
              </span>
            </div>
            
            <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span class="text-gray-600">End Date</span>
              <span class="font-medium text-gray-900">
                {{ project.end_date ? formatDate(project.end_date) : 'Not set' }}
              </span>
            </div>

            <!-- Progress Bar -->
            <div class="mt-6">
              <div class="flex justify-between text-sm text-gray-600 mb-2">
                <span>Overall Progress</span>
                <span>{{ getStaticProgress(project) }}%</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-3">
                <div 
                  class="bg-gradient-to-r from-blue-500 to-blue-600 h-3 rounded-full transition-all duration-500"
                  :style="{ width: `${getStaticProgress(project)}%` }"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Project Information -->
        <div class="bg-white rounded-lg shadow-sm border p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-4 flex items-center">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            Project Information
          </h2>
          
          <div class="space-y-4">
            <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span class="text-gray-600">Project Manager</span>
              <span class="font-medium text-gray-900">
                <template v-if="project?.manager">
                  <span v-if="project.manager.first_name && project.manager.last_name">
                    {{ project.manager.first_name }} {{ project.manager.last_name }}
                  </span>
                  <span v-else>
                    {{ project.manager.email }}
                  </span>
                </template>
                <span v-else class="text-gray-500 italic">No manager assigned</span>
              </span>
            </div>
            
            <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span class="text-gray-600">Status</span>
              <span 
                :class="getStatusBadgeClass(project.status)"
                class="px-2 py-1 text-xs font-medium rounded-full"
              >
                {{ formatStatus(project.status) }}
              </span>
            </div>
            
            <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span class="text-gray-600">Created</span>
              <span class="font-medium text-gray-900">
                {{ project.created_at ? formatDate(project.created_at) : 'Unknown' }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Placeholder sections for future features -->
      <div class="grid md:grid-cols-2 gap-8">
        <!-- Recent Tasks -->
        <div class="bg-white rounded-lg shadow-sm border p-6">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-semibold text-gray-900">Recent Tasks</h2>
            <button class="text-blue-600 hover:text-blue-800 text-md font-medium">View All</button>
          </div>
          <div class="text-center py-8 text-gray-500">
            <svg class="w-12 h-12 mx-auto mb-2 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
            </svg>
            <p>Tasks will be displayed here</p>
          </div>
        </div>

        <!-- Organization Members -->
        <div class="bg-white rounded-lg shadow-sm border p-6">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-semibold text-gray-900">Project Members</h2>
            <button 
              @click="manageMembers"
              class="text-blue-600 hover:text-blue-800 text-md font-medium"
            >
              Manage
            </button>
          </div>
          <div class="text-center py-8 text-gray-500">
            <svg class="w-12 h-12 mx-auto mb-2 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-2.239"></path>
            </svg>
            <p>Project members will be displayed here</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from "@/plugins/axiosConfig.js"
import { extractIdFromSlug } from "@/utils/slugUtils.js"

const router = useRouter()
const route = useRoute()

// Reactive data
const project = ref(null)
const loading = ref(true)
const error = ref('')

// Get project slug from route
const projectSlug = computed(() => route.params.slug)

// Extract project ID from slug for API calls
const projectId = computed(() => {
  const slug = projectSlug.value
  return extractIdFromSlug(slug)
})

// Fetch project details from API
const fetchProject = async () => {
  try {
    loading.value = true
    error.value = ''
    
    // Extract ID from slug for API call
    const id = projectId.value
    if (!id) {
      error.value = 'Invalid project URL - could not extract project ID'
      return
    }
    
    // API call uses ID (projects/3/) but URL shows slug (projects/ems-project-3)
    const response = await axios.get(`projects/${id}/`)
    
    // Handle your API response structure
    const projectData = response.data.data || response.data || null
    project.value = projectData

    // Optional: Validate that the slug in URL matches the slug from API
    if (projectData && projectData.slug) {
      const expectedSlug = `${projectData.slug}-${projectData.id}`
      const currentSlug = projectSlug.value
      
      // If the slug doesn't match, redirect to correct slug
      if (expectedSlug !== currentSlug) {
        router.replace(`/projects/${expectedSlug}`)
      }
    }

  } catch (err) {
    console.error('Failed to fetch project:', err)
    if (err.response?.status === 404) {
      error.value = 'Project not found'
    } else if (err.response?.status === 401) {
      error.value = 'You need to login to view this project'
    } else if (err.response?.data?.detail) {
      error.value = err.response.data.detail
    } else {
      error.value = 'Failed to load project details. Please try again.'
    }
  } finally {
    loading.value = false
  }
}

// Static data functions (same as in ProjectsList)
const getStaticTasksCount = (project) => {
  const counts = [3, 5, 8, 12, 15, 7, 4, 9, 11, 6]
  return counts[project.id % counts.length] || 5
}

const getStaticMembersCount = (project) => {
  const counts = [2, 3, 5, 4, 6, 3, 2, 4, 7, 5]
  return counts[project.id % counts.length] || 3
}

const getStaticProgress = (project) => {
  const progressValues = [25, 45, 60, 75, 30, 85, 40, 90, 65, 50]
  return progressValues[project.id % progressValues.length] || 50
}

// Get status badge CSS class (same as in ProjectsList)
const getStatusBadgeClass = (status) => {
  const statusLower = (status || 'active').toLowerCase()
  
  switch (statusLower) {
    case 'active':
      return 'bg-green-100 text-green-800'
    case 'completed':
      return 'bg-blue-100 text-blue-800'
    case 'on_hold':
    case 'paused':
      return 'bg-yellow-100 text-yellow-800'
    case 'cancelled':
      return 'bg-red-100 text-red-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

// Format status for display
const formatStatus = (status) => {
  if (!status) return 'Active'
  return status.charAt(0).toUpperCase() + status.slice(1).replace('_', ' ')
}

// Format date helper
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
}

// Calculate days remaining or elapsed
const getDaysRemaining = () => {
  if (!project.value?.end_date) return '--'
  
  const today = new Date()
  const endDate = new Date(project.value.end_date)
  const diffTime = endDate - today
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  return Math.abs(diffDays)
}

const getDaysLabel = () => {
  if (!project.value?.end_date) return 'No deadline'
  
  const today = new Date()
  const endDate = new Date(project.value.end_date)
  const diffTime = endDate - today
  
  if (diffTime > 0) {
    return 'Days left'
  } else if (diffTime < 0) {
    return 'Days overdue'
  } else {
    return 'Due today'
  }
}

// Action functions
const editProject = () => {
  // Navigate to edit project page using slug-id format
  const slug = project.value.slug ? `${project.value.slug}-${project.value.id}` : project.value.id
  router.push(`/projects/${slug}/edit`)
}

const manageMembers = () => {
  // Navigate to project members management page
  const slug = project.value.slug ? `${project.value.slug}-${project.value.id}` : project.value.id
  router.push({ name: 'projects.members', params: { slug } })
}

// Fetch project on component mount
onMounted(() => {
  fetchProject()
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