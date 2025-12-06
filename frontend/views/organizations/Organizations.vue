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
              <button v-for="item in menuItems" :key=" item.key " @click="currentView = item.key" :class=" [
                'w-full text-left px-4 py-3 rounded-lg transition-all duration-200 flex items-center space-x-3 cursor-pointer',
                currentView === item.key
                  ? 'bg-blue-50 text-blue-700 border border-blue-200 shadow-sm'
                  : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
              ] ">
                <component :is=" item.icon " class="w-5 h-5" />
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

          <!-- Tasks -->
          <div v-if="currentView === 'tasks'" class="cursor-disabled">
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
import Button from '@/components/Button.vue'

const router = useRouter()

// Reactive data
const currentView = ref('members')
const organizations = ref([])
const loading = ref(true)
const selectedOrganization = ref(null)


// Menu items with icons
const menuItems = computed(() => [
  {
    key: 'members',
    label: 'Members',
    icon: () => h('svg', { class: 'w-5 h-5', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-2.239' })
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
    tasks: 'Organization Tasks',
    members: 'Organization Members',
    analytics: 'Organization Analytics',
    settings: 'Organization Settings'
  }
  return titles[currentView.value] || 'Organizations'
}

const getPageDescription = () => {
  const descriptions = {
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

  } catch (error) {
    console.error('Error fetching organizations:', error)
    // Fallback to empty array
    organizations.value = []
  } finally {
    loading.value = false
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