import { useState, useEffect } from 'react';
import { useTasks } from './hooks/useTasks';

export default function App() {
  const [currentView, setCurrentView] = useState('tasks');
  const { tasks, loading, error, fetchTasks } = useTasks();

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex h-16 items-center justify-between">
            {/* Logo/Title */}
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-900">Pyboot Tasks</h1>
            </div>
            
            {/* Navigation */}
            <nav className="flex space-x-4">
              <button
                onClick={() => setCurrentView('tasks')}
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  currentView === 'tasks'
                    ? 'bg-gray-100 text-gray-900'
                    : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                }`}
              >
                Tasks
              </button>
              <button
                onClick={() => setCurrentView('create')}
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  currentView === 'create'
                    ? 'bg-gray-100 text-gray-900'
                    : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                }`}
              >
                New Task
              </button>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto py-6 px-4 sm:px-6 lg:px-8">
        {/* Error Message */}
        {error && (
          <div className="mb-4 bg-red-50 border-l-4 border-red-400 p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <span className="text-red-400">⚠</span>
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-700">
                  {error}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Content Views */}
        {currentView === 'tasks' && (
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">All Tasks</h2>
            
            {loading ? (
              <div className="flex justify-center py-4">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
              </div>
            ) : tasks.length === 0 ? (
              <p className="text-gray-500 text-center py-4">
                No tasks found. Create your first task!
              </p>
            ) : (
              <ul className="divide-y divide-gray-200">
                {tasks.map(task => (
                  <li key={task.id} className="py-4">
                    <div className="flex items-center">
                      <input
                        type="checkbox"
                        checked={task.completed}
                        className="h-4 w-4 text-blue-600 rounded border-gray-300"
                        onChange={() => {/* Will implement in TaskList component */}}
                      />
                      <div className="ml-3">
                        <p className={`text-sm font-medium ${
                          task.completed ? 'text-gray-400 line-through' : 'text-gray-900'
                        }`}>
                          {task.title}
                        </p>
                        {task.description && (
                          <p className="text-sm text-gray-500">{task.description}</p>
                        )}
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}
        
        {currentView === 'create' && (
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">Create New Task</h2>
            <p className="text-gray-500">Task form will go here</p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200">
        <div className="max-w-7xl mx-auto py-4 px-4">
          <p className="text-center text-sm text-gray-500">
            Pyboot Task Manager - {new Date().getFullYear()}
          </p>
        </div>
      </footer>
    </div>
  );
}