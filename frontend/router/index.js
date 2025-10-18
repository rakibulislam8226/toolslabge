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
    meta: { requiresGuest: true }
  },
  {
    path: "/login",
    name: "auth.login",
    component: () => import("@/views/auth/Login.vue"),
    meta: { requiresGuest: true }
  },
  {
    path: "/dashboard",
    name: "dashboard.index",
    component: () => import("@/views/dashboard/Dashboard.vue"),
    meta: { requiresAuth: true }
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

// Route guards
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('access')
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    // Redirect to home if trying to access protected route without auth
    next({ name: 'home.index' })
  } else if (to.meta.requiresGuest && isAuthenticated) {
    // Redirect to dashboard if trying to access guest-only route while authenticated
    next({ name: 'dashboard.index' })
  } else {
    next()
  }
})

export default router;
