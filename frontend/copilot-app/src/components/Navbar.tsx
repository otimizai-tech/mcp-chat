import React, { useState } from "react";
import { ThemeSwitcher } from "./ThemeSwitcher";
import { Sidebar } from "./Sidebar";

export function Navbar() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <>
      <div className="absolute top-4 left-6 z-50">
        <Sidebar isOpen={isSidebarOpen} onToggle={toggleSidebar} />
      </div>
      <div className="absolute top-4 right-6 z-50">
        <ThemeSwitcher />
      </div>
    </>
  );
}
