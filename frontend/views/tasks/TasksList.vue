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
                        <div class="relative">
                            <select v-model="selectedPriority" @change="handlePriorityChange"
                                class="appearance-none bg-white border border-gray-300 rounded-md px-3 py-2 pr-8 text-sm text-gray-700 hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200 min-w-[130px]">
                                <option value="" class="text-gray-500">All Priorities</option>
                                <option value="high" class="text-red-600 font-medium">High</option>
                                <option value="medium" class="text-yellow-600 font-medium">Medium</option>
                                <option value="low" class="text-green-600 font-medium">Low</option>
                            </select>
                            <div class="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
                                <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M19 9l-7 7-7-7"></path>
                                </svg>
                            </div>
                        </div>

                        <!-- Refresh Button -->
                        <Button variant="primary" size="md" :loading="loading" loadingText="Loading..." label="Refresh"
                            @click="refreshTasks">
                            <template #icon>
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15">
                                    </path>
                                </svg>
                            </template>
                        </Button>
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
                        <Button variant="ghost" size="sm" label="Try again" @click="fetchTasks" />
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
                    {{ hasFilters ? 'Try adjusting your filters to see more tasks.' : 'Create a task.' }}
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
import Button from '@/components/Button.vue'
import { useAuth } from '@/composables/useAuth.js'
import { useTasks } from '@/composables/useTasks.js'

export default {
    name: 'TasksList',
    components: {
        TaskCard,
        Pagination,
        Button
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
        const taskStatuses = ref([])

        // Computed properties
        const totalTasks = computed(() => meta.value?.total || 0)
        const hasFilters = computed(() => selectedPriority.value)

        // Methods
        const fetchTasks = async (page = 1) => {
            if (!isAuthenticated.value) {
                error.value = 'Please log in to view your tasks'
                return
            }

            const params = {
                page,
                ...(selectedPriority.value && { priority: selectedPriority.value })
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
            currentPage.value = 1
            fetchTasks(1)
        }

        const handlePriorityChange = () => {
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
            taskStatuses,
            totalTasks,
            hasFilters,
            fetchTasks,
            refreshTasks,
            handlePriorityChange,
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