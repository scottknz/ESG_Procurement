"use client";

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard, FileText, ClipboardList, Users, Library,
  MessageSquare, Bell, Shield, Settings, Mail, Upload,
  FolderOpen, Star, PanelLeftClose, PanelLeftOpen, MoreHorizontal,
} from 'lucide-react';
import { buyerNav, supplierNav, NavItem } from '@/config/nav';
import { useShell } from './ShellContext';
import { cn } from '@/lib/utils';

const iconMap: Record<string, React.ElementType> = {
  LayoutDashboard, FileText, ClipboardList, Users, Library,
  MessageSquare, Bell, Shield, Settings, Mail, Upload,
  FolderOpen, Star,
};

interface SidebarProps {
  variant: 'buyer' | 'supplier';
}

export function Sidebar({ variant }: SidebarProps) {
  const pathname = usePathname();
  const { isSidebarCollapsed, toggleSidebar, toggleChatPanel } = useShell();

  const navItems = variant === 'buyer' ? buyerNav : supplierNav;
  const mainItems = navItems.filter((item) => item.section === 'main');
  const secondaryItems = navItems.filter((item) => item.section === 'secondary');

  const renderNavItems = (items: NavItem[]) => {
    return items.map((item) => {
      const Icon = iconMap[item.icon] || FileText;
      const isActive = pathname === item.href;
      
      const content = (
        <>
          <Icon className="h-4 w-4 shrink-0" aria-hidden="true" />
          {!isSidebarCollapsed && (
            <span className="ml-3 truncate text-[13px] font-medium leading-5">
              {item.label}
            </span>
          )}
          {item.badge && !isSidebarCollapsed && (
            <span className="ml-auto flex h-2 w-2 rounded-full bg-brand-green" aria-hidden="true" />
          )}
        </>
      );

      const className = cn(
        'group flex items-center px-3 py-2 text-sm font-medium transition-colors',
        isSidebarCollapsed ? 'justify-center' : 'justify-start rounded-md',
        isActive
          ? 'bg-brand-green-light text-brand-green border-l-[3px] border-brand-green -ml-[3px] rounded-l-none'
          : 'text-text-secondary hover:bg-surface-hover hover:text-text-primary'
      );

      if (item.isChatTrigger) {
        return (
          <button
            key={item.label}
            onClick={toggleChatPanel}
            className={cn('w-full', className)}
            aria-label={item.label}
          >
            {content}
          </button>
        );
      }

      return (
        <Link
          key={item.label}
          href={item.href}
          className={className}
          aria-label={isSidebarCollapsed ? item.label : undefined}
        >
          {content}
        </Link>
      );
    });
  };

  return (
    <div
      className={cn(
        'flex flex-col border-r border-border bg-surface transition-all duration-300 ease-in-out',
        isSidebarCollapsed ? 'w-[56px]' : 'w-[220px]'
      )}
    >
      <div className="flex h-14 items-center justify-between border-b border-border px-4">
        {!isSidebarCollapsed && (
          <div className="flex items-center gap-2 overflow-hidden">
            <div className="h-6 w-6 rounded bg-text-primary shrink-0" aria-hidden="true" />
            <span className="truncate font-semibold tracking-tight text-text-primary">
              ProcureESG
            </span>
          </div>
        )}
        <button
          onClick={toggleSidebar}
          className="text-text-secondary hover:text-text-primary"
          aria-label={isSidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {isSidebarCollapsed ? (
            <PanelLeftOpen className="h-4 w-4" />
          ) : (
            <PanelLeftClose className="h-4 w-4" />
          )}
        </button>
      </div>

      <nav className="flex-1 space-y-1 overflow-y-auto px-2 py-4">
        {renderNavItems(mainItems)}
      </nav>

      <div className="px-2 py-4 border-t border-border">
        <nav className="space-y-1">
          {renderNavItems(secondaryItems)}
        </nav>
      </div>

      <div className="border-t border-border p-2">
        <button
          className={cn(
            'flex w-full items-center gap-3 rounded-md p-2 text-sm transition-colors hover:bg-surface-hover',
            isSidebarCollapsed ? 'justify-center' : 'justify-start'
          )}
          aria-label="User menu"
        >
          <div className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-border-strong text-xs font-semibold text-text-primary">
            U
          </div>
          {!isSidebarCollapsed && (
            <>
              <span className="flex-1 truncate text-left font-medium text-text-primary">
                Current User
              </span>
              <MoreHorizontal className="h-4 w-4 text-text-muted" />
            </>
          )}
        </button>
      </div>
    </div>
  );
}
