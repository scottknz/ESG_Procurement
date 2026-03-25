"use client";

import React from 'react';
import { ShellProvider } from './ShellContext';
import { Sidebar } from './Sidebar';
import { ChatPanel } from './ChatPanel';

interface DashboardShellProps {
  children: React.ReactNode;
  variant: 'buyer' | 'supplier';
}

export function DashboardShell({ children, variant }: DashboardShellProps) {
  return (
    <ShellProvider>
      <div className="flex h-screen w-full overflow-hidden bg-background text-text-primary">
        <Sidebar variant={variant} />
        <ChatPanel />
        <main className="flex-1 overflow-y-auto">
          {children}
        </main>
      </div>
    </ShellProvider>
  );
}
