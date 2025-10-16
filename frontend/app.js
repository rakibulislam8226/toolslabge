import { createApp } from "vue";
import App from "./App.vue";
// import router from "./router";
import iziToastPlugin from "@/plugins/izitoast.js";
import { createPinia } from "pinia";

const app = createApp(App);
const pinia = createPinia();
app.use(pinia);
app.use(router);
app.use(iziToastPlugin);
app.mount("#app");
