<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow">
      <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div class="md:flex md:items-center md:justify-between">
          <div class="flex-1 min-w-0">
            <h2 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
              Organization Members
            </h2>
            <p class="mt-1 text-sm text-gray-500">
              Manage your organization's members and invite new ones.
            </p>
          </div>
          <div class="mt-6 flex space-x-3 md:mt-0 md:ml-4">
            <button
              @click="openInviteModal = true"
              class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 active:bg-blue-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transform hover:scale-105 transition-all duration-200 ease-in-out"
            >
              <svg class="-ml-1 mr-2 h-5 w-5 transition-transform duration-200 group-hover:rotate-90" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
              </svg>
              Invite Member
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Organization Members List -->
      <div class="bg-white shadow-lg overflow-hidden sm:rounded-xl border border-gray-200 hover:shadow-xl transition-shadow duration-300">
        <div class="px-6 py-6 sm:p-8">
          <h3 class="text-lg leading-6 font-semibold text-gray-900 mb-6">Current Members</h3>
           <!-- Members Summary -->
            <div class="mt-6 p-5 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl border border-blue-100">
              <div class="flex items-center justify-between text-sm">
                <span class="text-blue-700 font-medium">Total: {{ members.length }} members</span>
                <span class="text-green-700 font-medium">Active: {{ activeMembers }} members</span>
              </div>
            </div>
          
          <!-- Loading state -->
          <div v-if="loading" class="text-center py-12">
            <div class="inline-block animate-spin rounded-full h-10 w-10 border-4 border-blue-200 border-t-blue-600 shadow-sm"></div>
            <p class="mt-4 text-sm text-gray-500 font-medium">Loading organization members...</p>
          </div>

          <!-- Members list -->
          <div v-else-if="members.length > 0" class="space-y-4 mt-6">
            <div 
              v-for="member in members" 
              :key="member.id"
              class="flex items-center justify-between p-6 border border-gray-200 rounded-xl hover:shadow-lg hover:border-blue-200 transition-all duration-300 ease-in-out transform hover:-translate-y-1 bg-white cursor-pointer group"
            >
              <div class="flex items-center space-x-4">
                <!-- Profile Photo or Initials -->
                <div class="relative group">
                  <img 
                    v-if="member.user.photo" 
                    :src="member.user.photo" 
                    :alt="`${member.user.first_name} ${member.user.last_name}`"
                    class="w-14 h-14 rounded-full object-cover border-3 border-gray-200 group-hover:border-blue-300 transition-all duration-300 shadow-md hover:shadow-lg"
                  />
                  <div 
                    v-else 
                    class="w-14 h-14 rounded-full flex items-center justify-center text-white font-semibold text-lg shadow-md hover:shadow-lg transition-all duration-300 group-hover:scale-110"
                    :class="getAvatarColor(member.user.email)"
                  >
                    {{ getInitials(member.user.first_name, member.user.last_name, member.user.email) }}
                  </div>
                  <!-- Active Status Indicator -->
                  <div 
                    v-if="member.is_active" 
                    class="absolute -bottom-1 -right-1 w-5 h-5 bg-green-400 border-3 border-white rounded-full shadow-sm animate-pulse"
                    title="Active member"
                  ></div>
                </div>
                
                <!-- Member Info -->
                <div class="group-hover:translate-x-1 transition-transform duration-300">
                  <h4 class="text-lg font-semibold text-gray-900 group-hover:text-blue-600 transition-colors duration-300">
                    {{ getDisplayName(member.user) }}
                  </h4>
                  <p class="text-sm text-gray-600 group-hover:text-gray-700 transition-colors duration-300">{{ member.user.email }}</p>
                  <p class="text-xs text-gray-500 mt-1 group-hover:text-gray-600 transition-colors duration-300">
                    Member since {{ formatDate(member.joined_at) }}
                  </p>
                </div>
              </div>
              
              <!-- Role and Actions -->
              <div class="flex items-center space-x-4">
                <div class="flex flex-col items-end justify-between space-y-2">
                  <span class="inline-flex items-center px-4 py-2 rounded-full text-sm font-semibold shadow-sm border transition-all duration-300 hover:shadow-md"
                        :class="getRoleBadgeClass(member.role)">
                    {{ getRoleDisplay(member.role) }}
                  </span>
                </div>
                
                <!-- Actions Menu (optional) -->
                <div class="relative">
                  <button 
                    class="p-3 text-gray-400 hover:text-gray-600 rounded-full hover:bg-gray-100 transition-all duration-300 transform hover:scale-110 active:scale-95 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                    title="Member options"
                  >
                    <svg class="w-5 h-5 transition-transform duration-300 hover:rotate-90" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"></path>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
            
            
          </div>

          <!-- Empty state -->
          <div v-else class="text-center py-16">
            <div class="bg-gradient-to-br from-blue-50 to-indigo-100 rounded-full w-24 h-24 mx-auto mb-6 flex items-center justify-center shadow-lg">
              <svg class="w-12 h-12 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-2.239"></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-2">Organization Management</h3>
            <p class="text-gray-600 mb-6 max-w-md mx-auto">Invite organization members to collaborate on your projects and build amazing things together.</p>
            <button
              @click="openInviteModal = true"
              class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 active:bg-blue-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transform hover:scale-105 transition-all duration-200 shadow-md hover:shadow-lg"
            >
              <svg class="-ml-1 mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
              </svg>
              Invite Your First Member
            </button>
          </div>
        </div>
      </div>

      <!-- Pending Invitations -->
      <div v-if="false" class="mt-8 bg-white shadow-lg overflow-hidden sm:rounded-xl border border-gray-200">
        <div class="px-6 py-6 sm:p-8">
          <h3 class="text-lg leading-6 font-semibold text-gray-900 mb-6">Pending Invitations</h3>
          <div class="space-y-4">
            <div 
              v-for="invitation in pendingInvitations" 
              :key="invitation.id"
              class="flex items-center justify-between p-5 border border-yellow-200 bg-gradient-to-r from-yellow-50 to-amber-50 rounded-xl hover:shadow-md transition-all duration-300 transform hover:-translate-y-1"
            >
              <div class="flex items-center space-x-4">
                <div class="w-12 h-12 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-full flex items-center justify-center shadow-md">
                  <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"></path>
                  </svg>
                </div>
                <div>
                  <h4 class="text-sm font-semibold text-gray-900">{{ invitation.email }}</h4>
                  <p class="text-sm text-yellow-700 font-medium">Invitation pending</p>
                </div>
              </div>
              <div class="flex items-center space-x-4">
                <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold border shadow-sm"
                      :class="getRoleBadgeClass(invitation.role)">
                  {{ getRoleDisplay(invitation.role) }}
                </span>
                <span class="text-sm text-gray-600 font-medium">
                  Sent {{ formatDate(invitation.created_at) }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Invite Modal -->
    <InviteModal 
      v-if="openInviteModal" 
      @close="openInviteModal = false"
      @invited="handleInviteSent"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuth } from '@/composables/useAuth.js'
import axios from '@/plugins/axiosConfig.js'
import InviteModal from '@/components/modals/InviteModal.vue'

const { fetchUserProfile } = useAuth()
const loading = ref(true)
const members = ref([])
const pendingInvitations = ref([])
const openInviteModal = ref(false)

// Fetch organization members
const fetchMembers = async () => {
  try {
    loading.value = true
    const response = await axios.get(`organizations/members/`)
    
    // Handle the API response structure
    if (response.data.status && response.data.data) {
      members.value = response.data.data
    } else {
      members.value = []
      console.warn('Unexpected API response structure:', response.data)
    }
  } catch (error) {
    console.error("Error fetching organization members:", error)
    members.value = []
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

// Computed properties
const activeMembers = computed(() => {
  return members.value.filter(member => member.is_active).length
})

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