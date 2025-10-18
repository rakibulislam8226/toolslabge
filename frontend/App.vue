<template>
    <Navbar />
    <router-view />
    
    <!-- Global Logout Confirmation Modal -->
    <LogoutConfirmationModal 
      :isVisible="showLogoutModal" 
      @close="closeLogoutModal" 
    />
</template>

<script setup>
import Navbar from '@components/Navbar.vue';
import LogoutConfirmationModal from '@/components/modals/LogoutConfirmationModal.vue';
import { useLogoutModal } from '@/composables/useLogoutModal.js';

const { showLogoutModal, closeLogoutModal } = useLogoutModal();
</script>
