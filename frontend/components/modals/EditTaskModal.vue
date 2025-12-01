<template>
    <BaseModal :is-open="isOpen" title="Edit Task" size="xxxl" @close="closeModal">
        <!-- Loading State -->
        <div v-if="loading" class="flex items-center justify-center py-8">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <span class="ml-2 text-gray-600">Loading task details...</span>
        </div>

        <!-- Main Content - Responsive Layout with Tabs on Mobile -->
        <div v-else class="h-[75vh] flex flex-col">
            <!-- Mobile Tabs (visible only on mobile) -->
            <div class="lg:hidden mb-4">
                <div class="border-b border-gray-200 dark:border-gray-700">
                    <nav class="-mb-px flex space-x-8">
                        <button @click="activeTab = 'edit'" :class="[
                            'py-2 px-1 border-b-2 font-medium text-sm whitespace-nowrap',
                            activeTab === 'edit'
                                ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
                        ]">
                            Edit Task
                        </button>
                        <button @click="activeTab = 'comments'" :class="[
                            'py-2 px-1 border-b-2 font-medium text-sm whitespace-nowrap',
                            activeTab === 'comments'
                                ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
                        ]">
                            Comments ({{ commentsCount }})
                        </button>
                    </nav>
                </div>
            </div>

            <!-- Desktop Layout & Mobile Tab Content -->
            <div class="flex-1 flex flex-col lg:flex-row gap-4 lg:gap-6 min-h-0">
                <div :class="[
                    'flex-1 lg:pr-6 lg:border-r border-gray-200 dark:border-gray-700 lg:min-w-0 min-h-0',
                    { 'hidden lg:block': activeTab !== 'edit' }
                ]">
                    <div class="h-full overflow-y-auto pr-2 custom-scrollbar">
                        <form @submit.prevent="updateTask" class="space-y-4 pb-4">
                            <BaseInput v-model="form.title" label="Title" placeholder="Enter task title" required
                                :error="fieldErrors.title" :disabled="!canEditTask" />

                            <BaseTextarea v-model="form.description" label="Description"
                                placeholder="Enter task description" :rows="3" :error="fieldErrors.description"
                                :disabled="!canEditTask" />

                            <!-- Status and Priority Row -->
                            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                <BaseSelect v-model="form.status_id" label="Status" placeholder="Select status"
                                    :options="statuses" option-value="id" option-label="name"
                                    :error="fieldErrors.status_id" :disabled="!canEditTask" />

                                <BaseSelect v-model="form.priority" label="Priority" :options="priorityOptions"
                                    :error="fieldErrors.priority" :disabled="!canEditTask" />
                            </div>

                            <!-- Scheduling Section -->
                            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                <BaseDatePicker v-model="form.scheduled_start" label="Scheduled Start"
                                    placeholder="Select start date & time" :error="fieldErrors.start_date"
                                    :disabled="!canEditTask || !canEditDateRelated" />

                                <BaseDatePicker v-model="form.target_completion" label="Target Completion"
                                    placeholder="Select completion date & time" :error="fieldErrors.due_date"
                                    :disabled="!canEditTask || !canEditDateRelated" />
                            </div>

                            <!-- Estimated Hours -->
                            <BaseInput v-model="form.estimated_hours" label="Estimated Hours" type="number"
                                placeholder="e.g., 4.5" step="0.5" min="0" max="999"
                                :error="fieldErrors.estimated_hours" :disabled="!canEditTask || !canEditDateRelated" />

                            <!-- Deadline Extension Section -->
                            <div class="space-y-4 deadline-extension-responsive">
                                <div
                                    class="rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden bg-white dark:bg-gray-800">
                                    <div
                                        class="px-3 lg:px-6 py-3 lg:py-4 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
                                        <div class="flex items-center space-x-3">
                                            <div>
                                                <h3 class="text-sm font-semibold text-gray-900 dark:text-gray-100">
                                                    Deadline Extension</h3>
                                                <p class="text-xs text-gray-600 dark:text-gray-400">Extend deadlines
                                                    when needed</p>
                                            </div>
                                        </div>
                                    </div>

                                    <div class="p-3 lg:p-6 space-y-4 lg:space-y-5">
                                        <!-- Current Due Date Card -->
                                        <div v-if="form.target_completion"
                                            class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4 shadow-sm glass-card">
                                            <div class="flex items-center justify-between">
                                                <div class="flex items-center space-x-3">
                                                    <div class="w-2 h-2 bg-blue-500 rounded-full deadline-pulse"></div>
                                                    <div>
                                                        <p
                                                            class="text-xs font-medium text-gray-600 dark:text-gray-400 uppercase tracking-wider">
                                                            Current Deadline</p>
                                                        <p
                                                            class="text-sm font-semibold text-gray-900 dark:text-gray-100 mt-0.5">
                                                            {{ formatDateTime(form.target_completion) }}
                                                        </p>
                                                    </div>
                                                </div>
                                                <div class="text-right">
                                                    <span
                                                        class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-gray-700 dark:text-blue-200 status-indicator">
                                                        Active
                                                    </span>
                                                </div>
                                            </div>
                                        </div>

                                        <!-- Extension Form -->
                                        <div
                                            class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4 space-y-4 glass-card">
                                            <div class="flex items-center space-x-2 mb-3">
                                                <svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor"
                                                    viewBox="0 0 24 24">
                                                    <path stroke-linecap="round" stroke-linejoin="round"
                                                        stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                                                </svg>
                                                <h4 class="text-sm font-medium text-gray-900 dark:text-gray-100">Request
                                                    Extension</h4>
                                            </div>

                                            <div class="grid gap-4">
                                                <!-- New Deadline -->
                                                <div>
                                                    <BaseDatePicker v-model="deadlineExtension.new_due_date"
                                                        label="New Deadline"
                                                        placeholder="Select new deadline date & time"
                                                        :error="deadlineExtension.errors.new_due_date"
                                                        class="deadline-picker"
                                                        :disabled="!canEditTask || !canEditDateRelated" />
                                                </div>

                                                <!-- Reason -->
                                                <div>
                                                    <BaseTextarea v-model="deadlineExtension.reason"
                                                        label="Justification"
                                                        placeholder="Briefly explain why this extension is necessary..."
                                                        :rows="3" :error="deadlineExtension.errors.reason"
                                                        class="reason-input"
                                                        :disabled="!canEditTask || !canEditDateRelated" />
                                                </div>

                                                <!-- Submit Button -->
                                                <button @click="submitDeadlineExtension"
                                                    :disabled="!deadlineExtension.new_due_date || extensionLoading || !canEditTask || !canEditDateRelated"
                                                    type="button"
                                                    class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium py-3 px-4 rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-md hover:shadow-lg transform hover:-translate-y-0.5 disabled:transform-none deadline-extend-btn">
                                                    <span v-if="extensionLoading"
                                                        class="flex items-center justify-center">
                                                        <svg class="animate-spin -ml-1 mr-3 h-4 w-4" fill="none"
                                                            viewBox="0 0 24 24">
                                                            <circle class="opacity-25" cx="12" cy="12" r="10"
                                                                stroke="currentColor" stroke-width="4" />
                                                            <path class="opacity-75" fill="currentColor"
                                                                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                                                        </svg>
                                                        Processing Extension...
                                                    </span>
                                                    <span v-else class="flex items-center justify-center">
                                                        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor"
                                                            viewBox="0 0 24 24">
                                                            <path stroke-linecap="round" stroke-linejoin="round"
                                                                stroke-width="2"
                                                                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                                        </svg>
                                                        Extend Deadline
                                                    </span>
                                                </button>
                                            </div>
                                        </div>

                                        <!-- Extension History -->
                                        <div v-if="deadlineExtensions.length > 0"
                                            class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden glass-card">
                                            <div
                                                class="px-4 py-3 bg-gray-50 dark:bg-gray-700 border-b border-gray-200 dark:border-gray-600">
                                                <div class="flex items-center space-x-2">
                                                    <h4 class="text-sm font-medium text-gray-900 dark:text-gray-100">
                                                        Extension
                                                        History
                                                    </h4>
                                                    <span
                                                        class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-gray-200 text-gray-800 dark:bg-gray-600 dark:text-gray-200 extension-badge">
                                                        {{ deadlineExtensions.length }}
                                                    </span>
                                                </div>
                                            </div>

                                            <div class="max-h-48 overflow-y-auto extension-history-scroll">
                                                <div class="divide-y divide-gray-200 dark:divide-gray-700">
                                                    <div v-for="(extension, index) in deadlineExtensions"
                                                        :key="extension.id"
                                                        class="p-4 hover:bg-gray-100 dark:hover:bg-gray-700/50 transition-colors duration-150 extension-item">
                                                        <div class="flex items-start justify-between space-x-4">
                                                            <div class="flex-1 min-w-0">
                                                                <!-- Timeline -->
                                                                <div class="flex items-center space-x-2 text-sm">
                                                                    <span
                                                                        class="text-gray-500 dark:text-gray-400 font-medium">
                                                                        {{ formatDateTime(extension.previous_due_date)
                                                                        }}
                                                                    </span>
                                                                    <svg class="w-4 h-4 text-gray-400" fill="none"
                                                                        stroke="currentColor" viewBox="0 0 24 24">
                                                                        <path stroke-linecap="round"
                                                                            stroke-linejoin="round" stroke-width="2"
                                                                            d="M9 5l7 7-7 7" />
                                                                    </svg>
                                                                    <span
                                                                        class="text-gray-900 dark:text-gray-100 font-semibold">
                                                                        {{ formatDateTime(extension.new_due_date) }}
                                                                    </span>
                                                                </div>

                                                                <!-- Reason -->
                                                                <div v-if="extension.reason" class="mt-2">
                                                                    <p
                                                                        class="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
                                                                        {{ extension.reason }}
                                                                    </p>
                                                                </div>

                                                                <!-- Meta info -->
                                                                <div
                                                                    class="flex items-center space-x-4 mt-2 text-xs text-gray-500 dark:text-gray-400">
                                                                    <span class="flex items-center space-x-1">
                                                                        <svg class="w-3 h-3" fill="none"
                                                                            stroke="currentColor" viewBox="0 0 24 24">
                                                                            <path stroke-linecap="round"
                                                                                stroke-linejoin="round" stroke-width="2"
                                                                                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                                                        </svg>
                                                                        <span>{{ extension.created_by || 'Unknown'
                                                                            }}</span>
                                                                    </span>
                                                                    <span class="flex items-center space-x-1">
                                                                        <svg class="w-3 h-3" fill="none"
                                                                            stroke="currentColor" viewBox="0 0 24 24">
                                                                            <path stroke-linecap="round"
                                                                                stroke-linejoin="round" stroke-width="2"
                                                                                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                                                        </svg>
                                                                        <span>{{ formatDateTime(extension.created_at)
                                                                            }}</span>
                                                                    </span>
                                                                </div>
                                                            </div>

                                                            <!-- Extension number badge -->
                                                            <div class="shrink-0">
                                                                <span
                                                                    class="inline-flex items-center justify-center w-6 h-6 rounded-full text-xs font-medium extension-badge"
                                                                    :class="index === 0 ? 'bg-blue-100 text-blue-800 dark:bg-gray-700 dark:text-blue-200' : 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-400'">
                                                                    {{ deadlineExtensions.length - index }}
                                                                </span>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Task Members -->
                            <div>
                                <div class="mb-2">
                                    <BaseInput label="Task Members" placeholder="Search task members..."
                                        @input="debouncedMemberSearch($event.target.value)" size="sm"
                                        :disabled="!canEditTask || !canEditDateRelated" />
                                </div> <!-- Selected Members Display -->
                                <div v-if="form.assigned_members.length > 0"
                                    class="mb-2 p-2 bg-gray-50 dark:bg-blue-900/20 rounded-lg">
                                    <div class="text-xs font-medium text-gray-600 dark:text-blue-300 mb-1">Assigned Team
                                        Members:</div>
                                    <div class="flex flex-wrap gap-1">
                                        <span v-for="memberId in form.assigned_members" :key="memberId"
                                            class="inline-flex items-center px-2 py-1 text-xs bg-gray-100 dark:bg-blue-800 text-gray-700 dark:text-blue-200 rounded-full">
                                            {{ getSelectedMemberName(memberId) }}
                                            <button v-if="canEditTask && canEditDateRelated"
                                                @click="removeMember(memberId)"
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
                                        class="flex items-center space-x-2 hover:bg-blue-50 hover:border-blue-200 border border-transparent dark:hover:bg-gray-700 dark:hover:border-gray-600 p-1 rounded cursor-pointer transition-all duration-200"
                                        :class="{ 'opacity-50 cursor-not-allowed': !canEditTask || !canEditDateRelated }">
                                        <input type="checkbox" :value="member.user" v-model="form.assigned_members"
                                            class="rounded border-gray-200 dark:border-gray-600 text-blue-600 focus:ring-blue-500 dark:bg-gray-700"
                                            :disabled="!canEditTask || !canEditDateRelated" />
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
                    </div>
                </div>

                <!-- Right Side - Comments Section -->
                <div :class="[
                    'w-full lg:w-96 min-h-0',
                    { 'hidden lg:block': activeTab !== 'comments' }
                ]">
                    <TaskCommentsSection :task-id="task?.id" :project-id="projectId" :project-members="projectMembers"
                        @comments-updated="handleCommentsUpdated" />
                </div>
            </div>
        </div>

        <template #footer>
            <div class="flex space-x-3 justify-end">
                <BaseButton variant="secondary" @click="closeModal" :disabled="updating" type="button">
                    Cancel
                </BaseButton>

                <BaseButton variant="primary" @click="updateTask"
                    :disabled="updating || !form.title.trim() || !canEditTask" :loading="updating"
                    loadingText="Updating...">
                    Update Task
                </BaseButton>
            </div>
        </template>
    </BaseModal>

    <!-- Confirmation Modal -->
    <ConfirmModal :is-open="showConfirmModal" :title="confirmModalData.title" :message="confirmModalData.message"
        :confirm-text="confirmModalData.confirmText" cancel-text="Cancel"
        confirm-class="bg-red-600 hover:bg-red-700 focus:ring-red-500" @confirm="handleConfirmAction"
        @cancel="handleCancelConfirm" />
</template>

<script setup>
import { ref, reactive, watch, computed, onMounted, nextTick, inject } from 'vue'
import axios from "@/plugins/axiosConfig.js"
import { useAuth } from '@/composables/useAuth.js'
import BaseModal from './BaseModal.vue'
import ConfirmModal from './ConfirmModal.vue'
import TaskCommentsSection from '@/components/tasks/TaskCommentsSection.vue'
import { BaseInput, BaseTextarea, BaseSelect, BaseDatePicker, BaseButton } from '@/components/forms'
import { useRoute } from 'vue-router'

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
        default: ''
    }
})

// Emits
const emit = defineEmits(['close', 'updated'])

const $toast = inject("toast")
const { user } = useAuth()
const route = useRoute()

// Priority options
const priorityOptions = [
    { value: 'low', label: 'Low' },
    { value: 'medium', label: 'Medium' },
    { value: 'high', label: 'High' }
]

// Reactive data
const loading = ref(false)
const updating = ref(false)
const extensionLoading = ref(false)
const error = ref('')
const fieldErrors = ref({})
const projectMembers = ref([])
const memberSearchQuery = ref('')
const searchTimeout = ref(null)
const deadlineExtensions = ref([])

// Mobile tab state
const activeTab = ref('edit') // 'edit' | 'comments'

// Comments count for UI display
const commentsCount = ref(0)

// Project role for permissions
const myProjectRole = ref('')

// Confirmation modal state
const showConfirmModal = ref(false)
const confirmModalData = ref({
    title: '',
    message: '',
    confirmText: '',
    action: null
})

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

const deadlineExtension = reactive({
    new_due_date: null,
    reason: '',
    errors: {}
})

// Computed
const projectId = computed(() => {
    return props.task?.project?.id
})

// Permission checking computed properties
const isTaskOwner = computed(() => {
    return user.value && props.task && user.value.id === props.task.created_by
})

const canEditTask = computed(() => {
    if (!props.task || !user.value) return false

    // Manager can edit everything regardless of ownership
    if (myProjectRole.value === 'manager') return true

    if (myProjectRole.value === 'contributor') return true

    // Viewer cannot edit anything
    if (myProjectRole.value === 'viewer') return false

    return false
})

const canEditDateRelated = computed(() => {
    // Managers can always edit deadlines
    if (myProjectRole.value === 'manager') return true

    // Contributors can edit if they are the task owner
    if (myProjectRole.value === 'contributor' && isTaskOwner.value) return true

    // Viewers cannot edit deadlines
    return false
})

// Handler for comments updated event from TaskCommentsSection
const handleCommentsUpdated = (updatedComments) => {
    commentsCount.value = updatedComments.length
}

// Confirmation modal handlers  
const handleConfirmAction = async () => {
    if (confirmModalData.value.action) {
        await confirmModalData.value.action()
    }
}

const handleCancelConfirm = () => {
    showConfirmModal.value = false
    confirmModalData.value = {
        title: '',
        message: '',
        confirmText: '',
        action: null
    }
}

// Fetch detailed task information
const fetchTaskDetails = async () => {
    if (!props.task?.id || !projectId.value) return

    try {
        loading.value = true
        const response = await axios.get(`projects/${projectId.value}/tasks/${props.task.id}/`)
        const taskDetails = response.data.data || response.data
        populateForm(taskDetails)
        myProjectRole.value = taskDetails.my_project_role || ''

        // Fetch deadline extensions separately if not included
        if (!taskDetails.deadline_extensions) {
            await fetchDeadlineExtensions()
        }
    } catch (err) {
        console.error('Failed to fetch task details:', err)
        error.value = 'Failed to load task details'
        // Fallback to basic task data
        populateForm(props.task)
    } finally {
        loading.value = false
    }
}

// Fetch deadline extensions history
const fetchDeadlineExtensions = async () => {
    if (!props.task?.id || !projectId.value) return

    try {
        const response = await axios.get(`projects/${projectId.value}/tasks/${props.task.id}/extend-deadline/`)
        deadlineExtensions.value = response.data.data || response.data || []
    } catch (err) {
        console.error('Failed to fetch deadline extensions:', err)
        deadlineExtensions.value = []
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

    // Populate deadline extensions history if available
    deadlineExtensions.value = Array.isArray(task.deadline_extensions) ? task.deadline_extensions : []

    error.value = ''
    fieldErrors.value = {}

    // Reset deadline extension form
    deadlineExtension.new_due_date = null
    deadlineExtension.reason = ''
    deadlineExtension.errors = {}
}

const formatDateTime = (dateString) => {
    if (!dateString) return ''
    try {
        return new Date(dateString).toLocaleString()
    } catch (e) {
        return dateString
    }
}

const submitDeadlineExtension = async () => {
    if (!deadlineExtension.new_due_date || !props.task?.id) return

    try {
        extensionLoading.value = true
        deadlineExtension.errors = {}

        const payload = {
            task: props.task.id,
            new_due_date: new Date(deadlineExtension.new_due_date).toISOString(),
            reason: deadlineExtension.reason.trim() || null
        }

        const response = await axios.post(
            `projects/${projectId.value}/tasks/${props.task.id}/extend-deadline/`,
            payload
        )

        const newExtension = response.data.data || response.data

        // Add to history
        deadlineExtensions.value.unshift(newExtension)

        // Update the task's due date in the form
        form.target_completion = newExtension.new_due_date

        // Reset form
        deadlineExtension.new_due_date = null
        deadlineExtension.reason = ''

        $toast.success('Deadline extended successfully')

        // Emit updated task to parent
        const updatedTask = { ...props.task, due_date: newExtension.new_due_date }
        emit('updated', updatedTask)

    } catch (err) {
        const responseData = err.response?.data

        if (responseData?.message) {
            $toast.error(responseData.message)
        }

        if (responseData?.data?.errors) {
            deadlineExtension.errors = responseData.data.errors
        } else if (!responseData?.message) {
            deadlineExtension.errors = { general: 'Failed to extend deadline. Please try again.' }
            $toast.error('Failed to extend deadline')
        }
    } finally {
        extensionLoading.value = false
    }
}

const closeModal = () => {
    if (!updating.value) {
        emit('close')
    }
}

const fetchProjectMembers = async (searchQuery = '') => {
    // Try to get project identifier from props or task data
    let projectIdentifier = props.projectSlug

    if (!projectIdentifier && props.task?.project) {
        // If no projectSlug prop but we have task project data, use project ID
        projectIdentifier = props.task.project.id || props.task.project.slug
    }

    if (!projectIdentifier) {
        console.warn('No project identifier available for fetching members')
        return
    }

    // If we already have members and no search query, don't refetch
    if (!searchQuery.trim() && projectMembers.value.length > 0) {
        return
    }

    try {
        let url = `projects/${projectIdentifier}/members/`
        if (searchQuery.trim()) {
            url += `?search=${encodeURIComponent(searchQuery.trim())}`
        }

        const response = await axios.get(url)
        projectMembers.value = response.data.data || response.data || []
    } catch (err) {
        console.error('Failed to fetch project members:', err)
        if (!searchQuery.trim()) {
            // Only clear members if it's the initial fetch that failed
            projectMembers.value = []
        }
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
            activeTab.value = 'edit' // Reset to edit tab when modal opens
            if (props.task) {
                fetchTaskDetails()
                fetchProjectMembers()
                // fetchCurrentUser()
            }
        } else {
            document.body.style.overflow = ''
        }
    })
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

/* Modern deadline extension styling */
.deadline-picker :deep(.flatpickr-input) {
    background: linear-gradient(to right, #fefbf3, #fef9f1);
    border: 1px solid #f3e8d0;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.deadline-picker :deep(.flatpickr-input:focus) {
    border-color: #f59e0b;
    box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.1);
    background: #ffffff;
}

.reason-input :deep(textarea) {
    background: linear-gradient(to right, #fefbf3, #fef9f1);
    border: 1px solid #f3e8d0;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    resize: vertical;
    min-height: 80px;
}

.reason-input :deep(textarea:focus) {
    border-color: #f59e0b;
    box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.1);
    background: #ffffff;
}

/* Smooth transitions for deadline section */
.deadline-section {
    animation: slideIn 0.5s ease-out;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Extension history animations */
.extension-history-enter-active {
    transition: all 0.3s ease-out;
}

.extension-history-enter-from {
    opacity: 0;
    transform: translateX(-20px);
}

.extension-history-enter-to {
    opacity: 1;
    transform: translateX(0);
}

/* Custom scrollbar for extension history */
.extension-history-scroll::-webkit-scrollbar {
    width: 6px;
}

.extension-history-scroll::-webkit-scrollbar-track {
    background: #f1f5f9;
    border-radius: 3px;
}

.extension-history-scroll::-webkit-scrollbar-thumb {
    background: linear-gradient(to bottom, #f59e0b, #d97706);
    border-radius: 3px;
}

.extension-history-scroll::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(to bottom, #d97706, #b45309);
}

/* Button hover effects */
.deadline-extend-btn {
    position: relative;
    overflow: hidden;
}

.deadline-extend-btn:before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: left 0.5s;
}

.deadline-extend-btn:hover:before {
    left: 100%;
}

/* Glass morphism effect for cards */
.glass-card {
    backdrop-filter: blur(12px);
    background: rgba(255, 255, 255, 0.8);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.dark .glass-card {
    background: rgba(31, 41, 55, 0.8);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

/* Pulse animation for active deadline */
.deadline-pulse {
    animation: pulse 2s infinite;
}

@keyframes pulse {

    0%,
    100% {
        transform: scale(1);
        opacity: 1;
    }

    50% {
        transform: scale(1.05);
        opacity: 0.9;
    }
}

/* Extension badge animation */
.extension-badge {
    animation: bounceIn 0.5s ease-out;
}

@keyframes bounceIn {
    0% {
        opacity: 0;
        transform: scale(0.3);
    }

    50% {
        opacity: 1;
        transform: scale(1.05);
    }

    70% {
        transform: scale(0.9);
    }

    100% {
        opacity: 1;
        transform: scale(1);
    }
}

/* Hover effects for extension history items */
.extension-item {
    transition: all 0.2s ease-out;
    border-left: 3px solid transparent;
}

.extension-item:hover {
    border-left-color: #f59e0b;
    transform: translateX(4px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.dark .extension-item:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

/* Status indicators with subtle animations */
.status-indicator {
    position: relative;
}

.status-indicator::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, transparent 30%, rgba(255, 255, 255, 0.1) 50%, transparent 70%);
    animation: shimmer 2s infinite;
}

@keyframes shimmer {
    0% {
        transform: translateX(-100%);
    }

    100% {
        transform: translateX(100%);
    }
}

/* Dark mode enhancements */
@media (prefers-color-scheme: dark) {
    .deadline-picker :deep(.flatpickr-input) {
        background: linear-gradient(to right, #1f2937, #374151);
        border-color: #4b5563;
        color: #f9fafb;
    }

    .reason-input :deep(textarea) {
        background: linear-gradient(to right, #1f2937, #374151);
        border-color: #4b5563;
        color: #f9fafb;
    }
}

/* Comments Section Styling */
.comment-textarea :deep(textarea) {
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    transition: all 0.2s ease-in-out;
    resize: vertical;
    min-height: 80px;
}

.comment-textarea :deep(textarea:focus) {
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    outline: none;
}

.comment-item {
    transition: all 0.2s ease-out;
    position: relative;
}

.comment-item:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.dark .comment-item:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

/* Custom scrollbar for comments */
.overflow-y-auto::-webkit-scrollbar {
    width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
    background: #f1f5f9;
    border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
    background: linear-gradient(to bottom, #3b82f6, #2563eb);
    border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(to bottom, #2563eb, #1d4ed8);
}

.dark .overflow-y-auto::-webkit-scrollbar-track {
    background: #374151;
}

.dark .overflow-y-auto::-webkit-scrollbar-thumb {
    background: linear-gradient(to bottom, #4f46e5, #3730a3);
}

/* Animation for new comments */
.comment-item {
    animation: slideInComment 0.3s ease-out;
}

@keyframes slideInComment {
    from {
        opacity: 0;
        transform: translateX(20px);
    }

    to {
        opacity: 1;
        transform: translateX(0);
    }
}

/* Button hover effects for comments */
.comment-item button {
    transition: all 0.2s ease-out;
}

.comment-item button:hover {
    transform: scale(1.05);
}

/* Multiple attachments styling */
.attachment-item {
    transition: all 0.2s ease-out;
    animation: slideInAttachment 0.3s ease-out;
}

.attachment-item:hover {
    transform: translateX(2px);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.dark .attachment-item:hover {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.attachment-preview {
    animation: fadeIn 0.3s ease-out;
}

@keyframes slideInAttachment {
    from {
        opacity: 0;
        transform: translateY(10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }
}

/* Attachment grid hover effects */
.attachment-preview .group:hover img {
    filter: brightness(1.1);
}

/* Scrollbar styling for attachment lists */
.max-h-40::-webkit-scrollbar {
    width: 4px;
}

.max-h-40::-webkit-scrollbar-track {
    background: #f1f5f9;
    border-radius: 2px;
}

.max-h-40::-webkit-scrollbar-thumb {
    background: linear-gradient(to bottom, #3b82f6, #2563eb);
    border-radius: 2px;
}

.dark .max-h-40::-webkit-scrollbar-track {
    background: #374151;
}

/* Mobile-first responsive design with tabs */
@media (max-width: 1023px) {

    /* Mobile modal uses full height more efficiently */
    .h-\[75vh\] {
        height: 85vh !important;
    }

    /* Tab transitions */
    .hidden.lg\:block {
        animation: fadeIn 0.2s ease-in-out;
    }
}

@media (max-width: 640px) {

    /* Extra mobile optimizations */
    .modal-layout {
        height: 90vh !important;
    }

    /* Better mobile padding for deadline extension */
    .deadline-extension-responsive .p-3,
    .deadline-extension-responsive .lg\:p-6 {
        padding: 0.75rem !important;
    }

    .deadline-extension-responsive .px-3,
    .deadline-extension-responsive .lg\:px-6 {
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
    }

    .deadline-extension-responsive .space-y-4,
    .deadline-extension-responsive .lg\:space-y-5>*+* {
        margin-top: 0.75rem !important;
    }

    /* Mobile attachment grid */
    .attachment-preview .grid-cols-2 {
        grid-template-columns: repeat(1, 1fr);
    }

    /* Reduce spacing on mobile */
    .space-y-4>*+* {
        margin-top: 0.75rem !important;
    }

    .lg\:space-y-4>*+* {
        margin-top: 0.75rem !important;
    }

    /* Mobile form controls */
    .grid-cols-1.sm\:grid-cols-2 {
        grid-template-columns: 1fr !important;
        gap: 0.75rem !important;
    }

    /* Better mobile buttons */
    .deadline-extend-btn {
        width: 100% !important;
        text-align: center;
    }
}

/* Custom scrollbar for separate scroll areas */
.custom-scrollbar::-webkit-scrollbar {
    width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
    background: #f1f5f9;
    border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background: linear-gradient(to bottom, #3b82f6, #2563eb);
    border-radius: 3px;
    transition: background 0.2s ease;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(to bottom, #2563eb, #1d4ed8);
}

.dark .custom-scrollbar::-webkit-scrollbar-track {
    background: #374151;
}

.dark .custom-scrollbar::-webkit-scrollbar-thumb {
    background: linear-gradient(to bottom, #4f46e5, #3730a3);
}

.dark .custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(to bottom, #3730a3, #312e81);
}

/* Tab animation */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Tab transition */
.hidden.lg\:block {
    animation: fadeIn 0.2s ease-in-out;
}
</style>