<template>
    <div class="space-y-1">
        <!-- Label -->
        <label v-if="label" :for="inputId" class="block text-sm font-medium text-gray-700" :class="labelClass">
            {{ label }}
            <span v-if="required" class="text-red-500 ml-1">*</span>
        </label>

        <!-- Flatpickr Input -->
        <flat-pickr :id="inputId" :model-value="computedValue || null" :config="flatpickrConfig"
            :placeholder="placeholder" :class="inputClasses" v-bind="$attrs" @update:model-value="handleInput"
            @blur="handleBlur" @focus="handleFocus" />

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
import flatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'

// Inherit attributes but exclude class to handle it manually
defineOptions({
    inheritAttrs: false
})

const props = defineProps({
    modelValue: {
        type: [String, Date],
        default: null
    },
    label: {
        type: String,
        default: ''
    },
    placeholder: {
        type: String,
        default: 'Select date & time'
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
    enableTime: {
        type: Boolean,
        default: true
    },
    dateFormat: {
        type: String,
        default: 'Y-m-d H:i'
    },
    altFormat: {
        type: String,
        default: 'F j, Y \\a\\t H:i'
    },
    time24hr: {
        type: Boolean,
        default: false
    },
    minuteIncrement: {
        type: Number,
        default: 30
    },
    size: {
        type: String,
        default: 'md',
        validator: (value) => ['sm', 'md', 'lg'].includes(value)
    },
    labelClass: {
        type: String,
        default: ''
    },
    config: {
        type: Object,
        default: () => ({})
    }
})

const emit = defineEmits(['update:modelValue', 'blur', 'focus', 'input', 'change'])

const attrs = useAttrs()

// Computed properties
const computedValue = computed(() => {
    // Convert empty string to null for FlatPickr
    if (props.modelValue === '' || props.modelValue === undefined) {
        return null
    }
    return props.modelValue
})

// Generate unique ID for input
const inputId = computed(() => {
    return attrs.id || `datepicker-${Math.random().toString(36).substr(2, 9)}`
})

// Flatpickr configuration
const flatpickrConfig = computed(() => {
    const defaultConfig = {
        enableTime: props.enableTime,
        dateFormat: props.dateFormat,
        altInput: true,
        altFormat: props.altFormat,
        time_24hr: props.time24hr,
        allowInput: true,
        clickOpens: true,
        defaultDate: null,
        minuteIncrement: props.minuteIncrement,
        // Ensure empty value handling
        onReady: function (selectedDates, dateStr, instance) {
            if (!dateStr || dateStr === '') {
                instance.clear();
            }
        }
    }

    return {
        ...defaultConfig,
        ...props.config
    }
})

// Compute input classes based on props
const inputClasses = computed(() => {
    const baseClasses = [
        'w-full',
        'border',
        'rounded-lg',
        'focus:outline-none',
        'focus:ring-2',
        'focus:ring-blue-500',
        'focus:border-transparent',
        'transition-colors',
        'duration-200'
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
    let value = Array.isArray(event) && event.length > 0 ? event[0] : event

    if (value instanceof Date) {
        // Format date to YYYY-MM-DD for backend compatibility
        const year = value.getFullYear()
        const month = String(value.getMonth() + 1).padStart(2, '0')
        const day = String(value.getDate()).padStart(2, '0')

        if (props.enableTime) {
            // If time is enabled, include time in ISO format
            value = value.toISOString()
        } else {
            // If only date, format as YYYY-MM-DD
            value = `${year}-${month}-${day}`
        }
    } else if (value === '' || value === undefined) {
        // Convert empty values to null
        value = null
    }

    emit('update:modelValue', value)
    emit('input', value)
}

const handleBlur = (event) => {
    emit('blur', event)
}

const handleFocus = (event) => {
    emit('focus', event)
}
</script>