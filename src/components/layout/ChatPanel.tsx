"use client";

import React from 'react';
import { X, Paperclip, Mic, ArrowUp, Loader2 } from 'lucide-react';
import { useShell } from './ShellContext';
import { cn } from '@/lib/utils';

export function ChatPanel() {
  const { isChatPanelOpen, toggleChatPanel } = useShell();

  return (
    <div
      className={cn(
        'flex flex-col border-r border-border bg-surface transition-all duration-300 ease-in-out',
        isChatPanelOpen ? 'w-[30%] min-w-[340px]' : 'w-0 overflow-hidden border-r-0'
      )}
    >
      <div className="flex h-14 shrink-0 items-center justify-between border-b border-border bg-background px-4 shadow-sm z-10">
        <span className="font-semibold text-text-primary">AI Copilot</span>
        <button
          onClick={toggleChatPanel}
          className="rounded-md text-text-muted hover:bg-surface-hover hover:text-text-primary p-1.5 transition-colors"
          aria-label="Close chat panel"
        >
          <X className="h-4 w-4" />
        </button>
      </div>
      
      {/* Chat Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6 bg-background">
        
        {/* Welcome Message (AI) */}
        <div className="flex gap-3">
          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-brand-green-light text-brand-green border border-brand-green/20">
            <Loader2 className="h-4 w-4 animate-spin-slow" />
          </div>
          <div className="flex-1 space-y-2">
            <div className="rounded-lg rounded-tl-none bg-surface p-3 text-[13px] leading-5 text-text-primary border border-border">
              Hello! I'm your procurement assistant. I can help you summarize responses, adapt regulatory templates, or draft emails. What would you like to do?
            </div>
            <div className="flex flex-wrap gap-2 pt-1">
              <button className="flex items-center gap-1.5 rounded-full border border-border bg-background px-3 py-1 text-xs font-medium text-text-secondary hover:border-brand-green hover:text-brand-green transition-colors">
                Draft a new RFP
              </button>
              <button className="flex items-center gap-1.5 rounded-full border border-border bg-background px-3 py-1 text-xs font-medium text-text-secondary hover:border-brand-green hover:text-brand-green transition-colors">
                Summarize latest bids
              </button>
            </div>
          </div>
        </div>

        {/* User Message */}
        <div className="flex flex-row-reverse gap-3">
          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-surface border border-border text-xs font-semibold text-text-primary">
            U
          </div>
          <div className="flex-1 space-y-2 flex flex-col items-end">
            <div className="rounded-lg rounded-tr-none bg-brand-green text-white p-3 text-[13px] leading-5 border border-brand-green-mid">
              Can you help me define evaluation criteria for an ISO 27001 requirement?
            </div>
          </div>
        </div>
      </div>

      {/* Input Area */}
      <div className="shrink-0 border-t border-border bg-background p-4">
        <div className="relative flex w-full items-end gap-2 rounded-xl border border-border bg-surface p-2 shadow-sm focus-within:border-brand-green focus-within:ring-1 focus-within:ring-brand-green transition-all">
          <button
            type="button"
            className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md text-text-muted hover:bg-surface-hover hover:text-text-primary transition-colors"
            aria-label="Attach file"
          >
            <Paperclip className="h-4 w-4" />
          </button>
          
          <textarea
            className="flex-1 resize-none bg-transparent py-1.5 text-sm text-text-primary placeholder:text-text-muted focus:outline-none min-h-[32px] max-h-[120px]"
            placeholder="Ask Copilot anything..."
            rows={1}
          />
          
          <div className="flex shrink-0 items-center gap-1">
            <button
              type="button"
              className="flex h-8 w-8 items-center justify-center rounded-md text-text-muted hover:bg-surface-hover hover:text-text-primary transition-colors"
              aria-label="Voice input"
            >
              <Mic className="h-4 w-4" />
            </button>
            <button
              type="button"
              className="flex h-8 w-8 items-center justify-center rounded-md bg-brand-green text-white shadow-sm hover:bg-brand-green-mid transition-colors disabled:opacity-50"
              aria-label="Send message"
            >
              <ArrowUp className="h-4 w-4" />
            </button>
          </div>
        </div>
        <div className="mt-2 text-center">
          <span className="text-[11px] text-text-muted">
            AI can make mistakes. Check important info.
          </span>
        </div>
      </div>
    </div>
  );
}
