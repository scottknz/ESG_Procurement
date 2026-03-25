"use client";

import React from 'react';
import { StatCard } from '@/components/dashboard/StatCard';
import { ActivityFeed, ActivityItem } from '@/components/dashboard/ActivityFeed';
import { DataTable } from '@/components/ui/DataTable';
import { StatusBadge } from '@/components/ui/StatusBadge';
import { Button } from '@/components/ui/button';
import { TenderState } from '@/config/site';
import {
  FileText, AlertCircle, Users, Award, Clock,
  CheckCircle2, Mail, MoreHorizontal
} from 'lucide-react';

interface TenderRow {
  id: string;
  name: string;
  status: TenderState;
  deadline: string;
  suppliers: number;
  score: string | null;
  isNearingDeadline?: boolean;
}

const mockTenders: TenderRow[] = [
  { id: '1', name: 'Cloud Infrastructure Upgrade 2026', status: 'under_review', deadline: '2026-03-20', suppliers: 5, score: 'Pending' },
  { id: '2', name: 'Scope 3 Emissions Audit', status: 'open_for_proposals', deadline: '2026-03-25', suppliers: 12, score: null, isNearingDeadline: true },
  { id: '3', name: 'Office Supplies (Sustainable)', status: 'draft', deadline: '2026-04-15', suppliers: 0, score: null },
  { id: '4', name: 'Fleet Electrification Program', status: 'awarded', deadline: '2026-02-10', suppliers: 8, score: '85/100' },
];

const mockActivities: ActivityItem[] = [
  { id: '1', icon: CheckCircle2, action: 'Score confirmed for', target: 'Cloud Infrastructure Upgrade 2026', timestamp: '2 hours ago', isUnread: true },
  { id: '2', icon: Mail, action: 'Submission received from GreenTech Ltd', timestamp: '5 hours ago', isUnread: true },
  { id: '3', icon: FileText, action: 'Tender published:', target: 'Scope 3 Emissions Audit', timestamp: '1 day ago' },
  { id: '4', icon: Award, action: 'Contract awarded for', target: 'Fleet Electrification Program', timestamp: '2 days ago' },
];

const tenderColumns = [
  {
    key: 'name',
    header: 'Tender Name',
    cell: (row: TenderRow) => <span className="font-medium">{row.name}</span>,
    className: 'w-[40%]',
  },
  {
    key: 'status',
    header: 'Status',
    cell: (row: TenderRow) => <StatusBadge status={row.status} />,
  },
  {
    key: 'deadline',
    header: 'Deadline',
    cell: (row: TenderRow) => (
      <span className={row.isNearingDeadline ? 'text-warning font-medium flex items-center gap-1.5' : ''}>
        {row.isNearingDeadline && <Clock className="h-3 w-3" />}
        {row.deadline}
      </span>
    ),
  },
  {
    key: 'suppliers',
    header: 'Suppliers',
    cell: (row: TenderRow) => row.suppliers.toString(),
  },
  {
    key: 'score',
    header: 'Score',
    cell: (row: TenderRow) => (
      row.score ? <span className="text-text-secondary">{row.score}</span> : <span className="text-text-muted">-</span>
    ),
  },
  {
    key: 'actions',
    header: '',
    cell: () => (
      <button className="rounded hover:bg-surface-hover p-1 text-text-muted transition-colors" aria-label="More actions">
        <MoreHorizontal className="h-4 w-4" />
      </button>
    ),
    className: 'text-right',
  },
];

export default function BuyerDashboardPage() {
  return (
    <div className="flex flex-col min-h-full">
      <div className="sticky top-0 z-10 flex h-14 shrink-0 items-center justify-between border-b border-border bg-background px-6">
        <h1 className="text-lg font-semibold text-text-primary">Dashboard</h1>
        <Button className="bg-brand-green hover:bg-brand-green-mid text-white h-9 px-4 rounded-md">
          + New Tender
        </Button>
      </div>

      <div className="flex-1 p-6 space-y-6">
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <StatCard title="Active Tenders" value={12} icon={FileText} valueColor="text-brand-green" />
          <StatCard title="Awaiting Review" value={4} icon={AlertCircle} valueColor="text-warning" trend="up" trendValue="+2" trendLabel="since yesterday" />
          <StatCard title="Suppliers Invited" value={38} icon={Users} valueColor="text-info" />
          <StatCard title="Awarded YTD" value={24} icon={Award} />
        </div>

        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="lg:col-span-2 space-y-6">
            <div className="flex flex-col gap-4">
              <h2 className="text-sm font-semibold text-text-primary">Active Tenders</h2>
              <DataTable
                data={mockTenders}
                columns={tenderColumns}
                keyExtractor={(row) => row.id}
              />
            </div>
          </div>

          <div className="space-y-6">
            <ActivityFeed
              title="Recent Activity"
              items={mockActivities}
            />
            
            <div className="rounded-lg border border-border bg-background p-5 shadow-card">
              <h2 className="text-sm font-semibold text-text-primary mb-4">Upcoming Deadlines</h2>
              <ul className="space-y-4">
                <li className="flex items-start justify-between gap-4">
                  <div>
                    <p className="text-[13px] font-medium text-text-primary leading-tight">Scope 3 Emissions Audit</p>
                    <p className="text-xs text-warning mt-0.5 flex items-center gap-1">
                      <Clock className="h-3 w-3" /> 2 days remaining
                    </p>
                  </div>
                  <StatusBadge status="open_for_proposals" />
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
