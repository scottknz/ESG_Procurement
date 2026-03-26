"use client";

import React from 'react';
import { 
  Sheet, 
  SheetContent, 
  SheetDescription, 
  SheetHeader, 
  SheetTitle, 
  SheetTrigger 
} from "@/components/ui/sheet";
import { Plus, Type, Scale, Image, FileSignature } from 'lucide-react';
import { cn } from '@/lib/utils';

export type AssetType = 'standard_text' | 'legal_clause' | 'image_split' | 'pricing_grid';

interface AssetLibraryProps {
  onAddAsset: (type: AssetType) => void;
  className?: string;
}

const ASSETS: { id: AssetType; title: string; description: string; icon: any; }[] = [
  {
    id: 'standard_text',
    title: 'Standard Text Block',
    description: 'A blank rich-text editor for general content and scope of work.',
    icon: Type,
  },
  {
    id: 'legal_clause',
    title: 'Legal & Compliance Clause',
    description: 'Pre-formatted block for boilerplate legal or ESG requirements.',
    icon: FileSignature,
  },
  {
    id: 'image_split',
    title: 'Two-Column (Image & Text)',
    description: 'A layout block side-by-side placeholder for media and text.',
    icon: Image,
  },
  {
    id: 'pricing_grid',
    title: 'Pricing Grid',
    description: 'A structured table for capturing supplier commercial bids.',
    icon: Scale,
  },
];

export function AssetLibrary({ onAddAsset, className }: AssetLibraryProps) {
  const [open, setOpen] = React.useState(false);

  const handleSelect = (type: AssetType) => {
    onAddAsset(type);
    setOpen(false); // Close drawer after selection
  };

  return (
    <Sheet open={open} onOpenChange={setOpen}>
      <div className={cn("flex justify-center w-full relative py-4 group cursor-pointer", className)}>
        <div className="absolute inset-x-0 top-1/2 h-px bg-border group-hover:bg-brand-green/30 transition-colors pointer-events-none" />
        <SheetTrigger asChild>
          <button className="relative z-10 flex items-center rounded-full bg-surface hover:bg-brand-green hover:text-white border border-border hover:border-brand-green transition-colors px-4 py-1 h-8 gap-1 shadow-sm text-xs font-medium text-text-secondary">
            <Plus className="h-3.5 w-3.5" /> Add Section
          </button>
        </SheetTrigger>
      </div>
      
      <SheetContent className="bg-surface border-l-border sm:max-w-md">
        <SheetHeader className="mb-6">
          <SheetTitle className="text-text-primary">Asset Library</SheetTitle>
          <SheetDescription className="text-text-secondary">
            Select a template section to insert into your RFP document.
          </SheetDescription>
        </SheetHeader>
        
        <div className="space-y-4">
          {ASSETS.map((asset) => (
            <button
              key={asset.id}
              onClick={() => handleSelect(asset.id)}
              className="flex w-full items-start gap-4 rounded-lg border border-border bg-background p-4 text-left shadow-sm transition-all hover:border-brand-green hover:ring-1 hover:ring-brand-green focus:outline-none focus:ring-1 focus:ring-brand-green"
            >
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md bg-surface border border-border">
                <asset.icon className="h-5 w-5 text-text-secondary" />
              </div>
              <div>
                <h4 className="text-sm font-semibold text-text-primary">{asset.title}</h4>
                <p className="mt-1 text-xs text-text-secondary leading-relaxed">
                  {asset.description}
                </p>
              </div>
            </button>
          ))}
        </div>
      </SheetContent>
    </Sheet>
  );
}
