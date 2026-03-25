"use client";

import React, { createContext, useContext, useState, ReactNode } from 'react';

interface ShellContextType {
  isSidebarCollapsed: boolean;
  toggleSidebar: () => void;
  isChatPanelOpen: boolean;
  toggleChatPanel: () => void;
}

const ShellContext = createContext<ShellContextType | undefined>(undefined);

export function ShellProvider({ children }: { children: ReactNode }) {
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [isChatPanelOpen, setIsChatPanelOpen] = useState(false);

  const toggleSidebar = () => setIsSidebarCollapsed((prev) => !prev);
  const toggleChatPanel = () => setIsChatPanelOpen((prev) => !prev);

  return (
    <ShellContext.Provider
      value={{
        isSidebarCollapsed,
        toggleSidebar,
        isChatPanelOpen,
        toggleChatPanel,
      }}
    >
      {children}
    </ShellContext.Provider>
  );
}

export function useShell() {
  const context = useContext(ShellContext);
  if (context === undefined) {
    throw new Error('useShell must be used within a ShellProvider');
  }
  return context;
}
