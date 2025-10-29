<template>
    <div class="space-y-6">
        <!-- Organization Information -->
        <div class="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
            <div class="flex items-center justify-between mb-6">
                <h3 class="text-lg font-semibold text-gray-900">Organization Information</h3>
                <button @click="editing = !editing"
                    class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition duration-300">
                    {{ editing ? 'Cancel' : 'Edit' }}
                </button>
            </div>

            <form @submit.prevent="updateOrganization" v-if="editing">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Organization Name</label>
                        <input v-model="organizationForm.name" type="text" required
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                            placeholder="Enter organization name" />
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Website</label>
                        <input v-model="organizationForm.website" type="url"
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                            placeholder="https://example.com" />
                    </div>

                    <div class="md:col-span-2">
                        <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
                        <textarea v-model="organizationForm.description" rows="4"
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                            placeholder="Enter organization description"></textarea>
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Industry</label>
                        <select v-model="organizationForm.industry"
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                            <option value="">Select Industry</option>
                            <option value="technology">Technology</option>
                            <option value="healthcare">Healthcare</option>
                            <option value="finance">Finance</option>
                            <option value="education">Education</option>
                            <option value="retail">Retail</option>
                            <option value="manufacturing">Manufacturing</option>
                            <option value="other">Other</option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Company Size</label>
                        <select v-model="organizationForm.size"
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                            <option value="">Select Size</option>
                            <option value="1-10">1-10 employees</option>
                            <option value="11-50">11-50 employees</option>
                            <option value="51-200">51-200 employees</option>
                            <option value="201-500">201-500 employees</option>
                            <option value="501+">501+ employees</option>
                        </select>
                    </div>
                </div>

                <div class="flex justify-end space-x-3 mt-6">
                    <Button variant="secondary" size="md" label="Cancel" @click="editing = false" />
                    <Button type="submit" variant="primary" size="md" :loading="updating" loadingText="Updating..."
                        label="Update Organization" />
                </div>
            </form>

            <!-- Read-only view -->
            <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Organization Name</label>
                    <p class="text-gray-900">{{ organization?.name || 'Not set' }}</p>
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Website</label>
                    <p class="text-gray-900">
                        <a v-if="organization?.website" :href="organization.website" target="_blank"
                            class="text-blue-600 hover:text-blue-800">
                            {{ organization.website }}
                        </a>
                        <span v-else>Not set</span>
                    </p>
                </div>

                <div class="md:col-span-2">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
                    <p class="text-gray-900">{{ organization?.description || 'No description provided' }}</p>
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Industry</label>
                    <p class="text-gray-900">{{ formatIndustry(organization?.industry) || 'Not set' }}</p>
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Company Size</label>
                    <p class="text-gray-900">{{ organization?.size || 'Not set' }}</p>
                </div>
            </div>
        </div>

        <!-- Organization Preferences -->
        <div class="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-6">Organization Preferences</h3>

            <div class="space-y-6">
                <!-- Privacy Settings -->
                <div>
                    <h4 class="text-md font-medium text-gray-900 mb-4">Privacy Settings</h4>
                    <div class="space-y-4">
                        <div class="flex items-center justify-between">
                            <div>
                                <label class="text-sm font-medium text-gray-700">Public Organization</label>
                                <p class="text-sm text-gray-500">Allow others to find and request to join your
                                    organization</p>
                            </div>
                            <toggle-switch v-model="preferences.isPublic" @change="updatePreferences" />
                        </div>

                        <div class="flex items-center justify-between">
                            <div>
                                <label class="text-sm font-medium text-gray-700">Member Directory</label>
                                <p class="text-sm text-gray-500">Show member list to all organization members</p>
                            </div>
                            <toggle-switch v-model="preferences.showMemberDirectory" @change="updatePreferences" />
                        </div>
                    </div>
                </div>

                <!-- Notification Settings -->
                <div>
                    <h4 class="text-md font-medium text-gray-900 mb-4">Notification Settings</h4>
                    <div class="space-y-4">
                        <div class="flex items-center justify-between">
                            <div>
                                <label class="text-sm font-medium text-gray-700">Email Notifications</label>
                                <p class="text-sm text-gray-500">Send email notifications for important updates</p>
                            </div>
                            <toggle-switch v-model="preferences.emailNotifications" @change="updatePreferences" />
                        </div>

                        <div class="flex items-center justify-between">
                            <div>
                                <label class="text-sm font-medium text-gray-700">Task Notifications</label>
                                <p class="text-sm text-gray-500">Notify when tasks are assigned or completed</p>
                            </div>
                            <toggle-switch v-model="preferences.taskNotifications" @change="updatePreferences" />
                        </div>
                    </div>
                </div>

                <!-- Project Settings -->
                <div>
                    <h4 class="text-md font-medium text-gray-900 mb-4">Project Settings</h4>
                    <div class="space-y-4">
                        <div class="flex items-center justify-between">
                            <div>
                                <label class="text-sm font-medium text-gray-700">Auto-archive Completed Projects</label>
                                <p class="text-sm text-gray-500">Automatically archive projects after completion</p>
                            </div>
                            <toggle-switch v-model="preferences.autoArchiveProjects" @change="updatePreferences" />
                        </div>

                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Default Project
                                Visibility</label>
                            <select v-model="preferences.defaultProjectVisibility" @change="updatePreferences"
                                class="w-full md:w-64 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                                <option value="private">Private</option>
                                <option value="organization">Organization</option>
                                <option value="public">Public</option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Danger Zone -->
        <div class="bg-white rounded-xl shadow-lg border border-red-200 p-6">
            <h3 class="text-lg font-semibold text-red-900 mb-6">Danger Zone</h3>

            <div class="space-y-4">
                <div class="flex items-center justify-between p-4 border border-red-200 rounded-lg bg-red-50">
                    <div>
                        <h4 class="text-md font-medium text-red-900">Archive Organization</h4>
                        <p class="text-sm text-red-600">Archive this organization and hide it from members</p>
                    </div>
                    <button @click="archiveOrganization"
                        class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition duration-300">
                        Archive
                    </button>
                </div>

                <div class="flex items-center justify-between p-4 border border-red-200 rounded-lg bg-red-50">
                    <div>
                        <h4 class="text-md font-medium text-red-900">Delete Organization</h4>
                        <p class="text-sm text-red-600">Permanently delete this organization and all its data</p>
                    </div>
                    <button @click="showDeleteModal = true"
                        class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition duration-300">
                        Delete
                    </button>
                </div>
            </div>
        </div>

        <!-- Delete Confirmation Modal -->
        <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div class="bg-white rounded-xl shadow-2xl max-w-md w-full mx-4">
                <div class="p-6">
                    <div class="flex items-center justify-between mb-6">
                        <h3 class="text-xl font-semibold text-red-900">Delete Organization</h3>
                        <Button variant="ghost" size="sm" @click="showDeleteModal = false">
                            <template #icon>
                                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M6 18L18 6M6 6l12 12"></path>
                                </svg>
                            </template>
                        </Button>
                    </div>

                    <div class="mb-6">
                        <p class="text-gray-700 mb-4">
                            This action cannot be undone. This will permanently delete the organization and all
                            associated data.
                        </p>
                        <p class="text-sm text-gray-600 mb-4">
                            Please type <strong>{{ organization?.name }}</strong> to confirm deletion.
                        </p>
                        <input v-model="deleteConfirmation" type="text"
                            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500"
                            placeholder="Enter organization name" />
                    </div>

                    <div class="flex justify-end space-x-3">
                        <button type="button" @click="showDeleteModal = false"
                            class="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition duration-300">
                            Cancel
                        </button>
                        <button @click="deleteOrganization"
                            :disabled="deleteConfirmation !== organization?.name || deleting"
                            class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition duration-300 disabled:opacity-50">
                            {{ deleting ? 'Deleting...' : 'Delete Organization' }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axiosInstance from '@/plugins/axiosConfig.js'
import ToggleSwitch from '@/components/common/ToggleSwitch.vue'
import Button from '@/components/Button.vue'

const router = useRouter()

// Reactive data
const organization = ref(null)
const editing = ref(false)
const updating = ref(false)
const showDeleteModal = ref(false)
const deleting = ref(false)
const deleteConfirmation = ref('')

const organizationForm = reactive({
    name: '',
    description: '',
    website: '',
    industry: '',
    size: ''
})

const preferences = reactive({
    isPublic: false,
    showMemberDirectory: true,
    emailNotifications: true,
    taskNotifications: true,
    autoArchiveProjects: false,
    defaultProjectVisibility: 'organization'
})

// Methods
const fetchOrganization = async () => {
    try {
        // For now, we'll use a mock organization since the API might not be implemented
        const mockOrganization = {
            id: 1,
            name: 'My Organization',
            description: 'This is a sample organization description.',
            website: 'https://example.com',
            industry: 'technology',
            size: '11-50',
            created_at: '2024-01-01T00:00:00Z'
        }

        organization.value = mockOrganization

        // Populate form with current data
        Object.assign(organizationForm, mockOrganization)

        // Try to fetch real data
        try {
            const response = await axiosInstance.get('organizations/current/')
            organization.value = response.data
            Object.assign(organizationForm, response.data)
        } catch (error) {
            console.log('Using mock data - API not available:', error)
        }
    } catch (error) {
        console.error('Error fetching organization:', error)
    }
}

const updateOrganization = async () => {
    try {
        updating.value = true
        const response = await axiosInstance.patch('organizations/current/', organizationForm)
        organization.value = response.data
        editing.value = false
        // Show success message
    } catch (error) {
        console.error('Error updating organization:', error)
        // Handle error with toast notification
    } finally {
        updating.value = false
    }
}

const updatePreferences = async () => {
    try {
        await axiosInstance.patch('organizations/preferences/', preferences)
        // Show success message
    } catch (error) {
        console.error('Error updating preferences:', error)
        // Handle error with toast notification
    }
}

const archiveOrganization = async () => {
    if (confirm('Are you sure you want to archive this organization?')) {
        try {
            await axiosInstance.patch('organizations/current/', { is_archived: true })
            // Redirect to organizations list
            router.push({ name: 'dashboard.index' })
        } catch (error) {
            console.error('Error archiving organization:', error)
            // Handle error with toast notification
        }
    }
}

const deleteOrganization = async () => {
    try {
        deleting.value = true
        await axiosInstance.delete('organizations/current/')
        // Redirect to organizations list
        router.push({ name: 'dashboard.index' })
    } catch (error) {
        console.error('Error deleting organization:', error)
        // Handle error with toast notification
    } finally {
        deleting.value = false
    }
}

const formatIndustry = (industry) => {
    if (!industry) return null
    return industry.charAt(0).toUpperCase() + industry.slice(1)
}

// Lifecycle
onMounted(() => {
    fetchOrganization()
})
</script>

<style scoped></style>