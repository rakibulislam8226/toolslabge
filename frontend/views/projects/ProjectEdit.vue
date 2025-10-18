<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Loading State -->
    <div v-if="loading && !project" class="flex justify-center items-center py-24">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      <span class="ml-3 text-gray-600">Loading project...</span>
    </div>

    <!-- Error State -->
    <div v-else-if="error && !project" class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
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

    <!-- Edit Form -->
    <div v-else-if="project" class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-8">
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
            <li>
              <router-link 
                :to="`/projects/${project.slug ? `${project.slug}-${project.id}` : project.id}`" 
                class="hover:text-blue-600 transition duration-300"
              >
                {{ project.name }}
              </router-link>
            </li>
            <li>
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
              </svg>
            </li>
            <li class="text-gray-900 font-medium">Edit</li>
          </ol>
        </nav>

        <h1 class="text-3xl font-bold text-gray-900">Edit Project</h1>
        <p class="mt-2 text-gray-600">Update your project information</p>
      </div>

      <!-- Form -->
      <div class="bg-white rounded-lg shadow-sm border">
        <form @submit.prevent="updateProject" class="p-6 space-y-6">
          <!-- Project Name -->
          <div>
            <label for="name" class="block text-sm font-medium text-gray-700 mb-2">
              Project Name *
            </label>
            <input
              type="text"
              id="name"
              v-model="form.name"
              placeholder="Enter project name"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
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
              placeholder="Enter project description"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            ></textarea>
          </div>

          <!-- Date Fields -->
          <div class="grid md:grid-cols-2 gap-6">
            <!-- Start Date -->
            <div>
              <label for="start_date" class="block text-sm font-medium text-gray-700 mb-2">
                Start Date
              </label>
              <input
                type="date"
                id="start_date"
                v-model="form.start_date"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <!-- End Date -->
            <div>
              <label for="end_date" class="block text-sm font-medium text-gray-700 mb-2">
                End Date
              </label>
              <input
                type="date"
                id="end_date"
                v-model="form.end_date"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          <!-- Status -->
          <div>
            <label for="status" class="block text-sm font-medium text-gray-700 mb-2">
              Status
            </label>
            <select
              id="status"
              v-model="form.status"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="active">Active</option>
              <option value="completed">Completed</option>
              <option value="on_hold">On Hold</option>
              <option value="cancelled">Cancelled</option>
            </select>
          </div>

          <!-- Form Actions -->
          <div class="flex items-center justify-between pt-6 border-t border-gray-200">
            <router-link
              :to="`/projects/${project.slug ? `${project.slug}-${project.id}` : project.id}`"
              class="text-gray-600 hover:text-gray-800 font-medium transition duration-300"
            >
              Cancel
            </router-link>

            <div class="flex space-x-3">
              <button
                type="button"
                @click="showDeleteModal = true"
                class="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700 transition duration-300 flex items-center"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                </svg>
                Delete Project
              </button>

              <button
                type="submit"
                :disabled="updating"
                class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
              >
                <span v-if="updating" class="flex items-center">
                  <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Updating...
                </span>
                <span v-else class="flex items-center">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  Update Project
                </span>
              </button>
            </div>
          </div>
        </form>

        <!-- Success/Error Messages -->
        <div v-if="successMessage" class="p-6 pt-0">
          <div class="bg-green-50 border border-green-200 rounded-lg p-4">
            <p class="text-green-600 font-medium">{{ successMessage }}</p>
          </div>
        </div>

        <div v-if="updateError" class="p-6 pt-0">
          <div class="bg-red-50 border border-red-200 rounded-lg p-4">
            <p class="text-red-600 font-medium">{{ updateError }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md mx-4">
        <div class="flex items-center mb-4">
          <div class="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center mr-3">
            <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 15.5c-.77.833.192 2.5 1.732 2.5z"></path>
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900">Delete Project</h3>
        </div>
        
        <p class="text-gray-600 mb-6">
          Are you sure you want to delete "{{ project?.name }}"? This action cannot be undone and will remove all associated data.
        </p>
        
        <div class="flex space-x-3 justify-end">
          <button
            @click="showDeleteModal = false"
            :disabled="deleting"
            class="px-4 py-2 text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300 transition duration-300 disabled:opacity-50"
          >
            Cancel
          </button>
          <button
            @click="deleteProject"
            :disabled="deleting"
            class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition duration-300 disabled:opacity-50 flex items-center"
          >
            <span v-if="deleting" class="flex items-center">
              <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Deleting...
            </span>
            <span v-else>Delete Project</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from "@/plugins/axiosConfig.js"
import { extractIdFromSlug } from "@/utils/slugUtils.js"

const router = useRouter()
const route = useRoute()

// Reactive data
const project = ref(null)
const loading = ref(true)
const updating = ref(false)
const deleting = ref(false)
const error = ref('')
const updateError = ref('')
const successMessage = ref('')
const showDeleteModal = ref(false)

// Form data
const form = reactive({
  name: '',
  description: '',
  start_date: '',
  end_date: '',
  status: 'active'
})

// Get project ID from route slug
const projectId = computed(() => {
  const slug = route.params.slug
  return extractIdFromSlug(slug)
})

// Fetch project details from API
const fetchProject = async () => {
  try {
    loading.value = true
    error.value = ''
    
    const id = projectId.value
    if (!id) {
      error.value = 'Invalid project URL - could not extract project ID'
      return
    }
    
    const response = await axios.get(`projects/${id}/`)
    const projectData = response.data.data || response.data || null
    project.value = projectData

    // Populate form with current data
    if (projectData) {
      form.name = projectData.name || ''
      form.description = projectData.description || ''
      form.start_date = projectData.start_date || ''
      form.end_date = projectData.end_date || ''
      form.status = projectData.status || 'active'
    }

  } catch (err) {
    console.error('Failed to fetch project:', err)
    if (err.response?.status === 404) {
      error.value = 'Project not found'
    } else if (err.response?.status === 401) {
      error.value = 'You need to login to edit this project'
    } else if (err.response?.data?.detail) {
      error.value = err.response.data.detail
    } else {
      error.value = 'Failed to load project. Please try again.'
    }
  } finally {
    loading.value = false
  }
}

// Update project
const updateProject = async () => {
  try {
    updating.value = true
    updateError.value = ''
    successMessage.value = ''
    
    const id = projectId.value
    if (!id) {
      updateError.value = 'Cannot update - invalid project ID'
      return
    }

    // Prepare data for PATCH request
    const updateData = {
      name: form.name,
      description: form.description,
      start_date: form.start_date || null,
      end_date: form.end_date || null,
      status: form.status
    }

    const response = await axios.patch(`projects/${id}/`, updateData)
    
    // Update local project data
    const updatedProject = response.data.data || response.data
    if (updatedProject) {
      project.value = updatedProject
      successMessage.value = 'Project updated successfully!'
      
      // Clear success message after 3 seconds
      setTimeout(() => {
        successMessage.value = ''
      }, 3000)
    }

  } catch (err) {
    console.error('Failed to update project:', err)
    if (err.response?.data?.detail) {
      updateError.value = err.response.data.detail
    } else if (err.response?.data) {
      // Handle field-specific errors
      const errors = Object.values(err.response.data).flat()
      updateError.value = errors.join(', ')
    } else {
      updateError.value = 'Failed to update project. Please try again.'
    }
  } finally {
    updating.value = false
  }
}

// Delete project
const deleteProject = async () => {
  try {
    deleting.value = true
    
    const id = projectId.value
    if (!id) {
      updateError.value = 'Cannot delete - invalid project ID'
      return
    }
    
    await axios.delete(`projects/${id}/`)
    
    // Redirect to projects list after successful deletion
    router.push('/projects')
    
  } catch (err) {
    console.error('Failed to delete project:', err)
    showDeleteModal.value = false
    
    if (err.response?.data?.detail) {
      updateError.value = err.response.data.detail
    } else {
      updateError.value = 'Failed to delete project. Please try again.'
    }
  } finally {
    deleting.value = false
  }
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