<template>
  <BaseModal :is-open="true" title="Invite Organization's Member" @close="$emit('close')">
    <div class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
        <input
          v-model="form.email"
          type="email"
          class="w-full px-3 py-2 border rounded-lg"
          placeholder="Enter email"
        />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Role</label>
        <select v-model="form.role" class="w-full px-3 py-2 border rounded-lg">
          <option value="">Select role</option>
          <option value="member">Member</option>
          <option value="admin">Admin</option>
        </select>
      </div>
      <div v-if="message" class="p-3 rounded" :class="messageClass">{{ message }}</div>
    </div>
    <template #footer>
      <div class="flex space-x-3 justify-end">
        <button @click="$emit('close')" class="px-4 py-2 border rounded-lg">Cancel</button>
        <button @click="send" :disabled="loading" class="px-4 py-2 bg-blue-600 text-white rounded-lg">
          {{ loading ? 'Sending...' : 'Send' }}
        </button>
      </div>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuth } from '@/composables/useAuth.js'
import axios from '@/plugins/axiosConfig.js'
import BaseModal from './BaseModal.vue'

const emit = defineEmits(['close', 'invited'])
const { user } = useAuth()

const form = ref({ email: '', role: '' })
const loading = ref(false)
const message = ref('')
const isError = ref(false)

const messageClass = computed(() => 
  isError.value ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'
)

const send = async () => {
  if (!form.value.email || !form.value.role) return
  
  loading.value = true
  message.value = ''
  
  try {
    const orgId = user.value?.organizations?.[0]?.organization_id
    await axios.post(`organizations/${orgId}/invite/`, form.value)
    
    message.value = 'Invitation sent!'
    isError.value = false
    emit('invited', form.value)
    setTimeout(() => emit('close'), 1500)
  } catch (error) {
    message.value = 'Failed to send invitation'
    isError.value = true
  } finally {
    loading.value = false
  }
}
</script>
