import { ref } from "vue";
import axios from "@/plugins/axiosConfig.js";

export function useTasks() {
  const loading = ref(false);
  const error = ref(null);

  // Helper function to build task URLs based on context
  const buildTaskUrl = (taskId = null, projectId = null, action = "") => {
    if (projectId && taskId) {
      // Nested route: /projects/{projectId}/tasks/{taskId}/
      return `/projects/${projectId}/tasks/${taskId}/${action}`;
    } else if (taskId) {
      // Direct route: /tasks/{taskId}/
      return `/tasks/${taskId}/${action}`;
    } else if (projectId) {
      // Project tasks: /projects/{projectId}/tasks/
      return `/projects/${projectId}/tasks/${action}`;
    } else {
      // All tasks: /tasks/
      return `/tasks/${action}`;
    }
  };

  const fetchTasks = async (params = {}, projectId = null) => {
    loading.value = true;
    error.value = null;

    try {
      const url = buildTaskUrl(null, projectId);
      const response = await axios.get(url, { params });

      if (response.data.status) {
        return {
          success: true,
          data: response.data.data || [],
          meta: response.data.meta || null,
        };
      } else {
        throw new Error(response.data.message || "Failed to fetch tasks");
      }
    } catch (err) {
      console.error("Error fetching tasks:", err);
      error.value =
        err.response?.data?.message ||
        "Failed to load tasks. Please try again.";
      return {
        success: false,
        data: [],
        meta: null,
        error: error.value,
      };
    } finally {
      loading.value = false;
    }
  };

  const updateTaskStatus = async (taskId, statusId, projectId = null) => {
    try {
      const url = buildTaskUrl(taskId, projectId);
      const response = await axios.patch(url, {
        status: statusId,
      });

      if (response.data.status) {
        return {
          success: true,
          data: response.data.data,
        };
      } else {
        throw new Error(
          response.data.message || "Failed to update task status"
        );
      }
    } catch (err) {
      console.error("Error updating task status:", err);
      return {
        success: false,
        error: err.response?.data?.message || "Failed to update task status",
      };
    }
  };

  const deleteTask = async (taskId, projectId = null) => {
    try {
      const url = buildTaskUrl(taskId, projectId);
      await axios.delete(url);
      return { success: true };
    } catch (err) {
      console.error("Error deleting task:", err);
      return {
        success: false,
        error: err.response?.data?.message || "Failed to delete task",
      };
    }
  };

  const extractTaskStatuses = (tasks) => {
    const statusesMap = new Map();

    tasks.forEach((task) => {
      if (task.status && task.status.id) {
        statusesMap.set(task.status.id, task.status);
      }
    });

    return Array.from(statusesMap.values());
  };

  const fetchTaskStatuses = async () => {
    // Since there's no dedicated statuses endpoint, just return empty
    // Statuses will be extracted from task data
    console.log("Using task data to extract statuses (no dedicated endpoint)");
    return {
      success: true,
      data: [],
    };
  };

  const fetchTaskById = async (taskId, projectId = null) => {
    try {
      let response;
      let url;

      if (projectId) {
        // We have project ID, use nested route directly
        url = buildTaskUrl(taskId, projectId);
        console.log("Using nested route with project ID:", url);
        response = await axios.get(url);
      } else {
        // No project ID provided, we need to get it first
        console.log("No project ID, fetching task to get project context...");

        // Step 1: Get task using direct route to extract project info
        const directUrl = buildTaskUrl(taskId, null);
        const directResponse = await axios.get(directUrl);

        if (
          directResponse.data.status &&
          directResponse.data.data.project?.id
        ) {
          const extractedProjectId = directResponse.data.data.project.id;
          console.log(
            "Extracted project ID:",
            extractedProjectId,
            "now using nested route..."
          );

          // Step 2: Make the proper nested route call
          const nestedUrl = buildTaskUrl(taskId, extractedProjectId);
          try {
            const nestedResponse = await axios.get(nestedUrl);
            if (nestedResponse.data.status) {
              console.log("Successfully used nested route:", nestedUrl);
              response = nestedResponse;
            } else {
              console.log(
                "Nested route response invalid, using direct response"
              );
              response = directResponse;
            }
          } catch (nestedErr) {
            console.warn(
              "Nested route failed:",
              nestedErr.message,
              "using direct response"
            );
            response = directResponse;
          }
        } else {
          // No project context available, use direct response
          console.log("No project context found, using direct route response");
          response = directResponse;
        }
      }

      if (response.data.status) {
        return {
          success: true,
          data: response.data.data,
        };
      } else {
        throw new Error(response.data.message || "Failed to fetch task");
      }
    } catch (err) {
      console.error("Error fetching task:", err);

      // If nested route failed and we tried it, fallback to direct route
      if (projectId && err.response?.status === 404) {
        try {
          console.log(
            "Nested route failed with 404, falling back to direct route"
          );
          const fallbackUrl = buildTaskUrl(taskId, null);
          const fallbackResponse = await axios.get(fallbackUrl);

          if (fallbackResponse.data.status) {
            console.log("Fallback successful");
            return {
              success: true,
              data: fallbackResponse.data.data,
            };
          }
        } catch (fallbackErr) {
          console.error("Fallback also failed:", fallbackErr);
        }
      }

      return {
        success: false,
        error: err.response?.data?.message || "Failed to load task",
      };
    }
  };

  return {
    loading,
    error,
    fetchTasks,
    updateTaskStatus,
    deleteTask,
    extractTaskStatuses,
    fetchTaskStatuses,
    fetchTaskById,
  };
}
