<template>
    <div class="bg-white rounded-md border border-gray-200 hover:border-gray-300 shadow-sm hover:shadow-lg transition-all duration-300 p-3 group"
        @dragstart="$emit('dragstart', $event)" @dragend="$emit('dragend', $event)">
        <!-- Task Header -->
        <div class="flex items-start justify-between mb-2">
            <div class="flex-1 min-w-0">
                <h6 class="text-sm font-semibold text-gray-900 line-clamp-2 mb-1 cursor-pointer hover:text-blue-600 transition-colors duration-200"
                    @click="editTask">
                    {{ task.title }}
                </h6>
                <div class="flex items-center justify-between">
                    <!-- Priority Badge -->
                    <span class="inline-flex items-center px-1.5 py-1 text-xs font-medium rounded-sm"
                        :class="getPriorityColor(task.priority)">
                        {{ formatPriority(task.priority) }}
                    </span>

                    <!-- Status Change Dropdown (only if allowStatusChange is true) -->
                    <div v-if="typeof allowStatusChange === 'function' ? allowStatusChange(task) === true : allowStatusChange"
                        class="relative">
                        <select :value="task.status?.id || ''" @change="onStatusChange"
                            :class="`text-sm bg-linear-to-r ${getStatusColorClasses(task.status?.id, 'gradient')} border ${getStatusColorClasses(task.status?.id, 'border')} rounded-md px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 hover:shadow-md font-medium ${getStatusColorClasses(task.status?.id, 'text')} shadow-sm cursor-pointer`">
                            <option v-for="status in statuses" :key="status.id" :value="status.id">
                                {{ status.name }}
                            </option>
                        </select>
                    </div>

                    <!-- Status Badge (read-only when allowStatusChange is false) -->
                    <div v-else class="relative">
                        <span
                            :class="`text-sm bg-linear-to-r ${getStatusColorClasses(task.status?.id, 'gradient')} border ${getStatusColorClasses(task.status?.id, 'border')} rounded-lg px-3 py-1.5 font-medium ${getStatusColorClasses(task.status?.id, 'text')} shadow-sm`">
                            {{ task.status?.name || 'No Status' }}
                        </span>
                    </div>
                </div>
            </div>

            <!-- Actions Dropdown -->
            <div class="relative ml-2">
                <button @click="toggleDropdown"
                    class="text-gray-400 hover:text-gray-600 transition-colors duration-200">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 5v.01M12 12v.01M12 19v.01"></path>
                    </svg>
                </button>

                <!-- Dropdown Menu -->
                <div v-if="showDropdown" v-click-outside="closeDropdown"
                    class="absolute right-0 top-6 mt-1 w-40 bg-white rounded-xl shadow-lg border border-gray-200 z-10">
                    <button @click="editTask"
                        class="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 flex items-center rounded-lg transition-colors duration-200">
                        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z">
                            </path>
                        </svg>
                        Edit
                    </button>

                    <button @click="deleteTask"
                        class="w-full text-left px-3 py-2 text-sm text-red-600 hover:bg-red-50 flex items-center rounded-lg transition-colors duration-200">
                        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16">
                            </path>
                        </svg>
                        Delete
                    </button>
                </div>
            </div>
        </div>

        <!-- Task Metadata -->
        <div class="space-y-2">
            <!-- Dates -->
            <div class="flex items-center justify-between text-xs text-gray-500">
                <div class="flex items-center">
                    <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z">
                        </path>
                    </svg>
                    <span>Start: {{ task.start_date ? formatDate(task.start_date) : '-' }}</span>
                </div>
                <div class="flex items-center"
                    :class="{ 'text-red-500': isOverdue && (task.status?.slug.toLowerCase() === 'to-do' || task.status?.slug.toLowerCase() === 'in-progress') }">
                    <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z">
                        </path>
                    </svg>
                    <span>Due: {{ task.due_date ? formatDate(task.due_date) : '-' }}</span>
                    <!-- Extension indicator -->
                    <span v-if="hasDeadlineExtensions"
                        class="ml-1 inline-flex items-center px-1.5 py-0.5 text-xs bg-orange-100 text-orange-700 rounded-full"
                        :title="`Extended ${task.deadline_extensions?.length || 0} time(s)`">
                        <svg class="w-2.5 h-2.5 mr-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                        {{ task.deadline_extensions?.length || 0 }}
                    </span>
                </div>
            </div>

            <!-- Assigned Members -->
            <div v-if="task.assigned_members && task.assigned_members.length > 0" class="flex items-center">
                <svg class="w-3 h-3 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
                <div class="flex -space-x-1">
                    <div v-for="(member, index) in task.assigned_members.slice(0, 3)" :key="member.id" class="relative">
                        <img v-if="member.photo" :src="member.photo" :alt="member.first_name || member.email"
                            class="w-6 h-6 rounded-full border-2 border-white"
                            :title="`${member.first_name || ''} ${member.last_name || ''} (${member.email})`" />
                        <div v-else
                            class="w-6 h-6 rounded-full border-2 border-white bg-gray-300 flex items-center justify-center"
                            :title="`${member.first_name || ''} ${member.last_name || ''} (${member.email})`">
                            <span class="text-xs font-medium text-gray-600">
                                {{ getInitials(member) }}
                            </span>
                        </div>
                    </div>
                    <div v-if="task.assigned_members.length > 3"
                        class="w-6 h-6 rounded-full border-2 border-white bg-gray-100 flex items-center justify-center"
                        :title="`+${task.assigned_members.length - 3} more members`">
                        <span class="text-xs font-medium text-gray-600">
                            +{{ task.assigned_members.length - 3 }}
                        </span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, inject } from 'vue'

// Props
const props = defineProps({
    task: {
        type: Object,
        required: true
    },
    statuses: {
        type: Array,
        default: () => []
    },
    allowStatusChange: {
        type: [Boolean, Function],
        default: true
    }
})

// Emits
const emit = defineEmits(['edit', 'delete', 'status-change', 'dragstart', 'dragend'])

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

// Reactive data
const showDropdown = ref(false)

// Computed properties
const isOverdue = computed(() => {
    if (!props.task.due_date) return false
    return new Date(props.task.due_date) < new Date()
})

const hasDeadlineExtensions = computed(() => {
    return props.task.deadline_extensions && props.task.deadline_extensions.length > 0
})

// Methods
// Get status color classes based on status name
const getStatusColorClasses = (statusId, type = 'all') => {
    if (!statusId || !props.statuses) {
        return type === 'all' ? defaultColor : defaultColor[type] || ''
    }

    // Find the status object
    const status = props.statuses.find(s => s.id === statusId)
    if (!status) {
        return type === 'all' ? defaultColor : defaultColor[type] || ''
    }

    // Convert status name to lowercase for matching
    const statusName = status.name.toLowerCase().trim()

    // Check if it's a fixed status
    if (statusColorMapping[statusName]) {
        const colors = statusColorMapping[statusName]
        return type === 'all' ? colors : colors[type] || ''
    }

    // Use fallback colors for dynamic statuses
    const statusIndex = props.statuses.findIndex(s => s.id === statusId)
    const colorIndex = statusIndex >= 0 ? statusIndex % fallbackColors.length : 0
    const colors = fallbackColors[colorIndex]

    return type === 'all' ? colors : colors[type] || ''
}

const toggleDropdown = () => {
    showDropdown.value = !showDropdown.value
}

const closeDropdown = () => {
    showDropdown.value = false
}

const editTask = () => {
    emit('edit', props.task)
    closeDropdown()
}

const deleteTask = () => {
    emit('delete', props.task.id)
    closeDropdown()
}

const onStatusChange = (event) => {
    const newStatusId = parseInt(event.target.value)
    if (newStatusId !== props.task.status?.id) {
        emit('status-change', props.task.id, newStatusId)
    }
}

const getPriorityColor = (priority) => {
    const colors = {
        high: 'bg-red-100 text-red-800',
        medium: 'bg-yellow-100 text-yellow-800',
        low: 'bg-green-100 text-green-800'
    }
    return colors[priority] || colors.medium
}

const formatPriority = (priority) => {
    return priority ? priority.charAt(0).toUpperCase() + priority.slice(1) : 'Medium'
}

const formatDate = (dateString) => {
    if (!dateString) return ''
    const date = new Date(dateString)
    const dateOptions = {
        month: 'short',
        day: 'numeric',
        year: date.getFullYear() !== new Date().getFullYear() ? 'numeric' : undefined
    }
    const timeOptions = {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    }

    const dateStr = date.toLocaleDateString('en-US', dateOptions)
    const timeStr = date.toLocaleTimeString('en-US', timeOptions)

    return `${dateStr} at ${timeStr}`
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

// Click outside directive
const vClickOutside = {
    beforeMount(el, binding) {
        el.clickOutsideEvent = function (event) {
            if (!(el === event.target || el.contains(event.target))) {
                binding.value(event)
            }
        }
        document.addEventListener('click', el.clickOutsideEvent)
    },
    unmounted(el) {
        document.removeEventListener('click', el.clickOutsideEvent)
    }
}
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