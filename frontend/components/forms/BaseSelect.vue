<template>
    <div class="space-y-1">
        <!-- Label -->
        <label v-if="label" :for="inputId" class="block text-sm font-medium text-gray-700" :class="labelClass">
            {{ label }}
            <span v-if="required" class="text-red-500 ml-1">*</span>
        </label>

        <!-- Select Field -->
        <select :id="inputId" :value="modelValue" :required="required" :disabled="disabled" :class="selectClasses"
            v-bind="$attrs" @change="handleChange" @blur="handleBlur" @focus="handleFocus">
            <!-- Default option -->
            <option v-if="placeholder" value="" disabled>
                {{ placeholder }}
            </option>

            <!-- Options -->
            <option v-for="option in options" :key="getOptionValue(option)" :value="getOptionValue(option)">
                {{ getOptionLabel(option) }}
            </option>
        </select>

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
        type: [String, Number],
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
    options: {
        type: Array,
        default: () => []
    },
    optionValue: {
        type: String,
        default: 'value'
    },
    optionLabel: {
        type: String,
        default: 'label'
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

const emit = defineEmits(['update:modelValue', 'blur', 'focus', 'change'])

const attrs = useAttrs()

// Generate unique ID for input
const inputId = computed(() => {
    return attrs.id || `select-${Math.random().toString(36).substr(2, 9)}`
})

// Compute select classes based on props
const selectClasses = computed(() => {
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
        'appearance-none',
        'bg-no-repeat',
        'bg-right',
        'pr-8'
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

// Utility functions for options
const getOptionValue = (option) => {
    if (typeof option === 'object' && option !== null) {
        return option[props.optionValue]
    }
    return option
}

const getOptionLabel = (option) => {
    if (typeof option === 'object' && option !== null) {
        return option[props.optionLabel]
    }
    return option
}

// Event handlers
const handleChange = (event) => {
    const value = event.target.value
    emit('update:modelValue', value)
    emit('change', event)
}

const handleBlur = (event) => {
    emit('blur', event)
}

const handleFocus = (event) => {
    emit('focus', event)
}
</script>

<style scoped>
/* Custom dropdown arrow */
select {
    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
    background-position: right 0.5rem center;
    background-size: 1.5em 1.5em;
}
</style>