<template>
    <div class="space-y-6">
        <!-- Analytics Overview -->
        <div class="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
            <div class="flex items-center justify-between mb-6">
                <h3 class="text-lg font-semibold text-gray-900">Analytics Overview</h3>
                <div class="flex items-center space-x-3">
                    <select v-model="selectedTimeRange" @change="fetchAnalytics"
                        class="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                        <option value="7">Last 7 days</option>
                        <option value="30">Last 30 days</option>
                        <option value="90">Last 3 months</option>
                        <option value="365">Last year</option>
                    </select>
                    <button @click="fetchAnalytics"
                        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition duration-300">
                        Refresh
                    </button>
                </div>
            </div>

            <!-- Key Metrics -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <div class="bg-linear-to-r from-blue-50 to-blue-100 p-6 rounded-lg border border-blue-200">
                    <div class="flex items-center">
                        <div class="p-3 bg-blue-500 rounded-lg">
                            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z">
                                </path>
                            </svg>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm font-medium text-blue-600">Total Projects</p>
                            <p class="text-3xl font-bold text-blue-900">{{ analytics.totalProjects }}</p>
                            <p class="text-sm text-blue-600">
                                <span :class="analytics.projectsChange >= 0 ? 'text-green-600' : 'text-red-600'">
                                    {{ analytics.projectsChange >= 0 ? '+' : '' }}{{ analytics.projectsChange }}%
                                </span>
                                vs last period
                            </p>
                        </div>
                    </div>
                </div>

                <div class="bg-linear-to-r from-green-50 to-green-100 p-6 rounded-lg border border-green-200">
                    <div class="flex items-center">
                        <div class="p-3 bg-green-500 rounded-lg">
                            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm font-medium text-green-600">Completed Tasks</p>
                            <p class="text-3xl font-bold text-green-900">{{ analytics.completedTasks }}</p>
                            <p class="text-sm text-green-600">
                                <span :class="analytics.tasksChange >= 0 ? 'text-green-600' : 'text-red-600'">
                                    {{ analytics.tasksChange >= 0 ? '+' : '' }}{{ analytics.tasksChange }}%
                                </span>
                                vs last period
                            </p>
                        </div>
                    </div>
                </div>

                <div class="bg-linear-to-r from-purple-50 to-purple-100 p-6 rounded-lg border border-purple-200">
                    <div class="flex items-center">
                        <div class="p-3 bg-purple-500 rounded-lg">
                            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-2.239">
                                </path>
                            </svg>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm font-medium text-purple-600">Active Members</p>
                            <p class="text-3xl font-bold text-purple-900">{{ analytics.activeMembers }}</p>
                            <p class="text-sm text-purple-600">
                                <span :class="analytics.membersChange >= 0 ? 'text-green-600' : 'text-red-600'">
                                    {{ analytics.membersChange >= 0 ? '+' : '' }}{{ analytics.membersChange }}%
                                </span>
                                vs last period
                            </p>
                        </div>
                    </div>
                </div>

                <div class="bg-linear-to-r from-orange-50 to-orange-100 p-6 rounded-lg border border-orange-200">
                    <div class="flex items-center">
                        <div class="p-3 bg-orange-500 rounded-lg">
                            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                            </svg>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm font-medium text-orange-600">Productivity Score</p>
                            <p class="text-3xl font-bold text-orange-900">{{ analytics.productivityScore }}%</p>
                            <p class="text-sm text-orange-600">
                                <span :class="analytics.productivityChange >= 0 ? 'text-green-600' : 'text-red-600'">
                                    {{ analytics.productivityChange >= 0 ? '+' : '' }}{{ analytics.productivityChange
                                    }}%
                                </span>
                                vs last period
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Charts Section -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Task Completion Chart -->
            <div class="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
                <h4 class="text-lg font-semibold text-gray-900 mb-6">Task Completion Trends</h4>
                <div class="h-64 flex items-center justify-center bg-gray-50 rounded-lg">
                    <div class="text-center">
                        <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor"
                            viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
                                d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z">
                            </path>
                        </svg>
                        <p class="text-gray-500">Chart visualization would be here</p>
                        <p class="text-sm text-gray-400">Integration with Chart.js or similar library</p>
                    </div>
                </div>
            </div>

            <!-- Project Status Distribution -->
            <div class="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
                <h4 class="text-lg font-semibold text-gray-900 mb-6">Project Status Distribution</h4>
                <div class="space-y-4">
                    <div v-for="status in projectStatusData" :key="status.name"
                        class="flex items-center justify-between">
                        <div class="flex items-center space-x-3">
                            <div :class="status.color" class="w-4 h-4 rounded-full"></div>
                            <span class="text-gray-700">{{ status.name }}</span>
                        </div>
                        <div class="flex items-center space-x-2">
                            <span class="text-gray-900 font-medium">{{ status.count }}</span>
                            <span class="text-gray-500">({{ status.percentage }}%)</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Team Performance -->
        <div class="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
            <h4 class="text-lg font-semibold text-gray-900 mb-6">Team Performance</h4>

            <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                        <tr>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Member</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Tasks Completed</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Projects</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Performance</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Efficiency</th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                        <tr v-for="member in teamPerformance" :key="member.id" class="hover:bg-gray-50">
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="flex items-center">
                                    <div class="shrink-0 h-10 w-10">
                                        <img v-if="member.avatar" :src="member.avatar" :alt="member.name"
                                            class="h-10 w-10 rounded-full" />
                                        <div v-else
                                            class="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center">
                                            <span class="text-gray-600 font-medium">{{ getInitials(member.name)
                                                }}</span>
                                        </div>
                                    </div>
                                    <div class="ml-4">
                                        <div class="text-sm font-medium text-gray-900">{{ member.name }}</div>
                                        <div class="text-sm text-gray-500">{{ member.role }}</div>
                                    </div>
                                </div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ member.tasksCompleted }}
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ member.projectsCount }}
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="flex items-center">
                                    <div class="w-16 bg-gray-200 rounded-full h-2">
                                        <div :class="getPerformanceColor(member.performance)"
                                            class="h-2 rounded-full transition-all duration-300"
                                            :style="{ width: member.performance + '%' }"></div>
                                    </div>
                                    <span class="ml-2 text-sm text-gray-700">{{ member.performance }}%</span>
                                </div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span :class="getEfficiencyClass(member.efficiency)"
                                    class="px-2 py-1 text-xs font-medium rounded-full">
                                    {{ member.efficiency }}
                                </span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Recent Activity -->
        <div class="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
            <h4 class="text-lg font-semibold text-gray-900 mb-6">Recent Activity</h4>

            <div class="space-y-4">
                <div v-for="activity in recentActivity" :key="activity.id"
                    class="flex items-start space-x-3 p-3 rounded-lg hover:bg-gray-50 transition-colors duration-200">
                    <div :class="activity.iconBg" class="p-2 rounded-lg">
                        <component :is="activity.icon" class="w-4 h-4 text-white" />
                    </div>
                    <div class="flex-1 min-w-0">
                        <p class="text-sm text-gray-900">{{ activity.description }}</p>
                        <p class="text-xs text-gray-500">{{ formatRelativeTime(activity.timestamp) }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, h } from 'vue'
import axiosInstance from '@/plugins/axiosConfig.js'

// Reactive data
const analytics = reactive({
    totalProjects: 0,
    completedTasks: 0,
    activeMembers: 0,
    productivityScore: 0,
    projectsChange: 0,
    tasksChange: 0,
    membersChange: 0,
    productivityChange: 0
})

const selectedTimeRange = ref('30')
const projectStatusData = ref([])
const teamPerformance = ref([])
const recentActivity = ref([])

// Methods
const fetchAnalytics = async () => {
    try {
        // Mock data for demonstration
        const mockAnalytics = {
            totalProjects: 12,
            completedTasks: 145,
            activeMembers: 8,
            productivityScore: 87,
            projectsChange: 15,
            tasksChange: 23,
            membersChange: 12,
            productivityChange: 8
        }

        const mockProjectStatus = [
            { name: 'Active', count: 5, percentage: 42, color: 'bg-green-500' },
            { name: 'Planning', count: 3, percentage: 25, color: 'bg-blue-500' },
            { name: 'On Hold', count: 2, percentage: 17, color: 'bg-yellow-500' },
            { name: 'Completed', count: 2, percentage: 17, color: 'bg-gray-500' }
        ]

        const mockTeamPerformance = [
            { id: 1, name: 'John Doe', role: 'Project Manager', tasksCompleted: 23, projectsCount: 3, performance: 95, efficiency: 'Excellent', avatar: null },
            { id: 2, name: 'Jane Smith', role: 'Developer', tasksCompleted: 31, projectsCount: 2, performance: 88, efficiency: 'Good', avatar: null },
            { id: 3, name: 'Mike Johnson', role: 'Designer', tasksCompleted: 18, projectsCount: 2, performance: 76, efficiency: 'Average', avatar: null },
            { id: 4, name: 'Sarah Wilson', role: 'QA Engineer', tasksCompleted: 15, projectsCount: 1, performance: 82, efficiency: 'Good', avatar: null }
        ]

        const mockRecentActivity = [
            {
                id: 1,
                description: 'New project "Website Redesign" was created',
                timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
                icon: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
                    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M12 6v6m0 0v6m0-6h6m-6 0H6' })
                ]),
                iconBg: 'bg-green-500'
            },
            {
                id: 2,
                description: 'Task "Update user interface" was completed by John Doe',
                timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000), // 4 hours ago
                icon: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
                    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z' })
                ]),
                iconBg: 'bg-blue-500'
            },
            {
                id: 3,
                description: 'New member Jane Smith joined the organization',
                timestamp: new Date(Date.now() - 24 * 60 * 60 * 1000), // 1 day ago
                icon: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
                    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z' })
                ]),
                iconBg: 'bg-purple-500'
            }
        ]

        Object.assign(analytics, mockAnalytics)
        projectStatusData.value = mockProjectStatus
        teamPerformance.value = mockTeamPerformance
        recentActivity.value = mockRecentActivity

        // Try to fetch real data
        try {
            const response = await axiosInstance.get(`analytics/?days=${selectedTimeRange.value}`)
            if (response.data) {
                Object.assign(analytics, response.data)
            }
        } catch (error) {
            console.log('Using mock data - API not available:', error)
        }
    } catch (error) {
        console.error('Error fetching analytics:', error)
    }
}

const getInitials = (name) => {
    return name
        .split(' ')
        .map(word => word.charAt(0).toUpperCase())
        .slice(0, 2)
        .join('')
}

const getPerformanceColor = (performance) => {
    if (performance >= 90) return 'bg-green-500'
    if (performance >= 70) return 'bg-blue-500'
    if (performance >= 50) return 'bg-yellow-500'
    return 'bg-red-500'
}

const getEfficiencyClass = (efficiency) => {
    const classes = {
        'Excellent': 'bg-green-100 text-green-800',
        'Good': 'bg-blue-100 text-blue-800',
        'Average': 'bg-yellow-100 text-yellow-800',
        'Poor': 'bg-red-100 text-red-800'
    }
    return classes[efficiency] || 'bg-gray-100 text-gray-800'
}

const formatRelativeTime = (timestamp) => {
    const now = new Date()
    const diff = now - new Date(timestamp)
    const minutes = Math.floor(diff / (1000 * 60))
    const hours = Math.floor(minutes / 60)
    const days = Math.floor(hours / 24)

    if (days > 0) return `${days} day${days > 1 ? 's' : ''} ago`
    if (hours > 0) return `${hours} hour${hours > 1 ? 's' : ''} ago`
    if (minutes > 0) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`
    return 'Just now'
}

// Lifecycle
onMounted(() => {
    fetchAnalytics()
})
</script>

<style scoped></style>