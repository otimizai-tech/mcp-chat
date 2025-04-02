'use client';

import React from 'react';
import { X } from 'lucide-react';

interface CanvasCopilotProps {
  isOpen: boolean;
  onClose: () => void;
  content: string;
  title: string;
  onContentChange?: (content: string) => void;
}

export function CanvasCopilot({ isOpen, onClose, content, title, onContentChange }: CanvasCopilotProps) {
  return (
    <div
      className={`bg-white dark:bg-gray-800 rounded-lg shadow-md transition-all duration-300 ease-in-out transform ${
        isOpen ? 'w-full opacity-100 h-full scale-100' : 'w-0 opacity-0 h-0 scale-95'
      } overflow-hidden`}
      role="complementary"
      aria-label="Editor de texto"
    >
      <div className={`h-full flex flex-col transition-all duration-300 ease-in-out transform ${
        isOpen ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-4'
      }`}>
        <div className="flex items-center justify-between px-3 py-2 border-b dark:border-gray-700 bg-gray-50/50 dark:bg-gray-800/50">
          <h2 className="text-sm font-semibold text-black dark:text-white">{title}</h2>
          <button
            onClick={onClose}
            className="rounded-sm opacity-70 transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400"
            aria-label="Fechar editor"
          >
            <X className="h-3 w-3 text-black dark:text-white" />
            <span className="sr-only">Fechar</span>
          </button>
        </div>
        <div className="flex-1 overflow-auto p-2">
          <textarea
            value={content}
            onChange={(e) => onContentChange?.(e.target.value)}
            className="w-full h-full p-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 dark:bg-gray-700 dark:text-white dark:border-gray-600 text-sm resize-none"
            placeholder="Digite seu texto aqui..."
            autoFocus={isOpen}
            disabled={!onContentChange}
            aria-label="Área de edição de texto"
          />
        </div>
      </div>
    </div>
  );
}