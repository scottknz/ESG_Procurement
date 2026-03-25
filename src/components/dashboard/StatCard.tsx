import React from 'react';
import { cn } from '@/lib/utils';
import { LucideIcon } from 'lucide-react';

interface StatCardProps {
  title: string;
  value: string | number;
  icon?: LucideIcon;
  trend?: 'up' | 'down' | 'neutral';
  trendValue?: string;
  trendLabel?: string;
  valueColor?: string;
  className?: string;
}

export function StatCard({
  title,
  value,
  icon: Icon,
  trend,
  trendValue,
  trendLabel,
  valueColor = 'text-text-primary',
  className,
}: StatCardProps) {
  return (
    <div
      className={cn(
        'flex flex-col rounded-lg border border-border bg-background p-5 shadow-card',
        className
      )}
    >
      <div className="flex items-center justify-between">
        <h3 className="text-[13px] font-medium text-text-secondary tracking-wide">
          {title}
        </h3>
        {Icon && <Icon className="h-4 w-4 text-text-muted" aria-hidden="true" />}
      </div>
      
      <div className="mt-2 flex items-baseline gap-2">
        <p className={cn('text-3xl font-semibold', valueColor)}>{value}</p>
      </div>

      {(trendValue || trendLabel) && (
        <div className="mt-3 flex items-center text-xs">
          {trendValue && (
            <span
              className={cn(
                'font-medium',
                trend === 'up' && 'text-brand-green',
                trend === 'down' && 'text-destructive',
                trend === 'neutral' && 'text-text-secondary'
              )}
            >
              {trendValue}
            </span>
          )}
          {trendLabel && (
            <span className="ml-1.5 text-text-muted">{trendLabel}</span>
          )}
        </div>
      )}
    </div>
  );
}
