<template>
    <div class="min-h-screen bg-gray-50">
        <!-- Header Section -->
        <div class="bg-white shadow-sm border-b">
            <div class="max-w-full px-4 sm:px-6 lg:px-8 py-6">
                <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center">
                    <div>
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
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M9 5l7 7-7 7"></path>
                                    </svg>
                                </li>
                                <li>
                                    <button @click="goToProject"
                                        class="hover:text-blue-600 transition duration-300 truncate max-w-[200px]">
                                        {{ project?.name || 'Project' }}
                                    </button>
                                </li>
                                <li>
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M9 5l7 7-7 7"></path>
                                    </svg>
                                </li>
                                <li class="text-gray-900 font-medium">Tasks</li>
                            </ol>
                        </nav>

                        <h1 class="text-3xl font-bold text-gray-900">Project Tasks</h1>
                        <p class="mt-2 text-gray-600" v-if="project">
                            Manage tasks for {{ project.name }}
                        </p>
                    </div>

                    <div class="flex space-x-3 mt-4 sm:mt-0">
                        <button @click="refreshTasks" :disabled="loading"
                            class="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition duration-300 flex items-center"
                            :class="{ 'opacity-50 cursor-not-allowed': loading }">
                            <svg class="w-4 h-4 mr-2" :class="{ 'animate-spin': loading }" fill="none"
                                stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15">
                                </path>
                            </svg>
                            Refresh
                        </button>

                        <button @click="openCreateModal()"
                            class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition duration-300 flex items-center">
                            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M12 4v16m8-8H4"></path>
                            </svg>
                            Create Task
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading && !tasks.length" class="flex justify-center items-center py-20">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div class="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
                <svg class="w-12 h-12 text-red-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <h3 class="text-lg font-semibold text-red-900 mb-2">Error Loading Tasks</h3>
                <p class="text-red-700 mb-4">{{ error }}</p>
                <button @click="fetchTasks"
                    class="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition duration-300">
                    Try Again
                </button>
            </div>
        </div>

        <!-- Tasks Kanban Board -->
        <div v-else class="max-w-full px-4 sm:px-6 lg:px-8 py-8">
            <!-- Status Statistics -->
            <div class="bg-white rounded-lg shadow-sm border p-6 mb-8">
                <h2 class="text-lg font-semibold text-gray-900 mb-4">Task Overview</h2>
                <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4">
                    <div v-for="status in taskStatuses" :key="status.id" class="text-center">
                        <div class="w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-2"
                            :class="getStatusColor(status.id, 'bg')">
                            <span class="text-sm font-bold" :class="getStatusColor(status.id, 'text')">
                                {{ getTasksInStatus(status.id).length }}
                            </span>
                        </div>
                        <p class="text-sm font-medium text-gray-900 truncate">{{ status.name }}</p>
                    </div>
                </div>
            </div>

            <!-- Kanban Board -->
            <div class="overflow-x-auto">
                <div class="flex space-x-6 pb-8" style="min-width: max-content;">
                    <div v-for="status in taskStatuses" :key="status.id" class="flex-shrink-0 w-80">
                        <!-- Status Column Header -->
                        <div class="bg-white rounded-lg shadow-sm border mb-4">
                            <div class="px-4 py-3 border-b border-gray-200">
                                <div class="flex items-center justify-between">
                                    <div class="flex items-center">
                                        <div class="w-3 h-3 rounded-full mr-3" :class="getStatusColor(status.id, 'bg')">
                                        </div>
                                        <h3 class="font-semibold text-gray-900">{{ status.name }}</h3>
                                        <span class="ml-2 px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded-full">
                                            {{ getTasksInStatus(status.id).length }}
                                        </span>
                                    </div>
                                    <button @click="openCreateModal(status.id)"
                                        class="text-gray-400 hover:text-blue-600 transition duration-300">
                                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M12 4v16m8-8H4"></path>
                                        </svg>
                                    </button>
                                </div>
                            </div>
                        </div>

                        <!-- Tasks in Status Column -->
                        <div class="space-y-3 min-h-[400px]">
                            <TaskCard v-for="task in getTasksInStatus(status.id)" :key="task.id" :task="task"
                                :statuses="taskStatuses" @edit="openEditModal" @delete="deleteTask"
                                @status-change="updateTaskStatus" />

                            <!-- Empty State -->
                            <div v-if="getTasksInStatus(status.id).length === 0" class="text-center py-8 text-gray-400">
                                <svg class="w-12 h-12 mx-auto mb-2" fill="none" stroke="currentColor"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z">
                                    </path>
                                </svg>
                                <p class="text-sm">No tasks</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Empty State - No Statuses -->
            <div v-if="!loading && taskStatuses.length === 0" class="text-center py-20">
                <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z">
                    </path>
                </svg>
                <h3 class="text-xl font-semibold text-gray-900 mb-2">No task statuses found</h3>
                <p class="text-gray-600 mb-6">Contact your organization admin to set up task statuses</p>
            </div>
        </div>

        <!-- Create Task Modal -->
        <CreateTaskModal :is-open="showCreateModal" :project-id="String(projectId)"
            :initial-status-id="selectedStatusId" :statuses="taskStatuses" @close="closeCreateModal"
            @created="onTaskCreated" />

        <!-- Edit Task Modal -->
        <EditTaskModal :is-open="showEditModal" :task="selectedTask" :statuses="taskStatuses" @close="closeEditModal"
            @updated="onTaskUpdated" />
    </div>
</template>

<script setup>
import { ref, onMounted, computed, inject } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from "@/plugins/axiosConfig.js"
import { extractIdFromSlug } from "@/utils/slugUtils.js"
import TaskCard from '@/components/tasks/TaskCard.vue'
import CreateTaskModal from '@/components/modals/CreateTaskModal.vue'
import EditTaskModal from '@/components/modals/EditTaskModal.vue'

const router = useRouter()
const route = useRoute()
const $toast = inject("toast")

// Reactive data
const project = ref(null)
const tasks = ref([])
const taskStatuses = ref([])
const loading = ref(true)
const error = ref('')

// Modal states
const showCreateModal = ref(false)
const showEditModal = ref(false)
const selectedTask = ref(null)
const selectedStatusId = ref(null)

// Get project slug from route
const projectSlug = computed(() => route.params.slug)

// Extract project ID from slug for API calls
const projectId = computed(() => {
    const slug = projectSlug.value
    return extractIdFromSlug(slug)
})

// Status color mapping
const statusColors = [
    { bg: 'bg-gray-100', text: 'text-gray-700' },
    { bg: 'bg-blue-100', text: 'text-blue-700' },
    { bg: 'bg-yellow-100', text: 'text-yellow-700' },
    { bg: 'bg-green-100', text: 'text-green-700' },
    { bg: 'bg-purple-100', text: 'text-purple-700' },
    { bg: 'bg-pink-100', text: 'text-pink-700' },
    { bg: 'bg-indigo-100', text: 'text-indigo-700' },
]

// Get tasks for specific status
const getTasksInStatus = (statusId) => {
    return tasks.value.filter(task => task.status?.id === statusId)
}

// Get status color based on index
const getStatusColor = (statusId, type) => {
    const statusIndex = taskStatuses.value.findIndex(s => s.id === statusId)
    const colorIndex = statusIndex % statusColors.length
    return statusColors[colorIndex][type]
}

// Fetch project details
const fetchProject = async () => {
    try {
        const id = projectId.value
        if (!id) {
            error.value = 'Invalid project URL - could not extract project ID'
            return
        }

        const response = await axios.get(`projects/${id}/`)
        project.value = response.data.data
    } catch (err) {
        console.error('Failed to fetch project:', err)
        if (err.response?.status === 404) {
            error.value = 'Project not found'
        } else {
            error.value = 'Failed to load project details'
        }
    }
}

// Fetch task statuses
const fetchTaskStatuses = async () => {
    try {
        const response = await axios.get('tasks/status/')
        taskStatuses.value = response.data.data || response.data || []
    } catch (err) {
        console.error('Failed to fetch task statuses:', err)
        taskStatuses.value = []
    }
}

// Fetch tasks for the project
const fetchTasks = async () => {
    try {
        loading.value = true
        error.value = ''

        const id = projectId.value
        if (!id) {
            error.value = 'Invalid project URL - could not extract project ID'
            return
        }

        const response = await axios.get(`projects/${id}/tasks/`)
        tasks.value = response.data.data || response.data || []
    } catch (err) {
        console.error('Failed to fetch tasks:', err)
        if (err.response?.status === 404) {
            error.value = 'Project not found'
        } else if (err.response?.status === 403) {
            error.value = 'You do not have permission to view tasks for this project'
        } else {
            error.value = 'Failed to load tasks'
        }
    } finally {
        loading.value = false
    }
}

// Initialize data
const initializeData = async () => {
    loading.value = true
    await Promise.all([
        fetchProject(),
        fetchTaskStatuses(),
        fetchTasks()
    ])
    loading.value = false
}

// Refresh tasks
const refreshTasks = () => {
    fetchTasks()
}

// Navigate back to project
const goToProject = () => {
    const slug = project.value?.slug ? `${project.value.slug}-${project.value.id}` : projectId.value
    router.push(`/projects/${slug}`)
}

// Modal handlers
const openCreateModal = (statusId = null) => {
    selectedStatusId.value = statusId
    showCreateModal.value = true
}

const closeCreateModal = () => {
    showCreateModal.value = false
    selectedStatusId.value = null
}

const openEditModal = (task) => {
    selectedTask.value = task
    showEditModal.value = true
}

const closeEditModal = () => {
    showEditModal.value = false
    selectedTask.value = null
}

// Task operations
const onTaskCreated = (newTask) => {
    tasks.value.unshift(newTask)
    $toast?.success('Task created successfully')
    closeCreateModal()
}

const onTaskUpdated = (updatedTask) => {
    const index = tasks.value.findIndex(t => t.id === updatedTask.id)
    if (index !== -1) {
        tasks.value[index] = updatedTask
    }
    $toast?.success('Task updated successfully')
    closeEditModal()
}

const updateTaskStatus = async (taskId, newStatusId) => {
    try {
        const response = await axios.patch(`projects/${projectId.value}/tasks/${taskId}/`, {
            status_id: newStatusId
        })

        const updatedTask = response.data.data || response.data
        const index = tasks.value.findIndex(t => t.id === taskId)
        if (index !== -1) {
            tasks.value[index] = updatedTask
        }

        $toast?.success('Task status updated')
    } catch (err) {
        console.error('Failed to update task status:', err)
        $toast?.error('Failed to update task status')
    }
}

const deleteTask = async (taskId) => {
    if (!confirm('Are you sure you want to delete this task?')) {
        return
    }

    try {
        await axios.delete(`projects/${projectId.value}/tasks/${taskId}/`)
        tasks.value = tasks.value.filter(t => t.id !== taskId)
        $toast?.success('Task deleted successfully')
    } catch (err) {
        console.error('Failed to delete task:', err)
        $toast?.error('Failed to delete task')
    }
}

// Initialize on mount
onMounted(() => {
    initializeData()
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

/* Custom scrollbar for horizontal scroll */
.overflow-x-auto::-webkit-scrollbar {
    height: 8px;
}

.overflow-x-auto::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 4px;
}

.overflow-x-auto::-webkit-scrollbar-thumb {
    background: #c1c1c1;
    border-radius: 4px;
}

.overflow-x-auto::-webkit-scrollbar-thumb:hover {
    background: #a8a8a8;
}
</style>
