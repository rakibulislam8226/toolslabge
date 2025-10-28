<template>
    <div class="min-h-screen bg-gray-50">
        <!-- Header Section -->
        <div class="bg-white shadow-sm border-b border-gray-200 mb-6">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
                    <div>
                        <h1 class="text-2xl font-bold text-gray-900">My Tasks</h1>
                        <p class="mt-1 text-sm text-gray-500" v-if="!loading">
                            {{ totalTasks }} task{{ totalTasks !== 1 ? 's' : '' }} found
                        </p>
                    </div>

                    <!-- Filters and Actions -->
                    <div class="mt-4 sm:mt-0 flex flex-col sm:flex-row gap-3">
                        <!-- Priority Filter -->
                        <select v-model="selectedPriority" @change="fetchTasks"
                            class="rounded-lg border-gray-300 text-sm focus:border-blue-500 focus:ring-blue-500">
                            <option value="">All Priorities</option>
                            <option value="high">High Priority</option>
                            <option value="medium">Medium Priority</option>
                            <option value="low">Low Priority</option>
                        </select>

                        <!-- Status Filter -->
                        <select v-model="selectedStatus" @change="fetchTasks"
                            class="rounded-lg border-gray-300 text-sm focus:border-blue-500 focus:ring-blue-500">
                            <option value="">All Statuses</option>
                            <option v-for="status in taskStatuses" :key="status.id" :value="status.id">
                                {{ status.name }}
                            </option>
                        </select>

                        <!-- Refresh Button -->
                        <button @click="refreshTasks" :disabled="loading"
                            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors duration-200 text-sm font-medium">
                            <svg v-if="loading" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline"
                                xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                    stroke-width="4"></circle>
                                <path class="opacity-75" fill="currentColor"
                                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                                </path>
                            </svg>
                            {{ loading ? 'Loading...' : 'Refresh' }}
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Main Content -->
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <!-- Loading State -->
            <div v-if="loading && tasks.length === 0" class="flex justify-center items-center py-12">
                <div class="text-center">
                    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                    <p class="mt-4 text-gray-500">Loading tasks...</p>
                </div>
            </div>

            <!-- Error State -->
            <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-6 mb-6">
                <div class="flex items-center">
                    <svg class="w-5 h-5 text-red-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    <div>
                        <h3 class="text-sm font-medium text-red-800">Error loading tasks</h3>
                        <p class="text-sm text-red-700 mt-1">{{ error }}</p>
                        <button @click="fetchTasks" class="mt-2 text-sm text-red-600 hover:text-red-500 underline">
                            Try again
                        </button>
                    </div>
                </div>
            </div>

            <!-- Empty State -->
            <div v-else-if="!loading && tasks.length === 0" class="text-center py-12">
                <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2">
                    </path>
                </svg>
                <h3 class="mt-2 text-sm font-medium text-gray-900">No tasks found</h3>
                <p class="mt-1 text-sm text-gray-500">
                    {{ hasFilters ? 'Try adjusting your filters to see more tasks.' : 'Get started by creating your first task.' }}
                </p>
            </div>

            <!-- Tasks Grid -->
            <div v-else>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                    <TaskCard v-for="task in tasks" :key="task.id" :task="task" :statuses="taskStatuses"
                        @edit="handleTaskEdit" @delete="handleTaskDelete" @status-change="handleStatusChange" />
                </div>

                <!-- Pagination -->
                <div v-if="meta && meta.num_pages > 1" class="mt-8">
                    <Pagination v-model="currentPage" :total-pages="meta.num_pages" @page="handlePageChange" />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import TaskCard from '@/components/tasks/TaskCard.vue'
import Pagination from '@/components/Pagination.vue'
import { useAuth } from '@/composables/useAuth.js'
import { useTasks } from '@/composables/useTasks.js'

export default {
    name: 'TasksList',
    components: {
        TaskCard,
        Pagination
    },
    setup() {
        const { isAuthenticated } = useAuth()
        const router = useRouter()
        const { loading, error, fetchTasks: fetchTasksAPI, updateTaskStatus, deleteTask, extractTaskStatuses } = useTasks()

        // Reactive data
        const tasks = ref([])
        const meta = ref(null)
        const currentPage = ref(1)
        const selectedPriority = ref('')
        const selectedStatus = ref('')
        const taskStatuses = ref([])

        // Computed properties
        const totalTasks = computed(() => meta.value?.total || 0)
        const hasFilters = computed(() => selectedPriority.value || selectedStatus.value)

        // Methods
        const fetchTasks = async (page = 1) => {
            if (!isAuthenticated.value) {
                error.value = 'Please log in to view your tasks'
                return
            }

            const params = {
                page,
                ...(selectedPriority.value && { priority: selectedPriority.value }),
                ...(selectedStatus.value && { status: selectedStatus.value })
            }

            const result = await fetchTasksAPI(params)

            if (result.success) {
                tasks.value = result.data
                meta.value = result.meta
                currentPage.value = page

                // Extract and update task statuses
                const statuses = extractTaskStatuses(result.data)
                if (statuses.length > 0) {
                    taskStatuses.value = statuses
                }
            } else {
                tasks.value = []
                meta.value = null
            }
        }

        const refreshTasks = () => {
            selectedPriority.value = ''
            selectedStatus.value = ''
            currentPage.value = 1
            fetchTasks(1)
        }

        const handlePageChange = (page) => {
            fetchTasks(page)
        }

        const handleStatusChange = async (taskId, newStatusId) => {
            // Find task to get project context
            const task = tasks.value.find(t => t.id === taskId)
            const projectId = task?.project?.id

            const result = await updateTaskStatus(taskId, newStatusId, projectId)

            if (result.success) {
                // Update the task in the local state
                const taskIndex = tasks.value.findIndex(task => task.id === taskId)
                if (taskIndex !== -1) {
                    tasks.value[taskIndex] = result.data
                }
            } else {
                // Optionally show an error message to the user
                console.error('Failed to update task status:', result.error)
            }
        }

        const handleTaskEdit = (task) => {
            // Navigate to task detail page with project context if available
            if (task.project?.id) {
                // Pass project ID as query param for API optimization
                router.push({
                    name: 'tasks.detail',
                    params: { id: task.id },
                    query: { projectId: task.project.id }
                })
            } else {
                router.push(`/tasks/${task.id}`)
            }
        }

        const handleTaskDelete = async (taskId) => {
            // Find task to get project context
            const task = tasks.value.find(t => t.id === taskId)
            const projectId = task?.project?.id

            const result = await deleteTask(taskId, projectId)

            if (result.success) {
                // Remove task from local state
                tasks.value = tasks.value.filter(task => task.id !== taskId)
                // Update meta count
                if (meta.value) {
                    meta.value.total = Math.max(0, meta.value.total - 1)
                }
            } else {
                // Optionally show an error message to the user
                console.error('Failed to delete task:', result.error)
            }
        }

        // Lifecycle
        onMounted(() => {
            fetchTasks()
        })

        return {
            tasks,
            meta,
            loading,
            error,
            currentPage,
            selectedPriority,
            selectedStatus,
            taskStatuses,
            totalTasks,
            hasFilters,
            fetchTasks,
            refreshTasks,
            handlePageChange,
            handleStatusChange,
            handleTaskEdit,
            handleTaskDelete
        }
    }
}
</script>

<style scoped>
/* Additional custom styles if needed */
.line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
</style>