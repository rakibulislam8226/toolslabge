<template>
    <div class="space-y-1">
        <!-- Label -->
        <label v-if="label" :for="inputId" class="block text-sm font-medium text-gray-700" :class="labelClass">
            {{ label }}
            <span v-if="required" class="text-red-500 ml-1">*</span>
        </label>

        <!-- Textarea Field -->
        <textarea :id="inputId" :value="modelValue" :placeholder="placeholder" :required="required" :disabled="disabled"
            :readonly="readonly" :rows="rows" :class="textareaClasses" v-bind="$attrs" @input="handleInput"
            @blur="handleBlur" @focus="handleFocus"></textarea>

        <!-- Error Message -->
        <p v-if="error" class="text-sm text-red-600">
            {{ error }}
        </p>

        <!-- Helper Text -->
        <p v-if="helpText && !error" class="text-sm text-gray-500">
            {{ helpText }}
        </p>
    </div>
</template>

<script setup>
import { computed, useAttrs } from 'vue'

// Inherit attributes but exclude class to handle it manually
defineOptions({
    inheritAttrs: false
})

const props = defineProps({
    modelValue: {
        type: String,
        default: ''
    },
    label: {
        type: String,
        default: ''
    },
    placeholder: {
        type: String,
        default: ''
    },
    error: {
        type: String,
        default: ''
    },
    helpText: {
        type: String,
        default: ''
    },
    required: {
        type: Boolean,
        default: false
    },
    disabled: {
        type: Boolean,
        default: false
    },
    readonly: {
        type: Boolean,
        default: false
    },
    rows: {
        type: [String, Number],
        default: 3
    },
    size: {
        type: String,
        default: 'md',
        validator: (value) => ['sm', 'md', 'lg'].includes(value)
    },
    labelClass: {
        type: String,
        default: ''
    }
})

const emit = defineEmits(['update:modelValue', 'blur', 'focus', 'input'])

const attrs = useAttrs()

// Generate unique ID for input
const inputId = computed(() => {
    return attrs.id || `textarea-${Math.random().toString(36).substr(2, 9)}`
})

// Compute textarea classes based on props
const textareaClasses = computed(() => {
    const baseClasses = [
        'w-full',
        'border',
        'rounded-lg',
        'focus:outline-none',
        'focus:ring-2',
        'focus:ring-blue-500',
        'focus:border-transparent',
        'transition-colors',
        'duration-200',
        'resize-vertical'
    ]

    // Size classes
    const sizeClasses = {
        sm: 'px-2 py-1.5 text-sm',
        md: 'px-3 py-2 text-sm',
        lg: 'px-4 py-3 text-base'
    }

    // State classes
    const stateClasses = []

    if (props.error) {
        stateClasses.push('border-red-500', 'bg-red-50')
    } else if (props.disabled) {
        stateClasses.push('border-gray-300', 'bg-gray-100', 'text-gray-500', 'cursor-not-allowed')
    } else if (props.readonly) {
        stateClasses.push('border-gray-300', 'bg-gray-50', 'text-gray-700')
    } else {
        stateClasses.push('border-gray-300', 'bg-white', 'hover:border-gray-400')
    }

    return [
        ...baseClasses,
        sizeClasses[props.size],
        ...stateClasses,
        attrs.class || ''
    ].join(' ')
})

// Event handlers
const handleInput = (event) => {
    const value = event.target.value
    emit('update:modelValue', value)
    emit('input', event)
}

const handleBlur = (event) => {
    emit('blur', event)
}

const handleFocus = (event) => {
    emit('focus', event)
}
</script>