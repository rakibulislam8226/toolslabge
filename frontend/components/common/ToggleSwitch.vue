<template>
    <button @click="toggle" :class="[
        'relative inline-flex items-center h-6 w-11 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
        isOn ? 'bg-blue-600' : 'bg-gray-200'
    ]" role="switch" :aria-checked="isOn">
        <span :class="[
            'pointer-events-none inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition duration-200 ease-in-out',
            isOn ? 'translate-x-5' : 'translate-x-0'
        ]" />
    </button>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
    modelValue: {
        type: Boolean,
        default: false
    }
})

const emit = defineEmits(['update:modelValue', 'change'])

const isOn = computed(() => props.modelValue)

const toggle = () => {
    const newValue = !isOn.value
    emit('update:modelValue', newValue)
    emit('change', newValue)
}
</script>

<style scoped></style>