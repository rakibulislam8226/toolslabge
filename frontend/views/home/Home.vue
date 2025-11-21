<template>
  <div :class="[
    isDark ? 'bg-slate-900 text-slate-100' : 'bg-white text-slate-900',
    'min-h-screen transition-all duration-300'
  ]">
    <!-- Hero Section -->
    <div :class="[
      isDark ? 'bg-gradient-to-br from-slate-800 to-slate-900' : 'bg-gradient-to-br from-blue-50 to-indigo-100',
      'transition-all duration-300'
    ]">
      <div class="container mx-auto px-6 py-16">
        <div class="text-center">
          <h1 :class="[
            isDark ? 'text-slate-100' : 'text-gray-800',
            'text-5xl font-bold mb-6 transition-colors duration-300'
          ]">
            Welcome to <span :class="[
              isDark ? 'text-cyan-400' : 'text-blue-600',
              'transition-colors duration-300'
            ]">TrackTools</span>
          </h1>
          <p :class="[
            isDark ? 'text-slate-300' : 'text-gray-600',
            'text-xl mb-8 max-w-2xl mx-auto transition-colors duration-300'
          ]">
            Streamline your organization's workflow with our powerful project management and tracking solution.
            Get started today and transform how your organization collaborates.
          </p>

          <div class="space-y-4 sm:space-y-0 sm:space-x-4 sm:flex sm:justify-center">
            <router-link to="/register" :class="[
              isDark
                ? 'bg-cyan-600 hover:bg-cyan-700 text-white'
                : 'bg-blue-600 hover:bg-blue-700 text-white',
              'inline-block px-8 py-3 rounded-lg font-semibold transition-all duration-300 shadow-lg'
            ]">
              Create Your Organization
            </router-link>
            <router-link to="/login" :class="[
              isDark
                ? 'border border-cyan-400 text-cyan-400 hover:bg-slate-800'
                : 'border border-blue-600 text-blue-600 hover:bg-blue-50',
              'inline-block px-8 py-3 rounded-lg font-semibold transition-all duration-300'
            ]">
              Already have an account? Login
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div :class="[
      isDark ? 'bg-slate-800' : 'bg-white',
      'py-16 transition-all duration-300'
    ]">
      <div class="container mx-auto px-6">
        <h2 :class="[
          isDark ? 'text-slate-100' : 'text-gray-800',
          'text-3xl font-bold text-center mb-12 transition-colors duration-300'
        ]">
          Why Choose TrackTools?
        </h2>

        <div class="grid md:grid-cols-3 gap-8">
          <div class="text-center p-6">
            <div :class="[
              isDark ? 'bg-cyan-900' : 'bg-blue-100',
              'w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 transition-all duration-300'
            ]">
              <svg :class="[
                isDark ? 'text-cyan-400' : 'text-blue-600',
                'w-8 h-8 transition-colors duration-300'
              ]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z">
                </path>
              </svg>
            </div>
            <h3 :class="[
              isDark ? 'text-slate-100' : 'text-gray-900',
              'text-xl font-semibold mb-2 transition-colors duration-300'
            ]">Project Management</h3>
            <p :class="[
              isDark ? 'text-slate-300' : 'text-gray-600',
              'transition-colors duration-300'
            ]">Organize and track your projects with ease. Monitor progress and deadlines efficiently.</p>
          </div>

          <div class="text-center p-6">
            <div :class="[
              isDark ? 'bg-emerald-900' : 'bg-green-100',
              'w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 transition-all duration-300'
            ]">
              <svg :class="[
                isDark ? 'text-emerald-400' : 'text-green-600',
                'w-8 h-8 transition-colors duration-300'
              ]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z">
                </path>
              </svg>
            </div>
            <h3 :class="[
              isDark ? 'text-slate-100' : 'text-gray-900',
              'text-xl font-semibold mb-2 transition-colors duration-300'
            ]">Organization Collaboration</h3>
            <p :class="[
              isDark ? 'text-slate-300' : 'text-gray-600',
              'transition-colors duration-300'
            ]">Connect your organization members and enhance collaboration with real-time updates.</p>
          </div>

          <div class="text-center p-6">
            <div :class="[
              isDark ? 'bg-violet-900' : 'bg-purple-100',
              'w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 transition-all duration-300'
            ]">
              <svg :class="[
                isDark ? 'text-violet-400' : 'text-purple-600',
                'w-8 h-8 transition-colors duration-300'
              ]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <h3 :class="[
              isDark ? 'text-slate-100' : 'text-gray-900',
              'text-xl font-semibold mb-2 transition-colors duration-300'
            ]">Task Tracking</h3>
            <p :class="[
              isDark ? 'text-slate-300' : 'text-gray-600',
              'transition-colors duration-300'
            ]">Keep track of tasks, assignments, and deliverables with our intuitive system.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- CTA Section -->
    <div :class="[
      isDark ? 'bg-slate-700' : 'bg-blue-600',
      'py-16 transition-all duration-300'
    ]">
      <div class="container mx-auto px-6 text-center">
        <h2 class="text-3xl font-bold text-white mb-4">
          Ready to Get Started?
        </h2>
        <p :class="[
          isDark ? 'text-slate-200' : 'text-blue-100',
          'mb-8 max-w-2xl mx-auto transition-colors duration-300'
        ]">
          Join thousands of organizations already using TrackTools to streamline their operations and boost productivity.
        </p>
        <div class="space-y-4 sm:space-y-0 sm:space-x-4 sm:flex sm:justify-center">
          <router-link to="/register" :class="[
            isDark
              ? 'bg-cyan-500 text-slate-900 hover:bg-cyan-400'
              : 'bg-white text-blue-600 hover:bg-gray-100',
            'inline-block px-8 py-3 rounded-lg font-semibold transition-all duration-300 shadow-lg'
          ]">
            Start Your Free Organization
          </router-link>
          <router-link to="/login"
            class="inline-block border border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-black hover:bg-opacity-10 transition-all duration-300">
            Login to Existing Account
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useTheme } from '@/composables/useTheme.js'

const { isDark } = useTheme()
</script>

<style scoped>
/* Optional: make container max width responsive */
</style>
