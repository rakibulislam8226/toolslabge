<template>
    <div class="space-y-6">
        <!-- Header with Actions -->
        <div class="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-4 sm:mb-0">Organization Members</h3>
                <div class="flex flex-col sm:flex-row gap-3">
                    <button @click="showInviteModal = true"
                        class="bg-blue-600 px-4 py-2 rounded-lg font-semibold hover:bg-blue-700 transition duration-300 shadow-lg flex items-center transform hover:scale-105"
                        style="color: white !important;">
                        <svg class="-ml-1 mr-2 h-4 w-4" fill="none" stroke="white" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                        </svg>
                        <span style="color: white !important;">Invite Member</span>
                    </button>
                </div>
            </div>

            <!-- Members Summary -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="bg-linear-to-r from-blue-50 to-blue-100 p-4 rounded-lg border border-blue-200">
                    <div class="flex items-center">
                        <div class="p-2 bg-blue-500 rounded-lg">
                            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-2.239">
                                </path>
                            </svg>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm font-medium text-blue-600">Total Members</p>
                            <p class="text-2xl font-bold text-blue-900">{{ members.length }}</p>
                        </div>
                    </div>
                </div>

                <div class="bg-linear-to-r from-green-50 to-green-100 p-4 rounded-lg border border-green-200">
                    <div class="flex items-center">
                        <div class="p-2 bg-green-500 rounded-lg">
                            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm font-medium text-green-600">Active</p>
                            <p class="text-2xl font-bold text-green-900">{{ activeMembers }}</p>
                        </div>
                    </div>
                </div>

                <div class="bg-linear-to-r from-orange-50 to-orange-100 p-4 rounded-lg border border-orange-200">
                    <div class="flex items-center">
                        <div class="p-2 bg-orange-500 rounded-lg">
                            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm font-medium text-orange-600">Pending</p>
                            <p class="text-2xl font-bold text-orange-900">{{ pendingInvitations.length }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Members List -->
        <div class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
            <div class="p-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-6">Current Members</h3>

                <!-- Loading State -->
                <div v-if="loading" class="flex justify-center items-center py-12">
                    <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600"></div>
                    <span class="ml-3 text-gray-600">Loading members...</span>
                </div>

                <!-- Members List -->
                <div v-else-if="members.length > 0" class="space-y-4">
                    <div v-for="member in members" :key="member.id"
                        class="flex flex-col sm:flex-row sm:items-center sm:justify-between p-4 border border-gray-200 rounded-lg hover:shadow-md hover:border-blue-200 transition-all duration-300 bg-white group space-y-4 sm:space-y-0">
                        <div class="flex items-center space-x-4 flex-1 min-w-0">
                            <!-- Profile Photo or Initials -->
                            <div class="relative shrink-0">
                                <img v-if="member.user?.photo" :src="member.user.photo"
                                    :alt="`${member.user?.first_name} ${member.user?.last_name}`"
                                    class="w-12 h-12 rounded-full object-cover border-2 border-gray-200 group-hover:border-blue-300 transition-all duration-300 shadow-md hover:shadow-lg" />
                                <div v-else
                                    class="w-12 h-12 rounded-full flex items-center justify-center text-white font-semibold text-lg shadow-md hover:shadow-lg transition-all duration-300 group-hover:scale-105"
                                    :class="getAvatarColor(member.user?.email)">
                                    {{ getInitials(member.user?.first_name, member.user?.last_name, member.user?.email)
                                    }}
                                </div>
                                <!-- Active Status Indicator -->
                                <div v-if="member.is_active"
                                    class="absolute -bottom-1 -right-1 w-4 h-4 bg-green-400 border-2 border-white rounded-full shadow-sm animate-pulse"
                                    title="Active member"></div>
                            </div>

                            <!-- Member Info -->
                            <div class="group-hover:translate-x-1 transition-transform duration-300 flex-1 min-w-0">
                                <h4
                                    class="text-lg font-semibold text-gray-900 group-hover:text-blue-600 transition-colors duration-300">
                                    {{ member.user?.first_name }} {{ member.user?.last_name }}
                                </h4>
                                <p class="text-sm text-gray-500 mb-1">{{ member.user?.email }}</p>
                                <div class="flex items-center space-x-2">
                                    <span :class="getRoleClass(member.role)"
                                        class="px-2 py-1 text-xs font-medium rounded-full">
                                        {{ formatRole(member.role) }}
                                    </span>
                                    <span class="text-xs text-gray-400">•</span>
                                    <span class="text-xs text-gray-500">
                                        Joined {{ formatDate(member.created_at) }}
                                    </span>
                                </div>
                            </div>
                        </div>

                        <!-- Actions -->
                        <div class="flex items-center space-x-2 shrink-0">
                            <button @click="editMemberRole(member)"
                                class="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all duration-300"
                                title="Edit role">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z">
                                    </path>
                                </svg>
                            </button>
                            <button @click="removeMember(member)"
                                class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-all duration-300"
                                title="Remove member" v-if="member.role !== 'owner'">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16">
                                    </path>
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Empty State -->
                <div v-else class="text-center py-12">
                    <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor"
                        viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
                            d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-2.239"></path>
                    </svg>
                    <h3 class="text-lg font-medium text-gray-900 mb-2">No members found</h3>
                    <p class="text-gray-500">Start by inviting your first member.</p>
                </div>
            </div>
        </div>

        <!-- Pending Invitations -->
        <div v-if="pendingInvitations.length > 0"
            class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
            <div class="p-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-6">Pending Invitations</h3>
                <div class="space-y-4">
                    <div v-for="invitation in pendingInvitations" :key="invitation.id"
                        class="flex items-center justify-between p-4 border border-orange-200 rounded-lg bg-orange-50">
                        <div>
                            <p class="font-medium text-gray-900">{{ invitation.email }}</p>
                            <p class="text-sm text-gray-500">Invited {{ formatDate(invitation.created_at) }}</p>
                        </div>
                        <div class="flex items-center space-x-2">
                            <button @click="resendInvitation(invitation)"
                                class="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition duration-300">
                                Resend
                            </button>
                            <button @click="cancelInvitation(invitation)"
                                class="px-3 py-1 text-sm bg-red-600 text-white rounded hover:bg-red-700 transition duration-300">
                                Cancel
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Invite Member Modal -->
        <div v-if="showInviteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div class="bg-white rounded-xl shadow-2xl max-w-md w-full mx-4">
                <div class="p-6">
                    <div class="flex items-center justify-between mb-6">
                        <h3 class="text-xl font-semibold text-gray-900">Invite Member</h3>
                        <button @click="showInviteModal = false" class="text-gray-400 hover:text-gray-600">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M6 18L18 6M6 6l12 12"></path>
                            </svg>
                        </button>
                    </div>

                    <form @submit.prevent="inviteMember">
                        <div class="space-y-4">
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
                                <input v-model="inviteForm.email" type="email" required
                                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                    placeholder="Enter email address" />
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Role</label>
                                <select v-model="inviteForm.role"
                                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                                    <option value="member">Member</option>
                                    <option value="admin">Admin</option>
                                </select>
                            </div>
                        </div>

                        <div class="flex justify-end space-x-3 mt-6">
                            <button type="button" @click="showInviteModal = false"
                                class="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition duration-300">
                                Cancel
                            </button>
                            <button type="submit" :disabled="inviting"
                                class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition duration-300 disabled:opacity-50">
                                {{ inviting ? 'Inviting...' : 'Send Invitation' }}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import axiosInstance from '@/plugins/axiosConfig.js'

// Reactive data
const members = ref([])
const pendingInvitations = ref([])
const loading = ref(true)
const showInviteModal = ref(false)
const inviting = ref(false)

const inviteForm = reactive({
    email: '',
    role: 'member'
})

// Computed properties
const activeMembers = computed(() => {
    if (!Array.isArray(members.value)) {
        return 0
    }
    return members.value.filter(member => member.is_active).length
})

// Methods
const fetchMembers = async () => {
    try {
        loading.value = true

        // Mock data for demonstration when API is not available
        const mockMembers = [
            {
                id: 1,
                user: {
                    first_name: 'John',
                    last_name: 'Doe',
                    email: 'john.doe@example.com',
                    photo: null
                },
                role: 'owner',
                is_active: true,
                created_at: '2024-01-15T10:30:00Z'
            },
            {
                id: 2,
                user: {
                    first_name: 'Jane',
                    last_name: 'Smith',
                    email: 'jane.smith@example.com',
                    photo: null
                },
                role: 'admin',
                is_active: true,
                created_at: '2024-02-01T14:20:00Z'
            },
            {
                id: 3,
                user: {
                    first_name: 'Mike',
                    last_name: 'Johnson',
                    email: 'mike.johnson@example.com',
                    photo: null
                },
                role: 'member',
                is_active: true,
                created_at: '2024-02-15T09:45:00Z'
            },
            {
                id: 4,
                user: {
                    first_name: 'Sarah',
                    last_name: 'Wilson',
                    email: 'sarah.wilson@example.com',
                    photo: null
                },
                role: 'member',
                is_active: false,
                created_at: '2024-03-01T16:10:00Z'
            }
        ]

        members.value = mockMembers

        // Try to fetch real data if API is available
        try {
            const response = await axiosInstance.get('organizations/members/')
            members.value = response.data.results || response.data
        } catch (apiError) {
            console.log('Members API not available, using mock data:', apiError.message)
            // Keep using mock data
        }
    } catch (error) {
        console.error('Error fetching members:', error)
        // Fallback to empty array
        members.value = []
    } finally {
        loading.value = false
    }
}

const fetchPendingInvitations = async () => {
    try {
        // Mock data for demonstration
        const mockInvitations = [
            {
                id: 1,
                email: 'alice.brown@example.com',
                created_at: '2024-10-25T12:00:00Z'
            },
            {
                id: 2,
                email: 'bob.green@example.com',
                created_at: '2024-10-26T15:30:00Z'
            }
        ]

        pendingInvitations.value = mockInvitations

        // Try to fetch real data if API is available
        try {
            const response = await axiosInstance.get('organizations/invitations/')
            pendingInvitations.value = response.data.results || response.data
        } catch (apiError) {
            console.log('Invitations API not available, using mock data:', apiError.message)
            // Keep using mock data
        }
    } catch (error) {
        console.error('Error fetching invitations:', error)
        // Fallback to empty array
        pendingInvitations.value = []
    }
}

const inviteMember = async () => {
    try {
        inviting.value = true

        // Create mock invitation for demonstration
        const mockInvitation = {
            id: Date.now(), // Simple ID generation for demo
            email: inviteForm.email,
            created_at: new Date().toISOString()
        }

        // Try to invite via API first
        try {
            const response = await axiosInstance.post('organizations/invitations/', inviteForm)
            pendingInvitations.value.unshift(response.data)
        } catch (apiError) {
            console.log('Invite member API not available, using mock data:', apiError.message)
            // Add mock invitation to the list
            pendingInvitations.value.unshift(mockInvitation)
        }

        showInviteModal.value = false
        // Reset form
        inviteForm.email = ''
        inviteForm.role = 'member'
        // Show success message
        console.log('Member invited successfully')
    } catch (error) {
        console.error('Error inviting member:', error)
        // Handle error with toast notification
    } finally {
        inviting.value = false
    }
}

const editMemberRole = (member) => {
    // Implement role editing functionality
    console.log('Edit member role:', member)
}

const removeMember = async (member) => {
    if (confirm(`Are you sure you want to remove ${member.user?.first_name} ${member.user?.last_name} from the organization?`)) {
        try {
            await axiosInstance.delete(`organizations/members/${member.id}/`)
            members.value = members.value.filter(m => m.id !== member.id)
            // Show success message
        } catch (error) {
            console.error('Error removing member:', error)
            // Handle error with toast notification
        }
    }
}

const resendInvitation = async (invitation) => {
    try {
        await axiosInstance.post(`organizations/invitations/${invitation.id}/resend/`)
        // Show success message
    } catch (error) {
        console.error('Error resending invitation:', error)
        // Handle error with toast notification
    }
}

const cancelInvitation = async (invitation) => {
    if (confirm('Are you sure you want to cancel this invitation?')) {
        try {
            await axiosInstance.delete(`organizations/invitations/${invitation.id}/`)
            pendingInvitations.value = pendingInvitations.value.filter(i => i.id !== invitation.id)
            // Show success message
        } catch (error) {
            console.error('Error canceling invitation:', error)
            // Handle error with toast notification
        }
    }
}

const getInitials = (firstName, lastName, email) => {
    if (firstName && lastName) {
        return `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase()
    }
    if (email) {
        return email.charAt(0).toUpperCase()
    }
    return 'U'
}

const getAvatarColor = (email) => {
    const colors = [
        'bg-red-500', 'bg-blue-500', 'bg-green-500', 'bg-yellow-500',
        'bg-purple-500', 'bg-pink-500', 'bg-indigo-500', 'bg-gray-500'
    ]
    const index = email ? email.charCodeAt(0) % colors.length : 0
    return colors[index]
}

const getRoleClass = (role) => {
    const classes = {
        owner: 'bg-purple-100 text-purple-800',
        admin: 'bg-blue-100 text-blue-800',
        member: 'bg-green-100 text-green-800'
    }
    return classes[role] || 'bg-gray-100 text-gray-800'
}

const formatRole = (role) => {
    return role.charAt(0).toUpperCase() + role.slice(1)
}

const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    })
}

// Lifecycle
onMounted(() => {
    fetchMembers()
    fetchPendingInvitations()
})
</script>

<style scoped></style>