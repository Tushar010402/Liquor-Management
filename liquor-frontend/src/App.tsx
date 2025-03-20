import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { CssBaseline } from '@mui/material';
import ThemeProvider from './theme/ThemeProvider';
import AuthProvider from './contexts/AuthContext';
import ProtectedRoute from './components/auth/ProtectedRoute';
import MainLayout from './components/layout/MainLayout';

// Auth pages
import LoginPage from './pages/auth/LoginPage';

// SaaS Admin pages
import SaasAdminDashboard from './pages/saas-admin/Dashboard';

// Tenant Admin pages
import TenantAdminDashboard from './pages/tenant-admin/Dashboard';

// Manager pages
import ManagerDashboard from './pages/manager/Dashboard';

// Assistant Manager pages
import AssistantManagerDashboard from './pages/assistant-manager/Dashboard';

// Executive pages
import ExecutiveDashboard from './pages/executive/Dashboard';
import NewSale from './pages/executive/Sales/NewSale';
import MySales from './pages/executive/Sales/MySales';
import SingleAdjustment from './pages/executive/Stock/SingleAdjustment';
const NotFoundPage = () => <div>404 - Page Not Found</div>;

const App: React.FC = () => {
  return (
    <ThemeProvider>
      <Router>
        <AuthProvider>
          <CssBaseline />
          <Routes>
            {/* Public routes */}
            <Route path="/login" element={<LoginPage />} />
            
            {/* Protected routes for SaaS Admin */}
            <Route element={<ProtectedRoute allowedRoles={['saas_admin']} />}>
              <Route element={<MainLayout />}>
                <Route path="/saas-admin/dashboard" element={<SaasAdminDashboard />} />
                <Route path="/saas-admin/tenants" element={<div>Tenants List</div>} />
                <Route path="/saas-admin/tenants/new" element={<div>Add New Tenant</div>} />
                <Route path="/saas-admin/billing-plans" element={<div>Billing Plans</div>} />
                <Route path="/saas-admin/team" element={<div>Team Members</div>} />
                <Route path="/saas-admin/roles" element={<div>Role Management</div>} />
                <Route path="/saas-admin/system-health" element={<div>System Health</div>} />
                <Route path="/saas-admin/error-logs" element={<div>Error Logs</div>} />
                <Route path="/saas-admin/system-config" element={<div>System Configuration</div>} />
                <Route path="/saas-admin/backup-schedule" element={<div>Backup Schedule</div>} />
                <Route path="/saas-admin/manual-backup" element={<div>Manual Backup</div>} />
                <Route path="/saas-admin/restore-data" element={<div>Restore Data</div>} />
                <Route path="/saas-admin/tenant-growth" element={<div>Tenant Growth</div>} />
                <Route path="/saas-admin/revenue-analytics" element={<div>Revenue Analytics</div>} />
                <Route path="/saas-admin/usage-statistics" element={<div>Usage Statistics</div>} />
                <Route path="/saas-admin/profile" element={<div>Profile</div>} />
                <Route path="/saas-admin/settings" element={<div>Settings</div>} />
              </Route>
            </Route>
            
            {/* Protected routes for Tenant Admin */}
            <Route element={<ProtectedRoute allowedRoles={['tenant_admin']} />}>
              <Route element={<MainLayout />}>
                <Route path="/tenant-admin/dashboard" element={<TenantAdminDashboard />} />
                <Route path="/tenant-admin/shops" element={<div>Shops List</div>} />
                <Route path="/tenant-admin/shops/new" element={<div>Add New Shop</div>} />
                <Route path="/tenant-admin/shop-performance" element={<div>Shop Performance</div>} />
                <Route path="/tenant-admin/team" element={<div>Team Members</div>} />
                <Route path="/tenant-admin/team/new" element={<div>Add Team Member</div>} />
                <Route path="/tenant-admin/team-performance" element={<div>Team Performance</div>} />
                <Route path="/tenant-admin/brands" element={<div>Brands List</div>} />
                <Route path="/tenant-admin/brands/new" element={<div>Add New Brand</div>} />
                <Route path="/tenant-admin/brand-categories" element={<div>Brand Categories</div>} />
                <Route path="/tenant-admin/price-management" element={<div>Price Management</div>} />
                <Route path="/tenant-admin/suppliers" element={<div>Suppliers List</div>} />
                <Route path="/tenant-admin/suppliers/new" element={<div>Add New Supplier</div>} />
                <Route path="/tenant-admin/supplier-performance" element={<div>Supplier Performance</div>} />
                <Route path="/tenant-admin/chart-of-accounts" element={<div>Chart of Accounts</div>} />
                <Route path="/tenant-admin/general-ledger" element={<div>General Ledger</div>} />
                <Route path="/tenant-admin/profit-loss" element={<div>Profit & Loss</div>} />
                <Route path="/tenant-admin/balance-sheet" element={<div>Balance Sheet</div>} />
                <Route path="/tenant-admin/sales-reports" element={<div>Sales Reports</div>} />
                <Route path="/tenant-admin/inventory-reports" element={<div>Inventory Reports</div>} />
                <Route path="/tenant-admin/financial-reports" element={<div>Financial Reports</div>} />
                <Route path="/tenant-admin/custom-reports" element={<div>Custom Reports</div>} />
                <Route path="/tenant-admin/company-profile" element={<div>Company Profile</div>} />
                <Route path="/tenant-admin/approval-workflows" element={<div>Approval Workflows</div>} />
                <Route path="/tenant-admin/role-permissions" element={<div>Role Permissions</div>} />
                <Route path="/tenant-admin/profile" element={<div>Profile</div>} />
                <Route path="/tenant-admin/settings" element={<div>Settings</div>} />
              </Route>
            </Route>
            
            {/* Protected routes for Manager */}
            <Route element={<ProtectedRoute allowedRoles={['manager']} />}>
              <Route element={<MainLayout />}>
                <Route path="/manager/dashboard" element={<ManagerDashboard />} />
                <Route path="/manager/stock-levels" element={<div>Stock Levels</div>} />
                <Route path="/manager/stock-transfers" element={<div>Stock Transfers</div>} />
                <Route path="/manager/expiry-tracking" element={<div>Expiry Tracking</div>} />
                <Route path="/manager/pending-sales" element={<div>Pending Sales</div>} />
                <Route path="/manager/approved-sales" element={<div>Approved Sales</div>} />
                <Route path="/manager/sales-history" element={<div>Sales History</div>} />
                <Route path="/manager/pending-returns" element={<div>Pending Returns</div>} />
                <Route path="/manager/return-history" element={<div>Return History</div>} />
                <Route path="/manager/create-purchase-order" element={<div>Create Purchase Order</div>} />
                <Route path="/manager/purchase-order-tracking" element={<div>Purchase Order Tracking</div>} />
                <Route path="/manager/receive-inventory" element={<div>Receive Inventory</div>} />
                <Route path="/manager/pending-deposits" element={<div>Pending Deposits</div>} />
                <Route path="/manager/pending-expenses" element={<div>Pending Expenses</div>} />
                <Route path="/manager/financial-reconciliation" element={<div>Financial Reconciliation</div>} />
                <Route path="/manager/sales-approvals" element={<div>Sales Approvals</div>} />
                <Route path="/manager/adjustment-approvals" element={<div>Adjustment Approvals</div>} />
                <Route path="/manager/return-approvals" element={<div>Return Approvals</div>} />
                <Route path="/manager/batch-approvals" element={<div>Batch Approvals</div>} />
                <Route path="/manager/sales-analytics" element={<div>Sales Analytics</div>} />
                <Route path="/manager/inventory-analytics" element={<div>Inventory Analytics</div>} />
                <Route path="/manager/executive-performance" element={<div>Executive Performance</div>} />
                <Route path="/manager/profile" element={<div>Profile</div>} />
                <Route path="/manager/settings" element={<div>Settings</div>} />
              </Route>
            </Route>
            
            {/* Protected routes for Assistant Manager */}
            <Route element={<ProtectedRoute allowedRoles={['assistant_manager']} />}>
              <Route element={<MainLayout />}>
                <Route path="/assistant-manager/dashboard" element={<AssistantManagerDashboard />} />
                <Route path="/assistant-manager/stock-levels" element={<div>Stock Levels</div>} />
                <Route path="/assistant-manager/stock-transfers" element={<div>Stock Transfers</div>} />
                <Route path="/assistant-manager/expiry-tracking" element={<div>Expiry Tracking</div>} />
                <Route path="/assistant-manager/sales-approvals" element={<div>Sales Approvals</div>} />
                <Route path="/assistant-manager/adjustment-approvals" element={<div>Adjustment Approvals</div>} />
                <Route path="/assistant-manager/return-approvals" element={<div>Return Approvals</div>} />
                <Route path="/assistant-manager/create-purchase-order" element={<div>Create Purchase Order</div>} />
                <Route path="/assistant-manager/track-purchase-orders" element={<div>Track Purchase Orders</div>} />
                <Route path="/assistant-manager/receive-inventory" element={<div>Receive Inventory</div>} />
                <Route path="/assistant-manager/sales-analytics" element={<div>Sales Analytics</div>} />
                <Route path="/assistant-manager/inventory-analytics" element={<div>Inventory Analytics</div>} />
                <Route path="/assistant-manager/executive-analytics" element={<div>Executive Analytics</div>} />
                <Route path="/assistant-manager/profile" element={<div>Profile</div>} />
                <Route path="/assistant-manager/settings" element={<div>Settings</div>} />
              </Route>
            </Route>
            
            {/* Protected routes for Executive */}
            <Route element={<ProtectedRoute allowedRoles={['executive']} />}>
              <Route element={<MainLayout />}>
                <Route path="/executive/dashboard" element={<ExecutiveDashboard />} />
                <Route path="/executive/new-sale" element={<NewSale />} />
                <Route path="/executive/batch-sale" element={<div>Batch Sale Entry</div>} />
                <Route path="/executive/my-sales" element={<MySales />} />
                <Route path="/executive/draft-sales" element={<div>Draft Sales</div>} />
                <Route path="/executive/single-adjustment" element={<SingleAdjustment />} />
                <Route path="/executive/batch-adjustment" element={<div>Batch Adjustment</div>} />
                <Route path="/executive/my-adjustments" element={<div>View My Adjustments</div>} />
                <Route path="/executive/create-return" element={<div>Create Return</div>} />
                <Route path="/executive/my-returns" element={<div>View My Returns</div>} />
                <Route path="/executive/cash-balance" element={<div>Cash Balance</div>} />
                <Route path="/executive/record-deposit" element={<div>Record Bank Deposit</div>} />
                <Route path="/executive/record-expense" element={<div>Record Expense</div>} />
                <Route path="/executive/cash-history" element={<div>Cash History</div>} />
                <Route path="/executive/today-summary" element={<div>Today's Summary</div>} />
                <Route path="/executive/payment-breakdown" element={<div>Payment Breakdown</div>} />
                <Route path="/executive/brand-sales" element={<div>Brand-wise Sales</div>} />
                <Route path="/executive/pending-approvals" element={<div>Pending Items</div>} />
                <Route path="/executive/approved-items" element={<div>Approved Items</div>} />
                <Route path="/executive/rejected-items" element={<div>Rejected Items</div>} />
                <Route path="/executive/profile" element={<div>Profile</div>} />
                <Route path="/executive/settings" element={<div>Settings</div>} />
              </Route>
            </Route>
            
            {/* Redirect root to login */}
            <Route path="/" element={<Navigate to="/login" replace />} />
            
            {/* 404 page */}
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </AuthProvider>
      </Router>
    </ThemeProvider>
  );
};

export default App;
