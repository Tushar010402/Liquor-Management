# UI Component Structure by Role

## SaaS Admin Sidebar Menu

```
├── Dashboard
├── Tenant Management
│   ├── All Tenants
│   ├── Add New Tenant
│   ├── Billing Plans
│   └── Tenant Activity
├── Platform Team
│   ├── Team Members
│   ├── Add Team Member
│   └── Role Management
├── System Administration
│   ├── System Health
│   ├── API Usage
│   ├── Error Logs
│   └── System Configuration
├── Backup & Restore
│   ├── Backup Schedule
│   ├── Manual Backup
│   └── Restore Data
├── Platform Analytics
│   ├── Tenant Growth
│   ├── Revenue Analytics
│   └── Usage Statistics
├── Activity Monitoring
│   ├── User Registrations
│   ├── Tenant Activity
│   ├── Sales Transactions
│   └── Inventory Changes
├── Audit Logs
│   ├── User Action Logs
│   ├── Security Logs
│   ├── System Change Logs
│   └── Export Audit Data
└── My Account
    ├── Profile Settings
    ├── Security Settings
    └── Notification Settings
```

## Tenant Admin Sidebar Menu

```
├── Dashboard
├── Shop Management
│   ├── All Shops
│   ├── Add New Shop
│   └── Shop Performance
├── Team Management
│   ├── All Team Members
│   ├── Add Team Member
│   └── Team Performance
├── Brand Management
│   ├── All Brands
│   ├── Add New Brand
│   ├── Brand Categories
│   ├── Price Management
│   └── Bulk Updates
├── Supplier Management
│   ├── All Suppliers
│   ├── Add New Supplier
│   ├── Supplier Performance
│   └── Supplier History
├── Tax Management
│   ├── Tax Categories
│   ├── Product Tax Assignment
│   └── Tax Reports
├── Financial Accounting
│   ├── Chart of Accounts
│   ├── General Ledger
│   ├── Profit & Loss
│   ├── Balance Sheet
│   └── Bank Reconciliation
├── Reports & Analytics
│   ├── Sales Reports
│   ├── Inventory Reports
│   ├── Financial Reports
│   ├── Tax Reports
│   ├── Executive Reports
│   └── Custom Reports
├── Business Settings
│   ├── Company Profile
│   ├── Approval Workflows
│   ├── Payment Methods
│   ├── Notification Settings
│   └── Role Permissions
└── My Account
    ├── Profile Settings
    ├── Security Settings
    └── Notification Preferences
```

## Manager Sidebar Menu

```
├── Dashboard
├── Inventory Management
│   ├── Stock Levels
│   ├── Stock Transfers
│   ├── Pending Stock Adjustments
│   ├── Add/Edit Brands
│   └── Expiry Tracking
├── Sales Management
│   ├── Pending Sales
│   ├── Approved Sales
│   ├── Sales History
│   └── Sales Targets
├── Returns Management
│   ├── Pending Returns
│   ├── Return History
│   └── Return Reports
├── Purchase Management
│   ├── Create Purchase Order
│   ├── Purchase Order Tracking
│   ├── Receive Inventory
│   ├── Purchase Invoices
│   └── Purchase History
├── Financial Verification
│   ├── Pending Deposits
│   ├── Pending UPI Transactions
│   ├── Pending Expenses
│   └── Financial Reconciliation
├── Approval Center
│   ├── Sales Approvals
│   ├── Adjustment Approvals
│   ├── Return Approvals
│   ├── Deposit Approvals
│   └── Batch Approvals
├── Analytics
│   ├── Sales Analytics
│   ├── Inventory Analytics
│   ├── Financial Analytics
│   ├── Executive Performance
│   └── Supplier Analytics
├── Reports
│   ├── Generate Reports
│   ├── Scheduled Reports
│   ├── Custom Reports
│   └── Report History
└── My Account
    ├── Profile Settings
    ├── Security Settings
    └── Notification Preferences
```

## Assistant Manager Sidebar Menu

```
├── Dashboard
├── Inventory Management
│   ├── View Stock Levels
│   ├── Stock Transfers
│   ├── Add/Edit Brands
│   └── Expiry Tracking
├── Pending Approvals
│   ├── Sales Approvals
│   ├── Adjustment Approvals
│   ├── Return Approvals
│   └── Deposit Approvals
├── Purchase Management
│   ├── Create Purchase Order
│   ├── Track Purchase Orders
│   └── Receive Inventory
├── Analytics
│   ├── Sales Analytics
│   ├── Inventory Analytics
│   └── Executive Analytics
├── Reports
│   ├── Generate Reports
│   └── Report History
└── My Account
    ├── Profile Settings
    ├── Security Settings
    └── Notification Preferences
```

## Executive Sidebar Menu

```
├── Dashboard
├── Shop Selector
│   └── [List of Assigned Shops]
├── Sales
│   ├── New Sale
│   ├── Batch Sale Entry
│   ├── View My Sales
│   └── Draft Sales
├── Stock Management
│   ├── Single Adjustment
│   ├── Batch Adjustment
│   ├── View My Adjustments
│   └── Draft Adjustments
├── Returns
│   ├── Create Return
│   ├── View My Returns
│   └── Return History
├── Cash Management
│   ├── Cash Balance
│   ├── Record Bank Deposit
│   ├── Record UPI Transaction
│   ├── Record Expense
│   └── Cash History
├── Daily Summary
│   ├── Today's Summary
│   ├── Payment Breakdown
│   ├── Brand-wise Sales
│   └── Summary Reports
├── Expiry Management
│   ├── View Expiring Items
│   ├── Report Expired Items
│   └── Expiry Actions
├── My Approvals
│   ├── Pending Items
│   ├── Approved Items
│   ├── Rejected Items
│   └── Resubmit Items
├── My Reports
│   ├── Daily Sales
│   ├── Stock Reports
│   └── Cash Reports
└── My Account
    ├── Profile Settings
    ├── Security Settings
    └── Notification Preferences
```

## Main Dashboard Components by Role

### SaaS Admin Dashboard
- Tenant growth metrics chart
- New registrations counter
- System health status indicators
- Billing status summary
- Recent platform activities
- API usage statistics
- Quick action shortcuts

### Tenant Admin Dashboard
- Multi-shop performance overview
- Sales trend chart (daily/weekly/monthly)
- Top performing brands
- Stock value summary
- Team performance metrics
- Pending approvals counter
- Financial highlights
- Quick action shortcuts

### Manager Dashboard
- Shop-specific sales metrics
- Pending approvals counter with breakdown
- Low stock alerts
- Expiring stock notifications
- Financial reconciliation status
- Executive performance summary
- Recent activities log
- Quick action shortcuts

### Assistant Manager Dashboard
- Stock level summary
- Pending approvals counter
- Daily sales progress
- Purchase order status
- Expiry alerts
- Team activity summary
- Quick action shortcuts

### Executive Dashboard
- Active shop indicator
- Daily sales target progress
- Stock adjustment status
- Cash balance summary
- Pending approvals status
- Recent activities log
- Quick action shortcuts