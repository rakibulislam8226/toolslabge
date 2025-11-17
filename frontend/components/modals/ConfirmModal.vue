<template>
  <BaseModal :is-open=" isOpen " :title=" title " size="md" @close=" handleCancel ">
    <div class="space-y-4">
      <!-- Icon -->
      <div class="flex items-center justify-center w-12 h-12 mx-auto bg-red-100 rounded-full">
        <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z">
          </path>
        </svg>
      </div>

      <!-- Message -->
      <div class="text-center">
        <p class="text-sm text-gray-700 whitespace-pre-line leading-relaxed">{{ message }}</p>
      </div>
    </div>

    <template #footer>
      <div class="flex justify-end space-x-3">
        <button type="button" @click=" handleCancel "
          class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
          :disabled=" loading ">
          {{ cancelText }}
        </button>
        <button type="button" @click=" handleConfirm " :class=" confirmClass "
          class="px-4 py-2 text-sm font-medium text-white border border-transparent rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
          :disabled=" loading ">
          <svg v-if="loading" class="w-4 h-4 mr-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" class="opacity-25"></circle>
            <path fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              class="opacity-75"></path>
          </svg>
          {{ loading ? loadingText : confirmText }}
        </button>
      </div>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref } from 'vue'
import BaseModal from './BaseModal.vue'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: 'Confirm Action'
  },
  message: {
    type: String,
    required: true
  },
  confirmText: {
    type: String,
    default: 'Confirm'
  },
  cancelText: {
    type: String,
    default: 'Cancel'
  },
  loadingText: {
    type: String,
    default: 'Processing...'
  },
  confirmClass: {
    type: String,
    default: 'bg-red-600 hover:bg-red-700 focus:ring-red-500'
  }
})

const emit = defineEmits(['confirm', 'cancel'])

const loading = ref(false)

const handleConfirm = async () => {
  loading.value = true
  try {
    await emit('confirm')
  } finally {
    loading.value = false
  }
}

const handleCancel = () => {
  if (!loading.value) {
    emit('cancel')
  }
}
</script>

<style scoped>
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}
</style>