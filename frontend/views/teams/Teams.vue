<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow">
      <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div class="md:flex md:items-center md:justify-between">
          <div class="flex-1 min-w-0">
            <h2 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
              Team Members
            </h2>
            <p class="mt-1 text-sm text-gray-500">
              Manage your organization's team members and invite new ones.
            </p>
          </div>
          <div class="mt-6 flex space-x-3 md:mt-0 md:ml-4">
            <button
              @click="openInviteModal = true"
              class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <svg class="-ml-1 mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
      <!-- Team Members List -->
      <div class="bg-white shadow overflow-hidden sm:rounded-md">
        <div class="px-4 py-5 sm:p-6">
          <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Current Members</h3>
          
          <!-- Loading state -->
          <div v-if="loading" class="text-center py-8">
            <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <p class="mt-2 text-sm text-gray-500">Loading team members...</p>
          </div>

          <!-- Members list -->
          <div v-else-if="members.length > 0" class="space-y-4">
            <div 
              v-for="member in members" 
              :key="member.id"
              class="flex items-center justify-between p-6 border border-gray-200 rounded-lg hover:shadow-md transition-shadow duration-200"
            >
              <div class="flex items-center space-x-4">
                <!-- Profile Photo or Initials -->
                <div class="relative">
                  <img 
                    v-if="member.user.photo" 
                    :src="member.user.photo" 
                    :alt="`${member.user.first_name} ${member.user.last_name}`"
                    class="w-12 h-12 rounded-full object-cover border-2 border-gray-200"
                  />
                  <div 
                    v-else 
                    class="w-12 h-12 rounded-full flex items-center justify-center text-white font-semibold text-lg"
                    :class="getAvatarColor(member.user.email)"
                  >
                    {{ getInitials(member.user.first_name, member.user.last_name, member.user.email) }}
                  </div>
                  <!-- Active Status Indicator -->
                  <div 
                    v-if="member.is_active" 
                    class="absolute -bottom-0 -right-0 w-4 h-4 bg-green-400 border-2 border-white rounded-full"
                    title="Active member"
                  ></div>
                </div>
                
                <!-- Member Info -->
                <div>
                  <h4 class="text-lg font-semibold text-gray-900">
                    {{ getDisplayName(member.user) }}
                  </h4>
                  <p class="text-sm text-gray-600">{{ member.user.email }}</p>
                  <p class="text-xs text-gray-500 mt-1">
                    Member since {{ formatDate(member.joined_at) }}
                  </p>
                </div>
              </div>
              
              <!-- Role and Actions -->
              <div class="flex items-center space-x-4">
                <div class="text-right">
                  <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium"
                        :class="getRoleBadgeClass(member.role)">
                    {{ getRoleDisplay(member.role) }}
                  </span>
                  <p class="text-xs text-gray-500 mt-1">
                    {{ member.is_active ? 'Active' : 'Inactive' }}
                  </p>
                </div>
                
                <!-- Actions Menu (optional) -->
                <div class="relative">
                  <button 
                    class="p-2 text-gray-400 hover:text-gray-600 rounded-full hover:bg-gray-100 transition-colors duration-200"
                    title="Member options"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"></path>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
            
            <!-- Members Summary -->
            <div class="mt-6 p-4 bg-gray-50 rounded-lg">
              <div class="flex items-center justify-between text-sm text-gray-600">
                <span>Total: {{ members.length }} members</span>
                <span>Active: {{ activeMembers }} members</span>
              </div>
            </div>
          </div>

          <!-- Empty state -->
          <div v-else class="text-center py-8">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-2.239"></path>
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900">Team Management</h3>
            <p class="mt-1 text-sm text-gray-500">Invite team members to collaborate on your projects.</p>
            
            <!-- Debug Info -->
            <div class="mt-4 p-3 bg-gray-100 rounded text-xs">
              <p><strong>Debug:</strong></p>
              <p>Organization ID: {{ organizationId || 'Not found' }}</p>
              <p>User loaded: {{ !!user }}</p>
              <p>User has data: {{ !!user?.data }}</p>
              <p>User.data has organizations: {{ user?.data?.organizations?.length || 0 }}</p>
              <p>User has organizations: {{ user?.organizations?.length || 0 }}</p>
              <p>User.data has org memberships: {{ user?.data?.organization_memberships?.length || 0 }}</p>
              <p>User has org memberships: {{ user?.organization_memberships?.length || 0 }}</p>
              <div class="mt-2 p-2 bg-white rounded text-xs max-h-20 overflow-y-auto">
                <pre>{{ JSON.stringify(user, null, 2) }}</pre>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Pending Invitations -->
      <div v-if="false" class="mt-8 bg-white shadow overflow-hidden sm:rounded-md">
        <div class="px-4 py-5 sm:p-6">
          <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Pending Invitations</h3>
          <div class="space-y-4">
            <div 
              v-for="invitation in pendingInvitations" 
              :key="invitation.id"
              class="flex items-center justify-between p-4 border border-yellow-200 bg-yellow-50 rounded-lg"
            >
              <div class="flex items-center space-x-4">
                <div class="w-10 h-10 bg-yellow-500 rounded-full flex items-center justify-center">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"></path>
                  </svg>
                </div>
                <div>
                  <h4 class="text-sm font-medium text-gray-900">{{ invitation.email }}</h4>
                  <p class="text-sm text-gray-500">Invitation pending</p>
                </div>
              </div>
              <div class="flex items-center space-x-4">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                      :class="getRoleBadgeClass(invitation.role)">
                  {{ getRoleDisplay(invitation.role) }}
                </span>
                <span class="text-sm text-gray-500">
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

const { user, fetchUserProfile } = useAuth()
const loading = ref(true)
const members = ref([])
const pendingInvitations = ref([])
const openInviteModal = ref(false)

// Get current organization ID from user data
const organizationId = computed(() => {
  // Try different possible paths for organization data
  if (user.value?.data?.organizations?.[0]?.organization_id) {
    return user.value.data.organizations[0].organization_id
  }
  if (user.value?.organizations?.[0]?.organization_id) {
    return user.value.organizations[0].organization_id
  }
  if (user.value?.data?.organization_memberships?.[0]?.organization_id) {
    return user.value.data.organization_memberships[0].organization_id
  }
  if (user.value?.organization_memberships?.[0]?.organization_id) {
    return user.value.organization_memberships[0].organization_id
  }
  if (user.value?.data?.organization_id) {
    return user.value.data.organization_id
  }
  
  console.log('Organization ID not found in user data:', user.value)
  return null
})

// Fetch team members
const fetchMembers = async () => {
  try {
    loading.value = true
    const response = await axios.get(`organizations/${organizationId.value}/members/`)
    
    // Handle the API response structure
    if (response.data.status && response.data.data) {
      members.value = response.data.data
    } else {
      members.value = []
      console.warn('Unexpected API response structure:', response.data)
    }
  } catch (error) {
    console.error("Error fetching team members:", error)
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
    'owner': 'bg-purple-100 text-purple-800',
    'admin': 'bg-red-100 text-red-800',
    'manager': 'bg-blue-100 text-blue-800',
    'member': 'bg-green-100 text-green-800'
  }
  return classMap[role] || 'bg-gray-100 text-gray-800'
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

onMounted(async () => {
  // If no organization ID is found, try to fetch user profile first
  if (!organizationId.value) {
    console.log('No organization ID found, fetching user profile...')
    await fetchUserProfile()
  }
  
  if (organizationId.value) {
    await fetchMembers()
    await fetchPendingInvitations()
  } else {
    console.error('Still no organization ID found after fetching user profile')
    loading.value = false
  }
})
</script>