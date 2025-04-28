"use client";

import "@copilotkit/react-ui/styles.css";
import { Navbar } from "../components/Navbar";
import { useState, useEffect } from "react";
import { CopilotChat } from "@copilotkit/react-ui";
import {
  CopilotKit,
  useCopilotAction,
  useCopilotChat,
  useCoAgent,
} from "@copilotkit/react-core";
import { ThemeProvider } from "next-themes";
import { SourcesProvider, useSourceManager } from "../hooks/useSourceManager";
import DataSource from "../components/Sources";
import React from "react";
import { CanvasCopilot } from "../components/CanvasCopilot";
import { motion } from "framer-motion";
import { TextMessage, MessageRole } from "@copilotkit/runtime-client-gql";

function CustomChatInterface() {
  const [isOpen, setIsOpen] = useState(false);
  const [content, setContent] = useState("");
  const [isAnimating, setIsAnimating] = useState(false);
  const [hasInteracted, setHasInteracted] = useState(false);
  const [userInput, setUserInput] = useState("");
  const { visibleMessages } = useCopilotChat();

  // Use the agent directly similar to HomeView.tsx
  const { run: runChatAgent } = useCoAgent({
    name: "mcp_agent",
  });

  const action = useCopilotAction({
    name: "openCanvas",
    description:
      "Opens a text editor canvas and writes the specified content. Use this when the user wants to write or edit text.",
    parameters: [
      {
        name: "content",
        type: "string",
        description: "The content to write in the canvas",
        required: true,
      },
    ],

    handler: async ({ content }) => {
      setContent(content);
      setIsOpen(true);
      return "Editor aberto! Você pode editar o texto agora.";
    },
  });

  const handleClose = () => {
    setIsAnimating(true);
    setIsOpen(false);
    setTimeout(() => {
      setContent("");
      setIsAnimating(false);
    }, 300);
  };

  useEffect(() => {
    if (visibleMessages.length > 0 && !hasInteracted) {
      setHasInteracted(true);
    }
  }, [visibleMessages, hasInteracted]);

  const sendMessageToChat = (message: string) => {
    if (!message.trim()) return;

    runChatAgent(() => {
      return new TextMessage({
        role: MessageRole.User,
        content: message,
      });
    });

    setHasInteracted(true);
    setUserInput("");
  };

  // Função para lidar com a submissão inicial da mensagem
  const handleInitialSubmit = (query: string) => {
    sendMessageToChat(query);
  };

  // Sugestões para exibir na tela de boas-vindas
  const suggestions = [
    { label: "Como faço para usar o MCP?", icon: "🤖" },
    { label: "O que é o Otimizai?", icon: "💻" },
    { label: "Gere um texto sobre I.A pra mim", icon: "✍️" },
    { label: "Preciso de ajuda com análise de dados", icon: "📊" },
  ];

  return (
    <div className="flex-1 relative h-screen">
      <div className="flex h-full pt-16">
        {!hasInteracted ? (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="w-full flex flex-col items-center justify-center p-6"
          >
            <motion.div
              className="max-w-3xl w-full flex flex-col items-center mb-8 text-center"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.2, duration: 0.5 }}
            >
              <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Bem-vindo ao Vector Bot
              </h1>
              <p className="text-xl text-gray-600 dark:text-gray-300 mb-6">
                O assistente inteligente da Otimizai para ajudar em suas tarefas
              </p>
              <p className="text-md text-gray-500 dark:text-gray-400 mb-8">
                Como posso te ajudar hoje?
              </p>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 w-full max-w-2xl mb-8">
                {suggestions.map((suggestion) => (
                  <div
                    key={suggestion.label}
                    onClick={() => handleInitialSubmit(suggestion.label)}
                    className="p-3 bg-white dark:bg-gray-800 rounded-md border border-gray-200 dark:border-gray-700 flex cursor-pointer items-center space-x-3 hover:bg-gray-50 dark:hover:bg-gray-700 transition-all duration-300 shadow-sm"
                  >
                    <span className="text-xl">{suggestion.icon}</span>
                    <span className="flex-1">{suggestion.label}</span>
                  </div>
                ))}
              </div>
            </motion.div>

            <motion.div
              className="w-full max-w-3xl"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4, duration: 0.5 }}
            >
              <div
                className={`transition-all duration-500 ease-in-out ${
                  isOpen ? "w-[calc(100%-350px)]" : "w-full"
                }`}
              >
                <CopilotChat
                  className="border rounded-xl shadow-md dark:border-gray-700"
                  labels={{
                    title: "MCP Assistant",
                    initial:
                      "Digite sua mensagem ou escolha uma sugestão acima",
                    placeholder: "Digite sua pergunta aqui...",
                  }}
                />
              </div>
            </motion.div>
          </motion.div>
        ) : (
          <>
            <div
              className={`h-full transition-all duration-500 ease-in-out ${
                isOpen ? "w-[calc(100%-350px)]" : "w-full"
              }`}
            >
              <CopilotChat
                className="h-full border-r dark:border-gray-700"
                labels={{
                  title: "MCP Assistant",
                  initial: "Como posso ajudar?",
                  placeholder: "Digite sua pergunta aqui...",
                }}
              />
            </div>
            {(isOpen || isAnimating) && (
              <div
                className={`flex items-start pt-4 pr-4 pl-2 transition-all duration-300 ease-in-out ${
                  isOpen
                    ? "w-[450px] opacity-100 translate-x-0"
                    : "w-0 opacity-0 translate-x-4"
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
          </>
        )}
      </div>
    </div>
  );
}

export default function CopilotPage() {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      <CopilotKit runtimeUrl="/api/copilotkit" agent="mcp_agent">
        <SourcesProvider>
          <div className="h-screen bg-gray-50 dark:bg-gray-900 flex flex-col overflow-hidden">
            <Navbar />
            <div className="flex-1 relative">
              <CustomChatInterface />
            </div>
          </div>
        </SourcesProvider>
      </CopilotKit>
    </ThemeProvider>
  );
}
