<template>
  <BaseModal :is-open="true" title="Invite Organization's Member" @close="$emit('close')">
    <div class="space-y-6">
      <!-- Intro / Hint -->
      <p class="text-sm text-gray-500 flex items-start gap-2">
        An invitation email will be sent to the specified address with instructions to join your organization.
      </p>

      <!-- Email Field -->
      <div class="group">
        <label class="flex items-center text-xs font-semibold tracking-wide text-gray-600 mb-2 uppercase">
          <svg xmlns="http://www.w3.org/2000/svg"
            class="h-4 w-4 mr-1 text-gray-400 group-focus-within:text-blue-500 transition-colors" viewBox="0 0 24 24"
            fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M3 8l9 6 9-6M4 6h16a1 1 0 011 1v10a1 1 0 01-1 1H4a1 1 0 01-1-1V7a1 1 0 011-1z" />
          </svg>
          Email Address
        </label>
        <div class="relative">
          <input v-model.trim="form.email" type="email" :aria-invalid="emailError ? 'true' : 'false'"
            @blur="validateEmail()"
            class="peer w-full px-3 py-2 bg-white/70 backdrop-blur-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition disabled:opacity-60"
            placeholder="team-member@company.com" />
          <div v-if="emailError" class="absolute -bottom-5 left-1 text-xs text-red-600 flex items-center gap-1">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24"
              stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01M12 5.5l7.5 13h-15L12 5.5z" />
            </svg>
            {{ emailError }}
          </div>
        </div>
      </div>

      <!-- Role Field -->
      <div class="group">
        <label class="flex items-center text-xs font-semibold tracking-wide text-gray-600 mb-2 uppercase">
          <svg xmlns="http://www.w3.org/2000/svg"
            class="h-4 w-4 mr-1 text-gray-400 group-focus-within:text-blue-500 transition-colors" viewBox="0 0 24 24"
            fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
          </svg>
          Role
        </label>
        <select v-model="form.role"
          class="w-full px-3 py-2 bg-white/70 backdrop-blur-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition">
          <option value="" disabled>Select a role</option>
          <option value="member">Member</option>
          <option value="manager">Manager</option>
          <option value="admin">Admin</option>
        </select>
      </div>

      <!-- Feedback Message -->
      <transition name="fade-in" mode="out-in">
        <div v-if="message" :key="message" class="flex items-start gap-3 p-3 rounded-lg border text-sm shadow-sm"
          :class="isError ? 'bg-red-50 border-red-200 text-red-700' : 'bg-green-50 border-green-200 text-green-700'">
          <svg v-if="!isError" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 flex-shrink-0" fill="none"
            viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 flex-shrink-0" fill="none" viewBox="0 0 24 24"
            stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01M12 5.5l7.5 13h-15L12 5.5z" />
          </svg>
          <span>{{ message }}</span>
        </div>
      </transition>
    </div>

    <template #footer>
      <div class="flex flex-col sm:flex-row sm:justify-end gap-3 pt-2">
        <button @click="$emit('close')"
          class="px-4 py-2 rounded-lg border border-gray-300 bg-white/60 backdrop-blur-sm text-gray-700 hover:bg-gray-100 active:scale-[.98] transition cursor-pointer">
          Cancel
        </button>
        <button @click="send" :disabled="loading || !isValid"
          class="relative px-5 py-2 rounded-lg font-medium text-white bg-gradient-to-r from-blue-600 to-indigo-600 shadow hover:shadow-md enabled:hover:from-blue-500 enabled:hover:to-indigo-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed overflow-hidden transition">
          <span v-if="!loading" class="flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
              stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M16 12H8m0 0l4 4m-4-4l4-4" />
            </svg>
            Send Invite
          </span>
          <span v-else class="flex items-center gap-2">
            <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
              viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
            </svg>
            Sending...
          </span>
        </button>
      </div>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, computed, inject } from 'vue'
import { useAuth } from '@/composables/useAuth.js'
import axios from '@/plugins/axiosConfig.js'
import BaseModal from './BaseModal.vue'
const $toast = inject("toast");

const emit = defineEmits(['close', 'invited'])
const { user } = useAuth()

const form = ref({ email: '', role: '' })
const loading = ref(false)
const message = ref('')
const isError = ref(false)
const emailError = ref('')

// Basic validation states
const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const isValid = computed(() => emailPattern.test(form.value.email) && !!form.value.role && !loading.value)

const validateEmail = () => {
  if (!form.value.email) {
    emailError.value = 'Email is required.'
  } else if (!emailPattern.test(form.value.email)) {
    emailError.value = 'Enter a valid email.'
  } else {
    emailError.value = ''
  }
}

const send = async () => {
  validateEmail()
  if (emailError.value || !form.value.role) return

  loading.value = true
  message.value = ''

  try {
    const response = await axios.post(`organizations/invite/`, form.value)
    message.value = response.data.message || 'Invitation sent successfully'
    isError.value = false
    emit('invited', form.value)
    $toast.success('Invitation sent successfully')
  } catch (error) {
    message.value = error.response.data.message || 'Failed to send invitation'
    isError.value = true
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.fade-in-enter-active,
.fade-in-leave-active {
  transition: opacity .25s, transform .25s;
}

.fade-in-enter-from,
.fade-in-leave-to {
  opacity: 0;
  transform: translateY(4px);
}
</style>
