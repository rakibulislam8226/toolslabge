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
            <BaseInput v-model="form.title" label="Title" placeholder="Enter task title" required
                :error="fieldErrors.title" />

            <!-- Description -->
            <BaseTextarea v-model="form.description" label="Description" placeholder="Enter task description" :rows="3"
                :error="fieldErrors.description" />

            <!-- Status and Priority Row -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <!-- Status -->
                <BaseSelect v-model="form.status_id" label="Status" placeholder="Select status" :options="statuses"
                    option-value="id" option-label="name" :error="fieldErrors.status_id" />

                <!-- Priority -->
                <BaseSelect v-model="form.priority" label="Priority" :options="priorityOptions"
                    :error="fieldErrors.priority" />
            </div>

            <!-- Scheduling Section -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <!-- Scheduled Start -->
                <BaseDatePicker v-model="form.scheduled_start" label="Scheduled Start"
                    placeholder="Select start date & time" :error="fieldErrors.start_date" />

                <!-- Target Completion -->
                <BaseDatePicker v-model="form.target_completion" label="Target Completion"
                    placeholder="Select completion date & time" :error="fieldErrors.due_date" />
            </div>

            <!-- Estimated Hours -->
            <BaseInput v-model="form.estimated_hours" label="Estimated Hours" type="number" placeholder="e.g., 4.5"
                step="0.5" min="0" max="999" :error="fieldErrors.estimated_hours" />

            <!-- Team Assignment -->
            <div>
                <label for="edit-assigned-members" class="block text-sm font-medium text-gray-700 mb-1">
                    Team Assignment
                </label>

                <!-- Search Input -->
                <!-- Search Input -->
                <div class="mb-2">
                    <BaseInput placeholder="Search team members..." @input="debouncedMemberSearch($event.target.value)"
                        size="sm" />
                </div> <!-- Selected Members Display -->
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
import { ref, reactive, watch, computed, onMounted, nextTick, inject } from 'vue'
import axios from "@/plugins/axiosConfig.js"
import BaseModal from './BaseModal.vue'
import { BaseInput, BaseTextarea, BaseSelect, BaseDatePicker } from '@/components/forms'

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
    },
    projectSlug: {
        type: String,
        required: true
    }
})

// Emits
const emit = defineEmits(['close', 'updated'])

const $toast = inject("toast")

// Priority options
const priorityOptions = [
    { value: 'low', label: 'Low' },
    { value: 'medium', label: 'Medium' },
    { value: 'high', label: 'High' }
]

// Reactive data
const loading = ref(false)
const updating = ref(false)
const error = ref('')
const fieldErrors = ref({})
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
    form.scheduled_start = task.start_date || null
    form.target_completion = task.due_date || null
    form.estimated_hours = task.estimated_hours || null
    form.assigned_members = task.assigned_members ? task.assigned_members.map(m => m.id) : []
    error.value = ''
    fieldErrors.value = {}
}

const closeModal = () => {
    if (!updating.value) {
        emit('close')
    }
}

const fetchProjectMembers = async (searchQuery = '') => {
    if (!props.projectSlug) return

    try {
        let url = `projects/${props.projectSlug}/members/`
        if (searchQuery.trim()) {
            url += `?search=${encodeURIComponent(searchQuery.trim())}`
        }

        const response = await axios.get(url)
        projectMembers.value = response.data.data || response.data || []
    } catch (err) {
        projectMembers.value = []
    }
}

const updateTask = async () => {
    if (!form.title.trim() || !props.task) return

    try {
        updating.value = true
        error.value = ''
        fieldErrors.value = {}

        const payload = {
            title: form.title.trim(),
            description: form.description.trim() || null,
            priority: form.priority,
            members: form.assigned_members
        }

        if (form.status_id) {
            payload.status_id = parseInt(form.status_id)
        }

        if (form.scheduled_start) {
            const startDate = new Date(form.scheduled_start)
            if (!isNaN(startDate.getTime())) {
                payload.start_date = startDate.toISOString()
            }
        }

        if (form.target_completion) {
            const endDate = new Date(form.target_completion)
            if (!isNaN(endDate.getTime())) {
                payload.due_date = endDate.toISOString()
            }
        }

        if (form.estimated_hours) {
            payload.estimated_hours = form.estimated_hours
        }

        const response = await axios.patch(`projects/${projectId.value}/tasks/${props.task.id}/`, payload)
        const updatedTask = response.data.data || response.data
        $toast.success('Task updated successfully')

        emit('updated', updatedTask)
    } catch (err) {
        const responseData = err.response?.data

        if (responseData?.message) {
            $toast.error(responseData.message)
        }

        if (responseData?.data?.errors && Array.isArray(responseData.data.errors)) {
            responseData.data.errors.forEach(errorItem => {
                Object.assign(fieldErrors.value, errorItem)
            })
        } else if (!responseData?.message) {
            error.value = 'Failed to update task. Please try again.'
            $toast.error('Failed to update task')
        }
    } finally {
        updating.value = false
    }
}

const getInitials = (member) => {
    const name = member.user_name || member.user_email
    if (!name) return '?'

    const parts = name.trim().split(' ')
    return parts.length > 1
        ? `${parts[0][0]}${parts[parts.length - 1][0]}`.toUpperCase()
        : parts[0][0].toUpperCase()
}

const getSelectedMemberName = (memberId) => {
    const member = projectMembers.value.find(m => m.user === memberId)
    return member?.user_name?.trim() || member?.user_email || 'Unknown'
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