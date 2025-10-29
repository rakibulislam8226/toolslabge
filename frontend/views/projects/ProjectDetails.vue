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
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <h3 class="text-lg font-semibold text-red-800 mb-2">Failed to load project</h3>
        <p class="text-red-600 mb-4">{{ error }}</p>
        <div class="space-x-3">
          <Button variant="danger" size="md" label="Try Again" @click="fetchProject" />
          <router-link to="/projects"
            class="bg-gray-600 px-4 py-2 rounded-lg hover:bg-gray-700 transition duration-300 inline-block"
            style="color: white !important;">
            Back to Projects
          </router-link>
        </div>
      </div>
    </div>

    <!-- Project Details Content -->
    <div v-else-if="project" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-6 lg:py-8">
      <!-- Header Section -->
      <!-- Header Section -->
      <div class="bg-white rounded-xl shadow-lg border border-gray-200 mb-6 sm:mb-8 overflow-hidden">
        <div class="px-4 sm:px-6 py-4 sm:py-6 border-b border-gray-200">
          <div class="flex flex-col lg:flex-row lg:items-start lg:justify-between space-y-4 lg:space-y-0">
            <div class="flex-1 lg:mr-6">
              <!-- Breadcrumb -->
              <nav class="mb-3 sm:mb-4">
                <ol class="flex items-center space-x-2 text-sm text-gray-500">
                  <li>
                    <router-link to="/projects" class="hover:text-blue-600 transition duration-300 font-medium">
                      Projects
                    </router-link>
                  </li>
                  <li>
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                    </svg>
                  </li>
                  <li class="text-gray-900 font-semibold truncate">{{ project.name }}</li>
                </ol>
              </nav>

              <!-- Project Title and Status -->
              <div class="flex flex-col sm:flex-row sm:items-center mb-3 sm:mb-4 space-y-2 sm:space-y-0">
                <h1 class="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900 sm:mr-4 leading-tight">
                  {{ project.name }}
                </h1>
                <span :class="getStatusBadgeClass(project.status)"
                  class="px-3 py-1.5 text-sm font-semibold rounded-full self-start shadow-sm">
                  {{ formatStatus(project.status) }}
                </span>
              </div>

              <!-- Project Description -->
              <p class="text-gray-600 text-base sm:text-lg leading-relaxed max-w-3xl">
                {{ project.description || 'No description available for this project.' }}
              </p>
            </div>

            <!-- Action Buttons -->
            <div
              class="flex flex-col sm:flex-row items-stretch sm:items-center space-y-2 sm:space-y-0 sm:space-x-3 lg:flex-shrink-0">
              <Button @click="editProject" variant="primary" size="md"
                class="bg-blue-600 px-4 py-2.5 rounded-lg hover:bg-blue-700 transition-all duration-300 flex items-center justify-center shadow-md hover:shadow-lg transform hover:-translate-y-0.5 cursor-pointer"
                style="color: white !important;" label="Edit Project">
                <template #prepend>
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="white" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z">
                    </path>
                  </svg>
                </template>
              </Button>
              <router-link :to="`/projects/${project.slug}/tasks`"
                class="bg-indigo-600 px-4 py-2.5 rounded-lg hover:bg-indigo-700 transition-all duration-300 flex items-center justify-center shadow-md hover:shadow-lg transform hover:-translate-y-0.5"
                style="color: white !important;">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="white" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z">
                  </path>
                </svg>
                <span class="font-medium" style="color: white !important;">View Tasks</span>
              </router-link>
            </div>
          </div>
        </div>

        <!-- Project Stats -->
        <div class="px-4 sm:px-6 py-4 sm:py-6 bg-gray-50">
          <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
            <!-- Tasks -->
            <div
              class="text-center p-4 rounded-xl bg-white shadow-sm border border-gray-100 hover:shadow-md transition-all duration-300 transform hover:-translate-y-1">
              <div
                class="w-14 h-14 bg-gradient-to-br from-blue-100 to-blue-200 rounded-2xl flex items-center justify-center mx-auto mb-3 shadow-sm">
                <svg class="w-7 h-7 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <p class="text-2xl sm:text-3xl font-bold text-gray-900 mb-1">{{ getStaticTasksCount(project) }}</p>
              <p class="text-sm font-medium text-gray-600">Tasks</p>
            </div>

            <!-- Members -->
            <div
              class="text-center p-4 rounded-xl bg-white shadow-sm border border-gray-100 hover:shadow-md transition-all duration-300 transform hover:-translate-y-1">
              <div
                class="w-14 h-14 bg-gradient-to-br from-green-100 to-green-200 rounded-2xl flex items-center justify-center mx-auto mb-3 shadow-sm">
                <svg class="w-7 h-7 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-2.239"></path>
                </svg>
              </div>
              <p class="text-2xl sm:text-3xl font-bold text-gray-900 mb-1">{{ getStaticMembersCount(project) }}</p>
              <p class="text-sm font-medium text-gray-600">Members</p>
            </div>

            <!-- Progress -->
            <div
              class="text-center p-4 rounded-xl bg-white shadow-sm border border-gray-100 hover:shadow-md transition-all duration-300 transform hover:-translate-y-1">
              <div
                class="w-14 h-14 bg-gradient-to-br from-purple-100 to-purple-200 rounded-2xl flex items-center justify-center mx-auto mb-3 shadow-sm">
                <svg class="w-7 h-7 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z">
                  </path>
                </svg>
              </div>
              <p class="text-2xl sm:text-3xl font-bold text-gray-900 mb-1">{{ getStaticProgress(project) }}%</p>
              <p class="text-sm font-medium text-gray-600">Complete</p>
            </div>

            <!-- Status Days -->
            <div
              class="text-center p-4 rounded-xl bg-white shadow-sm border border-gray-100 hover:shadow-md transition-all duration-300 transform hover:-translate-y-1 col-span-2 lg:col-span-1">
              <div
                class="w-14 h-14 bg-gradient-to-br from-amber-100 to-amber-200 rounded-2xl flex items-center justify-center mx-auto mb-3 shadow-sm">
                <svg class="w-7 h-7 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <p class="text-2xl sm:text-3xl font-bold text-gray-900 mb-1">{{ getDaysRemaining() }}</p>
              <p class="text-sm font-medium text-gray-600">{{ getDaysLabel() }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Project Dates and Details -->
      <div class="grid lg:grid-cols-2 gap-6 sm:gap-8 mb-6 sm:mb-8">
        <!-- Project Timeline -->
        <div
          class="bg-white rounded-xl shadow-lg border border-gray-200 p-4 sm:p-6 hover:shadow-xl transition-all duration-300">
          <h2 class="text-xl sm:text-2xl font-bold text-gray-900 mb-4 sm:mb-6 flex items-center">
            <div
              class="w-8 h-8 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center mr-3 shadow-sm">
              <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
              </svg>
            </div>
            Project Timeline
          </h2>

          <div class="space-y-4">
            <div
              class="flex flex-col sm:flex-row sm:justify-between sm:items-center p-4 bg-white rounded-xl border border-gray-200 shadow-sm">
              <span class="text-gray-600 font-medium mb-1 sm:mb-0">Start Date</span>
              <span class="font-semibold text-gray-900 text-sm sm:text-base">
                {{ project.start_date ? formatDate(project.start_date) : 'Not set' }}
              </span>
            </div>

            <div
              class="flex flex-col sm:flex-row sm:justify-between sm:items-center p-4 bg-white rounded-xl border border-gray-200 shadow-sm">
              <span class="text-gray-600 font-medium mb-1 sm:mb-0">End Date</span>
              <span class="font-semibold text-gray-900 text-sm sm:text-base">
                {{ project.end_date ? formatDate(project.end_date) : 'Not set' }}
              </span>
            </div>

            <!-- Progress Bar -->
            <div class="mt-6 p-4 bg-white rounded-xl border border-gray-200 shadow-sm">
              <div class="flex justify-between text-sm font-medium text-gray-700 mb-3">
                <span>Overall Progress</span>
                <span class="text-blue-600 font-bold">{{ getStaticProgress(project) }}%</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-4 shadow-inner">
                <div
                  class="bg-gradient-to-r from-blue-500 via-blue-600 to-blue-700 h-4 rounded-full transition-all duration-700 shadow-sm"
                  :style="{ width: `${getStaticProgress(project)}%` }"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Project Information -->
        <div
          class="bg-white rounded-xl shadow-lg border border-gray-200 p-4 sm:p-6 hover:shadow-xl transition-all duration-300">
          <h2 class="text-xl sm:text-2xl font-bold text-gray-900 mb-4 sm:mb-6 flex items-center">
            <div
              class="w-8 h-8 bg-gradient-to-br from-indigo-500 to-indigo-600 rounded-lg flex items-center justify-center mr-3 shadow-sm">
              <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            Project Information
          </h2>

          <div class="space-y-4">
            <div
              class="flex flex-col sm:flex-row sm:justify-between sm:items-center p-4 bg-white rounded-xl border border-gray-200 shadow-sm">
              <span class="text-gray-600 font-medium mb-1 sm:mb-0">Project Manager</span>
              <span class="font-semibold text-gray-900 text-sm sm:text-base break-words">
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

            <div
              class="flex flex-col sm:flex-row sm:justify-between sm:items-center p-4 bg-white rounded-xl border border-gray-200 shadow-sm">
              <span class="text-gray-600 font-medium mb-2 sm:mb-0">Status</span>
              <span :class="getStatusBadgeClass(project.status)"
                class="px-3 py-1.5 text-sm font-semibold rounded-full shadow-sm self-start sm:self-center">
                {{ formatStatus(project.status) }}
              </span>
            </div>

            <div
              class="flex flex-col sm:flex-row sm:justify-between sm:items-center p-4 bg-white rounded-xl border border-gray-200 shadow-sm">
              <span class="text-gray-600 font-medium mb-1 sm:mb-0">Created</span>
              <span class="font-semibold text-gray-900 text-sm sm:text-base">
                {{ project.created_at ? formatDate(project.created_at) : 'Unknown' }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Placeholder sections for future features -->
      <div class="grid lg:grid-cols-2 gap-6 sm:gap-8">
        <!-- Recent Tasks -->
        <div
          class="bg-white rounded-xl shadow-lg border border-gray-200 p-4 sm:p-6 hover:shadow-xl transition-all duration-300">
          <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-4 sm:mb-6 space-y-2 sm:space-y-0">
            <h2 class="text-xl sm:text-2xl font-bold text-gray-900 flex items-center">
              <div
                class="w-8 h-8 bg-gradient-to-br from-green-500 to-green-600 rounded-lg flex items-center justify-center mr-3 shadow-sm">
                <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2">
                  </path>
                </svg>
              </div>
              Recent Tasks
            </h2>
            <button @click="viewAllTasks"
              class="text-green-600 hover:text-green-800 text-md font-semibold transition-colors duration-200 hover:underline self-start sm:self-center">
              View All →
            </button>
          </div>
          <div class="text-center py-8 sm:py-12 text-gray-500">
            <div
              class="w-16 h-16 bg-gradient-to-br from-green-100 to-green-200 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-sm">
              <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2">
                </path>
              </svg>
            </div>
            <p class="text-gray-600 font-medium mb-4">Tasks will be displayed here</p>
            <Button @click="viewAllTasks"
              class="bg-green-600 px-6 py-3 rounded-xl hover:bg-green-700 transition-all duration-300 font-semibold shadow-md hover:shadow-lg transform hover:-translate-y-0.5"
              style="color: white !important;">
              View Tasks
            </Button>
          </div>
        </div>

        <!-- Project Members -->
        <div
          class="bg-white rounded-xl shadow-lg border border-gray-200 p-4 sm:p-6 hover:shadow-xl transition-all duration-300">
          <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-4 sm:mb-6 space-y-2 sm:space-y-0">
            <h2 class="text-xl sm:text-2xl font-bold text-gray-900 flex items-center">
              <div
                class="w-8 h-8 bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg flex items-center justify-center mr-3 shadow-sm">
                <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-2.239"></path>
                </svg>
              </div>
              Project Members
            </h2>
            <button @click="manageMembers"
              class="text-purple-600 hover:text-purple-800 text-md font-semibold transition-colors duration-200 hover:underline self-start sm:self-center">
              Manage →
            </button>
          </div>
          <div class="text-center py-8 sm:py-12 text-gray-500">
            <div
              class="w-16 h-16 bg-gradient-to-br from-purple-100 to-purple-200 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-sm">
              <svg class="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-2.239"></path>
              </svg>
            </div>
            <p class="text-gray-600 font-medium mb-4">Project members will be displayed here</p>
            <Button @click="manageMembers"
              class="bg-purple-600 px-6 py-3 rounded-xl hover:bg-purple-700 transition-all duration-300 font-semibold shadow-md hover:shadow-lg transform hover:-translate-y-0.5"
              style="color: white !important;">
              Manage Members
            </Button>
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
import Button from '@/components/Button.vue'

const router = useRouter()
const route = useRoute()

// Reactive data
const project = ref(null)
const loading = ref(true)
const error = ref('')

// Get project slug from route
const projectSlug = computed(() => route.params.slug)

// Fetch project details from API
const fetchProject = async () => {
  try {
    loading.value = true
    error.value = ''

    const slug = projectSlug.value
    if (!slug) {
      error.value = 'Invalid project URL - missing slug'
      return
    }

    // API call uses backend slug directly: projects/{slug}/
    const response = await axios.get(`projects/${slug}/`)

    // Handle your API response structure
    const projectData = response.data.data || response.data || null
    project.value = projectData

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
  // Navigate to edit project page using backend slug
  const slug = project.value.slug
  router.push(`/projects/${slug}/edit`)
}

const viewAllTasks = () => {
  // Navigate to tasks page for this project
  const slug = project.value.slug
  router.push(`/projects/${slug}/tasks`)
}

const manageMembers = () => {
  // Navigate to project members management page
  const slug = project.value.slug
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

/* Additional animations and effects */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }

  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.fade-in-up {
  animation: fadeInUp 0.6s ease-out;
}

.slide-in-right {
  animation: slideInRight 0.8s ease-out;
}

/* Hover effects for cards */
.hover-lift {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.hover-lift:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

/* Progress bar animation */
.progress-bar {
  transition: width 1s ease-in-out;
  background: linear-gradient(90deg, #3b82f6, #1d4ed8, #2563eb);
  animation: shimmer 2s ease-in-out infinite;
}

@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }

  100% {
    background-position: 200% 0;
  }
}

/* Custom scrollbar for better UX */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 8px;
}

::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 8px;
}

::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Button hover effects */
.btn-primary {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  box-shadow: 0 4px 15px 0 rgba(59, 130, 246, 0.3);
  transition: all 0.3s ease;
}

.btn-primary:hover {
  box-shadow: 0 8px 25px 0 rgba(59, 130, 246, 0.4);
  transform: translateY(-2px);
}

/* Glass morphism effect */
.glass-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Mobile-specific optimizations */
@media (max-width: 640px) {
  .mobile-stack {
    flex-direction: column;
    align-items: stretch;
  }

  .mobile-full-width {
    width: 100%;
  }
}

/* Loading skeleton animation */
.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
}

@keyframes loading {
  0% {
    background-position: 200% 0;
  }

  100% {
    background-position: -200% 0;
  }
}
</style>