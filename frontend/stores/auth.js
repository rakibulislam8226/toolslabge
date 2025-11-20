import { defineStore } from "pinia";

function getUserInfo() {
  const userInfo = localStorage.getItem("user");
  if (!userInfo) return null;
  return JSON.parse(userInfo);
}

export const useAuthStore = defineStore("auth", {
  state: () => ({
    myInfo: getUserInfo(),
  }),

  actions: {
    setMyInfo(info) {
      this.myInfo = { ...info };
      localStorage.setItem("user", JSON.stringify(this.myInfo));
    },
  },
});
