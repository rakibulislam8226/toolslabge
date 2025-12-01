<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
        <div class="text-center">
          <!-- Loading State -->
          <div v-if="loading" class="space-y-4">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <h2 class="text-lg font-medium text-gray-900">Verifying your email...</h2>
          </div>

          <!-- Success State -->
          <div v-else-if="verified" class="space-y-4">
            <div class="rounded-full bg-green-100 p-3 w-16 h-16 mx-auto flex items-center justify-center">
              <svg class="h-8 w-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
              </svg>
            </div>
            <h2 class="text-xl font-semibold text-gray-900">Email Verified Successfully!</h2>
            <p class="text-gray-600">Your account has been activated.</p>
            <div class="mt-6">
              <router-link
                to="/login"
                class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Continue to Login
              </router-link>
            </div>
          </div>

          <!-- Error State -->
          <div v-else class="space-y-4">
            <div class="rounded-full bg-red-100 p-3 w-16 h-16 mx-auto flex items-center justify-center">
              <svg class="h-8 w-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </div>
            <h2 class="text-xl font-semibold text-gray-900">Verification Failed</h2>
            <p class="text-gray-600">{{ errorMessage }}</p>
            
            <!-- Resend Option -->
            <div v-if="showResend" class="mt-6 space-y-3">
              <div>
                <label for="email" class="sr-only">Email</label>
                <input
                  id="email"
                  v-model="resendEmail"
                  type="email"
                  placeholder="Enter your email"
                  class="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                />
              </div>
              <button
                @click="resendVerification"
                :disabled="resendLoading || !resendEmail"
                class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span v-if="resendLoading" class="flex items-center">
                  <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
                  </svg>
                  Sending...
                </span>
                <span v-else>Resend Verification Email</span>
              </button>
              <p v-if="resendMessage" class="text-sm" :class="resendSuccess ? 'text-green-600' : 'text-red-600'">
                {{ resendMessage }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { useAuth } from '@/composables/useAuth.js'

export default {
  name: 'EmailVerification',
  setup() {
    const { isAuthenticated, fetchUserProfile } = useAuth()
    
    return {
      isAuthenticated,
      fetchUserProfile
    }
  },
  data() {
    return {
      loading: true,
      verified: false,
      errorMessage: '',
      showResend: false,
      resendEmail: '',
      resendLoading: false,
      resendMessage: '',
      resendSuccess: false
    }
  },
  mounted() {
    this.verifyToken()
  },
  methods: {
    async verifyToken() {
      const token = this.$route.params.token
      
      if (!token) {
        this.loading = false
        this.errorMessage = 'Invalid verification link. No token provided.'
        this.showResend = true
        return
      }

      try {
        const response = await axios.post('/api/v1/users/email/verify/', {
          token: token
        })
        
        if (response.data.message && response.data.message.includes('successfully')) {
          this.verified = true
          
          // If user is logged in, refresh their profile data and redirect to dashboard
          if (this.isAuthenticated) {
            await this.fetchUserProfile()
            setTimeout(() => this.$router.push('/dashboard'), 2000)
          } else {
            // Auto-redirect to login after 3 seconds
            setTimeout(() => this.$router.push('/login'), 3000)
          }
        } else {
          throw new Error(response.data.message || 'Verification failed')
        }
      } catch (error) {
        this.errorMessage = error.response?.data?.message || 
                           error.response?.data?.errors?.token?.[0] || 
                           'Verification failed. Please try again.'
        this.showResend = true
      } finally {
        this.loading = false
      }
    },

    async resendVerification() {
      if (!this.resendEmail) return
      
      this.resendLoading = true
      this.resendMessage = ''
      
      try {
        const response = await axios.post('/api/v1/users/email/resend-verification/', {
          email: this.resendEmail
        })
        
        this.resendMessage = response.data.message
        this.resendSuccess = true
      } catch (error) {
        this.resendMessage = error.response?.data?.message || 
                           error.response?.data?.errors?.email?.[0] || 
                           'Failed to send verification email.'
        this.resendSuccess = false
      } finally {
        this.resendLoading = false
      }
    }
  }
}
</script>