<template>
    <nav class="bg-white shadow-lg sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16">
                <!-- Left: Logo -->
                <div class="flex items-center">
                    <router-link :to="isAuthenticated ? '/dashboard' : '/'" class="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent hover:scale-105 transition-transform duration-300">
                        BaseTrack
                    </router-link>
                </div>

                <!-- Right: Menu Items -->
                <div class="hidden md:flex items-center space-x-6">
                    <!-- Authenticated Menu -->
                    <template v-if="isAuthenticated">
                        <router-link to="/projects"
                            class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-300 hover:bg-blue-50">
                            Projects
                        </router-link>
                        <router-link to="/teams"
                            class="text-gray-700 hover:text-green-600 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-300 hover:bg-green-50">
                            Teams
                        </router-link>
                        <router-link to="/tasks"
                            class="text-gray-700 hover:text-purple-600 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-300 hover:bg-purple-50">
                            Tasks
                        </router-link>
                        <router-link to="/profile"
                            class="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-300 hover:bg-indigo-50">
                            Profile
                        </router-link>
                        <span class="text-gray-600 text-sm">{{ user?.first_name || 'User' }}</span>
                        <button @click="handleLogout"
                            class="bg-gradient-to-r from-red-500 to-red-600 text-white px-4 py-2 rounded-full text-sm font-medium hover:from-red-600 hover:to-red-700 transform hover:scale-105 transition-all duration-300 shadow-md">
                            Logout
                        </button>
                    </template>

                    <!-- Guest Menu -->
                    <template v-else>
                        <router-link to="/login"
                            class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-300 hover:bg-blue-50">
                            Login
                        </router-link>
                        <router-link to="/register"
                            class="bg-gradient-to-r from-blue-500 to-blue-600 text-white px-4 py-2 rounded-full text-sm font-medium hover:from-blue-600 hover:to-blue-700 transform hover:scale-105 transition-all duration-300 shadow-md">
                            Get Started
                        </router-link>
                    </template>
                </div>

                <!-- Mobile Menu Button -->
                <div class="flex items-center md:hidden">
                    <button @click="mobileMenuOpen = !mobileMenuOpen" class="text-gray-700 focus:outline-none">
                        <svg v-if="!mobileMenuOpen" class="h-6 w-6" fill="none" stroke="currentColor"
                            viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M4 6h16M4 12h16M4 18h16"></path>
                        </svg>
                        <svg v-else class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"
                            xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>
            </div>
        </div>

        <!-- Mobile Menu -->
        <transition 
            enter-active-class="transition ease-out duration-200"
            enter-from-class="opacity-0 scale-95"
            enter-to-class="opacity-100 scale-100"
            leave-active-class="transition ease-in duration-150"
            leave-from-class="opacity-100 scale-100"
            leave-to-class="opacity-0 scale-95"
        >
            <div v-if="mobileMenuOpen" class="md:hidden bg-white border-t border-gray-200 px-2 pt-2 pb-3 space-y-2 shadow-lg">
                <!-- Authenticated Mobile Menu -->
                <template v-if="isAuthenticated">
                    <router-link to="/projects"
                        class="block text-gray-700 hover:text-blue-600 hover:bg-blue-50 px-3 py-2 rounded-lg text-base font-medium transition-all duration-300">
                        Projects
                    </router-link>
                    <router-link to="/teams"
                        class="block text-gray-700 hover:text-green-600 hover:bg-green-50 px-3 py-2 rounded-lg text-base font-medium transition-all duration-300">
                        Teams
                    </router-link>
                    <router-link to="/tasks"
                        class="block text-gray-700 hover:text-purple-600 hover:bg-purple-50 px-3 py-2 rounded-lg text-base font-medium transition-all duration-300">
                        Tasks
                    </router-link>
                    <router-link to="/profile"
                        class="block text-gray-700 hover:text-indigo-600 hover:bg-indigo-50 px-3 py-2 rounded-lg text-base font-medium transition-all duration-300">
                        Profile
                    </router-link>
                    <div class="px-3 py-2 text-gray-600 text-sm border-t border-gray-200">
                        {{ user?.first_name || 'User' }}
                    </div>
                    <button @click="handleLogout"
                        class="w-full text-left bg-gradient-to-r from-red-500 to-red-600 text-white px-3 py-2 rounded-lg text-base font-medium hover:from-red-600 hover:to-red-700 transition-all duration-300 mt-2">
                        Logout
                    </button>
                </template>

                <!-- Guest Mobile Menu -->
                <template v-else>
                    <router-link to="/login"
                        class="block text-gray-700 hover:text-blue-600 hover:bg-blue-50 px-3 py-2 rounded-lg text-base font-medium transition-all duration-300">
                        Login
                    </router-link>
                    <router-link to="/register"
                        class="block w-full text-center bg-gradient-to-r from-blue-500 to-blue-600 text-white px-3 py-2 rounded-lg text-base font-medium hover:from-blue-600 hover:to-blue-700 transition-all duration-300 mt-2">
                        Get Started
                    </router-link>
                </template>
            </div>
        </transition>
    </nav>
</template>

<script setup>
import { ref } from "vue";
import { useAuth } from "@/composables/useAuth.js";
import { useLogoutModal } from "@/composables/useLogoutModal.js";

const mobileMenuOpen = ref(false);
const { isAuthenticated, user } = useAuth();
const { openLogoutModal } = useLogoutModal();

function handleLogout() {
    openLogoutModal();
    mobileMenuOpen.value = false;
}
</script>
