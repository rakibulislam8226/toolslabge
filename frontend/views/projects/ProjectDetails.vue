<template>
  <div :class=" [
    isDark ? 'bg-slate-900' : 'bg-gray-50',
    'min-h-screen transition-colors duration-300'
  ] ">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-24">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      <span :class=" [
        isDark ? 'text-slate-300' : 'text-gray-600',
        'ml-3 transition-colors duration-300'
      ] ">Loading project details...</span>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div :class=" [
        isDark ? 'bg-red-900/20 border-red-800/30' : 'bg-red-50 border-red-200',
        'border rounded-lg p-6 text-center transition-colors duration-300'
      ] ">
        <svg :class=" [
          isDark ? 'text-red-400' : 'text-red-400',
          'w-12 h-12 mx-auto mb-4'
        ] " fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <h3 :class=" [
          isDark ? 'text-red-300' : 'text-red-800',
          'text-lg font-semibold mb-2 transition-colors duration-300'
        ] ">Failed to load project</h3>
        <p :class=" [
          isDark ? 'text-red-400' : 'text-red-600',
          'mb-4 transition-colors duration-300'
        ] ">{{ error }}</p>
        <div class="space-x-3">
          <Button variant="danger" size="md" label="Try Again" @click=" fetchProject " />
          <router-link to="/projects" :class=" [
            isDark ? 'bg-slate-600 hover:bg-slate-700 text-white' : 'bg-gray-600 hover:bg-gray-700 text-white',
            'px-4 py-2 rounded-lg transition duration-300 inline-block'
          ] ">
            Back to Projects
          </router-link>
        </div>
      </div>
    </div>

    <!-- Project Details Content -->
    <div v-else-if="project" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-6 lg:py-8">
      <!-- Header Section -->
      <!-- Header Section -->
      <div :class=" [
        isDark ? 'bg-slate-800 border-slate-700' : 'bg-white border-gray-200',
        'rounded-xl shadow-lg border mb-6 sm:mb-8 overflow-hidden transition-colors duration-300'
      ] ">
        <div :class=" [
          isDark ? 'border-slate-700' : 'border-gray-200',
          'px-4 sm:px-6 py-4 sm:py-6 border-b transition-colors duration-300'
        ] ">
          <div class="flex flex-col lg:flex-row lg:items-start lg:justify-between space-y-4 lg:space-y-0">
            <div class="flex-1 lg:mr-6">
              <!-- Breadcrumb -->
              <nav class="mb-3 sm:mb-4">
                <ol :class=" [
                  isDark ? 'text-slate-400' : 'text-gray-500',
                  'flex items-center space-x-2 text-sm transition-colors duration-300'
                ] ">
                  <li>
                    <router-link to="/projects" :class=" [
                      isDark ? 'hover:text-cyan-400' : 'hover:text-blue-600',
                      'transition duration-300 font-medium'
                    ] ">
                      Projects
                    </router-link>
                  </li>
                  <li>
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                    </svg>
                  </li>
                  <li :class=" [
                    isDark ? 'text-slate-100' : 'text-gray-900',
                    'font-semibold truncate transition-colors duration-300'
                  ] ">{{ project.name }}</li>
                </ol>
              </nav>

              <!-- Project Title and Status -->
              <div class="flex flex-col sm:flex-row sm:items-center mb-3 sm:mb-4 space-y-2 sm:space-y-0">
                <h1 :class=" [
                  isDark ? 'text-slate-100' : 'text-gray-900',
                  'text-2xl sm:text-3xl lg:text-4xl font-bold sm:mr-4 leading-tight transition-colors duration-300'
                ] ">
                  {{ project.name }}
                </h1>
                <span :class=" getStatusBadgeClass(project.status) "
                  class="px-3 py-1.5 text-sm font-semibold rounded-full self-start shadow-sm">
                  {{ formatStatus(project.status) }}
                </span>
              </div>

              <!-- Project Description -->
              <p :class=" [
                isDark ? 'text-slate-300' : 'text-gray-600',
                'text-base sm:text-lg leading-relaxed max-w-3xl transition-colors duration-300'
              ] ">
                {{ project.description || 'No description available for this project.' }}
              </p>
            </div>

            <!-- Action Buttons -->
            <div
              class="flex flex-col sm:flex-row items-stretch sm:items-center space-y-2 sm:space-y-0 sm:space-x-3 lg:flex-shrink-0">
              <Button v-if="hasRole('owner', 'admin', 'manager')" @click=" editProject " variant="primary" size="md"
                :class=" [
                  isDark ? 'bg-cyan-600 hover:bg-cyan-700' : 'bg-blue-600 hover:bg-blue-700',
                  'px-4 py-2.5 rounded-lg transition-all duration-300 flex items-center justify-center shadow-md hover:shadow-lg transform hover:-translate-y-0.5 cursor-pointer text-white'
                ] " label="Edit Project">
                <template #prepend>
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="white" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z">
                    </path>
                  </svg>
                </template>
              </Button>
              <router-link :to=" `/projects/${ project.slug }/tasks` " :class=" [
                isDark ? 'bg-violet-600 hover:bg-violet-700' : 'bg-indigo-600 hover:bg-indigo-700',
                'px-4 py-2.5 rounded-lg transition-all duration-300 flex items-center justify-center shadow-md hover:shadow-lg transform hover:-translate-y-0.5 text-white'
              ] ">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="white" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z">
                  </path>
                </svg>
                <span class="font-medium text-white">View Tasks</span>
              </router-link>
            </div>
          </div>
        </div>

        <!-- Project Stats -->
        <div :class=" [
          isDark ? 'bg-slate-700/50' : 'bg-gray-50',
          'px-4 sm:px-6 py-4 sm:py-6 transition-colors duration-300'
        ] ">
          <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
            <!-- Tasks -->
            <div :class=" [
              isDark ? 'bg-slate-800 border-slate-700 hover:bg-slate-700/80' : 'bg-white border-gray-100 hover:shadow-md',
              'text-center p-4 rounded-xl shadow-sm border transition-all duration-300 transform hover:-translate-y-1'
            ] ">
              <div :class=" [
                isDark ? 'bg-blue-900/50' : 'bg-gradient-to-br from-blue-100 to-blue-200',
                'w-14 h-14 rounded-2xl flex items-center justify-center mx-auto mb-3 shadow-sm transition-colors duration-300'
              ] ">
                <svg :class=" [
                  isDark ? 'text-blue-400' : 'text-blue-600',
                  'w-7 h-7 transition-colors duration-300'
                ] " fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <p :class=" [
                isDark ? 'text-slate-100' : 'text-gray-900',
                'text-2xl sm:text-3xl font-bold mb-1 transition-colors duration-300'
              ] ">{{ project.total_tasks }}</p>
              <p :class=" [
                isDark ? 'text-slate-400' : 'text-gray-600',
                'text-sm font-medium transition-colors duration-300'
              ] ">Tasks</p>
            </div>

            <!-- Members -->
            <div :class=" [
              isDark ? 'bg-slate-800 border-slate-700 hover:bg-slate-700/80' : 'bg-white border-gray-100 hover:shadow-md',
              'text-center p-4 rounded-xl shadow-sm border transition-all duration-300 transform hover:-translate-y-1'
            ] ">
              <div :class=" [
                isDark ? 'bg-green-900/50' : 'bg-gradient-to-br from-green-100 to-green-200',
                'w-14 h-14 rounded-2xl flex items-center justify-center mx-auto mb-3 shadow-sm transition-colors duration-300'
              ] ">
                <svg :class=" [
                  isDark ? 'text-green-400' : 'text-green-600',
                  'w-7 h-7 transition-colors duration-300'
                ] " fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-2.239"></path>
                </svg>
              </div>
              <p :class=" [
                isDark ? 'text-slate-100' : 'text-gray-900',
                'text-2xl sm:text-3xl font-bold mb-1 transition-colors duration-300'
              ] ">{{ project.total_members }}</p>
              <p :class=" [
                isDark ? 'text-slate-400' : 'text-gray-600',
                'text-sm font-medium transition-colors duration-300'
              ] ">Members</p>
            </div>

            <!-- Progress -->
            <div :class=" [
              isDark ? 'bg-slate-800 border-slate-700 hover:bg-slate-700/80' : 'bg-white border-gray-100 hover:shadow-md',
              'text-center p-4 rounded-xl shadow-sm border transition-all duration-300 transform hover:-translate-y-1'
            ] ">
              <div :class=" [
                isDark ? 'bg-purple-900/50' : 'bg-gradient-to-br from-purple-100 to-purple-200',
                'w-14 h-14 rounded-2xl flex items-center justify-center mx-auto mb-3 shadow-sm transition-colors duration-300'
              ] ">
                <svg :class=" [
                  isDark ? 'text-purple-400' : 'text-purple-600',
                  'w-7 h-7 transition-colors duration-300'
                ] " fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z">
                  </path>
                </svg>
              </div>
              <p :class=" [
                isDark ? 'text-slate-100' : 'text-gray-900',
                'text-2xl sm:text-3xl font-bold mb-1 transition-colors duration-300'
              ] ">{{ getStaticProgress(project) }}%</p>
              <p :class=" [
                isDark ? 'text-slate-400' : 'text-gray-600',
                'text-sm font-medium transition-colors duration-300'
              ] ">Complete</p>
            </div>

            <!-- Status Days -->
            <div :class=" [
              isDark ? 'bg-slate-800 border-slate-700 hover:bg-slate-700/80' : 'bg-white border-gray-100 hover:shadow-md',
              'text-center p-4 rounded-xl shadow-sm border transition-all duration-300 transform hover:-translate-y-1 col-span-2 lg:col-span-1'
            ] ">
              <div :class=" [
                isDark ? 'bg-amber-900/50' : 'bg-gradient-to-br from-amber-100 to-amber-200',
                'w-14 h-14 rounded-2xl flex items-center justify-center mx-auto mb-3 shadow-sm transition-colors duration-300'
              ] ">
                <svg :class=" [
                  isDark ? 'text-amber-400' : 'text-amber-600',
                  'w-7 h-7 transition-colors duration-300'
                ] " fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <p :class=" [
                isDark ? 'text-slate-100' : 'text-gray-900',
                'text-2xl sm:text-3xl font-bold mb-1 transition-colors duration-300'
              ] ">{{ getDaysRemaining() }}</p>
              <p :class=" [
                isDark ? 'text-slate-400' : 'text-gray-600',
                'text-sm font-medium transition-colors duration-300'
              ] ">{{ getDaysLabel() }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Project Dates and Details -->
      <div class="grid lg:grid-cols-2 gap-6 sm:gap-8 mb-6 sm:mb-8">
        <!-- Project Timeline -->
        <div :class=" [
          isDark ? 'bg-slate-800 border-slate-700' : 'bg-white border-gray-200',
          'rounded-xl shadow-lg border p-4 sm:p-6 hover:shadow-xl transition-all duration-300'
        ] ">
          <h2 :class=" [
            isDark ? 'text-slate-100' : 'text-gray-900',
            'text-xl sm:text-2xl font-bold mb-4 sm:mb-6 flex items-center transition-colors duration-300'
          ] ">
            <div :class=" [
              isDark ? 'bg-cyan-600' : 'bg-gradient-to-br from-blue-500 to-blue-600',
              'w-8 h-8 rounded-lg flex items-center justify-center mr-3 shadow-sm transition-colors duration-300'
            ] ">
              <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
              </svg>
            </div>
            Project Timeline
          </h2>

          <div class="space-y-4">
            <div :class=" [
              isDark ? 'bg-slate-700/50 border-slate-600' : 'bg-white border-gray-200',
              'flex flex-col sm:flex-row sm:justify-between sm:items-center p-4 rounded-xl border shadow-sm transition-colors duration-300'
            ] ">
              <span :class=" [
                isDark ? 'text-slate-300' : 'text-gray-600',
                'font-medium mb-1 sm:mb-0 transition-colors duration-300'
              ] ">Start Date</span>
              <span :class=" [
                isDark ? 'text-slate-100' : 'text-gray-900',
                'font-semibold text-sm sm:text-base transition-colors duration-300'
              ] ">
                {{ project.start_date ? formatDate(project.start_date) : 'Not set' }}
              </span>
            </div>

            <div :class=" [
              isDark ? 'bg-slate-700/50 border-slate-600' : 'bg-white border-gray-200',
              'flex flex-col sm:flex-row sm:justify-between sm:items-center p-4 rounded-xl border shadow-sm transition-colors duration-300'
            ] ">
              <span :class=" [
                isDark ? 'text-slate-300' : 'text-gray-600',
                'font-medium mb-1 sm:mb-0 transition-colors duration-300'
              ] ">End Date</span>
              <span :class=" [
                isDark ? 'text-slate-100' : 'text-gray-900',
                'font-semibold text-sm sm:text-base transition-colors duration-300'
              ] ">
                {{ project.end_date ? formatDate(project.end_date) : 'Not set' }}
              </span>
            </div>

            <!-- Progress Bar -->
            <div :class=" [
              isDark ? 'bg-slate-700/50 border-slate-600' : 'bg-white border-gray-200',
              'mt-6 p-4 rounded-xl border shadow-sm transition-colors duration-300'
            ] ">
              <div :class=" [
                isDark ? 'text-slate-300' : 'text-gray-700',
                'flex justify-between text-sm font-medium mb-3 transition-colors duration-300'
              ] ">
                <span>Overall Progress</span>
                <span :class=" [
                  isDark ? 'text-cyan-400' : 'text-blue-600',
                  'font-bold transition-colors duration-300'
                ] ">{{ getStaticProgress(project) }}%</span>
              </div>
              <div :class=" [
                isDark ? 'bg-slate-600' : 'bg-gray-200',
                'w-full rounded-full h-4 shadow-inner transition-colors duration-300'
              ] ">
                <div :class=" [
                  isDark ? 'bg-gradient-to-r from-cyan-500 via-cyan-600 to-cyan-700' : 'bg-gradient-to-r from-blue-500 via-blue-600 to-blue-700',
                  'h-4 rounded-full transition-all duration-700 shadow-sm'
                ] " :style=" { width: `${ getStaticProgress(project) }%` } "></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Project Information -->
        <div :class=" [
          isDark ? 'bg-slate-800 border-slate-700' : 'bg-white border-gray-200',
          'rounded-xl shadow-lg border p-4 sm:p-6 hover:shadow-xl transition-all duration-300'
        ] ">
          <h2 :class=" [
            isDark ? 'text-slate-100' : 'text-gray-900',
            'text-xl sm:text-2xl font-bold mb-4 sm:mb-6 flex items-center transition-colors duration-300'
          ] ">
            <div :class=" [
              isDark ? 'bg-violet-600' : 'bg-gradient-to-br from-indigo-500 to-indigo-600',
              'w-8 h-8 rounded-lg flex items-center justify-center mr-3 shadow-sm transition-colors duration-300'
            ] ">
              <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            Project Information
          </h2>

          <div class="space-y-4">
            <div :class=" [
              isDark ? 'bg-slate-700/50 border-slate-600' : 'bg-white border-gray-200',
              'flex flex-col sm:flex-row sm:justify-between sm:items-center p-4 rounded-xl border shadow-sm transition-colors duration-300'
            ] ">
              <span :class=" [
                isDark ? 'text-slate-300' : 'text-gray-600',
                'font-medium mb-1 sm:mb-0 transition-colors duration-300'
              ] ">Project Manager</span>
              <span :class=" [
                isDark ? 'text-slate-100' : 'text-gray-900',
                'font-semibold text-sm sm:text-base break-words transition-colors duration-300'
              ] ">
                <template v-if="project?.manager">
                  <span v-if="project.manager.first_name && project.manager.last_name">
                    {{ project.manager.first_name }} {{ project.manager.last_name }}
                  </span>
                  <span v-else>
                    {{ project.manager.email }}
                  </span>
                </template>
                <span v-else :class=" [
                  isDark ? 'text-slate-400' : 'text-gray-500',
                  'italic transition-colors duration-300'
                ] ">No manager assigned</span>
              </span>
            </div>

            <div :class=" [
              isDark ? 'bg-slate-700/50 border-slate-600' : 'bg-white border-gray-200',
              'flex flex-col sm:flex-row sm:justify-between sm:items-center p-4 rounded-xl border shadow-sm transition-colors duration-300'
            ] ">
              <span :class=" [
                isDark ? 'text-slate-300' : 'text-gray-600',
                'font-medium mb-2 sm:mb-0 transition-colors duration-300'
              ] ">Status</span>
              <span :class=" getStatusBadgeClass(project.status) "
                class="px-3 py-1.5 text-sm font-semibold rounded-full shadow-sm self-start sm:self-center">
                {{ formatStatus(project.status) }}
              </span>
            </div>

            <div :class=" [
              isDark ? 'bg-slate-700/50 border-slate-600' : 'bg-white border-gray-200',
              'flex flex-col sm:flex-row sm:justify-between sm:items-center p-4 rounded-xl border shadow-sm transition-colors duration-300'
            ] ">
              <span :class=" [
                isDark ? 'text-slate-300' : 'text-gray-600',
                'font-medium mb-1 sm:mb-0 transition-colors duration-300'
              ] ">Created</span>
              <span :class=" [
                isDark ? 'text-slate-100' : 'text-gray-900',
                'font-semibold text-sm sm:text-base transition-colors duration-300'
              ] ">
                {{ project.created_at ? formatDate(project.created_at) : 'Unknown' }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Placeholder sections for future features -->
      <div class="grid lg:grid-cols-2 gap-6 sm:gap-8">
        <!-- Recent Tasks -->
        <div :class=" [
          isDark ? 'bg-slate-800 border-slate-700' : 'bg-white border-gray-200',
          'rounded-xl shadow-lg border p-4 sm:p-6 hover:shadow-xl transition-all duration-300'
        ] ">
          <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-4 sm:mb-6 space-y-2 sm:space-y-0">
            <h2 :class=" [
              isDark ? 'text-slate-100' : 'text-gray-900',
              'text-xl sm:text-2xl font-bold flex items-center transition-colors duration-300'
            ] ">
              <div :class=" [
                isDark ? 'bg-emerald-600' : 'bg-gradient-to-br from-green-500 to-green-600',
                'w-8 h-8 rounded-lg flex items-center justify-center mr-3 shadow-sm transition-colors duration-300'
              ] ">
                <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2">
                  </path>
                </svg>
              </div>
              Recent Tasks
            </h2>
            <button @click=" viewAllTasks " :class=" [
              isDark ? 'text-emerald-400 hover:text-emerald-300' : 'text-green-600 hover:text-green-800',
              'text-md font-semibold transition-colors duration-200 hover:underline self-start sm:self-center'
            ] ">
              View All →
            </button>
          </div>
          <div :class=" [
            isDark ? 'text-slate-400' : 'text-gray-500',
            'text-center py-8 sm:py-12 transition-colors duration-300'
          ] ">
            <div :class=" [
              isDark ? 'bg-emerald-900/50' : 'bg-gradient-to-br from-green-100 to-green-200',
              'w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-sm transition-colors duration-300'
            ] ">
              <svg :class=" [
                isDark ? 'text-emerald-400' : 'text-green-600',
                'w-8 h-8 transition-colors duration-300'
              ] " fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2">
                </path>
              </svg>
            </div>
            <p :class=" [
              isDark ? 'text-slate-300' : 'text-gray-600',
              'font-medium mb-4 transition-colors duration-300'
            ] ">Tasks will be displayed here</p>
            <Button @click=" viewAllTasks " :class=" [
              isDark ? 'bg-emerald-600 hover:bg-emerald-700' : 'bg-green-600 hover:bg-green-700',
              'px-6 py-3 rounded-xl transition-all duration-300 font-semibold shadow-md hover:shadow-lg transform hover:-translate-y-0.5 text-white'
            ] ">
              View Tasks
            </Button>
          </div>
        </div>

        <!-- Project Members -->
        <div :class=" [
          isDark ? 'bg-slate-800 border-slate-700' : 'bg-white border-gray-200',
          'rounded-xl shadow-lg border p-4 sm:p-6 hover:shadow-xl transition-all duration-300'
        ] ">
          <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-4 sm:mb-6 space-y-2 sm:space-y-0">
            <h2 :class=" [
              isDark ? 'text-slate-100' : 'text-gray-900',
              'text-xl sm:text-2xl font-bold flex items-center transition-colors duration-300'
            ] ">
              <div :class=" [
                isDark ? 'bg-violet-600' : 'bg-gradient-to-br from-purple-500 to-purple-600',
                'w-8 h-8 rounded-lg flex items-center justify-center mr-3 shadow-sm transition-colors duration-300'
              ] ">
                <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-2.239"></path>
                </svg>
              </div>
              Project Members
            </h2>
            <button @click=" manageMembers " :class=" [
              isDark ? 'text-violet-400 hover:text-violet-300' : 'text-purple-600 hover:text-purple-800',
              'text-md font-semibold transition-colors duration-200 hover:underline self-start sm:self-center'
            ] ">
              Manage →
            </button>
          </div>
          <div :class=" [
            isDark ? 'text-slate-400' : 'text-gray-500',
            'text-center py-8 sm:py-12 transition-colors duration-300'
          ] ">
            <div :class=" [
              isDark ? 'bg-violet-900/50' : 'bg-gradient-to-br from-purple-100 to-purple-200',
              'w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-sm transition-colors duration-300'
            ] ">
              <svg :class=" [
                isDark ? 'text-violet-400' : 'text-purple-600',
                'w-8 h-8 transition-colors duration-300'
              ] " fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-2.239"></path>
              </svg>
            </div>
            <p :class=" [
              isDark ? 'text-slate-300' : 'text-gray-600',
              'font-medium mb-4 transition-colors duration-300'
            ] ">Project members will be displayed here</p>
            <Button @click=" manageMembers " :class=" [
              isDark ? 'bg-violet-600 hover:bg-violet-700' : 'bg-purple-600 hover:bg-purple-700',
              'px-6 py-3 rounded-xl transition-all duration-300 font-semibold shadow-md hover:shadow-lg transform hover:-translate-y-0.5 text-white'
            ] ">
              View Members
            </Button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from "@/plugins/axiosConfig.js"
import Button from '@/components/Button.vue'
import { useAuth } from "@/composables/useAuth.js";
import { useTheme } from '@/composables/useTheme.js';

const { hasRole } = useAuth()
const { isDark } = useTheme()
const router = useRouter()
const route = useRoute()

// Reactive data
const project = ref(null)
const loading = ref(true)
const error = ref('')

// Get project slug from route
const projectSlug = computed(() => route.params.slug)

// Fetch project details from API
const fetchProject = async () => {
  try {
    loading.value = true
    error.value = ''

    const slug = projectSlug.value
    if (!slug) {
      error.value = 'Invalid project URL - missing slug'
      return
    }

    // API call uses backend slug directly: projects/{slug}/
    const response = await axios.get(`projects/${slug}/`)

    // Handle your API response structure
    const projectData = response.data.data || response.data || null
    project.value = projectData

  } catch (err) {
    console.error('Failed to fetch project:', err)
    if (err.response?.status === 404) {
      error.value = 'Project not found'
    } else if (err.response?.status === 401) {
      error.value = 'You need to login to view this project'
    } else if (err.response?.data?.detail) {
      error.value = err.response.data.detail
    } else {
      error.value = 'Failed to load project details. Please try again.'
    }
  } finally {
    loading.value = false
  }
}

const getStaticProgress = (project) => {
  if (project.total_tasks > 0) {
    return Math.round((project.completed_tasks / project.total_tasks) * 100)
  }
  return 0
}

// Get status badge CSS class (same as in ProjectsList)
const getStatusBadgeClass = (status) => {
  const statusLower = (status || 'active').toLowerCase()

  switch (statusLower) {
    case 'active':
      return isDark.value
        ? 'bg-green-900/50 text-green-300 border border-green-700/50'
        : 'bg-green-100 text-green-800'
    case 'completed':
      return isDark.value
        ? 'bg-blue-900/50 text-blue-300 border border-blue-700/50'
        : 'bg-blue-100 text-blue-800'
    case 'on_hold':
    case 'paused':
      return isDark.value
        ? 'bg-yellow-900/50 text-yellow-300 border border-yellow-700/50'
        : 'bg-yellow-100 text-yellow-800'
    case 'cancelled':
      return isDark.value
        ? 'bg-red-900/50 text-red-300 border border-red-700/50'
        : 'bg-red-100 text-red-800'
    default:
      return isDark.value
        ? 'bg-gray-800/50 text-gray-300 border border-gray-600/50'
        : 'bg-gray-100 text-gray-800'
  }
}

// Format status for display
const formatStatus = (status) => {
  if (!status) return 'Active'
  return status.charAt(0).toUpperCase() + status.slice(1).replace('_', ' ')
}

// Format date helper
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// Calculate days remaining or elapsed
const getDaysRemaining = () => {
  if (!project.value?.end_date) return '--'

  const today = new Date()
  const endDate = new Date(project.value.end_date)
  const diffTime = endDate - today
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  return Math.abs(diffDays)
}

const getDaysLabel = () => {
  if (!project.value?.end_date) return 'No deadline'

  const today = new Date()
  const endDate = new Date(project.value.end_date)
  const diffTime = endDate - today

  if (diffTime > 0) {
    return 'Days left'
  } else if (diffTime < 0) {
    return 'Days overdue'
  } else {
    return 'Due today'
  }
}

// Action functions
const editProject = () => {
  const slug = project.value.slug
  router.push(`/projects/${slug}/edit`)
}

const viewAllTasks = () => {
  const slug = project.value.slug
  router.push(`/projects/${slug}/tasks`)
}

const manageMembers = () => {
  const slug = project.value.slug
  router.push({ name: 'projects.members', params: { slug } })
}

// Fetch project on component mount
onMounted(() => {
  fetchProject()
})
</script>

<style scoped>
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}
</style>