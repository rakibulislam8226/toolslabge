import { ref } from 'vue'

// Global state for logout confirmation modal
const showLogoutModal = ref(false)

export function useLogoutModal() {
  const openLogoutModal = () => {
    showLogoutModal.value = true
  }

  const closeLogoutModal = () => {
    showLogoutModal.value = false
  }

  return {
    showLogoutModal: showLogoutModal,
    openLogoutModal,
    closeLogoutModal
  }
}