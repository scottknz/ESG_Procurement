import React from 'react';
import { DashboardShell } from '@/components/layout/DashboardShell';

export default function SupplierLayout({ children }: { children: React.ReactNode }) {
  return <DashboardShell variant="supplier">{children}</DashboardShell>;
}
