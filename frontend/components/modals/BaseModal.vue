<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto" @click.self=" handleBackdropClick ">
    <!-- Backdrop with blur effect -->
    <div class="fixed inset-0 backdrop-blur-md bg-black/20 transition-all duration-300"></div>

    <!-- Modal Content -->
    <div class="flex min-h-full items-center justify-center p-4">
      <div class="relative bg-white rounded-2xl shadow-xl w-full transform transition-all duration-300"
        :class=" modalClass " @click.stop>
        <!-- Close Button -->
        <button v-if="showCloseButton" @click=" close "
          class="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition-colors duration-200 z-10 cursor-pointer">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>

        <!-- Modal Header -->
        <div v-if="title || $slots.header" class="px-6 py-4 border-b border-gray-200">
          <slot name="header">
            <h3 class="text-lg font-semibold text-gray-900">{{ title }}</h3>
          </slot>
        </div>

        <!-- Modal Body -->
        <div class="px-6 py-4">
          <slot></slot>
        </div>

        <!-- Modal Footer -->
        <div v-if="$slots.footer" class="px-6 py-4 border-t border-gray-200 bg-gray-50 rounded-b-2xl">
          <slot name="footer"></slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, watch, nextTick } from 'vue'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: ''
  },
  size: {
    type: String,
    default: 'md', // sm, md, lg, xl, xxl
    validator: (value) => ['sm', 'md', 'lg', 'xl', 'xxl'].includes(value)
  },
  showCloseButton: {
    type: Boolean,
    default: true
  },
  closeOnBackdrop: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['close', 'open'])

// Modal size classes
const modalClass = computed(() => {
  const sizeClasses = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-2xl',
    xxl: 'max-w-5xl',
    xxxl: 'max-w-7xl'
  }
  return sizeClasses[props.size]
})

// Handle backdrop click
const handleBackdropClick = () => {
  if (props.closeOnBackdrop) {
    close()
  }
}

// Close modal
const close = () => {
  emit('close')
}

// Handle escape key
const handleEscape = (event) => {
  if (event.key === 'Escape' && props.isOpen) {
    close()
  }
}

// Watch for modal open/close to handle body scroll
watch(() => props.isOpen, (isOpen) => {
  nextTick(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden'
      document.addEventListener('keydown', handleEscape)
      emit('open')
    } else {
      document.body.style.overflow = ''
      document.removeEventListener('keydown', handleEscape)
    }
  })
})
</script>