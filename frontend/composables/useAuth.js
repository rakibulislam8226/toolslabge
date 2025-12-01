import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import axios from "@/plugins/axiosConfig.js";
import { useAuthStore } from "../stores/auth";

// Global authentication state (you could also use Pinia for this)
const accessToken = ref(localStorage.getItem("access") || null);
const refreshToken = ref(localStorage.getItem("refresh") || null);
const user = ref(JSON.parse(localStorage.getItem("user") || "null"));

export function useAuth() {
  const router = useRouter();
  const authStore = useAuthStore();

  // Computed property to check if user is authenticated
  const isAuthenticated = computed(() => !!accessToken.value);

  // Computed property to check if user email is verified
  const isEmailVerified = computed(() => user.value?.is_verified || false);

  // Login function - sets tokens and fetches user data
  const login = async (tokens, userData = null) => {
    if (tokens.access) {
      accessToken.value = tokens.access;
      localStorage.setItem("access", tokens.access);
    }

    if (tokens.refresh) {
      refreshToken.value = tokens.refresh;
      localStorage.setItem("refresh", tokens.refresh);
    }

    // Always fetch fresh user data after login
    try {
      const userInfo = await fetchUserProfile();
      if (userInfo) {
        user.value = userInfo;
        authStore.setMyInfo(userInfo);
      }
    } catch (error) {
      console.error("Failed to fetch user profile after login:", error);
    }
  };

  // Logout function - clears tokens and user data
  const logout = () => {
    accessToken.value = null;
    refreshToken.value = null;
    user.value = null;

    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("user");

    router.push("/");
  };

  // Set user data
  const setUser = (userData) => {
    user.value = userData;
    localStorage.setItem("user", JSON.stringify(userData));
  };

  // Get current tokens
  const getTokens = () => ({
    access: accessToken.value,
    refresh: refreshToken.value,
  });

  // Fetch user profile (automatically called after login)
  const fetchUserProfile = async () => {
    try {
      const response = await axios.get("users/my-info/");
      let userData;

      if (response.data.status && response.data.data) {
        userData = response.data.data;
      } else {
        userData = response.data;
      }

      // Ensure is_verified is included and stored
      if (userData && typeof userData.is_verified === "undefined") {
        userData.is_verified = false; // Default to false if not provided
      }

      setUser(userData);
      return userData;
    } catch (error) {
      console.error("Failed to fetch user profile:", error);
      return null;
    }
  };

  const hasRole = (...roles) => {
    for (let i = 0; i < roles.length; i++) {
      const role = roles[i];
      if (authStore.myInfo.organization_role === role) {
        return true;
      }
    }
    return false;
  };

  return {
    // State
    accessToken: computed(() => accessToken.value),
    refreshToken: computed(() => refreshToken.value),
    user: computed(() => user.value),
    isAuthenticated,
    isEmailVerified,

    // Methods
    login,
    logout,
    setUser,
    getTokens,
    fetchUserProfile,
    hasRole,
  };
}
