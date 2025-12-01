<template>
  <div :class=" [
    isDark ? 'bg-slate-900 text-slate-100' : 'bg-gray-50 text-gray-900',
    'min-h-screen transition-all duration-300'
  ] ">
    <!-- Main Content -->
    <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <!-- Welcome Section -->
      <div :class=" [
        isDark ? 'bg-slate-800 border border-slate-700' : 'bg-white border border-gray-200',
        'rounded-lg shadow p-6 mb-8 transition-all duration-300'
      ] ">
        <h2 :class=" [
          isDark ? 'text-slate-100' : 'text-gray-900',
          'text-2xl font-bold mb-4 transition-colors duration-300'
        ] ">Welcome to TrackTools!</h2>
        <p :class=" [
          isDark ? 'text-slate-300' : 'text-gray-600',
          'mb-4 transition-colors duration-300'
        ] ">
          Your organization has been successfully created and you're now logged in.
          Here's what you can do next:
        </p>

        <div class="grid md:grid-cols-3 gap-6 mt-6">
          <div v-if="hasRole('owner', 'admin')">
            <router-link to="/organizations/members" :class=" [
              isDark
                ? 'border border-slate-600 hover:border-cyan-400 hover:bg-slate-700 bg-slate-800'
                : 'border border-gray-200 hover:border-blue-300 hover:bg-blue-50 bg-white',
              'rounded-lg p-4 transition-all duration-300 block'
            ] ">
              <div class="flex items-center mb-3">
                <div :class=" [
                  isDark ? 'bg-cyan-900' : 'bg-blue-100',
                  'w-8 h-8 rounded-full flex items-center justify-center mr-3 transition-all duration-300'
                ] ">
                  <svg :class=" [
                    isDark ? 'text-cyan-400' : 'text-blue-600',
                    'w-4 h-4 transition-colors duration-300'
                  ] " fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-2.239"></path>
                  </svg>
                </div>
                <h3 :class=" [
                  isDark ? 'text-slate-100' : 'text-gray-900',
                  'font-semibold transition-colors duration-300'
                ] ">Organization Members</h3>
              </div>
              <p :class=" [
                isDark ? 'text-slate-400' : 'text-gray-600',
                'text-sm transition-colors duration-300'
              ] ">Add your organization members to start collaborating on projects.</p>
            </router-link>
          </div>

          <router-link to="/projects" :class=" [
            isDark
              ? 'border border-slate-600 hover:border-emerald-400 hover:bg-slate-700 bg-slate-800'
              : 'border border-gray-200 hover:border-green-300 hover:bg-green-50 bg-white',
            'rounded-lg p-4 transition-all duration-300 block'
          ] ">
            <div class="flex items-center mb-3">
              <div :class=" [
                isDark ? 'bg-emerald-900' : 'bg-green-100',
                'w-8 h-8 rounded-full flex items-center justify-center mr-3 transition-all duration-300'
              ] ">
                <svg :class=" [
                  isDark ? 'text-emerald-400' : 'text-green-600',
                  'w-4 h-4 transition-colors duration-300'
                ] " fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2">
                  </path>
                </svg>
              </div>
              <h3 :class=" [
                isDark ? 'text-slate-100' : 'text-gray-900',
                'font-semibold transition-colors duration-300'
              ] ">View Projects</h3>
            </div>
            <p :class=" [
              isDark ? 'text-slate-400' : 'text-gray-600',
              'text-sm transition-colors duration-300'
            ] ">View and manage your projects, or create your first one.</p>
          </router-link>

          <div :class=" [
            isDark ? 'border border-slate-600 bg-slate-800' : 'border border-gray-200 bg-white',
            'rounded-lg p-4 transition-all duration-300'
          ] ">
            <div class="flex items-center mb-3">
              <div :class=" [
                isDark ? 'bg-violet-900' : 'bg-purple-100',
                'w-8 h-8 rounded-full flex items-center justify-center mr-3 transition-all duration-300'
              ] ">
                <svg :class=" [
                  isDark ? 'text-violet-400' : 'text-purple-600',
                  'w-4 h-4 transition-colors duration-300'
                ] " fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z">
                  </path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                </svg>
              </div>
              <h3 :class=" [
                isDark ? 'text-slate-100' : 'text-gray-900',
                'font-semibold transition-colors duration-300'
              ] ">Configure Settings</h3>
            </div>
            <p :class=" [
              isDark ? 'text-slate-400' : 'text-gray-600',
              'text-sm transition-colors duration-300'
            ] ">Customize your organization settings and preferences.</p>
          </div>
        </div>
      </div>

      <!-- Quick Stats -->
      <div class="grid md:grid-cols-4 gap-6 mb-8">
        <router-link to="/projects" :class=" [
          isDark
            ? 'bg-slate-800 border border-slate-700 hover:shadow-lg hover:bg-slate-700 hover:border-cyan-400'
            : 'bg-white border border-gray-200 hover:shadow-lg hover:bg-blue-50 hover:border-blue-300',
          'rounded-lg shadow p-6 transition-all duration-300 block'
        ] ">
          <div class="flex items-center">
            <div class="shrink-0">
              <div :class=" [
                isDark ? 'bg-cyan-600' : 'bg-blue-500',
                'w-8 h-8 rounded-md flex items-center justify-center transition-all duration-300'
              ] ">
                <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2">
                  </path>
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <p :class=" [
                isDark ? 'text-slate-400' : 'text-gray-500',
                'text-sm font-medium transition-colors duration-300'
              ] ">Projects</p>
              <p :class=" [
                isDark ? 'text-slate-100' : 'text-gray-900',
                'text-2xl font-semibold transition-colors duration-300'
              ] ">0</p>
            </div>
          </div>
        </router-link>

        <router-link to="/tasks" :class=" [
          isDark
            ? 'bg-slate-800 border border-slate-700 hover:shadow-lg hover:bg-slate-700 hover:border-emerald-400'
            : 'bg-white border border-gray-200 hover:shadow-lg hover:bg-green-50 hover:border-green-300',
          'rounded-lg shadow p-6 transition-all duration-300 block'
        ] ">
          <div class="flex items-center">
            <div class="shrink-0">
              <div :class=" [
                isDark ? 'bg-emerald-600' : 'bg-green-500',
                'w-8 h-8 rounded-md flex items-center justify-center transition-all duration-300'
              ] ">
                <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2">
                  </path>
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <p :class=" [
                isDark ? 'text-slate-400' : 'text-gray-500',
                'text-sm font-medium transition-colors duration-300'
              ] ">Tasks</p>
              <p :class=" [
                isDark ? 'text-slate-100' : 'text-gray-900',
                'text-2xl font-semibold transition-colors duration-300'
              ] ">0</p>
            </div>
          </div>
        </router-link>

        <router-link to="/organizations" :class=" [
          isDark
            ? 'bg-slate-800 border border-slate-700 hover:shadow-lg hover:bg-slate-700 hover:border-violet-400'
            : 'bg-white border border-gray-200 hover:shadow-lg hover:bg-purple-50 hover:border-purple-300',
          'rounded-lg shadow p-6 transition-all duration-300 block'
        ] ">
          <div class="flex items-center">
            <div class="shrink-0">
              <div :class=" [
                isDark ? 'bg-violet-600' : 'bg-purple-500',
                'w-8 h-8 rounded-md flex items-center justify-center transition-all duration-300'
              ] ">
                <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-2.239"></path>
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <p :class=" [
                isDark ? 'text-slate-400' : 'text-gray-500',
                'text-sm font-medium transition-colors duration-300'
              ] ">Organization Members</p>
              <p :class=" [
                isDark ? 'text-slate-100' : 'text-gray-900',
                'text-2xl font-semibold transition-colors duration-300'
              ] ">1</p>
            </div>
          </div>
        </router-link>

        <div :class=" [
          isDark ? 'bg-slate-800 border border-slate-700' : 'bg-white border border-gray-200',
          'rounded-lg shadow p-6 transition-all duration-300'
        ] ">
          <div class="flex items-center">
            <div class="shrink-0">
              <div :class=" [
                isDark ? 'bg-amber-600' : 'bg-yellow-500',
                'w-8 h-8 rounded-md flex items-center justify-center transition-all duration-300'
              ] ">
                <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M15 17h5l-5 5v-5zM10.07 2.82l3.8 3.8M4.93 17.07l3.8-3.8M2.82 10.07l3.8 3.8"></path>
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <p :class=" [
                isDark ? 'text-slate-400' : 'text-gray-500',
                'text-sm font-medium transition-colors duration-300'
              ] ">Active</p>
              <p :class=" [
                isDark ? 'text-slate-100' : 'text-gray-900',
                'text-2xl font-semibold transition-colors duration-300'
              ] ">New</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuth } from "@/composables/useAuth.js";
import { useLogoutModal } from "@/composables/useLogoutModal.js";
import { useTheme } from '@/composables/useTheme.js'

const { user, hasRole, fetchUserProfile } = useAuth();
const { openLogoutModal } = useLogoutModal();
const { isDark } = useTheme()

// Refresh user data when component mounts
onMounted(async () => {
  await fetchUserProfile()
})

const handleLogout = () => {
  openLogoutModal();
}
</script>

<style scoped>
/* Additional styles if needed */
</style>