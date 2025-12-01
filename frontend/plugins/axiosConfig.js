import axios from "axios";

const instance = axios.create({
  baseURL: "/api/v1/",
});

// Function to get CSRF token from meta tag or cookies
function getCSRFToken() {
  // First try to get from meta tag
  const metaTag = document.querySelector(`meta[name="csrf-token"]`);
  if (metaTag) {
    return metaTag.getAttribute("content");
  }

  // Fallback to cookie
  const name = "csrftoken";
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Set CSRF token
const csrftoken = getCSRFToken();
if (csrftoken) {
  instance.defaults.headers.common["X-CSRFToken"] = csrftoken;
}

// Request Interceptor
instance.interceptors.request.use(
  function (config) {
    // Add Authorization header if access token is available
    const access = localStorage.getItem("access");
    if (access) {
      config.headers["Authorization"] = `Bearer ${access}`;
    }

    // Ensure CSRF token is set for each request
    if (!config.headers["X-CSRFToken"]) {
      const csrfToken = getCSRFToken();
      if (csrfToken) {
        config.headers["X-CSRFToken"] = csrfToken;
      }
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
