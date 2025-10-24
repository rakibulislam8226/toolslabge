<template>
    <div class="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
        <!-- Header Section -->
        <div class="bg-gradient-to-r from-white to-blue-50 shadow-lg border-b border-blue-100">
            <div class="max-w-full px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
                <div
                    class="flex flex-col lg:flex-row justify-between items-start lg:items-center space-y-4 lg:space-y-0">
                    <div class="flex-1">
                        <!-- Breadcrumb -->
                        <nav class="mb-4 sm:mb-6">
                            <ol class="flex items-center space-x-2 text-sm text-gray-500">
                                <li>
                                    <router-link to="/projects"
                                        class="hover:text-blue-600 transition-all duration-300 font-medium hover:underline">
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
                                        class="hover:text-blue-600 transition-all duration-300 truncate max-w-[200px] font-medium hover:underline">
                                        {{ project?.name || 'Project' }}
                                    </button>
                                </li>
                                <li>
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M9 5l7 7-7 7"></path>
                                    </svg>
                                </li>
                                <li class="text-gray-900 font-semibold">Tasks</li>
                            </ol>
                        </nav>

                        <div class="flex items-center mb-4">
                            <div
                                class="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center mr-4 shadow-lg">
                                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                </svg>
                            </div>
                            <div>
                                <h1 class="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900 leading-tight">
                                    Project Tasks</h1>
                                <p class="mt-1 text-gray-600 text-sm sm:text-base" v-if="project">
                                    Manage and track tasks for <span class="font-semibold text-blue-600">{{ project.name
                                        }}</span>
                                </p>
                            </div>
                        </div>
                    </div>

                    <div
                        class="flex flex-col sm:flex-row items-stretch sm:items-center space-y-3 sm:space-y-0 sm:space-x-3 lg:flex-shrink-0">
                        <button @click="refreshTasks" :disabled="loading"
                            class="bg-white text-gray-700 px-4 py-2.5 rounded-xl hover:bg-gray-50 transition-all duration-300 flex items-center justify-center shadow-md border border-gray-200 font-medium hover:shadow-lg transform hover:-translate-y-0.5"
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
                            class="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-6 py-2.5 rounded-xl hover:from-blue-700 hover:to-indigo-700 transition-all duration-300 flex items-center justify-center shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 font-medium">
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
        <div v-if="loading && !tasks.length" class="flex flex-col justify-center items-center py-24">
            <div class="animate-spin rounded-full h-16 w-16 border-4 border-blue-200 border-t-blue-600 mb-4"></div>
            <p class="text-gray-600 font-medium">Loading tasks...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <div
                class="bg-gradient-to-br from-red-50 to-red-100 border-2 border-red-200 rounded-2xl p-8 text-center shadow-lg">
                <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6">
                    <svg class="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                </div>
                <h3 class="text-xl font-bold text-red-900 mb-3">Error Loading Tasks</h3>
                <p class="text-red-700 mb-6 max-w-md mx-auto">{{ error }}</p>
                <button @click="fetchTasks"
                    class="bg-gradient-to-r from-red-600 to-red-700 text-white px-6 py-3 rounded-xl hover:from-red-700 hover:to-red-800 transition-all duration-300 font-semibold shadow-md hover:shadow-lg transform hover:-translate-y-0.5">
                    Try Again
                </button>
            </div>
        </div>

        <!-- Tasks Kanban Board -->
        <div v-else class="max-w-full px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
            <!-- Status Statistics -->
            <div
                class="bg-gradient-to-br from-white to-indigo-50 rounded-2xl shadow-lg border border-indigo-100 p-4 sm:p-6 lg:p-8 mb-8 hover:shadow-xl transition-all duration-300">
                <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-4 sm:mb-6">
                    <div class="flex items-center mb-4 sm:mb-0">
                        <div
                            class="w-8 h-8 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center mr-3 shadow-sm">
                            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z">
                                </path>
                            </svg>
                        </div>
                        <h2 class="text-lg sm:text-xl lg:text-2xl font-bold text-gray-900">Task Overview</h2>
                    </div>
                    <div class="text-sm text-gray-600 font-medium">
                        {{ tasks.length }} total tasks
                    </div>
                </div>

                <!-- Horizontal scrollable status cards -->
                <div class="overflow-x-auto scrollbar-modern">
                    <div class="flex justify-between pb-2" style="min-width: max-content;">
                        <div v-for="status in taskStatuses" :key="status.id"
                            class="text-center p-4 bg-white bg-opacity-70 rounded-xl border border-white shadow-sm hover:shadow-md transition-all duration-300 transform hover:-translate-y-1 flex-1 mx-2 min-w-[120px] max-w-[200px]">
                            <div class="w-12 h-12 sm:w-14 sm:h-14 rounded-2xl flex items-center justify-center mx-auto mb-3 shadow-sm transition-all duration-300"
                                :class="getStatusColor(status.id, 'bg')">
                                <span class="text-base sm:text-lg font-bold" :class="getStatusColor(status.id, 'text')">
                                    {{ getTasksInStatus(status.id).length }}
                                </span>
                            </div>
                            <p class="text-xs sm:text-sm font-semibold text-gray-900 truncate px-1">{{ status.name }}
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Kanban Board -->
            <div class="overflow-x-auto scrollbar-modern">
                <div class="flex space-x-6 pb-8" style="min-width: max-content;">
                    <div v-for="status in taskStatuses" :key="status.id" class="flex-shrink-0 w-80 sm:w-96">
                        <!-- Status Column Header -->
                        <div
                            class="bg-gradient-to-br from-white to-gray-50 rounded-xl shadow-lg border border-gray-200 mb-4 hover:shadow-xl transition-all duration-300">
                            <div class="px-4 sm:px-6 py-4 border-b border-gray-200">
                                <div class="flex items-center justify-between">
                                    <div class="flex items-center">
                                        <div class="w-4 h-4 rounded-full mr-3 shadow-sm"
                                            :class="getStatusColor(status.id, 'bg')">
                                        </div>
                                        <h3 class="font-bold text-gray-900 text-lg">{{ status.name }}</h3>
                                        <span class="ml-3 px-3 py-1 text-xs font-semibold rounded-full shadow-sm"
                                            :class="getStatusColor(status.id, 'bg') + ' ' + getStatusColor(status.id, 'text')">
                                            {{ getTasksInStatus(status.id).length }}
                                        </span>
                                    </div>
                                    <button @click="openCreateModal(status.id)"
                                        class="text-gray-400 hover:text-blue-600 transition-all duration-300 p-2 rounded-lg hover:bg-blue-50">
                                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M12 4v16m8-8H4"></path>
                                        </svg>
                                    </button>
                                </div>
                            </div>
                        </div>

                        <!-- Tasks in Status Column -->
                        <div class="space-y-4 min-h-[400px] p-2 bg-gradient-to-b from-gray-50 to-white rounded-xl">
                            <TaskCard v-for="task in getTasksInStatus(status.id)" :key="task.id" :task="task"
                                :statuses="taskStatuses" @edit="openEditModal" @delete="deleteTask"
                                @status-change="updateTaskStatus"
                                class="hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1" />

                            <!-- Empty State -->
                            <div v-if="getTasksInStatus(status.id).length === 0"
                                class="text-center py-12 text-gray-400">
                                <div
                                    class="w-16 h-16 bg-gradient-to-br from-gray-100 to-gray-200 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-sm">
                                    <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor"
                                        viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z">
                                        </path>
                                    </svg>
                                </div>
                                <p class="text-sm font-medium text-gray-500">No tasks in this status</p>
                                <button @click="openCreateModal(status.id)"
                                    class="mt-3 text-blue-600 hover:text-blue-800 text-sm font-semibold transition-colors duration-200 hover:underline">
                                    Add a task
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Empty State - No Statuses -->
            <div v-if="!loading && taskStatuses.length === 0" class="text-center py-24">
                <div
                    class="w-20 h-20 bg-gradient-to-br from-gray-100 to-gray-200 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-sm">
                    <svg class="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z">
                        </path>
                    </svg>
                </div>
                <h3 class="text-2xl font-bold text-gray-900 mb-3">No task statuses found</h3>
                <p class="text-gray-600 mb-8 max-w-md mx-auto">Contact your organization admin to set up task statuses
                    before you can start managing tasks</p>
                <div class="flex flex-col sm:flex-row gap-3 justify-center items-center">
                    <button @click="fetchTaskStatuses"
                        class="bg-gradient-to-r from-gray-600 to-gray-700 text-white px-6 py-3 rounded-xl hover:from-gray-700 hover:to-gray-800 transition-all duration-300 font-semibold shadow-md hover:shadow-lg transform hover:-translate-y-0.5">
                        Refresh Statuses
                    </button>
                </div>
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

/* Modern scrollbar styling */
.scrollbar-modern::-webkit-scrollbar {
    height: 10px;
}

.scrollbar-modern::-webkit-scrollbar-track {
    background: linear-gradient(90deg, #f8fafc, #e2e8f0);
    border-radius: 8px;
}

.scrollbar-modern::-webkit-scrollbar-thumb {
    background: linear-gradient(90deg, #cbd5e1, #94a3b8);
    border-radius: 8px;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
}

.scrollbar-modern::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(90deg, #94a3b8, #64748b);
}

/* Enhanced animations */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-30px);
    }

    to {
        opacity: 1;
        transform: translateX(0);
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

.slide-in-left {
    animation: slideInLeft 0.8s ease-out;
}

.slide-in-right {
    animation: slideInRight 0.8s ease-out;
}

/* Card hover effects */
.hover-lift {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.hover-lift:hover {
    transform: translateY(-8px);
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15);
}

/* Button improvements */
.btn-gradient {
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    box-shadow: 0 4px 15px 0 rgba(59, 130, 246, 0.3);
    transition: all 0.3s ease;
}

.btn-gradient:hover {
    box-shadow: 0 8px 25px 0 rgba(59, 130, 246, 0.4);
    transform: translateY(-2px);
}

/* Glass morphism effects */
.glass-effect {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.3);
}

.glass-effect-light {
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Kanban column styling */
.kanban-column {
    background: linear-gradient(145deg, #ffffff, #f8fafc);
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    transition: all 0.3s ease;
}

.kanban-column:hover {
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    transform: translateY(-2px);
}

/* Status indicator animations */
.status-indicator {
    position: relative;
    overflow: hidden;
}

.status-indicator::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
    transition: left 0.5s ease;
}

.status-indicator:hover::before {
    left: 100%;
}

/* Loading skeleton animations */
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

/* Pulse effect for loading states */
.pulse {
    animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {

    0%,
    100% {
        opacity: 1;
    }

    50% {
        opacity: .5;
    }
}

/* Mobile-specific improvements */
@media (max-width: 640px) {
    .mobile-stack {
        flex-direction: column;
        align-items: stretch;
    }

    .mobile-full-width {
        width: 100%;
    }

    .kanban-column {
        min-width: 280px;
    }
}

@media (max-width: 480px) {
    .kanban-column {
        min-width: 260px;
    }
}

/* Improved focus states for accessibility */
button:focus,
.focusable:focus {
    outline: 2px solid #3b82f6;
    outline-offset: 2px;
}

/* Enhanced transitions */
.transition-all-smooth {
    transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

/* Gradient text effects */
.text-gradient {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* Custom shadows */
.shadow-soft {
    box-shadow: 0 2px 15px 0 rgba(0, 0, 0, 0.08);
}

.shadow-medium {
    box-shadow: 0 4px 25px 0 rgba(0, 0, 0, 0.12);
}

.shadow-strong {
    box-shadow: 0 8px 40px 0 rgba(0, 0, 0, 0.16);
}
</style>
