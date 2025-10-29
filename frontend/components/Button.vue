<template>
    <button :type="type" :class="buttonClasses" :disabled="disabled || loading" @click="handleClick">
        <!-- Prepend Slot -->
        <span v-if="$slots.prepend">
            <slot name="prepend"></slot>
        </span>

        <!-- Loading Spinner -->
        <svg v-if="loading" class="animate-spin -ml-1 mr-2 h-4 w-4"
            :class="{ 'h-3 w-3': size === 'sm', 'h-5 w-5': size === 'lg' }" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
            </path>
        </svg>

        <!-- Icon Slot -->
        <span v-if="$slots.icon && !loading" class="mr-2">
            <slot name="icon"></slot>
        </span>

        <!-- Button Content -->
        <span v-if="!loading || loadingText">
            <slot>{{ loading && loadingText ? loadingText : label }}</slot>
        </span>

        <!-- Append Slot -->
        <span v-if="$slots.append">
            <slot name="append"></slot>
        </span>
    </button>
</template>

<script>
export default {
    name: 'Button',
    emits: ['click'],
    props: {
        // Content props
        label: {
            type: String,
            default: ''
        },
        loadingText: {
            type: String,
            default: ''
        },

        // Behavior props
        type: {
            type: String,
            default: 'button'
        },
        disabled: {
            type: Boolean,
            default: false
        },
        loading: {
            type: Boolean,
            default: false
        },

        // Style props
        variant: {
            type: String,
            default: 'primary',
            validator: (value) => ['primary', 'secondary', 'danger', 'ghost', 'outline'].includes(value)
        },
        size: {
            type: String,
            default: 'md',
            validator: (value) => ['sm', 'md', 'lg'].includes(value)
        },
        fullWidth: {
            type: Boolean,
            default: false
        },

        // Legacy support (will be deprecated)
        buttonClass: {
            type: String,
            default: ''
        }
    },
    computed: {
        buttonClasses() {
            // If legacy buttonClass is provided, use it for backward compatibility
            if (this.buttonClass) {
                const baseClasses = 'inline-flex items-center justify-center font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 transition-all duration-200 cursor-pointer disabled:cursor-not-allowed'
                return `${baseClasses} ${this.buttonClass}`
            }

            // Build classes based on variant, size, and state
            const classes = [
                // Base classes
                'inline-flex',
                'items-center',
                'justify-center',
                'font-medium',
                'rounded-md',
                'focus:outline-none',
                'focus:ring-2',
                'focus:ring-offset-2',
                'transition-all',
                'duration-200',
                'cursor-pointer',
                'disabled:cursor-not-allowed',

                // Size classes
                this.sizeClasses,

                // Variant classes
                this.variantClasses,

                // Width classes
                this.fullWidth ? 'w-full' : '',

                // Disabled/loading states
                (this.disabled || this.loading) ? 'disabled:opacity-50' : ''
            ]

            return classes.filter(Boolean).join(' ')
        },

        sizeClasses() {
            const sizeMap = {
                sm: 'px-3 py-2 text-sm',
                md: 'px-4 py-2.5 text-base',
                lg: 'px-6 py-3 text-lg'
            }
            return sizeMap[this.size] || sizeMap.md
        },

        variantClasses() {
            const variants = {
                primary: [
                    // Light theme - Professional blue
                    'bg-blue-600 text-white border border-blue-600 shadow-sm',
                    'hover:bg-blue-700 hover:border-blue-700 hover:shadow-md',
                    'active:bg-blue-800 active:shadow-inner',
                    'focus:ring-blue-500 focus:ring-offset-2',
                    // Dark theme
                    'dark:bg-blue-600 dark:border-blue-600',
                    'dark:hover:bg-blue-700 dark:hover:border-blue-700',
                    'dark:active:bg-blue-800',
                    'dark:focus:ring-blue-400'
                ].join(' '),

                secondary: [
                    // Light theme - Professional gray
                    'bg-white text-gray-700 border border-gray-300 shadow-sm',
                    'hover:bg-gray-50 hover:border-gray-400 hover:shadow-md',
                    'active:bg-gray-100 active:shadow-inner',
                    'focus:ring-gray-500 focus:ring-offset-2',
                    // Dark theme
                    'dark:bg-gray-800 dark:text-gray-100 dark:border-gray-600',
                    'dark:hover:bg-gray-700 dark:hover:border-gray-500',
                    'dark:active:bg-gray-600',
                    'dark:focus:ring-gray-400'
                ].join(' '),

                danger: [
                    // Light theme - Professional red
                    'bg-red-600 text-white border border-red-600 shadow-sm',
                    'hover:bg-red-700 hover:border-red-700 hover:shadow-md',
                    'active:bg-red-800 active:shadow-inner',
                    'focus:ring-red-500 focus:ring-offset-2',
                    // Dark theme
                    'dark:bg-red-600 dark:border-red-600',
                    'dark:hover:bg-red-700 dark:hover:border-red-700',
                    'dark:active:bg-red-800',
                    'dark:focus:ring-red-400'
                ].join(' '),

                ghost: [
                    // Light theme - Clean ghost
                    'bg-transparent text-gray-600 border border-transparent',
                    'hover:bg-gray-100 hover:text-gray-800',
                    'active:bg-gray-200',
                    'focus:ring-gray-500 focus:ring-offset-2',
                    // Dark theme
                    'dark:text-gray-300 dark:hover:bg-gray-800',
                    'dark:hover:text-gray-100 dark:active:bg-gray-700',
                    'dark:focus:ring-gray-400'
                ].join(' '),

                outline: [
                    // Light theme - Professional outline
                    'bg-transparent text-blue-600 border border-blue-600',
                    'hover:bg-blue-50 hover:text-blue-700 hover:border-blue-700',
                    'active:bg-blue-100',
                    'focus:ring-blue-500 focus:ring-offset-2',
                    // Dark theme
                    'dark:text-blue-400 dark:border-blue-400',
                    'dark:hover:bg-blue-900/20 dark:hover:text-blue-300',
                    'dark:hover:border-blue-300 dark:active:bg-blue-900/30',
                    'dark:focus:ring-blue-400'
                ].join(' ')
            }

            return variants[this.variant] || variants.primary
        }
    },
    methods: {
        handleClick(event) {
            if (!this.disabled && !this.loading) {
                this.$emit('click', event)
            }
        }
    }
}
</script>

<style scoped>
/* Loading animation */
@keyframes spin {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}

.animate-spin {
    animation: spin 1s linear infinite;
}

/* Focus ring offset for dark mode */
.dark button:focus {
    --tw-ring-offset-color: #1f2937;
}
</style>
