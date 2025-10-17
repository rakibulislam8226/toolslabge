import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/home",
    name: "home.index",
    component: () => import("@/views/home/Home.vue"),
  },
  {
    path: "/:pathMatch(.*)*",
    name: "not-found",
    component: () => import("@views/errors/404.vue"),
  },
];

const router = createRouter({
  history: createWebHistory("/"),
  routes,
});
export default router;
