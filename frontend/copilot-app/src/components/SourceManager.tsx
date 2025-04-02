import { useState } from 'react';
import { useSourceManager } from '../hooks/useSourceManager';
import { Plus, Trash2 } from 'lucide-react';

export function SourceManager() {
  const { sources, addSource, deleteSource } = useSourceManager();
  const [newSourceName, setNewSourceName] = useState('');

  const handleAddSource = () => {
    if (newSourceName.trim()) {
      addSource(newSourceName.trim());
      setNewSourceName('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleAddSource();
    }
  };

  return (
    <div className="p-6 bg-white dark:bg-gray-900 h-full">
      <div className="mb-6">
        <h2 className="text-2xl font-semibold mb-2 text-gray-800 dark:text-white">Data Sources</h2>
        <p className="text-gray-600 dark:text-gray-300">Manage your data sources here</p>
      </div>

      {/* Add new source */}
      <div className="mb-6">
        <div className="flex gap-2">
          <input
            type="text"
            value={newSourceName}
            onChange={(e) => setNewSourceName(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="Enter source name"
            className="flex-1 p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700 dark:text-white"
          />
          <button
            onClick={handleAddSource}
            disabled={!newSourceName.trim()}
            className={`p-2 rounded-lg flex items-center gap-2 ${
              !newSourceName.trim()
                ? 'bg-gray-200 text-gray-400 dark:bg-gray-700 dark:text-gray-500'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            <Plus size={20} />
            Add
          </button>
        </div>
      </div>

      {/* Sources list */}
      <div className="space-y-2">
        {sources.map((source) => (
          <div
            key={source.id}
            className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg"
          >
            <span className="text-gray-800 dark:text-gray-200">{source.name}</span>
            <button
              onClick={() => deleteSource(source.id)}
              className="p-1 text-red-600 hover:bg-red-100 dark:hover:bg-red-900 rounded-lg transition-colors"
              aria-label="Delete source"
            >
              <Trash2 size={18} />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
