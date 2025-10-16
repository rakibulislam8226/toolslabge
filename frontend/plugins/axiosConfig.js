import axios from "axios";

const instance = axios.create({
  baseURL: "/api/v1/",
});

const metaTag = document.querySelector(`meta[name="csrf-token"]`);
const csrftoken = metaTag ? metaTag.getAttribute("content") : null;
instance.defaults.headers.common["X-CSRFToken"] = csrftoken;

// Request Interceptor
instance.interceptors.request.use(
  function (config) {
    // Add Authorization header if access token is available
    const access = localStorage.getItem("access");
    if (access) {
      config.headers["Authorization"] = `Bearer ${access}`;
    }
    return config;
  },
  function (error) {
    return Promise.reject(error);
  }
);

// Response Interceptor
instance.interceptors.response.use(
  function (response) {
    return response;
  },
  function (error) {
    if (error.response) {
      if (error.response.status === 401) {
        //
      }
    }
    if (error.response && error.response.status === 404) {
      if (error.config.method === "get") {
        // window.location.href = "/not-found";
      }
    }
    return Promise.reject(error);
  }
);

export default instance;
