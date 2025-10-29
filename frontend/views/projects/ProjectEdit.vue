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
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <h3 class="text-lg font-semibold text-red-800 mb-2">Failed to load project</h3>
        <p class="text-red-600 mb-4">{{ error }}</p>
        <div class="space-x-3">
          <button @click="fetchProject" class="bg-red-600 px-4 py-2 rounded-lg hover:bg-red-700 transition duration-300"
            style="color: white !important;">
            Try Again
          </button>
          <router-link to="/projects"
            class="bg-gray-600 px-4 py-2 rounded-lg hover:bg-gray-700 transition duration-300 inline-block"
            style="color: white !important;">
            Back to Projects
          </router-link>
        </div>
      </div>
    </div>

    <!-- Edit Form -->
    <div v-else-if="project" class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
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
                <router-link :to="`/projects/${project.slug}`" class="hover:text-blue-600 transition duration-300">
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
        <div>
          <router-link :to="`/projects/${project.slug}/members`"
            class="bg-green-600 px-6 py-2 rounded-lg hover:bg-green-700 transition duration-300 flex items-center"
            style="color: white !important;">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="white" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656 0-1.28-.195-1.835M7 20v-2a3 3 0 015.356-1.857M7 20h10M12 12a5 5 0 100-10 5 5 0 000 10zm-7 8a7 7 0 0114 0v1H5v-1z">
              </path>
            </svg>
            <span style="color: white !important;">️ Manage Users</span>
          </router-link>
        </div>
      </div>

      <!-- Form -->
      <div class="bg-white rounded-lg shadow-sm border">
        <form @submit.prevent="updateProject" class="p-6 space-y-6">
          <!-- Project Name -->
          <BaseInput v-model="form.name" label="Project Name" placeholder="Enter project name" required
            :error="fieldErrors.name" />

          <!-- Project Description -->
          <BaseTextarea v-model="form.description" label="Description" placeholder="Enter project description" :rows="4"
            :error="fieldErrors.description" />

          <!-- Date Fields -->
          <div class="grid md:grid-cols-2 gap-6">
            <!-- Start Date -->
            <BaseDatePicker v-model="form.start_date" label="Start Date" placeholder="Select start date"
              :enable-time="false" date-format="Y-m-d" alt-format="F j, Y" :error="fieldErrors.start_date" />

            <!-- End Date -->
            <BaseDatePicker v-model="form.end_date" label="End Date" placeholder="Select end date" :enable-time="false"
              date-format="Y-m-d" alt-format="F j, Y" :error="fieldErrors.end_date" />
          </div>

          <!-- Status -->
          <BaseSelect v-model="form.status" label="Status" :options="statusOptions" :error="fieldErrors.status" />

          <!-- Form Actions -->
          <div class="flex items-center justify-between pt-6 border-t border-gray-200">
            <router-link :to="`/projects/${project.slug}`"
              class="text-gray-600 hover:text-gray-800 font-medium transition duration-300">
              Cancel
            </router-link>

            <div class="flex space-x-3">
              <button type="button" @click="showDeleteModal = true"
                class="bg-red-600 px-6 py-2 rounded-lg hover:bg-red-700 transition duration-300 flex items-center cursor-pointer"
                style="color: white !important;">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="white" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16">
                  </path>
                </svg>
                <span style="color: white !important;">Delete Project</span>
              </button>

              <button type="submit" :disabled="updating"
                class="bg-blue-600 px-6 py-2 rounded-lg hover:bg-blue-700 transition duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center cursor-pointer"
                style="color: white !important;">
                <span v-if="updating" class="flex items-center" style="color: white !important;">
                  <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
                    viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                    </path>
                  </svg>
                  <span style="color: white !important;">Updating...</span>
                </span>
                <span v-else class="flex items-center" style="color: white !important;">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="white" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  <span style="color: white !important;">Update Project</span>
                </span>
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md mx-4">
        <div class="flex items-center mb-4">
          <div class="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center mr-3">
            <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 15.5c-.77.833.192 2.5 1.732 2.5z">
              </path>
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900">Delete Project</h3>
        </div>

        <p class="text-gray-600 mb-6">
          Are you sure you want to delete "{{ project?.name }}"? This action cannot be undone and will remove all
          associated data.
        </p>

        <div class="flex space-x-3 justify-end">
          <button @click="showDeleteModal = false" :disabled="deleting"
            class="px-4 py-2 text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300 transition duration-300 disabled:opacity-50">
            Cancel
          </button>
          <button @click="deleteProject" :disabled="deleting"
            class="px-4 py-2 bg-red-600 rounded-lg hover:bg-red-700 transition duration-300 disabled:opacity-50 flex items-center"
            style="color: white !important;">
            <span v-if="deleting" class="flex items-center" style="color: white !important;">
              <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
                viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                </path>
              </svg>
              <span style="color: white !important;">Deleting...</span>
            </span>
            <span v-else style="color: white !important;">Delete Project</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, inject } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from "@/plugins/axiosConfig.js"
import { BaseInput, BaseTextarea, BaseSelect, BaseDatePicker } from '@/components/forms'

const router = useRouter()
const route = useRoute()
const $toast = inject("toast")

// Status options
const statusOptions = [
  { value: 'active', label: 'Active' },
  { value: 'completed', label: 'Completed' },
  { value: 'on_hold', label: 'On Hold' },
  { value: 'cancelled', label: 'Cancelled' }
]

// Reactive data
const project = ref(null)
const loading = ref(true)
const updating = ref(false)
const deleting = ref(false)
const error = ref('')
const fieldErrors = ref({})
const showDeleteModal = ref(false)

// Form data
const form = reactive({
  name: '',
  description: '',
  start_date: '',
  end_date: '',
  status: 'active'
})

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

    const response = await axios.get(`projects/${slug}/`)
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
    if (err.response?.data?.detail) {
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
    fieldErrors.value = {}

    const slug = projectSlug.value
    if (!slug) {
      $toast?.error('Cannot update - invalid project slug')
      return
    }

    const updateData = { ...form }
    const response = await axios.patch(`projects/${slug}/`, updateData)
    const updatedProject = response.data.data || response.data

    if (updatedProject) {
      project.value = updatedProject
      $toast?.success('Project updated successfully')
      router.push(`/projects/${updatedProject.slug}`)
    }
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
      $toast?.error('Failed to update project')
    }
  } finally {
    updating.value = false
  }
}

// Delete project
const deleteProject = async () => {
  try {
    deleting.value = true

    const slug = projectSlug.value
    if (!slug) {
      $toast?.error('Cannot delete - invalid project slug')
      return
    }

    await axios.delete(`projects/${slug}/`)
    $toast?.success('Project deleted successfully')
    router.push('/projects')
  } catch (err) {
    showDeleteModal.value = false

    if (err.response?.data?.detail) {
      $toast?.error(err.response.data.detail)
    } else {
      $toast?.error('Failed to delete project')
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

<script>
export default {
  components: {
    flatpickr
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