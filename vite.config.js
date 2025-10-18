import { defineConfig } from "vite";
import { djangoVitePlugin } from "django-vite-plugin";
import vue from "@vitejs/plugin-vue";
import tailwindcss from "@tailwindcss/vite";
import path from "path";

export default defineConfig({
  server: {
    host: "0.0.0.0",
    port: 5173,
  },
  plugins: [vue(), tailwindcss(), djangoVitePlugin(["frontend/app.js"])],
  resolve: {
    alias: {
      vue: "vue/dist/vue.esm-bundler.js",
      "@": path.resolve(__dirname, "frontend"),
      "@views": path.resolve(__dirname, "frontend/views"),
      "@constants": path.resolve(__dirname, "frontend/constants"),
      "@plugins": path.resolve(__dirname, "frontend/plugins"),
      "@components": path.resolve(__dirname, "frontend/components"),
    },
  },
});
