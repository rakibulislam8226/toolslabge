<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
    <!-- Hero Section -->
    <div class="container mx-auto px-6 py-16">
      <div class="text-center">
        <h1 class="text-5xl font-bold text-gray-800 mb-6">
          Welcome to <span class="text-blue-600">BaseTrack</span>
        </h1>
        <p class="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Streamline your organization's workflow with our powerful project management and tracking solution. 
          Get started today and transform how your organization collaborates.
        </p>
        
        <div class="space-y-4 sm:space-y-0 sm:space-x-4 sm:flex sm:justify-center">
          <router-link 
            to="/register" 
            class="inline-block bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition duration-300 shadow-lg"
          >
            Create Your Organization
          </router-link>
          <router-link 
            to="/login" 
            class="inline-block border border-blue-600 text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition duration-300"
          >
            Already have an account? Login
          </router-link>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div class="bg-white py-16">
      <div class="container mx-auto px-6">
        <h2 class="text-3xl font-bold text-center text-gray-800 mb-12">
          Why Choose BaseTrack?
        </h2>
        
        <div class="grid md:grid-cols-3 gap-8">
          <div class="text-center p-6">
            <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2">Project Management</h3>
            <p class="text-gray-600">Organize and track your projects with ease. Monitor progress and deadlines efficiently.</p>
          </div>
          
          <div class="text-center p-6">
            <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2">Organization Collaboration</h3>
            <p class="text-gray-600">Connect your organization members and enhance collaboration with real-time updates.</p>
          </div>
          
          <div class="text-center p-6">
            <div class="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2">Task Tracking</h3>
            <p class="text-gray-600">Keep track of tasks, assignments, and deliverables with our intuitive system.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- CTA Section -->
    <div class="bg-blue-600 py-16">
      <div class="container mx-auto px-6 text-center">
        <h2 class="text-3xl font-bold text-white mb-4">
          Ready to Get Started?
        </h2>
        <p class="text-blue-100 mb-8 max-w-2xl mx-auto">
          Join thousands of organizations already using BaseTrack to streamline their operations and boost productivity.
        </p>
        <div class="space-y-4 sm:space-y-0 sm:space-x-4 sm:flex sm:justify-center">
          <router-link 
            to="/register" 
            class="inline-block bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition duration-300 shadow-lg"
          >
            Start Your Free Organization
          </router-link>
          <router-link 
            to="/login" 
            class="inline-block border border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition duration-300"
          >
            Login to Existing Account
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// This is now just an informational landing page
// No form logic needed here
</script>

<style scoped>
/* Optional: make container max width responsive */
</style>
