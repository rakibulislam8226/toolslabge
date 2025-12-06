<template>
    <div class="min-h-screen transition-colors duration-300" :class=" isDark ? 'bg-slate-900' : 'bg-gray-50' ">
        <div class="max-w-2xl mx-auto p-6">
            <!-- Header -->
            <div class="mb-10">
                <div class="flex items-center gap-4 mb-6">
                    <router-link to="/profile" class="p-3 rounded-xl transition-all duration-300 hover:scale-110 group"
                        :class=" isDark ? 'text-slate-300 hover:bg-slate-700 hover:text-white' : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900' ">
                        <svg class="w-5 h-5 transition-transform duration-300 group-hover:-translate-x-1" fill="none"
                            stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                        </svg>
                    </router-link>
                    <div>
                        <h1 class="text-4xl font-bold transition-colors duration-300 bg-gradient-to-r bg-clip-text text-transparent"
                            :class=" isDark ? 'from-cyan-400 to-blue-400' : 'from-indigo-600 to-purple-600' ">
                            Change Password
                        </h1>
                        <p class="text-sm mt-2 transition-colors duration-300"
                            :class=" isDark ? 'text-slate-400' : 'text-gray-500' ">
                            Keep your account secure with a strong password
                        </p>
                    </div>
                </div>
            </div>

            <!-- Change Password Form -->
            <div class="relative">
                <!-- Card with enhanced styling -->
                <div class="rounded-2xl shadow-xl border backdrop-blur-sm transition-all duration-300 overflow-hidden"
                    :class=" isDark ? 'bg-slate-800/90 border-slate-700/60 shadow-slate-900/20' : 'bg-white/90 border-gray-200/60 shadow-gray-900/10' ">

                    <!-- Gradient accent -->
                    <div class="h-1 bg-gradient-to-r"
                        :class=" isDark ? 'from-cyan-500 to-blue-500' : 'from-indigo-500 to-purple-500' "></div>

                    <form @submit.prevent=" handleSubmit " class="p-8 space-y-8">


                        <!-- Password Fields -->
                        <div class="space-y-6">
                            <div>
                                <div class="relative">
                                    <BaseInput v-model=" form.current_password "
                                        :type=" showCurrentPassword ? 'text' : 'password' " label="Current Password"
                                        placeholder="Enter your current password"
                                        :error=" getErrorMessage('current_password') " />
                                    <button type="button" @click="showCurrentPassword = !showCurrentPassword"
                                        class="absolute right-3 top-8 p-1 rounded transition-colors duration-200"
                                        :class=" isDark ? 'text-slate-400 hover:text-slate-200' : 'text-gray-400 hover:text-gray-600' ">
                                        <svg v-if="showCurrentPassword" class="w-5 h-5" fill="none"
                                            stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21" />
                                        </svg>
                                        <svg v-else class="w-5 h-5" fill="none" stroke="currentColor"
                                            viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                        </svg>
                                    </button>
                                </div>
                            </div>

                            <div>
                                <div class="relative">
                                    <BaseInput v-model=" form.new_password "
                                        :type=" showNewPassword ? 'text' : 'password' " label="New Password"
                                        placeholder="Enter your new password"
                                        :error=" getErrorMessage('new_password') " />
                                    <button type="button" @click="showNewPassword = !showNewPassword"
                                        class="absolute right-3 top-8 p-1 rounded transition-colors duration-200"
                                        :class=" isDark ? 'text-slate-400 hover:text-slate-200' : 'text-gray-400 hover:text-gray-600' ">
                                        <svg v-if="showNewPassword" class="w-5 h-5" fill="none" stroke="currentColor"
                                            viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21" />
                                        </svg>
                                        <svg v-else class="w-5 h-5" fill="none" stroke="currentColor"
                                            viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                        </svg>
                                    </button>
                                </div>

                                <!-- Password Strength Indicator -->
                                <div v-if="form.new_password" class="mt-3 space-y-2">
                                    <div class="flex items-center gap-2 text-xs">
                                        <span :class=" isDark ? 'text-slate-400' : 'text-gray-600' ">Strength:</span>
                                        <div class="flex gap-1">
                                            <div class="h-1 w-6 rounded"
                                                :class=" passwordValidation.strength >= 1 ? 'bg-red-500' : (isDark ? 'bg-slate-600' : 'bg-gray-200') ">
                                            </div>
                                            <div class="h-1 w-6 rounded"
                                                :class=" passwordValidation.strength >= 2 ? 'bg-yellow-500' : (isDark ? 'bg-slate-600' : 'bg-gray-200') ">
                                            </div>
                                            <div class="h-1 w-6 rounded"
                                                :class=" passwordValidation.strength >= 3 ? 'bg-green-500' : (isDark ? 'bg-slate-600' : 'bg-gray-200') ">
                                            </div>
                                        </div>
                                        <span class="text-xs" :class=" passwordValidation.color ">
                                            {{ passwordValidation.text }}
                                        </span>
                                    </div>

                                    <!-- Requirements List -->
                                    <div class="space-y-1 text-xs">
                                        <div class="flex items-center gap-2">
                                            <svg class="w-3 h-3"
                                                :class=" passwordValidation.hasMinLength ? 'text-green-500' : (isDark ? 'text-slate-500' : 'text-gray-400') "
                                                fill="currentColor" viewBox="0 0 20 20">
                                                <path fill-rule="evenodd"
                                                    d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                                    clip-rule="evenodd" />
                                            </svg>
                                            <span
                                                :class=" passwordValidation.hasMinLength ? 'text-green-500' : (isDark ? 'text-slate-400' : 'text-gray-500') ">At
                                                least 8 characters</span>
                                        </div>
                                        <div class="flex items-center gap-2">
                                            <svg class="w-3 h-3"
                                                :class=" passwordValidation.hasLowercase ? 'text-green-500' : (isDark ? 'text-slate-500' : 'text-gray-400') "
                                                fill="currentColor" viewBox="0 0 20 20">
                                                <path fill-rule="evenodd"
                                                    d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                                    clip-rule="evenodd" />
                                            </svg>
                                            <span
                                                :class=" passwordValidation.hasLowercase ? 'text-green-500' : (isDark ? 'text-slate-400' : 'text-gray-500') ">Lowercase
                                                letter</span>
                                        </div>
                                        <div class="flex items-center gap-2">
                                            <svg class="w-3 h-3"
                                                :class=" passwordValidation.hasUppercase ? 'text-green-500' : (isDark ? 'text-slate-500' : 'text-gray-400') "
                                                fill="currentColor" viewBox="0 0 20 20">
                                                <path fill-rule="evenodd"
                                                    d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                                    clip-rule="evenodd" />
                                            </svg>
                                            <span
                                                :class=" passwordValidation.hasUppercase ? 'text-green-500' : (isDark ? 'text-slate-400' : 'text-gray-500') ">Uppercase
                                                letter</span>
                                        </div>
                                        <div class="flex items-center gap-2">
                                            <svg class="w-3 h-3"
                                                :class=" passwordValidation.hasNumber ? 'text-green-500' : (isDark ? 'text-slate-500' : 'text-gray-400') "
                                                fill="currentColor" viewBox="0 0 20 20">
                                                <path fill-rule="evenodd"
                                                    d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                                    clip-rule="evenodd" />
                                            </svg>
                                            <span
                                                :class=" passwordValidation.hasNumber ? 'text-green-500' : (isDark ? 'text-slate-400' : 'text-gray-500') ">Number</span>
                                        </div>
                                        <div class="flex items-center gap-2">
                                            <svg class="w-3 h-3"
                                                :class=" passwordValidation.hasSpecialChar ? 'text-green-500' : (isDark ? 'text-slate-500' : 'text-gray-400') "
                                                fill="currentColor" viewBox="0 0 20 20">
                                                <path fill-rule="evenodd"
                                                    d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                                    clip-rule="evenodd" />
                                            </svg>
                                            <span
                                                :class=" passwordValidation.hasSpecialChar ? 'text-green-500' : (isDark ? 'text-slate-400' : 'text-gray-500') ">Special
                                                character</span>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div>
                                <div class="relative">
                                    <BaseInput v-model=" form.confirm_password "
                                        :type=" showConfirmPassword ? 'text' : 'password' " label="Confirm New Password"
                                        placeholder="Confirm your new password"
                                        :error=" getErrorMessage('confirm_password') " />
                                    <button type="button" @click="showConfirmPassword = !showConfirmPassword"
                                        class="absolute right-3 top-8 p-1 rounded transition-colors duration-200"
                                        :class=" isDark ? 'text-slate-400 hover:text-slate-200' : 'text-gray-400 hover:text-gray-600' ">
                                        <svg v-if="showConfirmPassword" class="w-5 h-5" fill="none"
                                            stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21" />
                                        </svg>
                                        <svg v-else class="w-5 h-5" fill="none" stroke="currentColor"
                                            viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                        </svg>
                                    </button>
                                </div>

                                <!-- Password Match Indicator -->
                                <div v-if="form.confirm_password" class="mt-2 flex items-center gap-2 text-xs">
                                    <svg class="w-3 h-3" :class=" passwordsMatch ? 'text-green-500' : 'text-red-500' "
                                        fill="currentColor" viewBox="0 0 20 20">
                                        <path v-if="passwordsMatch" fill-rule="evenodd"
                                            d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                            clip-rule="evenodd" />
                                        <path v-else fill-rule="evenodd"
                                            d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                                            clip-rule="evenodd" />
                                    </svg>
                                    <span :class=" passwordsMatch ? 'text-green-500' : 'text-red-500' ">
                                        {{ passwordsMatch ? 'Passwords match' : 'Passwords do not match' }}
                                    </span>
                                </div>
                            </div>
                        </div>

                        <!-- Action Buttons -->
                        <Button type="submit" variant="primary" size="lg" :loading=" loading "
                            :disabled=" !isFormValid " class="order-1 sm:order-2 min-w-[160px]">
                            <template #icon v-if="!loading">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                                </svg>
                            </template>
                            {{ loading ? 'Updating...' : 'Update' }}
                        </Button>

                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, computed, inject } from 'vue';
import { useRouter } from 'vue-router';
import { useTheme } from '@/composables/useTheme.js';
import axios from '@/plugins/axiosConfig.js';
import Button from '@/components/Button.vue';
import { BaseInput } from '@/components/forms';

const $toast = inject("toast")

const { isDark } = useTheme();
const router = useRouter();

const loading = ref(false);
const errors = ref({});
const showCurrentPassword = ref(false);
const showNewPassword = ref(false);
const showConfirmPassword = ref(false);

const form = reactive({
    current_password: '',
    new_password: '',
    confirm_password: ''
});

// Password validation regex patterns (cached for performance)
const PASSWORD_PATTERNS = {
    lowercase: /[a-z]/,
    uppercase: /[A-Z]/,
    number: /[0-9]/,
    special: /[!@#$%^&*(),.?":{}|<>]/
};

// Combined password validation computed properties
const passwordValidation = computed(() => {
    const password = form.new_password;
    const hasLowercase = PASSWORD_PATTERNS.lowercase.test(password);
    const hasUppercase = PASSWORD_PATTERNS.uppercase.test(password);
    const hasNumber = PASSWORD_PATTERNS.number.test(password);
    const hasSpecialChar = PASSWORD_PATTERNS.special.test(password);
    const hasMinLength = password.length >= 8;

    let strength = 0;
    if (hasMinLength) strength++;
    if (hasLowercase && hasUppercase) strength++;
    if (hasNumber && hasSpecialChar) strength++;

    return {
        hasLowercase,
        hasUppercase,
        hasNumber,
        hasSpecialChar,
        hasMinLength,
        strength,
        text: ['Weak', 'Weak', 'Medium', 'Strong'][strength] || 'Weak',
        color: ['text-red-500', 'text-red-500', 'text-yellow-500', 'text-green-500'][strength] || 'text-red-500'
    };
});

const passwordsMatch = computed(() =>
    form.new_password === form.confirm_password && form.confirm_password.length > 0
);

const isFormValid = computed(() => {
    const validation = passwordValidation.value;
    return form.current_password.length > 0 &&
        validation.hasMinLength &&
        validation.hasLowercase &&
        validation.hasUppercase &&
        validation.hasNumber &&
        validation.hasSpecialChar &&
        passwordsMatch.value;
});

const getErrorMessage = (field) => {
    const errorData = errors.value;

    // Handle nested API response format
    if (errorData.data?.errors?.length) {
        const fieldError = errorData.data.errors.find(error => error[field]);
        if (fieldError) return fieldError[field];
    }

    // Handle direct field errors
    const directError = errorData[field];
    return Array.isArray(directError) ? directError[0] : directError || '';
};

const clearForm = () => {
    Object.assign(form, {
        current_password: '',
        new_password: '',
        confirm_password: ''
    });
};

const handleSubmit = async () => {
    if (loading.value) return;

    loading.value = true;
    errors.value = {};

    try {
        const { data } = await axios.patch('users/password-reset/update-password/', form);
        console.log('Success response:', data);

        $toast.success(data?.message || 'Password updated successfully!');
        clearForm();
        router.push('/profile');

    } catch (error) {
        console.log('Error response:', error.response?.data);
        errors.value = error.response?.data || { general: 'An error occurred. Please try again.' };
    } finally {
        loading.value = false;
    }
};
</script>