<template>
    <div class="min-h-screen bg-gray-50">
        <!-- Header Section -->
        <div class="bg-white shadow-lg border-b border-gray-200">
            <div class="max-w-full px-4 sm:px-6 lg:px-8 py-3 sm:py-4">
                <div
                    class="flex flex-col lg:flex-row justify-between items-start lg:items-center space-y-3 lg:space-y-0">
                    <div class="flex-1">
                        <!-- Breadcrumb -->
                        <nav class="mb-2 sm:mb-3">
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

                        <div class="flex items-center mb-2">
                            <div
                                class="w-8 h-8 bg-linear-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center mr-3 shadow-lg">
                                <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                </svg>
                            </div>
                            <div>
                                <h1 class="text-xl sm:text-2xl lg:text-3xl font-bold text-gray-900 leading-tight">
                                    Project Tasks</h1>
                                <p class="mt-0.5 text-gray-600 text-sm" v-if="project">
                                    Manage and track tasks for <span class="font-semibold text-blue-600">{{ project.name
                                    }}</span>
                                </p>
                            </div>
                        </div>
                    </div>

                    <div
                        class="flex flex-col sm:flex-row items-stretch sm:items-center space-y-2 sm:space-y-0 sm:space-x-3 lg:flex-shrink-0">
                        <button @click="refreshTasks" :disabled="loading"
                            class="bg-white text-gray-700 px-4 py-2 rounded-xl hover:bg-gray-50 transition-all duration-300 flex items-center justify-center shadow-md border border-gray-200 font-medium hover:shadow-lg transform hover:-translate-y-0.5"
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
                            class="bg-blue-600 px-6 py-2 rounded-xl hover:bg-blue-700 transition-all duration-300 flex items-center justify-center shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 font-medium"
                            style="color: white !important;">
                            <svg class="w-4 h-4 mr-2" fill="none" stroke="white" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M12 4v16m8-8H4"></path>
                            </svg>
                            <span style="color: white !important;">Create Task</span>
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
            <div class="bg-red-50 border-2 border-red-200 rounded-2xl p-8 text-center shadow-lg">
                <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6">
                    <svg class="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                </div>
                <h3 class="text-xl font-bold text-red-900 mb-3">Error Loading Tasks</h3>
                <p class="text-red-700 mb-6 max-w-md mx-auto">{{ error }}</p>
                <button @click="fetchTasks"
                    class="bg-red-600 px-6 py-3 rounded-xl hover:bg-red-700 transition-all duration-300 font-semibold shadow-md hover:shadow-lg transform hover:-translate-y-0.5"
                    style="color: white !important;">
                    Try Again
                </button>
            </div>
        </div>

        <!-- Tasks Kanban Board -->
        <div v-else class="max-w-full px-2 sm:px-4 lg:px-4 py-6 sm:py-8">
            <!-- Status Statistics -->
            <div
                class="bg-white rounded-lg shadow-sm border border-gray-200 px-3 py-2 mb-4 hover:shadow-md transition-all duration-300">
                <div class="flex items-center justify-between">
                    <div class="flex items-center">
                        <div
                            class="w-4 h-4 bg-gradient-to-br from-indigo-500 to-purple-600 rounded flex items-center justify-center mr-2">
                            <svg class="w-2.5 h-2.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z">
                                </path>
                            </svg>
                        </div>
                        <h2 class="text-sm font-semibold text-gray-900">Tasks Overview</h2>
                    </div>

                    <!-- Status indicators on the right -->
                    <div class="flex items-center space-x-3 overflow-x-auto">
                        <div v-for="status in taskStatuses" :key="status.id"
                            class="flex items-center space-x-1.5 px-2 py-1 rounded-md border transition-all duration-200 hover:shadow-sm flex-shrink-0"
                            :class="getStatusColor(status.id, 'bg') + ' ' + getStatusColor(status.id, 'border')">
                            <div class="w-5 h-5 rounded flex items-center justify-center"
                                :class="getStatusColor(status.id, 'bg')">
                                <span class="text-xs font-bold" :class="getStatusColor(status.id, 'text')">
                                    {{ getTasksInStatus(status.id).length }}
                                </span>
                            </div>
                            <span class="text-xs font-medium text-gray-700 whitespace-nowrap">{{ status.name }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Kanban Board -->
            <div class="overflow-x-auto scrollbar-modern">
                <div class="flex space-x-4 pb-8" style="min-width: max-content;">
                    <div v-for="status in taskStatuses" :key="status.id" class="flex-shrink-0 w-80 sm:w-96">
                        <!-- Sticky Header -->
                        <div
                            class="bg-white rounded-t-xl shadow-lg border border-gray-200 hover:shadow-xl transition-all duration-300 sticky top-0 z-20">
                            <div class="px-4 sm:px-6 py-4 border-b border-gray-200">
                                <div class="flex items-center justify-between">
                                    <div class="flex items-center">
                                        <div class="w-4 h-4 rounded-full mr-3 shadow-sm"
                                            :class="getStatusColor(status.id, 'bg')"></div>
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
                                                d="M12 4v16m8-8H4" />
                                        </svg>
                                    </button>
                                </div>
                            </div>
                        </div>

                        <!-- Independent Scrollable Tasks -->
                        <div class="space-y-4 min-h-[400px] max-h-[calc(100vh-220px)] overflow-y-auto p-2 bg-gray-50 rounded-b-xl status-column transition-all duration-200"
                            :class="{
                                'bg-blue-50 border-2 border-blue-300 border-dashed': draggedOverStatus === status.id && draggedTask && canStatusChange(draggedTask),
                                'bg-gray-50': draggedOverStatus !== status.id || !draggedTask || !canStatusChange(draggedTask)
                            }" @dragover="onDragOver($event, status.id)" @dragleave="onDragLeave"
                            @drop="onDrop($event, status.id)">
                            <TaskCard v-for="task in getTasksInStatus(status.id)" :key="task.id" :task="task"
                                :statuses="taskStatuses" :allow-status-change="canStatusChange(task)"
                                @edit="openEditModal" @delete="deleteTask" @status-change="updateTaskStatus"
                                @dragstart="onDragStart($event, task)" @dragend="onDragEnd"
                                :draggable="canStatusChange(task)"
                                class="hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1"
                                :class="{
                                    'opacity-50 transform rotate-1 scale-95': draggedTask && draggedTask.id === task.id,
                                    'cursor-grab': canStatusChange(task),
                                    'cursor-not-allowed': !canStatusChange(task)
                                }" />

                            <!-- Empty State -->
                            <div v-if="getTasksInStatus(status.id).length === 0"
                                class="text-center py-12 text-gray-400 transition-all duration-200" :class="{
                                    'text-blue-600': draggedOverStatus === status.id && draggedTask && canStatusChange(draggedTask)
                                }">
                                <div class="w-16 h-16 bg-gray-100 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-sm transition-all duration-200"
                                    :class="{
                                        'bg-blue-100 border-2 border-blue-300 border-dashed': draggedOverStatus === status.id && draggedTask && canStatusChange(draggedTask)
                                    }">
                                    <svg class="w-8 h-8" :class="{
                                        'text-blue-500': draggedOverStatus === status.id && draggedTask && canStatusChange(draggedTask),
                                        'text-gray-400': !(draggedOverStatus === status.id && draggedTask && canStatusChange(draggedTask))
                                    }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                    </svg>
                                </div>
                                <p class="text-sm font-medium" :class="{
                                    'text-blue-600': draggedOverStatus === status.id && draggedTask && canStatusChange(draggedTask),
                                    'text-gray-500': !(draggedOverStatus === status.id && draggedTask && canStatusChange(draggedTask))
                                }">
                                    {{ draggedOverStatus === status.id && draggedTask && canStatusChange(draggedTask) ?
                                    'Drop task here' : 'No tasks in this status' }}
                                </p>
                                <button
                                    v-if="!(draggedOverStatus === status.id && draggedTask && canStatusChange(draggedTask))"
                                    @click="openCreateModal(status.id)"
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
                <div class="w-20 h-20 bg-gray-100 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-sm">
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
                        class="bg-gray-600 px-6 py-3 rounded-xl hover:bg-gray-700 transition-all duration-300 font-semibold shadow-md hover:shadow-lg transform hover:-translate-y-0.5"
                        style="color: white !important;">
                        Refresh Statuses
                    </button>
                </div>
            </div>
        </div>

        <!-- Create Task Modal -->
        <CreateTaskModal :is-open="showCreateModal" :project-id="projectId" :project-slug="projectSlug"
            :initial-status-id="selectedStatusId" :statuses="taskStatuses" @close="closeCreateModal"
            @created="onTaskCreated" />

        <!-- Edit Task Modal -->
        <EditTaskModal :is-open="showEditModal" :task="selectedTask" :project-slug="projectSlug"
            :statuses="taskStatuses" @close="closeEditModal" @updated="onTaskUpdated" />
    </div>
</template>

<script setup>
import { ref, onMounted, computed, inject } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from "@/plugins/axiosConfig.js"
import { useAuthStore } from '@/stores/auth.js'
import TaskCard from '@/components/tasks/TaskCard.vue'
import CreateTaskModal from '@/components/modals/CreateTaskModal.vue'
import EditTaskModal from '@/components/modals/EditTaskModal.vue'

const router = useRouter()
const route = useRoute()
const $toast = inject("toast")
const authStore = useAuthStore()

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

// Drag and drop state
const draggedTask = ref(null)
const draggedOverStatus = ref(null)

// Get project slug from route
const projectSlug = computed(() => route.params.slug)

// Get project ID from project data for nested API calls
const projectId = computed(() => {
    if (project.value?.id) {
        return project.value.id
    }
    return null
})

// Status color mapping based on status names
const statusColorMapping = {
    // Fixed status colors
    'todo': { bg: 'bg-gray-100', text: 'text-gray-700', gradient: 'from-gray-50 to-gray-100', border: 'border-gray-200' },
    'in progress': { bg: 'bg-blue-100', text: 'text-blue-700', gradient: 'from-blue-50 to-blue-100', border: 'border-blue-200' },
    'review': { bg: 'bg-yellow-100', text: 'text-yellow-700', gradient: 'from-yellow-50 to-yellow-100', border: 'border-yellow-200' },
    'done': { bg: 'bg-green-100', text: 'text-green-700', gradient: 'from-green-50 to-green-100', border: 'border-green-200' },
    'closed': { bg: 'bg-red-100', text: 'text-red-700', gradient: 'from-red-50 to-red-100', border: 'border-red-200' },
}

// Fallback colors for dynamic statuses
const fallbackColors = [
    { bg: 'bg-purple-100', text: 'text-purple-700', gradient: 'from-purple-50 to-purple-100', border: 'border-purple-200' },
    { bg: 'bg-pink-100', text: 'text-pink-700', gradient: 'from-pink-50 to-pink-100', border: 'border-pink-200' },
    { bg: 'bg-indigo-100', text: 'text-indigo-700', gradient: 'from-indigo-50 to-indigo-100', border: 'border-indigo-200' },
    { bg: 'bg-teal-100', text: 'text-teal-700', gradient: 'from-teal-50 to-teal-100', border: 'border-teal-200' },
    { bg: 'bg-orange-100', text: 'text-orange-700', gradient: 'from-orange-50 to-orange-100', border: 'border-orange-200' },
    { bg: 'bg-cyan-100', text: 'text-cyan-700', gradient: 'from-cyan-50 to-cyan-100', border: 'border-cyan-200' },
    { bg: 'bg-emerald-100', text: 'text-emerald-700', gradient: 'from-emerald-50 to-emerald-100', border: 'border-emerald-200' },
    { bg: 'bg-violet-100', text: 'text-violet-700', gradient: 'from-violet-50 to-violet-100', border: 'border-violet-200' },
]

// Default color for unknown statuses
const defaultColor = { bg: 'bg-slate-100', text: 'text-slate-700', gradient: 'from-slate-50 to-slate-100', border: 'border-slate-200' }

// Get tasks for specific status
const getTasksInStatus = (statusId) => {
    return tasks.value.filter(task => task.status?.id === statusId)
}

// Get status color based on status name
const getStatusColor = (statusId, type) => {
    if (!statusId || !taskStatuses.value) {
        return defaultColor[type] || ''
    }

    // Find the status object
    const status = taskStatuses.value.find(s => s.id === statusId)
    if (!status) {
        return defaultColor[type] || ''
    }

    // Convert status name to lowercase for matching
    const statusName = status.name.toLowerCase().trim()

    // Check if it's a fixed status
    if (statusColorMapping[statusName]) {
        return statusColorMapping[statusName][type] || ''
    }

    // Use fallback colors for dynamic statuses
    const statusIndex = taskStatuses.value.findIndex(s => s.id === statusId)
    const colorIndex = statusIndex >= 0 ? statusIndex % fallbackColors.length : 0

    return fallbackColors[colorIndex][type] || ''
}

// Fetch project details
const fetchProject = async () => {
    try {
        const slug = projectSlug.value

        if (!slug) {
            throw new Error('Missing project slug')
        }
        const response = await axios.get(`projects/${slug}/`)

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
            error.value = 'Project not loaded yet - cannot fetch tasks'
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

    try {
        // First fetch project to get the project ID
        await fetchProject()

        // Then fetch tasks and statuses in parallel
        await Promise.all([
            fetchTaskStatuses(),
            fetchTasks()
        ])
    } catch (err) {
        console.error('Failed to initialize data:', err)
    } finally {
        loading.value = false
    }
}

// Refresh tasks
const refreshTasks = () => {
    fetchTasks()
}

// Navigate back to project
const goToProject = () => {
    const slug = project.value?.slug
    if (slug) {
        router.push(`/projects/${slug}`)
    }
}

// Modal handlers
const openCreateModal = (statusId = null) => {
    const currentProjectId = projectId.value
    console.log('openCreateModal: project ID =', currentProjectId)

    if (!currentProjectId) {
        console.error('openCreateModal: No project ID available. Project data:', project.value)
        $toast?.error('Project not loaded yet. Please wait and try again.')
        return
    }

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

// const onTaskUpdatedFromView = (updatedTask) => {
//     const index = tasks.value.findIndex(t => t.id === updatedTask.id)
//     if (index !== -1) {
//         tasks.value[index] = updatedTask
//     }
// }

// const onTaskDeletedFromView = (taskId) => {
//     tasks.value = tasks.value.filter(t => t.id !== taskId)
//     closeViewModal()
// }

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

const canStatusChange = (task) => {
    // Cannot change status of closed tasks
    if (task.status?.name.toLowerCase() === 'closed') {
        return false
    }

    // Managers can change any task status in their project
    if (task.my_project_role === 'manager') {
        return true
    }

    // Contributors can only change status of tasks they are assigned to
    if (task.my_project_role === 'contributor') {
        const currentUserId = authStore.myInfo?.id
        if (currentUserId && task.assigned_members.some(member => member.id === currentUserId)) {
            return true
        }
    }

    // All other cases: no permission to change status
    return false
}

// Drag and drop handlers
const onDragStart = (event, task) => {
    if (!canStatusChange(task)) {
        event.preventDefault()
        return
    }
    draggedTask.value = task
    event.dataTransfer.effectAllowed = 'move'
    event.dataTransfer.setData('text/html', '')

    // Add visual feedback
    if (event.target) {
        event.target.style.opacity = '0.5'
        event.target.style.transform = 'rotate(1deg) scale(0.95)'
    }
}

const onDragEnd = (event) => {
    // Reset visual feedback
    if (event.target) {
        event.target.style.opacity = ''
        event.target.style.transform = ''
    }

    draggedTask.value = null
    draggedOverStatus.value = null
}

const onDragOver = (event, statusId) => {
    if (draggedTask.value && canStatusChange(draggedTask.value)) {
        event.preventDefault()
        draggedOverStatus.value = statusId
    }
}

const onDragLeave = () => {
    draggedOverStatus.value = null
}

const onDrop = async (event, statusId) => {
    event.preventDefault()

    if (draggedTask.value && canStatusChange(draggedTask.value) && draggedTask.value.status?.id !== statusId) {
        await updateTaskStatus(draggedTask.value.id, statusId)
    }

    draggedTask.value = null
    draggedOverStatus.value = null
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

.status-column::-webkit-scrollbar {
    width: 8px;
}

.status-column::-webkit-scrollbar-thumb {
    background-color: rgba(100, 116, 139, 0.3);
    border-radius: 8px;
}

.status-column::-webkit-scrollbar-thumb:hover {
    background-color: rgba(100, 116, 139, 0.5);
}

/* Drag and Drop Styles */
.drag-ghost {
    opacity: 0.5;
    transform: rotate(2deg) scale(0.95);
    z-index: 1000;
}

.drag-over {
    background-color: rgba(59, 130, 246, 0.1) !important;
    border-color: rgba(59, 130, 246, 0.3) !important;
    transform: scale(1.02);
}

.drop-zone {
    transition: all 0.3s ease;
    border: 2px dashed transparent;
}

.drop-zone-active {
    border-color: #3b82f6;
    background-color: rgba(59, 130, 246, 0.05);
    transform: scale(1.01);
}

.task-draggable {
    cursor: grab;
    transition: all 0.2s ease;
}

.task-draggable:active {
    cursor: grabbing;
}

.task-being-dragged {
    opacity: 0.5;
    transform: rotate(1deg) scale(0.95);
    cursor: grabbing;
}

.task-not-draggable {
    cursor: not-allowed;
    opacity: 0.7;
}

@keyframes dropZonePulse {

    0%,
    100% {
        background-color: rgba(59, 130, 246, 0.05);
    }

    50% {
        background-color: rgba(59, 130, 246, 0.1);
    }
}

.drop-zone-pulse {
    animation: dropZonePulse 1.5s ease-in-out infinite;
}
</style>
