<template>
    <div class="min-h-screen bg-gray-50">
        <!-- Header -->
        <div class="bg-white shadow-sm border-b border-gray-200">
            <div class="max-w-7xl mx-auto py-4 px-4 sm:py-6 sm:px-6 lg:px-8">
                <div class="flex flex-col space-y-4 sm:flex-row sm:items-center sm:justify-between sm:space-y-0">
                    <div class="flex-1 min-w-0">
                        <h2 class="text-xl font-bold leading-7 text-gray-900 sm:text-2xl lg:text-3xl sm:truncate">
                            Organization Members
                        </h2>
                        <p class="mt-1 text-sm text-gray-500 sm:text-base">
                            Manage your organization's members and invite new ones.
                        </p>
                    </div>
                    <div v-if="hasRole('owner', 'admin')" class="flex-shrink-0">
                        <button @click="openInviteModal = true"
                            class="bg-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition duration-300 shadow-lg flex items-center transform hover:scale-105"
                            style="color: white !important;">
                            <svg class="-ml-1 mr-2 h-5 w-5 transition-transform duration-200" fill="none" stroke="white"
                                viewBox="0 0 24 24" style="color: white !important;">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                            </svg>
                            <span class="hidden sm:inline" style="color: white !important;">Invite Member</span>
                            <span class="sm:hidden" style="color: white !important;">Invite</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Main Content -->
        <div class="max-w-7xl mx-auto py-4 px-4 sm:py-6 sm:px-6 lg:px-8">
            <!-- Organization Members List -->
            <div
                class="bg-white shadow-lg overflow-hidden rounded-lg sm:rounded-xl border border-gray-200 hover:shadow-xl transition-shadow duration-300">
                <div class="px-4 py-6 sm:px-6 lg:px-8">
                    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
                        <h3 class="text-lg leading-6 font-semibold text-gray-900 mb-4 sm:mb-0">Current Members</h3>
                        <!-- Members Summary -->
                        <div class="p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-100">
                            <div
                                class="flex flex-col space-y-2 sm:flex-row sm:items-center sm:space-y-0 sm:space-x-6 text-sm">
                                <span class="text-blue-700 font-medium">Total: {{ members.length }} members</span>
                            </div>
                        </div>
                    </div>

                    <!-- Loading state -->
                    <div v-if="loading" class="text-center py-12">
                        <div
                            class="inline-block animate-spin rounded-full h-10 w-10 border-4 border-blue-200 border-t-blue-600 shadow-sm">
                        </div>
                        <p class="mt-4 text-sm text-gray-500 font-medium">Loading organization members...</p>
                    </div>

                    <!-- Members list -->
                    <div v-else-if="members.length > 0" class="space-y-4">
                        <div v-for="member in members" :key=" member.id "
                            class="flex flex-col sm:flex-row sm:items-center sm:justify-between p-4 sm:p-6 border border-gray-200 rounded-lg sm:rounded-xl hover:shadow-lg hover:border-blue-200 transition-all duration-300 ease-in-out transform hover:-translate-y-1 bg-white group space-y-4 sm:space-y-0">
                            <div class="flex items-center space-x-4 flex-1 min-w-0">
                                <!-- Profile Photo or Initials -->
                                <div class="relative flex-shrink-0">
                                    <img v-if="member.user.photo" :src=" member.user.photo "
                                        :alt=" `${ member.user.first_name } ${ member.user.last_name }` "
                                        class="w-12 h-12 sm:w-14 sm:h-14 rounded-full object-cover border-2 border-gray-200 group-hover:border-blue-300 transition-all duration-300 shadow-md hover:shadow-lg" />
                                    <div v-else
                                        class="w-12 h-12 sm:w-14 sm:h-14 rounded-full flex items-center justify-center text-white font-semibold text-sm sm:text-lg shadow-md hover:shadow-lg transition-all duration-300 group-hover:scale-105"
                                        :class=" getAvatarColor(member.user.email) ">
                                        {{ getInitials(member.user.first_name, member.user.last_name, member.user.email)
                                        }}
                                    </div>
                                    <!-- Active Status Indicator -->
                                    <div v-if="member.is_active"
                                        class="absolute -bottom-1 -right-1 w-4 h-4 sm:w-5 sm:h-5 bg-green-400 border-2 sm:border-3 border-white rounded-full shadow-sm animate-pulse"
                                        title="Active member"></div>
                                </div>

                                <!-- Member Info -->
                                <div class="group-hover:translate-x-1 transition-transform duration-300 flex-1 min-w-0">
                                    <h4
                                        class="text-base sm:text-lg font-semibold text-gray-900 group-hover:text-blue-600 transition-colors duration-300 truncate">
                                        {{ getDisplayName(member.user) }}
                                    </h4>
                                    <p
                                        class="text-sm text-gray-600 group-hover:text-gray-700 transition-colors duration-300 truncate">
                                        {{ member.user.email }}</p>
                                    <p
                                        class="text-xs text-gray-500 mt-1 group-hover:text-gray-600 transition-colors duration-300 hidden sm:block">
                                        Member since {{ formatDate(member.joined_at) }}
                                    </p>
                                </div>
                            </div>

                            <!-- Role and Actions -->
                            <div
                                class="flex items-center justify-between sm:justify-end space-x-3 sm:space-x-4 flex-shrink-0">
                                <span
                                    class="inline-flex items-center px-3 py-1 sm:px-4 sm:py-2 rounded-full text-xs sm:text-sm font-semibold shadow-sm border transition-all duration-300 hover:shadow-md"
                                    :class=" getRoleBadgeClass(member.role) ">
                                    {{ getRoleDisplay(member.role) }}
                                </span>

                                <!-- Actions Menu (optional) -->
                                <div class="relative">
                                    <button
                                        class="p-2 sm:p-3 text-gray-400 hover:text-gray-600 rounded-full hover:bg-gray-100 transition-all duration-300 transform hover:scale-110 active:scale-95 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                                        title="Member options">
                                        <svg class="w-4 h-4 sm:w-5 sm:h-5 transition-transform duration-300 hover:rotate-90"
                                            fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z">
                                            </path>
                                        </svg>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Empty state -->
                    <div v-else class="text-center py-12 sm:py-16">
                        <div
                            class="bg-gradient-to-br from-blue-50 to-indigo-100 rounded-full w-20 h-20 sm:w-24 sm:h-24 mx-auto mb-6 flex items-center justify-center shadow-lg">
                            <svg class="w-10 h-10 sm:w-12 sm:h-12 text-blue-500" fill="none" stroke="currentColor"
                                viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-2.239">
                                </path>
                            </svg>
                        </div>
                        <h3 class="text-lg sm:text-xl font-semibold text-gray-900 mb-2">Organization Management</h3>
                        <p class="text-sm sm:text-base text-gray-600 mb-6 max-w-md mx-auto px-4">Invite organization
                            members to collaborate on
                            your projects and build amazing things together.</p>
                        <button @click="openInviteModal = true"
                            class="w-full sm:w-auto inline-flex items-center justify-center px-6 py-3 border border-transparent text-sm sm:text-base font-medium rounded-lg bg-blue-600 hover:bg-blue-700 active:bg-blue-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transform hover:scale-105 transition-all duration-200 shadow-md hover:shadow-lg"
                            style="color: white !important;">
                            <svg class="-ml-1 mr-2 h-5 w-5" fill="none" stroke="white" viewBox="0 0 24 24"
                                style="color: white !important;">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                            </svg>
                            <span style="color: white !important;">Invite Your First Member</span>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Pagination -->
            <div v-if="meta.num_pages > 1" class="mt-6 sm:mt-8">
                <div
                    class="bg-white rounded-lg sm:rounded-xl shadow-sm border border-gray-200 px-4 py-4 sm:px-6 sm:py-6">
                    <Pagination v-model=" currentPage " :totalPages=" meta.num_pages " />
                </div>
            </div>

            <!-- Pending Invitations -->
            <div v-if="false"
                class="mt-6 sm:mt-8 bg-white shadow-lg overflow-hidden rounded-lg sm:rounded-xl border border-gray-200">
                <div class="px-4 py-6 sm:px-6 lg:px-8">
                    <h3 class="text-lg leading-6 font-semibold text-gray-900 mb-6">Pending Invitations</h3>
                    <div class="space-y-4">
                        <div v-for="invitation in pendingInvitations" :key=" invitation.id "
                            class="flex flex-col sm:flex-row sm:items-center sm:justify-between p-4 sm:p-5 border border-yellow-200 bg-gradient-to-r from-yellow-50 to-amber-50 rounded-lg sm:rounded-xl hover:shadow-md transition-all duration-300 transform hover:-translate-y-1 space-y-3 sm:space-y-0">
                            <div class="flex items-center space-x-4">
                                <div
                                    class="w-10 h-10 sm:w-12 sm:h-12 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-full flex items-center justify-center shadow-md flex-shrink-0">
                                    <svg class="w-5 h-5 sm:w-6 sm:h-6 text-white" fill="none" stroke="currentColor"
                                        viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207">
                                        </path>
                                    </svg>
                                </div>
                                <div class="flex-1 min-w-0">
                                    <h4 class="text-sm font-semibold text-gray-900 truncate">{{ invitation.email }}</h4>
                                    <p class="text-sm text-yellow-700 font-medium">Invitation pending</p>
                                </div>
                            </div>
                            <div class="flex flex-col sm:flex-row sm:items-center space-y-2 sm:space-y-0 sm:space-x-4">
                                <span
                                    class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold border shadow-sm"
                                    :class=" getRoleBadgeClass(invitation.role) ">
                                    {{ getRoleDisplay(invitation.role) }}
                                </span>
                                <span class="text-xs sm:text-sm text-gray-600 font-medium">
                                    Sent {{ formatDate(invitation.created_at) }}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        </div>


        <!-- Invite Modal -->
        <InviteModal v-if="openInviteModal" @close="openInviteModal = false" @invited=" handleInviteSent " />
    </div>

</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useAuth } from '@/composables/useAuth.js'
import axios from '@/plugins/axiosConfig.js'
import InviteModal from '@/components/modals/InviteModal.vue'
import Pagination from "@/components/Pagination.vue";
import { usePermissions } from '@/composables/usePermissions.js'

const { hasRole } = useAuth();


const { hasPermission } = usePermissions()
const { fetchUserProfile } = useAuth()
const loading = ref(true)
const members = ref([])
const pendingInvitations = ref([])
const openInviteModal = ref(false)
const meta = ref({})
const currentPage = ref(1)

// Watch for page changes
watch(currentPage, (newPage) => {
    fetchMembers(newPage)
})

// Fetch organization members
const fetchMembers = async (page = 1) => {
    try {
        loading.value = true
        const response = await axios.get(`organizations/members/`, {
            params: { page }
        })

        // Handle the API response structure
        if (response.data.status && response.data.data) {
            members.value = response.data.data
            meta.value = response.data.meta || {}
            currentPage.value = response.data.meta?.current_page || page
        } else {
            members.value = []
            meta.value = {}
            console.warn('Unexpected API response structure:', response.data)
        }
    } catch (error) {
        console.error("Error fetching organization members:", error)
        members.value = []
        meta.value = {}
    } finally {
        loading.value = false
    }
}

// Fetch pending invitations  
const fetchPendingInvitations = async () => {
    // For now, we'll just show a simple placeholder since the backend endpoint for listing invitations is not required
    // You can add this functionality later when you create the invitations listing endpoint
}

// Handle successful invitation
const handleInviteSent = (invitation) => {
    pendingInvitations.value.unshift(invitation)
    openInviteModal.value = false
}

// Utility functions
const getDisplayName = (user) => {
    const firstName = user.first_name?.trim() || ''
    const lastName = user.last_name?.trim() || ''

    if (firstName || lastName) {
        return `${firstName} ${lastName}`.trim()
    }

    // Fallback to email username if no name is provided
    return user.email.split('@')[0]
}

const getInitials = (firstName, lastName, email) => {
    const first = firstName?.trim() || ''
    const last = lastName?.trim() || ''

    if (first || last) {
        return `${first.charAt(0)}${last.charAt(0)}`.toUpperCase()
    }

    // Fallback to first two letters of email
    return email.substring(0, 2).toUpperCase()
}

const getAvatarColor = (email) => {
    // Generate consistent color based on email
    const colors = [
        'bg-blue-500', 'bg-green-500', 'bg-purple-500', 'bg-red-500',
        'bg-yellow-500', 'bg-indigo-500', 'bg-pink-500', 'bg-gray-500'
    ]
    const hash = email.split('').reduce((a, b) => {
        a = ((a << 5) - a) + b.charCodeAt(0)
        return a & a
    }, 0)
    return colors[Math.abs(hash) % colors.length]
}

const getRoleDisplay = (role) => {
    const roleMap = {
        'owner': 'Owner',
        'admin': 'Admin',
        'member': 'Member',
        'manager': 'Manager'
    }
    return roleMap[role] || role
}

const getRoleBadgeClass = (role) => {
    const classMap = {
        'owner': 'bg-purple-100 text-purple-800 border-purple-200 hover:bg-purple-200',
        'admin': 'bg-red-100 text-red-800 border-red-200 hover:bg-red-200',
        'manager': 'bg-blue-100 text-blue-800 border-blue-200 hover:bg-blue-200',
        'member': 'bg-green-100 text-green-800 border-green-200 hover:bg-green-200'
    }
    return classMap[role] || 'bg-gray-100 text-gray-800 border-gray-200 hover:bg-gray-200'
}

const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString()
}

onMounted(async () => {
    await fetchUserProfile()
    await fetchMembers()
    await fetchPendingInvitations()
})
</script>