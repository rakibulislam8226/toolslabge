<template>
    <nav class="bg-white shadow-lg sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16">
                <!-- Left: Logo -->
                <div class="flex items-center">
                    <router-link to="/" class="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent hover:scale-105 transition-transform duration-300">
                        BaseTrack
                    </router-link>
                </div>

                <!-- Right: Menu Items -->
                <div class="hidden md:flex items-center space-x-6">
                    <router-link to="/projects"
                        class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-300 hover:bg-blue-50">
                        Projects
                    </router-link>
                    <router-link to="/tasks"
                        class="text-gray-700 hover:text-purple-600 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-300 hover:bg-purple-50">
                        Tasks
                    </router-link>
                    <router-link to="/profile"
                        class="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-300 hover:bg-indigo-50">
                        Profile
                    </router-link>
                    <button @click="logout"
                        class="bg-gradient-to-r from-red-500 to-red-600 text-white px-4 py-2 rounded-full text-sm font-medium hover:from-red-600 hover:to-red-700 transform hover:scale-105 transition-all duration-300 shadow-md">
                        Logout
                    </button>
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
                <router-link to="/projects"
                    class="block text-gray-700 hover:text-blue-600 hover:bg-blue-50 px-3 py-2 rounded-lg text-base font-medium transition-all duration-300">
                    Projects
                </router-link>
                <router-link to="/tasks"
                    class="block text-gray-700 hover:text-purple-600 hover:bg-purple-50 px-3 py-2 rounded-lg text-base font-medium transition-all duration-300">
                    Tasks
                </router-link>
                <router-link to="/profile"
                    class="block text-gray-700 hover:text-indigo-600 hover:bg-indigo-50 px-3 py-2 rounded-lg text-base font-medium transition-all duration-300">
                    Profile
                </router-link>
                <button @click="logout"
                    class="w-full text-left bg-gradient-to-r from-red-500 to-red-600 text-white px-3 py-2 rounded-lg text-base font-medium hover:from-red-600 hover:to-red-700 transition-all duration-300 mt-2">
                    Logout
                </button>
            </div>
        </transition>
    </nav>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const mobileMenuOpen = ref(false);
const router = useRouter();

function logout() {
    localStorage.removeItem("token");
    router.push("/login");
}
</script>
