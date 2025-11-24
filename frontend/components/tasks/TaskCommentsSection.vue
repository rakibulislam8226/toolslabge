<template>
    <div class="h-full flex flex-col">
        <!-- Comments Header (hidden on mobile, shown in tabs) -->
        <div
            class="hidden lg:flex items-center justify-between mb-4 pb-3 border-b border-gray-200 dark:border-gray-700 shrink-0">
            <h3 class="text-base lg:text-lg font-semibold text-gray-900 dark:text-gray-100 flex items-center">
                <svg class="w-4 h-4 lg:w-5 lg:h-5 mr-2 text-blue-600" fill="none" stroke="currentColor"
                    viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
                Comments
            </h3>
            <span class="text-sm text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded-full">
                {{ comments.length }}
            </span>
        </div>

        <!-- Add Comment Form -->
        <div class="mb-4 bg-gray-50 dark:bg-gray-800 rounded-lg p-3 lg:p-4 shrink-0">
            <div class="flex-1">
                <!-- Comment Box with Attachment Section -->
                <div class="relative border border-gray-200 dark:border-gray-600 rounded-lg overflow-hidden bg-white dark:bg-gray-900 transition-all duration-200"
                    @dragenter="handleDragEnter" @dragleave="handleDragLeave" @dragover="handleDragOver"
                    @drop="handleDrop"
                    :class="{ 'ring-2 ring-blue-300 border-blue-300 bg-blue-50 dark:bg-blue-900/20 dark:border-blue-500': isDragOver }">
                    <!-- Textarea Container -->
                    <div class="relative">
                        <BaseTextarea ref="commentTextarea" v-model="newComment"
                            :placeholder="isDragOver ? 'Drop file here or type your comment...' : 'Add a comment... (Type @ to mention members, Ctrl+Enter to submit)'"
                            :rows="4"
                            class="comment-textarea border-0 rounded-none resize-none pr-16 transition-colors duration-200"
                            :error="commentErrors.content" @keydown="handleCommentKeydown"
                            @input="handleCommentInput" />

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

                    <!-- Mention Dropdown -->
                    <div v-if="mentionDropdownVisible"
                        class="fixed mention-dropdown bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-600 rounded-lg shadow-lg max-h-48 overflow-y-auto z-50"
                        :style="{ top: mentionPosition.top + 'px', left: mentionPosition.left + 'px' }">
                        <div v-if="filteredMentionMembers.length === 0"
                            class="px-3 py-1.5 text-sm text-gray-500 dark:text-gray-400">
                            No members found
                        </div>
                        <button v-for="(member, index) in filteredMentionMembers" :key="member.id"
                            @click="selectMentionMember(member)" :class="[
                                'mention-member-item w-full text-left px-3 py-1.5 text-sm flex items-center space-x-2',
                                selectedMentionIndex === index
                                    ? 'mention-member-selected'
                                    : 'hover:bg-blue-50 dark:hover:bg-gray-700'
                            ]">
                            <div
                                class="w-5 h-5 rounded-full bg-blue-100 dark:bg-gray-600 flex items-center justify-center shrink-0">
                                <span class="text-xs font-medium text-blue-600 dark:text-gray-300">
                                    {{ getInitials(member) }}
                                </span>
                            </div>
                            <div class="flex-1 min-w-0">
                                <div :class="[
                                    'truncate text-sm',
                                    selectedMentionIndex === index
                                        ? 'font-bold mention-selected-text'
                                        : 'font-medium text-gray-800 dark:text-gray-100'
                                ]">
                                    {{ member.user_name || member.user_email }}
                                </div>
                                <div v-if="member.user_name && member.user_email" :class="[
                                    'text-xs truncate',
                                    selectedMentionIndex === index
                                        ? 'mention-selected-email'
                                        : 'text-gray-500 dark:text-gray-400'
                                ]">
                                    {{ member.user_email }}
                                </div>
                            </div>
                        </button>
                    </div>

                    <!-- Hidden File Input -->
                    <input type="file" ref="fileInput" @change="handleFileSelect" multiple
                        accept="image/*,.pdf,.doc,.docx,.txt,.zip" class="hidden" />

                    <!-- Attachments Section Inside Comment Box -->
                    <div v-if="selectedAttachments.length > 0"
                        class="border-t border-gray-200 dark:border-gray-600 p-2 lg:p-3 bg-gray-50 dark:bg-gray-800">
                        <div class="space-y-1 lg:space-y-2 max-h-32 overflow-y-auto">
                            <div v-for="(attachment, index) in selectedAttachments" :key="`attachment-${index}`"
                                class="flex items-center space-x-2 lg:space-x-3 p-1.5 lg:p-2 bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 attachment-item">
                                <!-- File Icon/Preview -->
                                <div class="shrink-0">
                                    <div v-if="isImageFile(attachment)" class="relative cursor-pointer">
                                        <img :src="getFilePreviewUrl(attachment)" :alt="attachment.name"
                                            class="w-8 h-8 rounded object-cover border border-gray-200 dark:border-gray-600 hover:opacity-80 transition-opacity cursor-pointer"
                                            @click="previewAttachment(attachment)" />
                                    </div>
                                    <div v-else
                                        class="w-8 h-8 bg-blue-100 dark:bg-blue-900 rounded flex items-center justify-center cursor-pointer hover:bg-blue-200 dark:hover:bg-blue-800 transition-colors"
                                        @click="previewAttachment(attachment)">
                                        <svg class="w-4 h-4 text-blue-600 dark:text-blue-400" fill="none"
                                            stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                        </svg>
                                    </div>
                                </div>

                                <!-- File Name Only -->
                                <div class="flex-1 min-w-0">
                                    <p class="text-xs lg:text-sm text-gray-700 dark:text-gray-300 truncate">
                                        {{ attachment.name }}
                                    </p>
                                </div>

                                <!-- Remove Button -->
                                <button @click="removeAttachment(index)"
                                    class="text-red-400 hover:text-red-600 transition-colors cursor-pointer p-1"
                                    :title="`Remove ${attachment.name}`">
                                    <svg class="w-3 h-3 lg:w-4 lg:h-4" fill="none" stroke="currentColor"
                                        viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M6 18L18 6M6 6l12 12" />
                                    </svg>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Bottom Actions Bar Inside Comment Box -->
                <div class="border-t border-gray-200 dark:border-gray-600 px-3 py-1 bg-gray-50 dark:bg-gray-800">
                    <div
                        class="flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-2 sm:space-y-0 p-1 lg:p-2">
                        <div class="flex items-center space-x-2">
                            <div class="text-xs text-gray-500 dark:text-gray-400">
                                <div class="flex items-center space-x-1">
                                    <span :class="newComment.length > 1000 ? 'text-red-500' : ''">
                                        {{ newComment.length }}
                                    </span>
                                    <span class="text-gray-400">/1000</span>
                                </div>
                            </div>
                        </div>

                        <BaseButton variant="primary" size="sm" @click="addComment"
                            :disabled="(!newComment.trim() && selectedAttachments.length === 0) || addingComment || newComment.length > 1000"
                            :loading="addingComment" loadingText="Adding..." class="w-full sm:w-auto">
                            <template v-if="!addingComment" #icon>
                                <svg class="w-3 h-3 lg:w-4 lg:h-4" fill="none" stroke="currentColor"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
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
                    <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">Be the first to add a comment!</p>
                </div>

                <!-- Comment Items -->
                <div v-for="comment in comments" :key="comment.id"
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
                                <p class="text-xs lg:text-sm font-medium text-gray-900 dark:text-gray-100 truncate">
                                    {{ getCommentAuthorName(comment) }}
                                </p>
                                <p class="text-xs text-gray-500 dark:text-gray-400">
                                    {{ formatCommentDate(getCommentTimestamp(comment)) }}
                                    <span v-if="isCommentEdited(comment)" class="ml-1">(edited)</span>
                                </p>
                            </div>
                        </div>

                        <!-- Comment Actions -->
                        <div v-if="canEditComment(comment)" class="flex items-center space-x-1 lg:space-x-2 shrink-0">
                            <button @click="startEditComment(comment)"
                                class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors cursor-pointer p-1"
                                title="Edit comment">
                                <svg class="w-3 h-3 lg:w-4 lg:h-4" fill="none" stroke="currentColor"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.536L16.732 3.732z" />
                                </svg>
                            </button>
                            <button @click="deleteComment(comment.id)" :disabled="deletingComment === comment.id"
                                class="text-red-400 hover:text-red-600 transition-colors disabled:opacity-50 cursor-pointer p-1"
                                title="Delete comment">
                                <svg v-if="deletingComment === comment.id" class="animate-spin w-3 h-3 lg:w-4 lg:h-4"
                                    fill="none" viewBox="0 0 24 24">
                                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                        stroke-width="4" />
                                    <path class="opacity-75" fill="currentColor"
                                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                                </svg>
                                <svg v-else class="w-3 h-3 lg:w-4 lg:h-4" fill="none" stroke="currentColor"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                </svg>
                            </button>
                        </div>
                    </div>

                    <!-- Comment Content -->
                    <div v-if="editingComment?.id === comment.id">
                        <!-- Edit Form -->
                        <div class="mt-2 space-y-3">
                            <BaseTextarea v-model="editingComment.content" :rows="3" class="comment-textarea"
                                :error="commentErrors.content" />

                            <!-- Existing Attachments -->
                            <div v-if="editingComment.attachments && editingComment.attachments.length > 0"
                                class="space-y-2">
                                <h6 class="text-xs font-medium text-gray-600 dark:text-gray-400">Current Attachments
                                </h6>
                                <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2">
                                    <div v-for="attachment in editingComment.attachments" :key="attachment.id"
                                        class="relative group bg-gray-50 dark:bg-gray-700 rounded-lg p-2 border">
                                        <!-- Attachment Preview -->
                                        <div class="flex items-center space-x-2">
                                            <div v-if="isImageFile(attachment.file)" class="shrink-0">
                                                <img :src="attachment.file" :alt="getFileName(attachment.file)"
                                                    class="w-8 h-8 object-cover rounded">
                                            </div>
                                            <div v-else class="shrink-0">
                                                <svg class="w-8 h-8 text-gray-400" fill="currentColor"
                                                    viewBox="0 0 20 20">
                                                    <path
                                                        d="M4 3a2 2 0 00-2 2v1.586l.293-.293a1 1 0 011.414 0L8 10.586l2.293-2.293a1 1 0 011.414 0L14 10.586l1.293-1.293a1 1 0 011.414 0L17 9.586V5a2 2 0 00-2-2H4zM2 13.414V15a2 2 0 002 2h12a2 2 0 002-2v-1.586l-1.293 1.293a1 1 0 01-1.414 0L13 12.414l-2.293 2.293a1 1 0 01-1.414 0L7 12.414l-1.293 1.293a1 1 0 01-1.414 0L2 13.414z" />
                                                </svg>
                                            </div>
                                            <div class="flex-1 min-w-0">
                                                <p class="text-xs text-gray-600 dark:text-gray-300 truncate">
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
                                <h6 class="text-xs font-medium text-gray-600 dark:text-gray-400">New Attachments</h6>
                                <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2">
                                    <div v-for="(file, index) in editingAttachments" :key="`new-${index}`"
                                        class="relative group bg-blue-50 dark:bg-blue-900/20 rounded-lg p-2 border border-blue-200 dark:border-blue-800">
                                        <div class="flex items-center space-x-2">
                                            <div class="shrink-0">
                                                <svg class="w-8 h-8 text-blue-500" fill="currentColor"
                                                    viewBox="0 0 20 20">
                                                    <path fill-rule="evenodd"
                                                        d="M4 3a2 2 0 00-2 2v1.586l.293-.293a1 1 0 011.414 0L8 10.586l2.293-2.293a1 1 0 011.414 0L14 10.586l1.293-1.293a1 1 0 011.414 0L17 9.586V5a2 2 0 00-2-2H4zM2 13.414V15a2 2 0 002 2h12a2 2 0 002-2v-1.586l-1.293 1.293a1 1 0 01-1.414 0L13 12.414l-2.293 2.293a1 1 0 01-1.414 0L7 12.414l-1.293 1.293a1 1 0 01-1.414 0L2 13.414z"
                                                        clip-rule="evenodd" />
                                                </svg>
                                            </div>
                                            <div class="flex-1 min-w-0">
                                                <p class="text-xs text-gray-600 dark:text-gray-300 truncate">
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
                                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                                    </svg>
                                    Add Attachments
                                    <input type="file" @change="handleEditFileSelect" multiple class="hidden">
                                </label>
                            </div>

                            <div class="flex flex-col sm:flex-row justify-end space-y-2 sm:space-y-0 sm:space-x-2 mt-3">
                                <button @click="cancelEditComment"
                                    class="px-3 py-1.5 text-xs font-medium text-gray-600 hover:text-gray-800 transition-colors">
                                    Cancel
                                </button>
                                <button @click="saveEditComment"
                                    :disabled="!editingComment.content.trim() || updatingComment"
                                    class="inline-flex items-center justify-center px-3 py-1.5 text-xs font-medium bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors">
                                    <svg v-if="updatingComment" class="animate-spin -ml-1 mr-1 h-3 w-3" fill="none"
                                        viewBox="0 0 24 24">
                                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                            stroke-width="4" />
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
                            class="text-sm text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-wrap wrap-break-words overflow-wrap-anywhere">
                            {{ comment.content }}</p>

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
                                            :key="`comment-${comment.id}-attachment-${index}`"
                                            class="attachment-preview cursor-pointer"
                                            @click="openAttachment(attachment.file)">
                                            <!-- Image Preview -->
                                            <div v-if="isImageFile(attachment.file)" class="relative group">
                                                <img :src="attachment.file" :alt="getFileName(attachment.file)"
                                                    class="w-full h-20 object-cover rounded-lg shadow-sm hover:opacity-90 transition-opacity"
                                                    @error="$event.target.style.display = 'none'" />
                                                <div
                                                    class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-10 transition-all rounded-lg flex items-center justify-center">
                                                    <svg class="w-5 h-5 text-white opacity-0 group-hover:opacity-100 transition-opacity"
                                                        fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                        <path stroke-linecap="round" stroke-linejoin="round"
                                                            stroke-width="2"
                                                            d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                                                    </svg>
                                                </div>
                                            </div>
                                            <!-- File Icon for Non-Images -->
                                            <div v-else
                                                class="w-full h-20 bg-blue-100 dark:bg-blue-900/20 rounded-lg flex flex-col items-center justify-center hover:bg-blue-200 dark:hover:bg-blue-800/40 transition-colors">
                                                <svg class="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none"
                                                    stroke="currentColor" viewBox="0 0 24 24">
                                                    <path stroke-linecap="round" stroke-linejoin="round"
                                                        stroke-width="2"
                                                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                                </svg>
                                                <span
                                                    class="text-xs text-blue-600 dark:text-blue-400 mt-1 truncate max-w-full px-1">
                                                    {{ getFileName(attachment.file).substring(0, 8) }}...
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
                                        <img :src="comment.attachment[0].file"
                                            :alt="getFileName(comment.attachment[0].file)"
                                            class="w-20 h-20 object-cover rounded-lg shadow-sm hover:opacity-90 transition-opacity"
                                            @error="$event.target.style.display = 'none'" />
                                    </div>
                                    <div v-else class="inline-block">
                                        <div
                                            class="w-20 h-20 bg-blue-100 dark:bg-blue-900/20 rounded-lg flex items-center justify-center hover:bg-blue-200 dark:hover:bg-blue-800/40 transition-colors">
                                            <svg class="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none"
                                                stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                            </svg>
                                        </div>
                                        <p class="text-xs text-gray-500 dark:text-gray-400 mt-1 max-w-20 truncate">
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

    <!-- Confirmation Modal -->
    <ConfirmModal :is-open="showConfirmModal" :title="confirmModalData.title" :message="confirmModalData.message"
        :confirm-text="confirmModalData.confirmText" cancel-text="Cancel"
        confirm-class="bg-red-600 hover:bg-red-700 focus:ring-red-500" @confirm="handleConfirmAction"
        @cancel="handleCancelConfirm" />
</template>

<script setup>
import { ref, computed, nextTick, watch, inject } from 'vue'
import axios from "@/plugins/axiosConfig.js"
import { useAuth } from '@/composables/useAuth.js'
import { BaseTextarea, BaseButton } from '@/components/forms'
import ConfirmModal from '@/components/modals/ConfirmModal.vue'

const props = defineProps({
    taskId: {
        type: [Number, String],
        required: true
    },
    projectId: {
        type: [Number, String],
        required: true
    },
    projectMembers: {
        type: Array,
        default: () => []
    }
})

const emit = defineEmits(['commentsUpdated'])

const $toast = inject("toast")
const { user } = useAuth()

// Comments related data
const comments = ref([])
const newComment = ref('')
const loadingComments = ref(false)
const addingComment = ref(false)
const deletingComment = ref(null)
const updatingComment = ref(false)
const editingComment = ref(null)
const editingAttachments = ref([])
const commentErrors = ref({})

// Mention functionality
const mentionDropdownVisible = ref(false)
const mentionPosition = ref({ top: 0, left: 0 })
const mentionQuery = ref('')
const mentionStartIndex = ref(-1)
const selectedMentionIndex = ref(-1)
const commentTextarea = ref(null)

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

// Computed
const filteredMentionMembers = computed(() => {
    if (!mentionQuery.value.trim()) {
        return props.projectMembers.slice(0, 5)
    }

    const query = mentionQuery.value.toLowerCase()
    return props.projectMembers.filter(member => {
        const name = (member.user_name || '').toLowerCase()
        const email = (member.user_email || '').toLowerCase()
        return name.includes(query) || email.includes(query)
    }).slice(0, 5)
})

// Methods
const fetchComments = async () => {
    if (!props.taskId || !props.projectId) return

    try {
        loadingComments.value = true
        const response = await axios.get(`projects/${props.projectId}/tasks/${props.taskId}/comments/`)
        comments.value = response.data.data || response.data || []
        emit('commentsUpdated', comments.value)
    } catch (err) {
        console.error('Failed to fetch comments:', err)
        comments.value = []
    } finally {
        loadingComments.value = false
    }
}

const addComment = async () => {
    if ((!newComment.value.trim() && selectedAttachments.value.length === 0) || !props.taskId || !props.projectId) return

    try {
        addingComment.value = true
        commentErrors.value = {}

        // Detect mentions in comment for future backend processing
        const commentText = newComment.value.trim() || ''
        const mentionRegex = /@([\w\s\.]+?)(?=\s|$|@|[^\w\s\.])/g
        const mentions = []
        const processedUsers = new Set()
        let match

        while ((match = mentionRegex.exec(commentText)) !== null) {
            const mentionedName = match[1].trim()
            const mentionedMember = props.projectMembers.find(member => {
                const userName = (member.user_name || '').toLowerCase()
                const userEmail = (member.user_email || '').toLowerCase()
                const searchName = mentionedName.toLowerCase()

                return userName === searchName ||
                    userEmail === searchName ||
                    userName.includes(searchName) ||
                    userEmail.includes(searchName)
            })

            if (mentionedMember && !processedUsers.has(mentionedMember.user)) {
                processedUsers.add(mentionedMember.user)
                mentions.push({
                    email: mentionedMember.user_email,
                    userId: mentionedMember.user
                })
            }
        }

        // Create FormData for file uploads
        const formData = new FormData()
        formData.append('content', commentText)

        if (mentions.length > 0) {
            formData.append('mentions', JSON.stringify(mentions))
        }

        selectedAttachments.value.forEach((file) => {
            formData.append('attachment', file)
        })

        const response = await axios.post(
            `projects/${props.projectId}/tasks/${props.taskId}/comments/`,
            formData,
            {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            }
        )

        const comment = response.data.data || response.data
        comments.value.unshift(comment)

        // Reset form
        newComment.value = ''
        selectedAttachments.value = []
        hideMentionDropdown()

        $toast.success('Comment added successfully')
        emit('commentsUpdated', comments.value)
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
        attachments: comment.attachment || []
    }
    editingAttachments.value = []
    commentErrors.value = {}
}

const cancelEditComment = () => {
    editingComment.value = null
    editingAttachments.value = []
    commentErrors.value = {}
}

const saveEditComment = async () => {
    if (!editingComment.value?.content.trim() || !props.projectId) return

    try {
        updatingComment.value = true
        commentErrors.value = {}

        const formData = new FormData()
        formData.append('content', editingComment.value.content.trim())
        formData.append('process_attachments', 'true')

        editingAttachments.value.forEach((file) => {
            formData.append('attachment', file)
        })

        const attachmentsToKeep = editingComment.value.attachments || []
        attachmentsToKeep.forEach((attachment) => {
            if (attachment.id) {
                formData.append('keep_attachment_ids[]', attachment.id.toString())
            }
        })

        const response = await axios.patch(
            `projects/${props.projectId}/tasks/${props.taskId}/comments/${editingComment.value.id}/`,
            formData,
            {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }
        )
        const updatedComment = response.data.data || response.data

        const index = comments.value.findIndex(c => c.id === editingComment.value.id)
        if (index !== -1) {
            comments.value[index] = updatedComment
        }

        editingComment.value = null
        editingAttachments.value = []
        $toast.success('Comment updated successfully')
        emit('commentsUpdated', comments.value)
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
    if (!commentId || !props.projectId) return

    const comment = comments.value.find(c => c.id === commentId)
    const commentPreview = comment?.content?.length > 100
        ? comment.content.substring(0, 100) + '...'
        : comment?.content || 'this comment'

    confirmModalData.value = {
        title: 'Delete Comment',
        message: `Are you sure you want to delete this comment?\nThis action cannot be undone.`,
        confirmText: 'Delete Comment',
        action: () => performDeleteComment(commentId)
    }
    showConfirmModal.value = true
}

const performDeleteComment = async (commentId) => {
    try {
        deletingComment.value = commentId

        await axios.delete(`projects/${props.projectId}/tasks/${props.taskId}/comments/${commentId}/`)

        comments.value = comments.value.filter(c => c.id !== commentId)
        $toast.success('Comment deleted successfully')
        emit('commentsUpdated', comments.value)
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
    return comment.author?.id == user.value?.id
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

const getCommentTimestamp = (comment) => {
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
    return Math.abs(updatedTime - createdTime) > 1000
}

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
    if (mentionDropdownVisible.value) {
        if (event.key === 'ArrowDown') {
            event.preventDefault()
            selectedMentionIndex.value = Math.min(
                selectedMentionIndex.value + 1,
                filteredMentionMembers.value.length - 1
            )
        } else if (event.key === 'ArrowUp') {
            event.preventDefault()
            selectedMentionIndex.value = Math.max(
                selectedMentionIndex.value - 1,
                0
            )
        } else if (event.key === 'Enter' || event.key === 'Tab') {
            event.preventDefault()
            if (filteredMentionMembers.value[selectedMentionIndex.value]) {
                insertMention(filteredMentionMembers.value[selectedMentionIndex.value])
            }
        } else if (event.key === 'Escape') {
            hideMentionDropdown()
        }
    } else {
        if (event.ctrlKey && event.key === 'Enter') {
            event.preventDefault()
            addComment()
        }
    }
}

// Mention functionality methods
const handleCommentInput = (event) => {
    const textarea = event.target
    const value = textarea.value
    const cursorPosition = textarea.selectionStart

    const textBeforeCursor = value.substring(0, cursorPosition)
    const lastAtIndex = textBeforeCursor.lastIndexOf('@')

    if (lastAtIndex !== -1) {
        const charBeforeAt = lastAtIndex > 0 ? textBeforeCursor[lastAtIndex - 1] : ' '
        if (charBeforeAt === ' ' || charBeforeAt === '\n' || lastAtIndex === 0) {
            const mentionText = textBeforeCursor.substring(lastAtIndex + 1)

            if (!mentionText.includes(' ') && !mentionText.includes('\n')) {
                mentionQuery.value = mentionText
                mentionStartIndex.value = lastAtIndex
                selectedMentionIndex.value = 0
                showMentionDropdown(textarea)
                return
            }
        }
    }

    hideMentionDropdown()
}

const showMentionDropdown = (textarea) => {
    const rect = textarea.getBoundingClientRect()
    const lines = textarea.value.substring(0, mentionStartIndex.value).split('\n')
    const currentLineLength = lines[lines.length - 1].length

    const charWidth = 8
    const lineHeight = 20

    mentionPosition.value = {
        top: rect.top + (lines.length - 1) * lineHeight + lineHeight + window.scrollY,
        left: rect.left + currentLineLength * charWidth + window.scrollX
    }

    mentionDropdownVisible.value = true
}

const hideMentionDropdown = () => {
    mentionDropdownVisible.value = false
    mentionQuery.value = ''
    mentionStartIndex.value = -1
    selectedMentionIndex.value = -1
}

const insertMention = (member) => {
    const memberName = member.user_name || member.user_email
    const mentionText = `@${memberName} `

    const textareaComponent = commentTextarea.value
    if (!textareaComponent) return

    const value = newComment.value
    const beforeMention = value.substring(0, mentionStartIndex.value)
    const afterCursor = value.substring(mentionStartIndex.value + mentionQuery.value.length + 1)

    newComment.value = beforeMention + mentionText + afterCursor

    nextTick(() => {
        const newPosition = mentionStartIndex.value + mentionText.length

        let textareaElement = null

        if (textareaComponent.$el) {
            textareaElement = textareaComponent.$el.querySelector('textarea')
            if (!textareaElement) {
                textareaElement = textareaComponent.$el.querySelector('input')
            }
            if (!textareaElement && textareaComponent.$el.tagName === 'TEXTAREA') {
                textareaElement = textareaComponent.$el
            }
        }

        if (!textareaElement && textareaComponent.$refs && textareaComponent.$refs.input) {
            textareaElement = textareaComponent.$refs.input
        }

        if (textareaElement && typeof textareaElement.setSelectionRange === 'function') {
            textareaElement.focus()
            textareaElement.setSelectionRange(newPosition, newPosition)
        } else if (textareaElement && typeof textareaElement.selectionStart !== 'undefined') {
            textareaElement.focus()
            textareaElement.selectionStart = textareaElement.selectionEnd = newPosition
        }
    })

    hideMentionDropdown()
}

const selectMentionMember = (member) => {
    insertMention(member)
}

// Attachment functions
const handleFileSelect = (event) => {
    const files = Array.from(event.target.files)
    if (files.length > 0) {
        selectedAttachments.value = [...selectedAttachments.value, ...files]
        showAttachmentInput.value = false
    }
}

const removeAttachment = (index) => {
    if (typeof index === 'number') {
        selectedAttachments.value.splice(index, 1)
    } else {
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
        selectedAttachments.value = [...selectedAttachments.value, ...files]
        showAttachmentInput.value = false
    }
}

// Edit attachment functions
const handleEditFileSelect = (event) => {
    const files = Array.from(event.target.files)
    if (files.length > 0) {
        editingAttachments.value = [...editingAttachments.value, ...files]
    }
    event.target.value = ''
}

const removeEditAttachment = (index) => {
    editingAttachments.value.splice(index, 1)
}

const markAttachmentForDeletion = (attachment) => {
    if (editingComment.value && editingComment.value.attachments) {
        editingComment.value.attachments = editingComment.value.attachments.filter(a => a.id !== attachment.id)
    }
}

const getFilePreviewUrl = (file) => {
    if (file instanceof File) {
        return URL.createObjectURL(file)
    }
    return file
}

const isImageFile = (fileOrUrl) => {
    if (!fileOrUrl) return false

    let fileName = ''

    if (fileOrUrl instanceof File) {
        fileName = fileOrUrl.name
    } else if (typeof fileOrUrl === 'string') {
        fileName = fileOrUrl.split('/').pop() || ''
    } else if (typeof fileOrUrl === 'object' && fileOrUrl.file) {
        if (typeof fileOrUrl.file === 'string') {
            fileName = fileOrUrl.file.split('/').pop() || ''
        } else if (fileOrUrl.file instanceof File) {
            fileName = fileOrUrl.file.name
        }
    } else if (typeof fileOrUrl === 'object' && fileOrUrl.name) {
        fileName = fileOrUrl.name
    } else if (typeof fileOrUrl === 'object' && fileOrUrl.attachment) {
        if (typeof fileOrUrl.attachment === 'string') {
            fileName = fileOrUrl.attachment.split('/').pop() || ''
        }
    } else {
        return false
    }

    if (!fileName) return false

    const imageExtensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'svg']
    const extension = fileName.split('.').pop()?.toLowerCase()
    return imageExtensions.includes(extension)
}

const getFileName = (fileData) => {
    if (!fileData) return 'Unknown file'

    if (fileData instanceof File) {
        return fileData.name
    }

    if (typeof fileData === 'string') {
        return fileData.split('/').pop() || 'Unknown file'
    }

    if (typeof fileData === 'object' && fileData.file) {
        if (typeof fileData.file === 'string') {
            return fileData.file.split('/').pop() || 'Unknown file'
        }
        if (fileData.file instanceof File) {
            return fileData.file.name
        }
    }

    if (typeof fileData === 'object' && fileData.name) {
        return fileData.name
    }

    return 'Unknown file'
}

const openAttachment = (url) => {
    if (!url) return
    window.open(url, '_blank', 'noopener,noreferrer')
}

const getInitials = (member) => {
    const name = member.user_name || member.user_email
    if (!name) return '?'

    const parts = name.trim().split(' ')
    return parts.length > 1
        ? `${parts[0][0]}${parts[parts.length - 1][0]}`.toUpperCase()
        : parts[0][0].toUpperCase()
}

// Expose methods for parent component
defineExpose({
    fetchComments,
    hideMentionDropdown
})

// Watch for prop changes to refetch comments
watch(() => [props.taskId, props.projectId], ([newTaskId, newProjectId]) => {
    if (newTaskId && newProjectId) {
        fetchComments()
    }
}, { immediate: true })
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

/* Custom scrollbar */
.custom-scrollbar::-webkit-scrollbar {
    width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
    background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background: rgba(156, 163, 175, 0.5);
    border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: rgba(156, 163, 175, 0.8);
}

/* Comment textarea styling */
.comment-textarea :deep(textarea) {
    border: 0 !important;
    box-shadow: none !important;
    outline: none !important;
}

.comment-textarea :deep(textarea:focus) {
    border: 0 !important;
    box-shadow: none !important;
    outline: none !important;
}

/* Mention dropdown styling */
.mention-dropdown {
    z-index: 9999;
}

.mention-member-selected {
    background: linear-gradient(90deg, #3b82f6, #6366f1);
    color: white;
}

.mention-selected-text {
    color: white !important;
}

.mention-selected-email {
    color: rgba(255, 255, 255, 0.8) !important;
}

/* Attachment preview styling */
.attachment-item {
    transition: all 0.2s ease-in-out;
}

.attachment-item:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.attachment-preview {
    transition: all 0.2s ease-in-out;
}

.attachment-preview:hover {
    transform: scale(1.02);
}

/* Comment item styling */
.comment-item {
    transition: all 0.2s ease-in-out;
}

.comment-item:hover {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* Dark mode adjustments */
@media (prefers-color-scheme: dark) {
    .custom-scrollbar::-webkit-scrollbar-thumb {
        background: rgba(75, 85, 99, 0.5);
    }

    .custom-scrollbar::-webkit-scrollbar-thumb:hover {
        background: rgba(75, 85, 99, 0.8);
    }
}
</style>