<template>
    <div class="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div class="bg-white p-8 rounded-xl shadow-2xl w-full max-w-md border border-gray-100">
            <!-- Header -->
            <div class="text-center mb-8">
                <div class="mx-auto w-16 h-16 bg-orange-500 rounded-full flex items-center justify-center mb-4">
                    <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-3a1 1 0 011-1h2.586l4.707-4.707A6 6 0 0121 9z" />
                    </svg>
                </div>
                <h1 class="text-3xl font-bold text-gray-900 mb-2">Forgot Password?</h1>
                <p class="text-gray-600">Enter your email address and we'll send you a verification code to reset your
                    password</p>
            </div>



            <!-- Error Alert -->
            <div v-if="errors.general" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                <div class="flex items-center">
                    <svg class="w-5 h-5 text-red-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <p class="text-sm text-red-800">{{ errors.general }}</p>
                </div>
            </div>

            <!-- Form -->
            <form @submit.prevent=" requestOTP " class="space-y-6">
                <!-- Email Field -->
                <BaseInput v-model=" form.email " label="Email Address" type="email"
                    placeholder="Enter your email address" :error=" errors.email " :disabled=" loading " required size="lg"
                    autocomplete="email" @blur="validateField('email')" @input="clearError('email')" />

                <!-- Rate Limit Warning -->
                <div v-if="cooldownTime > 0" class="p-3 bg-amber-50 border border-amber-200 rounded-lg">
                    <div class="flex items-center">
                        <svg class="w-5 h-5 text-amber-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.866-.833-2.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z" />
                        </svg>
                        <p class="text-sm text-amber-700">
                            Please wait {{ formatTime(cooldownTime) }} before requesting again
                        </p>
                    </div>
                </div>

                <!-- Submit Button -->
                <Button type="submit" variant="primary" size="lg" fullWidth :loading=" loading "
                    :disabled=" !isFormValid || cooldownTime > 0 "
                    class="bg-indigo-600 hover:bg-indigo-700 focus:ring-indigo-500">
                    {{ loading ? 'Sending...' : 'Send Verification Code' }}
                </Button>
            </form>

            <!-- Navigation Links -->
            <div class="mt-8 text-center">
                <div class="relative mb-6">
                    <div class="absolute inset-0 flex items-center">
                        <div class="w-full border-t border-slate-200"></div>
                    </div>
                    <div class="relative flex justify-center text-sm">
                        <span class="px-3 bg-white text-slate-500">Remember your password?</span>
                    </div>
                </div>

                <router-link to="/login"
                    class="inline-flex items-center text-slate-600 hover:text-indigo-600 text-sm font-medium transition-colors">
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                    </svg>
                    Back to Login
                </router-link>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, computed, inject, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from "@/plugins/axiosConfig.js"
import Button from '@/components/Button.vue'
import { BaseInput } from '@/components/forms'

const route = useRoute()
const router = useRouter()
const toast = inject('toast')

// State
const loading = ref(false)
const errors = ref({})
const cooldownTime = ref(0)
const cooldownInterval = ref(null)

// Form data
const form = reactive({
    email: route.query.email || ''
})

// Computed
const isFormValid = computed(() => {
    return form.email && isValidEmail(form.email)
})

// Utilities
const isValidEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}

const clearError = (field) => {
    if (errors.value[field]) {
        delete errors.value[field]
    }
}

const validateField = (field) => {
    clearError(field)

    if (field === 'email' && form.email && !isValidEmail(form.email)) {
        errors.value.email = 'Please enter a valid email address'
    }
}

const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return mins > 0 ? `${mins}:${secs.toString().padStart(2, '0')}` : `${secs}s`
}

const startCooldown = (seconds = 90) => {
    cooldownTime.value = seconds
    cooldownInterval.value = setInterval(() => {
        cooldownTime.value--
        if (cooldownTime.value <= 0) clearInterval(cooldownInterval.value)
    }, 1000)
}

const requestOTP = async () => {
    if (loading.value || !isFormValid.value || cooldownTime.value > 0) return

    errors.value = {}
    loading.value = true

    try {
        const response = await axios.post('users/password-reset/request/', {
            email: form.email.trim()
        })

        // Show success message and redirect to OTP verification
        toast.success('Verification code sent successfully!')

        // Auto-redirect to OTP verification page
        router.push({
            name: 'auth.verify-otp',
            query: {
                email: form.email,
                message: `OTP sent successfully to ${form.email}. Please check your email.`
            }
        })

    } catch (error) {
        console.error('Failed to send OTP:', error)
        const status = error.response?.status

        if (status === 404) {
            errors.value.general = 'No account found with this email address'
        } else if (status === 429) {
            errors.value.general = 'OTP already sent. Please wait before requesting again.'
            startCooldown(90)
        } else if (error.response?.data?.message) {
            errors.value.general = error.response.data.message
        } else {
            errors.value.general = 'Failed to send verification code. Please try again.'
        }

        toast.error(errors.value.general)
    } finally {
        loading.value = false
    }
}

// Lifecycle
onMounted(() => {
    if (route.query.email) {
        validateField('email')
    }
})

onUnmounted(() => {
    if (cooldownInterval.value) {
        clearInterval(cooldownInterval.value)
    }
})
</script>
