<template>
    <div class="min-h-screen transition-colors duration-300" :class=" isDark ? 'bg-slate-900' : 'bg-gray-50' ">
        <div class="max-w-4xl mx-auto p-6">
            <!-- Header -->
            <div class="mb-8">
                <h1 class="text-3xl font-bold mb-2 transition-colors duration-300"
                    :class=" isDark ? 'text-white' : 'text-gray-900' ">
                    Profile Settings
                </h1>
                <p class="transition-colors duration-300" :class=" isDark ? 'text-slate-400' : 'text-gray-600' ">
                    Update your personal information and profile photo
                </p>
            </div>

            <!-- Profile Form -->
            <div class="rounded-lg shadow-sm border transition-colors duration-300"
                :class=" isDark ? 'bg-slate-800 border-slate-700' : 'bg-white border-gray-200' ">
                <form @submit.prevent=" handleSubmit " class="p-6 space-y-6">

                    <!-- Profile Photo Section -->
                    <div class="space-y-6">
                        <h3 class="text-lg font-medium transition-colors duration-300"
                            :class=" isDark ? 'text-white' : 'text-gray-900' ">
                            Profile Photo
                        </h3>

                        <div class="flex flex-col sm:flex-row sm:items-start gap-6">
                            <!-- Current Photo Display -->
                            <div class="flex-shrink-0">
                                <div class="relative">
                                    <img v-if="getPhotoPreview() && !shouldRemovePhoto" :src=" getPhotoPreview() "
                                        :alt=" user?.first_name || user?.email "
                                        class="w-32 h-32 rounded-full object-cover border-4 transition-colors duration-300"
                                        :class=" isDark ? 'border-slate-600' : 'border-gray-200' ">
                                    <div v-else
                                        class="w-32 h-32 rounded-full flex items-center justify-center text-white font-bold text-2xl border-4 transition-colors duration-300"
                                        :class=" [getAvatarColor(user?.email || ''), isDark ? 'border-slate-600' : 'border-gray-200'] ">
                                        {{ getInitial() }}
                                    </div>

                                    <!-- Upload Button -->
                                    <label
                                        class="absolute bottom-0 right-0 bg-blue-600 hover:bg-blue-700 text-white rounded-full p-2 cursor-pointer transition-colors duration-200">
                                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z">
                                            </path>
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"></path>
                                        </svg>
                                        <input ref="fileInput" type="file" accept="image/*"
                                            @change=" handlePhotoChange " class="hidden">
                                    </label>
                                </div>
                            </div>

                            <!-- Photo Controls -->
                            <div class="flex-1" v-if="(form.photo || user?.photo) && !shouldRemovePhoto">
                                <Button class="mt-2 px-3 py-1 text-xs rounded" type="button" variant="secondary"
                                    size="sm" @click=" removePhoto ">
                                    Remove Photo
                                </Button>
                            </div>
                        </div>
                    </div>

                    <!-- Personal Information -->
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
                        <div>
                            <label for="first_name"
                                class="block text-sm font-medium mb-2 transition-colors duration-300"
                                :class=" isDark ? 'text-white' : 'text-gray-900' ">
                                First Name
                            </label>
                            <input v-model=" form.first_name " type="text" id="first_name"
                                class="w-full px-4 py-3 rounded-lg border transition-all duration-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                :class=" [
                                    isDark
                                        ? 'bg-slate-700 border-slate-600 text-white placeholder-slate-400'
                                        : 'bg-white border-gray-300 text-gray-900 placeholder-gray-500',
                                    fieldErrors.first_name ? 'border-red-500' : ''
                                ] " placeholder="Enter your first name">
                            <p v-if="fieldErrors.first_name" class="mt-1 text-sm text-red-600">
                                {{ Array.isArray(fieldErrors.first_name) ? fieldErrors.first_name[0] :
                                    fieldErrors.first_name }}
                            </p>
                        </div>

                        <div>
                            <label for="last_name" class="block text-sm font-medium mb-2 transition-colors duration-300"
                                :class=" isDark ? 'text-white' : 'text-gray-900' ">
                                Last Name
                            </label>
                            <input v-model=" form.last_name " type="text" id="last_name"
                                class="w-full px-4 py-3 rounded-lg border transition-all duration-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                :class=" [
                                    isDark
                                        ? 'bg-slate-700 border-slate-600 text-white placeholder-slate-400'
                                        : 'bg-white border-gray-300 text-gray-900 placeholder-gray-500',
                                    fieldErrors.last_name ? 'border-red-500' : ''
                                ] " placeholder="Enter your last name">
                            <p v-if="fieldErrors.last_name" class="mt-1 text-sm text-red-600">
                                {{ Array.isArray(fieldErrors.last_name) ? fieldErrors.last_name[0] :
                                    fieldErrors.last_name }}
                            </p>
                        </div>
                    </div>

                    <!-- Email Address (Read-only) -->
                    <div>
                        <BaseInput label="Email Address" type="email" :value=" user?.email || '' " readonly :class=" isDark ? 'bg-slate-700 border-slate-600 text-white placeholder-slate-400' :
                            'bg-gray-100 border-gray-300 text-gray-900 placeholder-gray-500 cursor-not-allowed' ">
                        </BaseInput>
                    </div>

                    <div class="flex justify-end pt-6 border-t transition-colors duration-300"
                        :class=" isDark ? 'border-slate-700' : 'border-gray-200' ">
                        <Button type="submit" variant="primary" :loading=" loading ">
                            {{ loading ? 'Updating...' : 'Update Profile' }}
                        </Button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted, inject } from 'vue'
import { useAuth } from "@/composables/useAuth.js"
import { useTheme } from '@/composables/useTheme.js'
import axios from '@/plugins/axiosConfig.js'
import Button from '@/components/Button.vue'
import { BaseInput, BaseSelect } from '@/components/forms'

const { user, fetchUserProfile } = useAuth()
const { isDark } = useTheme()
const toast = inject('toast')

const loading = ref(false)
const fieldErrors = ref({})
const fileInput = ref(null)
const shouldRemovePhoto = ref(false)

const form = reactive({
    first_name: '',
    last_name: '',
    photo: null
})

// Initialize form with current user data
onMounted(async () => {
    await fetchUserProfile()
    if (user.value) {
        form.first_name = user.value.first_name || ''
        form.last_name = user.value.last_name || ''
    }
})

// Get photo preview URL
const getPhotoPreview = () => {
    if (form.photo && typeof form.photo !== 'string') {
        return URL.createObjectURL(form.photo)
    }
    if (form.photo && typeof form.photo === 'string') {
        return form.photo
    }
    return user.value?.photo || null
}

// Handle photo upload
const handlePhotoChange = (event) => {
    const file = event.target.files[0]
    if (file) {
        // Validate file size (max 5MB)
        if (file.size > 5 * 1024 * 1024) {
            toast.error('Photo must be smaller than 5MB')
            event.target.value = ''
            return
        }

        if (!file.type.startsWith('image/')) {
            toast.error('Please select a valid image file')
            event.target.value = ''
            return
        }

        form.photo = file
        shouldRemovePhoto.value = false
    }
}

// Remove photo
const removePhoto = () => {
    shouldRemovePhoto.value = true
    form.photo = null
    if (fileInput.value) {
        fileInput.value.value = ''
    }
}



// Handle form submission
const handleSubmit = async () => {
    if (loading.value) return

    loading.value = true
    fieldErrors.value = {}

    try {
        const formData = new FormData()
        formData.append('first_name', form.first_name)
        formData.append('last_name', form.last_name)

        // Handle photo: new file upload, remove existing, or keep current
        if (form.photo && typeof form.photo !== 'string') {
            formData.append('photo', form.photo)
        } else if (shouldRemovePhoto.value) {
            formData.append('photo', '')
        }

        const response = await axios.patch('users/profile/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })

        // Update user data in store
        await fetchUserProfile()

        form.photo = null
        shouldRemovePhoto.value = false
        if (fileInput.value) {
            fileInput.value.value = ''
        }

        toast.success('Profile updated successfully!')

    } catch (error) {
        console.error('Profile update error:', error)

        if (error.response?.data?.errors) {
            fieldErrors.value = error.response.data.errors
        } else if (error.response?.data) {
            const errorData = error.response.data
            if (typeof errorData === 'object') {
                fieldErrors.value = errorData
            } else {
                toast.error('Failed to update profile')
            }
        } else {
            toast.error('Failed to update profile')
        }
    } finally {
        loading.value = false
    }
}

// Utility functions for avatar
const getInitial = () => {
    if (!user.value?.email) return 'U'
    return user.value.email.charAt(0).toUpperCase()
}

const getAvatarColor = (email) => {
    if (!email) return 'bg-gray-500'

    const colors = [
        'bg-indigo-500', 'bg-emerald-500', 'bg-violet-500', 'bg-rose-500',
        'bg-cyan-500', 'bg-amber-500', 'bg-pink-500', 'bg-lime-500'
    ]

    let hash = 0
    for (let i = 0; i < email.length; i++) {
        hash = ((hash << 5) - hash) + email.charCodeAt(i)
        hash = hash & hash // Convert to 32bit integer
    }

    return colors[Math.abs(hash) % colors.length]
}
</script>