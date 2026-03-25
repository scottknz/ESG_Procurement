import React from 'react';
import { cn } from '@/lib/utils';
import { TenderState, SubmissionState } from '@/config/site';

interface StatusBadgeProps {
  status: TenderState | SubmissionState | 'ai_only' | 'human_confirmed';
  className?: string;
}

export function StatusBadge({ status, className }: StatusBadgeProps) {
  let styleClasses = '';
  let label = status.replace(/_/g, ' ');

  switch (status) {
    case 'draft':
    case 'closed':
    case 'archived':
      styleClasses = 'bg-surface-hover border-text-muted text-text-secondary';
      break;
    case 'open_for_proposals':
    case 'human_confirmed':
      styleClasses = 'bg-brand-green-light border-brand-green text-brand-green';
      label = status === 'open_for_proposals' ? 'Open' : label;
      break;
    case 'under_review':
      styleClasses = 'bg-warning-light border-warning text-warning';
      break;
    case 'awarded':
      styleClasses = 'bg-info-light border-info text-info';
      break;
    case 'withdrawn':
    case 'disqualified':
    case 'not_awarded':
      styleClasses = 'bg-destructive-light border-destructive text-destructive';
      break;
    case 'ai_only':
      styleClasses = 'bg-surface border-text-muted text-text-muted italic';
      label = 'AI Only';
      break;
    default:
      styleClasses = 'bg-surface border-border text-text-secondary';
  }

  return (
    <span
      className={cn(
        'inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-medium border capitalize tracking-wide',
        styleClasses,
        className
      )}
    >
      {label}
    </span>
  );
}
