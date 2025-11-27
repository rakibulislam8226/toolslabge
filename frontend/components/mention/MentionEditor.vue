<template>
    <div class="relative w-full">
        <!-- Editor -->
        <div ref="editorRef"
            class="min-h-[100px] border border-gray-300 p-2 rounded outline-none focus:ring-2 focus:ring-blue-200"
            contenteditable="true" @input="handleInput" @keydown="handleKeyDown" @click="handleClick"></div>


        <!-- Mention Dropdown -->
        <ul v-if="isDropdownVisible"
            class="absolute bg-white border border-gray-200 rounded shadow w-52 max-h-40 overflow-y-auto mt-1 z-50"
            :style="dropdownStyle">
            <li v-for="(option, idx) in suggestedOptions" :key="getValueByPath(option, valueKey)" :class="[
                'px-3 py-2 cursor-pointer',
                idx === mentionState.focusedIndex
                    ? 'bg-blue-100 font-bold'
                    : '',
            ]" @mousedown.prevent="insertMention(option)">
                @{{ getValueByPath(option, labelKey) }}
            </li>
        </ul>
    </div>
</template>

<script setup>
import {
    ref,
    reactive,
    computed,
    watch,
    nextTick,
    defineProps,
    defineEmits,
} from "vue";

/* Props */
const props = defineProps({
    modelValue: { type: Object, default: () => ({ text: "", mentions: [] }) },
    labelKey: { type: String, default: "name" },
    valueKey: { type: String, default: "username" },
    options: { type: Array, required: true },
});

const emit = defineEmits(["update:modelValue"]);

/* Helper for dot notation */
function getValueByPath(obj, path) {
    return path.split(".").reduce((acc, part) => acc && acc[part], obj);
}

function setValueByPath(obj, path, value) {
    const keys = path.split(".");
    let current = obj;
    for (let i = 0; i < keys.length - 1; i++) {
        const key = keys[i];
        if (!current[key]) current[key] = {};
        current = current[key];
    }
    current[keys[keys.length - 1]] = value;
}

/* State */
const editorRef = ref(null);
const mentionState = reactive({
    query: "",
    isVisible: false,
    position: { top: 0, left: 0 },
    focusedIndex: 0,
});

/* Computed */
const suggestedOptions = computed(() => {
    if (!mentionState.query) return props.options;
    return props.options.filter((u) => {
        const val = getValueByPath(u, props.labelKey);
        return (
            val &&
            String(val).toLowerCase().includes(mentionState.query.toLowerCase())
        );
    });
});

const isDropdownVisible = computed(
    () => mentionState.isVisible && suggestedOptions.value.length > 0
);

const dropdownStyle = computed(() => ({
    position: "absolute",
    top: mentionState.position.top + "px",
    left: mentionState.position.left + "px",
    zIndex: 1000,
}));

/* Event Handlers */
function handleInput() {
    detectTrigger();
    syncContent();
}

function handleKeyDown(e) {
    const sel = window.getSelection();
    if (!sel.rangeCount) return;
    const node = sel.anchorNode;

    // Prevent caret from entering mention span
    if (
        node &&
        node.nodeType === Node.ELEMENT_NODE &&
        node.tagName === "SPAN" &&
        node.getAttribute("contenteditable") === "false"
    ) {
        e.preventDefault();
        const range = document.createRange();
        if (e.key === "ArrowLeft") range.setStartBefore(node);
        else if (e.key === "ArrowRight") range.setStartAfter(node);
        range.collapse(true);
        sel.removeAllRanges();
        sel.addRange(range);
        return;
    }

    // Dropdown navigation
    if (isDropdownVisible.value) {
        if (e.key === "ArrowDown") {
            e.preventDefault();
            mentionState.focusedIndex =
                (mentionState.focusedIndex + 1) % suggestedOptions.value.length;
            scrollToFocusedOption();
        } else if (e.key === "ArrowUp") {
            e.preventDefault();
            mentionState.focusedIndex =
                (mentionState.focusedIndex -
                    1 +
                    suggestedOptions.value.length) %
                suggestedOptions.value.length;
            scrollToFocusedOption();
        } else if (e.key === "Enter") {
            e.preventDefault();
            insertMention(suggestedOptions.value[mentionState.focusedIndex]);
        } else if (e.key === "Escape") {
            mentionState.isVisible = false;
        }
        return;
    }
}

function handleClick() {
    mentionState.isVisible = false;
}

/* Core Logic */
function detectTrigger() {
    const sel = window.getSelection();
    if (!sel.rangeCount) return;
    const range = sel.getRangeAt(0);
    const text = range.startContainer.textContent || "";
    const upToCursor = text.slice(0, range.startOffset);
    const atIdx = upToCursor.lastIndexOf("@");

    if (atIdx !== -1) {
        mentionState.query = upToCursor.slice(atIdx + 1);
        mentionState.isVisible = true;
        mentionState.focusedIndex = 0;
        updateDropdownPosition();
    } else {
        mentionState.isVisible = false;
        mentionState.query = "";
    }
}

function insertMention(user) {
    const sel = window.getSelection();
    if (!sel.rangeCount) return;
    const range = sel.getRangeAt(0);
    const text = range.startContainer.textContent || "";
    const upToCursor = text.slice(0, range.startOffset);
    const atIdx = upToCursor.lastIndexOf("@");
    if (atIdx === -1) return;

    const mentionStart = range.startOffset - (upToCursor.length - atIdx);
    const mentionEnd = range.startOffset;
    const mentionRange = range.cloneRange();
    mentionRange.setStart(range.startContainer, mentionStart);
    mentionRange.setEnd(range.startContainer, mentionEnd);

    // Create elements
    const span = document.createElement("span");
    span.className = "bg-blue-100 text-blue-700 rounded px-1 font-medium";
    span.contentEditable = "false";
    span.dataset.value = getValueByPath(user, props.valueKey);
    span.textContent = `@${getValueByPath(user, props.labelKey)}`;

    const space = document.createTextNode("\u00A0"); // Non-breaking space

    const frag = document.createDocumentFragment();
    frag.appendChild(span);
    frag.appendChild(space);

    mentionRange.deleteContents();
    mentionRange.insertNode(frag);

    // Move caret after the space
    const newRange = document.createRange();
    newRange.setStart(space, 1);
    newRange.collapse(true);
    sel.removeAllRanges();
    sel.addRange(newRange);

    syncContent();

    mentionState.isVisible = false;
    mentionState.query = "";
}

const lastEmittedValue = ref(null);

function syncContent() {
    const childNodes = Array.from(editorRef.value.childNodes);
    let text = "";
    const mentions = [];

    childNodes.forEach((node) => {
        if (node.nodeType === Node.TEXT_NODE) {
            text += node.textContent;
        } else if (
            node.nodeType === Node.ELEMENT_NODE &&
            node.tagName === "SPAN" &&
            node.dataset.value
        ) {
            const value = node.dataset.value;

            // 1. Try to find in props.options
            let optionObj = props.options.find(
                (u) =>
                    String(getValueByPath(u, props.valueKey)) === String(value)
            );

            // 2. If not found, try to find in existing modelValue.mentions
            if (!optionObj) {
                optionObj = props.modelValue.mentions.find(
                    (m) =>
                        String(getValueByPath(m, props.valueKey)) ===
                        String(value)
                );
            }

            if (optionObj) {
                mentions.push(optionObj);
            } else {
                // Fallback: create partial object
                const partial = {};
                setValueByPath(partial, props.valueKey, value);
                setValueByPath(
                    partial,
                    props.labelKey,
                    node.textContent.slice(1)
                );
                mentions.push(partial);
            }

            text += `@${value}`;
        }
    });

    const newValue = { text, mentions };
    if (JSON.stringify(newValue) !== JSON.stringify(props.modelValue)) {
        lastEmittedValue.value = JSON.stringify(newValue);
        emit("update:modelValue", newValue);
    }
}

function updateDropdownPosition() {
    const sel = window.getSelection();
    if (!sel || !sel.rangeCount) return;

    const range = sel.getRangeAt(0);
    const rect = range.getBoundingClientRect();

    if (!editorRef.value || !editorRef.value.parentElement) return;
    const parentRect = editorRef.value.parentElement.getBoundingClientRect();

    mentionState.position.top = rect.bottom - parentRect.top + 5;
    mentionState.position.left = rect.left - parentRect.left;
}

function scrollToFocusedOption() {
    nextTick(() => {
        const items = document.querySelectorAll(".absolute ul li");
        if (!items.length) return;
        const item = items[mentionState.focusedIndex];
        if (item) item.scrollIntoView({ block: "nearest" });
    });
}

/* Watcher */
watch(
    () => props.modelValue,
    (val) => {
        console.log('Model value changed:', val);
        if (JSON.stringify(val) === lastEmittedValue.value) {
            return;
        }

        nextTick(() => {
            if (!editorRef.value) return;
            editorRef.value.innerHTML = "";

            let html = "";
            let lastIndex = 0;
            const { text, mentions } = val || { text: "", mentions: [] };

            mentions.forEach((option) => {
                const value = getValueByPath(option, props.valueKey);
                const label = getValueByPath(option, props.labelKey);
                const idx = text.indexOf(`@${value}`, lastIndex);
                if (idx === -1) return;

                html += text.slice(lastIndex, idx);
                html += `<span class="bg-blue-100 text-blue-700 rounded px-1 font-medium" contenteditable="false" data-value="${value}">@${label}</span>`;
                lastIndex = idx + String(value).length + 1;
            });

            html += text.slice(lastIndex);
            editorRef.value.innerHTML = html;

            const sel = window.getSelection();
            const range = document.createRange();

            let lastNode = editorRef.value.lastChild;

            if (!lastNode) {
                lastNode = document.createTextNode("");
                editorRef.value.appendChild(lastNode);
            }

            if (lastNode.nodeType === Node.ELEMENT_NODE) {
                const textNode = document.createTextNode("");
                editorRef.value.appendChild(textNode);
                lastNode = textNode;
            }

            range.setStart(lastNode, lastNode.textContent.length);
            range.collapse(true);
            sel.removeAllRanges();
            sel.addRange(range);
        });
    },
    {
        immediate: true,
        deep: true,
    }
);
</script>
