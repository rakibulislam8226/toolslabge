<template>
    <div id="app" class="min-h-screen">
        <Navbar />
        <main class="min-h-screen">
            <router-view />
        </main>
    </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useTheme } from '@/composables/useTheme.js';
import Navbar from '@components/Navbar.vue';

// Initialize global theme
const { initializeTheme, watchSystemTheme } = useTheme();

onMounted(() => {
    initializeTheme();
    watchSystemTheme();
});
</script>
