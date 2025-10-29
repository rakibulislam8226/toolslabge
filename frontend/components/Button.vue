<template>
    <button :type="type" :class="computedClass" @click="$emit('click')">
        <slot>{{ label }}</slot>
    </button>
</template>

<script>
export default {
    name: 'Button',
    props: {
        label: {
            type: String,
            default: ''
        },
        type: {
            type: String,
            default: 'button'
        },
        buttonClass: {
            type: String,
            default: ''
        }
    },
    computed: {
        computedClass() {
            // Default style for all buttons
            const defaultStyle = 'bg-blue-600 text-white px-4 py-2 rounded text-sm font-medium hover:bg-blue-700 transition duration-300 cursor-pointer';
            // If buttonClass is provided, override only the color/variant
            return this.buttonClass
                ? `${defaultStyle} ${this.buttonClass}`
                : defaultStyle;
        }
    }
}
</script>

<style scoped></style>
