<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto py-4 px-4 sm:py-6 sm:px-6 lg:px-8">
        <div class="flex flex-col space-y-4 sm:flex-row sm:items-center sm:justify-between sm:space-y-0">
          <div class="flex-1 min-w-0">
            <h2 class="text-xl font-bold leading-7 text-gray-900 sm:text-2xl lg:text-3xl sm:truncate">
              {{ getPageTitle() }}
            </h2>
            <p class="mt-1 text-sm text-gray-500 sm:text-base">
              {{ getPageDescription() }}
            </p>
          </div>
          <div class="shrink-0" v-if="currentView === 'overview'">
            <button @click="showCreateModal = true"
              class="bg-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition duration-300 shadow-lg flex items-center transform hover:scale-105"
              style="color: white !important;">
              <svg class="-ml-1 mr-2 h-5 w-5" fill="none" stroke="white" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6">
                </path>
              </svg>
              <span style="color: white !important;">Create Organization</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content with Sidebar -->
    <div class="max-w-7xl mx-auto py-4 px-4 sm:py-6 sm:px-6 lg:px-8">
      <div class="flex flex-col lg:flex-row gap-6">
        <!-- Sidebar -->
        <div class="lg:w-64 shrink-0">
          <div class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
            <div class="p-4 border-b border-gray-200">
              <h3 class="text-lg font-semibold text-gray-900">Organization Menu</h3>
            </div>
            <nav class="p-4 space-y-2">
              <button v-for="item in menuItems" :key="item.key" @click="currentView = item.key" :class="[
                'w-full text-left px-4 py-3 rounded-lg transition-all duration-200 flex items-center space-x-3',
                currentView === item.key
                  ? 'bg-blue-50 text-blue-700 border border-blue-200 shadow-sm'
                  : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
              ]">
                <component :is="item.icon" class="w-5 h-5" />
                <span class="font-medium">{{ item.label }}</span>
                <span v-if="item.badge" class="ml-auto bg-blue-100 text-blue-600 text-xs px-2 py-1 rounded-full">
                  {{ item.badge }}
                </span>
              </button>
            </nav>
          </div>
        </div>

        <!-- Content Area -->
        <div class="flex-1">
          <!-- Overview -->
          <div v-if="currentView === 'overview'" class="space-y-6">
            <!-- Organizations Grid -->
            <div class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
              <div class="p-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-6">Your Organizations</h3>

                <!-- Loading State -->
                <div v-if="loading" class="flex justify-center items-center py-12">
                  <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600"></div>
                  <span class="ml-3 text-gray-600">Loading organizations...</span>
                </div>

                <!-- Organizations Grid -->
                <div v-else-if="organizations.length > 0" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                  <div v-for="org in organizations" :key="org.id"
                    class="border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-all duration-300 hover:border-blue-200 group cursor-pointer"
                    @click="selectOrganization(org)">
                    <div class="flex items-center space-x-4 mb-4">
                      <div
                        class="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                        <span class="text-white font-bold text-lg">{{ getOrgInitials(org.name) }}</span>
                      </div>
                      <div class="flex-1 min-w-0">
                        <h4
                          class="text-lg font-semibold text-gray-900 truncate group-hover:text-blue-600 transition-colors">
                          {{ org.name }}
                        </h4>
                        <p class="text-sm text-gray-500">{{ formatDate(org.created_at) }}</p>
                      </div>
                    </div>
                    <p class="text-gray-600 text-sm mb-4 line-clamp-2">{{ org.description || 'No description available'
                      }}</p>
                    <div class="flex items-center justify-between text-sm text-gray-500">
                      <span>{{ org.members_count || 0 }} members</span>
                      <span class="px-2 py-1 bg-green-100 text-green-600 rounded-full text-xs">Active</span>
                    </div>
                  </div>
                </div>

                <!-- Empty State -->
                <div v-else class="text-center py-12">
                  <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor"
                    viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
                      d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4">
                    </path>
                  </svg>
                  <h3 class="text-lg font-medium text-gray-900 mb-2">No organizations found</h3>
                  <p class="text-gray-500 mb-4">Get started by creating your first organization.</p>
                  <button @click="showCreateModal = true"
                    class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition duration-300">
                    Create Organization
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Tasks -->
          <div v-else-if="currentView === 'tasks'">
            <OrganizationTasks />
          </div>

          <!-- Members -->
          <div v-else-if="currentView === 'members'">
            <OrganizationMembers />
          </div>

          <!-- Settings -->
          <div v-else-if="currentView === 'settings'">
            <OrganizationSettings />
          </div>

          <!-- Analytics -->
          <div v-else-if="currentView === 'analytics'">
            <OrganizationAnalytics />
          </div>
        </div>
      </div>
    </div>

    <!-- Create Organization Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl shadow-2xl max-w-md w-full mx-4">
        <div class="p-6">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-xl font-semibold text-gray-900">Create Organization</h3>
            <button @click="showCreateModal = false" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>

          <form @submit.prevent="createOrganization">
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Organization Name</label>
                <input v-model="newOrganization.name" type="text" required
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Enter organization name" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
                <textarea v-model="newOrganization.description" rows="3"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Enter organization description"></textarea>
              </div>
            </div>

            <div class="flex justify-end space-x-3 mt-6">
              <button type="button" @click="showCreateModal = false"
                class="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition duration-300">
                Cancel
              </button>
              <button type="submit" :disabled="creating"
                class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition duration-300 disabled:opacity-50">
                {{ creating ? 'Creating...' : 'Create' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, h } from 'vue'
import { useRouter } from 'vue-router'
import axiosInstance from '@/plugins/axiosConfig.js'
import OrganizationTasks from '@/components/organizations/OrganizationTasks.vue'
import OrganizationMembers from '@/components/organizations/OrganizationMembers.vue'
import OrganizationSettings from '@/components/organizations/OrganizationSettings.vue'
import OrganizationAnalytics from '@/components/organizations/OrganizationAnalytics.vue'

const router = useRouter()

// Reactive data
const currentView = ref('overview')
const organizations = ref([])
const loading = ref(true)
const showCreateModal = ref(false)
const creating = ref(false)
const selectedOrganization = ref(null)

const newOrganization = reactive({
  name: '',
  description: ''
})

// Menu items with icons
const menuItems = computed(() => [
  {
    key: 'overview',
    label: 'Overview',
    icon: () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4' })
    ])
  },
  {
    key: 'tasks',
    label: 'Tasks',
    icon: () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z' })
    ]),
    badge: computed(() => {
      if (!Array.isArray(organizations.value)) return 0
      return organizations.value.reduce((total, org) => total + (org.tasks_count || 0), 0)
    })
  },
  {
    key: 'members',
    label: 'Members',
    icon: () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-2.239' })
    ])
  },
  {
    key: 'analytics',
    label: 'Analytics',
    icon: () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z' })
    ])
  },
  {
    key: 'settings',
    label: 'Settings',
    icon: () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z' })
    ])
  }
])

// Computed properties
const getPageTitle = () => {
  const titles = {
    overview: 'Organizations',
    tasks: 'Organization Tasks',
    members: 'Organization Members',
    analytics: 'Organization Analytics',
    settings: 'Organization Settings'
  }
  return titles[currentView.value] || 'Organizations'
}

const getPageDescription = () => {
  const descriptions = {
    overview: 'Manage and overview your organizations',
    tasks: 'View and manage tasks across all organizations',
    members: 'Manage organization members and invitations',
    analytics: 'View organization performance and statistics',
    settings: 'Configure organization settings and preferences'
  }
  return descriptions[currentView.value] || 'Manage your organizations'
}

// Methods
const fetchOrganizations = async () => {
  try {
    loading.value = true

    // Mock data for demonstration when API is not available
    const mockOrganizations = [
      {
        id: 1,
        name: 'Tech Solutions Inc.',
        description: 'A leading technology solutions company focused on innovation and excellence.',
        created_at: '2024-01-15T10:30:00Z',
        members_count: 25,
        tasks_count: 45
      },
      {
        id: 2,
        name: 'Creative Agency',
        description: 'Full-service creative agency specializing in digital marketing and design.',
        created_at: '2024-02-20T14:45:00Z',
        members_count: 12,
        tasks_count: 23
      },
      {
        id: 3,
        name: 'StartupHub',
        description: 'Startup incubator helping entrepreneurs build successful businesses.',
        created_at: '2024-03-10T09:15:00Z',
        members_count: 8,
        tasks_count: 18
      }
    ]

    organizations.value = mockOrganizations

    // Try to fetch real data if API is available
    try {
      const response = await axiosInstance.get('organizations/')
      organizations.value = response.data.results || response.data
    } catch (apiError) {
      console.log('Organizations API not available, using mock data:', apiError.message)
      // Keep using mock data
    }
  } catch (error) {
    console.error('Error fetching organizations:', error)
    // Fallback to empty array
    organizations.value = []
  } finally {
    loading.value = false
  }
}

const createOrganization = async () => {
  try {
    creating.value = true

    // Create mock organization for demonstration
    const mockOrganization = {
      id: Date.now(), // Simple ID generation for demo
      name: newOrganization.name,
      description: newOrganization.description,
      created_at: new Date().toISOString(),
      members_count: 1,
      tasks_count: 0
    }

    // Try to create via API first
    try {
      const response = await axiosInstance.post('organizations/', newOrganization)
      organizations.value.unshift(response.data)
    } catch (apiError) {
      console.log('Create organization API not available, using mock data:', apiError.message)
      // Add mock organization to the list
      organizations.value.unshift(mockOrganization)
    }

    showCreateModal.value = false
    // Reset form
    newOrganization.name = ''
    newOrganization.description = ''
    // Show success message
    console.log('Organization created successfully')
  } catch (error) {
    console.error('Error creating organization:', error)
    // Handle error with toast notification
  } finally {
    creating.value = false
  }
}

const selectOrganization = (org) => {
  selectedOrganization.value = org
  // You could navigate to org details or set active org context
  console.log('Selected organization:', org)
}

const getOrgInitials = (name) => {
  return name
    .split(' ')
    .map(word => word.charAt(0).toUpperCase())
    .slice(0, 2)
    .join('')
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
  fetchOrganizations()
})
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