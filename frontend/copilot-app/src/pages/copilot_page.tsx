'use client';

import "@copilotkit/react-ui/styles.css";
import { Navbar } from "../components/Navbar";
import { useState } from "react";
import { CopilotChat } from "@copilotkit/react-ui";
import { CopilotKit, useCopilotAction, useCopilotChat } from "@copilotkit/react-core"; 
import { ThemeProvider } from "next-themes";
import { SourcesProvider, useSourceManager } from "../hooks/useSourceManager";
import DataSource from "../components/Sources";
import React from "react";
import { CanvasCopilot } from "../components/CanvasCopilot";

function SourcesAction() {
  const { sources } = useSourceManager();

  useCopilotAction({
    name: "showSources",
    description: "Displays the list of available data sources",
    parameters: [
      {
        name: "filter",
        type: "string",
        description: "Filter sources by name (optional)",
        required: false
      }
    ],
    render: ({ status, args }) => {
      const { filter } = args;

      if (status === 'inProgress') {
        return <div className="animate-pulse">Loading sources...</div>;
      }

      const filteredSources = filter
        ? sources.filter(source => 
            source.name.toLowerCase().includes(filter.toLowerCase())
          )
        : sources;

      return <DataSource sources={filteredSources} />;
    },
  });

  return null;
}

function CustomChatInterface() {
  const [isOpen, setIsOpen] = useState(false);
  const [content, setContent] = useState('');
  const [isAnimating, setIsAnimating] = useState(false);
  const { visibleMessages } = useCopilotChat();

  const action = useCopilotAction({
    name: "openCanvas",
    description: "Opens a text editor canvas and writes the specified content. Use this when the user wants to write or edit text.",
    parameters: [
      {
        name: "content",
        type: "string",
        description: "The content to write in the canvas",
        required: true
      }
    ],
    
    handler: async ({ content }) => {
      setContent(content);
      setIsOpen(true);
      return "Editor aberto! Você pode editar o texto agora.";
    }
  });

  const handleClose = () => {
    setIsAnimating(true);
    setIsOpen(false);
    setTimeout(() => {
      setContent('');
      setIsAnimating(false);
    }, 300);
  };

  return (
    <div className="flex-1 relative h-[calc(100vh-64px)]">
      <div className="flex h-full">
        <div className={`transition-all duration-300 ease-in-out ${isOpen ? 'w-[calc(100%-350px)]' : 'w-full'}`}>
          <CopilotChat className="h-full border-r dark:border-gray-700"
          //instructions={"You are assisting the user as best as you can. Answer in the best way possible given the data you have."}
          labels={{
            title: "MCP Assistant",
            initial: "Precisa de Ajuda?",
          }} />
        </div>
        {(isOpen || isAnimating) && (
          <div 
            className={`flex items-start pt-4 pr-4 pl-2 transition-all duration-300 ease-in-out ${
              isOpen ? 'w-[450px] opacity-100 translate-x-0' : 'w-0 opacity-0 translate-x-4'
            }`}
            aria-hidden={!isOpen}
          >
            <CanvasCopilot
              isOpen={isOpen}
              onClose={handleClose}
              content={content}
              title="Canvas Copilot"
              onContentChange={isAnimating ? undefined : setContent}
            />
          </div>
        )}
      </div>
    </div>
  );
}

export default function CopilotPage() {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      <CopilotKit runtimeUrl="/api/copilotkit">
        <SourcesProvider>
          <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex flex-col">
            <Navbar />
            <div className="flex flex-1 relative" style={{ marginTop: '64px' }}>
              <SourcesAction />
              <CustomChatInterface />
            </div>
          </div>
        </SourcesProvider>
      </CopilotKit>
    </ThemeProvider>
  );
}
