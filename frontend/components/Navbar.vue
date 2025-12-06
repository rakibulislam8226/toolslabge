<template>
    <nav class="sticky top-0 z-50 transition-all duration-300 border-b shadow-lg"
        :class=" isDark ? 'bg-slate-900/95 backdrop-blur-md border-slate-700 shadow-slate-900/20' : 'bg-white/95 backdrop-blur-md border-gray-200 shadow-gray-900/10' ">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16">
                <!-- Logo -->
                <div class="flex items-center">
                    <router-link :to=" isAuthenticated ? '/dashboard' : '/' "
                        class="text-2xl font-bold transition-colors duration-300"
                        :class=" isDark ? 'text-cyan-400' : 'text-indigo-600' ">
                        TrackTools
                    </router-link>
                </div>

                <!-- Desktop Menu -->
                <div class="flex items-center space-x-4">
                    <!-- Theme Toggle -->
                    <button @click=" toggleTheme " class="p-2 rounded-lg transition-all duration-300 hover:scale-105"
                        :class=" isDark ? 'text-yellow-400 hover:bg-slate-800' : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900' ">
                        <svg v-if="isDark" class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                            <path
                                d="M12 2.25a.75.75 0 01.75.75v2.25a.75.75 0 01-1.5 0V3a.75.75 0 01.75-.75zM7.5 12a4.5 4.5 0 119 0 4.5 4.5 0 01-9 0zM18.894 6.166a.75.75 0 00-1.06-1.06l-1.591 1.59a.75.75 0 101.06 1.061l1.591-1.59zM21.75 12a.75.75 0 01-.75.75h-2.25a.75.75 0 010-1.5H21a.75.75 0 01.75.75zM17.834 18.894a.75.75 0 001.06-1.06l-1.59-1.591a.75.75 0 10-1.061 1.06l1.59 1.591zM12 18a.75.75 0 01.75.75V21a.75.75 0 01-1.5 0v-2.25A.75.75 0 0112 18zM7.758 17.303a.75.75 0 00-1.061-1.06l-1.591 1.59a.75.75 0 001.06 1.061l1.591-1.59zM6 12a.75.75 0 01-.75.75H3a.75.75 0 010-1.5h2.25A.75.75 0 016 12zM6.697 7.757a.75.75 0 001.06-1.06l-1.59-1.591a.75.75 0 00-1.061 1.06l1.59 1.591z" />
                        </svg>
                        <svg v-else class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                            <path fill-rule="evenodd"
                                d="M9.528 1.718a.75.75 0 01.162.819A8.97 8.97 0 009 6a9 9 0 009 9 8.97 8.97 0 003.463-.69.75.75 0 01.981.98 10.503 10.503 0 01-9.694 6.46c-5.799 0-10.5-4.701-10.5-10.5 0-4.368 2.667-8.112 6.46-9.694a.75.75 0 01.818.162z"
                                clip-rule="evenodd" />
                        </svg>
                    </button>

                    <!-- Authenticated Menu -->
                    <template v-if="isAuthenticated">
                        <div class="hidden md:flex items-center space-x-4">
                            <router-link to="/projects"
                                class="px-4 py-2 rounded-lg text-sm transition-all duration-300 hover:scale-105"
                                :class=" $route.path.startsWith('/projects')
                                    ? (isDark ? 'bg-cyan-600 text-white shadow-lg shadow-cyan-600/25 font-bold' : 'bg-indigo-100 text-indigo-900 shadow-lg font-bold')
                                    : (isDark ? 'text-slate-300 hover:text-white hover:bg-slate-700 font-semibold' : 'text-gray-800 hover:text-indigo-600 hover:bg-indigo-50 font-semibold') ">
                                Projects
                            </router-link>
                            <!-- <router-link to="/organizations/members"
                                class="px-4 py-2 rounded-lg text-sm transition-all duration-300 hover:scale-105"
                                :class="$route.path.startsWith('/organizations/members')
                                    ? (isDark ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-600/25 font-bold' : 'bg-emerald-100 text-emerald-900 shadow-lg font-bold')
                                    : (isDark ? 'text-slate-300 hover:text-white hover:bg-slate-700 font-semibold' : 'text-gray-800 hover:text-emerald-600 hover:bg-emerald-50 font-semibold')">
                                Members
                            </router-link> -->
                            <router-link to="/tasks"
                                class="px-4 py-2 rounded-lg text-sm transition-all duration-300 hover:scale-105"
                                :class=" $route.path.startsWith('/tasks')
                                    ? (isDark ? 'bg-violet-600 text-white shadow-lg shadow-violet-600/25 font-bold' : 'bg-violet-100 text-violet-900 shadow-lg font-bold')
                                    : (isDark ? 'text-slate-300 hover:text-white hover:bg-slate-700 font-semibold' : 'text-gray-800 hover:text-violet-600 hover:bg-violet-50 font-semibold') ">
                                Tasks
                            </router-link> <!-- Profile Dropdown -->
                            <div class="relative ml-4" @click.stop>
                                <button @click="dropdownOpen = !dropdownOpen"
                                    class="flex items-center space-x-2 p-2 rounded-lg transition-all duration-300 hover:scale-105 cursor-pointer"
                                    :class=" isDark ? 'hover:bg-slate-800' : 'hover:bg-gray-100 hover:shadow-md' ">
                                    <!-- Avatar -->
                                    <div class="relative">
                                        <img v-if="user?.photo" :src=" user.photo "
                                            :alt=" user?.first_name || user?.email "
                                            class="w-8 h-8 rounded-full object-cover shadow-md"
                                            :class=" isDark ? 'ring-2 ring-slate-600' : 'ring-2 ring-gray-500' " />
                                        <div v-else
                                            class="w-8 h-8 rounded-full flex items-center justify-center text-white font-bold text-sm shadow-md"
                                            :class=" getAvatarColor(user?.email || '') ">
                                            {{ getInitial() }}
                                        </div>
                                        <div
                                            class="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-emerald-400 border-2 border-white rounded-full shadow-sm">
                                        </div>
                                    </div>
                                    <!-- User Info -->
                                    <div class="hidden sm:block text-left">
                                        <div class="text-sm font-semibold"
                                            :class=" isDark ? 'text-slate-100' : 'text-gray-900' ">
                                            {{ user?.first_name || 'User' }}
                                        </div>
                                        <div class="text-xs" :class=" isDark ? 'text-slate-400' : 'text-gray-600' ">
                                            {{ user?.email }}
                                        </div>
                                    </div>
                                    <!-- Dropdown Arrow -->
                                    <svg class="w-4 h-4 transition-transform duration-300"
                                        :class=" [{ 'rotate-180': dropdownOpen }, isDark ? 'text-slate-400' : 'text-gray-700'] "
                                        fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M19 9l-7 7-7-7"></path>
                                    </svg>
                                </button>

                                <!-- Dropdown Menu -->
                                <transition enter-active-class="transition ease-out duration-200"
                                    enter-from-class="opacity-0 scale-95" enter-to-class="opacity-100 scale-100"
                                    leave-active-class="transition ease-in duration-150"
                                    leave-from-class="opacity-100 scale-100" leave-to-class="opacity-0 scale-95">
                                    <div v-if="dropdownOpen"
                                        class="absolute right-0 mt-2 w-64 rounded-lg shadow-lg py-2 z-50 border"
                                        :class=" isDark ? 'bg-slate-800 border-slate-700' : 'bg-white border-gray-200' "
                                        @click.stop>
                                        <!-- User Info Header -->
                                        <router-link to="/profile" @click="dropdownOpen = false"
                                            class="flex items-center px-4 py-3 border-b"
                                            :class=" isDark ? 'border-slate-700 hover:bg-slate-700' : 'border-gray-200 hover:bg-gray-100' ">
                                            <div class="relative">
                                                <img v-if="user?.photo" :src=" user.photo "
                                                    :alt=" user?.first_name || user?.email "
                                                    class="w-10 h-10 rounded-full object-cover shadow-md"
                                                    :class=" isDark ? 'ring-2 ring-slate-600' : 'ring-2 ring-gray-500' " />
                                                <div v-else
                                                    class="w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-sm shadow-md"
                                                    :class=" getAvatarColor(user?.email || '') ">
                                                    {{ getInitial() }}
                                                </div>
                                                <div
                                                    class="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-emerald-400 border-2 border-white rounded-full shadow-sm">
                                                </div>
                                            </div>
                                            <div class="ml-3 text-left">
                                                <div class="text-sm font-semibold"
                                                    :class=" isDark ? 'text-slate-100' : 'text-gray-900' ">
                                                    {{ user?.first_name || 'User' }}
                                                </div>
                                                <div class="text-xs"
                                                    :class=" isDark ? 'text-slate-400' : 'text-gray-600' ">
                                                    {{ user?.email }}
                                                </div>
                                            </div>
                                        </router-link>

                                        <!-- Menu Items -->
                                        <div class="py-1">

                                            <div v-if="hasRole('owner', 'admin')">
                                                <router-link to="/organizations" @click="dropdownOpen = false"
                                                    class="flex items-center px-4 py-2 text-sm transition-colors duration-200"
                                                    :class=" isDark ? 'text-slate-300 hover:bg-slate-700 hover:text-slate-100' : 'text-gray-900 hover:bg-gray-100 hover:text-black' ">
                                                    <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor"
                                                        viewBox="0 0 24 24">
                                                        <path stroke-linecap="round" stroke-linejoin="round"
                                                            stroke-width="2"
                                                            d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4">
                                                        </path>
                                                    </svg>
                                                    Organization
                                                </router-link>
                                                <router-link to="/organizations/members" @click="dropdownOpen = false"
                                                    class="flex items-center px-4 py-2 text-sm transition-colors duration-200"
                                                    :class=" isDark ? 'text-slate-300 hover:bg-slate-700 hover:text-slate-100' : 'text-gray-900 hover:bg-gray-100 hover:text-black' ">
                                                    <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor"
                                                        viewBox="0 0 24 24">
                                                        <path stroke-linecap="round" stroke-linejoin="round"
                                                            stroke-width="2"
                                                            d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zm-10 0a2 2 0 11-4 0 2 2 0 014 0z">
                                                        </path>
                                                    </svg>
                                                    Members
                                                </router-link>
                                            </div>
                                            <div class="my-1 border-t"
                                                :class=" isDark ? 'border-slate-700' : 'border-gray-200' "></div>
                                                <router-link to="/change-password" @click="dropdownOpen = false"
                                                class="flex items-center px-4 py-2 text-sm transition-colors duration-200"
                                                :class=" isDark ? 'text-slate-300 hover:bg-slate-700 hover:text-slate-100' : 'text-gray-900 hover:bg-gray-100 hover:text-black' ">
                                                <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor"
                                                    viewBox="0 0 24 24">
                                                    <path stroke-linecap="round" stroke-linejoin="round"
                                                        stroke-width="2"
                                                        d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                                                </svg>
                                                Change Password
                                            </router-link>
                                            <button @click=" handleLogout "
                                                class="flex items-center w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors duration-200 cursor-pointer">
                                                <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor"
                                                    viewBox="0 0 24 24">
                                                    <path stroke-linecap="round" stroke-linejoin="round"
                                                        stroke-width="2"
                                                        d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1">
                                                    </path>
                                                </svg>
                                                Sign Out
                                            </button>
                                        </div>
                                    </div>
                                </transition>
                            </div>
                        </div>
                    </template>

                    <!-- Guest Menu -->
                    <template v-else>
                        <div class="hidden md:flex items-center space-x-4">
                            <router-link to="/login"
                                class="px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-300 hover:scale-105"
                                :class=" isDark ? 'text-slate-300 hover:text-white hover:bg-slate-700' : 'text-gray-800 hover:text-indigo-600 hover:bg-indigo-50' ">
                                Login
                            </router-link>
                            <router-link to="/register"
                                class="px-4 py-2 rounded-lg text-sm font-semibold text-white transition-all duration-300 hover:scale-105 shadow-lg"
                                :class=" isDark ? 'bg-cyan-600 hover:bg-cyan-700 shadow-cyan-600/25' : 'bg-indigo-600 hover:bg-indigo-700 shadow-indigo-600/25' ">
                                Get Started
                            </router-link>
                        </div>
                    </template>

                    <!-- Mobile Menu Button -->
                    <button @click.stop="mobileMenuOpen = !mobileMenuOpen"
                        class="md:hidden p-2 rounded-lg transition-all duration-300 hover:scale-105"
                        :class=" isDark ? 'text-slate-300 hover:bg-slate-700' : 'text-gray-800 hover:bg-gray-100 hover:text-gray-900' ">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M4 6h16M4 12h16M4 18h16"></path>
                            <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>
            </div>
        </div>

        <!-- Mobile Menu -->
        <transition enter-active-class="transition ease-out duration-200" enter-from-class="opacity-0 scale-95"
            enter-to-class="opacity-100 scale-100" leave-active-class="transition ease-in duration-150"
            leave-from-class="opacity-100 scale-100" leave-to-class="opacity-0 scale-95">
            <div v-if="mobileMenuOpen" class="md:hidden border-t px-4 py-4 space-y-2"
                :class=" isDark ? 'bg-slate-900 border-slate-700' : 'bg-white border-gray-200' " @click.stop>

                <template v-if="isAuthenticated">
                    <!-- User Info for Mobile -->
                    <div class="flex items-center space-x-3 p-3 rounded-lg mb-4 border"
                        :class=" isDark ? 'bg-slate-800 border-slate-700' : 'bg-gray-50 border-gray-200' ">
                        <div class="relative">
                            <img v-if="user?.photo" :src=" user.photo " :alt=" user?.first_name || user?.email "
                                class="w-10 h-10 rounded-full object-cover"
                                :class=" isDark ? 'ring-2 ring-slate-600' : 'ring-2 ring-gray-300' " />
                            <div v-else
                                class="w-10 h-10 rounded-full flex items-center justify-center text-white font-bold"
                                :class=" getAvatarColor(user?.email || '') ">
                                {{ getInitial() }}
                            </div>
                            <div
                                class="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-emerald-400 border-2 border-white rounded-full">
                            </div>
                        </div>
                        <div class="flex-1 min-w-0">
                            <p class="text-sm font-medium truncate"
                                :class=" isDark ? 'text-slate-100' : 'text-slate-900' ">
                                {{ user?.first_name || 'User' }}
                            </p>
                            <p class="text-xs truncate" :class=" isDark ? 'text-slate-400' : 'text-slate-600' ">
                                {{ user?.email }}
                            </p>
                        </div>
                    </div>

                    <router-link to="/projects" @click="mobileMenuOpen = false"
                        class="block px-4 py-2 rounded-lg text-base transition-colors duration-300"
                        :class=" $route.path.startsWith('/projects')
                            ? (isDark ? 'bg-cyan-600 text-white font-bold' : 'bg-indigo-100 text-indigo-900 font-bold')
                            : (isDark ? 'text-slate-300 hover:bg-slate-700 font-semibold' : 'text-gray-800 hover:bg-indigo-50 hover:text-indigo-600 font-semibold') ">
                        Projects
                    </router-link>
                    <router-link to="/organizations/members" @click="mobileMenuOpen = false"
                        class="block px-4 py-2 rounded-lg text-base transition-colors duration-300"
                        :class=" $route.path.startsWith('/organizations/members')
                            ? (isDark ? 'bg-emerald-600 text-white font-bold' : 'bg-emerald-100 text-emerald-900 font-bold')
                            : (isDark ? 'text-slate-300 hover:bg-slate-700 font-semibold' : 'text-gray-800 hover:bg-emerald-50 hover:text-emerald-600 font-semibold') ">
                        Members
                    </router-link>
                    <router-link to="/tasks" @click="mobileMenuOpen = false"
                        class="block px-4 py-2 rounded-lg text-base transition-colors duration-300"
                        :class=" $route.path.startsWith('/tasks')
                            ? (isDark ? 'bg-violet-600 text-white font-bold' : 'bg-violet-100 text-violet-900 font-bold')
                            : (isDark ? 'text-slate-300 hover:bg-slate-700 font-semibold' : 'text-gray-800 hover:bg-violet-50 hover:text-violet-600 font-semibold') ">
                        Tasks
                    </router-link>
                    <router-link to="/profile" @click="mobileMenuOpen = false"
                        class="block px-4 py-2 rounded-lg text-base transition-colors duration-300"
                        :class=" $route.path === '/profile'
                            ? (isDark ? 'bg-cyan-600 text-white font-bold' : 'bg-indigo-100 text-indigo-900 font-bold')
                            : (isDark ? 'text-slate-300 hover:bg-slate-700 font-semibold' : 'text-gray-800 hover:bg-indigo-50 hover:text-indigo-600 font-semibold') ">
                        Profile
                    </router-link>
                    <router-link to="/organizations" @click="mobileMenuOpen = false"
                        class="block px-4 py-2 rounded-lg text-base transition-colors duration-300"
                        :class=" $route.path.startsWith('/organizations') && !$route.path.startsWith('/organizations/members')
                            ? (isDark ? 'bg-gray-600 text-white font-bold' : 'bg-gray-100 text-gray-900 font-bold')
                            : (isDark ? 'text-slate-300 hover:bg-slate-700 font-semibold' : 'text-gray-800 hover:bg-gray-50 hover:text-gray-600 font-semibold') ">
                        Organization
                    </router-link>
                    <div class="my-2 border-t" :class=" isDark ? 'border-slate-700' : 'border-gray-200' "></div>
                    <button @click=" handleLogout "
                        class="w-full text-left px-4 py-2 rounded-lg text-base font-semibold text-red-600 hover:bg-red-50 transition-colors duration-300">
                        Sign Out
                    </button>
                </template>

                <!-- Guest Mobile Menu -->
                <template v-else>
                    <router-link to="/login" @click="mobileMenuOpen = false"
                        class="block px-4 py-2 rounded-lg text-base font-semibold transition-colors duration-300"
                        :class=" isDark ? 'text-slate-300 hover:bg-slate-700' : 'text-gray-800 hover:bg-indigo-50 hover:text-indigo-600' ">
                        Login
                    </router-link>
                    <router-link to="/register" @click="mobileMenuOpen = false"
                        class="block w-full text-center px-4 py-2 rounded-lg text-base font-semibold text-white transition-colors duration-300 mt-3 shadow-lg"
                        :class=" isDark ? 'bg-cyan-600 hover:bg-cyan-700' : 'bg-indigo-600 hover:bg-indigo-700' ">
                        Get Started
                    </router-link>
                </template>
            </div>
        </transition>
    </nav>

    <!-- Logout Modal -->
    <LogoutModal :is-open=" showLogoutModal " @close=" closeLogoutModal " />
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useAuth } from "@/composables/useAuth.js";
import { useLogoutModal } from "@/composables/useLogoutModal.js";
import { useTheme } from "@/composables/useTheme.js";
import LogoutModal from "./modals/LogoutModal.vue";

const { hasRole } = useAuth();
const mobileMenuOpen = ref(false);
const dropdownOpen = ref(false);
const { isAuthenticated, user } = useAuth();
const { showLogoutModal, openLogoutModal, closeLogoutModal } = useLogoutModal();

// Use global theme composable
const { isDark, toggleTheme } = useTheme();

function handleLogout() {
    openLogoutModal();
    mobileMenuOpen.value = false;
    dropdownOpen.value = false;
}

// Close dropdown when clicking outside
const handleClickOutside = (event) => {
    // Check if click is on mobile menu button or its children
    const mobileMenuButton = event.target.closest('button[class*="md:hidden"]');

    if (dropdownOpen.value && !event.target.closest('.relative')) {
        dropdownOpen.value = false;
    }
    if (mobileMenuOpen.value && !mobileMenuButton && !event.target.closest('.md\:hidden')) {
        mobileMenuOpen.value = false;
    }
}

// Simple utility function for avatar
const getInitial = () => {
    if (!user.value?.email) return 'U';
    return user.value.email.charAt(0).toUpperCase();
}

const getAvatarColor = (email) => {
    if (!email) return 'bg-gray-500';

    const colors = [
        'bg-indigo-500', 'bg-emerald-500', 'bg-violet-500', 'bg-rose-500',
        'bg-amber-500', 'bg-cyan-500', 'bg-pink-500', 'bg-teal-500'
    ];
    const hash = email.split('').reduce((a, b) => {
        a = ((a << 5) - a) + b.charCodeAt(0);
        return a & a;
    }, 0);
    return colors[Math.abs(hash) % colors.length];
}

onMounted(() => {
    document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
/* Clean focus styles - no outline borders */
button:focus {
    outline: none;
}

/* Smooth transitions for all interactive elements */
* {
    transition-property: color, background-color, border-color, transform, opacity;
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}
</style>
