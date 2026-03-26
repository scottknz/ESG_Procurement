"use client";

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Loader2, ArrowRight, Mic, Sparkles } from 'lucide-react';
import { cn } from '@/lib/utils';

export default function TenderWizardPage() {
  const router = useRouter();
  const [isGenerating, setIsGenerating] = useState(false);
  const [messages, setMessages] = useState<{ role: 'ai' | 'user'; text: string }[]>([
    { role: 'ai', text: "Welcome! Let's draft your RFP. To start, what is the primary goal of this procurement project?" },
  ]);
  const [inputValue, setInputValue] = useState('');

  const handleSend = () => {
    if (!inputValue.trim()) return;
    
    setMessages(prev => [...prev, { role: 'user', text: inputValue }]);
    setInputValue('');

    setIsGenerating(true);
    setTimeout(() => {
      setMessages(prev => [...prev, { 
        role: 'ai', 
        text: "Got it. Are there any specific ESG frameworks or ISO standards this supplier must comply with? (e.g., ISO 27001, Scope 3 reporting)" 
      }]);
      setIsGenerating(false);
    }, 1500);
  };

  const handleComplete = () => {
    setIsGenerating(true);
    setTimeout(() => {
      router.push('/buyer/tenders/123/edit');
    }, 2000);
  };

  return (
    <div className="flex h-full flex-col bg-background">
      <div className="flex h-14 shrink-0 items-center justify-between border-b border-border px-6">
        <div className="flex items-center gap-2">
          <Sparkles className="h-4 w-4 text-brand-green" />
          <h1 className="text-lg font-semibold text-text-primary">AI Setup Wizard</h1>
        </div>
        <Button 
          onClick={handleComplete} 
          disabled={messages.length < 3 || isGenerating}
          className="bg-brand-green hover:bg-brand-green-mid text-white gap-2"
        >
          {isGenerating ? <Loader2 className="h-4 w-4 animate-spin" /> : 'Generate Draft'}
          {!isGenerating && <ArrowRight className="h-4 w-4" />}
        </Button>
      </div>

      <div className="flex-1 overflow-y-auto p-6">
        <div className="mx-auto max-w-3xl space-y-6">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={cn(
                "flex gap-4",
                msg.role === 'user' ? "flex-row-reverse" : "flex-row"
              )}
            >
              <div className={cn(
                "flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-xs font-semibold border",
                msg.role === 'user' 
                  ? "bg-surface border-border text-text-primary" 
                  : "bg-brand-green-light border-brand-green/20 text-brand-green"
              )}>
                {msg.role === 'user' ? 'U' : <Sparkles className="h-4 w-4" />}
              </div>
              <div className={cn(
                "max-w-[80%] rounded-lg p-4 text-[14px] leading-relaxed",
                msg.role === 'user'
                  ? "bg-brand-green text-white border border-brand-green-mid rounded-tr-none"
                  : "bg-surface border border-border text-text-primary rounded-tl-none"
              )}>
                {msg.text}
              </div>
            </div>
          ))}
          {isGenerating && messages[messages.length - 1].role === 'user' && (
            <div className="flex gap-4">
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-brand-green-light border border-brand-green/20 text-brand-green">
                <Loader2 className="h-4 w-4 animate-spin-slow" />
              </div>
              <div className="max-w-[80%] rounded-lg rounded-tl-none bg-surface border border-border p-4">
                <div className="flex space-x-1">
                  <div className="h-2 w-2 rounded-full bg-text-muted animate-bounce" />
                  <div className="h-2 w-2 rounded-full bg-text-muted animate-bounce delay-75" />
                  <div className="h-2 w-2 rounded-full bg-text-muted animate-bounce delay-150" />
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="shrink-0 border-t border-border bg-surface p-4">
        <div className="mx-auto max-w-3xl">
          <div className="relative flex w-full items-end gap-2 rounded-xl border border-border bg-background p-2 shadow-sm focus-within:border-brand-green focus-within:ring-1 focus-within:ring-brand-green transition-all">
            <textarea
              className="flex-1 resize-none bg-transparent py-2 px-3 text-[14px] text-text-primary placeholder:text-text-muted focus:outline-none min-h-[44px] max-h-[200px]"
              placeholder="Type your answer..."
              rows={1}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
            />
            <div className="flex shrink-0 items-center gap-1 pb-1">
              <button
                type="button"
                className="flex h-9 w-9 items-center justify-center rounded-md text-text-muted hover:bg-surface-hover hover:text-text-primary transition-colors"
                aria-label="Voice input"
              >
                <Mic className="h-5 w-5" />
              </button>
              <Button
                onClick={handleSend}
                disabled={!inputValue.trim() || isGenerating}
                className="h-9 w-9 p-0 bg-brand-green hover:bg-brand-green-mid text-white rounded-md transition-colors"
                aria-label="Send message"
              >
                <ArrowRight className="h-5 w-5" />
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}