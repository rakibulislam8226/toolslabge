<template>
    <div class="min-h-screen bg-gray-50">
        <!-- Loading State -->
        <div v-if="loading" class="flex items-center justify-center py-12">
            <div class="text-center">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                <p class="mt-4 text-gray-500">Loading task details...</p>
            </div>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div class="bg-red-50 border border-red-200 rounded-lg p-6">
                <div class="flex items-center">
                    <svg class="w-5 h-5 text-red-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    <div>
                        <h3 class="text-sm font-medium text-red-800">Error loading task</h3>
                        <p class="text-sm text-red-700 mt-1">{{ error }}</p>
                        <Button variant="ghost" size="sm" label="Try again" @click="fetchTask" />
                    </div>
                </div>
            </div>
        </div>

        <!-- Task Detail Content -->
        <div v-else-if="task" class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <!-- Header with Breadcrumb -->
            <div class="mb-8">
                <nav class="flex items-center space-x-2 text-sm text-gray-500 mb-4">
                    <router-link :to="breadcrumbUrl" class="hover:text-gray-700 transition-colors flex items-center">
                        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7">
                            </path>
                        </svg>
                        {{ breadcrumbText }}
                    </router-link>
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                    </svg>
                    <span class="text-gray-900 font-medium">{{ task.title }}</span>
                </nav>

                <!-- Action Buttons -->
                <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
                    <div class="flex items-center space-x-3">
                        <h1 class="text-3xl font-bold text-gray-900">{{ task.title }}</h1>
                        <span class="inline-flex items-center px-3 py-1 text-sm font-medium rounded-full"
                            :class="getPriorityColor(task.priority)">
                            {{ formatPriority(task.priority) }}
                        </span>
                    </div>

                    <div class="mt-4 sm:mt-0 flex space-x-3">
                        <button @click="editTask"
                            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200 text-sm font-medium">
                            <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z">
                                </path>
                            </svg>
                            Edit Task
                        </button>
                        <button @click="confirmDelete"
                            class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors duration-200 text-sm font-medium">
                            <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16">
                                </path>
                            </svg>
                            Delete
                        </button>
                    </div>
                </div>
            </div>

            <!-- Main Content Grid -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <!-- Main Content -->
                <div class="lg:col-span-2 space-y-6">
                    <!-- Task Description -->
                    <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                        <h2 class="text-lg font-semibold text-gray-900 mb-4">Description</h2>
                        <div v-if="task.description" class="prose prose-sm max-w-none text-gray-700">
                            <p class="whitespace-pre-wrap">{{ task.description }}</p>
                        </div>
                        <p v-else class="text-gray-500 italic">No description provided</p>
                    </div>

                    <!-- Task Timeline -->
                    <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                        <h2 class="text-lg font-semibold text-gray-900 mb-4">Timeline</h2>
                        <div class="space-y-4">
                            <div v-if="task.start_date" class="flex items-center">
                                <svg class="w-5 h-5 text-green-500 mr-3" fill="none" stroke="currentColor"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                </svg>
                                <div>
                                    <p class="text-sm font-medium text-gray-900">Start Date</p>
                                    <p class="text-sm text-gray-600">{{ formatDate(task.start_date) }}</p>
                                </div>
                            </div>

                            <div v-if="task.due_date" class="flex items-center">
                                <svg class="w-5 h-5 text-red-500 mr-3" fill="none" stroke="currentColor"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                </svg>
                                <div>
                                    <p class="text-sm font-medium text-gray-900">Due Date</p>
                                    <p class="text-sm text-gray-600"
                                        :class="{ 'text-red-600 font-semibold': isOverdue }">
                                        {{ formatDate(task.due_date) }}
                                        <span v-if="isOverdue" class="text-red-600 ml-1">(Overdue)</span>
                                    </p>
                                </div>
                            </div>

                            <div class="flex items-center">
                                <svg class="w-5 h-5 text-gray-400 mr-3" fill="none" stroke="currentColor"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                </svg>
                                <div>
                                    <p class="text-sm font-medium text-gray-900">Created</p>
                                    <p class="text-sm text-gray-600">{{ formatDate(task.created_at) }}</p>
                                </div>
                            </div>

                            <div class="flex items-center">
                                <svg class="w-5 h-5 text-gray-400 mr-3" fill="none" stroke="currentColor"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                </svg>
                                <div>
                                    <p class="text-sm font-medium text-gray-900">Last Updated</p>
                                    <p class="text-sm text-gray-600">{{ formatDate(task.updated_at) }}</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Assigned Members -->
                    <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                        <h2 class="text-lg font-semibold text-gray-900 mb-4">Assigned Team Members</h2>
                        <div v-if="task.assigned_members && task.assigned_members.length > 0" class="space-y-3">
                            <div v-for="member in task.assigned_members" :key="member.id"
                                class="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                                <div class="shrink-0">
                                    <img v-if="member.photo" :src="member.photo"
                                        :alt="member.first_name || member.email" class="w-10 h-10 rounded-full" />
                                    <div v-else
                                        class="w-10 h-10 rounded-full bg-gray-300 flex items-center justify-center">
                                        <span class="text-sm font-medium text-gray-600">
                                            {{ getInitials(member) }}
                                        </span>
                                    </div>
                                </div>
                                <div class="flex-1 min-w-0">
                                    <p class="text-sm font-medium text-gray-900">
                                        {{ member.first_name || member.last_name ? `${member.first_name}
                                        ${member.last_name}`.trim() : 'Unnamed User' }}
                                    </p>
                                    <p class="text-sm text-gray-500">{{ member.email }}</p>
                                </div>
                            </div>
                        </div>
                        <p v-else class="text-gray-500 italic">No team members assigned</p>
                    </div>
                </div>

                <!-- Sidebar -->
                <div class="space-y-6">
                    <!-- Task Status -->
                    <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                        <h3 class="text-lg font-semibold text-gray-900 mb-4">Status</h3>
                        <div class="space-y-4">
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Current Status</label>
                                <select v-model="currentStatusId" @change="updateStatus"
                                    :class="`w-full text-sm bg-gradient-to-r ${getStatusColorClasses(currentStatusId, 'gradient')} border ${getStatusColorClasses(currentStatusId, 'border')} rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 font-medium ${getStatusColorClasses(currentStatusId, 'text')}`">
                                    <option v-for="status in taskStatuses" :key="status.id" :value="status.id">
                                        {{ status.name }}
                                    </option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <!-- Project Info -->
                    <div v-if="task.project" class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                        <h3 class="text-lg font-semibold text-gray-900 mb-4">Project</h3>
                        <div class="flex items-center space-x-3 p-3 bg-blue-50 rounded-lg">
                            <div class="shrink-0">
                                <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                                    <span class="text-white text-sm font-semibold">{{ task.project.name.charAt(0)
                                        }}</span>
                                </div>
                            </div>
                            <div>
                                <p class="text-sm font-medium text-gray-900">{{ task.project.name }}</p>
                                <p class="text-xs text-gray-500">Project ID: {{ task.project.id }}</p>
                            </div>
                        </div>
                    </div>

                    <!-- Task Details -->
                    <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                        <h3 class="text-lg font-semibold text-gray-900 mb-4">Details</h3>
                        <div class="space-y-3">
                            <div class="flex justify-between items-center py-2 border-b border-gray-100">
                                <span class="text-sm font-medium text-gray-500">Task ID</span>
                                <span class="text-sm text-gray-900">#{{ task.id }}</span>
                            </div>
                            <div class="flex justify-between items-center py-2 border-b border-gray-100">
                                <span class="text-sm font-medium text-gray-500">Priority</span>
                                <span class="inline-flex items-center px-2 py-1 text-xs font-medium rounded-full"
                                    :class="getPriorityColor(task.priority)">
                                    {{ formatPriority(task.priority) }}
                                </span>
                            </div>
                            <div v-if="task.estimated_hours"
                                class="flex justify-between items-center py-2 border-b border-gray-100">
                                <span class="text-sm font-medium text-gray-500">Estimated Hours</span>
                                <span class="text-sm text-gray-900">{{ task.estimated_hours }}h</span>
                            </div>
                            <div class="flex justify-between items-center py-2">
                                <span class="text-sm font-medium text-gray-500">Created By</span>
                                <span class="text-sm text-gray-900">User #{{ task.created_by }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Edit Task Modal -->
        <EditTaskModal v-if="showEditModal" :is-open="showEditModal" :task-id="task?.id" @close="showEditModal = false"
            @updated="handleTaskUpdated" />

        <!-- Delete Confirmation Modal -->
        <ConfirmModal v-if="showDeleteModal" :is-open="showDeleteModal" title="Delete Task"
            message="Are you sure you want to delete this task? This action cannot be undone." confirm-text="Delete"
            confirm-class="bg-red-600 hover:bg-red-700" @confirm="deleteTask" @cancel="showDeleteModal = false" />
    </div>
</template>

<script>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from '@/plugins/axiosConfig.js'
import { useTasks } from '@/composables/useTasks.js'
import EditTaskModal from '@/components/modals/EditTaskModal.vue'
import ConfirmModal from '@/components/modals/ConfirmModal.vue'
import Button from '@/components/Button.vue'

export default {
    name: 'TaskDetail',
    components: {
        EditTaskModal,
        ConfirmModal
    },
    setup() {
        const route = useRoute()
        const router = useRouter()
        const { loading, error, updateTaskStatus, deleteTask: deleteTaskAPI, fetchTaskById, fetchTaskStatuses } = useTasks()

        // Reactive data
        const task = ref(null)
        const taskStatuses = ref([])
        const currentStatusId = ref(null)
        const showEditModal = ref(false)
        const showDeleteModal = ref(false)
        const projectId = ref(null) // Store project ID for API calls

        // Computed properties
        const isOverdue = computed(() => {
            if (!task.value?.due_date) return false
            return new Date(task.value.due_date) < new Date()
        })

        const breadcrumbUrl = computed(() => {
            // Check if we're in a project context
            const projectSlug = route.params.slug
            return projectSlug ? `/projects/${projectSlug}/tasks` : '/tasks'
        })

        const breadcrumbText = computed(() => {
            const projectSlug = route.params.slug
            return projectSlug ? 'Project Tasks' : 'Tasks'
        })

        // Status color mapping
        const statusColorMapping = {
            'todo': { gradient: 'from-gray-50 to-gray-100', border: 'border-gray-200', text: 'text-gray-700' },
            'in progress': { gradient: 'from-blue-50 to-blue-100', border: 'border-blue-200', text: 'text-blue-700' },
            'review': { gradient: 'from-yellow-50 to-yellow-100', border: 'border-yellow-200', text: 'text-yellow-700' },
            'done': { gradient: 'from-green-50 to-green-100', border: 'border-green-200', text: 'text-green-700' },
            'closed': { gradient: 'from-red-50 to-red-100', border: 'border-red-200', text: 'text-red-700' },
        }

        const defaultStatusColor = { gradient: 'from-slate-50 to-slate-100', border: 'border-slate-200', text: 'text-slate-700' }

        // Methods
        const fetchTask = async () => {
            // Check if we're in a project context (route contains slug parameter)
            const projectSlug = route.params.slug

            // Check for project ID in query params (passed from TasksList)
            const queryProjectId = route.query.projectId ? parseInt(route.query.projectId) : null

            // Use query project ID if available, otherwise use stored projectId
            const contextProjectId = queryProjectId || projectId.value

            // If we got project ID from query, store it immediately
            if (queryProjectId) {
                projectId.value = queryProjectId
            }

            console.log('Fetching task with context:', {
                taskId: route.params.id,
                projectSlug,
                queryProjectId,
                contextProjectId
            })

            // Extract project ID from task data if available in route or context
            const result = await fetchTaskById(route.params.id, contextProjectId)

            if (result.success) {
                task.value = result.data
                currentStatusId.value = task.value.status?.id

                // Store project ID for subsequent API calls
                if (task.value.project?.id) {
                    projectId.value = task.value.project.id
                }

                // Fetch all available statuses
                const statusesResult = await fetchTaskStatuses()
                if (statusesResult.success && statusesResult.data.length > 0) {
                    taskStatuses.value = statusesResult.data
                } else {
                    // Fallback: use the current task's status
                    if (task.value.status) {
                        taskStatuses.value = [task.value.status]
                    }
                }
            } else {
                error.value = result.error

                // If task not found, redirect appropriately
                if (result.error.includes('404') || result.error.includes('not found')) {
                    if (projectSlug) {
                        router.push(`/projects/${projectSlug}/tasks`)
                    } else {
                        router.push('/tasks')
                    }
                }
            }
        }

        const updateStatus = async () => {
            if (!currentStatusId.value || currentStatusId.value === task.value.status?.id) return

            const result = await updateTaskStatus(task.value.id, currentStatusId.value, projectId.value)

            if (result.success) {
                task.value = result.data
            } else {
                // Reset status on failure
                currentStatusId.value = task.value.status?.id
                console.error('Failed to update task status:', result.error)
            }
        }

        const editTask = () => {
            showEditModal.value = true
        }

        const confirmDelete = () => {
            showDeleteModal.value = true
        }

        const deleteTask = async () => {
            const result = await deleteTaskAPI(task.value.id, projectId.value)

            if (result.success) {
                router.push('/tasks')
            } else {
                console.error('Failed to delete task:', result.error)
            }

            showDeleteModal.value = false
        }

        const handleTaskUpdated = (updatedTask) => {
            task.value = updatedTask
            currentStatusId.value = updatedTask.status?.id
            showEditModal.value = false
        }

        const getStatusColorClasses = (statusId, type = 'all') => {
            if (!statusId || !taskStatuses.value) {
                return type === 'all' ? defaultStatusColor : defaultStatusColor[type] || ''
            }

            const status = taskStatuses.value.find(s => s.id === statusId)
            if (!status) {
                return type === 'all' ? defaultStatusColor : defaultStatusColor[type] || ''
            }

            const statusName = status.name.toLowerCase().trim()
            const colorConfig = statusColorMapping[statusName] || defaultStatusColor

            return type === 'all' ? colorConfig : colorConfig[type] || ''
        }

        const getPriorityColor = (priority) => {
            const colors = {
                'high': 'bg-red-100 text-red-800',
                'medium': 'bg-yellow-100 text-yellow-800',
                'low': 'bg-green-100 text-green-800'
            }
            return colors[priority] || colors['medium']
        }

        const formatPriority = (priority) => {
            return priority ? priority.charAt(0).toUpperCase() + priority.slice(1) : 'Medium'
        }

        const formatDate = (dateString) => {
            if (!dateString) return ''
            const date = new Date(dateString)
            return date.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            })
        }

        const getInitials = (member) => {
            if (member.first_name && member.last_name) {
                return `${member.first_name.charAt(0)}${member.last_name.charAt(0)}`.toUpperCase()
            } else if (member.first_name) {
                return member.first_name.charAt(0).toUpperCase()
            } else if (member.email) {
                return member.email.charAt(0).toUpperCase()
            }
            return '?'
        }

        // Watch for route changes
        watch(() => route.params.id, () => {
            if (route.params.id) {
                fetchTask()
            }
        }, { immediate: true })

        // Lifecycle
        onMounted(() => {
            // fetchTask() is already called by the watcher above

            // Add keyboard shortcut for going back
            const handleKeyPress = (e) => {
                if (e.key === 'Escape') {
                    const projectSlug = route.params.slug
                    if (projectSlug) {
                        router.push(`/projects/${projectSlug}/tasks`)
                    } else {
                        router.push('/tasks')
                    }
                }
            }

            document.addEventListener('keydown', handleKeyPress)

            // Store cleanup function
            onUnmounted(() => {
                document.removeEventListener('keydown', handleKeyPress)
            })
        })

        return {
            task,
            loading,
            error,
            taskStatuses,
            currentStatusId,
            showEditModal,
            showDeleteModal,
            isOverdue,
            breadcrumbUrl,
            breadcrumbText,
            fetchTask,
            updateStatus,
            editTask,
            confirmDelete,
            deleteTask,
            handleTaskUpdated,
            getStatusColorClasses,
            getPriorityColor,
            formatPriority,
            formatDate,
            getInitials
        }
    }
}
</script>

<style scoped>
.prose p {
    margin-bottom: 1rem;
}
</style>