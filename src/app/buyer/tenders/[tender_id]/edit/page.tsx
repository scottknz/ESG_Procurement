"use client";

import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { RichTextEditor } from '@/components/ui/RichTextEditor';
import { AssetLibrary, AssetType } from '@/components/tender/AssetLibrary';
import { ChevronLeft, Save, Eye, Send, GripVertical, Trash2 } from 'lucide-react';
import Link from 'next/link';
import { useParams } from 'next/navigation';

interface Section {
  id: string;
  type: AssetType;
  title: string;
  content: any;
}

const mockInitialSections: Section[] = [
  {
    id: 's1',
    type: 'standard_text',
    title: 'Project Overview',
    content: {
      type: 'doc',
      content: [
        {
          type: 'heading',
          attrs: { level: 1 },
          content: [{ type: 'text', text: 'Request for Proposal: Cloud Infrastructure Migration' }]
        },
        {
          type: 'paragraph',
          content: [{ type: 'text', text: 'ProcureESG is seeking proposals from qualified vendors to migrate our primary data centers to a carbon-neutral cloud infrastructure provider by Q3 2027.' }]
        }
      ]
    }
  },
  {
    id: 's2',
    type: 'legal_clause',
    title: 'ESG Requirements',
    content: {
      type: 'doc',
      content: [
        {
          type: 'heading',
          attrs: { level: 2 },
          content: [{ type: 'text', text: 'Scope 3 Emissions' }]
        },
        {
          type: 'blockquote',
          content: [
            {
              type: 'paragraph',
              content: [{ type: 'text', text: 'All responding vendors must provide their most recent Scope 3 emissions report and a commitment to maintaining 100% renewable energy usage for the duration of the contract.' }]
            }
          ]
        },
      ]
    }
  }
];

export default function RFPEditorPage() {
  const params = useParams();
  const tenderId = params.tender_id as string;
  
  const [sections, setSections] = useState<Section[]>(mockInitialSections);

  const handleAddSection = (index: number, type: AssetType) => {
    const newSection: Section = {
      id: Math.random().toString(36).substr(2, 9),
      type,
      title: type === 'legal_clause' ? 'New Legal Clause' : 'New Section',
      content: { type: 'doc', content: [{ type: 'paragraph', content: [] }] }
    };
    
    const updated = [...sections];
    updated.splice(index + 1, 0, newSection);
    setSections(updated);
  };

  const handleRemoveSection = (id: string) => {
    setSections(sections.filter(s => s.id !== id));
  };

  const handleUpdateSectionContent = (id: string, content: any) => {
    setSections(sections.map(s => s.id === id ? { ...s, content } : s));
  };

  return (
    <div className="flex h-full flex-col bg-surface">
      <div className="sticky top-0 z-10 flex h-14 shrink-0 items-center justify-between border-b border-border bg-background px-6 shadow-sm">
        <div className="flex items-center gap-4">
          <Link href={`/buyer/tenders/${tenderId}`}>
            <Button variant="outline" size="sm" className="h-8 border-border px-2">
              <ChevronLeft className="h-4 w-4 mr-1" /> Back
            </Button>
          </Link>
          <div className="h-4 w-px bg-border" />
          <h1 className="text-sm font-semibold text-text-primary">Editing: <span className="font-normal text-text-secondary">RFP Document</span></h1>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" className="h-8 border-border text-text-primary gap-2">
            <Eye className="h-4 w-4" /> Preview PDF
          </Button>
          <Button variant="outline" className="h-8 border-border text-text-primary gap-2">
            <Save className="h-4 w-4" /> Save Draft
          </Button>
          <Button className="h-8 bg-brand-green hover:bg-brand-green-mid text-white gap-2">
            <Send className="h-4 w-4" /> Publish Tender
          </Button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-8">
        <div className="mx-auto max-w-[850px]">
          
          <AssetLibrary onAddAsset={(type) => handleAddSection(-1, type)} />

          {sections.map((section, idx) => (
            <div key={section.id} className="relative group">
              
              <div className="flex gap-4">
                <div className="flex flex-col items-center pt-2 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button className="p-1 text-text-muted hover:text-text-primary cursor-grab" aria-label="Drag to reorder">
                    <GripVertical className="h-4 w-4" />
                  </button>
                  <button 
                    onClick={() => handleRemoveSection(section.id)}
                    className="p-1 mt-2 text-text-muted hover:text-destructive transition-colors" 
                    aria-label="Delete section"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>

                <div className="flex-1 space-y-2">
                  <div className="flex items-center justify-between pl-1">
                    <input 
                      value={section.title}
                      onChange={(e) => setSections(sections.map(s => s.id === section.id ? { ...s, title: e.target.value } : s))}
                      className="text-xs font-bold uppercase tracking-wider text-text-secondary bg-transparent focus:outline-none focus:text-brand-green w-full"
                    />
                    <span className="text-[10px] text-text-muted uppercase tracking-wider border border-border px-1.5 py-0.5 rounded bg-background shrink-0">
                      {section.type.replace('_', ' ')}
                    </span>
                  </div>
                  
                  <RichTextEditor 
                    initialContent={section.content}
                    onChange={(newContent) => handleUpdateSectionContent(section.id, newContent)}
                    className={section.type === 'legal_clause' ? 'ring-1 ring-warning/20 border-warning/30' : ''}
                  />
                </div>
              </div>

              <AssetLibrary onAddAsset={(type) => handleAddSection(idx, type)} />
            </div>
          ))}

        </div>
      </div>
    </div>
  );
}
