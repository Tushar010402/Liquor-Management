import React, { useState } from 'react';
import {
  Box,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Collapse,
  Divider,
  Typography,
  IconButton,
  useTheme,
  useMediaQuery,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Store as StoreIcon,
  People as PeopleIcon,
  Inventory as InventoryIcon,
  LocalShipping as SupplierIcon,
  Receipt as SalesIcon,
  AssignmentReturn as ReturnIcon,
  MonetizationOn as CashIcon,
  Assessment as ReportIcon,
  Settings as SettingsIcon,
  ExpandLess,
  ExpandMore,
  Business as BusinessIcon,
  AccountCircle as AccountIcon,
  Apartment as TenantIcon,
  Security as SecurityIcon,
  Storage as SystemIcon,
  Backup as BackupIcon,
  Analytics as AnalyticsIcon,
  Approval as ApprovalIcon,
  ShoppingCart as PurchaseIcon,
  Paid as FinancialIcon,
  Summarize as SummaryIcon,
  Logout as LogoutIcon,
  Menu as MenuIcon,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import useAuth from '../../hooks/useAuth';
import { UserRole } from '../../contexts/AuthContext';

interface MenuItem {
  title: string;
  path?: string;
  icon: React.ReactNode;
  children?: MenuItem[];
  roles?: UserRole[];
}

interface SidebarProps {
  open: boolean;
  onClose: () => void;
  variant: 'permanent' | 'temporary';
}

const Sidebar: React.FC<SidebarProps> = ({ open, onClose, variant }) => {
  const theme = useTheme();
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [openSubMenus, setOpenSubMenus] = useState<{ [key: string]: boolean }>({});

  const handleSubMenuToggle = (title: string) => {
    setOpenSubMenus((prev) => ({
      ...prev,
      [title]: !prev[title],
    }));
  };

  const handleNavigate = (path: string) => {
    navigate(path);
    if (isMobile) {
      onClose();
    }
  };

  const isActive = (path: string) => {
    return location.pathname === path || location.pathname.startsWith(`${path}/`);
  };

  // Define menu items based on user role
  const getMenuItems = (): MenuItem[] => {
    if (!user) return [];

    switch (user.role) {
      case 'saas_admin':
        return [
          {
            title: 'Dashboard',
            path: '/saas-admin/dashboard',
            icon: <DashboardIcon />,
          },
          {
            title: 'Tenant Management',
            icon: <TenantIcon />,
            children: [
              {
                title: 'All Tenants',
                path: '/saas-admin/tenants',
                icon: <BusinessIcon />,
              },
              {
                title: 'Add New Tenant',
                path: '/saas-admin/tenants/new',
                icon: <BusinessIcon />,
              },
              {
                title: 'Billing Plans',
                path: '/saas-admin/billing-plans',
                icon: <MonetizationOn />,
              },
            ],
          },
          {
            title: 'Platform Team',
            icon: <PeopleIcon />,
            children: [
              {
                title: 'Team Members',
                path: '/saas-admin/team',
                icon: <PeopleIcon />,
              },
              {
                title: 'Role Management',
                path: '/saas-admin/roles',
                icon: <SecurityIcon />,
              },
            ],
          },
          {
            title: 'System Administration',
            icon: <SystemIcon />,
            children: [
              {
                title: 'System Health',
                path: '/saas-admin/system-health',
                icon: <SystemIcon />,
              },
              {
                title: 'Error Logs',
                path: '/saas-admin/error-logs',
                icon: <SystemIcon />,
              },
              {
                title: 'System Configuration',
                path: '/saas-admin/system-config',
                icon: <SettingsIcon />,
              },
            ],
          },
          {
            title: 'Backup & Restore',
            icon: <BackupIcon />,
            children: [
              {
                title: 'Backup Schedule',
                path: '/saas-admin/backup-schedule',
                icon: <BackupIcon />,
              },
              {
                title: 'Manual Backup',
                path: '/saas-admin/manual-backup',
                icon: <BackupIcon />,
              },
              {
                title: 'Restore Data',
                path: '/saas-admin/restore-data',
                icon: <BackupIcon />,
              },
            ],
          },
          {
            title: 'Platform Analytics',
            icon: <AnalyticsIcon />,
            children: [
              {
                title: 'Tenant Growth',
                path: '/saas-admin/tenant-growth',
                icon: <AnalyticsIcon />,
              },
              {
                title: 'Revenue Analytics',
                path: '/saas-admin/revenue-analytics',
                icon: <MonetizationOn />,
              },
              {
                title: 'Usage Statistics',
                path: '/saas-admin/usage-statistics',
                icon: <AnalyticsIcon />,
              },
            ],
          },
        ];
      case 'tenant_admin':
        return [
          {
            title: 'Dashboard',
            path: '/tenant-admin/dashboard',
            icon: <DashboardIcon />,
          },
          {
            title: 'Shop Management',
            icon: <StoreIcon />,
            children: [
              {
                title: 'All Shops',
                path: '/tenant-admin/shops',
                icon: <StoreIcon />,
              },
              {
                title: 'Add New Shop',
                path: '/tenant-admin/shops/new',
                icon: <StoreIcon />,
              },
              {
                title: 'Shop Performance',
                path: '/tenant-admin/shop-performance',
                icon: <AnalyticsIcon />,
              },
            ],
          },
          {
            title: 'Team Management',
            icon: <PeopleIcon />,
            children: [
              {
                title: 'All Team Members',
                path: '/tenant-admin/team',
                icon: <PeopleIcon />,
              },
              {
                title: 'Add Team Member',
                path: '/tenant-admin/team/new',
                icon: <PeopleIcon />,
              },
              {
                title: 'Team Performance',
                path: '/tenant-admin/team-performance',
                icon: <AnalyticsIcon />,
              },
            ],
          },
          {
            title: 'Brand Management',
            icon: <BusinessIcon />,
            children: [
              {
                title: 'All Brands',
                path: '/tenant-admin/brands',
                icon: <BusinessIcon />,
              },
              {
                title: 'Add New Brand',
                path: '/tenant-admin/brands/new',
                icon: <BusinessIcon />,
              },
              {
                title: 'Brand Categories',
                path: '/tenant-admin/brand-categories',
                icon: <BusinessIcon />,
              },
              {
                title: 'Price Management',
                path: '/tenant-admin/price-management',
                icon: <MonetizationOn />,
              },
            ],
          },
          {
            title: 'Supplier Management',
            icon: <SupplierIcon />,
            children: [
              {
                title: 'All Suppliers',
                path: '/tenant-admin/suppliers',
                icon: <SupplierIcon />,
              },
              {
                title: 'Add New Supplier',
                path: '/tenant-admin/suppliers/new',
                icon: <SupplierIcon />,
              },
              {
                title: 'Supplier Performance',
                path: '/tenant-admin/supplier-performance',
                icon: <AnalyticsIcon />,
              },
            ],
          },
          {
            title: 'Financial Accounting',
            icon: <FinancialIcon />,
            children: [
              {
                title: 'Chart of Accounts',
                path: '/tenant-admin/chart-of-accounts',
                icon: <FinancialIcon />,
              },
              {
                title: 'General Ledger',
                path: '/tenant-admin/general-ledger',
                icon: <FinancialIcon />,
              },
              {
                title: 'Profit & Loss',
                path: '/tenant-admin/profit-loss',
                icon: <FinancialIcon />,
              },
              {
                title: 'Balance Sheet',
                path: '/tenant-admin/balance-sheet',
                icon: <FinancialIcon />,
              },
            ],
          },
          {
            title: 'Reports & Analytics',
            icon: <ReportIcon />,
            children: [
              {
                title: 'Sales Reports',
                path: '/tenant-admin/sales-reports',
                icon: <SalesIcon />,
              },
              {
                title: 'Inventory Reports',
                path: '/tenant-admin/inventory-reports',
                icon: <InventoryIcon />,
              },
              {
                title: 'Financial Reports',
                path: '/tenant-admin/financial-reports',
                icon: <FinancialIcon />,
              },
              {
                title: 'Custom Reports',
                path: '/tenant-admin/custom-reports',
                icon: <ReportIcon />,
              },
            ],
          },
          {
            title: 'Business Settings',
            icon: <SettingsIcon />,
            children: [
              {
                title: 'Company Profile',
                path: '/tenant-admin/company-profile',
                icon: <BusinessIcon />,
              },
              {
                title: 'Approval Workflows',
                path: '/tenant-admin/approval-workflows',
                icon: <ApprovalIcon />,
              },
              {
                title: 'Role Permissions',
                path: '/tenant-admin/role-permissions',
                icon: <SecurityIcon />,
              },
            ],
          },
        ];
      case 'manager':
        return [
          {
            title: 'Dashboard',
            path: '/manager/dashboard',
            icon: <DashboardIcon />,
          },
          {
            title: 'Inventory Management',
            icon: <InventoryIcon />,
            children: [
              {
                title: 'Stock Levels',
                path: '/manager/stock-levels',
                icon: <InventoryIcon />,
              },
              {
                title: 'Stock Transfers',
                path: '/manager/stock-transfers',
                icon: <InventoryIcon />,
              },
              {
                title: 'Expiry Tracking',
                path: '/manager/expiry-tracking',
                icon: <InventoryIcon />,
              },
            ],
          },
          {
            title: 'Sales Management',
            icon: <SalesIcon />,
            children: [
              {
                title: 'Pending Sales',
                path: '/manager/pending-sales',
                icon: <SalesIcon />,
              },
              {
                title: 'Approved Sales',
                path: '/manager/approved-sales',
                icon: <SalesIcon />,
              },
              {
                title: 'Sales History',
                path: '/manager/sales-history',
                icon: <SalesIcon />,
              },
            ],
          },
          {
            title: 'Returns Management',
            icon: <ReturnIcon />,
            children: [
              {
                title: 'Pending Returns',
                path: '/manager/pending-returns',
                icon: <ReturnIcon />,
              },
              {
                title: 'Return History',
                path: '/manager/return-history',
                icon: <ReturnIcon />,
              },
            ],
          },
          {
            title: 'Purchase Management',
            icon: <PurchaseIcon />,
            children: [
              {
                title: 'Create Purchase Order',
                path: '/manager/create-purchase-order',
                icon: <PurchaseIcon />,
              },
              {
                title: 'Purchase Order Tracking',
                path: '/manager/purchase-order-tracking',
                icon: <PurchaseIcon />,
              },
              {
                title: 'Receive Inventory',
                path: '/manager/receive-inventory',
                icon: <InventoryIcon />,
              },
            ],
          },
          {
            title: 'Financial Verification',
            icon: <FinancialIcon />,
            children: [
              {
                title: 'Pending Deposits',
                path: '/manager/pending-deposits',
                icon: <CashIcon />,
              },
              {
                title: 'Pending Expenses',
                path: '/manager/pending-expenses',
                icon: <CashIcon />,
              },
              {
                title: 'Financial Reconciliation',
                path: '/manager/financial-reconciliation',
                icon: <FinancialIcon />,
              },
            ],
          },
          {
            title: 'Approval Center',
            icon: <ApprovalIcon />,
            children: [
              {
                title: 'Sales Approvals',
                path: '/manager/sales-approvals',
                icon: <SalesIcon />,
              },
              {
                title: 'Adjustment Approvals',
                path: '/manager/adjustment-approvals',
                icon: <InventoryIcon />,
              },
              {
                title: 'Return Approvals',
                path: '/manager/return-approvals',
                icon: <ReturnIcon />,
              },
              {
                title: 'Batch Approvals',
                path: '/manager/batch-approvals',
                icon: <ApprovalIcon />,
              },
            ],
          },
          {
            title: 'Analytics',
            icon: <AnalyticsIcon />,
            children: [
              {
                title: 'Sales Analytics',
                path: '/manager/sales-analytics',
                icon: <SalesIcon />,
              },
              {
                title: 'Inventory Analytics',
                path: '/manager/inventory-analytics',
                icon: <InventoryIcon />,
              },
              {
                title: 'Executive Performance',
                path: '/manager/executive-performance',
                icon: <PeopleIcon />,
              },
            ],
          },
        ];
      case 'assistant_manager':
        return [
          {
            title: 'Dashboard',
            path: '/assistant-manager/dashboard',
            icon: <DashboardIcon />,
          },
          {
            title: 'Inventory Management',
            icon: <InventoryIcon />,
            children: [
              {
                title: 'View Stock Levels',
                path: '/assistant-manager/stock-levels',
                icon: <InventoryIcon />,
              },
              {
                title: 'Stock Transfers',
                path: '/assistant-manager/stock-transfers',
                icon: <InventoryIcon />,
              },
              {
                title: 'Expiry Tracking',
                path: '/assistant-manager/expiry-tracking',
                icon: <InventoryIcon />,
              },
            ],
          },
          {
            title: 'Pending Approvals',
            icon: <ApprovalIcon />,
            children: [
              {
                title: 'Sales Approvals',
                path: '/assistant-manager/sales-approvals',
                icon: <SalesIcon />,
              },
              {
                title: 'Adjustment Approvals',
                path: '/assistant-manager/adjustment-approvals',
                icon: <InventoryIcon />,
              },
              {
                title: 'Return Approvals',
                path: '/assistant-manager/return-approvals',
                icon: <ReturnIcon />,
              },
            ],
          },
          {
            title: 'Purchase Management',
            icon: <PurchaseIcon />,
            children: [
              {
                title: 'Create Purchase Order',
                path: '/assistant-manager/create-purchase-order',
                icon: <PurchaseIcon />,
              },
              {
                title: 'Track Purchase Orders',
                path: '/assistant-manager/track-purchase-orders',
                icon: <PurchaseIcon />,
              },
              {
                title: 'Receive Inventory',
                path: '/assistant-manager/receive-inventory',
                icon: <InventoryIcon />,
              },
            ],
          },
          {
            title: 'Analytics',
            icon: <AnalyticsIcon />,
            children: [
              {
                title: 'Sales Analytics',
                path: '/assistant-manager/sales-analytics',
                icon: <SalesIcon />,
              },
              {
                title: 'Inventory Analytics',
                path: '/assistant-manager/inventory-analytics',
                icon: <InventoryIcon />,
              },
              {
                title: 'Executive Analytics',
                path: '/assistant-manager/executive-analytics',
                icon: <PeopleIcon />,
              },
            ],
          },
        ];
      case 'executive':
        return [
          {
            title: 'Dashboard',
            path: '/executive/dashboard',
            icon: <DashboardIcon />,
          },
          {
            title: 'Sales',
            icon: <SalesIcon />,
            children: [
              {
                title: 'New Sale',
                path: '/executive/new-sale',
                icon: <SalesIcon />,
              },
              {
                title: 'Batch Sale Entry',
                path: '/executive/batch-sale',
                icon: <SalesIcon />,
              },
              {
                title: 'View My Sales',
                path: '/executive/my-sales',
                icon: <SalesIcon />,
              },
              {
                title: 'Draft Sales',
                path: '/executive/draft-sales',
                icon: <SalesIcon />,
              },
            ],
          },
          {
            title: 'Stock Management',
            icon: <InventoryIcon />,
            children: [
              {
                title: 'Single Adjustment',
                path: '/executive/single-adjustment',
                icon: <InventoryIcon />,
              },
              {
                title: 'Batch Adjustment',
                path: '/executive/batch-adjustment',
                icon: <InventoryIcon />,
              },
              {
                title: 'View My Adjustments',
                path: '/executive/my-adjustments',
                icon: <InventoryIcon />,
              },
            ],
          },
          {
            title: 'Returns',
            icon: <ReturnIcon />,
            children: [
              {
                title: 'Create Return',
                path: '/executive/create-return',
                icon: <ReturnIcon />,
              },
              {
                title: 'View My Returns',
                path: '/executive/my-returns',
                icon: <ReturnIcon />,
              },
            ],
          },
          {
            title: 'Cash Management',
            icon: <CashIcon />,
            children: [
              {
                title: 'Cash Balance',
                path: '/executive/cash-balance',
                icon: <CashIcon />,
              },
              {
                title: 'Record Bank Deposit',
                path: '/executive/record-deposit',
                icon: <CashIcon />,
              },
              {
                title: 'Record Expense',
                path: '/executive/record-expense',
                icon: <CashIcon />,
              },
              {
                title: 'Cash History',
                path: '/executive/cash-history',
                icon: <CashIcon />,
              },
            ],
          },
          {
            title: 'Daily Summary',
            icon: <SummaryIcon />,
            children: [
              {
                title: "Today's Summary",
                path: '/executive/today-summary',
                icon: <SummaryIcon />,
              },
              {
                title: 'Payment Breakdown',
                path: '/executive/payment-breakdown',
                icon: <CashIcon />,
              },
              {
                title: 'Brand-wise Sales',
                path: '/executive/brand-sales',
                icon: <BusinessIcon />,
              },
            ],
          },
          {
            title: 'My Approvals',
            icon: <ApprovalIcon />,
            children: [
              {
                title: 'Pending Items',
                path: '/executive/pending-approvals',
                icon: <ApprovalIcon />,
              },
              {
                title: 'Approved Items',
                path: '/executive/approved-items',
                icon: <ApprovalIcon />,
              },
              {
                title: 'Rejected Items',
                path: '/executive/rejected-items',
                icon: <ApprovalIcon />,
              },
            ],
          },
        ];
      default:
        return [];
    }
  };

  const menuItems = getMenuItems();

  const renderMenuItems = (items: MenuItem[]) => {
    return items.map((item) => {
      // Check if the item should be shown for the current user role
      if (item.roles && user && !item.roles.includes(user.role)) {
        return null;
      }

      // If the item has children, render a collapsible menu
      if (item.children) {
        const isSubMenuOpen = openSubMenus[item.title] || false;
        const isAnyChildActive = item.children.some(
          (child) => child.path && isActive(child.path)
        );

        return (
          <React.Fragment key={item.title}>
            <ListItem disablePadding>
              <ListItemButton
                onClick={() => handleSubMenuToggle(item.title)}
                selected={isAnyChildActive}
                sx={{
                  pl: 2,
                  py: 1.5,
                  '&.Mui-selected': {
                    backgroundColor: 'rgba(94, 53, 177, 0.08)',
                    '&:hover': {
                      backgroundColor: 'rgba(94, 53, 177, 0.12)',
                    },
                  },
                }}
              >
                <ListItemIcon sx={{ color: isAnyChildActive ? 'primary.main' : 'inherit' }}>
                  {item.icon}
                </ListItemIcon>
                <ListItemText
                  primary={item.title}
                  primaryTypographyProps={{
                    fontWeight: isAnyChildActive ? 600 : 400,
                    color: isAnyChildActive ? 'primary.main' : 'inherit',
                  }}
                />
                {isSubMenuOpen ? <ExpandLess /> : <ExpandMore />}
              </ListItemButton>
            </ListItem>
            <Collapse in={isSubMenuOpen} timeout="auto" unmountOnExit>
              <List component="div" disablePadding>
                {item.children.map((child) => (
                  <ListItem key={child.title} disablePadding>
                    <ListItemButton
                      onClick={() => child.path && handleNavigate(child.path)}
                      selected={child.path ? isActive(child.path) : false}
                      sx={{
                        pl: 6,
                        py: 1.25,
                        '&.Mui-selected': {
                          backgroundColor: 'rgba(94, 53, 177, 0.08)',
                          '&:hover': {
                            backgroundColor: 'rgba(94, 53, 177, 0.12)',
                          },
                        },
                      }}
                    >
                      <ListItemIcon
                        sx={{
                          color: child.path && isActive(child.path) ? 'primary.main' : 'inherit',
                          minWidth: 36,
                        }}
                      >
                        {child.icon}
                      </ListItemIcon>
                      <ListItemText
                        primary={child.title}
                        primaryTypographyProps={{
                          fontSize: '0.875rem',
                          fontWeight: child.path && isActive(child.path) ? 600 : 400,
                          color: child.path && isActive(child.path) ? 'primary.main' : 'inherit',
                        }}
                      />
                    </ListItemButton>
                  </ListItem>
                ))}
              </List>
            </Collapse>
          </React.Fragment>
        );
      }

      // Otherwise, render a regular menu item
      return (
        <ListItem key={item.title} disablePadding>
          <ListItemButton
            onClick={() => item.path && handleNavigate(item.path)}
            selected={item.path ? isActive(item.path) : false}
            sx={{
              pl: 2,
              py: 1.5,
              '&.Mui-selected': {
                backgroundColor: 'rgba(94, 53, 177, 0.08)',
                '&:hover': {
                  backgroundColor: 'rgba(94, 53, 177, 0.12)',
                },
              },
            }}
          >
            <ListItemIcon
              sx={{ color: item.path && isActive(item.path) ? 'primary.main' : 'inherit' }}
            >
              {item.icon}
            </ListItemIcon>
            <ListItemText
              primary={item.title}
              primaryTypographyProps={{
                fontWeight: item.path && isActive(item.path) ? 600 : 400,
                color: item.path && isActive(item.path) ? 'primary.main' : 'inherit',
              }}
            />
          </ListItemButton>
        </ListItem>
      );
    });
  };

  const drawerContent = (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          p: 2,
          backgroundColor: 'primary.main',
          color: 'white',
        }}
      >
        <Typography variant="h6" component="div" sx={{ fontWeight: 600 }}>
          Liquor Management
        </Typography>
        {isMobile && (
          <IconButton color="inherit" onClick={onClose} edge="end">
            <MenuIcon />
          </IconButton>
        )}
      </Box>

      <Box sx={{ p: 2 }}>
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            mb: 1,
          }}
        >
          <AccountIcon sx={{ mr: 1, color: 'primary.main' }} />
          <Box>
            <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
              {user?.full_name}
            </Typography>
            <Typography variant="body2" color="textSecondary">
              {user?.role.replace('_', ' ').replace(/\b\w/g, (l) => l.toUpperCase())}
            </Typography>
          </Box>
        </Box>
      </Box>

      <Divider />

      <Box sx={{ flexGrow: 1, overflow: 'auto' }}>
        <List component="nav" sx={{ px: 1 }}>
          {renderMenuItems(menuItems)}
        </List>
      </Box>

      <Divider />

      <List>
        <ListItem disablePadding>
          <ListItemButton onClick={logout} sx={{ py: 1.5 }}>
            <ListItemIcon>
              <LogoutIcon color="error" />
            </ListItemIcon>
            <ListItemText
              primary="Logout"
              primaryTypographyProps={{ color: 'error.main' }}
            />
          </ListItemButton>
        </ListItem>
      </List>
    </Box>
  );

  if (variant === 'temporary') {
    return (
      <Drawer
        variant="temporary"
        open={open}
        onClose={onClose}
        ModalProps={{
          keepMounted: true, // Better open performance on mobile
        }}
        sx={{
          display: { xs: 'block', md: 'none' },
          '& .MuiDrawer-paper': {
            boxSizing: 'border-box',
            width: 280,
          },
        }}
      >
        {drawerContent}
      </Drawer>
    );
  }

  return (
    <Drawer
      variant="permanent"
      open={open}
      sx={{
        display: { xs: 'none', md: 'block' },
        '& .MuiDrawer-paper': {
          boxSizing: 'border-box',
          width: 280,
          borderRight: 'none',
        },
      }}
    >
      {drawerContent}
    </Drawer>
  );
};

export default Sidebar;