<template>
  <div class="min-h-screen bg-linear-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-xl border border-white/20 w-full max-w-md">
      <div class="text-center">
        <!-- Email Icon -->
        <div class="w-20 h-20 bg-linear-to-r from-blue-600 to-purple-600 rounded-full mx-auto mb-6 flex items-center justify-center">
          <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
          </svg>
        </div>

        <!-- Title -->
        <h2 class="text-2xl font-bold text-gray-900 mb-3">Check Your Email</h2>
        
        <!-- Description -->
        <div class="space-y-3 text-gray-600 mb-8">
          <p>We've sent a verification link to:</p>
          <p class="font-semibold text-gray-900 bg-gray-100 px-4 py-2 rounded-lg">{{ email }}</p>
          <p class="text-sm">Click the link in your email to verify your account and start using TrackTools.</p>
        </div>

        <!-- Resend Section -->
        <div class="space-y-4">
          <p class="text-sm text-gray-500">Didn't receive the email?</p>
          
          <button
            @click="resendVerification"
            :disabled="resendLoading || countdown > 0"
            class="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <span v-if="resendLoading" class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
              </svg>
              Sending...
            </span>
            <span v-else-if="countdown > 0">Resend in {{ countdown }}s</span>
            <span v-else>Resend Verification Email</span>
          </button>

          <p v-if="resendMessage" class="text-sm" :class="resendSuccess ? 'text-green-600' : 'text-red-600'">
            {{ resendMessage }}
          </p>
        </div>

        <!-- Help Text -->
        <div class="mt-8 p-4 bg-blue-50 rounded-lg">
          <h3 class="font-semibold text-blue-900 mb-2">Email not in your inbox?</h3>
          <ul class="text-sm text-blue-700 space-y-1 text-left">
            <li>• Check your spam/junk folder</li>
            <li>• Make sure {{ email }} is correct</li>
            <li>• The link expires in 24 hours</li>
          </ul>
        </div>

        <!-- Back to Login -->
        <div class="mt-6">
          <router-link
            to="/login"
            class="text-blue-600 hover:text-blue-800 text-sm font-medium transition duration-300 hover:underline"
          >
            Back to Login
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject, onMounted, onUnmounted } from 'vue'
import axios from '@/plugins/axiosConfig.js'

const props = defineProps({
  email: {
    type: String,
    required: true
  }
})

const toast = inject('toast')
const resendLoading = ref(false)
const resendMessage = ref('')
const resendSuccess = ref(false)
const countdown = ref(0)
let countdownTimer = null

const resendVerification = async () => {
  if (resendLoading.value || countdown.value > 0) return
  
  resendLoading.value = true
  resendMessage.value = ''
  
  try {
    const response = await axios.post('/users/email/resend-verification/', {
      email: props.email
    })
    
    resendMessage.value = 'Verification email sent! Please check your inbox.'
    resendSuccess.value = true
    toast.success('Verification email sent successfully!')
    
    // Start 60 second countdown
    countdown.value = 60
    startCountdown()
    
  } catch (error) {
    resendMessage.value = error.response?.data?.message || 'Failed to send verification email.'
    resendSuccess.value = false
    toast.error('Failed to send verification email. Please try again.')
  } finally {
    resendLoading.value = false
  }
}

const startCountdown = () => {
  countdownTimer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(countdownTimer)
    }
  }, 1000)
}

onMounted(() => {
  // Auto-check if email gets verified (optional)
  const checkInterval = setInterval(async () => {
    try {
      const response = await axios.get(`/users/email/status/${props.email}/`)
      if (response.data.is_verified) {
        clearInterval(checkInterval)
        toast.success('Email verified successfully!')
        // Could redirect to login or dashboard here
      }
    } catch (error) {
      // Silently fail
    }
  }, 10000) // Check every 10 seconds

  // Clean up after 5 minutes
  setTimeout(() => clearInterval(checkInterval), 300000)
})

onUnmounted(() => {
  if (countdownTimer) {
    clearInterval(countdownTimer)
  }
})
</script>