import React from 'react';
import { cn } from '@/lib/utils';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';

interface DataTableColumn<T> {
  key: string;
  header: React.ReactNode;
  cell: (row: T) => React.ReactNode;
  className?: string;
}

interface DataTableProps<T> {
  data: T[];
  columns: DataTableColumn<T>[];
  keyExtractor: (row: T) => string;
  className?: string;
}

export function DataTable<T>({
  data,
  columns,
  keyExtractor,
  className,
}: DataTableProps<T>) {
  return (
    <div className={cn('rounded-lg border border-border bg-background shadow-card overflow-hidden', className)}>
      <div className="overflow-x-auto">
        <Table>
          <TableHeader>
            <TableRow className="bg-surface hover:bg-surface border-b border-border">
              {columns.map((col) => (
                <TableHead
                  key={col.key}
                  className={cn(
                    'text-xs font-medium text-text-secondary uppercase tracking-wide h-10',
                    col.className
                  )}
                >
                  {col.header}
                </TableHead>
              ))}
            </TableRow>
          </TableHeader>
          <TableBody>
            {data.length === 0 ? (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="h-24 text-center text-sm text-text-muted"
                >
                  No results found.
                </TableCell>
              </TableRow>
            ) : (
              data.map((row, idx) => (
                <TableRow
                  key={keyExtractor(row)}
                  className={cn(
                    'transition-colors hover:bg-surface-hover border-b border-border last:border-0',
                    idx % 2 === 0 ? 'bg-background' : 'bg-surface/30'
                  )}
                >
                  {columns.map((col) => (
                    <TableCell key={col.key} className={cn('text-[13px] py-3 text-text-primary', col.className)}>
                      {col.cell(row)}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
      
      {data.length > 0 && (
        <div className="flex items-center justify-between border-t border-border bg-surface px-4 py-3 sm:px-6">
          <p className="text-xs text-text-secondary">
            Showing <span className="font-medium text-text-primary">{data.length}</span> results
          </p>
          <div className="flex gap-2">
            <button className="rounded px-2 py-1 text-xs font-medium text-text-secondary hover:bg-surface-hover border border-transparent hover:border-border transition-all disabled:opacity-50">
              Previous
            </button>
            <button className="rounded px-2 py-1 text-xs font-medium text-text-secondary hover:bg-surface-hover border border-transparent hover:border-border transition-all disabled:opacity-50">
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
