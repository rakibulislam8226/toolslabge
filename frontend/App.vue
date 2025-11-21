<template>
    <div id="app" class="min-h-screen">
        <Navbar v-if="!hideNavbar" />
        <main class="min-h-screen">
            <router-view />
        </main>
    </div>
</template>

<script setup>
import { onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useTheme } from '@/composables/useTheme.js';
import Navbar from '@components/Navbar.vue';

const route = useRoute();

// Initialize global theme
const { initializeTheme, watchSystemTheme } = useTheme();

// Hide navbar on certain pages
const hideNavbar = computed(() => {
    const hideOnRoutes = ['auth.accept-invite'];
    return hideOnRoutes.includes(route.name);
});

onMounted(() => {
    initializeTheme();
    watchSystemTheme();
});
</script>
