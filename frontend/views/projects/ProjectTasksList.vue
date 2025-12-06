<template>
    <div :class=" [
        isDark ? 'bg-slate-900' : 'bg-gray-50',
        'min-h-screen transition-colors duration-300'
    ] ">
        <!-- Header Section -->
        <div :class=" [
            isDark ? 'bg-slate-800 border-slate-700' : 'bg-white border-gray-200',
            'shadow-lg border-b transition-colors duration-300'
        ] ">
            <div class="max-w-full px-4 sm:px-6 lg:px-8 py-3 sm:py-4">
                <div
                    class="flex flex-col lg:flex-row justify-between items-start lg:items-center space-y-3 lg:space-y-0">
                    <div class="flex-1">
                        <!-- Breadcrumb -->
                        <nav class="mb-2 sm:mb-3">
                            <ol :class=" [
                                isDark ? 'text-slate-400' : 'text-gray-500',
                                'flex items-center space-x-2 text-sm transition-colors duration-300'
                            ] ">
                                <li>
                                    <router-link to="/projects" :class=" [
                                        isDark ? 'hover:text-cyan-400' : 'hover:text-blue-600',
                                        'transition-all duration-300 font-medium hover:underline'
                                    ] ">
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
                                    <button @click=" goToProject " :class=" [
                                        isDark ? 'hover:text-cyan-400' : 'hover:text-blue-600',
                                        'transition-all duration-300 truncate max-w-[200px] font-medium hover:underline'
                                    ] ">
                                        {{ project?.name || 'Project' }}
                                    </button>
                                </li>
                                <li>
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M9 5l7 7-7 7"></path>
                                    </svg>
                                </li>
                                <li :class=" [
                                    isDark ? 'text-slate-100' : 'text-gray-900',
                                    'font-semibold transition-colors duration-300'
                                ] ">Tasks</li>
                            </ol>
                        </nav>

                        <div class="flex items-center mb-2">
                            <div :class=" [
                                isDark ? 'bg-cyan-600' : 'bg-linear-to-br from-blue-500 to-indigo-600',
                                'w-8 h-8 rounded-xl flex items-center justify-center mr-3 shadow-lg transition-colors duration-300'
                            ] ">
                                <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                </svg>
                            </div>
                            <div>
                                <h1 :class=" [
                                    isDark ? 'text-slate-100' : 'text-gray-900',
                                    'text-xl sm:text-2xl lg:text-3xl font-bold leading-tight transition-colors duration-300'
                                ] ">
                                    Project Tasks</h1>
                                <p :class=" [
                                    isDark ? 'text-slate-300' : 'text-gray-600',
                                    'mt-0.5 text-sm transition-colors duration-300'
                                ] " v-if="project">
                                    Manage and track tasks for <span :class=" [
                                        isDark ? 'text-cyan-400' : 'text-blue-600',
                                        'font-semibold transition-colors duration-300'
                                    ] ">{{ project.name }}</span>
                                </p>
                            </div>
                        </div>
                    </div>

                    <div
                        class="flex flex-col sm:flex-row items-stretch sm:items-center space-y-2 sm:space-y-0 sm:space-x-3 lg:flex-shrink-0">
                        <button @click=" refreshTasks " :disabled=" loading " :class=" [
                            isDark ? 'bg-slate-700 text-slate-300 border-slate-600 hover:bg-slate-600' : 'bg-white text-gray-700 border-gray-200 hover:bg-gray-50',
                            'px-4 py-2 rounded-xl transition-all duration-300 flex items-center justify-center shadow-md font-medium hover:shadow-lg transform hover:-translate-y-0.5',
                            { 'opacity-50 cursor-not-allowed': loading }
                        ] ">
                            <svg class="w-4 h-4 mr-2" :class=" { 'animate-spin': loading } " fill="none"
                                stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15">
                                </path>
                            </svg>
                            Refresh
                        </button>

                        <button @click="openCreateModal()" :class=" [
                            isDark ? 'bg-cyan-600 hover:bg-cyan-700' : 'bg-blue-600 hover:bg-blue-700',
                            'px-6 py-2 rounded-xl transition-all duration-300 flex items-center justify-center shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 font-medium text-white'
                        ] ">
                            <svg class="w-4 h-4 mr-2" fill="none" stroke="white" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M12 4v16m8-8H4"></path>
                            </svg>
                            <span class="text-white">Create Task</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading && !tasks.length" class="flex flex-col justify-center items-center py-24">
            <div :class=" [
                isDark ? 'border-slate-700 border-t-cyan-400' : 'border-blue-200 border-t-blue-600',
                'animate-spin rounded-full h-16 w-16 border-4 mb-4 transition-colors duration-300'
            ] "></div>
            <p :class=" [
                isDark ? 'text-slate-300' : 'text-gray-600',
                'font-medium transition-colors duration-300'
            ] ">Loading tasks...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <div :class=" [
                isDark ? 'bg-red-900/20 border-red-800/30' : 'bg-red-50 border-red-200',
                'border-2 rounded-2xl p-8 text-center shadow-lg transition-colors duration-300'
            ] ">
                <div :class=" [
                    isDark ? 'bg-red-900/50' : 'bg-red-100',
                    'w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6 transition-colors duration-300'
                ] ">
                    <svg :class=" [
                        isDark ? 'text-red-400' : 'text-red-500',
                        'w-8 h-8 transition-colors duration-300'
                    ] " fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                </div>
                <h3 :class=" [
                    isDark ? 'text-red-300' : 'text-red-900',
                    'text-xl font-bold mb-3 transition-colors duration-300'
                ] ">Error Loading Tasks</h3>
                <p :class=" [
                    isDark ? 'text-red-400' : 'text-red-700',
                    'mb-6 max-w-md mx-auto transition-colors duration-300'
                ] ">{{ error }}</p>
                <button @click=" fetchTasks " :class=" [
                    isDark ? 'bg-red-600 hover:bg-red-700' : 'bg-red-600 hover:bg-red-700',
                    'px-6 py-3 rounded-xl transition-all duration-300 font-semibold shadow-md hover:shadow-lg transform hover:-translate-y-0.5 text-white'
                ] ">
                    Try Again
                </button>
            </div>
        </div>

        <!-- Tasks Kanban Board -->
        <div v-else class="max-w-full px-2 sm:px-4 lg:px-4 py-6 sm:py-8">
            <!-- FIXME: tasks filtering as like others filtering -->
            <!-- <div :class=" [
                isDark ? 'bg-slate-800 border-slate-700 hover:bg-slate-700/50' : 'bg-white border-gray-200 hover:shadow-md',
                'rounded-lg shadow-sm border px-3 py-2 mb-4 transition-all duration-300'
            ] ">
                <div class="flex items-center justify-between">
                    <div class="flex items-center">
                        <div :class=" [
                            isDark ? 'bg-violet-600' : 'bg-gradient-to-br from-indigo-500 to-purple-600',
                            'w-4 h-4 rounded flex items-center justify-center mr-2 transition-colors duration-300'
                        ] ">
                            <svg class="w-2.5 h-2.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z">
                                </path>
                            </svg>
                        </div>
                        <h2 :class=" [
                            isDark ? 'text-slate-100' : 'text-gray-900',
                            'text-sm font-semibold transition-colors duration-300'
                        ] ">Tasks Overview</h2>
                    </div>

                    <div class="flex items-center space-x-3 overflow-x-auto">
                        <p>Filtering will be later</p>
                    </div>
                </div>
            </div> -->

            <!-- Kanban Board -->
            <div class="overflow-x-auto scrollbar-modern">
                <div class="flex space-x-4 pb-8" style="min-width: max-content;">
                    <div v-for="status in taskStatuses" :key=" status.id " class="flex-shrink-0 w-80 sm:w-96">
                        <!-- Sticky Header -->
                        <div :class=" [
                            isDark ? 'bg-slate-800 border-slate-700 hover:bg-slate-700/50' : 'bg-white border-gray-200 hover:shadow-xl',
                            'rounded-t-md shadow-lg border transition-all duration-300 sticky top-0 z-20'
                        ] ">
                            <div :class=" [
                                isDark ? 'border-slate-700' : 'border-gray-200',
                                'px-4 sm:px-6 py-1.5 border-b transition-colors duration-300'
                            ] ">
                                <div class="flex items-center justify-between">
                                    <div class="flex items-center">
                                        <div class="w-4 h-4 rounded-full mr-3 shadow-sm"
                                            :class=" getStatusColor(status.id, 'bg') "></div>
                                        <h3 :class=" [
                                            isDark ? 'text-slate-100' : 'text-gray-900',
                                            'font-bold text-lg transition-colors duration-300'
                                        ] ">{{ status.name }}</h3>
                                        <span class="ml-3 px-3 py-1 text-xs font-semibold rounded-full shadow-sm"
                                            :class=" getStatusColor(status.id, 'bg') + ' ' + getStatusColor(status.id, 'text') ">
                                            {{ getTasksInStatus(status.id).length }}
                                        </span>
                                    </div>
                                    <button @click="openCreateModal(status.id)" :class=" [
                                        isDark ? 'text-slate-400 hover:text-cyan-400 hover:bg-slate-600' : 'text-gray-400 hover:text-blue-600 hover:bg-blue-50',
                                        'transition-all duration-300 p-2 rounded-lg'
                                    ] ">
                                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M12 4v16m8-8H4" />
                                        </svg>
                                    </button>
                                </div>
                            </div>
                        </div>

                        <!-- Independent Scrollable Tasks -->
                        <div :class=" [
                            isDark ? 'bg-slate-700/30' : 'bg-gray-50',
                            'space-y-4 min-h-[400px] max-h-[calc(100vh-220px)] overflow-y-auto p-2 rounded-b-xl status-column transition-all duration-200',
                            {
                                'bg-cyan-900/20 border border-cyan-600/50 border-dashed': isDark && draggedOverStatus === status.id && draggedTask && canStatusChange(draggedTask),
                                'bg-blue-50 border border-blue-300 border-dashed': !isDark && draggedOverStatus === status.id && draggedTask && canStatusChange(draggedTask)
                            }
                        ] " @dragover="onDragOver($event, status.id)" @dragleave=" onDragLeave "
                            @drop="onDrop($event, status.id)">
                            <TaskCard v-for="task in getTasksInStatus(status.id)" :key=" task.id " :task=" task "
                                :statuses=" taskStatuses " :allow-status-change=" canStatusChange(task) "
                                @edit=" openEditModal " @delete=" deleteTask " @status-change=" updateTaskStatus "
                                @dragstart="onDragStart($event, task)" @dragend=" onDragEnd "
                                :draggable=" canStatusChange(task) "
                                class="hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1"
                                :class=" {
                                    'opacity-50 transform rotate-1 scale-95': draggedTask && draggedTask.id === task.id,
                                    'cursor-grab': canStatusChange(task),
                                    'cursor-not-allowed': !canStatusChange(task)
                                } " />

                            <!-- Empty State -->
                            <div v-if="getTasksInStatus(status.id).length === 0" :class=" [
                                isDark ? 'text-slate-500' : 'text-gray-400',
                                'text-center py-12 transition-all duration-200',
                                {
                                    'text-cyan-400': isDark && draggedOverStatus === status.id && draggedTask && canStatusChange(draggedTask),
                                    'text-blue-600': !isDark && draggedOverStatus === status.id && draggedTask && canStatusChange(draggedTask)
                                }
                            ] ">
                                <div :class=" [
                                    isDark ? 'bg-slate-600/50' : 'bg-gray-100',
                                    'w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-sm transition-all duration-200',
                                    {
                                        'bg-cyan-900/50 border-2 border-cyan-600/50 border-dashed': isDark && draggedOverStatus === status.id && draggedTask && canStatusChange(draggedTask),
                                        'bg-blue-100 border-2 border-blue-300 border-dashed': !isDark && draggedOverStatus === status.id && draggedTask && canStatusChange(draggedTask)
                                    }
                                ] ">
                                    <svg class="w-8 h-8" :class=" {
                                        'text-cyan-400': isDark && draggedOverStatus === status.id && draggedTask && canStatusChange(draggedTask),
                                        'text-blue-500': !isDark && draggedOverStatus === status.id && draggedTask && canStatusChange(draggedTask),
                                        'text-slate-500': isDark && !(draggedOverStatus === status.id && draggedTask && canStatusChange(draggedTask)),
                                        'text-gray-400': !isDark && !(draggedOverStatus === status.id && draggedTask && canStatusChange(draggedTask))
                                    } " fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                    </svg>
                                </div>
                                <p class="text-sm font-medium" :class=" {
                                    'text-cyan-400': isDark && draggedOverStatus === status.id && draggedTask && canStatusChange(draggedTask),
                                    'text-blue-600': !isDark && draggedOverStatus === status.id && draggedTask && canStatusChange(draggedTask),
                                    'text-slate-400': isDark && !(draggedOverStatus === status.id && draggedTask && canStatusChange(draggedTask)),
                                    'text-gray-500': !isDark && !(draggedOverStatus === status.id && draggedTask && canStatusChange(draggedTask))
                                } ">
                                    {{ draggedOverStatus === status.id && draggedTask && canStatusChange(draggedTask) ?
                                        'Drop task here' : 'No tasks in this status' }}
                                </p>
                                <button
                                    v-if="!(draggedOverStatus === status.id && draggedTask && canStatusChange(draggedTask))"
                                    @click="openCreateModal(status.id)" :class=" [
                                        isDark ? 'text-cyan-400 hover:text-cyan-300' : 'text-blue-600 hover:text-blue-800',
                                        'mt-3 text-sm font-semibold transition-colors duration-200 hover:underline'
                                    ] ">
                                    Add a task
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>


            <!-- Empty State - No Statuses -->
            <div v-if="!loading && taskStatuses.length === 0" class="text-center py-24">
                <div :class=" [
                    isDark ? 'bg-slate-700/50' : 'bg-gray-100',
                    'w-20 h-20 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-sm transition-colors duration-300'
                ] ">
                    <svg :class=" [
                        isDark ? 'text-slate-500' : 'text-gray-400',
                        'w-10 h-10 transition-colors duration-300'
                    ] " fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z">
                        </path>
                    </svg>
                </div>
                <h3 :class=" [
                    isDark ? 'text-slate-100' : 'text-gray-900',
                    'text-2xl font-bold mb-3 transition-colors duration-300'
                ] ">No task statuses found</h3>
                <p :class=" [
                    isDark ? 'text-slate-400' : 'text-gray-600',
                    'mb-8 max-w-md mx-auto transition-colors duration-300'
                ] ">Contact your organization admin to set up task statuses
                    before you can start managing tasks</p>
                <div class="flex flex-col sm:flex-row gap-3 justify-center items-center">
                    <button @click=" fetchTaskStatuses " :class=" [
                        isDark ? 'bg-slate-600 hover:bg-slate-700' : 'bg-gray-600 hover:bg-gray-700',
                        'px-6 py-3 rounded-xl transition-all duration-300 font-semibold shadow-md hover:shadow-lg transform hover:-translate-y-0.5 text-white'
                    ] ">
                        Refresh Statuses
                    </button>
                </div>
            </div>
        </div>

        <!-- Create Task Modal -->
        <CreateTaskModal :is-open=" showCreateModal " :project-id=" projectId " :project-slug=" projectSlug "
            :initial-status-id=" selectedStatusId " :statuses=" taskStatuses " @close=" closeCreateModal "
            @created=" onTaskCreated " />

        <!-- Edit Task Modal -->
        <EditTaskModal :is-open=" showEditModal " :task=" selectedTask " :project-slug=" projectSlug "
            :statuses=" taskStatuses " @close=" closeEditModal " @updated=" onTaskUpdated " />
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
import { useTheme } from '@/composables/useTheme.js'

const router = useRouter()
const route = useRoute()
const $toast = inject("toast")
const authStore = useAuthStore()
const { isDark } = useTheme()

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
onMounted(async () => {
    await initializeData();
    const { task_id = null } = route.query;
    const taskId = isNaN(parseInt(task_id)) ? null : parseInt(task_id);
    if (taskId) {
        const task = tasks.value.find(({ id }) => taskId === id);
        if (task) {
            selectedTask.value = task;
            showEditModal.value = true;
            router.replace({ query: { ...route.query, task_id: undefined } });
        }
    }
})
</script>

<style scoped>
/* Keep only essential animations and styles that can't be done with Tailwind */
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

/* Status column scrollbars */
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
</style>
