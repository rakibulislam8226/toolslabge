<template>
  <div class="empty-container">
    <div class="empty-img">
      <!-- Updated SVG illustration -->
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
        class="icon icon-tabler icons-tabler-outline icon-tabler-error-404"
      >
        <path stroke="none" d="M0 0h24v24H0z" fill="none" />
        <path d="M3 8v3a1 1 0 0 0 1 1h3" />
        <path d="M7 8v8" />
        <path d="M17 8v3a1 1 0 0 0 1 1h3" />
        <path d="M21 8v8" />
        <path d="M10 10v4a2 2 0 1 0 4 0v-4a2 2 0 1 0 -4 0" />
      </svg>
      <!-- End of SVG -->
    </div>
    <p class="empty-title">No Data Found</p>
    <p class="empty-subtitle">
      It looks like there's nothing to display here yet.
    </p>
  </div>
</template>

<script setup>
// No additional logic required
</script>

<style scoped>
.empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1rem;
  text-align: center;
}

.empty-img {
  margin-bottom: 1rem;
}

.icon {
  width: 120px;
  height: 120px;
  color: #a0aec0; /* light gray-blue tone */
}

.empty-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0.5rem 0;
}

.empty-subtitle {
  font-size: 1rem;
  color: #6c757d;
  max-width: 300px;
}
</style>