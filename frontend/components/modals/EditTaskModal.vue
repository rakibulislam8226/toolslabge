<template>
    <BaseModal :is-open="isOpen" title="Edit Task" size="xxl" @close="closeModal">
        <!-- Loading State -->
        <div v-if="loading" class="flex items-center justify-center py-8">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <span class="ml-2 text-gray-600">Loading task details...</span>
        </div>

        <!-- Form -->
        <form v-else @submit.prevent="updateTask" class="space-y-4">
            <!-- Title -->
            <div>
                <label for="edit-title" class="block text-sm font-medium text-gray-700 mb-1">
                    Title <span class="text-red-500">*</span>
                </label>
                <input id="edit-title" v-model="form.title" type="text" required
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Enter task title" />
            </div>

            <!-- Description -->
            <div>
                <label for="edit-description" class="block text-sm font-medium text-gray-700 mb-1">
                    Description
                </label>
                <textarea id="edit-description" v-model="form.description" rows="3"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Enter task description"></textarea>
            </div>

            <!-- Status and Priority Row -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <!-- Status -->
                <div>
                    <label for="edit-status" class="block text-sm font-medium text-gray-700 mb-1">
                        Status
                    </label>
                    <select id="edit-status" v-model="form.status_id"
                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                        <option value="">Select status</option>
                        <option v-for="status in statuses" :key="status.id" :value="status.id">
                            {{ status.name }}
                        </option>
                    </select>
                </div>

                <!-- Priority -->
                <div>
                    <label for="edit-priority" class="block text-sm font-medium text-gray-700 mb-1">
                        Priority
                    </label>
                    <select id="edit-priority" v-model="form.priority"
                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                        <option value="low">Low</option>
                        <option value="medium">Medium</option>
                        <option value="high">High</option>
                    </select>
                </div>
            </div>

            <!-- Scheduling Section -->
            <!-- Scheduling Section -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <!-- Scheduled Start -->
                <div>
                    <label for="edit-scheduled-start" class="block text-sm font-medium text-gray-700 mb-1">
                        Scheduled Start
                    </label>
                    <flat-pickr id="edit-scheduled-start" v-model="form.scheduled_start" :config="flatpickrConfig"
                        placeholder="Select start date & time"
                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
                </div>

                <!-- Target Completion -->
                <div>
                    <label for="edit-target-completion" class="block text-sm font-medium text-gray-700 mb-1">
                        Target Completion
                    </label>
                    <flat-pickr id="edit-target-completion" v-model="form.target_completion" :config="flatpickrConfig"
                        placeholder="Select completion date & time"
                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
                </div>
            </div>

            <!-- Estimated Hours -->
            <div>
                <label for="edit-estimated_hours" class="block text-sm font-medium text-gray-700 mb-1">
                    Estimated Hours
                </label>
                <input id="edit-estimated_hours" v-model.number="form.estimated_hours" type="number" step="0.5" min="0"
                    max="999"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="e.g., 4.5" />
            </div>

            <!-- Team Assignment -->
            <div>
                <label for="edit-assigned-members" class="block text-sm font-medium text-gray-700 mb-1">
                    Team Assignment
                </label>

                <!-- Search Input -->
                <div class="mb-2">
                    <input type="text" placeholder="Search team members..."
                        @input="debouncedMemberSearch($event.target.value)"
                        class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500" />
                </div>

                <!-- Selected Members Display -->
                <div v-if="form.assigned_members.length > 0" class="mb-2 p-2 bg-gray-50 dark:bg-blue-900/20 rounded-lg">
                    <div class="text-xs font-medium text-gray-600 dark:text-blue-300 mb-1">Assigned Team Members:</div>
                    <div class="flex flex-wrap gap-1">
                        <span v-for="memberId in form.assigned_members" :key="memberId"
                            class="inline-flex items-center px-2 py-1 text-xs bg-gray-100 dark:bg-blue-800 text-gray-700 dark:text-blue-200 rounded-full">
                            {{ getSelectedMemberName(memberId) }}
                            <button @click="removeMember(memberId)"
                                class="ml-1 text-gray-500 dark:text-blue-400 hover:text-gray-700 dark:hover:text-blue-200">
                                ×
                            </button>
                        </span>
                    </div>
                </div>

                <!-- Members List -->
                <div
                    class="space-y-2 max-h-32 overflow-y-auto border border-gray-200 dark:border-gray-600 rounded-lg p-2 bg-gray-50 dark:bg-gray-800">
                    <div v-if="projectMembers.length === 0 && !memberSearchQuery"
                        class="text-sm text-gray-400 dark:text-gray-400 text-center py-2">
                        No project members available
                    </div>
                    <div v-else-if="projectMembers.length === 0 && memberSearchQuery"
                        class="text-sm text-gray-400 dark:text-gray-400 text-center py-2">
                        No members found matching "{{ memberSearchQuery }}"
                    </div>
                    <label v-for="member in projectMembers" :key="member.id"
                        class="flex items-center space-x-2 hover:bg-blue-50 hover:border-blue-200 border border-transparent dark:hover:bg-gray-700 dark:hover:border-gray-600 p-1 rounded cursor-pointer transition-all duration-200">
                        <input type="checkbox" :value="member.user" v-model="form.assigned_members"
                            class="rounded border-gray-200 dark:border-gray-600 text-blue-600 focus:ring-blue-500 dark:bg-gray-700" />
                        <div class="flex items-center space-x-2 flex-1 min-w-0">
                            <div
                                class="w-6 h-6 rounded-full bg-gray-200 dark:bg-gray-600 flex items-center justify-center">
                                <span class="text-xs font-medium text-gray-500 dark:text-gray-300">
                                    {{ getInitials(member) }}
                                </span>
                            </div>
                            <span class="text-sm font-medium text-gray-700 dark:text-gray-100 truncate">
                                {{ member.user_name || member.user_email }}
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

        <template #footer>
            <div class="flex space-x-3 justify-end">
                <button @click="closeModal" :disabled="updating" type="button"
                    class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed">
                    Cancel
                </button>
                <button @click="updateTask" :disabled="updating || !form.title.trim()"
                    class="inline-flex justify-center rounded-lg border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-sm font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed">
                    <svg v-if="updating" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                        xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4">
                        </circle>
                        <path class="opacity-75" fill="currentColor"
                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                        </path>
                    </svg>
                    {{ updating ? 'Updating...' : 'Update Task' }}
                </button>
            </div>
        </template>
    </BaseModal>
</template>

<script setup>
import { ref, reactive, watch, computed, onMounted, nextTick } from 'vue'
import axios from "@/plugins/axiosConfig.js"
import flatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'
import BaseModal from './BaseModal.vue'

// Props
const props = defineProps({
    isOpen: {
        type: Boolean,
        default: false
    },
    task: {
        type: Object,
        default: null
    },
    statuses: {
        type: Array,
        default: () => []
    }
})

// Emits
const emit = defineEmits(['close', 'updated'])

// Flatpickr configuration
const flatpickrConfig = {
    enableTime: true,
    dateFormat: 'Y-m-d H:i',
    altInput: true,
    altFormat: 'F j, Y \\a\\t H:i',
    time_24hr: false,
    allowInput: true,
    clickOpens: true,
    defaultDate: null,
    minuteIncrement: 30
}

// Reactive data
const loading = ref(false)
const updating = ref(false)
const error = ref('')
const projectMembers = ref([])
const memberSearchQuery = ref('')
const searchTimeout = ref(null)

const form = reactive({
    title: '',
    description: '',
    status_id: '',
    priority: 'medium',
    scheduled_start: null,
    target_completion: null,
    estimated_hours: null,
    assigned_members: []
})

// Computed
const projectId = computed(() => {
    return props.task?.project?.id
})

// Watch for task changes to populate form
watch(() => props.task, (newTask) => {
    if (newTask) {
        populateForm(newTask)
    }
}, { immediate: true })

// Watch for dialog open/close
watch(() => props.isOpen, (isOpen) => {
    nextTick(() => {
        if (isOpen) {
            document.body.style.overflow = 'hidden'
            if (props.task) {
                fetchTaskDetails()
                fetchProjectMembers()
            }
        } else {
            document.body.style.overflow = ''
        }
    })
})

// Fetch detailed task information
const fetchTaskDetails = async () => {
    if (!props.task?.id || !projectId.value) return

    try {
        loading.value = true
        const response = await axios.get(`projects/${projectId.value}/tasks/${props.task.id}/`)
        const taskDetails = response.data.data || response.data
        populateForm(taskDetails)
    } catch (err) {
        console.error('Failed to fetch task details:', err)
        error.value = 'Failed to load task details'
        // Fallback to basic task data
        populateForm(props.task)
    } finally {
        loading.value = false
    }
}

// Debounced search for members
const debouncedMemberSearch = (query) => {
    if (searchTimeout.value) {
        clearTimeout(searchTimeout.value)
    }

    searchTimeout.value = setTimeout(() => {
        memberSearchQuery.value = query
        fetchProjectMembers(query)
    }, 300)
}

// Methods
const populateForm = (task) => {
    form.title = task.title || ''
    form.description = task.description || ''
    form.status_id = task.status?.id || ''
    form.priority = task.priority || 'medium'

    // Format dates for flatpickr (expects Date objects)
    if (task.start_date) {
        const startDate = new Date(task.start_date)
        if (!isNaN(startDate.getTime())) {
            form.scheduled_start = startDate
        }
    }

    if (task.due_date) {
        const dueDate = new Date(task.due_date)
        if (!isNaN(dueDate.getTime())) {
            form.target_completion = dueDate
        }
    }

    form.estimated_hours = task.estimated_hours || null
    form.assigned_members = task.assigned_members ? task.assigned_members.map(m => m.id) : []
    error.value = ''
}

const formatDateForInput = (dateString) => {
    if (!dateString) return ''
    const date = new Date(dateString)
    // Format for datetime-local input (YYYY-MM-DDTHH:MM)
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    return `${year}-${month}-${day}T${hours}:${minutes}`
}

const closeModal = () => {
    if (!updating.value) {
        emit('close')
    }
}

const fetchProjectMembers = async (searchQuery = '') => {
    if (!projectId.value) return

    try {
        let url = `projects/${projectId.value}/members/`
        if (searchQuery.trim()) {
            url += `?search=${encodeURIComponent(searchQuery.trim())}`
        }

        const response = await axios.get(url)
        projectMembers.value = response.data.data || response.data || []
    } catch (err) {
        console.error('Failed to fetch project members:', err)
        projectMembers.value = []
    }
}

const updateTask = async () => {
    if (!form.title.trim() || !props.task) return

    try {
        updating.value = true
        error.value = ''

        // Prepare payload
        const payload = {
            title: form.title.trim(),
            description: form.description.trim() || null,
            priority: form.priority,
            members: form.assigned_members
        }

        // Add optional fields
        if (form.status_id) {
            payload.status_id = parseInt(form.status_id)
        }

        if (form.scheduled_start) {
            // Handle date conversion properly
            let startDate
            if (typeof form.scheduled_start === 'string') {
                startDate = new Date(form.scheduled_start)
            } else if (form.scheduled_start instanceof Date) {
                startDate = form.scheduled_start
            }
            if (startDate && !isNaN(startDate.getTime())) {
                payload.start_date = startDate.toISOString()
            } else {
                payload.start_date = null
            }
        } else {
            payload.start_date = null
        }

        if (form.target_completion) {
            // Handle date conversion properly
            let endDate
            if (typeof form.target_completion === 'string') {
                endDate = new Date(form.target_completion)
            } else if (form.target_completion instanceof Date) {
                endDate = form.target_completion
            }
            if (endDate && !isNaN(endDate.getTime())) {
                payload.due_date = endDate.toISOString()
            } else {
                payload.due_date = null
            }
        } else {
            payload.due_date = null
        } if (form.estimated_hours) {
            payload.estimated_hours = form.estimated_hours
        } else {
            payload.estimated_hours = null
        }

        const response = await axios.patch(`projects/${projectId.value}/tasks/${props.task.id}/`, payload)
        const updatedTask = response.data.data || response.data

        emit('updated', updatedTask)
    } catch (err) {
        console.error('Failed to update task:', err)

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
            error.value = 'Failed to update task. Please try again.'
        }
    } finally {
        updating.value = false
    }
}

const getInitials = (member) => {
    if (member.user_name) {
        const nameParts = member.user_name.trim().split(' ')
        if (nameParts.length >= 2) {
            return `${nameParts[0].charAt(0)}${nameParts[nameParts.length - 1].charAt(0)}`.toUpperCase()
        } else {
            return nameParts[0].charAt(0).toUpperCase()
        }
    } else if (member.user_email) {
        return member.user_email.charAt(0).toUpperCase()
    }
    return '?'
}

const getSelectedMemberName = (memberId) => {
    const member = projectMembers.value.find(m => m.user === memberId)
    if (member) {
        return member.user_name ?
            member.user_name.trim() :
            member.user_email || 'Unknown'
    }
    return 'Unknown'
}

const removeMember = (memberId) => {
    const index = form.assigned_members.indexOf(memberId)
    if (index > -1) {
        form.assigned_members.splice(index, 1)
    }
}

// Initialize on mount
onMounted(() => {
    if (props.isOpen && props.task) {
        populateForm(props.task)
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

/* Custom flatpickr styling */
:deep(.flatpickr-input) {
    background-color: #ffffff;
    border: 1px solid #d1d5db;
    border-radius: 0.5rem;
    padding: 0.5rem 0.75rem;
    font-size: 0.875rem;
    transition: all 0.2s;
}

:deep(.flatpickr-input:focus) {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

:deep(.flatpickr-calendar) {
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    border-radius: 0.75rem;
    border: none;
}
</style>