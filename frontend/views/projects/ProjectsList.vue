<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header Section -->
    <div class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="flex justify-between items-center">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">Projects</h1>
            <p class="mt-2 text-gray-600">Manage and track all your organization's projects</p>
          </div>
          <button
            @click="createNewProject"
            class="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition duration-300 shadow-lg flex items-center"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
            </svg>
            New Project
          </button>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <span class="ml-3 text-gray-600">Loading projects...</span>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
        <svg class="w-12 h-12 text-red-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <h3 class="text-lg font-semibold text-red-800 mb-2">Failed to load projects</h3>
        <p class="text-red-600 mb-4">{{ error }}</p>
        <button
          @click="fetchProjects"
          class="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition duration-300"
        >
          Try Again
        </button>
      </div>

      <!-- Empty State -->
      <div v-else-if="projects.length === 0" class="text-center py-12">
        <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
        </svg>
        <h3 class="text-xl font-semibold text-gray-900 mb-2">No projects yet</h3>
        <p class="text-gray-600 mb-6">Get started by creating your first project</p>
        <button
          @click="createNewProject"
          class="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition duration-300 shadow-lg inline-flex items-center"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
          </svg>
          Create Your First Project
        </button>
      </div>

      <!-- Projects Grid -->
      <div v-else class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <div
          v-for="project in projects"
          :key="project.id"
          class="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 cursor-pointer border border-gray-200"
          @click="viewProject(project)"
        >
          <!-- Project Header -->
          <div class="p-6 border-b border-gray-100">
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <h3 class="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
                  {{ project.name || 'Untitled Project' }}
                </h3>
                <p class="text-gray-600 text-sm line-clamp-3">
                  {{ project.description || 'No description available' }}
                </p>
              </div>
              
              <!-- Status Badge -->
              <span 
                :class="getStatusBadgeClass(project.status)"
                class="px-2 py-1 text-xs font-medium rounded-full ml-3 flex-shrink-0"
              >
                {{ project.status || 'Active' }}
              </span>
            </div>
          </div>

            <!-- Project Stats -->
            <div class="px-6 py-4">
              <div class="flex items-center justify-between text-sm text-gray-600">
                <div class="flex items-center">
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  {{ getStaticTasksCount(project) }} tasks
                </div>
                
                <div class="flex items-center">
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-2.239"></path>
                  </svg>
                  {{ getStaticMembersCount(project) }} members
                </div>
              </div>

              <!-- Progress Bar (static for now) -->
              <div class="mt-4">
                <div class="flex justify-between text-xs text-gray-600 mb-1">
                  <span>Progress</span>
                  <span>{{ getStaticProgress(project) }}%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    class="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    :style="{ width: `${getStaticProgress(project)}%` }"
                  ></div>
                </div>
              </div>

              <!-- Project Dates -->
              <div class="mt-4 flex justify-between text-xs text-gray-500">
                <span v-if="project.start_date">
                  Started {{ formatDate(project.start_date) }}
                </span>
                <span v-if="project.end_date">
                  Due {{ formatDate(project.end_date) }}
                </span>
                <span v-if="!project.start_date && !project.end_date" class="text-gray-400">
                  No dates set
                </span>
              </div>
            </div>          <!-- Project Actions -->
          <div class="px-6 py-4 bg-gray-50 border-t border-gray-100 flex justify-between items-center">
            <button
              @click.stop="editProject(project)"
              class="text-blue-600 hover:text-blue-800 text-sm font-medium transition duration-300"
            >
              Edit
            </button>
            <button
              @click.stop="viewProject(project)"
              class="bg-blue-600 text-white px-4 py-2 rounded text-sm font-medium hover:bg-blue-700 transition duration-300"
            >
              View Details
            </button>
          </div>
        </div>
      </div>

      <!-- Load More Button (if pagination exists) -->
      <div v-if="hasMore && !loading" class="text-center mt-8">
        <button
          @click="loadMore"
          class="bg-gray-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-gray-700 transition duration-300"
        >
          Load More Projects
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from "@/plugins/axiosConfig.js"

const router = useRouter()

// Reactive data
const projects = ref([])
const loading = ref(true)
const error = ref('')
const hasMore = ref(false)
const currentPage = ref(1)

// Fetch projects from API
const fetchProjects = async (page = 1) => {
  try {
    loading.value = true
    error.value = ''
    
    const response = await axios.get(`projects/`, {
      params: { page }
    })

    // Handle your API response structure
    const projectsData = response.data.data || []
    const meta = response.data.meta || {}

    if (page === 1) {
      projects.value = projectsData
    } else {
      projects.value.push(...projectsData)
    }

    // Handle pagination based on your API meta structure
    hasMore.value = meta.has_next || false
    currentPage.value = meta.current_page || page

  } catch (err) {
    console.error('Failed to fetch projects:', err)
    if (err.response?.status === 401) {
      error.value = 'You need to login to view projects'
    } else if (err.response?.data?.detail) {
      error.value = err.response.data.detail
    } else {
      error.value = 'Failed to load projects. Please try again.'
    }
  } finally {
    loading.value = false
  }
}

// Load more projects (pagination)
const loadMore = () => {
  fetchProjects(currentPage.value + 1)
}

// Get status badge CSS class
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

// Format date helper
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  })
}

// Static data functions (will be replaced with real API data later)
const getStaticTasksCount = (project) => {
  // Generate a pseudo-random number based on project ID for consistency
  const counts = [3, 5, 8, 12, 15, 7, 4, 9, 11, 6]
  return counts[project.id % counts.length] || 5
}

const getStaticMembersCount = (project) => {
  // Generate a pseudo-random number based on project ID for consistency
  const counts = [2, 3, 5, 4, 6, 3, 2, 4, 7, 5]
  return counts[project.id % counts.length] || 3
}

const getStaticProgress = (project) => {
  // Generate a pseudo-random progress based on project ID for consistency
  const progressValues = [25, 45, 60, 75, 30, 85, 40, 90, 65, 50]
  return progressValues[project.id % progressValues.length] || 50
}

// Navigation functions
const createNewProject = () => {
  // Navigate to create project page (you can implement this later)
  console.log('Navigate to create project page')
  // router.push('/projects/create')
}

const viewProject = (project) => {
  // Navigate to project detail page using slug-id format
  // URL will be: /projects/ems-project-3 (slug-id)
  // API will be called with: projects/3/ (just id)
  const slug = project.slug ? `${project.slug}-${project.id}` : project.id
  router.push(`/projects/${slug}`)
}

const editProject = (project) => {
  // Navigate to edit project page using slug-id format
  const slug = project.slug ? `${project.slug}-${project.id}` : project.id
  router.push(`/projects/${slug}/edit`)
}

// Fetch projects on component mount
onMounted(() => {
  fetchProjects()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;  
  overflow: hidden;
}

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