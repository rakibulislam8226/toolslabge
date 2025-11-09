import { computed } from "vue";

export function usePermissions() {
  const userPermissions = computed(() => {
    return JSON.parse(localStorage.getItem("user"))?.permissions || [];
  });

  const hasPermission = (permission) => {
    return userPermissions.value.includes(permission);
  };

  return {
    userPermissions,
    hasPermission,
  };
}
