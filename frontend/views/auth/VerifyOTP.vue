<template>
  <div class="min-h-screen bg-slate-50 flex items-center justify-center py-12 px-4">
    <div class="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md border border-slate-200">
      <div class="text-center mb-8">
        <div class="mx-auto w-16 h-16 bg-indigo-600 rounded-full flex items-center justify-center mb-4">
          <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M3 8l7.89 2.26a2 2 0 001.22 0L20 8m-17 4v8a2 2 0 002 2h14a2 2 0 002-2v-8" />
          </svg>
        </div>
        <h1 class="text-3xl font-bold text-slate-900 mb-2">Verify Your Code</h1>
        <p class="text-slate-600">We sent a 4-digit code to <span class="font-medium text-slate-900">{{ email }}</span>
        </p>
      </div>

      <!-- Success Message from Previous Page -->
      <div v-if="route.query.message" class="mb-6 p-4 bg-emerald-50 border border-emerald-200 rounded-lg">
        <p class="text-sm text-emerald-800 flex items-center">
          <svg class="w-4 h-4 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd"
              d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
              clip-rule="evenodd" />
          </svg>
          {{ route.query.message }}
        </p>
      </div>

      <!-- OTP Verified Message -->
      <div v-if="otpVerified" class="mb-6 p-4 bg-emerald-50 border border-emerald-200 rounded-lg">
        <p class="text-sm text-emerald-800 flex items-center">
          <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd"
              d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
              clip-rule="evenodd" />
          </svg>
          OTP verified! Redirecting...
        </p>
      </div>

      <!-- Error Alert -->
      <div v-if="errors.general" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
        <p class="text-sm text-red-800 flex items-center">
          <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd"
              d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
              clip-rule="evenodd" />
          </svg>
          {{ errors.general }}
        </p>
      </div>

      <form @submit.prevent=" verifyOTP " class="space-y-6" v-if="!otpVerified">
        <BaseInput v-model=" form.email " label="Email Address" type="email" disabled class="opacity-75" />

        <div class="space-y-3">
          <label class="block text-sm font-medium text-slate-700">Verification Code</label>
          <div class="flex space-x-3 justify-center">
            <input v-for="(digit, index) in otpDigits" :key=" index " :ref=" el => otpInputs[index] = el "
              v-model=" otpDigits[index] " type="text" maxlength="1" :disabled=" loading "
              class="w-12 h-12 text-center text-lg font-semibold border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all"
              :class=" errors.otp ? 'border-red-300 bg-red-50' : 'border-slate-300' "
              @input="handleOTPInput(index, $event)" @keydown="handleKeydown(index, $event)"
              @paste="handlePaste($event)" />
          </div>
          <p v-if="errors.otp" class="text-sm text-red-600">{{ errors.otp }}</p>
          <p class="text-xs text-slate-500 text-center">Enter the 4-digit code sent to your email</p>
        </div>

        <Button type="submit" variant="primary" size="lg" fullWidth :loading=" loading " :disabled=" !isFormValid "
          class="bg-indigo-600 hover:bg-indigo-700 focus:ring-indigo-500">
          {{ loading ? 'Verifying...' : 'Verify Code' }}
        </Button>
      </form>

      <!-- Resend Section -->
      <div v-if="!otpVerified" class="mt-6 text-center">
        <p class="text-sm text-slate-600 mb-4">Didn't receive the code?</p>
        <Button type="button" variant="outline" size="sm" :disabled=" loading || cooldownTime > 0 " @click=" resendOTP "
          class="text-indigo-600 border-indigo-300 hover:bg-indigo-50 hover:border-indigo-400 focus:ring-indigo-500">
          {{ cooldownTime > 0 ? `Resend in ${ formatTime(cooldownTime) }` : 'Resend verification code' }}
        </Button>
      </div>

      <!-- Navigation Links -->
      <div class="mt-8 text-center">
        <div class="relative mb-6">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-slate-200"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-3 bg-white text-slate-500">Need help?</span>
          </div>
        </div>

        <div class="space-y-3">
          <router-link :to=" { name: 'auth.forgot-password', query: { email } } "
            class="block text-sm text-slate-600 hover:text-indigo-600 transition-colors">
            ← Back to request new code
          </router-link>
          <router-link to="/login" class="block text-sm text-slate-600 hover:text-indigo-600 transition-colors">
            Cancel and return to login
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, inject, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from "@/plugins/axiosConfig.js"
import Button from '@/components/Button.vue'
import { BaseInput } from '@/components/forms'

const route = useRoute()
const router = useRouter()
const toast = inject('toast')

const loading = ref(false)
const errors = ref({})
const otpVerified = ref(false)
const cooldownTime = ref(0)
const cooldownInterval = ref(null)
const otpInputs = ref([])
const email = ref(route.query.email || '')
const form = reactive({ email: email.value, otp: '' })
const otpDigits = ref(['', '', '', ''])

const isFormValid = computed(() => form.email && form.otp.length === 4)

const updateOTP = () => form.otp = otpDigits.value.join('')
const clearError = (field) => delete errors.value[field]

const formatTime = (seconds) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return mins > 0 ? `${mins}:${secs.toString().padStart(2, '0')}` : `${secs}s`
}

const handleOTPInput = (index, event) => {
  const value = event.target.value.replace(/[^0-9]/g, '')

  if (value.length > 1) {
    const digits = value.substring(0, 4).split('')
    digits.forEach((digit, i) => {
      if (index + i < 4) otpDigits.value[index + i] = digit
    })
    const nextIndex = Math.min(index + digits.length, 3)
    otpInputs.value[nextIndex]?.focus()
  } else {
    otpDigits.value[index] = value
    if (value && index < 3) otpInputs.value[index + 1]?.focus()
  }
  updateOTP()
  clearError('otp')
}

const handleKeydown = (index, event) => {
  if (event.key === 'Backspace') {
    if (!otpDigits.value[index] && index > 0) {
      otpInputs.value[index - 1]?.focus()
      otpDigits.value[index - 1] = ''
    } else {
      otpDigits.value[index] = ''
    }
    updateOTP()
  } else if (event.key === 'ArrowLeft' && index > 0) {
    otpInputs.value[index - 1]?.focus()
  } else if (event.key === 'ArrowRight' && index < 3) {
    otpInputs.value[index + 1]?.focus()
  }
}

const handlePaste = (event) => {
  event.preventDefault()
  const digits = event.clipboardData.getData('text').replace(/[^0-9]/g, '').substring(0, 4).split('')
  if (digits.length) {
    digits.forEach((digit, i) => otpDigits.value[i] = digit || '')
    updateOTP()
    otpInputs.value[Math.min(digits.length - 1, 3)]?.focus()
  }
}

const startCooldown = (seconds = 90) => {
  cooldownTime.value = seconds
  cooldownInterval.value = setInterval(() => {
    cooldownTime.value--
    if (cooldownTime.value <= 0) clearInterval(cooldownInterval.value)
  }, 1000)
}

const verifyOTP = async () => {
  if (loading.value || !isFormValid.value) return

  errors.value = {}
  loading.value = true

  try {
    const response = await axios.post('users/password-reset/verify-otp/', {
      email: form.email.trim(),
      otp: form.otp
    })

    console.log('Backend Response:', response.data)

    // Handle nested response structure: response.data.data.password_reset_token
    const responseData = response.data.data || response.data
    const passwordResetToken = responseData.password_reset_token

    console.log('Extracted Token:', passwordResetToken)

    if (passwordResetToken) {
      otpVerified.value = true
      toast.success('OTP verified successfully!')
      setTimeout(() => {
        router.push({
          name: 'auth.reset-password',
          query: { token: passwordResetToken, email: form.email }
        })
      }, 1500)
    } else {
      console.error('No token found in response:', responseData)
      throw new Error('Invalid response format - no token received')
    }
  } catch (error) {
    console.error('OTP Verification Error:', error)
    console.error('Error Response:', error.response?.data)

    const status = error.response?.status

    if (status === 404) {
      errors.value.general = 'Invalid or expired OTP. Please request a new one.'
    } else if (error.response?.data?.message) {
      errors.value.general = error.response.data.message
    } else if (error.message.includes('Invalid response format')) {
      errors.value.general = 'Server response error. Please try again.'
    } else {
      errors.value.general = 'Failed to verify OTP. Please try again.'
    }

    errors.value.otp = 'Invalid verification code'
    otpDigits.value = ['', '', '', '']
    updateOTP()
    otpInputs.value[0]?.focus()
    toast.error(errors.value.general)
  } finally {
    loading.value = false
  }
}

const resendOTP = async () => {
  if (loading.value || cooldownTime.value > 0) return

  loading.value = true
  errors.value = {}

  try {
    await axios.post('users/password-reset/request/', { email: form.email.trim() })
    startCooldown(90)
    toast.success('New verification code sent!')
    otpDigits.value = ['', '', '', '']
    updateOTP()
    otpInputs.value[0]?.focus()
  } catch (error) {
    errors.value.general = error.response?.data?.message || 'Failed to resend verification code'
    toast.error(errors.value.general)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  if (!email.value) {
    router.push({ name: 'auth.forgot-password' })
    return
  }
  await nextTick()
  otpInputs.value[0]?.focus()

  // Start cooldown timer when page loads (user just requested OTP)
  startCooldown(90)
})

onUnmounted(() => cooldownInterval.value && clearInterval(cooldownInterval.value))
</script>