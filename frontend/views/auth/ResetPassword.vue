<template>
  <div class="min-h-screen bg-slate-50 flex items-center justify-center py-12 px-4">
    <div class="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md border border-slate-200">
      <div class="text-center mb-8">
        <div class="mx-auto w-16 h-16 bg-indigo-600 rounded-full flex items-center justify-center mb-4">
          <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        </div>
        <h1 class="text-3xl font-bold text-slate-900 mb-2">Reset Password</h1>
        <p class="text-slate-600">Create a new secure password for your account</p>
      </div>

      <div v-if="passwordReset" class="mb-6 p-4 bg-emerald-50 border border-emerald-200 rounded-lg">
        <p class="text-sm text-emerald-800 flex items-center">
          <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd"
              d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
              clip-rule="evenodd" />
          </svg>
          Password reset successfully! Redirecting to login...
        </p>
      </div>

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

      <form @submit.prevent=" resetPassword " class="space-y-6" v-if="!passwordReset">
        <div class="relative">
          <BaseInput v-model=" form.newPassword " label="New Password" :type=" showNewPassword ? 'text' : 'password' "
            placeholder="Enter your new password" :error=" errors.newPassword " :disabled=" loading " required
            @blur=" validatePassword " @input="clearError('newPassword')" />
          <button type="button" @click="showNewPassword = !showNewPassword"
            class="absolute right-3 top-9 text-gray-500 hover:text-gray-700">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="showNewPassword" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L8.464 8.464a10.007 10.007 0 00-1.563 3.029M9.878 9.878l.742-.742M21.535 12a10.05 10.05 0 01-2.985 4.825M3 3l18 18" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
          </button>
        </div>

        <div class="relative">
          <BaseInput v-model=" form.confirmPassword " label="Confirm Password"
            :type=" showConfirmPassword ? 'text' : 'password' " placeholder="Confirm your new password"
            :error=" errors.confirmPassword " :disabled=" loading " required @blur=" validateConfirmPassword "
            @input="clearError('confirmPassword')" />
          <button type="button" @click="showConfirmPassword = !showConfirmPassword"
            class="absolute right-3 top-9 text-gray-500 hover:text-gray-700">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="showConfirmPassword" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L8.464 8.464a10.007 10.007 0 00-1.563 3.029M9.878 9.878l.742-.742M21.535 12a10.05 10.05 0 01-2.985 4.825M3 3l18 18" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
          </button>
        </div>

        <div v-if="form.newPassword" class="space-y-2">
          <div class="flex justify-between">
            <span class="text-sm text-slate-700">Password Strength</span>
            <span class="text-sm" :class=" strengthColor ">{{ strengthText }}</span>
          </div>
          <div class="w-full bg-slate-200 rounded-full h-2">
            <div class="h-2 rounded-full transition-all" :class=" strengthColor " :style=" { width: strength + '%' } ">
            </div>
          </div>
          <div class="grid grid-cols-2 gap-2 text-xs">
            <div :class=" checks.length ? 'text-emerald-600' : 'text-slate-400' ">✓ 8+ characters</div>
            <div :class=" checks.uppercase ? 'text-emerald-600' : 'text-slate-400' ">✓ Uppercase</div>
            <div :class=" checks.lowercase ? 'text-emerald-600' : 'text-slate-400' ">✓ Lowercase</div>
            <div :class=" checks.number ? 'text-emerald-600' : 'text-slate-400' ">✓ Number</div>
          </div>
        </div>

        <Button type="submit" variant="primary" size="lg" fullWidth :loading=" loading " :disabled=" !isFormValid "
          class="bg-indigo-600 hover:bg-indigo-700 focus:ring-indigo-500">
          {{ loading ? 'Resetting...' : 'Reset Password' }}
        </Button>
      </form>

      <div class="mt-8 text-center" v-if="!passwordReset">
        <div class="relative mb-6">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-slate-200"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-3 bg-white text-slate-500">Need help?</span>
          </div>
        </div>
        <router-link to="/login"
          class="text-sm text-slate-600 hover:text-indigo-600 transition-colors inline-flex items-center">
          ← Back to Login
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, inject, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from "@/plugins/axiosConfig.js"
import Button from '@/components/Button.vue'
import { BaseInput } from '@/components/forms'

const route = useRoute()
const router = useRouter()
const toast = inject('toast')

const loading = ref(false)
const errors = ref({})
const passwordReset = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)

const token = ref(route.query.token || '')
const email = ref(route.query.email || '')

const form = reactive({
  newPassword: '',
  confirmPassword: ''
})

const isFormValid = computed(() =>
  form.newPassword &&
  form.confirmPassword &&
  form.newPassword === form.confirmPassword &&
  form.newPassword.length >= 8
)

const checks = computed(() => ({
  length: form.newPassword.length >= 8,
  uppercase: /[A-Z]/.test(form.newPassword),
  lowercase: /[a-z]/.test(form.newPassword),
  number: /[0-9]/.test(form.newPassword)
}))

const strength = computed(() => {
  const score = Object.values(checks.value).filter(Boolean).length
  return score === 0 ? 0 : (score / 4) * 100
})

const strengthText = computed(() => {
  const score = Object.values(checks.value).filter(Boolean).length
  return ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong'][score] || 'Very Weak'
})

const strengthColor = computed(() => {
  const score = Object.values(checks.value).filter(Boolean).length
  const colors = ['bg-red-500 text-red-500', 'bg-red-500 text-red-500', 'bg-amber-500 text-amber-500', 'bg-emerald-500 text-emerald-500', 'bg-emerald-600 text-emerald-600']
  return colors[score] || colors[0]
})

const clearError = (field) => delete errors.value[field]

const validatePassword = () => {
  clearError('newPassword')
  if (form.newPassword && form.newPassword.length < 8) {
    errors.value.newPassword = 'Password must be at least 8 characters'
  }
}

const validateConfirmPassword = () => {
  clearError('confirmPassword')
  if (form.confirmPassword && form.newPassword !== form.confirmPassword) {
    errors.value.confirmPassword = 'Passwords do not match'
  }
}

const resetPassword = async () => {
  if (loading.value || !isFormValid.value) return

  errors.value = {}
  validatePassword()
  validateConfirmPassword()

  if (Object.keys(errors.value).length > 0) return

  loading.value = true

  try {
    await axios.post('users/password-reset/', {
      password_reset_token: token.value,
      new_password: form.newPassword,
      confirm_password: form.confirmPassword
    })

    passwordReset.value = true
    toast.success('Password reset successfully!')

    setTimeout(() => {
      router.push({
        name: 'auth.login',
        query: {
          message: 'Password reset successfully. Please login with your new password.',
          email: email.value
        }
      })
    }, 2000)

  } catch (error) {
    const status = error.response?.status
    if (status === 404) {
      errors.value.general = 'Invalid or expired reset token. Please request a new password reset.'
    } else if (error.response?.data?.errors) {
      const backendErrors = error.response.data.errors
      if (backendErrors.new_password) {
        errors.value.newPassword = Array.isArray(backendErrors.new_password) ? backendErrors.new_password[0] : backendErrors.new_password
      }
      if (backendErrors.confirm_password) {
        errors.value.confirmPassword = Array.isArray(backendErrors.confirm_password) ? backendErrors.confirm_password[0] : backendErrors.confirm_password
      }
      if (!errors.value.newPassword && !errors.value.confirmPassword) {
        errors.value.general = 'Please check your password requirements'
      }
    } else {
      errors.value.general = error.response?.data?.message || 'Failed to reset password'
    }

    toast.error(errors.value.general || 'Password reset failed')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (!token.value) {
    router.push({ name: 'auth.forgot-password' })
  }
})
</script>