<template>
  <!-- Global Logout Confirmation Modal -->
  <Teleport to="body">
    <div v-if="isVisible" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-[9999]">
      <div class="bg-white rounded-lg p-6 w-full max-w-md mx-4 transform transition-all duration-300 scale-100">
        <div class="flex items-center mb-4">
          <div class="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center mr-3">
            <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 15.5c-.77.833.192 2.5 1.732 2.5z"></path>
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900">Confirm Logout</h3>
        </div>
        
        <p class="text-gray-600 mb-6">
          Are you sure you want to logout? You'll need to sign in again to access your dashboard.
        </p>
        
        <div class="flex space-x-3 justify-end">
          <button
            @click="handleCancel"
            class="px-4 py-2 text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300 transition duration-300 focus:outline-none focus:ring-2 focus:ring-gray-300"
          >
            Cancel
          </button>
          <button
            @click="handleConfirm"
            class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition duration-300 focus:outline-none focus:ring-2 focus:ring-red-500"
          >
            Yes, Logout
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { useAuth } from "@/composables/useAuth.js";

const { logout } = useAuth();

// Props
const props = defineProps({
  isVisible: {
    type: Boolean,
    default: false
  }
});

// Emits
const emit = defineEmits(['close']);

const handleCancel = () => {
  emit('close');
};

const handleConfirm = () => {
  emit('close');
  logout();
};

// Close modal on Escape key
const handleKeydown = (event) => {
  if (event.key === 'Escape' && props.isVisible) {
    handleCancel();
  }
};

// Add/remove event listener for Escape key
import { onMounted, onUnmounted, watch } from 'vue';

onMounted(() => {
  document.addEventListener('keydown', handleKeydown);
});

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown);
});

// Prevent body scroll when modal is open
watch(() => props.isVisible, (newValue) => {
  if (newValue) {
    document.body.style.overflow = 'hidden';
  } else {
    document.body.style.overflow = '';
  }
});
</script>

<style scoped>
/* Additional modal animations if needed */
</style>