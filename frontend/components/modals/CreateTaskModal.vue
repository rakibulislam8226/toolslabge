<template>
    <div v-if="isOpen" class="fixed inset-0 overflow-y-auto" style="z-index: 9999; background: rgba(0,0,0,0.5);">
        <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <!-- Background overlay -->
            <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="closeModal"
                style="z-index: 9999;"></div>

            <!-- Modal panel -->
            <div class="relative inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full"
                style="z-index: 10000;">
                <!-- Header -->
                <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-lg font-semibold text-gray-900">Create New Task</h3>
                        <button @click="closeModal"
                            class="text-gray-400 hover:text-gray-600 transition-colors duration-200">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M6 18L18 6M6 6l12 12"></path>
                            </svg>
                        </button>
                    </div>

                    <!-- Form -->
                    <form @submit.prevent="createTask" class="space-y-4">
                        <!-- Title -->
                        <div>
                            <label for="title" class="block text-sm font-medium text-gray-700 mb-1">
                                Title <span class="text-red-500">*</span>
                            </label>
                            <input id="title" v-model="form.title" type="text" required
                                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="Enter task title" />
                        </div>

                        <!-- Description -->
                        <div>
                            <label for="description" class="block text-sm font-medium text-gray-700 mb-1">
                                Description
                            </label>
                            <textarea id="description" v-model="form.description" rows="3"
                                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="Enter task description"></textarea>
                        </div>

                        <!-- Status and Priority Row -->
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <!-- Status -->
                            <div>
                                <label for="status" class="block text-sm font-medium text-gray-700 mb-1">
                                    Status
                                </label>
                                <select id="status" v-model="form.status_id"
                                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                                    <option value="">Select status</option>
                                    <option v-for="status in statuses" :key="status.id" :value="status.id">
                                        {{ status.name }}
                                    </option>
                                </select>
                            </div>

                            <!-- Priority -->
                            <div>
                                <label for="priority" class="block text-sm font-medium text-gray-700 mb-1">
                                    Priority
                                </label>
                                <select id="priority" v-model="form.priority"
                                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                                    <option value="low">Low</option>
                                    <option value="medium">Medium</option>
                                    <option value="high">High</option>
                                </select>
                            </div>
                        </div>

                        <!-- Dates Row -->
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <!-- Start Date -->
                            <div>
                                <label for="start_date" class="block text-sm font-medium text-gray-700 mb-1">
                                    Start Date
                                </label>
                                <input id="start_date" v-model="form.start_date" type="datetime-local"
                                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
                            </div>

                            <!-- Due Date -->
                            <div>
                                <label for="due_date" class="block text-sm font-medium text-gray-700 mb-1">
                                    Due Date
                                </label>
                                <input id="due_date" v-model="form.due_date" type="datetime-local"
                                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
                            </div>
                        </div>

                        <!-- Estimated Hours -->
                        <div>
                            <label for="estimated_hours" class="block text-sm font-medium text-gray-700 mb-1">
                                Estimated Hours
                            </label>
                            <input id="estimated_hours" v-model.number="form.estimated_hours" type="number" step="0.5"
                                min="0" max="999"
                                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="e.g., 4.5" />
                        </div>

                        <!-- Assign Members -->
                        <div>
                            <label for="members" class="block text-sm font-medium text-gray-700 mb-1">
                                Assign Members
                            </label>
                            <div class="space-y-2 max-h-32 overflow-y-auto border border-gray-300 rounded-lg p-2">
                                <div v-if="projectMembers.length === 0" class="text-sm text-gray-500 text-center py-2">
                                    No project members available
                                </div>
                                <label v-for="member in projectMembers" :key="member.id"
                                    class="flex items-center space-x-2 hover:bg-gray-50 p-1 rounded cursor-pointer">
                                    <input type="checkbox" :value="member.user.id" v-model="form.members"
                                        class="rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
                                    <div class="flex items-center space-x-2 flex-1 min-w-0">
                                        <img v-if="member.user.photo" :src="member.user.photo"
                                            :alt="member.user.first_name || member.user.email"
                                            class="w-6 h-6 rounded-full" />
                                        <div v-else
                                            class="w-6 h-6 rounded-full bg-gray-300 flex items-center justify-center">
                                            <span class="text-xs font-medium text-gray-600">
                                                {{ getInitials(member.user) }}
                                            </span>
                                        </div>
                                        <span class="text-sm font-medium text-gray-900 truncate">
                                            {{ member.user.first_name || member.user.email }}
                                            {{ member.user.last_name }}
                                        </span>
                                    </div>
                                </label>
                            </div>
                        </div>

                        <!-- Error message -->
                        <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-3">
                            <p class="text-sm text-red-600">{{ error }}</p>
                        </div>
                    </form>
                </div>

                <!-- Footer -->
                <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                    <button @click="createTask" :disabled="creating || !form.title.trim()"
                        class="w-full inline-flex justify-center rounded-lg border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed">
                        <svg v-if="creating" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                            xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4">
                            </circle>
                            <path class="opacity-75" fill="currentColor"
                                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                            </path>
                        </svg>
                        {{ creating ? 'Creating...' : 'Create Task' }}
                    </button>
                    <button @click="closeModal" :disabled="creating" type="button"
                        class="mt-3 w-full inline-flex justify-center rounded-lg border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed">
                        Cancel
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted } from 'vue'
import axios from "@/plugins/axiosConfig.js"

// Debug logging
console.log('CreateTaskModal script loaded')

// Props
const props = defineProps({
    isOpen: {
        type: Boolean,
        default: false
    },
    projectId: {
        type: [String, Number],
        required: true
    },
    initialStatusId: {
        type: [String, Number],
        default: null
    },
    statuses: {
        type: Array,
        default: () => []
    }
})

// Emits
const emit = defineEmits(['close', 'created'])

// Reactive data
const creating = ref(false)
const error = ref('')
const projectMembers = ref([])

const form = reactive({
    title: '',
    description: '',
    status_id: props.initialStatusId || '',
    priority: 'medium',
    start_date: '',
    due_date: '',
    estimated_hours: null,
    members: []
})

// Watch for initial status changes
watch(() => props.initialStatusId, (newValue) => {
    if (newValue) {
        form.status_id = newValue
    }
})

// Watch for dialog open/close to reset form
watch(() => props.isOpen, (isOpen) => {
    if (isOpen) {
        resetForm()
        fetchProjectMembers()
    }
})

// Methods
const resetForm = () => {
    form.title = ''
    form.description = ''
    form.status_id = props.initialStatusId || ''
    form.priority = 'medium'
    form.start_date = ''
    form.due_date = ''
    form.estimated_hours = null
    form.members = []
    error.value = ''
}

const closeModal = () => {
    if (!creating.value) {
        emit('close')
    }
}

const fetchProjectMembers = async () => {
    if (!props.projectId) return

    try {
        const response = await axios.get(`projects/${props.projectId}/members/`)
        projectMembers.value = response.data.data || response.data || []
    } catch (err) {
        console.error('Failed to fetch project members:', err)
        projectMembers.value = []
    }
}

const createTask = async () => {
    if (!form.title.trim()) return
    if (!props.projectId) {
        error.value = 'Project ID is required'
        return
    }

    try {
        creating.value = true
        error.value = ''

        // Prepare payload
        const payload = {
            project_id: parseInt(props.projectId),
            title: form.title.trim(),
            description: form.description.trim() || null,
            priority: form.priority,
            members: form.members
        }

        // Add optional fields
        if (form.status_id) {
            payload.status_id = parseInt(form.status_id)
        }

        if (form.start_date) {
            payload.start_date = new Date(form.start_date).toISOString()
        }

        if (form.due_date) {
            payload.due_date = new Date(form.due_date).toISOString()
        }

        if (form.estimated_hours) {
            payload.estimated_hours = form.estimated_hours
        }

        const response = await axios.post(`projects/${props.projectId}/tasks/`, payload)
        const newTask = response.data.data || response.data

        emit('created', newTask)
    } catch (err) {
        console.error('Failed to create task:', err)

        if (err.response?.data?.detail) {
            error.value = err.response.data.detail
        } else if (err.response?.data) {
            // Handle field-specific errors
            const errors = []
            Object.entries(err.response.data).forEach(([field, messages]) => {
                if (Array.isArray(messages)) {
                    errors.push(`${field}: ${messages.join(', ')}`)
                } else {
                    errors.push(`${field}: ${messages}`)
                }
            })
            error.value = errors.join('\n')
        } else {
            error.value = 'Failed to create task. Please try again.'
        }
    } finally {
        creating.value = false
    }
}

const getInitials = (user) => {
    if (user.first_name && user.last_name) {
        return `${user.first_name.charAt(0)}${user.last_name.charAt(0)}`.toUpperCase()
    } else if (user.first_name) {
        return user.first_name.charAt(0).toUpperCase()
    } else if (user.email) {
        return user.email.charAt(0).toUpperCase()
    }
    return '?'
}

// Initialize on mount
onMounted(() => {
    if (props.isOpen) {
        fetchProjectMembers()
    }
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