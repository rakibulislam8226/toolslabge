<template>
    <BaseModal :is-open=" isOpen " title="Edit Task" size="xxxl" @close=" closeModal ">
        <!-- Loading State -->
        <div v-if="loading" class="flex items-center justify-center py-8">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <span class="ml-2 text-gray-600">Loading task details...</span>
        </div>

        <!-- Main Content - Responsive Layout with Tabs on Mobile -->
        <div v-else class="h-[75vh] flex flex-col">
            <!-- Mobile Tabs (visible only on mobile) -->
            <div class="lg:hidden mb-4">
                <div class="border-b border-gray-200 dark:border-gray-700">
                    <nav class="-mb-px flex space-x-8">
                        <button @click="activeTab = 'edit'" :class=" [
                            'py-2 px-1 border-b-2 font-medium text-sm whitespace-nowrap',
                            activeTab === 'edit'
                                ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
                        ] ">
                            Edit Task
                        </button>
                        <button @click="activeTab = 'comments'" :class=" [
                            'py-2 px-1 border-b-2 font-medium text-sm whitespace-nowrap',
                            activeTab === 'comments'
                                ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
                        ] ">
                            Comments ({{ comments.length }})
                        </button>
                    </nav>
                </div>
            </div>

            <!-- Desktop Layout & Mobile Tab Content -->
            <div class="flex-1 flex flex-col lg:flex-row gap-4 lg:gap-6 min-h-0">
                <!-- Left Side - Task Form -->
                <div :class=" [
                    'flex-1 lg:pr-6 lg:border-r border-gray-200 dark:border-gray-700 lg:min-w-0 min-h-0',
                    { 'hidden lg:block': activeTab !== 'edit' }
                ] ">
                    <div class="h-full overflow-y-auto pr-2 custom-scrollbar">
                        <form @submit.prevent=" updateTask " class="space-y-4 pb-4">
                            <!-- Title -->
                            <BaseInput v-model=" form.title " label="Title" placeholder="Enter task title" required
                                :error=" fieldErrors.title " />

                            <!-- Description -->
                            <BaseTextarea v-model=" form.description " label="Description"
                                placeholder="Enter task description" :rows=" 3 " :error=" fieldErrors.description " />

                            <!-- Status and Priority Row -->
                            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                <!-- Status -->
                                <BaseSelect v-model=" form.status_id " label="Status" placeholder="Select status"
                                    :options=" statuses " option-value="id" option-label="name"
                                    :error=" fieldErrors.status_id " />

                                <!-- Priority -->
                                <BaseSelect v-model=" form.priority " label="Priority" :options=" priorityOptions "
                                    :error=" fieldErrors.priority " />
                            </div>

                            <!-- Scheduling Section -->
                            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                <!-- Scheduled Start -->
                                <BaseDatePicker v-model=" form.scheduled_start " label="Scheduled Start"
                                    placeholder="Select start date & time" :error=" fieldErrors.start_date " />

                                <!-- Target Completion -->
                                <BaseDatePicker v-model=" form.target_completion " label="Target Completion"
                                    placeholder="Select completion date & time" :error=" fieldErrors.due_date " />
                            </div>

                            <!-- Estimated Hours -->
                            <BaseInput v-model=" form.estimated_hours " label="Estimated Hours" type="number"
                                placeholder="e.g., 4.5" step="0.5" min="0" max="999"
                                :error=" fieldErrors.estimated_hours " />

                            <!-- Deadline Extension Section -->
                            <div class="space-y-4 deadline-extension-responsive">
                                <div
                                    class="rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden bg-white dark:bg-gray-800">
                                    <!-- Header -->
                                    <div
                                        class="px-3 lg:px-6 py-3 lg:py-4 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
                                        <div class="flex items-center space-x-3">
                                            <div>
                                                <h3 class="text-sm font-semibold text-gray-900 dark:text-gray-100">
                                                    Deadline Extension</h3>
                                                <p class="text-xs text-gray-600 dark:text-gray-400">Extend deadlines
                                                    when
                                                    needed</p>
                                            </div>
                                        </div>
                                    </div>

                                    <div class="p-3 lg:p-6 space-y-4 lg:space-y-5">
                                        <!-- Current Due Date Card -->
                                        <div v-if="form.target_completion"
                                            class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4 shadow-sm glass-card">
                                            <div class="flex items-center justify-between">
                                                <div class="flex items-center space-x-3">
                                                    <div class="w-2 h-2 bg-blue-500 rounded-full deadline-pulse"></div>
                                                    <div>
                                                        <p
                                                            class="text-xs font-medium text-gray-600 dark:text-gray-400 uppercase tracking-wider">
                                                            Current Deadline</p>
                                                        <p
                                                            class="text-sm font-semibold text-gray-900 dark:text-gray-100 mt-0.5">
                                                            {{ formatDateTime(form.target_completion) }}
                                                        </p>
                                                    </div>
                                                </div>
                                                <div class="text-right">
                                                    <span
                                                        class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-gray-700 dark:text-blue-200 status-indicator">
                                                        Active
                                                    </span>
                                                </div>
                                            </div>
                                        </div>

                                        <!-- Extension Form -->
                                        <div
                                            class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4 space-y-4 glass-card">
                                            <div class="flex items-center space-x-2 mb-3">
                                                <svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor"
                                                    viewBox="0 0 24 24">
                                                    <path stroke-linecap="round" stroke-linejoin="round"
                                                        stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                                                </svg>
                                                <h4 class="text-sm font-medium text-gray-900 dark:text-gray-100">Request
                                                    Extension</h4>
                                            </div>

                                            <div class="grid gap-4">
                                                <!-- New Deadline -->
                                                <div>
                                                    <BaseDatePicker v-model=" deadlineExtension.new_due_date "
                                                        label="New Deadline"
                                                        placeholder="Select new deadline date & time"
                                                        :error=" deadlineExtension.errors.new_due_date "
                                                        class="deadline-picker" />
                                                </div>

                                                <!-- Reason -->
                                                <div>
                                                    <BaseTextarea v-model=" deadlineExtension.reason "
                                                        label="Justification"
                                                        placeholder="Briefly explain why this extension is necessary..."
                                                        :rows=" 3 " :error=" deadlineExtension.errors.reason "
                                                        class="reason-input" />
                                                </div>

                                                <!-- Submit Button -->
                                                <button @click=" submitDeadlineExtension "
                                                    :disabled=" !deadlineExtension.new_due_date || extensionLoading "
                                                    type="button"
                                                    class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium py-3 px-4 rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-md hover:shadow-lg transform hover:-translate-y-0.5 disabled:transform-none deadline-extend-btn">
                                                    <span v-if="extensionLoading"
                                                        class="flex items-center justify-center">
                                                        <svg class="animate-spin -ml-1 mr-3 h-4 w-4" fill="none"
                                                            viewBox="0 0 24 24">
                                                            <circle class="opacity-25" cx="12" cy="12" r="10"
                                                                stroke="currentColor" stroke-width="4" />
                                                            <path class="opacity-75" fill="currentColor"
                                                                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                                                        </svg>
                                                        Processing Extension...
                                                    </span>
                                                    <span v-else class="flex items-center justify-center">
                                                        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor"
                                                            viewBox="0 0 24 24">
                                                            <path stroke-linecap="round" stroke-linejoin="round"
                                                                stroke-width="2"
                                                                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                                        </svg>
                                                        Extend Deadline
                                                    </span>
                                                </button>
                                            </div>
                                        </div>

                                        <!-- Extension History -->
                                        <div v-if="deadlineExtensions.length > 0"
                                            class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden glass-card">
                                            <div
                                                class="px-4 py-3 bg-gray-50 dark:bg-gray-700 border-b border-gray-200 dark:border-gray-600">
                                                <div class="flex items-center space-x-2">
                                                    <h4 class="text-sm font-medium text-gray-900 dark:text-gray-100">
                                                        Extension
                                                        History
                                                    </h4>
                                                    <span
                                                        class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-gray-200 text-gray-800 dark:bg-gray-600 dark:text-gray-200 extension-badge">
                                                        {{ deadlineExtensions.length }}
                                                    </span>
                                                </div>
                                            </div>

                                            <div class="max-h-48 overflow-y-auto extension-history-scroll">
                                                <div class="divide-y divide-gray-200 dark:divide-gray-700">
                                                    <div v-for="(extension, index) in deadlineExtensions"
                                                        :key=" extension.id "
                                                        class="p-4 hover:bg-gray-100 dark:hover:bg-gray-700/50 transition-colors duration-150 extension-item">
                                                        <div class="flex items-start justify-between space-x-4">
                                                            <div class="flex-1 min-w-0">
                                                                <!-- Timeline -->
                                                                <div class="flex items-center space-x-2 text-sm">
                                                                    <span
                                                                        class="text-gray-500 dark:text-gray-400 font-medium">
                                                                        {{ formatDateTime(extension.previous_due_date)
                                                                        }}
                                                                    </span>
                                                                    <svg class="w-4 h-4 text-gray-400" fill="none"
                                                                        stroke="currentColor" viewBox="0 0 24 24">
                                                                        <path stroke-linecap="round"
                                                                            stroke-linejoin="round" stroke-width="2"
                                                                            d="M9 5l7 7-7 7" />
                                                                    </svg>
                                                                    <span
                                                                        class="text-gray-900 dark:text-gray-100 font-semibold">
                                                                        {{ formatDateTime(extension.new_due_date) }}
                                                                    </span>
                                                                </div>

                                                                <!-- Reason -->
                                                                <div v-if="extension.reason" class="mt-2">
                                                                    <p
                                                                        class="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">
                                                                        {{ extension.reason }}
                                                                    </p>
                                                                </div>

                                                                <!-- Meta info -->
                                                                <div
                                                                    class="flex items-center space-x-4 mt-2 text-xs text-gray-500 dark:text-gray-400">
                                                                    <span class="flex items-center space-x-1">
                                                                        <svg class="w-3 h-3" fill="none"
                                                                            stroke="currentColor" viewBox="0 0 24 24">
                                                                            <path stroke-linecap="round"
                                                                                stroke-linejoin="round" stroke-width="2"
                                                                                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                                                        </svg>
                                                                        <span>{{ extension.created_by || 'Unknown'
                                                                            }}</span>
                                                                    </span>
                                                                    <span class="flex items-center space-x-1">
                                                                        <svg class="w-3 h-3" fill="none"
                                                                            stroke="currentColor" viewBox="0 0 24 24">
                                                                            <path stroke-linecap="round"
                                                                                stroke-linejoin="round" stroke-width="2"
                                                                                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                                                        </svg>
                                                                        <span>{{ formatDateTime(extension.created_at)
                                                                            }}</span>
                                                                    </span>
                                                                </div>
                                                            </div>

                                                            <!-- Extension number badge -->
                                                            <div class="shrink-0">
                                                                <span
                                                                    class="inline-flex items-center justify-center w-6 h-6 rounded-full text-xs font-medium extension-badge"
                                                                    :class=" index === 0 ? 'bg-blue-100 text-blue-800 dark:bg-gray-700 dark:text-blue-200' : 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-400' ">
                                                                    {{ deadlineExtensions.length - index }}
                                                                </span>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Task Members -->
                            <div>
                                <div class="mb-2">
                                    <BaseInput label="Task Members" placeholder="Search task members..."
                                        @input="debouncedMemberSearch($event.target.value)" size="sm" />
                                </div> <!-- Selected Members Display -->
                                <div v-if="form.assigned_members.length > 0"
                                    class="mb-2 p-2 bg-gray-50 dark:bg-blue-900/20 rounded-lg">
                                    <div class="text-xs font-medium text-gray-600 dark:text-blue-300 mb-1">Assigned Team
                                        Members:</div>
                                    <div class="flex flex-wrap gap-1">
                                        <span v-for="memberId in form.assigned_members" :key=" memberId "
                                            class="inline-flex items-center px-2 py-1 text-xs bg-gray-100 dark:bg-blue-800 text-gray-700 dark:text-blue-200 rounded-full">
                                            {{ getSelectedMemberName(memberId) }}
                                            <button @click="removeMember(memberId)"
                                                class="ml-1 text-gray-500 dark:text-blue-400 hover:text-gray-700 dark:hover:text-blue-200">
                                                ×
                                            </button>
                                        </span>
                                    </div>
                                </div>

                                <!-- Members List -->
                                <div
                                    class="space-y-2 max-h-32 overflow-y-auto border border-gray-200 dark:border-gray-600 rounded-lg p-2 bg-gray-50 dark:bg-gray-800">
                                    <div v-if="projectMembers.length === 0 && !memberSearchQuery"
                                        class="text-sm text-gray-400 dark:text-gray-400 text-center py-2">
                                        No project members available
                                    </div>
                                    <div v-else-if="projectMembers.length === 0 && memberSearchQuery"
                                        class="text-sm text-gray-400 dark:text-gray-400 text-center py-2">
                                        No members found matching "{{ memberSearchQuery }}"
                                    </div>
                                    <label v-for="member in projectMembers" :key=" member.id "
                                        class="flex items-center space-x-2 hover:bg-blue-50 hover:border-blue-200 border border-transparent dark:hover:bg-gray-700 dark:hover:border-gray-600 p-1 rounded cursor-pointer transition-all duration-200">
                                        <input type="checkbox" :value=" member.user " v-model=" form.assigned_members "
                                            class="rounded border-gray-200 dark:border-gray-600 text-blue-600 focus:ring-blue-500 dark:bg-gray-700" />
                                        <div class="flex items-center space-x-2 flex-1 min-w-0">
                                            <div
                                                class="w-6 h-6 rounded-full bg-gray-200 dark:bg-gray-600 flex items-center justify-center">
                                                <span class="text-xs font-medium text-gray-500 dark:text-gray-300">
                                                    {{ getInitials(member) }}
                                                </span>
                                            </div>
                                            <span class="text-sm font-medium text-gray-700 dark:text-gray-100 truncate">
                                                {{ member.user_name || member.user_email }}
                                            </span>
                                        </div>
                                    </label>
                                </div>
                            </div>

                            <!-- Error message -->
                            <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-3">
                                <p class="text-sm text-red-600">{{ error }}</p>
                            </div>
                        </form>
                    </div>
                </div>

                <!-- Right Side - Comments Section -->
                <div :class=" [
                    'w-full lg:w-96 min-h-0',
                    { 'hidden lg:block': activeTab !== 'comments' }
                ] ">
                    <div class="h-full flex flex-col">
                        <!-- Comments Header (hidden on mobile, shown in tabs) -->
                        <div
                            class="hidden lg:flex items-center justify-between mb-4 pb-3 border-b border-gray-200 dark:border-gray-700 flex-shrink-0">
                            <h3
                                class="text-base lg:text-lg font-semibold text-gray-900 dark:text-gray-100 flex items-center">
                                <svg class="w-4 h-4 lg:w-5 lg:h-5 mr-2 text-blue-600" fill="none" stroke="currentColor"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                                </svg>
                                Comments
                            </h3>
                            <span
                                class="text-sm text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded-full">
                                {{ comments.length }}
                            </span>
                        </div>

                        <!-- Add Comment Form -->
                        <div class="mb-4 bg-gray-50 dark:bg-gray-800 rounded-lg p-3 lg:p-4 flex-shrink-0">
                            <div class="flex-1">
                                <!-- Comment Box with Attachment Section -->
                                <div class="relative border border-gray-200 dark:border-gray-600 rounded-lg overflow-hidden bg-white dark:bg-gray-900 transition-all duration-200"
                                    @dragenter=" handleDragEnter " @dragleave=" handleDragLeave "
                                    @dragover=" handleDragOver " @drop=" handleDrop "
                                    :class=" { 'ring-2 ring-blue-300 border-blue-300 bg-blue-50 dark:bg-blue-900/20 dark:border-blue-500': isDragOver } ">
                                    <!-- Textarea Container -->
                                    <div class="relative">
                                        <BaseTextarea v-model=" newComment "
                                            :placeholder=" isDragOver ? 'Drop file here or type your comment...' : 'Add a comment... (Ctrl+Enter to submit)' "
                                            :rows=" 4 "
                                            class="comment-textarea border-0 rounded-none resize-none pr-16 transition-colors duration-200"
                                            :error=" commentErrors.content " @keydown=" handleCommentKeydown " />

                                        <!-- Attach Button Inside Textarea -->
                                        <button v-if="!showAttachmentInput" @click="$refs.fileInput.click()"
                                            class="absolute bottom-2 right-2 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 transition-all duration-200 cursor-pointer p-2 rounded hover:bg-gray-50 dark:hover:bg-gray-700"
                                            title="Add attachment">
                                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                    d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                                            </svg>
                                        </button>
                                    </div>

                                    <!-- Hidden File Input -->
                                    <input type="file" ref="fileInput" @change=" handleFileSelect " multiple
                                        accept="image/*,.pdf,.doc,.docx,.txt,.zip" class="hidden" />

                                    <!-- Attachments Section Inside Comment Box -->
                                    <div v-if="selectedAttachments.length > 0"
                                        class="border-t border-gray-200 dark:border-gray-600 p-2 lg:p-3 bg-gray-50 dark:bg-gray-800">
                                        <!-- Simple file list -->
                                        <div class="space-y-1 lg:space-y-2 max-h-32 overflow-y-auto">
                                            <div v-for="(attachment, index) in selectedAttachments"
                                                :key=" `attachment-${ index }` "
                                                class="flex items-center space-x-2 lg:space-x-3 p-1.5 lg:p-2 bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 attachment-item">
                                                <!-- File Icon/Preview -->
                                                <div class="shrink-0">
                                                    <div v-if="isImageFile(attachment)" class="relative cursor-pointer">
                                                        <img :src=" getFilePreviewUrl(attachment) "
                                                            :alt=" attachment.name "
                                                            class="w-8 h-8 rounded object-cover border border-gray-200 dark:border-gray-600 hover:opacity-80 transition-opacity cursor-pointer"
                                                            @click="previewAttachment(attachment)" />
                                                    </div>
                                                    <div v-else
                                                        class="w-8 h-8 bg-blue-100 dark:bg-blue-900 rounded flex items-center justify-center cursor-pointer hover:bg-blue-200 dark:hover:bg-blue-800 transition-colors"
                                                        @click="previewAttachment(attachment)">
                                                        <svg class="w-4 h-4 text-blue-600 dark:text-blue-400"
                                                            fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                            <path stroke-linecap="round" stroke-linejoin="round"
                                                                stroke-width="2"
                                                                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                                        </svg>
                                                    </div>
                                                </div>

                                                <!-- File Name Only -->
                                                <div class="flex-1 min-w-0">
                                                    <p
                                                        class="text-xs lg:text-sm text-gray-700 dark:text-gray-300 truncate">
                                                        {{ attachment.name }}
                                                    </p>
                                                </div>

                                                <!-- Remove Button -->
                                                <button @click="removeAttachment(index)"
                                                    class="text-red-400 hover:text-red-600 transition-colors cursor-pointer p-1"
                                                    :title=" `Remove ${ attachment.name }` ">
                                                    <svg class="w-3 h-3 lg:w-4 lg:h-4" fill="none" stroke="currentColor"
                                                        viewBox="0 0 24 24">
                                                        <path stroke-linecap="round" stroke-linejoin="round"
                                                            stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                                                    </svg>
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- Bottom Actions Bar Inside Comment Box -->
                                <div
                                    class="border-t border-gray-200 dark:border-gray-600 px-3 py-2 bg-gray-50 dark:bg-gray-800">
                                    <!-- Character Counter and Actions -->
                                    <div
                                        class="flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-2 sm:space-y-0 p-2 lg:p-3">
                                        <div class="flex items-center space-x-3">
                                            <!-- Character Counter -->
                                            <div class="text-xs text-gray-500 dark:text-gray-400">
                                                <span :class=" newComment.length > 1000 ? 'text-red-500' : '' ">
                                                    {{ newComment.length }}
                                                </span>
                                                <span class="text-gray-400">/1000</span>
                                            </div>
                                        </div>

                                        <BaseButton variant="primary" size="sm" @click=" addComment "
                                            :disabled=" (!newComment.trim() && selectedAttachments.length === 0) || addingComment || newComment.length > 1000 "
                                            :loading=" addingComment " loadingText="Adding..." class="w-full sm:w-auto">
                                            <template v-if=" !addingComment " #icon>
                                                <svg class="w-3 h-3 lg:w-4 lg:h-4" fill="none" stroke="currentColor"
                                                    viewBox="0 0 24 24">
                                                    <path stroke-linecap="round" stroke-linejoin="round"
                                                        stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                                                </svg>
                                            </template>
                                            Comment
                                        </BaseButton>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Comments List -->
                        <div class="flex-1 overflow-y-auto pr-2 custom-scrollbar min-h-0">
                            <div class="space-y-3 lg:space-y-4 pb-4">
                                <div v-if="loadingComments" class="flex items-center justify-center py-8">
                                    <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
                                    <span class="ml-2 text-sm text-gray-600">Loading comments...</span>
                                </div>

                                <div v-else-if="comments.length === 0" class="text-center py-8">
                                    <svg class="w-12 h-12 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor"
                                        viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                                    </svg>
                                    <p class="text-sm text-gray-500 dark:text-gray-400">No comments yet</p>
                                    <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">Be the first to add a
                                        comment!</p>
                                </div>

                                <!-- Comment Items -->
                                <div v-for="comment in comments" :key=" comment.id "
                                    class="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 p-3 lg:p-4 comment-item">
                                    <!-- Comment Header -->
                                    <div class="flex items-start justify-between mb-2">
                                        <div class="flex items-center space-x-2 lg:space-x-3">
                                            <div
                                                class="w-7 h-7 lg:w-8 lg:h-8 rounded-full bg-gray-100 dark:bg-gray-700 flex items-center justify-center shrink-0">
                                                <span class="text-xs font-medium text-gray-600 dark:text-gray-300">
                                                    {{ getCommentAuthorInitials(comment) }}
                                                </span>
                                            </div>
                                            <div class="min-w-0">
                                                <p
                                                    class="text-xs lg:text-sm font-medium text-gray-900 dark:text-gray-100 truncate">
                                                    {{ getCommentAuthorName(comment) }}
                                                </p>
                                                <p class="text-xs text-gray-500 dark:text-gray-400">
                                                    {{ formatCommentDate(getCommentTimestamp(comment)) }}
                                                    <span v-if="isCommentEdited(comment)" class="ml-1">(edited)</span>
                                                </p>
                                            </div>
                                        </div>

                                        <!-- Comment Actions -->
                                        <div v-if="canEditComment(comment)"
                                            class="flex items-center space-x-1 lg:space-x-2 shrink-0">
                                            <button @click="startEditComment(comment)"
                                                class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors cursor-pointer p-1"
                                                title="Edit comment">
                                                <svg class="w-3 h-3 lg:w-4 lg:h-4" fill="none" stroke="currentColor"
                                                    viewBox="0 0 24 24">
                                                    <path stroke-linecap="round" stroke-linejoin="round"
                                                        stroke-width="2"
                                                        d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.536L16.732 3.732z" />
                                                </svg>
                                            </button>
                                            <button @click="deleteComment(comment.id)"
                                                :disabled=" deletingComment === comment.id "
                                                class="text-red-400 hover:text-red-600 transition-colors disabled:opacity-50 cursor-pointer p-1"
                                                title="Delete comment">
                                                <svg v-if="deletingComment === comment.id"
                                                    class="animate-spin w-3 h-3 lg:w-4 lg:h-4" fill="none"
                                                    viewBox="0 0 24 24">
                                                    <circle class="opacity-25" cx="12" cy="12" r="10"
                                                        stroke="currentColor" stroke-width="4" />
                                                    <path class="opacity-75" fill="currentColor"
                                                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                                                </svg>
                                                <svg v-else class="w-3 h-3 lg:w-4 lg:h-4" fill="none"
                                                    stroke="currentColor" viewBox="0 0 24 24">
                                                    <path stroke-linecap="round" stroke-linejoin="round"
                                                        stroke-width="2"
                                                        d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                                </svg>
                                            </button>
                                        </div>
                                    </div>

                                    <!-- Comment Content -->
                                    <div v-if="editingComment?.id === comment.id">
                                        <!-- Edit Form -->
                                        <div class="mt-2 space-y-3">
                                            <BaseTextarea v-model=" editingComment.content " :rows=" 3 "
                                                class="comment-textarea" :error=" commentErrors.content " />

                                            <!-- Existing Attachments -->
                                            <div v-if="editingComment.attachments && editingComment.attachments.length > 0"
                                                class="space-y-2">
                                                <h6 class="text-xs font-medium text-gray-600 dark:text-gray-400">Current
                                                    Attachments
                                                </h6>
                                                <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2">
                                                    <div v-for="attachment in editingComment.attachments"
                                                        :key=" attachment.id "
                                                        class="relative group bg-gray-50 dark:bg-gray-700 rounded-lg p-2 border">
                                                        <!-- Attachment Preview -->
                                                        <div class="flex items-center space-x-2">
                                                            <div v-if="isImageFile(attachment.file)"
                                                                class="flex-shrink-0">
                                                                <img :src=" attachment.file "
                                                                    :alt=" getFileName(attachment.file) "
                                                                    class="w-8 h-8 object-cover rounded">
                                                            </div>
                                                            <div v-else class="flex-shrink-0">
                                                                <svg class="w-8 h-8 text-gray-400" fill="currentColor"
                                                                    viewBox="0 0 20 20">
                                                                    <path
                                                                        d="M4 3a2 2 0 00-2 2v1.586l.293-.293a1 1 0 011.414 0L8 10.586l2.293-2.293a1 1 0 011.414 0L14 10.586l1.293-1.293a1 1 0 011.414 0L17 9.586V5a2 2 0 00-2-2H4zM2 13.414V15a2 2 0 002 2h12a2 2 0 002-2v-1.586l-1.293 1.293a1 1 0 01-1.414 0L13 12.414l-2.293 2.293a1 1 0 01-1.414 0L7 12.414l-1.293 1.293a1 1 0 01-1.414 0L2 13.414z" />
                                                                </svg>
                                                            </div>
                                                            <div class="flex-1 min-w-0">
                                                                <p
                                                                    class="text-xs text-gray-600 dark:text-gray-300 truncate">
                                                                    {{ getFileName(attachment.file) }}
                                                                </p>
                                                            </div>
                                                        </div>
                                                        <!-- Delete Button -->
                                                        <button @click="markAttachmentForDeletion(attachment)"
                                                            class="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center text-xs hover:bg-red-600">
                                                            ×
                                                        </button>
                                                    </div>
                                                </div>
                                            </div>

                                            <!-- New Attachments -->
                                            <div v-if="editingAttachments.length > 0" class="space-y-2">
                                                <h6 class="text-xs font-medium text-gray-600 dark:text-gray-400">New
                                                    Attachments
                                                </h6>
                                                <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2">
                                                    <div v-for="(file, index) in editingAttachments"
                                                        :key=" `new-${ index }` "
                                                        class="relative group bg-blue-50 dark:bg-blue-900/20 rounded-lg p-2 border border-blue-200 dark:border-blue-800">
                                                        <div class="flex items-center space-x-2">
                                                            <div class="flex-shrink-0">
                                                                <svg class="w-8 h-8 text-blue-500" fill="currentColor"
                                                                    viewBox="0 0 20 20">
                                                                    <path fill-rule="evenodd"
                                                                        d="M4 3a2 2 0 00-2 2v1.586l.293-.293a1 1 0 011.414 0L8 10.586l2.293-2.293a1 1 0 011.414 0L14 10.586l1.293-1.293a1 1 0 011.414 0L17 9.586V5a2 2 0 00-2-2H4zM2 13.414V15a2 2 0 002 2h12a2 2 0 002-2v-1.586l-1.293 1.293a1 1 0 01-1.414 0L13 12.414l-2.293 2.293a1 1 0 01-1.414 0L7 12.414l-1.293 1.293a1 1 0 01-1.414 0L2 13.414z"
                                                                        clip-rule="evenodd" />
                                                                </svg>
                                                            </div>
                                                            <div class="flex-1 min-w-0">
                                                                <p
                                                                    class="text-xs text-gray-600 dark:text-gray-300 truncate">
                                                                    {{ file.name }}
                                                                </p>
                                                            </div>
                                                        </div>
                                                        <button @click="removeEditAttachment(index)"
                                                            class="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center text-xs hover:bg-red-600">
                                                            ×
                                                        </button>
                                                    </div>
                                                </div>
                                            </div>

                                            <!-- Add Attachments Button -->
                                            <div class="flex items-center justify-between">
                                                <label
                                                    class="inline-flex items-center px-3 py-1.5 text-xs font-medium text-gray-600 hover:text-gray-800 cursor-pointer transition-colors">
                                                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor"
                                                        viewBox="0 0 24 24">
                                                        <path stroke-linecap="round" stroke-linejoin="round"
                                                            stroke-width="2"
                                                            d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                                                    </svg>
                                                    Add Attachments
                                                    <input type="file" @change=" handleEditFileSelect " multiple
                                                        class="hidden">
                                                </label>
                                            </div>

                                            <div
                                                class="flex flex-col sm:flex-row justify-end space-y-2 sm:space-y-0 sm:space-x-2 mt-3">
                                                <button @click=" cancelEditComment "
                                                    class="px-3 py-1.5 text-xs font-medium text-gray-600 hover:text-gray-800 transition-colors">
                                                    Cancel
                                                </button>
                                                <button @click=" saveEditComment "
                                                    :disabled=" !editingComment.content.trim() || updatingComment "
                                                    class="inline-flex items-center justify-center px-3 py-1.5 text-xs font-medium bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors">
                                                    <svg v-if="updatingComment" class="animate-spin -ml-1 mr-1 h-3 w-3"
                                                        fill="none" viewBox="0 0 24 24">
                                                        <circle class="opacity-25" cx="12" cy="12" r="10"
                                                            stroke="currentColor" stroke-width="4" />
                                                        <path class="opacity-75" fill="currentColor"
                                                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                                                    </svg>
                                                    {{ updatingComment ? 'Updating...' : 'Update' }}
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                    <div v-else class="mt-2">
                                        <p
                                            class="text-sm text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-wrap break-words overflow-wrap-anywhere">
                                            {{
                                                comment.content }}</p>

                                        <!-- Comment Attachments -->
                                        <div v-if="comment.attachment && comment.attachment.length > 0" class="mt-3">
                                            <!-- Multiple attachments from new structure -->
                                            <div
                                                v-if="comment.attachment && Array.isArray(comment.attachment) && comment.attachment.length > 0">
                                                <div v-if="comment.attachment.length > 1" class="space-y-2">
                                                    <p class="text-xs text-gray-500 dark:text-gray-400 font-medium">
                                                        {{ comment.attachment.length }} attachments
                                                    </p>
                                                    <div
                                                        class="grid grid-cols-2 lg:grid-cols-3 gap-1.5 lg:gap-2 max-w-full lg:max-w-md">
                                                        <div v-for="(attachment, index) in comment.attachment"
                                                            :key=" `comment-${ comment.id }-attachment-${ index }` "
                                                            class="attachment-preview cursor-pointer"
                                                            @click="openAttachment(attachment.file)">
                                                            <!-- Image Preview -->
                                                            <div v-if="isImageFile(attachment.file)"
                                                                class="relative group">
                                                                <img :src=" attachment.file "
                                                                    :alt=" getFileName(attachment.file) "
                                                                    class="w-full h-20 object-cover rounded-lg shadow-sm hover:opacity-90 transition-opacity"
                                                                    @error="$event.target.style.display = 'none'" />
                                                                <div
                                                                    class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-10 transition-all rounded-lg flex items-center justify-center">
                                                                    <svg class="w-5 h-5 text-white opacity-0 group-hover:opacity-100 transition-opacity"
                                                                        fill="none" stroke="currentColor"
                                                                        viewBox="0 0 24 24">
                                                                        <path stroke-linecap="round"
                                                                            stroke-linejoin="round" stroke-width="2"
                                                                            d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                                                                    </svg>
                                                                </div>
                                                            </div>
                                                            <!-- File Icon for Non-Images -->
                                                            <div v-else
                                                                class="w-full h-20 bg-blue-100 dark:bg-blue-900/20 rounded-lg flex flex-col items-center justify-center hover:bg-blue-200 dark:hover:bg-blue-800/40 transition-colors">
                                                                <svg class="w-6 h-6 text-blue-600 dark:text-blue-400"
                                                                    fill="none" stroke="currentColor"
                                                                    viewBox="0 0 24 24">
                                                                    <path stroke-linecap="round" stroke-linejoin="round"
                                                                        stroke-width="2"
                                                                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                                                </svg>
                                                                <span
                                                                    class="text-xs text-blue-600 dark:text-blue-400 mt-1 truncate max-w-full px-1">
                                                                    {{ getFileName(attachment.file).substring(0, 8)
                                                                    }}...
                                                                </span>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>

                                                <!-- Single attachment from new structure -->
                                                <div v-else-if="comment.attachment.length === 1"
                                                    class="attachment-preview cursor-pointer"
                                                    @click="openAttachment(comment.attachment[0].file)">
                                                    <div v-if="isImageFile(comment.attachment[0].file)">
                                                        <img :src=" comment.attachment[0].file "
                                                            :alt=" getFileName(comment.attachment[0].file) "
                                                            class="w-20 h-20 object-cover rounded-lg shadow-sm hover:opacity-90 transition-opacity"
                                                            @error="$event.target.style.display = 'none'" />
                                                    </div>
                                                    <div v-else class="inline-block">
                                                        <div
                                                            class="w-20 h-20 bg-blue-100 dark:bg-blue-900/20 rounded-lg flex items-center justify-center hover:bg-blue-200 dark:hover:bg-blue-800/40 transition-colors">
                                                            <svg class="w-6 h-6 text-blue-600 dark:text-blue-400"
                                                                fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                                <path stroke-linecap="round" stroke-linejoin="round"
                                                                    stroke-width="2"
                                                                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                                            </svg>
                                                        </div>
                                                        <p
                                                            class="text-xs text-gray-500 dark:text-gray-400 mt-1 max-w-20 truncate">
                                                            {{ getFileName(comment.attachment[0].file) }}
                                                        </p>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <template #footer>
            <div class="flex space-x-3 justify-end">
                <BaseButton variant="secondary" @click=" closeModal " :disabled=" updating " type="button">
                    Cancel
                </BaseButton>

                <BaseButton variant="primary" @click=" updateTask " :disabled=" updating || !form.title.trim() "
                    :loading=" updating " loadingText="Updating...">
                    Update Task
                </BaseButton>
            </div>
        </template>
    </BaseModal>

    <!-- Confirmation Modal -->
    <ConfirmModal :is-open=" showConfirmModal " :title=" confirmModalData.title " :message=" confirmModalData.message "
        :confirm-text=" confirmModalData.confirmText " cancel-text="Cancel"
        confirm-class="bg-red-600 hover:bg-red-700 focus:ring-red-500" @confirm=" handleConfirmAction "
        @cancel=" handleCancelConfirm " />
</template>

<script setup>
import { ref, reactive, watch, computed, onMounted, nextTick, inject } from 'vue'
import axios from "@/plugins/axiosConfig.js"
import BaseModal from './BaseModal.vue'
import ConfirmModal from './ConfirmModal.vue'
import { BaseInput, BaseTextarea, BaseSelect, BaseDatePicker, BaseButton } from '@/components/forms'

// Props
const props = defineProps({
    isOpen: {
        type: Boolean,
        default: false
    },
    task: {
        type: Object,
        default: null
    },
    statuses: {
        type: Array,
        default: () => []
    },
    projectSlug: {
        type: String,
        default: ''
    }
})

// Emits
const emit = defineEmits(['close', 'updated'])

const $toast = inject("toast")

// Priority options
const priorityOptions = [
    { value: 'low', label: 'Low' },
    { value: 'medium', label: 'Medium' },
    { value: 'high', label: 'High' }
]

// Reactive data
const loading = ref(false)
const updating = ref(false)
const extensionLoading = ref(false)
const error = ref('')
const fieldErrors = ref({})
const projectMembers = ref([])
const memberSearchQuery = ref('')
const searchTimeout = ref(null)
const deadlineExtensions = ref([])

// Mobile tab state
const activeTab = ref('edit') // 'edit' | 'comments'

// Comments related data
const comments = ref([])
const newComment = ref('')
const loadingComments = ref(false)
const addingComment = ref(false)
const deletingComment = ref(null)
const updatingComment = ref(false)
const editingComment = ref(null)
const editingAttachments = ref([]) // New attachments to add during edit
const attachmentsToDelete = ref([]) // IDs of attachments to delete during edit
const commentErrors = ref({})
const currentUser = ref(null) // Will be set from auth context or API

// Attachment related data
const selectedAttachments = ref([])
const showAttachmentInput = ref(false)
const fileInput = ref(null)
const isDragOver = ref(false)

// Confirmation modal state
const showConfirmModal = ref(false)
const confirmModalData = ref({
    title: '',
    message: '',
    confirmText: '',
    action: null
})

const form = reactive({
    title: '',
    description: '',
    status_id: '',
    priority: 'medium',
    scheduled_start: null,
    target_completion: null,
    estimated_hours: null,
    assigned_members: []
})

const deadlineExtension = reactive({
    new_due_date: null,
    reason: '',
    errors: {}
})

// Computed
const projectId = computed(() => {
    return props.task?.project?.id
})

// Comments Methods
const fetchComments = async () => {
    if (!props.task?.id || !projectId.value) return

    try {
        loadingComments.value = true
        const response = await axios.get(`projects/${projectId.value}/tasks/${props.task.id}/comments/`)
        comments.value = response.data.data || response.data || []
    } catch (err) {
        console.error('Failed to fetch comments:', err)
        comments.value = []
    } finally {
        loadingComments.value = false
    }
}

const addComment = async () => {
    if ((!newComment.value.trim() && selectedAttachments.value.length === 0) || !props.task?.id || !projectId.value) return

    try {
        addingComment.value = true
        commentErrors.value = {}

        // Use FormData for file uploads
        const formData = new FormData()
        formData.append('content', newComment.value.trim() || '')

        // Add multiple attachments
        selectedAttachments.value.forEach((file, index) => {
            formData.append('attachment', file)
        })

        const response = await axios.post(
            `projects/${projectId.value}/tasks/${props.task.id}/comments/`,
            formData,
            {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            }
        )
        const comment = response.data.data || response.data

        // Add comment to the beginning of the list
        comments.value.unshift(comment)
        newComment.value = ''

        // Clear attachments
        selectedAttachments.value = []

        $toast.success('Comment added successfully')
    } catch (err) {
        const responseData = err.response?.data

        if (responseData?.message) {
            $toast.error(responseData.message)
        }

        if (responseData?.data?.errors) {
            commentErrors.value = responseData.data.errors
        } else if (!responseData?.message) {
            commentErrors.value = { content: 'Failed to add comment. Please try again.' }
            $toast.error('Failed to add comment')
        }
    } finally {
        addingComment.value = false
    }
}

const startEditComment = (comment) => {
    editingComment.value = {
        id: comment.id,
        content: comment.content,
        attachments: comment.attachment || [] // Include existing attachments
    }
    editingAttachments.value = [] // Reset new attachments
    attachmentsToDelete.value = [] // Reset deleted attachments
    commentErrors.value = {}
}

const cancelEditComment = () => {
    editingComment.value = null
    editingAttachments.value = []
    attachmentsToDelete.value = []
    commentErrors.value = {}
}

const saveEditComment = async () => {
    if (!editingComment.value?.content.trim() || !projectId.value) return

    try {
        updatingComment.value = true
        commentErrors.value = {}

        // Create FormData for handling attachments
        const formData = new FormData()
        formData.append('content', editingComment.value.content.trim())

        // Check if we have any changes to attachments
        const hasAttachmentChanges = editingAttachments.value.length > 0 || attachmentsToDelete.value.length > 0

        if (hasAttachmentChanges) {
            // We have attachment changes, so we need to send ALL attachments we want to keep

            editingAttachments.value.forEach((file) => {
                formData.append('attachment', file)
            })
            // TODO: Implement proper existing attachment preservation if needed
        }

        const response = await axios.patch(
            `projects/${projectId.value}/tasks/${props.task.id}/comments/${editingComment.value.id}/`,
            formData,
            {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }
        )
        const updatedComment = response.data.data || response.data

        // Update comment in the list
        const index = comments.value.findIndex(c => c.id === editingComment.value.id)
        if (index !== -1) {
            comments.value[index] = updatedComment
        }

        editingComment.value = null
        editingAttachments.value = []
        attachmentsToDelete.value = []
        $toast.success('Comment updated successfully')
    } catch (err) {
        const responseData = err.response?.data

        if (responseData?.message) {
            $toast.error(responseData.message)
        }

        if (responseData?.data?.errors) {
            commentErrors.value = responseData.data.errors
        } else if (!responseData?.message) {
            commentErrors.value = { content: 'Failed to update comment. Please try again.' }
            $toast.error('Failed to update comment')
        }
    } finally {
        updatingComment.value = false
    }
}

const deleteComment = (commentId) => {
    if (!commentId || !projectId.value) return

    // Find the comment to get its content for the confirmation
    const comment = comments.value.find(c => c.id === commentId)
    const commentPreview = comment?.content?.length > 100
        ? comment.content.substring(0, 100) + '...'
        : comment?.content || 'this comment'

    // Show confirmation modal
    confirmModalData.value = {
        title: 'Delete Comment',
        message: `Are you sure you want to delete this comment?\n\n"${commentPreview}"\n\nThis action cannot be undone.`,
        confirmText: 'Delete Comment',
        action: () => performDeleteComment(commentId)
    }
    showConfirmModal.value = true
}

const performDeleteComment = async (commentId) => {
    try {
        deletingComment.value = commentId

        await axios.delete(`projects/${projectId.value}/tasks/${props.task.id}/comments/${commentId}/`)

        // Remove comment from the list
        comments.value = comments.value.filter(c => c.id !== commentId)

        $toast.success('Comment deleted successfully')
    } catch (err) {
        const responseData = err.response?.data

        if (responseData?.message) {
            $toast.error(responseData.message)
        } else {
            $toast.error('Failed to delete comment')
        }
    } finally {
        deletingComment.value = null
        showConfirmModal.value = false
    }
}

const canEditComment = (comment) => {
    return currentUser.value && (
        comment.created_by === currentUser.value.id ||
        comment.created_by === currentUser.value.email ||
        comment.author?.id === currentUser.value.id ||
        comment.author?.email === currentUser.value.email
    )
}

const getCommentAuthorName = (comment) => {
    return comment.author?.name ||
        comment.author?.first_name ||
        comment.author?.email ||
        comment.created_by_name ||
        'Unknown User'
}

const getCommentAuthorInitials = (comment) => {
    const name = getCommentAuthorName(comment)
    const parts = name.trim().split(' ')
    return parts.length > 1
        ? `${parts[0][0]}${parts[parts.length - 1][0]}`.toUpperCase()
        : parts[0][0].toUpperCase()
}

const formatCommentDate = (dateString) => {
    if (!dateString) return ''
    try {
        const date = new Date(dateString)
        const now = new Date()
        const diff = now.getTime() - date.getTime()
        const diffMinutes = Math.floor(diff / (1000 * 60))
        const diffHours = Math.floor(diff / (1000 * 60 * 60))
        const diffDays = Math.floor(diff / (1000 * 60 * 60 * 24))

        if (diffMinutes < 1) return 'Just now'
        if (diffMinutes < 60) return `${diffMinutes}m ago`
        if (diffHours < 24) return `${diffHours}h ago`
        if (diffDays < 7) return `${diffDays}d ago`

        return date.toLocaleDateString()
    } catch (e) {
        return dateString
    }
}

// Comment timestamp helpers
const getCommentTimestamp = (comment) => {
    // If comment has been updated, use updated_at, otherwise use created_at
    if (comment.updated_at && isCommentEdited(comment)) {
        return comment.updated_at
    }
    return comment.created_at
}

const isCommentEdited = (comment) => {
    if (!comment.updated_at || !comment.created_at) {
        return false
    }

    const createdTime = new Date(comment.created_at).getTime()
    const updatedTime = new Date(comment.updated_at).getTime()

    // If the difference is more than 1 second, consider it edited
    return Math.abs(updatedTime - createdTime) > 1000
}

// Confirmation modal handlers
const handleConfirmAction = async () => {
    if (confirmModalData.value.action) {
        await confirmModalData.value.action()
    }
}

const handleCancelConfirm = () => {
    showConfirmModal.value = false
    confirmModalData.value = {
        title: '',
        message: '',
        confirmText: '',
        action: null
    }
}

// Comment keyboard shortcuts
const handleCommentKeydown = (event) => {
    if (event.ctrlKey && event.key === 'Enter') {
        event.preventDefault()
        addComment()
    }
}

// Attachment functions
const handleFileSelect = (event) => {
    const files = Array.from(event.target.files)
    if (files.length > 0) {
        // Add new files to existing attachments
        selectedAttachments.value = [...selectedAttachments.value, ...files]

        showAttachmentInput.value = false
    }
}

const removeAttachment = (index) => {
    if (typeof index === 'number') {
        // Remove specific attachment by index
        selectedAttachments.value.splice(index, 1)
    } else {
        // Legacy support - clear all attachments
        selectedAttachments.value = []
    }

    if (fileInput.value) {
        fileInput.value.value = ''
    }
}

const previewAttachment = (file) => {
    if (file instanceof File) {
        const url = URL.createObjectURL(file)
        window.open(url, '_blank', 'noopener,noreferrer')
    } else if (typeof file === 'string') {
        openAttachment(file)
    }
}

// Drag and drop handlers
const handleDragEnter = (event) => {
    event.preventDefault()
    event.stopPropagation()
    isDragOver.value = true
}

const handleDragLeave = (event) => {
    event.preventDefault()
    event.stopPropagation()
    isDragOver.value = false
}

const handleDragOver = (event) => {
    event.preventDefault()
    event.stopPropagation()
}

const handleDrop = (event) => {
    event.preventDefault()
    event.stopPropagation()
    isDragOver.value = false

    const files = Array.from(event.dataTransfer.files)
    if (files.length > 0) {
        // Add dropped files to existing attachments
        selectedAttachments.value = [...selectedAttachments.value, ...files]
        showAttachmentInput.value = false
    }
}

// Edit attachment functions
const handleEditFileSelect = (event) => {
    const files = Array.from(event.target.files)
    if (files.length > 0) {
        // Add new files to editing attachments
        editingAttachments.value = [...editingAttachments.value, ...files]
    }
    // Clear the file input
    event.target.value = ''
}

const removeEditAttachment = (index) => {
    editingAttachments.value.splice(index, 1)
}

const markAttachmentForDeletion = (attachment) => {
    // Add attachment ID to deletion list
    if (attachment.id && !attachmentsToDelete.value.includes(attachment.id)) {
        attachmentsToDelete.value.push(attachment.id)
    }
    // Remove from the editing comment's attachments
    if (editingComment.value && editingComment.value.attachments) {
        editingComment.value.attachments = editingComment.value.attachments.filter(a => a.id !== attachment.id)
    }
}

const getFilePreviewUrl = (file) => {
    if (file instanceof File) {
        return URL.createObjectURL(file)
    }
    return file // If it's already a URL string
}

// Fetch detailed task information
const fetchTaskDetails = async () => {
    if (!props.task?.id || !projectId.value) return

    try {
        loading.value = true
        const response = await axios.get(`projects/${projectId.value}/tasks/${props.task.id}/`)
        const taskDetails = response.data.data || response.data
        populateForm(taskDetails)

        // Fetch deadline extensions separately if not included
        if (!taskDetails.deadline_extensions) {
            await fetchDeadlineExtensions()
        }
    } catch (err) {
        console.error('Failed to fetch task details:', err)
        error.value = 'Failed to load task details'
        // Fallback to basic task data
        populateForm(props.task)
    } finally {
        loading.value = false
    }
}

// Fetch deadline extensions history
const fetchDeadlineExtensions = async () => {
    if (!props.task?.id || !projectId.value) return

    try {
        const response = await axios.get(`projects/${projectId.value}/tasks/${props.task.id}/extend-deadline/`)
        deadlineExtensions.value = response.data.data || response.data || []
    } catch (err) {
        console.error('Failed to fetch deadline extensions:', err)
        deadlineExtensions.value = []
    }
}

// Debounced search for members
const debouncedMemberSearch = (query) => {
    if (searchTimeout.value) {
        clearTimeout(searchTimeout.value)
    }

    searchTimeout.value = setTimeout(() => {
        memberSearchQuery.value = query
        fetchProjectMembers(query)
    }, 300)
}

// Methods
const populateForm = (task) => {
    form.title = task.title || ''
    form.description = task.description || ''
    form.status_id = task.status?.id || ''
    form.priority = task.priority || 'medium'
    form.scheduled_start = task.start_date || null
    form.target_completion = task.due_date || null
    form.estimated_hours = task.estimated_hours || null
    form.assigned_members = task.assigned_members ? task.assigned_members.map(m => m.id) : []

    // Populate deadline extensions history if available
    deadlineExtensions.value = Array.isArray(task.deadline_extensions) ? task.deadline_extensions : []

    error.value = ''
    fieldErrors.value = {}

    // Reset deadline extension form
    deadlineExtension.new_due_date = null
    deadlineExtension.reason = ''
    deadlineExtension.errors = {}
}

const formatDateTime = (dateString) => {
    if (!dateString) return ''
    try {
        return new Date(dateString).toLocaleString()
    } catch (e) {
        return dateString
    }
}

const submitDeadlineExtension = async () => {
    if (!deadlineExtension.new_due_date || !props.task?.id) return

    try {
        extensionLoading.value = true
        deadlineExtension.errors = {}

        const payload = {
            task: props.task.id,
            new_due_date: new Date(deadlineExtension.new_due_date).toISOString(),
            reason: deadlineExtension.reason.trim() || null
        }

        const response = await axios.post(
            `projects/${projectId.value}/tasks/${props.task.id}/extend-deadline/`,
            payload
        )

        const newExtension = response.data.data || response.data

        // Add to history
        deadlineExtensions.value.unshift(newExtension)

        // Update the task's due date in the form
        form.target_completion = newExtension.new_due_date

        // Reset form
        deadlineExtension.new_due_date = null
        deadlineExtension.reason = ''

        $toast.success('Deadline extended successfully')

        // Emit updated task to parent
        const updatedTask = { ...props.task, due_date: newExtension.new_due_date }
        emit('updated', updatedTask)

    } catch (err) {
        const responseData = err.response?.data

        if (responseData?.message) {
            $toast.error(responseData.message)
        }

        if (responseData?.data?.errors) {
            deadlineExtension.errors = responseData.data.errors
        } else if (!responseData?.message) {
            deadlineExtension.errors = { general: 'Failed to extend deadline. Please try again.' }
            $toast.error('Failed to extend deadline')
        }
    } finally {
        extensionLoading.value = false
    }
}

const closeModal = () => {
    if (!updating.value) {
        emit('close')
    }
}

const fetchProjectMembers = async (searchQuery = '') => {
    // Try to get project identifier from props or task data
    let projectIdentifier = props.projectSlug

    if (!projectIdentifier && props.task?.project) {
        // If no projectSlug prop but we have task project data, use project ID
        projectIdentifier = props.task.project.id || props.task.project.slug
    }

    if (!projectIdentifier) {
        console.warn('No project identifier available for fetching members')
        return
    }

    try {
        let url = `projects/${projectIdentifier}/members/`
        if (searchQuery.trim()) {
            url += `?search=${encodeURIComponent(searchQuery.trim())}`
        }

        const response = await axios.get(url)
        projectMembers.value = response.data.data || response.data || []
    } catch (err) {
        console.error('Failed to fetch project members:', err)
        projectMembers.value = []
    }
}

const updateTask = async () => {
    if (!form.title.trim() || !props.task) return

    try {
        updating.value = true
        error.value = ''
        fieldErrors.value = {}

        const payload = {
            title: form.title.trim(),
            description: form.description.trim() || null,
            priority: form.priority,
            members: form.assigned_members
        }

        if (form.status_id) {
            payload.status_id = parseInt(form.status_id)
        }

        if (form.scheduled_start) {
            const startDate = new Date(form.scheduled_start)
            if (!isNaN(startDate.getTime())) {
                payload.start_date = startDate.toISOString()
            }
        }

        if (form.target_completion) {
            const endDate = new Date(form.target_completion)
            if (!isNaN(endDate.getTime())) {
                payload.due_date = endDate.toISOString()
            }
        }

        if (form.estimated_hours) {
            payload.estimated_hours = form.estimated_hours
        }

        const response = await axios.patch(`projects/${projectId.value}/tasks/${props.task.id}/`, payload)
        const updatedTask = response.data.data || response.data
        $toast.success('Task updated successfully')

        emit('updated', updatedTask)
    } catch (err) {
        const responseData = err.response?.data

        if (responseData?.message) {
            $toast.error(responseData.message)
        }

        if (responseData?.data?.errors && Array.isArray(responseData.data.errors)) {
            responseData.data.errors.forEach(errorItem => {
                Object.assign(fieldErrors.value, errorItem)
            })
        } else if (!responseData?.message) {
            error.value = 'Failed to update task. Please try again.'
            $toast.error('Failed to update task')
        }
    } finally {
        updating.value = false
    }
}

const getInitials = (member) => {
    const name = member.user_name || member.user_email
    if (!name) return '?'

    const parts = name.trim().split(' ')
    return parts.length > 1
        ? `${parts[0][0]}${parts[parts.length - 1][0]}`.toUpperCase()
        : parts[0][0].toUpperCase()
}

const getSelectedMemberName = (memberId) => {
    const member = projectMembers.value.find(m => m.user === memberId)
    return member?.user_name?.trim() || member?.user_email || 'Unknown'
}

const removeMember = (memberId) => {
    const index = form.assigned_members.indexOf(memberId)
    if (index > -1) {
        form.assigned_members.splice(index, 1)
    }
}

// Fetch current user information
const fetchCurrentUser = async () => {
    try {
        const response = await axios.get('/users/my-info/')
        currentUser.value = response.data.data || response.data
    } catch (err) {
        console.warn('Failed to fetch current user:', err)
        // Set a fallback user object
        currentUser.value = {
            id: 1,
            email: 'current@user.com',
            first_name: 'User'
        }
    }
}

// Watch for task changes to populate form
watch(() => props.task, (newTask) => {
    if (newTask) {
        populateForm(newTask)
    }
}, { immediate: true })

// Watch for dialog open/close
watch(() => props.isOpen, (isOpen) => {
    nextTick(() => {
        if (isOpen) {
            document.body.style.overflow = 'hidden'
            activeTab.value = 'edit' // Reset to edit tab when modal opens
            if (props.task) {
                fetchTaskDetails()
                fetchProjectMembers()
                fetchComments()
                fetchCurrentUser()
            }
        } else {
            document.body.style.overflow = ''
        }
    })
})

// Initialize on mount
onMounted(() => {
    fetchCurrentUser()
    if (props.isOpen && props.task) {
        populateForm(props.task)
        fetchProjectMembers()
        fetchComments()
    }
})

// Helper functions for attachment handling
const isImageFile = (fileOrUrl) => {
    if (!fileOrUrl) return false

    let fileName = ''

    // Handle File object
    if (fileOrUrl instanceof File) {
        fileName = fileOrUrl.name
    }
    // Handle string URL
    else if (typeof fileOrUrl === 'string') {
        fileName = fileOrUrl.split('/').pop() || ''
    }
    // Handle object with file property
    else if (typeof fileOrUrl === 'object' && fileOrUrl.file) {
        if (typeof fileOrUrl.file === 'string') {
            fileName = fileOrUrl.file.split('/').pop() || ''
        } else if (fileOrUrl.file instanceof File) {
            fileName = fileOrUrl.file.name
        }
    }
    // Handle object with name property
    else if (typeof fileOrUrl === 'object' && fileOrUrl.name) {
        fileName = fileOrUrl.name
    }
    // Handle object with attachment property
    else if (typeof fileOrUrl === 'object' && fileOrUrl.attachment) {
        if (typeof fileOrUrl.attachment === 'string') {
            fileName = fileOrUrl.attachment.split('/').pop() || ''
        }
    }
    else {
        return false
    }

    if (!fileName) return false

    const imageExtensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'svg']
    const extension = fileName.split('.').pop()?.toLowerCase()
    return imageExtensions.includes(extension)
}

const getFileName = (fileData) => {
    if (!fileData) return 'Unknown file'

    // If it's a File object
    if (fileData instanceof File) {
        return fileData.name
    }

    // If it's a string URL
    if (typeof fileData === 'string') {
        return fileData.split('/').pop() || 'Unknown file'
    }

    // If it's an object with file property
    if (typeof fileData === 'object' && fileData.file) {
        if (typeof fileData.file === 'string') {
            return fileData.file.split('/').pop() || 'Unknown file'
        }
        if (fileData.file instanceof File) {
            return fileData.file.name
        }
    }

    // If it's an object with name property
    if (typeof fileData === 'object' && fileData.name) {
        return fileData.name
    }

    return 'Unknown file'
}

const openAttachment = (url) => {
    if (!url) return
    // Open in new tab/window
    window.open(url, '_blank', 'noopener,noreferrer')
}
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

/* Custom flatpickr styling */
:deep(.flatpickr-input) {
    background-color: #ffffff;
    border: 1px solid #d1d5db;
    border-radius: 0.5rem;
    padding: 0.5rem 0.75rem;
    font-size: 0.875rem;
    transition: all 0.2s;
}

:deep(.flatpickr-input:focus) {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

:deep(.flatpickr-calendar) {
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    border-radius: 0.75rem;
    border: none;
}

/* Modern deadline extension styling */
.deadline-picker :deep(.flatpickr-input) {
    background: linear-gradient(to right, #fefbf3, #fef9f1);
    border: 1px solid #f3e8d0;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.deadline-picker :deep(.flatpickr-input:focus) {
    border-color: #f59e0b;
    box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.1);
    background: #ffffff;
}

.reason-input :deep(textarea) {
    background: linear-gradient(to right, #fefbf3, #fef9f1);
    border: 1px solid #f3e8d0;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    resize: vertical;
    min-height: 80px;
}

.reason-input :deep(textarea:focus) {
    border-color: #f59e0b;
    box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.1);
    background: #ffffff;
}

/* Smooth transitions for deadline section */
.deadline-section {
    animation: slideIn 0.5s ease-out;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Extension history animations */
.extension-history-enter-active {
    transition: all 0.3s ease-out;
}

.extension-history-enter-from {
    opacity: 0;
    transform: translateX(-20px);
}

.extension-history-enter-to {
    opacity: 1;
    transform: translateX(0);
}

/* Custom scrollbar for extension history */
.extension-history-scroll::-webkit-scrollbar {
    width: 6px;
}

.extension-history-scroll::-webkit-scrollbar-track {
    background: #f1f5f9;
    border-radius: 3px;
}

.extension-history-scroll::-webkit-scrollbar-thumb {
    background: linear-gradient(to bottom, #f59e0b, #d97706);
    border-radius: 3px;
}

.extension-history-scroll::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(to bottom, #d97706, #b45309);
}

/* Button hover effects */
.deadline-extend-btn {
    position: relative;
    overflow: hidden;
}

.deadline-extend-btn:before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: left 0.5s;
}

.deadline-extend-btn:hover:before {
    left: 100%;
}

/* Glass morphism effect for cards */
.glass-card {
    backdrop-filter: blur(12px);
    background: rgba(255, 255, 255, 0.8);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.dark .glass-card {
    background: rgba(31, 41, 55, 0.8);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

/* Pulse animation for active deadline */
.deadline-pulse {
    animation: pulse 2s infinite;
}

@keyframes pulse {

    0%,
    100% {
        transform: scale(1);
        opacity: 1;
    }

    50% {
        transform: scale(1.05);
        opacity: 0.9;
    }
}

/* Extension badge animation */
.extension-badge {
    animation: bounceIn 0.5s ease-out;
}

@keyframes bounceIn {
    0% {
        opacity: 0;
        transform: scale(0.3);
    }

    50% {
        opacity: 1;
        transform: scale(1.05);
    }

    70% {
        transform: scale(0.9);
    }

    100% {
        opacity: 1;
        transform: scale(1);
    }
}

/* Hover effects for extension history items */
.extension-item {
    transition: all 0.2s ease-out;
    border-left: 3px solid transparent;
}

.extension-item:hover {
    border-left-color: #f59e0b;
    transform: translateX(4px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.dark .extension-item:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

/* Status indicators with subtle animations */
.status-indicator {
    position: relative;
}

.status-indicator::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, transparent 30%, rgba(255, 255, 255, 0.1) 50%, transparent 70%);
    animation: shimmer 2s infinite;
}

@keyframes shimmer {
    0% {
        transform: translateX(-100%);
    }

    100% {
        transform: translateX(100%);
    }
}

/* Dark mode enhancements */
@media (prefers-color-scheme: dark) {
    .deadline-picker :deep(.flatpickr-input) {
        background: linear-gradient(to right, #1f2937, #374151);
        border-color: #4b5563;
        color: #f9fafb;
    }

    .reason-input :deep(textarea) {
        background: linear-gradient(to right, #1f2937, #374151);
        border-color: #4b5563;
        color: #f9fafb;
    }
}

/* Comments Section Styling */
.comment-textarea :deep(textarea) {
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    transition: all 0.2s ease-in-out;
    resize: vertical;
    min-height: 80px;
}

.comment-textarea :deep(textarea:focus) {
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    outline: none;
}

.comment-item {
    transition: all 0.2s ease-out;
    position: relative;
}

.comment-item:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.dark .comment-item:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

/* Custom scrollbar for comments */
.overflow-y-auto::-webkit-scrollbar {
    width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
    background: #f1f5f9;
    border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
    background: linear-gradient(to bottom, #3b82f6, #2563eb);
    border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(to bottom, #2563eb, #1d4ed8);
}

.dark .overflow-y-auto::-webkit-scrollbar-track {
    background: #374151;
}

.dark .overflow-y-auto::-webkit-scrollbar-thumb {
    background: linear-gradient(to bottom, #4f46e5, #3730a3);
}

/* Animation for new comments */
.comment-item {
    animation: slideInComment 0.3s ease-out;
}

@keyframes slideInComment {
    from {
        opacity: 0;
        transform: translateX(20px);
    }

    to {
        opacity: 1;
        transform: translateX(0);
    }
}

/* Button hover effects for comments */
.comment-item button {
    transition: all 0.2s ease-out;
}

.comment-item button:hover {
    transform: scale(1.05);
}

/* Multiple attachments styling */
.attachment-item {
    transition: all 0.2s ease-out;
    animation: slideInAttachment 0.3s ease-out;
}

.attachment-item:hover {
    transform: translateX(2px);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.dark .attachment-item:hover {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.attachment-preview {
    animation: fadeIn 0.3s ease-out;
}

@keyframes slideInAttachment {
    from {
        opacity: 0;
        transform: translateY(10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }
}

/* Attachment grid hover effects */
.attachment-preview .group:hover img {
    filter: brightness(1.1);
}

/* Scrollbar styling for attachment lists */
.max-h-40::-webkit-scrollbar {
    width: 4px;
}

.max-h-40::-webkit-scrollbar-track {
    background: #f1f5f9;
    border-radius: 2px;
}

.max-h-40::-webkit-scrollbar-thumb {
    background: linear-gradient(to bottom, #3b82f6, #2563eb);
    border-radius: 2px;
}

.dark .max-h-40::-webkit-scrollbar-track {
    background: #374151;
}

/* Mobile-first responsive design with tabs */
@media (max-width: 1023px) {

    /* Mobile modal uses full height more efficiently */
    .h-\[75vh\] {
        height: 85vh !important;
    }

    /* Tab transitions */
    .hidden.lg\:block {
        animation: fadeIn 0.2s ease-in-out;
    }
}

@media (max-width: 640px) {

    /* Extra mobile optimizations */
    .modal-layout {
        height: 90vh !important;
    }

    /* Better mobile padding for deadline extension */
    .deadline-extension-responsive .p-3,
    .deadline-extension-responsive .lg\:p-6 {
        padding: 0.75rem !important;
    }

    .deadline-extension-responsive .px-3,
    .deadline-extension-responsive .lg\:px-6 {
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
    }

    .deadline-extension-responsive .space-y-4,
    .deadline-extension-responsive .lg\:space-y-5>*+* {
        margin-top: 0.75rem !important;
    }

    /* Mobile attachment grid */
    .attachment-preview .grid-cols-2 {
        grid-template-columns: repeat(1, 1fr);
    }

    /* Reduce spacing on mobile */
    .space-y-4>*+* {
        margin-top: 0.75rem !important;
    }

    .lg\:space-y-4>*+* {
        margin-top: 0.75rem !important;
    }

    /* Mobile form controls */
    .grid-cols-1.sm\:grid-cols-2 {
        grid-template-columns: 1fr !important;
        gap: 0.75rem !important;
    }

    /* Better mobile buttons */
    .deadline-extend-btn {
        width: 100% !important;
        text-align: center;
    }
}

/* Custom scrollbar for separate scroll areas */
.custom-scrollbar::-webkit-scrollbar {
    width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
    background: #f1f5f9;
    border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background: linear-gradient(to bottom, #3b82f6, #2563eb);
    border-radius: 3px;
    transition: background 0.2s ease;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(to bottom, #2563eb, #1d4ed8);
}

.dark .custom-scrollbar::-webkit-scrollbar-track {
    background: #374151;
}

.dark .custom-scrollbar::-webkit-scrollbar-thumb {
    background: linear-gradient(to bottom, #4f46e5, #3730a3);
}

.dark .custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(to bottom, #3730a3, #312e81);
}

/* Tab animation */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Tab transition */
.hidden.lg\:block {
    animation: fadeIn 0.2s ease-in-out;
}
</style>