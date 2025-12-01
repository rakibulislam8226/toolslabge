import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    name: "home.index",
    component: () => import("@/views/home/Home.vue"),
  },
  {
    path: "/register",
    name: "auth.register",
    component: () => import("@/views/auth/Register.vue"),
    meta: { requiresGuest: true },
  },
  {
    path: "/login",
    name: "auth.login",
    component: () => import("@/views/auth/Login.vue"),
    meta: { requiresGuest: true },
  },
  {
    path: "/accept-invite",
    name: "auth.accept-invite",
    component: () => import("@/views/auth/AcceptInvite.vue"),
    meta: { requiresGuest: true },
  },
  {
    path: "/verify-email/:token",
    name: "auth.verify-email",
    component: () => import("@/views/auth/EmailVerification.vue"),
    meta: { requiresGuest: true },
  },
  {
    path: "/email-verification-required",
    name: "auth.email-verification-required",
    component: () => import("@/views/auth/EmailVerificationRequired.vue"),
    meta: { requiresGuest: true },
    props: (route) => ({ email: route.query.email }),
  },
  {
    path: "/dashboard",
    name: "dashboard.index",
    component: () => import("@/views/dashboard/Dashboard.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/projects",
    name: "projects.index",
    component: () => import("@/views/projects/ProjectsList.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/projects/:slug",
    name: "projects.details",
    component: () => import("@/views/projects/ProjectDetails.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/projects/:slug/members",
    name: "projects.members",
    component: () => import("@/views/projects/ProjectMembers.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/projects/:slug/edit",
    name: "projects.edit",
    component: () => import("@/views/projects/ProjectEdit.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/projects/:slug/tasks",
    name: "projects.tasks",
    component: () => import("@/views/projects/ProjectTasksList.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/tasks",
    name: "tasks.index",
    component: () => import("@/views/tasks/TasksList.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/organizations",
    name: "organizations.index",
    component: () => import("@/views/organizations/Organizations.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/organizations/members",
    name: "organizations.members.index",
    component: () => import("@/views/organizations/Members.vue"),
    meta: { requiresAuth: true },
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
router.beforeEach(async (to, from, next) => {
  const isAuthenticated = !!localStorage.getItem("access");
  const user = JSON.parse(localStorage.getItem("user") || "null");
  const isEmailVerified = user?.is_verified || false;

  // Allow access to auth routes for non-authenticated users
  if (to.meta.requiresGuest && isAuthenticated) {
    // If already authenticated, redirect based on verification status
    if (isEmailVerified) {
      next({ name: "dashboard.index" });
    } else {
      // Allow access to verification-related pages
      if (
        to.name?.includes("verify") ||
        to.name?.includes("email-verification")
      ) {
        next();
      } else {
        // Redirect unverified users to verification required page
        next({
          name: "auth.email-verification-required",
          query: { email: user?.email },
        });
      }
    }
  } else if (to.meta.requiresAuth && !isAuthenticated) {
    // Redirect to home if trying to access protected route without auth
    next({ name: "home.index" });
  } else if (to.meta.requiresAuth && isAuthenticated) {
    // Block unverified users from accessing protected routes except dashboard
    if (!isEmailVerified && to.name !== "dashboard.index") {
      next({
        name: "auth.email-verification-required",
        query: { email: user?.email },
      });
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
