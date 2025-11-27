<template>
    <div v-html="htmlContent"></div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
    text: {
        type: String,
        default: "",
    },
    mentions: {
        type: Array,
        default: () => [],
    },
    valueKey: {
        type: String,
        default: "id",
    },
    labelKey: {
        type: String,
        default: "name",
    },
});

function getValueByPath(obj, path) {
    return path.split(".").reduce((acc, part) => acc && acc[part], obj);
}

const htmlContent = computed(() => {
    let html = "";
    let lastIndex = 0;

    props.mentions.forEach((option) => {
        const value = getValueByPath(option, props.valueKey);
        const label = getValueByPath(option, props.labelKey);
        const idx = props.text.indexOf(`@${value}`, lastIndex);
        if (idx === -1) return;

        html += props.text.slice(lastIndex, idx);
        html += `<span class="bg-blue-100 text-blue-700 rounded px-1 font-medium" contenteditable="false" data-value="${value}">@${label}</span>`;
        lastIndex = idx + String(value).length + 1;
    });

    html += props.text.slice(lastIndex);
    return html;
});
</script>