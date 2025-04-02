'use client';

import { Navbar } from "../components/Navbar";
import { SourceManager } from "../components/SourceManager";
import { SourcesProvider } from "../hooks/useSourceManager";
import { ThemeProvider } from "next-themes";
import { CopilotKit } from "@copilotkit/react-core";
import { CopilotPopup } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";


export default function SourcesPage() {


  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      <CopilotKit runtimeUrl="/api/copilotkit">
        <SourcesProvider>
          <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex flex-col">
            <Navbar />
            <div className="flex flex-1" style={{ marginTop: '64px' }}>
              <main className="flex-1">
                <div className="h-[calc(100vh-64px)]">
                  <SourceManager />
                </div>
              </main>
            </div>
          </div>
        </SourcesProvider>
        <CopilotPopup
          labels={{
            title: "Your Assistant",
            initial: "Hi! 👋 How can I assist you today?",
          }}
        />
      </CopilotKit>
    </ThemeProvider>
  );
}
