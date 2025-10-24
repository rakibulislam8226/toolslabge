<template>
    <div v-if="isOpen" class="fixed inset-0 overflow-y-auto z-50">
        <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <!-- Background overlay with blur -->
            <div class="fixed inset-0 backdrop-blur-md bg-black/20 transition-all duration-300" @click="closeModal">
            </div>

            <!-- Modal panel -->
            <div
                class="relative inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full">
                <!-- Header -->
                <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-lg leading-6 font-medium text-gray-900">Create New Task</h3>
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
                                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="Enter task title" />
                        </div>

                        <!-- Description -->
                        <div>
                            <label for="description" class="block text-sm font-medium text-gray-700 mb-1">
                                Description
                            </label>
                            <textarea id="description" v-model="form.description" rows="3"
                                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
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
                                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent">
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
                                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                                    <option value="low">Low</option>
                                    <option value="medium">Medium</option>
                                    <option value="high">High</option>
                                </select>
                            </div>
                        </div>

                        <!-- Scheduling Section -->
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <!-- Scheduled Start -->
                            <div>
                                <label for="create-scheduled-start"
                                    class="block text-sm font-medium text-gray-700 mb-1">
                                    Scheduled Start
                                </label>
                                <flat-pickr id="create-scheduled-start" v-model="form.scheduled_start"
                                    :config="flatpickrConfig" placeholder="Select start date & time"
                                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
                            </div>

                            <!-- Target Completion -->
                            <div>
                                <label for="create-target-completion"
                                    class="block text-sm font-medium text-gray-700 mb-1">
                                    Target Completion
                                </label>
                                <flat-pickr id="create-target-completion" v-model="form.target_completion"
                                    :config="flatpickrConfig" placeholder="Select completion date & time"
                                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
                            </div>
                        </div> <!-- Estimated Hours -->
                        <div>
                            <label for="estimated_hours" class="block text-sm font-medium text-gray-700 mb-1">
                                Estimated Hours
                            </label>
                            <input id="estimated_hours" v-model.number="form.estimated_hours" type="number" step="0.5"
                                min="0" max="999"
                                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="e.g., 4.5" />
                        </div>

                        <!-- Assign Members -->
                        <!-- Team Assignment -->
                        <div>
                            <label for="create-assigned-members" class="block text-sm font-medium text-gray-700 mb-1">
                                Team Assignment
                            </label>

                            <!-- Search Input -->
                            <div class="mb-2">
                                <input type="text" placeholder="Search team members..."
                                    @input="debouncedMemberSearch($event.target.value)"
                                    class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500" />
                            </div>

                            <!-- Selected Members Display -->
                            <div v-if="form.assigned_members.length > 0" class="mb-2 p-2 bg-blue-50 rounded-lg">
                                <div class="text-xs font-medium text-blue-700 mb-1">Assigned Team Members:</div>
                                <div class="flex flex-wrap gap-1">
                                    <span v-for="memberId in form.assigned_members" :key="memberId"
                                        class="inline-flex items-center px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full">
                                        {{ getSelectedMemberName(memberId) }}
                                        <button @click="removeMember(memberId)"
                                            class="ml-1 text-blue-600 hover:text-blue-800">
                                            ×
                                        </button>
                                    </span>
                                </div>
                            </div>

                            <!-- Members List -->
                            <div class="space-y-2 max-h-32 overflow-y-auto border border-gray-300 rounded-lg p-2">
                                <div v-if="projectMembers.length === 0 && !memberSearchQuery"
                                    class="text-sm text-gray-500 text-center py-2">
                                    No project members available
                                </div>
                                <div v-else-if="projectMembers.length === 0 && memberSearchQuery"
                                    class="text-sm text-gray-500 text-center py-2">
                                    No members found matching "{{ memberSearchQuery }}"
                                </div>
                                <label v-for="member in projectMembers" :key="member.id"
                                    class="flex items-center space-x-2 hover:bg-gray-50 p-1 rounded cursor-pointer">
                                    <input type="checkbox" :value="member.user" v-model="form.assigned_members"
                                        class="rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
                                    <div class="flex items-center space-x-2 flex-1 min-w-0">
                                        <div class="w-6 h-6 rounded-full bg-gray-300 flex items-center justify-center">
                                            <span class="text-xs font-medium text-gray-600">
                                                {{ getInitials(member) }}
                                            </span>
                                        </div>
                                        <span class="text-sm font-medium text-gray-900 truncate">
                                            {{ member.user_name || member.user_email }}
                                        </span>
                                    </div>
                                </label>
                            </div>
                        </div> <!-- Error message -->
                        <div v-if="error" class="bg-red-50 border border-red-200 rounded-md p-3">
                            <p class="text-sm text-red-600">{{ error }}</p>
                        </div>
                    </form>
                </div>

                <!-- Footer -->
                <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                    <button @click="createTask" :disabled="creating || !form.title.trim()"
                        class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed">
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
                        class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed">
                        Cancel
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, watch, computed, onMounted, nextTick } from 'vue'
import axios from "@/plugins/axiosConfig.js"
import flatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'

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
const creating = ref(false)
const error = ref('')
const projectMembers = ref([])
const memberSearchQuery = ref('')
const searchTimeout = ref(null)

const form = reactive({
    title: '',
    description: '',
    status_id: props.initialStatusId || '',
    priority: 'medium',
    scheduled_start: null,
    target_completion: null,
    estimated_hours: null,
    assigned_members: []
})

// Computed properties
const filteredProjectMembers = computed(() => {
    if (!memberSearchQuery.value) {
        return projectMembers.value
    }

    const query = memberSearchQuery.value.toLowerCase()
    return projectMembers.value.filter(member => {
        const fullName = `${member.user.first_name || ''} ${member.user.last_name || ''}`.toLowerCase()
        const email = member.user.email.toLowerCase()
        const role = member.role.toLowerCase()

        return fullName.includes(query) || email.includes(query) || role.includes(query)
    })
})

// Watch for initial status changes
watch(() => props.initialStatusId, (newValue) => {
    if (newValue) {
        form.status_id = newValue
    }
})

// Watch for dialog open/close to reset form and manage body scroll
watch(() => props.isOpen, (isOpen) => {
    nextTick(() => {
        if (isOpen) {
            document.body.style.overflow = 'hidden'
            resetForm()
            fetchProjectMembers()
        } else {
            document.body.style.overflow = ''
        }
    })
})

// Methods
const resetForm = () => {
    form.title = ''
    form.description = ''
    form.status_id = props.initialStatusId || ''
    form.priority = 'medium'
    form.scheduled_start = null
    form.target_completion = null
    form.estimated_hours = null
    form.assigned_members = []
    error.value = ''
    memberSearchQuery.value = ''
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

const closeModal = () => {
    if (!creating.value) {
        emit('close')
    }
}

const fetchProjectMembers = async (searchQuery = '') => {
    if (!props.projectId) return

    try {
        let url = `projects/${props.projectId}/members/`
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
            }
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
            }
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

const getAvatarColor = (user) => {
    const colors = [
        'bg-blue-500', 'bg-green-500', 'bg-yellow-500', 'bg-red-500',
        'bg-purple-500', 'bg-pink-500', 'bg-indigo-500', 'bg-cyan-500'
    ]
    const index = (user.id || user.email.length) % colors.length
    return colors[index]
}

const formatRole = (role) => {
    return role.charAt(0).toUpperCase() + role.slice(1).toLowerCase()
}

const getRoleBadgeClass = (role) => {
    const roleClasses = {
        'manager': 'bg-purple-100 text-purple-800',
        'developer': 'bg-blue-100 text-blue-800',
        'designer': 'bg-pink-100 text-pink-800',
        'tester': 'bg-green-100 text-green-800',
        'member': 'bg-gray-100 text-gray-800'
    }
    return roleClasses[role.toLowerCase()] || 'bg-gray-100 text-gray-800'
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