import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    name: "home.index",
    component: () => import("@/views/home/Home.vue"),
  },
  {
    path: "/home",
    name: "home",
    component: () => import("@/views/home/Home.vue"),
  },
  {
    path: "/register",
    name: "auth.register",
    component: () => import("@/views/auth/Register.vue"),
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
