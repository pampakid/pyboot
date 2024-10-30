// src/services/api.js

const API_URL = 'http://localhost:5001/api';

/**
 * Generic fetch wrapper with error handling
 */
async function fetchApi(endpoint, options = {}) {
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({
      message: 'An error occurred while fetching the data.'
    }));
    throw new Error(error.message || `HTTP error! status: ${response.status}`);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

/**
 * Task-related API calls
 */
export const taskService = {
  // Get all tasks
  getAllTasks: () => {
    return fetchApi('/tasks');
  },

  // Get a single task by ID
  getTask: (taskId) => {
    return fetchApi(`/tasks/${taskId}`);
  },

  // Create a new task
  createTask: (taskData) => {
    return fetchApi('/tasks', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  },

  // Update a task
  updateTask: (taskId, taskData) => {
    return fetchApi(`/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
  },

  // Delete a task
  deleteTask: (taskId) => {
    return fetchApi(`/tasks/${taskId}`, {
      method: 'DELETE',
    });
  }
};

/**
 * Error types for handling different API errors
 */
export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}