"use client";

import React from 'react';
import { StatCard } from '@/components/dashboard/StatCard';
import { ActivityFeed, ActivityItem } from '@/components/dashboard/ActivityFeed';
import { DataTable } from '@/components/ui/DataTable';
import { StatusBadge } from '@/components/ui/StatusBadge';
import { Button } from '@/components/ui/button';
import { SubmissionState } from '@/config/site';
import {
  Mail, FileEdit, Send, Award, Clock, CheckCircle2,
  FileText, Search, MoreHorizontal
} from 'lucide-react';

interface SupplierTenderRow {
  id: string;
  name: string;
  buyer: string;
  deadline: string;
  status: SubmissionState;
  score: string | null;
  isNearingDeadline?: boolean;
}

const mockTenders: SupplierTenderRow[] = [
  { id: '1', name: 'Cloud Infrastructure Upgrade 2026', buyer: 'Acme Corp', deadline: '2026-03-20', status: 'under_review', score: null },
  { id: '2', name: 'Scope 3 Emissions Audit', buyer: 'Global Logistics Inc', deadline: '2026-03-25', status: 'draft', score: null, isNearingDeadline: true },
  { id: '3', name: 'Office Supplies (Sustainable)', buyer: 'City Council', deadline: '2026-04-15', status: 'submitted', score: null },
  { id: '4', name: 'Fleet Electrification Program', buyer: 'Transport Co', deadline: '2026-02-10', status: 'awarded', score: '85/100' },
];

const mockActivities: ActivityItem[] = [
  { id: '1', icon: Mail, action: 'Invitation received for', target: 'Scope 3 Emissions Audit', timestamp: '2 hours ago', isUnread: true },
  { id: '2', icon: Send, action: 'Submission confirmed for', target: 'Office Supplies (Sustainable)', timestamp: '1 day ago' },
  { id: '3', icon: FileText, action: 'Tender amended:', target: 'Cloud Infrastructure Upgrade 2026', timestamp: '2 days ago' },
  { id: '4', icon: CheckCircle2, action: 'Contract awarded for', target: 'Fleet Electrification Program', timestamp: '5 days ago' },
];

const tenderColumns = [
  {
    key: 'name',
    header: 'Tender Name',
    cell: (row: SupplierTenderRow) => <span className="font-medium">{row.name}</span>,
    className: 'w-[35%]',
  },
  {
    key: 'buyer',
    header: 'Buyer',
    cell: (row: SupplierTenderRow) => row.buyer,
  },
  {
    key: 'deadline',
    header: 'Deadline',
    cell: (row: SupplierTenderRow) => (
      <span className={row.isNearingDeadline ? 'text-warning font-medium flex items-center gap-1.5' : ''}>
        {row.isNearingDeadline && <Clock className="h-3 w-3" />}
        {row.deadline}
      </span>
    ),
  },
  {
    key: 'status',
    header: 'Status',
    cell: (row: SupplierTenderRow) => <StatusBadge status={row.status} />,
  },
  {
    key: 'score',
    header: 'Score',
    cell: (row: SupplierTenderRow) => (
      row.score ? <span className="text-brand-green font-medium">{row.score}</span> : <span className="text-text-muted">-</span>
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

export default function SupplierDashboardPage() {
  return (
    <div className="flex flex-col min-h-full">
      <div className="sticky top-0 z-10 flex h-14 shrink-0 items-center justify-between border-b border-border bg-background px-6">
        <h1 className="text-lg font-semibold text-text-primary">Dashboard</h1>
        <Button variant="outline" className="border-border text-text-primary h-9 px-4 rounded-md gap-2">
          <Search className="h-4 w-4" />
          Browse Public Tenders
        </Button>
      </div>

      <div className="flex-1 p-6 space-y-6">
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <StatCard title="Open Invitations" value={3} icon={Mail} valueColor="text-info" />
          <StatCard title="In Progress" value={5} icon={FileEdit} valueColor="text-brand-green" />
          <StatCard title="Submitted" value={12} icon={Send} valueColor="text-text-primary" />
          <StatCard title="Outcomes" value={8} icon={Award} />
        </div>

        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="lg:col-span-2 space-y-6">
            <div className="flex flex-col gap-4">
              <h2 className="text-sm font-semibold text-text-primary">My Tenders</h2>
              <DataTable
                data={mockTenders}
                columns={tenderColumns}
                keyExtractor={(row) => row.id}
              />
            </div>
            
            <div className="flex flex-col gap-4 mt-8">
              <h2 className="text-sm font-semibold text-text-primary">Invitation Inbox</h2>
              <div className="rounded-lg border border-border bg-background shadow-card divide-y divide-border">
                <div className="p-5 flex items-center justify-between">
                  <div className="flex gap-4">
                    <div className="h-10 w-10 rounded bg-brand-green-light text-brand-green flex items-center justify-center font-bold">
                      GL
                    </div>
                    <div>
                      <h3 className="font-semibold text-text-primary">Global Logistics Inc</h3>
                      <p className="text-sm text-text-secondary mt-1">Invited you to bid on: <span className="font-medium text-text-primary">European Freight Consolidation</span></p>
                    </div>
                  </div>
                  <div className="flex gap-3">
                    <Button variant="outline" className="text-text-secondary">Decline</Button>
                    <Button className="bg-brand-green hover:bg-brand-green-mid text-white">View Tender</Button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-6">
            <ActivityFeed
              title="Recent Activity"
              items={mockActivities}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
