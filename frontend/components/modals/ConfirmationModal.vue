<template>
  <BaseModal 
    :is-open="isOpen" 
    :title="title" 
    size="sm" 
    @close="close"
  >
    <!-- Icon -->
    <div class="text-center mb-4">
      <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full mb-4"
           :class="iconClass">
        <svg class="h-6 w-6" :class="iconColor" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="iconPath"></path>
        </svg>
      </div>
      
      <!-- Message -->
      <h3 class="text-lg font-medium text-gray-900 mb-2">{{ title }}</h3>
      <p class="text-sm text-gray-500">{{ message }}</p>
    </div>

    <!-- Footer with actions -->
    <template #footer>
      <div class="flex space-x-3 justify-end">
        <button
          @click="close"
          class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200"
        >
          {{ cancelText }}
        </button>
        <button
          @click="confirm"
          class="px-4 py-2 text-sm font-medium text-white border border-transparent rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors duration-200"
          :class="confirmButtonClass"
        >
          {{ confirmText }}
        </button>
      </div>
    </template>
  </BaseModal>
</template>

<script setup>
import { computed } from 'vue'
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
    default: 'Are you sure you want to proceed?'
  },
  type: {
    type: String,
    default: 'warning', // success, warning, danger, info
    validator: (value) => ['success', 'warning', 'danger', 'info'].includes(value)
  },
  confirmText: {
    type: String,
    default: 'Confirm'
  },
  cancelText: {
    type: String,
    default: 'Cancel'
  }
})

const emit = defineEmits(['close', 'confirm'])

// Dynamic styling based on type
const iconClass = computed(() => {
  const classes = {
    success: 'bg-green-100',
    warning: 'bg-yellow-100',
    danger: 'bg-red-100',
    info: 'bg-blue-100'
  }
  return classes[props.type]
})

const iconColor = computed(() => {
  const colors = {
    success: 'text-green-600',
    warning: 'text-yellow-600',
    danger: 'text-red-600',
    info: 'text-blue-600'
  }
  return colors[props.type]
})

const iconPath = computed(() => {
  const paths = {
    success: 'M5 13l4 4L19 7',
    warning: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z',
    danger: 'M6 18L18 6M6 6l12 12',
    info: 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z'
  }
  return paths[props.type]
})

const confirmButtonClass = computed(() => {
  const classes = {
    success: 'bg-green-600 hover:bg-green-700 focus:ring-green-500',
    warning: 'bg-yellow-600 hover:bg-yellow-700 focus:ring-yellow-500',
    danger: 'bg-red-600 hover:bg-red-700 focus:ring-red-500',
    info: 'bg-blue-600 hover:bg-blue-700 focus:ring-blue-500'
  }
  return classes[props.type]
})

const close = () => {
  emit('close')
}

const confirm = () => {
  emit('confirm')
  close()
}
</script>