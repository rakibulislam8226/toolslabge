import { defineConfig } from "vite";
import { djangoVitePlugin } from "django-vite-plugin";
import vue from "@vitejs/plugin-vue";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  server: {
    host: "0.0.0.0",
    port: 5173,
  },
  plugins: [vue(), tailwindcss(), djangoVitePlugin(["frontend/app.js"])],
  resolve: {
    alias: {
      vue: "vue/dist/vue.esm-bundler.js",
      "@": "/frontend",
      "@views": "/frontend/views",
      "@constants": "/frontend/constants",
      "@plugins": "/frontend/plugins",
    },
  },
});
