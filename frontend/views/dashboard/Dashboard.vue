<template>
  <div :class=" [
    isDark ? 'bg-slate-900 text-slate-100' : 'bg-gray-50 text-gray-900',
    'min-h-screen transition-all duration-300'
  ] ">
    <!-- Main Content -->
    <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">

      <!-- Hero Section -->
      <div :class=" [
        isDark ? 'bg-gradient-to-r from-slate-800 to-slate-700 border border-slate-600' : 'bg-gradient-to-r from-blue-50 to-indigo-50 border border-gray-200',
        'rounded-2xl shadow-lg p-8 mb-8 transition-all duration-300'
      ] ">
        <div class="text-center">
          <div class="flex justify-center mb-6">
            <div :class=" [
              isDark ? 'bg-cyan-600' : 'bg-blue-600',
              'w-16 h-16 rounded-full flex items-center justify-center transition-all duration-300'
            ] ">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01">
                </path>
              </svg>
            </div>
          </div>
          <h1 :class=" [
            isDark ? 'text-slate-100' : 'text-gray-900',
            'text-4xl font-bold mb-4 transition-colors duration-300'
          ] ">Welcome to TrackTools</h1>
          <p :class=" [
            isDark ? 'text-slate-300' : 'text-gray-700',
            'text-xl mb-6 max-w-3xl mx-auto leading-relaxed transition-colors duration-300'
          ] ">Your comprehensive project management system designed to streamline organizational workflows, enhance
            team collaboration, and boost productivity with intelligent task tracking and automated notifications.</p>
          <div class="flex flex-wrap justify-center gap-3">
            <span :class=" [
              isDark ? 'bg-cyan-900 text-cyan-200' : 'bg-blue-100 text-blue-800',
              'px-3 py-1 rounded-full text-sm font-medium transition-all duration-300'
            ] ">Organization-Based Management</span>
            <span :class=" [
              isDark ? 'bg-emerald-900 text-emerald-200' : 'bg-green-100 text-green-800',
              'px-3 py-1 rounded-full text-sm font-medium transition-all duration-300'
            ] ">Email Notifications</span>
            <span :class=" [
              isDark ? 'bg-violet-900 text-violet-200' : 'bg-purple-100 text-purple-800',
              'px-3 py-1 rounded-full text-sm font-medium transition-all duration-300'
            ] ">Real-time Collaboration</span>
            <span :class=" [
              isDark ? 'bg-rose-900 text-rose-200' : 'bg-red-100 text-red-800',
              'px-3 py-1 rounded-full text-sm font-medium transition-all duration-300'
            ] ">Task Priority Management</span>
          </div>
        </div>
      </div>

      <!-- Features Section -->
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
        <!-- Project Organization -->
        <div :class=" [
          isDark ? 'bg-slate-800 border border-slate-700' : 'bg-white border border-gray-200',
          'rounded-lg shadow p-6 transition-all duration-300 hover:shadow-lg'
        ] ">
          <div class="flex items-center mb-4">
            <div :class=" [
              isDark ? 'bg-cyan-600' : 'bg-blue-500',
              'w-10 h-10 rounded-lg flex items-center justify-center mr-4 transition-all duration-300'
            ] ">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M19 11H5m14-7l-2 2m0 10l2 2m-2-8H9a4 4 0 100 8h10">
                </path>
              </svg>
            </div>
            <h3 :class=" [
              isDark ? 'text-slate-100' : 'text-gray-900',
              'text-lg font-semibold transition-colors duration-300'
            ] ">Organization-Based Projects</h3>
          </div>
          <p :class=" [
            isDark ? 'text-slate-300' : 'text-gray-600',
            'text-sm leading-relaxed transition-colors duration-300'
          ] ">Create and manage projects within your organization structure. Set project timelines, assign members with
            specific roles, and organize work with customizable status tracking.</p>
        </div>

        <!-- Task Management -->
        <div :class=" [
          isDark ? 'bg-slate-800 border border-slate-700' : 'bg-white border border-gray-200',
          'rounded-lg shadow p-6 transition-all duration-300 hover:shadow-lg'
        ] ">
          <div class="flex items-center mb-4">
            <div :class=" [
              isDark ? 'bg-emerald-600' : 'bg-green-500',
              'w-10 h-10 rounded-lg flex items-center justify-center mr-4 transition-all duration-300'
            ] ">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z">
                </path>
              </svg>
            </div>
            <h3 :class=" [
              isDark ? 'text-slate-100' : 'text-gray-900',
              'text-lg font-semibold transition-colors duration-300'
            ] ">Advanced Task Management</h3>
          </div>
          <p :class=" [
            isDark ? 'text-slate-300' : 'text-gray-600',
            'text-sm leading-relaxed transition-colors duration-300'
          ] ">Create detailed tasks with priority levels (High, Medium, Low), estimated hours, due dates, and custom
            status workflows. Track status history and deadline extensions with full audit trails.</p>
        </div>

        <!-- Team Collaboration -->
        <div :class=" [
          isDark ? 'bg-slate-800 border border-slate-700' : 'bg-white border border-gray-200',
          'rounded-lg shadow p-6 transition-all duration-300 hover:shadow-lg'
        ] ">
          <div class="flex items-center mb-4">
            <div :class=" [
              isDark ? 'bg-violet-600' : 'bg-purple-500',
              'w-10 h-10 rounded-lg flex items-center justify-center mr-4 transition-all duration-300'
            ] ">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z">
                </path>
              </svg>
            </div>
            <h3 :class=" [
              isDark ? 'text-slate-100' : 'text-gray-900',
              'text-lg font-semibold transition-colors duration-300'
            ] ">Rich Collaboration Tools</h3>
          </div>
          <p :class=" [
            isDark ? 'text-slate-300' : 'text-gray-600',
            'text-sm leading-relaxed transition-colors duration-300'
          ] ">Collaborate through task comments with @mentions, file attachments, and real-time activity tracking.
            Share files, discuss progress, and maintain detailed project communication history.</p>
        </div>

        <!-- Progress Tracking -->
        <div :class=" [
          isDark ? 'bg-slate-800 border border-slate-700' : 'bg-white border border-gray-200',
          'rounded-lg shadow p-6 transition-all duration-300 hover:shadow-lg'
        ] ">
          <div class="flex items-center mb-4">
            <div :class=" [
              isDark ? 'bg-amber-600' : 'bg-yellow-500',
              'w-10 h-10 rounded-lg flex items-center justify-center mr-4 transition-all duration-300'
            ] ">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z">
                </path>
              </svg>
            </div>
            <h3 :class=" [
              isDark ? 'text-slate-100' : 'text-gray-900',
              'text-lg font-semibold transition-colors duration-300'
            ] ">Comprehensive Activity Tracking</h3>
          </div>
          <p :class=" [
            isDark ? 'text-slate-300' : 'text-gray-600',
            'text-sm leading-relaxed transition-colors duration-300'
          ] ">Track all project activities including task creation, updates, status changes, member assignments,
            comments, and file uploads. Monitor progress with detailed activity logs and status history.</p>
        </div>

        <!-- Notifications & Updates -->
        <div :class=" [
          isDark ? 'bg-slate-800 border border-slate-700' : 'bg-white border border-gray-200',
          'rounded-lg shadow p-6 transition-all duration-300 hover:shadow-lg'
        ] ">
          <div class="flex items-center mb-4">
            <div :class=" [
              isDark ? 'bg-rose-600' : 'bg-red-500',
              'w-10 h-10 rounded-lg flex items-center justify-center mr-4 transition-all duration-300'
            ] ">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z">
                </path>
              </svg>
            </div>
            <h3 :class=" [
              isDark ? 'text-slate-100' : 'text-gray-900',
              'text-lg font-semibold transition-colors duration-300'
            ] ">Automated Email Notifications</h3>
          </div>
          <p :class=" [
            isDark ? 'text-slate-300' : 'text-gray-600',
            'text-sm leading-relaxed transition-colors duration-300'
          ] ">Stay updated with automated email notifications for task assignments, comment mentions, member
            invitations, and project updates. Powered by Celery for reliable background processing.</p>
        </div>

        <!-- Flexible Workflow -->
        <div :class=" [
          isDark ? 'bg-slate-800 border border-slate-700' : 'bg-white border border-gray-200',
          'rounded-lg shadow p-6 transition-all duration-300 hover:shadow-lg'
        ] ">
          <div class="flex items-center mb-4">
            <div :class=" [
              isDark ? 'bg-indigo-600' : 'bg-indigo-500',
              'w-10 h-10 rounded-lg flex items-center justify-center mr-4 transition-all duration-300'
            ] ">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z">
                </path>
              </svg>
            </div>
            <h3 :class=" [
              isDark ? 'text-slate-100' : 'text-gray-900',
              'text-lg font-semibold transition-colors duration-300'
            ] ">Custom Status Management</h3>
          </div>
          <p :class=" [
            isDark ? 'text-slate-300' : 'text-gray-600',
            'text-sm leading-relaxed transition-colors duration-300'
          ] ">Create custom task statuses specific to your organization with positioning and default settings.
            Configure flexible workflows that match your team's processes and track status changes over time.</p>
        </div>
      </div>

      <!-- Getting Started Section -->
      <div :class=" [
        isDark ? 'bg-slate-800 border border-slate-700' : 'bg-white border border-gray-200',
        'rounded-lg shadow p-8 mb-8 transition-all duration-300'
      ] ">
        <div class="text-center mb-8">
          <h2 :class=" [
            isDark ? 'text-slate-100' : 'text-gray-900',
            'text-2xl font-bold mb-4 transition-colors duration-300'
          ] ">Key PMS Features You Get</h2>
          <p :class=" [
            isDark ? 'text-slate-300' : 'text-gray-600',
            'text-lg max-w-2xl mx-auto mb-8 transition-colors duration-300'
          ] ">TrackTools provides comprehensive project management capabilities designed for modern organizational
            workflows.</p>
        </div>

        <!-- PMS Feature Highlights -->
        <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div :class=" [
            isDark ? 'bg-slate-700 border border-slate-600' : 'bg-blue-50 border border-blue-200',
            'rounded-lg p-4 text-center transition-all duration-300'
          ] ">
            <div :class=" [
              isDark ? 'text-cyan-400' : 'text-blue-600',
              'text-2xl font-bold mb-1 transition-colors duration-300'
            ] ">Multi-Level</div>
            <div :class=" [
              isDark ? 'text-slate-300' : 'text-gray-700',
              'text-sm transition-colors duration-300'
            ] ">Organization → Project → Task Structure</div>
          </div>

          <div :class=" [
            isDark ? 'bg-slate-700 border border-slate-600' : 'bg-green-50 border border-green-200',
            'rounded-lg p-4 text-center transition-all duration-300'
          ] ">
            <div :class=" [
              isDark ? 'text-emerald-400' : 'text-green-600',
              'text-2xl font-bold mb-1 transition-colors duration-300'
            ] ">3 Priority Levels</div>
            <div :class=" [
              isDark ? 'text-slate-300' : 'text-gray-700',
              'text-sm transition-colors duration-300'
            ] ">High, Medium, Low Priority Tasks</div>
          </div>

          <div :class=" [
            isDark ? 'bg-slate-700 border border-slate-600' : 'bg-purple-50 border border-purple-200',
            'rounded-lg p-4 text-center transition-all duration-300'
          ] ">
            <div :class=" [
              isDark ? 'text-violet-400' : 'text-purple-600',
              'text-2xl font-bold mb-1 transition-colors duration-300'
            ] ">Role-Based</div>
            <div :class=" [
              isDark ? 'text-slate-300' : 'text-gray-700',
              'text-sm transition-colors duration-300'
            ] ">Project & Organization Permissions</div>
          </div>

          <div :class=" [
            isDark ? 'bg-slate-700 border border-slate-600' : 'bg-orange-50 border border-orange-200',
            'rounded-lg p-4 text-center transition-all duration-300'
          ] ">
            <div :class=" [
              isDark ? 'text-amber-400' : 'text-orange-600',
              'text-2xl font-bold mb-1 transition-colors duration-300'
            ] ">Email Alerts</div>
            <div :class=" [
              isDark ? 'text-slate-300' : 'text-gray-700',
              'text-sm transition-colors duration-300'
            ] ">Assignment, Mentions & Updates</div>
          </div>
        </div>

        <div class="text-center mb-8">
          <h2 :class=" [
            isDark ? 'text-slate-100' : 'text-gray-900',
            'text-2xl font-bold mb-4 transition-colors duration-300'
          ] ">Get Started with TrackTools</h2>
          <p :class=" [
            isDark ? 'text-slate-300' : 'text-gray-600',
            'text-lg max-w-2xl mx-auto transition-colors duration-300'
          ] ">Follow these simple steps to begin organizing your projects and maximizing your team's productivity.</p>
        </div>

        <div class="grid md:grid-cols-3 gap-8">
          <div class="text-center">
            <div :class=" [
              isDark ? 'bg-cyan-900 border border-cyan-600' : 'bg-blue-100 border border-blue-200',
              'w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 transition-all duration-300'
            ] ">
              <span :class=" [
                isDark ? 'text-cyan-300' : 'text-blue-600',
                'text-2xl font-bold transition-colors duration-300'
              ] ">1</span>
            </div>
            <h3 :class=" [
              isDark ? 'text-slate-100' : 'text-gray-900',
              'text-lg font-semibold mb-2 transition-colors duration-300'
            ] ">Create Your First Project</h3>
            <p :class=" [
              isDark ? 'text-slate-400' : 'text-gray-600',
              'text-sm transition-colors duration-300'
            ] ">Start by creating a project and defining its scope, objectives, and timeline.</p>
          </div>

          <div class="text-center">
            <div :class=" [
              isDark ? 'bg-emerald-900 border border-emerald-600' : 'bg-green-100 border border-green-200',
              'w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 transition-all duration-300'
            ] ">
              <span :class=" [
                isDark ? 'text-emerald-300' : 'text-green-600',
                'text-2xl font-bold transition-colors duration-300'
              ] ">2</span>
            </div>
            <h3 :class=" [
              isDark ? 'text-slate-100' : 'text-gray-900',
              'text-lg font-semibold mb-2 transition-colors duration-300'
            ] ">Invite Team Members</h3>
            <p :class=" [
              isDark ? 'text-slate-400' : 'text-gray-600',
              'text-sm transition-colors duration-300'
            ] ">Add your team members and assign roles to enable collaborative project management.</p>
          </div>

          <div class="text-center">
            <div :class=" [
              isDark ? 'bg-violet-900 border border-violet-600' : 'bg-purple-100 border border-purple-200',
              'w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 transition-all duration-300'
            ] ">
              <span :class=" [
                isDark ? 'text-violet-300' : 'text-purple-600',
                'text-2xl font-bold transition-colors duration-300'
              ] ">3</span>
            </div>
            <h3 :class=" [
              isDark ? 'text-slate-100' : 'text-gray-900',
              'text-lg font-semibold mb-2 transition-colors duration-300'
            ] ">Create & Assign Tasks</h3>
            <p :class=" [
              isDark ? 'text-slate-400' : 'text-gray-600',
              'text-sm transition-colors duration-300'
            ] ">Break down your project into tasks and assign them to team members with clear deadlines.</p>
          </div>
        </div>
      </div>

      <!-- Current Status -->
      <div :class=" [
        isDark ? 'bg-gradient-to-r from-slate-800 to-slate-700 border border-slate-600' : 'bg-gradient-to-r from-gray-50 to-blue-50 border border-gray-200',
        'rounded-lg shadow p-6 text-center transition-all duration-300'
      ] ">
        <h3 :class=" [
          isDark ? 'text-slate-100' : 'text-gray-900',
          'text-xl font-semibold mb-3 transition-colors duration-300'
        ] ">Ready to Transform Your Project Management?</h3>
        <p :class=" [
          isDark ? 'text-slate-300' : 'text-gray-700',
          'mb-6 transition-colors duration-300'
        ] ">You're all set up and ready to create your first project. Start organizing your work and experience the
          power of effective task management.</p>

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