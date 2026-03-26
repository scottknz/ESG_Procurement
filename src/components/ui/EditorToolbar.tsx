"use client";

import React from "react";
import { useEditor } from "novel";
import { Toggle } from "@/components/ui/toggle";
import { 
  Bold, Italic, Strikethrough, Heading1, Heading2, 
  Heading3, List, ListOrdered, Quote, Code 
} from "lucide-react";
import { cn } from "@/lib/utils";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";

export function EditorToolbar({ className }: { className?: string }) {
  const { editor } = useEditor();
  if (!editor) return null;

  return (
    <div className={cn("flex flex-wrap items-center gap-1 border-b border-border bg-surface p-1", className)}>
      <div className="flex items-center gap-0.5 border-r border-border pr-2 mr-1">
        <ToolbarItem label="Heading 1" icon={Heading1} isActive={editor.isActive('heading', { level: 1 })} onClick={() => editor.chain().focus().toggleHeading({ level: 1 }).run()} />
        <ToolbarItem label="Heading 2" icon={Heading2} isActive={editor.isActive('heading', { level: 2 })} onClick={() => editor.chain().focus().toggleHeading({ level: 2 }).run()} />
        <ToolbarItem label="Heading 3" icon={Heading3} isActive={editor.isActive('heading', { level: 3 })} onClick={() => editor.chain().focus().toggleHeading({ level: 3 }).run()} />
      </div>
      <div className="flex items-center gap-0.5 border-r border-border pr-2 mr-1">
        <ToolbarItem label="Bold" icon={Bold} isActive={editor.isActive('bold')} onClick={() => editor.chain().focus().toggleBold().run()} />
        <ToolbarItem label="Italic" icon={Italic} isActive={editor.isActive('italic')} onClick={() => editor.chain().focus().toggleItalic().run()} />
        <ToolbarItem label="Strikethrough" icon={Strikethrough} isActive={editor.isActive('strike')} onClick={() => editor.chain().focus().toggleStrike().run()} />
        <ToolbarItem label="Inline Code" icon={Code} isActive={editor.isActive('code')} onClick={() => editor.chain().focus().toggleCode().run()} />
      </div>
      <div className="flex items-center gap-0.5">
        <ToolbarItem label="Bullet List" icon={List} isActive={editor.isActive('bulletList')} onClick={() => editor.chain().focus().toggleBulletList().run()} />
        <ToolbarItem label="Numbered List" icon={ListOrdered} isActive={editor.isActive('orderedList')} onClick={() => editor.chain().focus().toggleOrderedList().run()} />
        <ToolbarItem label="Quote" icon={Quote} isActive={editor.isActive('blockquote')} onClick={() => editor.chain().focus().toggleBlockquote().run()} />
      </div>
    </div>
  );
}

function ToolbarItem({ label, icon: Icon, isActive, onClick }: any) {
  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <Toggle 
          size="sm"
          pressed={isActive}
          onPressedChange={onClick}
          aria-label={label}
          className="h-8 w-8 data-[state=on]:bg-brand-green-light data-[state=on]:text-brand-green hover:bg-surface-hover hover:text-text-primary text-text-secondary"
        >
          <Icon className="h-4 w-4" />
        </Toggle>
      </TooltipTrigger>
      <TooltipContent side="top" sideOffset={4} className="bg-text-primary text-background text-[10px] font-medium px-2 py-1">
        {label}
      </TooltipContent>
    </Tooltip>
  );
}
