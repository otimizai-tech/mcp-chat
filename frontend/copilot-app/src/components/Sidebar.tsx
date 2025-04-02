import { useState } from 'react';
import { Menu, X, Home, Settings, Users, HelpCircle, FileText } from 'lucide-react';
import { useRouter } from 'next/router';

interface SidebarProps {
  isOpen: boolean;
  onToggle: () => void;
}

export function Sidebar({ isOpen, onToggle }: SidebarProps) {
  const router = useRouter();

  const navigateTo = (path: string) => {
    router.push(path);
  };

  return (
    <>
      {/* Toggle Button */}
      <button
        onClick={onToggle}
        className="p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700 transition-all"
        aria-label="Toggle Sidebar"
      >
        <Menu className="text-black dark:text-white" size={24} />
      </button>

      {/* Sidebar */}
      <aside
        className={`fixed top-16 left-0 h-[calc(100%-4rem)] bg-white dark:bg-gray-800 shadow-lg transition-all duration-300 z-30 ${
          isOpen ? 'w-64' : 'w-0'
        } overflow-hidden`}
      >
        {/* Close button at the top */}
        {isOpen && (
          <div className="sticky top-0 p-4 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
            <button
              onClick={onToggle}
              className="p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700 transition-all"
              aria-label="Close Sidebar"
            >
              <X className="text-black dark:text-white" size={24} />
            </button>
          </div>
        )}

        {/* Navigation buttons */}
        <nav className="flex flex-col p-4 space-y-4">
          <button 
            onClick={() => navigateTo('/')}
            className="flex items-center space-x-2 p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md w-full transition-colors text-black dark:text-white"
          >
            <Home size={20} />
            <span>Home</span>
          </button>
          
          <button 
            onClick={() => navigateTo('/sources')}
            className="flex items-center space-x-2 p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md w-full transition-colors text-black dark:text-white"
          >
            <FileText size={20} />
            <span>Data Sources</span>
          </button>

          <button 
            onClick={() => navigateTo('/team')}
            className="flex items-center space-x-2 p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md w-full transition-colors text-black dark:text-white"
          >
            <Users size={20} />
            <span>Team</span>
          </button>

          <button 
            onClick={() => navigateTo('/settings')}
            className="flex items-center space-x-2 p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md w-full transition-colors text-black dark:text-white"
          >
            <Settings size={20} />
            <span>Settings</span>
          </button>

          <button 
            onClick={() => navigateTo('/help')}
            className="flex items-center space-x-2 p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md w-full transition-colors text-black dark:text-white"
          >
            <HelpCircle size={20} />
            <span>Help</span>
          </button>
        </nav>
      </aside>
    </>
  );
}
