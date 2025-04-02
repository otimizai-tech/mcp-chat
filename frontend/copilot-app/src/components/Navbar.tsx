import React, { useState } from 'react';
import { ThemeSwitcher } from './ThemeSwitcher';
import { Sidebar } from './Sidebar';

export function Navbar() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <>
      <nav className="fixed top-0 left-0 right-0 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 z-50">
        <div className="px-6 py-4 flex justify-between items-center">
          <div className="flex items-center gap-4">
            <Sidebar isOpen={isSidebarOpen} onToggle={toggleSidebar} />
            <h1 className="text-xl font-semibold text-gray-800 dark:text-white">Vector Bot</h1>
          </div>
          <ThemeSwitcher />
        </div>
      </nav>
    </>
  );
}
