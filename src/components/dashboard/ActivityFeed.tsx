import React from 'react';
import { LucideIcon } from 'lucide-react';
import { cn } from '@/lib/utils';

export interface ActivityItem {
  id: string;
  icon: LucideIcon;
  action: string;
  target?: string;
  timestamp: string;
  isUnread?: boolean;
}

interface ActivityFeedProps {
  title: string;
  items: ActivityItem[];
  onViewAll?: () => void;
  className?: string;
}

export function ActivityFeed({ title, items, onViewAll, className }: ActivityFeedProps) {
  return (
    <div className={cn('flex flex-col rounded-lg border border-border bg-background shadow-card', className)}>
      <div className="flex items-center justify-between border-b border-border px-5 py-4">
        <h2 className="text-sm font-semibold text-text-primary">{title}</h2>
        {onViewAll && (
          <button
            onClick={onViewAll}
            className="text-xs font-medium text-brand-green hover:text-brand-green-mid"
          >
            View all
          </button>
        )}
      </div>
      
      <div className="flex-1 divide-y divide-border overflow-y-auto">
        {items.length === 0 ? (
          <div className="p-6 text-center text-sm text-text-muted">No recent activity.</div>
        ) : (
          <ul className="divide-y divide-border">
            {items.map((item) => (
              <li
                key={item.id}
                className={cn(
                  'flex items-start gap-4 px-5 py-4 transition-colors hover:bg-surface-hover',
                  item.isUnread && 'bg-brand-green-light/30'
                )}
              >
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-surface border border-border">
                  <item.icon className="h-4 w-4 text-text-secondary" aria-hidden="true" />
                </div>
                <div className="flex-1 space-y-1">
                  <p className="text-sm text-text-primary leading-tight">
                    {item.action}{' '}
                    {item.target && <span className="font-medium">{item.target}</span>}
                  </p>
                  <p className="text-xs text-text-muted">{item.timestamp}</p>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
