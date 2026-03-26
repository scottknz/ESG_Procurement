import {
  LayoutDashboard, FileText, ClipboardList, Users, Library,
  MessageSquare, Bell, Shield, Settings, Mail, Upload,
  FolderOpen, Star,
  type LucideIcon,
} from 'lucide-react';

export interface NavItem {
  label: string;
  href: string;
  icon: string;
  section: 'main' | 'secondary';
  badge?: boolean;
  isChatTrigger?: boolean;
}

export const buyerNav: NavItem[] = [
  {
    label: 'Dashboard',
    href: '/buyer/dashboard',
    icon: 'LayoutDashboard',
    section: 'main',
  },
  {
    label: 'Tenders',
    href: '/buyer/tenders',
    icon: 'FileText',
    section: 'main',
  },
  {
    label: 'Evaluations',
    href: '/buyer/evaluations',
    icon: 'ClipboardList',
    section: 'main',
    badge: true,
  },
  {
    label: 'Suppliers',
    href: '/buyer/suppliers',
    icon: 'Users',
    section: 'main',
  },
  {
    label: 'AI Copilot',
    href: '#',
    icon: 'MessageSquare',
    section: 'secondary',
    isChatTrigger: true,
  },
  {
    label: 'Settings',
    href: '/buyer/settings',
    icon: 'Settings',
    section: 'secondary',
  },
];

export const supplierNav: NavItem[] = [
  {
    label: 'Dashboard',
    href: '/supplier/dashboard',
    icon: 'LayoutDashboard',
    section: 'main',
  },
  {
    label: 'My Bids',
    href: '/supplier/bids',
    icon: 'FileText',
    section: 'main',
    badge: true,
  },
  {
    label: 'Profile & Compliance',
    href: '/supplier/profile',
    icon: 'Shield',
    section: 'main',
  },
  {
    label: 'Settings',
    href: '/supplier/settings',
    icon: 'Settings',
    section: 'secondary',
  },
];
