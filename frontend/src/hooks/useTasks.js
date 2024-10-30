// src/hooks/useTasks.js

import { useState, useCallback } from 'react';
import { taskService } from '../services/api';

export function useTasks() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchTasks = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await taskService.getAllTasks();
      setTasks(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  const createTask = useCallback(async (taskData) => {
    setError(null);
    try {
      const newTask = await taskService.createTask(taskData);
      setTasks(current => [...current, newTask]);
      return newTask;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, []);

  const updateTask = useCallback(async (taskId, taskData) => {
    setError(null);
    try {
      const updatedTask = await taskService.updateTask(taskId, taskData);
      setTasks(current => 
        current.map(task => task.id === taskId ? updatedTask : task)
      );
      return updatedTask;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, []);

  const deleteTask = useCallback(async (taskId) => {
    setError(null);
    try {
      await taskService.deleteTask(taskId);
      setTasks(current => current.filter(task => task.id !== taskId));
    } catch (err) {
      setError(err.message);
      throw err;
    }
  }, []);

  return {
    tasks,
    loading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
  };
}