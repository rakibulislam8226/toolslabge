<script>
export default {
    props: {
        modelValue: { type: Number, default: 1 },
        totalPages: { type: Number, default: 1 },
    },
    emits: ["update:modelValue", "page"],
    data() {
        return {
            pages: [],
            showLeftDots: false,
            showRightDots: false,
        };
    },
    watch: {
        modelValue: {
            handler: "createPageItems",
            immediate: true,
        },
        totalPages: {
            handler: "createPageItems",
            immediate: true,
        },
    },
    methods: {
        createPageItems() {
            let min = 0;
            let max = 0;
            let isLeftDots = false;
            let isRightDots = false;

            const tempPages = [];

            if (this.totalPages > 5) {
                if (this.modelValue <= 4) {
                    min = 2;
                    max = 5;
                    isRightDots = true;
                } else if (
                    this.modelValue > 4 &&
                    this.modelValue < this.totalPages - 3
                ) {
                    min = this.modelValue - 1;
                    max = this.modelValue + 1;
                    isLeftDots = true;
                    isRightDots = true;
                } else {
                    min = this.totalPages - 4;
                    max = this.totalPages - 1;
                    isLeftDots = true;
                }
            } else {
                min = 1;
                max = this.totalPages;
            }

            for (let i = min; i <= max; i++) {
                tempPages.push(i);
            }

            this.pages = tempPages;
            this.showLeftDots = isLeftDots;
            this.showRightDots = isRightDots;
        },
        goTo(page) {
            if (this.modelValue === page) return;
            this.$emit("update:modelValue", page);
            this.$emit("page", page);
        },
        goToPrev() {
            if (this.modelValue > 1) {
                this.goTo(this.modelValue - 1);
            }
        },
        goToNext() {
            if (this.modelValue < this.totalPages) {
                this.goTo(this.modelValue + 1);
            }
        },
    },
};
</script>

<template>
    <nav v-if="totalPages" aria-label="Page navigation" class="flex justify-center">
        <ul class="flex items-center gap-1 sm:gap-2">
            <!-- Previous Button -->
            <li :class="{ 'opacity-50 pointer-events-none': modelValue === 1 }">
                <button type="button" @click="goToPrev"
                    class="px-2 py-2 sm:px-3 sm:py-2 rounded-lg border border-gray-300 text-gray-700 hover:bg-blue-50 hover:text-blue-600 hover:border-blue-300 duration-300 ease-in-out transition-all text-sm font-medium">
                    <span class="hidden sm:inline">Previous</span>
                    <svg class="w-4 h-4 sm:hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                    </svg>
                </button>
            </li>

            <!-- First page (if totalPages > 5) -->
            <li v-if="totalPages > 5">
                <button type="button" @click="goTo(1)" :class="[
                    'px-2 py-2 sm:px-3 sm:py-2 rounded-lg border border-gray-300 transition-all ease-in-out duration-300 text-sm font-medium min-w-[2.5rem] sm:min-w-[3rem]',
                    modelValue === 1
                        ? 'bg-blue-600 text-white border-blue-600 shadow-sm'
                        : 'text-gray-700 hover:bg-blue-50 hover:text-blue-600 hover:border-blue-300',
                ]">
                    1
                </button>
            </li>

            <!-- Left dots -->
            <li v-if="showLeftDots">
                <span class="px-2 py-2 sm:px-3 sm:py-2 text-gray-500 text-sm">...</span>
            </li>

            <!-- Page numbers -->
            <li v-for="page in pages" :key="page">
                <button type="button" @click="goTo(page)" :class="[
                    'px-2 py-2 sm:px-3 sm:py-2 rounded-lg border border-gray-300 transition-all ease-in-out duration-300 text-sm font-medium min-w-[2.5rem] sm:min-w-[3rem]',
                    page === modelValue
                        ? 'bg-blue-600 text-white border-blue-600 shadow-sm'
                        : 'text-gray-700 hover:text-blue-600 hover:bg-blue-50 hover:border-blue-300',
                ]">
                    {{ page }}
                </button>
            </li>

            <!-- Right dots -->
            <li v-if="showRightDots">
                <span class="px-2 py-2 sm:px-3 sm:py-2 text-gray-500 text-sm">...</span>
            </li>

            <!-- Last page (if totalPages > 5) -->
            <li v-if="totalPages > 5">
                <button type="button" @click="goTo(totalPages)" :class="[
                    'px-2 py-2 sm:px-3 sm:py-2 rounded-lg border border-gray-300 transition-all ease-in-out duration-300 text-sm font-medium min-w-[2.5rem] sm:min-w-[3rem]',
                    modelValue === totalPages
                        ? 'bg-blue-600 text-white border-blue-600 shadow-sm'
                        : 'text-gray-700 hover:text-blue-600 hover:bg-blue-50 hover:border-blue-300',
                ]">
                    {{ totalPages }}
                </button>
            </li>

            <!-- Next Button -->
            <li :class="{ 'opacity-50 pointer-events-none': modelValue === totalPages }">
                <button type="button" @click="goToNext"
                    class="px-2 py-2 sm:px-3 sm:py-2 rounded-lg border border-gray-300 text-gray-700 hover:bg-blue-50 hover:text-blue-600 hover:border-blue-300 duration-300 ease-in-out transition-all text-sm font-medium">
                    <span class="hidden sm:inline">Next</span>
                    <svg class="w-4 h-4 sm:hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                    </svg>
                </button>
            </li>
        </ul>
    </nav>
</template>
