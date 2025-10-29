<template>
    <div class="space-y-6">
        <!-- Header with Filters -->
        <div class="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-4 sm:mb-0">Organization Tasks</h3>
                <div class="flex flex-col sm:flex-row gap-3">
                    <!-- Status Filter -->
                    <div class="relative">
                        <select v-model="selectedStatus" @change="fetchTasks"
                            class="appearance-none bg-white border border-gray-300 rounded-md px-3 py-2 pr-8 text-sm text-gray-700 hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200 min-w-[130px]">
                            <option value="">All Status</option>
                            <option value="pending">Pending</option>
                            <option value="in_progress">In Progress</option>
                            <option value="completed">Completed</option>
                            <option value="cancelled">Cancelled</option>
                        </select>
                        <div class="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
                            <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M19 9l-7 7-7-7"></path>
                            </svg>
                        </div>
                    </div>

                    <!-- Priority Filter -->
                    <div class="relative">
                        <select v-model="selectedPriority" @change="fetchTasks"
                            class="appearance-none bg-white border border-gray-300 rounded-md px-3 py-2 pr-8 text-sm text-gray-700 hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200 min-w-[130px]">
                            <option value="">All Priorities</option>
                            <option value="high">High</option>
                            <option value="medium">Medium</option>
                            <option value="low">Low</option>
                        </select>
                        <div class="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
                            <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M19 9l-7 7-7-7"></path>
                            </svg>
                        </div>
                    </div>

                    <!-- Refresh Button -->
                    <button @click="fetchTasks" :disabled="loading"
                        class="inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white text-sm font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:cursor-not-allowed transition-colors duration-200">
                        <svg v-if="loading" class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4">
                            </circle>
                            <path class="opacity-75" fill="currentColor"
                                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                            </path>
                        </svg>
                        <svg v-else class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15">
                            </path>
                        </svg>
                        {{ loading ? 'Loading...' : 'Refresh' }}
                    </button>
                </div>
            </div>

            <!-- Task Statistics -->
            <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                <div class="bg-gradient-to-r from-blue-50 to-blue-100 p-4 rounded-lg border border-blue-200">
                    <div class="flex items-center">
                        <div class="p-2 bg-blue-500 rounded-lg">
                            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z">
                                </path>
                            </svg>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm font-medium text-blue-600">Total Tasks</p>
                            <p class="text-2xl font-bold text-blue-900">{{ taskStats.total }}</p>
                        </div>
                    </div>
                </div>

                <div class="bg-gradient-to-r from-yellow-50 to-yellow-100 p-4 rounded-lg border border-yellow-200">
                    <div class="flex items-center">
                        <div class="p-2 bg-yellow-500 rounded-lg">
                            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm font-medium text-yellow-600">In Progress</p>
                            <p class="text-2xl font-bold text-yellow-900">{{ taskStats.in_progress }}</p>
                        </div>
                    </div>
                </div>

                <div class="bg-gradient-to-r from-green-50 to-green-100 p-4 rounded-lg border border-green-200">
                    <div class="flex items-center">
                        <div class="p-2 bg-green-500 rounded-lg">
                            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm font-medium text-green-600">Completed</p>
                            <p class="text-2xl font-bold text-green-900">{{ taskStats.completed }}</p>
                        </div>
                    </div>
                </div>

                <div class="bg-gradient-to-r from-purple-50 to-purple-100 p-4 rounded-lg border border-purple-200">
                    <div class="flex items-center">
                        <div class="p-2 bg-purple-500 rounded-lg">
                            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                            </svg>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm font-medium text-purple-600">High Priority</p>
                            <p class="text-2xl font-bold text-purple-900">{{ taskStats.high_priority }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tasks List -->
        <div class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
            <div class="p-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-6">Recent Tasks</h3>

                <!-- Loading State -->
                <div v-if="loading" class="flex justify-center items-center py-12">
                    <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600"></div>
                    <span class="ml-3 text-gray-600">Loading tasks...</span>
                </div>

                <!-- Tasks List -->
                <div v-else-if="tasks.length > 0" class="space-y-4">
                    <div v-for="task in tasks" :key="task.id"
                        class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-all duration-300 hover:border-blue-200 cursor-pointer"
                        @click="viewTask(task)">
                        <div class="flex items-start justify-between">
                            <div class="flex-1 min-w-0">
                                <div class="flex items-center space-x-3 mb-2">
                                    <h4 class="text-lg font-medium text-gray-900 truncate">{{ task.title }}</h4>
                                    <span :class="getStatusClass(task.status)"
                                        class="px-2 py-1 text-xs font-medium rounded-full">
                                        {{ formatStatus(task.status) }}
                                    </span>
                                    <span :class="getPriorityClass(task.priority)"
                                        class="px-2 py-1 text-xs font-medium rounded-full">
                                        {{ formatPriority(task.priority) }}
                                    </span>
                                </div>
                                <p class="text-gray-600 text-sm mb-3 line-clamp-2">{{ task.description || 'No description' }}</p>
                                <div class="flex items-center space-x-4 text-sm text-gray-500">
                                    <span>{{ task.project?.name || 'No project' }}</span>
                                    <span>•</span>
                                    <span>{{ task.assigned_to?.first_name }} {{ task.assigned_to?.last_name }}</span>
                                    <span>•</span>
                                    <span>Due: {{ formatDate(task.due_date) }}</span>
                                </div>
                            </div>
                            <div class="ml-4 shrink-0">
                                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M9 5l7 7-7 7"></path>
                                </svg>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Empty State -->
                <div v-else class="text-center py-12">
                    <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor"
                        viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
                            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z">
                        </path>
                    </svg>
                    <h3 class="text-lg font-medium text-gray-900 mb-2">No tasks found</h3>
                    <p class="text-gray-500">No tasks match your current filters.</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axiosInstance from '@/plugins/axiosConfig.js'

const router = useRouter()

// Reactive data
const tasks = ref([])
const loading = ref(true)
const selectedStatus = ref('')
const selectedPriority = ref('')

// Computed task statistics
const taskStats = computed(() => {
    if (!Array.isArray(tasks.value)) {
        return {
            total: 0,
            in_progress: 0,
            completed: 0,
            high_priority: 0,
        }
    }

    return {
        total: tasks.value.length,
        in_progress: tasks.value.filter(task => task.status === 'in_progress').length,
        completed: tasks.value.filter(task => task.status === 'completed').length,
        high_priority: tasks.value.filter(task => task.priority === 'high').length,
    }
})

// Methods
const fetchTasks = async () => {
    try {
        loading.value = true

        // Mock data for demonstration when API is not available
        const mockTasks = [
            {
                id: 1,
                title: 'Update user authentication system',
                description: 'Implement JWT token refresh mechanism and improve security',
                status: 'in_progress',
                priority: 'high',
                due_date: '2024-11-15',
                project: { name: 'Security Enhancement' },
                assigned_to: { first_name: 'John', last_name: 'Doe' }
            },
            {
                id: 2,
                title: 'Design new dashboard layout',
                description: 'Create modern and responsive dashboard with better UX',
                status: 'completed',
                priority: 'medium',
                due_date: '2024-11-10',
                project: { name: 'UI/UX Redesign' },
                assigned_to: { first_name: 'Jane', last_name: 'Smith' }
            },
            {
                id: 3,
                title: 'Database optimization',
                description: 'Optimize query performance and add proper indexing',
                status: 'pending',
                priority: 'high',
                due_date: '2024-11-20',
                project: { name: 'Performance Optimization' },
                assigned_to: { first_name: 'Mike', last_name: 'Johnson' }
            },
            {
                id: 4,
                title: 'Unit test coverage',
                description: 'Increase unit test coverage to 90%',
                status: 'in_progress',
                priority: 'medium',
                due_date: '2024-11-25',
                project: { name: 'Quality Assurance' },
                assigned_to: { first_name: 'Sarah', last_name: 'Wilson' }
            }
        ]

        // Filter mock data based on selected filters
        let filteredTasks = mockTasks
        if (selectedStatus.value) {
            filteredTasks = filteredTasks.filter(task => task.status === selectedStatus.value)
        }
        if (selectedPriority.value) {
            filteredTasks = filteredTasks.filter(task => task.priority === selectedPriority.value)
        }

        tasks.value = filteredTasks

        // Try to fetch real data if API is available
        try {
            const params = {}
            if (selectedStatus.value) params.status = selectedStatus.value
            if (selectedPriority.value) params.priority = selectedPriority.value

            const response = await axiosInstance.get('tasks/', { params })
            tasks.value = response.data.results || response.data
        } catch (apiError) {
            console.log('API not available, using mock data:', apiError.message)
            // Keep using mock data
        }
    } catch (error) {
        console.error('Error fetching tasks:', error)
        // Fallback to empty array
        tasks.value = []
    } finally {
        loading.value = false
    }
}

const viewTask = (task) => {
    router.push({ name: 'tasks.detail', params: { id: task.id } })
}

const getStatusClass = (status) => {
    const classes = {
        pending: 'bg-gray-100 text-gray-800',
        in_progress: 'bg-yellow-100 text-yellow-800',
        completed: 'bg-green-100 text-green-800',
        cancelled: 'bg-red-100 text-red-800'
    }
    return classes[status] || 'bg-gray-100 text-gray-800'
}

const getPriorityClass = (priority) => {
    const classes = {
        high: 'bg-red-100 text-red-800',
        medium: 'bg-yellow-100 text-yellow-800',
        low: 'bg-green-100 text-green-800'
    }
    return classes[priority] || 'bg-gray-100 text-gray-800'
}

const formatStatus = (status) => {
    return status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())
}

const formatPriority = (priority) => {
    return priority.charAt(0).toUpperCase() + priority.slice(1)
}

const formatDate = (dateString) => {
    if (!dateString) return 'No due date'
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    })
}

// Lifecycle
onMounted(() => {
    fetchTasks()
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
</style>