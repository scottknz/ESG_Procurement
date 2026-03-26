"use client";

import React, { useState, useEffect } from 'react';
import { EditorRoot, EditorContent, type JSONContent } from 'novel';
import { cn } from '@/lib/utils';
import { EditorToolbar } from './EditorToolbar';

const defaultValue: JSONContent = {
  type: 'doc',
  content: [{ type: 'paragraph', content: [] }],
};

interface RichTextEditorProps {
  initialContent?: JSONContent;
  onChange?: (content: JSONContent) => void;
  className?: string;
}

export function RichTextEditor({
  initialContent = defaultValue,
  onChange,
  className,
}: RichTextEditorProps) {
  const [isFocused, setIsFocused] = useState(false);
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  if (!isMounted) {
    return <div className={cn("min-h-[150px] w-full animate-pulse bg-surface rounded-lg border border-border", className)} />;
  }

  return (
    <EditorRoot>
      <div 
        className={cn(
          "flex flex-col w-full rounded-lg border bg-background shadow-sm overflow-hidden transition-colors",
          isFocused ? "border-brand-green ring-1 ring-brand-green" : "border-border hover:border-border-strong",
          className
        )}
      >
        <EditorToolbar />
        <EditorContent
          immediatelyRender={false}
          initialContent={initialContent}
          onUpdate={({ editor }) => onChange?.(editor?.getJSON())}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          className={cn(
            "p-6 min-h-[150px] w-full max-w-none",
            "prose prose-slate prose-p:text-text-primary prose-headings:text-text-primary prose-headings:font-bold",
            "prose-h1:text-2xl prose-h2:text-xl prose-h3:text-lg",
            "prose-a:text-brand-green hover:prose-a:text-brand-green-mid",
            "prose-blockquote:border-l-brand-green prose-blockquote:bg-brand-green-light/20 prose-blockquote:not-italic prose-blockquote:py-1",
            "focus:outline-none focus-within:outline-none outline-none"
          )}
        />
      </div>
    </EditorRoot>
  );
}
