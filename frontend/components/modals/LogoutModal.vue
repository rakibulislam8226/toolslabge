<template>
  <BaseModal 
    :is-open="isOpen" 
    title="Sign Out" 
    size="sm" 
    @close="close"
  >
    <!-- Modal Content -->
    <div class="text-center">
      <!-- Icon -->
      <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100 mb-4">
        <svg class="h-6 w-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
        </svg>
      </div>
      
      <!-- Message -->
      <h3 class="text-lg font-medium text-gray-900 mb-2">Are you sure?</h3>
      <p class="text-sm text-gray-500 mb-6">
        You will be signed out of your account and redirected to the home page.
      </p>
    </div>

    <!-- Footer with actions -->
    <template #footer>
      <div class="flex space-x-3 justify-end">
        <button
          @click="close"
          class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200"
        >
          Cancel
        </button>
        <button
          @click="confirmLogout"
          class="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors duration-200"
        >
          Sign Out
        </button>
      </div>
    </template>
  </BaseModal>
</template>

<script setup>
import { useAuth } from '@/composables/useAuth.js'
import BaseModal from './BaseModal.vue'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close'])

const { logout } = useAuth()

const close = () => {
  emit('close')
}

const confirmLogout = () => {
  logout()
  close()
}
</script>