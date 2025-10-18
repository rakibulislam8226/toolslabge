<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Hero Section -->
    <section class="bg-white py-20">
      <div class="container mx-auto px-6 text-center">
        <h1 class="text-4xl font-bold mb-4">Welcome to Your Project Management Tool</h1>
        <p class="text-gray-600 mb-8">Create an organization to start managing projects and tasks efficiently.</p>

        <!-- Organization Form -->
        <form @submit.prevent="createOrganization" class="max-w-md mx-auto bg-gray-50 p-6 rounded-lg shadow">
          <div class="mb-4">
            <label class="block text-left text-gray-700 mb-2" for="name">Organization Name</label>
            <input
              type="text"
              id="name"
              v-model="organizationName"
              placeholder="Enter organization name"
              class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
          <button
            type="submit"
            class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
            :disabled="loading"
          >
            {{ loading ? "Creating..." : "Create Organization" }}
          </button>
        </form>

        <p v-if="successMessage" class="text-green-600 mt-4">{{ successMessage }}</p>
        <p v-if="errorMessage" class="text-red-600 mt-4">{{ errorMessage }}</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const organizationName = ref('')
const successMessage = ref('')
const errorMessage = ref('')
const loading = ref(false)

const createOrganization = async () => {
  successMessage.value = ''
  errorMessage.value = ''
  if (!organizationName.value) return

  loading.value = true
  try {
    const response = await axios.post('/api/v1/organizations/', {
      name: organizationName.value
    })
    successMessage.value = `Organization "${response.data.name}" created successfully!`
    organizationName.value = ''
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Something went wrong'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.container {
  max-width: 700px;
}
</style>
