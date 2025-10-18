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
                        <router-link to="/organization"
                            class="text-gray-700 hover:text-green-600 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-300 hover:bg-green-50">
                            Organization
                        </router-link>
                        <router-link to="/tasks"
                            class="text-gray-700 hover:text-purple-600 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-300 hover:bg-purple-50">
                            Tasks
                        </router-link>

                        <!-- User Profile Dropdown -->
                        <div class="relative" @click.stop>
                            <button 
                                @click="dropdownOpen = !dropdownOpen"
                                class="flex items-center space-x-2 p-1 rounded-full hover:bg-gray-100 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                                :class="{ 'bg-gray-100': dropdownOpen }"
                            >
                                <!-- User Avatar -->
                                <div class="relative group">
                                    <img 
                                        v-if="user?.photo" 
                                        :src="user.photo" 
                                        :alt="user?.first_name || user?.email"
                                        class="w-10 h-10 rounded-full object-cover border-2 border-gray-200 group-hover:border-blue-300 transition-all duration-300 shadow-sm hover:shadow-md"
                                    />
                                    <div 
                                        v-else 
                                        class="w-10 h-10 rounded-full flex items-center justify-center text-white font-semibold text-sm shadow-sm hover:shadow-md transition-all duration-300 group-hover:scale-105"
                                        :class="getAvatarColor(user?.email || '')"
                                    >
                                        {{ getInitial() }}
                                    </div>
                                    <!-- Online Status Indicator -->
                                    <div class="absolute -bottom-0 -right-0 w-3 h-3 bg-green-400 border-2 border-white rounded-full"></div>
                                </div>
                                <!-- Dropdown Arrow -->
                                <svg 
                                    class="w-4 h-4 text-gray-500 transition-transform duration-200"
                                    :class="{ 'rotate-180': dropdownOpen }"
                                    fill="none" 
                                    stroke="currentColor" 
                                    viewBox="0 0 24 24"
                                >
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                                </svg>
                            </button>

                            <!-- Dropdown Menu -->
                            <transition 
                                enter-active-class="transition ease-out duration-200"
                                enter-from-class="opacity-0 scale-95 translate-y-1"
                                enter-to-class="opacity-100 scale-100 translate-y-0"
                                leave-active-class="transition ease-in duration-150"
                                leave-from-class="opacity-100 scale-100 translate-y-0"
                                leave-to-class="opacity-0 scale-95 translate-y-1"
                            >
                                <div 
                                    v-if="dropdownOpen" 
                                    class="absolute right-0 mt-2 w-64 bg-white rounded-xl shadow-lg border border-gray-200 py-2 z-50"
                                    @click.stop
                                >
                                    <!-- User Info Header -->
                                    <div class="px-4 py-3 border-b border-gray-100">
                                        <div class="flex items-center space-x-3">
                                            <div class="relative">
                                                <img 
                                                    v-if="user?.photo" 
                                                    :src="user.photo" 
                                                    :alt="user?.first_name || user?.email"
                                                    class="w-12 h-12 rounded-full object-cover border-2 border-gray-200"
                                                />
                                                <div 
                                                    v-else 
                                                    class="w-12 h-12 rounded-full flex items-center justify-center text-white font-semibold text-lg"
                                                    :class="getAvatarColor(user?.email || '')"
                                                >
                                                    {{ getInitial() }}
                                                </div>
                                            </div>
                                            <div class="flex-1 min-w-0">
                                                <p class="text-xs text-gray-500 truncate">{{ user?.email }}</p>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- Menu Items -->
                                    <div class="py-1">
                                        <router-link 
                                            to="/profile"
                                            @click="dropdownOpen = false"
                                            class="flex items-center px-4 py-3 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-600 transition-all duration-200"
                                        >
                                            <svg class="w-5 h-5 mr-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                                            </svg>
                                            View Profile
                                        </router-link>
                                        
                                        <router-link 
                                            to="/settings"
                                            @click="dropdownOpen = false"
                                            class="flex items-center px-4 py-3 text-sm text-gray-700 hover:bg-gray-50 hover:text-gray-900 transition-all duration-200"
                                        >
                                            <svg class="w-5 h-5 mr-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                                            </svg>
                                            Settings
                                        </router-link>
                                        
                                        <div class="border-t border-gray-100 my-1"></div>
                                        
                                        <button 
                                            @click="handleLogout"
                                            class="flex items-center w-full px-4 py-3 text-sm text-red-600 hover:bg-red-50 hover:text-red-700 transition-all duration-200"
                                        >
                                            <svg class="w-5 h-5 mr-3 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
                                            </svg>
                                            Sign Out
                                        </button>
                                    </div>
                                </div>
                            </transition>
                        </div>
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
                    <!-- User Info Header for Mobile -->
                    <div class="flex items-center space-x-3 px-3 py-4 bg-gray-50 rounded-lg mb-3">
                        <div class="relative">
                            <img 
                                v-if="user?.photo" 
                                :src="user.photo" 
                                :alt="user?.first_name || user?.email"
                                class="w-12 h-12 rounded-full object-cover border-2 border-gray-200"
                            />
                            <div 
                                v-else 
                                class="w-12 h-12 rounded-full flex items-center justify-center text-white font-semibold text-lg"
                                :class="getAvatarColor(user?.email || '')"
                            >
                                {{ getInitial() }}
                            </div>
                            <!-- Online Status Indicator -->
                            <div class="absolute -bottom-0 -right-0 w-4 h-4 bg-green-400 border-2 border-white rounded-full"></div>
                        </div>
                        <div class="flex-1 min-w-0">
                            <p class="text-xs text-gray-500 truncate">{{ user?.email }}</p>
                        </div>
                    </div>

                    <router-link to="/projects"
                        class="block text-gray-700 hover:text-blue-600 hover:bg-blue-50 px-3 py-2 rounded-lg text-base font-medium transition-all duration-300">
                        Projects
                    </router-link>
                    <router-link to="/organization"
                        class="block text-gray-700 hover:text-green-600 hover:bg-green-50 px-3 py-2 rounded-lg text-base font-medium transition-all duration-300">
                        Organization
                    </router-link>
                    <router-link to="/tasks"
                        class="block text-gray-700 hover:text-purple-600 hover:bg-purple-50 px-3 py-2 rounded-lg text-base font-medium transition-all duration-300">
                        Tasks
                    </router-link>
                    <router-link to="/profile"
                        class="block text-gray-700 hover:text-indigo-600 hover:bg-indigo-50 px-3 py-2 rounded-lg text-base font-medium transition-all duration-300">
                        Profile
                    </router-link>
                    <router-link to="/settings"
                        class="block text-gray-700 hover:text-gray-600 hover:bg-gray-50 px-3 py-2 rounded-lg text-base font-medium transition-all duration-300">
                        Settings
                    </router-link>
                    <div class="border-t border-gray-200 my-2"></div>
                    <button @click="handleLogout"
                        class="w-full text-left bg-gradient-to-r from-red-500 to-red-600 text-white px-3 py-2 rounded-lg text-base font-medium hover:from-red-600 hover:to-red-700 transition-all duration-300 mt-2">
                        Sign Out
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

    <!-- Logout Modal -->
    <LogoutModal 
        :is-open="showLogoutModal" 
        @close="closeLogoutModal" 
    />
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useAuth } from "@/composables/useAuth.js";
import { useLogoutModal } from "@/composables/useLogoutModal.js";
import LogoutModal from "./modals/LogoutModal.vue";

const mobileMenuOpen = ref(false);
const dropdownOpen = ref(false);
const { isAuthenticated, user } = useAuth();
const { showLogoutModal, openLogoutModal, closeLogoutModal } = useLogoutModal();

function handleLogout() {
    openLogoutModal();
    mobileMenuOpen.value = false;
    dropdownOpen.value = false;
}

// Close dropdown when clicking outside
const handleClickOutside = (event) => {
    if (dropdownOpen.value) {
        dropdownOpen.value = false;
    }
    if (mobileMenuOpen.value) {
        mobileMenuOpen.value = false;
    }
}

// Simple utility function for avatar
const getInitial = () => {
    if (!user.value?.email) return 'U';
    
    // Use first letter of email
    return user.value.email.charAt(0).toUpperCase();
}

const getAvatarColor = (email) => {
    if (!email) return 'bg-gray-500';
    
    // Generate consistent color based on email
    const colors = [
        'bg-blue-500', 'bg-green-500', 'bg-purple-500', 'bg-red-500', 
        'bg-yellow-500', 'bg-indigo-500', 'bg-pink-500', 'bg-gray-500'
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
