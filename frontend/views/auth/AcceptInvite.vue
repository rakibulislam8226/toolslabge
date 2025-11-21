<template>
    <div
        class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div
            class="bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-xl border border-white/20 w-full max-w-md relative overflow-hidden">
            <!-- Background decoration -->
            <div
                class="absolute -top-10 -right-10 w-20 h-20 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full opacity-20">
            </div>
            <div
                class="absolute -bottom-10 -left-10 w-32 h-32 bg-gradient-to-tr from-indigo-400 to-blue-500 rounded-full opacity-20">
            </div>

            <!-- Header -->
            <div class="text-center mb-8 relative z-10">
                <div
                    class="w-16 h-16 bg-gradient-to-r from-green-600 to-blue-600 rounded-full mx-auto mb-4 flex items-center justify-center">
                    <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z">
                        </path>
                    </svg>
                </div>
                <h1
                    class="text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent mb-2">
                    Accept Invitation
                </h1>
                <p class="text-gray-600">Complete your account setup to join the organization</p>
            </div>

            <!-- Loading State -->
            <div v-if="checkingToken" class="text-center py-8 relative z-10">
                <div class="inline-flex items-center space-x-2">
                    <svg class="animate-spin h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4">
                        </circle>
                        <path class="opacity-75" fill="currentColor"
                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                        </path>
                    </svg>
                    <span class="text-gray-600">Verifying invitation...</span>
                </div>
            </div>

            <!-- Invalid Token State -->
            <div v-else-if="!tokenValid" class="text-center py-8 relative z-10">
                <div class="w-16 h-16 bg-red-100 rounded-full mx-auto mb-4 flex items-center justify-center">
                    <svg class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z">
                        </path>
                    </svg>
                </div>
                <h2 class="text-xl font-semibold text-red-600 mb-2">Invalid Invitation</h2>
                <p class="text-gray-600 mb-6">This invitation link is invalid or has already been used.</p>
                <router-link to="/login"
                    class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition duration-200">
                    Go to Login
                </router-link>
            </div>

            <!-- Accept Invitation Form -->
            <form v-else @submit.prevent=" handleSubmit " class="space-y-6 relative z-10">
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <BaseInput label="First Name" v-model=" form.first_name " placeholder="Enter your first name"
                        :error=" errors.first_name " size="md" @blur="validateField('first_name')"
                        @input="handleFieldInput('first_name')" required />

                    <BaseInput label="Last Name" v-model=" form.last_name " placeholder="Enter your last name"
                        :error=" errors.last_name " size="md" @blur="validateField('last_name')"
                        @input="handleFieldInput('last_name')" required />
                </div>

                <BaseInput label="Password" type="password" v-model=" form.password "
                    placeholder="Create a secure password" :error=" errors.password "
                    help-text="Password must be at least 8 characters long" size="md" @blur="validateField('password')"
                    @input="handleFieldInput('password')" required />

                <BaseInput label="Confirm Password" type="password" v-model=" form.confirm_password "
                    placeholder="Confirm your password" :error=" errors.confirm_password " size="md"
                    @blur="validateField('confirm_password')" @input="handleFieldInput('confirm_password')" required />

                <Button type="submit" variant="primary" size="lg" fullWidth :disabled=" !isFormValid || loading "
                    :loading=" loading " loadingText="Accepting Invitation..." label="Accept Invitation"
                    class="mt-8 bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700 shadow-lg hover:shadow-xl transition-all duration-200 transform hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none disabled:shadow-lg" />
            </form>

            <div class="mt-8 text-center space-y-3 relative z-10">
                <div class="flex items-center justify-center space-x-2">
                    <div class="h-px bg-gray-300 flex-1"></div>
                    <span class="text-gray-500 text-sm">or</span>
                    <div class="h-px bg-gray-300 flex-1"></div>
                </div>

                <p class="text-gray-600 text-sm">
                    Already have an account?
                    <router-link to="/login"
                        class="text-blue-600 hover:text-blue-800 text-sm font-semibold transition duration-300 hover:underline">
                        Sign in here
                    </router-link>
                </p>

                <router-link to="/"
                    class="inline-flex items-center text-gray-500 hover:text-gray-700 text-sm transition duration-300 hover:underline">
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M10 19l-7-7m0 0l7-7m-7 7h18">
                        </path>
                    </svg>
                    Back to Home
                </router-link>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, inject, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from "@/plugins/axiosConfig.js";
import { useAuth } from "@/composables/useAuth.js";
import Button from '@/components/Button.vue'
import { BaseInput } from '@/components/forms'

const router = useRouter()
const route = useRoute()
const { login } = useAuth()
const toast = inject('toast')

// Form data
const form = reactive({
    first_name: '',
    last_name: '',
    password: '',
    confirm_password: ''
})

const loading = ref(false)
const checkingToken = ref(true)
const tokenValid = ref(false)
const errors = ref({})
const token = ref('')

// Required fields
const requiredFields = ['first_name', 'last_name', 'password', 'confirm_password']

// Field labels for error messages
const fieldLabels = {
    first_name: 'First name',
    last_name: 'Last name',
    password: 'Password',
    confirm_password: 'Confirm password'
}

// Computed property to check if form is valid
const isFormValid = computed(() => {
    // Check if all required fields have values
    const hasAllValues = requiredFields.every(field => {
        const value = form[field]?.toString().trim()
        return value && value.length > 0
    })

    // Check if passwords match
    const passwordsMatch = form.password === form.confirm_password

    // Check if password meets minimum length
    const passwordValid = form.password && form.password.length >= 8

    // Check if there are no current errors
    const noErrors = Object.keys(errors.value).length === 0

    return hasAllValues && passwordsMatch && passwordValid && noErrors
})

// Check if token exists and is valid on component mount
onMounted(async () => {
    token.value = route.query.token

    if (!token.value) {
        toast.error('No invitation token provided.')
        checkingToken.value = false
        tokenValid.value = false
        return
    }

    // Token exists, assume it's valid for now
    // The actual validation will happen when the form is submitted
    checkingToken.value = false
    tokenValid.value = true
})

// Validate single field
const validateField = (fieldName) => {
    const value = form[fieldName]?.toString().trim()

    // Required field validation
    if (requiredFields.includes(fieldName) && !value) {
        errors.value[fieldName] = `${fieldLabels[fieldName]} is required`
        return false
    }

    // Password validation
    if (fieldName === 'password' && value && value.length < 8) {
        errors.value[fieldName] = 'Password must be at least 8 characters long'
        return false
    }

    // Confirm password validation
    if (fieldName === 'confirm_password' && value) {
        if (value !== form.password) {
            errors.value[fieldName] = 'Passwords do not match'
            return false
        }
    }

    // Clear error if validation passes
    delete errors.value[fieldName]
    return true
}

// Real-time validation on input change
const handleFieldInput = (fieldName) => {
    // Clear error immediately when user starts typing
    if (errors.value[fieldName]) {
        delete errors.value[fieldName]
    }

    // If confirm password field and password field has value, revalidate both
    if (fieldName === 'password' && form.confirm_password) {
        validateField('confirm_password')
    }
    if (fieldName === 'confirm_password' && form.password) {
        validateField('confirm_password')
    }
}

// Validate all fields
const validateForm = () => {
    let isValid = true
    requiredFields.forEach(field => {
        if (!validateField(field)) {
            isValid = false
        }
    })

    // Additional check for password matching
    if (form.password !== form.confirm_password) {
        errors.value.confirm_password = 'Passwords do not match'
        isValid = false
    }

    return isValid
}

// Clear error for specific field
const clearError = (fieldName) => {
    delete errors.value[fieldName]
}

// Check if token exists and is valid on component mount
const handleSubmit = async () => {
    // Validate all fields before submission
    let isValid = true
    requiredFields.forEach(field => {
        if (!validateField(field)) {
            isValid = false
        }
    })

    if (!isValid) {
        toast.error('Please fix the errors below and try again.')
        return
    }

    loading.value = true

    try {
        // Prepare data for API (exclude confirm_password)
        const apiData = {
            first_name: form.first_name.trim(),
            last_name: form.last_name.trim(),
            password: form.password
        }

        const response = await axios.post(`organizations/accept-invite/?token=${token.value}`, apiData)
        toast.success('Invitation accepted successfully! You can now log in.')

        // Redirect to login page after successful acceptance
        setTimeout(() => {
            router.push('/login')
        }, 1500)

    } catch (error) {
        console.error('Accept invitation error:', error)

        const errorData = error.response?.data

        if (error.response?.status === 400) {
            const errorMessage = errorData?.detail || 'Invalid or expired invitation token.'
            toast.error(errorMessage)

            // If token is invalid, update the UI state
            if (errorMessage.toLowerCase().includes('token') || errorMessage.toLowerCase().includes('invitation')) {
                tokenValid.value = false
                return
            }
        }

        // Handle field-specific validation errors
        if (errorData && typeof errorData === 'object') {
            let hasFieldErrors = false

            // Clear previous errors
            errors.value = {}

            // Handle different error response formats
            if (errorData.data?.errors) {
                // Handle API error format: { data: { errors: [{ field: "message" }] } }
                errorData.data.errors.forEach(errorObj => {
                    Object.assign(errors.value, errorObj)
                    hasFieldErrors = true
                })
            } else {
                // Handle standard validation errors
                Object.keys(errorData).forEach(field => {
                    if (requiredFields.includes(field)) {
                        const message = Array.isArray(errorData[field]) ? errorData[field][0] : errorData[field]
                        if (typeof message === 'string') {
                            errors.value[field] = message
                            hasFieldErrors = true
                        }
                    }
                })
            }

            if (hasFieldErrors) {
                toast.error('Please fix the errors below and try again.')
            } else {
                // General error message if no field-specific errors
                const message = errorData?.detail || errorData?.message || 'Something went wrong. Please try again.'
                toast.error(message)
            }
        } else {
            // Handle general errors
            const message = errorData?.detail || errorData?.message || 'Something went wrong. Please try again.'
            toast.error(message)
        }
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
/* Custom animations and enhanced styles */
.slide-fade-enter-active,
.slide-fade-leave-active {
    transition: all 0.3s ease;
}

.slide-fade-enter-from {
    opacity: 0;
    transform: translateY(-10px);
}

.slide-fade-leave-to {
    opacity: 0;
    transform: translateY(10px);
}

/* Enhanced button hover effects */
.group:hover .group-hover\:scale-105 {
    transform: scale(1.05);
}

/* Glassmorphism effect enhancement */
.backdrop-blur-sm {
    backdrop-filter: blur(8px);
}

/* Custom focus states for better accessibility */
.focus-within\:ring-2:focus-within {
    box-shadow: 0 0 0 2px rgb(59 130 246 / 0.5);
}

/* Loading spinner animation */
@keyframes spin {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}

.animate-spin {
    animation: spin 1s linear infinite;
}

/* Gradient text animation */
@keyframes gradient-shift {

    0%,
    100% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }
}

.animate-gradient {
    background-size: 200% 200%;
    animation: gradient-shift 3s ease infinite;
}

/* Form validation styling */
.error-shake {
    animation: shake 0.5s ease-in-out;
}

@keyframes shake {

    0%,
    100% {
        transform: translateX(0);
    }

    25% {
        transform: translateX(-5px);
    }

    75% {
        transform: translateX(5px);
    }
}

/* Enhanced shadow effects */
.shadow-glow {
    box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
}

/* Responsive improvements */
@media (max-width: 640px) {
    .grid-cols-1.sm\:grid-cols-2 {
        grid-template-columns: 1fr;
    }
}

/* Custom scrollbar for better UX */
::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.1);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb {
    background: rgba(59, 130, 246, 0.3);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(59, 130, 246, 0.5);
}
</style>