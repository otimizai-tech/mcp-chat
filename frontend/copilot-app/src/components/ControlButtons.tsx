import React from 'react';

interface ControlButtonsProps {
  activeView: 'canvas' | 'source';
  onViewChange: (view: 'canvas' | 'source') => void;
}

export function ControlButtons({ activeView, onViewChange }: ControlButtonsProps) {
  return (
    <div className="bg-gray-100 p-1.5 rounded-lg flex space-x-2">
      <button
        onClick={() => onViewChange('canvas')}
        className={`px-3 py-1 text-sm rounded-md transition-all ${
          activeView === 'canvas'
            ? 'bg-white text-gray-800 shadow-sm'
            : 'bg-gray-200 text-gray-600 hover:bg-gray-300'
        }`}
      >
        Canvas
      </button>
      <button
        onClick={() => onViewChange('source')}
        className={`px-3 py-1 text-sm rounded-md transition-all ${
          activeView === 'source'
            ? 'bg-white text-gray-800 shadow-sm'
            : 'bg-gray-200 text-gray-600 hover:bg-gray-300'
        }`}
      >
        Source
      </button>
    </div>
  );
}
