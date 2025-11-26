<template>
    <div class="tiptap-editor-container">
        <div v-if="editor" :class="[
            'tiptap-editor',
            'border border-gray-200 dark:border-gray-600 rounded-lg overflow-hidden bg-white dark:bg-gray-900',
            'transition-all duration-200',
            { 'ring-2 ring-blue-300 border-blue-300': focused },
            { 'border-red-300 ring-1 ring-red-300': error },
            editorClass
        ]">
            <EditorContent :editor="editor" :class="[
                'prose prose-sm max-w-none',
                'p-3 min-h-[100px] focus:outline-none',
                'dark:text-gray-300 dark:prose-invert'
            ]" />

            <!-- Character counter and actions bar -->
            <div
                class="border-t border-gray-200 dark:border-gray-600 px-3 py-2 bg-gray-50 dark:bg-gray-800 flex justify-between items-center">
                <div class="text-xs text-gray-500 dark:text-gray-400">
                    <span :class="characterCount > maxLength ? 'text-red-500' : ''">
                        {{ characterCount }}
                    </span>
                    <span class="text-gray-400">/{{ maxLength }}</span>
                </div>

                <div class="flex items-center space-x-2">
                    <slot name="actions"></slot>
                </div>
            </div>
        </div>

        <!-- Error message -->
        <div v-if="error" class="mt-1 text-sm text-red-600 dark:text-red-400">
            {{ error }}
        </div>
    </div>
</template>

<script setup>
import { ref, computed, watch, onBeforeUnmount } from 'vue'
import { Editor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Mention from '@tiptap/extension-mention'
import Placeholder from '@tiptap/extension-placeholder'
import tippy from 'tippy.js'

const props = defineProps({
    modelValue: {
        type: String,
        default: ''
    },
    placeholder: {
        type: String,
        default: 'Start typing...'
    },
    mentionItems: {
        type: Array,
        default: () => []
    },
    maxLength: {
        type: Number,
        default: 1000
    },
    error: {
        type: String,
        default: ''
    },
    editorClass: {
        type: String,
        default: ''
    }
})

const emit = defineEmits(['update:modelValue', 'mention', 'focus', 'blur', 'keydown'])

const focused = ref(false)
const editor = ref(null)

// Character count
const characterCount = computed(() => {
    if (!editor.value) return 0
    return editor.value.storage.characterCount?.characters() || 0
})

// Mention suggestion component
const createMentionList = (items, command, onKeyDown) => {
    let selectedIndex = 0

    const div = document.createElement('div')
    div.className = 'mention-dropdown bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-600 rounded-lg shadow-lg max-h-48 overflow-y-auto'

    const render = () => {
        if (items.length === 0) {
            div.innerHTML = '<div class="px-3 py-2 text-sm text-gray-500 dark:text-gray-400">No members found</div>'
            return
        }

        div.innerHTML = items.map((item, index) => {
            const initial = (item.user_name || item.user_email || item.label || '?').charAt(0).toUpperCase()
            const isSelected = selectedIndex === index

            return `
                <button class="mention-item w-full text-left px-3 py-2 text-sm flex items-center space-x-2 hover:bg-blue-50 dark:hover:bg-gray-700 ${isSelected ? 'bg-blue-100 dark:bg-blue-900' : ''}" data-index="${index}">
                    <div class="w-6 h-6 rounded-full bg-blue-100 dark:bg-gray-600 flex items-center justify-center shrink-0">
                        <span class="text-xs font-medium text-blue-600 dark:text-gray-300">${initial}</span>
                    </div>
                    <div class="flex-1 min-w-0">
                        <div class="font-medium text-gray-800 dark:text-gray-100 truncate">
                            ${item.user_name || item.user_email || item.label}
                        </div>
                        ${item.user_name && item.user_email ? `<div class="text-xs text-gray-500 dark:text-gray-400 truncate">${item.user_email}</div>` : ''}
                    </div>
                </button>
            `
        }).join('')

        // Add click listeners
        div.querySelectorAll('.mention-item').forEach((button, index) => {
            button.addEventListener('click', () => selectItem(index))
        })
    }

    const selectItem = (index) => {
        const item = items[index]
        if (item) {
            command({
                id: item.id || item.user,
                label: item.user_name || item.user_email || item.label,
                email: item.user_email || item.email
            })
        }
    }

    const handleKeyDown = (event) => {
        if (event.key === 'ArrowUp') {
            selectedIndex = Math.max(0, selectedIndex - 1)
            render()
            return true
        }

        if (event.key === 'ArrowDown') {
            selectedIndex = Math.min(items.length - 1, selectedIndex + 1)
            render()
            return true
        }

        if (event.key === 'Enter') {
            selectItem(selectedIndex)
            return true
        }

        return false
    }

    render()

    return {
        element: div,
        onKeyDown: handleKeyDown,
        updateItems: (newItems) => {
            items.splice(0, items.length, ...newItems)
            selectedIndex = 0
            render()
        }
    }
}

// Mention suggestion logic
const suggestion = {
    items: ({ query }) => {
        return props.mentionItems
            .filter(item => {
                const name = (item.user_name || '').toLowerCase()
                const email = (item.user_email || '').toLowerCase()
                const searchQuery = query.toLowerCase()
                return name.includes(searchQuery) || email.includes(searchQuery)
            })
            .slice(0, 5)
    },

    render: () => {
        let mentionList
        let popup

        return {
            onStart: (props) => {
                mentionList = createMentionList(props.items, props.command)

                if (!props.clientRect) {
                    return
                }

                popup = tippy('body', {
                    getReferenceClientRect: props.clientRect,
                    appendTo: () => document.body,
                    content: mentionList.element,
                    showOnCreate: true,
                    interactive: true,
                    trigger: 'manual',
                    placement: 'bottom-start',
                })
            },

            onUpdate(props) {
                if (mentionList) {
                    mentionList.updateItems(props.items)
                }

                if (!props.clientRect) {
                    return
                }

                popup?.[0]?.setProps({
                    getReferenceClientRect: props.clientRect,
                })
            },

            onKeyDown(props) {
                if (props.event.key === 'Escape') {
                    popup?.[0]?.hide()
                    return true
                }

                return mentionList?.onKeyDown(props.event) || false
            },

            onExit() {
                popup?.[0]?.destroy()
                mentionList = null
            },
        }
    },
}

// Initialize editor
const initEditor = () => {
    editor.value = new Editor({
        content: props.modelValue,
        extensions: [
            StarterKit.configure({
                heading: false,
                codeBlock: false,
                horizontalRule: false,
                blockquote: false,
            }),
            Placeholder.configure({
                placeholder: props.placeholder,
            }),
            Mention.configure({
                HTMLAttributes: {
                    class: 'mention bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-1 py-0.5 rounded font-medium',
                },
                suggestion,
            }),
        ],
        onUpdate: ({ editor }) => {
            emit('update:modelValue', editor.getHTML())
        },
        onFocus: () => {
            focused.value = true
            emit('focus')
        },
        onBlur: () => {
            focused.value = false
            emit('blur')
        },
        editorProps: {
            handleKeyDown(view, event) {
                emit('keydown', event)

                // Handle Ctrl+Enter for submission
                if (event.ctrlKey && event.key === 'Enter') {
                    event.preventDefault()
                    return true
                }

                return false
            },
            attributes: {
                class: 'focus:outline-none'
            }
        }
    })
}

// Watch for content changes from parent
watch(() => props.modelValue, (newValue) => {
    if (editor.value && editor.value.getHTML() !== newValue) {
        editor.value.commands.setContent(newValue || '', false)
    }
})

// Public methods
const focus = () => {
    editor.value?.commands.focus()
}

const clear = () => {
    editor.value?.commands.clearContent()
}

const insertText = (text) => {
    editor.value?.commands.insertContent(text)
}

const getPlainText = () => {
    return editor.value?.getText() || ''
}

// Expose methods
defineExpose({
    focus,
    clear,
    insertText,
    getPlainText,
    editor: computed(() => editor.value)
})

// Lifecycle
initEditor()

onBeforeUnmount(() => {
    editor.value?.destroy()
})
</script>

<style scoped>
.tiptap-editor-container :deep(.ProseMirror) {
    outline: none !important;
    border: none !important;
    padding: 0 !important;
}

.tiptap-editor-container :deep(.ProseMirror p.is-editor-empty:first-child::before) {
    color: #9CA3AF;
    content: attr(data-placeholder);
    float: left;
    height: 0;
    pointer-events: none;
}

.mention-dropdown {
    z-index: 9999;
}

.mention-item {
    transition: background-color 0.1s ease;
}

/* Dark mode mention styling */
.dark .tiptap-editor-container :deep(.mention) {
    background-color: rgb(30 58 138);
    color: rgb(191 219 254);
}

/* Custom scrollbar */
.mention-dropdown::-webkit-scrollbar {
    width: 6px;
}

.mention-dropdown::-webkit-scrollbar-track {
    background: transparent;
}

.mention-dropdown::-webkit-scrollbar-thumb {
    background: rgba(156, 163, 175, 0.5);
    border-radius: 3px;
}

.mention-dropdown::-webkit-scrollbar-thumb:hover {
    background: rgba(156, 163, 175, 0.8);
}
</style>