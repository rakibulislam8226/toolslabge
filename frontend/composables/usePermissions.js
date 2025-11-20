import { computed } from "vue";
import { useAuthStore } from "../stores/auth";

export function usePermissions() {
  const userPermissions = computed(() => {
    const authStore = useAuthStore()
    return authStore.myInfo.permissions || [];
  });

  const hasPermission = (permission) => {
    return userPermissions.value.includes(permission);
  };

  return {
    userPermissions,
    hasPermission,
  };
}
