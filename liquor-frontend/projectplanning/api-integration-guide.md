# Liquor Shop Management System - API Integration Guide

This document serves as a comprehensive guide for frontend developers to integrate with the Liquor Shop Management System backend APIs. It covers authentication, data formats, endpoints, and common workflows.

## Table of Contents

1. [Authentication](#authentication)
2. [General API Conventions](#general-api-conventions)
3. [User Roles and Permissions](#user-roles-and-permissions)
4. [API Endpoints by Module](#api-endpoints-by-module)
    - [Authentication Module](#authentication-module)
    - [Tenant Management](#tenant-management)
    - [Shop Management](#shop-management)
    - [User Management](#user-management)
    - [Inventory Management](#inventory-management)
    - [Sales Management](#sales-management)
    - [Cash Management](#cash-management)
    - [Reports Module](#reports-module)
    - [Analytics Module](#analytics-module)
    - [SaaS Admin Module](#saas-admin-module)
5. [Common Workflows](#common-workflows)
6. [Error Handling](#error-handling)
7. [Pagination](#pagination)
8. [Filtering and Sorting](#filtering-and-sorting)

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. All authenticated requests should include the Authorization header.

### Getting a Token

```
POST /api/auth/login/
```

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "secure_password"
}
```

**Response:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1...",
    "user": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "user@example.com",
        "full_name": "John Doe",
        "role": "manager",
        "tenant": "550e8400-e29b-41d4-a716-446655441111",
        "assigned_shops": ["550e8400-e29b-41d4-a716-446655442222"]
    }
}
```

### Using the Token

Include the access token in the Authorization header for all authenticated requests:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1...
```

### Refreshing a Token

```
POST /api/auth/token/refresh/
```

**Request Body:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1..."
}
```

**Response:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1..."
}
```

## General API Conventions

- All API endpoints are prefixed with `/api/`
- All responses are in JSON format
- Most list endpoints support pagination, filtering, and sorting
- Dates and times are in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)
- UUIDs are used as primary keys
- Nested resources are generally accessed using the parent resource ID

## User Roles and Permissions

The system has the following user roles, each with different permissions:

1. **SaaS Admin**: System-wide administration, tenant management
2. **Tenant Admin**: Manages all shops, users, inventory, and data for a tenant
3. **Manager**: Manages operations for assigned shops
4. **Assistant Manager**: Assists the manager in shop operations
5. **Executive**: Handles sales and daily operations

Endpoints will return 403 Forbidden if the user doesn't have permission to access them.

## API Endpoints by Module

### Authentication Module

#### Login
```
POST /api/auth/login/
```
Authenticates a user and returns tokens.

#### Logout
```
POST /api/auth/logout/
```
Invalidates the refresh token.

#### Password Change
```
POST /api/auth/password/change/
```
Changes the user's password.

**Request Body:**
```json
{
    "old_password": "current_password",
    "new_password": "new_secure_password"
}
```

#### Password Reset Request
```
POST /api/auth/password/reset/
```
Initiates a password reset process by sending an email.

**Request Body:**
```json
{
    "email": "user@example.com"
}
```

#### Password Reset Confirm
```
POST /api/auth/password/reset/confirm/
```
Completes the password reset process.

**Request Body:**
```json
{
    "token": "reset_token_from_email",
    "uid": "user_id_from_email",
    "new_password": "new_secure_password"
}
```

### Tenant Management

#### List Tenants (SaaS Admin only)
```
GET /api/saas/tenants/
```
Returns a list of all tenants in the system.

#### Create Tenant (SaaS Admin only)
```
POST /api/saas/tenants/
```
Creates a new tenant.

**Request Body:**
```json
{
    "name": "ABC Liquors",
    "address": "123 Main St, Cityville",
    "phone": "1234567890",
    "email": "contact@abcliquors.com",
    "admin_email": "admin@abcliquors.com",
    "admin_name": "John Smith"
}
```

#### Get Tenant Details
```
GET /api/saas/tenants/{tenant_id}/
```
Returns details of a specific tenant.

#### Update Tenant
```
PATCH /api/saas/tenants/{tenant_id}/
```
Updates a tenant's information.

**Request Body (partial):**
```json
{
    "phone": "9876543210",
    "address": "456 New St, Townsville"
}
```

#### Deactivate Tenant
```
POST /api/saas/tenants/{tenant_id}/deactivate/
```
Deactivates a tenant.

#### Activate Tenant
```
POST /api/saas/tenants/{tenant_id}/activate/
```
Activates a previously deactivated tenant.

### Shop Management

#### List Shops
```
GET /api/tenants/shops/
```
Returns a list of shops for the current tenant.

#### Create Shop
```
POST /api/tenants/shops/
```
Creates a new shop for the current tenant.

**Request Body:**
```json
{
    "name": "Downtown Store",
    "address": "789 Center Ave, Cityville",
    "license_number": "LIQ123456",
    "contact_phone": "1234567890",
    "contact_email": "downtown@abcliquors.com"
}
```

#### Get Shop Details
```
GET /api/tenants/shops/{shop_id}/
```
Returns details of a specific shop.

#### Update Shop
```
PATCH /api/tenants/shops/{shop_id}/
```
Updates a shop's information.

**Request Body (partial):**
```json
{
    "contact_phone": "9876543210",
    "address": "790 Center Ave, Cityville"
}
```

#### Deactivate Shop
```
POST /api/tenants/shops/{shop_id}/deactivate/
```
Deactivates a shop.

#### Activate Shop
```
POST /api/tenants/shops/{shop_id}/activate/
```
Activates a previously deactivated shop.

### User Management

#### List Users
```
GET /api/accounts/users/
```
Returns a list of users for the current tenant.

#### Create User
```
POST /api/accounts/users/
```
Creates a new user for the current tenant.

**Request Body:**
```json
{
    "email": "manager@abcliquors.com",
    "full_name": "Jane Smith",
    "phone": "1234567890",
    "role": "manager",
    "assigned_shops": ["550e8400-e29b-41d4-a716-446655442222"]
}
```

#### Get User Details
```
GET /api/accounts/users/{user_id}/
```
Returns details of a specific user.

#### Update User
```
PATCH /api/accounts/users/{user_id}/
```
Updates a user's information.

**Request Body (partial):**
```json
{
    "phone": "9876543210",
    "role": "assistant_manager"
}
```

#### Deactivate User
```
POST /api/accounts/users/{user_id}/deactivate/
```
Deactivates a user.

#### Activate User
```
POST /api/accounts/users/{user_id}/activate/
```
Activates a previously deactivated user.

#### Assign Shops to User
```
POST /api/accounts/users/{user_id}/assign-shops/
```
Assigns shops to a user.

**Request Body:**
```json
{
    "shop_ids": ["550e8400-e29b-41d4-a716-446655442222", "550e8400-e29b-41d4-a716-446655443333"]
}
```

### Inventory Management

#### List Stock
```
GET /api/inventory/stock/
```
Returns a list of stock items.

#### Get Stock by Shop
```
GET /api/inventory/stock/?shop={shop_id}
```
Returns stock items for a specific shop.

#### Create or Update Stock
```
POST /api/inventory/stock/
```
Creates or updates stock for a product in a shop.

**Request Body:**
```json
{
    "shop": "550e8400-e29b-41d4-a716-446655442222",
    "brand": "550e8400-e29b-41d4-a716-446655444444",
    "size": "750ml",
    "quantity": 50,
    "purchase_price": "800.00",
    "selling_price": "1000.00"
}
```

#### Get Stock Details
```
GET /api/inventory/stock/{stock_id}/
```
Returns details of a specific stock item.

#### Update Stock
```
PATCH /api/inventory/stock/{stock_id}/
```
Updates a stock item's information.

**Request Body (partial):**
```json
{
    "quantity": 45,
    "selling_price": "1050.00"
}
```

#### List Brands
```
GET /api/inventory/brands/
```
Returns a list of brands.

#### Create Brand
```
POST /api/inventory/brands/
```
Creates a new brand.

**Request Body:**
```json
{
    "name": "Premium Whiskey",
    "category": "whiskey",
    "sizes": ["180ml", "375ml", "750ml"]
}
```

#### Update Brand
```
PATCH /api/inventory/brands/{brand_id}/
```
Updates a brand's information.

**Request Body (partial):**
```json
{
    "sizes": ["180ml", "375ml", "750ml", "1000ml"]
}
```

#### Stock Adjustment
```
POST /api/inventory/stock-adjustments/
```
Creates a stock adjustment request.

**Request Body:**
```json
{
    "shop": "550e8400-e29b-41d4-a716-446655442222",
    "notes": "Damage during delivery",
    "items": [
        {
            "stock": "550e8400-e29b-41d4-a716-446655455555",
            "quantity": -5,
            "reason": "damaged"
        }
    ]
}
```

#### Approve Stock Adjustment
```
POST /api/inventory/stock-adjustments/{adjustment_id}/approve/
```
Approves a stock adjustment.

**Request Body:**
```json
{
    "notes": "Verified the damaged inventory"
}
```

#### Reject Stock Adjustment
```
POST /api/inventory/stock-adjustments/{adjustment_id}/reject/
```
Rejects a stock adjustment.

**Request Body:**
```json
{
    "notes": "Documentation insufficient"
}
```

#### Stock Transfer
```
POST /api/inventory/stock-transfers/
```
Creates a stock transfer between shops.

**Request Body:**
```json
{
    "from_shop": "550e8400-e29b-41d4-a716-446655442222",
    "to_shop": "550e8400-e29b-41d4-a716-446655443333",
    "notes": "Balancing inventory",
    "items": [
        {
            "stock": "550e8400-e29b-41d4-a716-446655455555",
            "quantity": 10
        }
    ]
}
```

### Sales Management

#### Create Sale
```
POST /api/sales/
```
Creates a new sale.

**Request Body:**
```json
{
    "shop_id": "550e8400-e29b-41d4-a716-446655442222",
    "payment_method": "cash",
    "items": [
        {
            "stock_id": "550e8400-e29b-41d4-a716-446655455555",
            "quantity": 2,
            "price": "1000.00"
        },
        {
            "stock_id": "550e8400-e29b-41d4-a716-446655466666",
            "quantity": 5,
            "price": "180.00"
        }
    ]
}
```

#### Get Sale Details
```
GET /api/sales/{sale_id}/
```
Returns details of a specific sale.

#### List Sales
```
GET /api/sales/
```
Returns a list of sales.

#### Approve Sale (Manager only)
```
POST /api/sales/{sale_id}/approve/
```
Approves a pending sale.

**Request Body:**
```json
{
    "notes": "Sale approved after verification"
}
```

#### Reject Sale (Manager only)
```
POST /api/sales/{sale_id}/reject/
```
Rejects a pending sale.

**Request Body:**
```json
{
    "notes": "Sale rejected due to discrepancy"
}
```

#### Create Sale Return
```
POST /api/sales/returns/
```
Creates a sale return.

**Request Body:**
```json
{
    "sale_id": "550e8400-e29b-41d4-a716-446655477777",
    "items": [
        {
            "sale_item_id": "550e8400-e29b-41d4-a716-446655488888",
            "quantity": 1,
            "reason": "defective"
        }
    ],
    "notes": "Customer returned defective product"
}
```

#### Approve Sale Return (Manager only)
```
POST /api/sales/returns/{return_id}/approve/
```
Approves a sale return.

**Request Body:**
```json
{
    "notes": "Return approved after verification"
}
```

### Cash Management

#### Executive Daily Login
```
POST /api/executive/daily-login/
```
Records the executive's daily login with opening cash.

**Request Body:**
```json
{
    "shop_id": "550e8400-e29b-41d4-a716-446655442222",
    "opening_cash": "500.00"
}
```

#### Executive Daily Logout
```
POST /api/executive/daily-logout/
```
Records the executive's daily logout with closing cash.

**Request Body:**
```json
{
    "cash_amount": "3400.00",
    "notes": "End of day reconciliation"
}
```

#### List Daily Sales Records
```
GET /api/manager/daily-records/
```
Returns a list of daily sales records.

#### Approve Daily Sales Record (Manager only)
```
POST /api/manager/daily-records/{record_id}/approve/
```
Approves a daily sales record.

**Request Body:**
```json
{
    "notes": "Daily record approved after verification"
}
```

#### Reject Daily Sales Record (Manager only)
```
POST /api/manager/daily-records/{record_id}/reject/
```
Rejects a daily sales record.

**Request Body:**
```json
{
    "notes": "Daily record rejected due to cash discrepancy"
}
```

#### Record Bank Deposit
```
POST /api/cash/bank-deposits/
```
Records a bank deposit.

**Request Body:**
```json
{
    "shop_id": "550e8400-e29b-41d4-a716-446655442222",
    "amount": "2500.00",
    "deposit_date": "2023-05-15",
    "reference_number": "DEP12345",
    "notes": "Deposit for yesterday's sales"
}
```

#### Get Shop Cash Balance
```
GET /api/cash/balance/{shop_id}/
```
Returns the current cash balance for a shop.

### Reports Module

#### Generate Report
```
POST /api/reports/generate/
```
Generates a new report.

**Request Body:**
```json
{
    "title": "Weekly Sales Report",
    "description": "Sales report for the past week",
    "report_type": "sales",
    "format": "pdf",
    "parameters": {
        "shop_id": "550e8400-e29b-41d4-a716-446655442222",
        "start_date": "2023-05-01",
        "end_date": "2023-05-07",
        "include_item_details": true
    }
}
```

#### List Reports
```
GET /api/reports/
```
Returns a list of generated reports.

#### Get Report Details
```
GET /api/reports/{report_id}/
```
Returns details of a specific report.

#### Download Report
```
GET /api/reports/{report_id}/download/
```
Downloads a report file.

#### Create Report Schedule
```
POST /api/reports/schedules/
```
Creates a new report schedule.

**Request Body:**
```json
{
    "report_type": "sales",
    "title": "Weekly Sales Report",
    "description": "Automatically generated weekly sales report",
    "frequency": "weekly",
    "parameters": {
        "shop_id": "550e8400-e29b-41d4-a716-446655442222",
        "include_item_details": true,
        "include_payment_breakdown": true
    },
    "format": "pdf",
    "recipients": ["manager@abcliquors.com", "executive@abcliquors.com"],
    "is_active": true
}
```

#### List Report Schedules
```
GET /api/reports/schedules/
```
Returns a list of report schedules.

### Analytics Module

#### Get Sales Analytics
```
GET /api/analytics/sales/
```
Returns sales analytics data.

#### Get Sales Analytics by Shop
```
GET /api/analytics/sales/?shop={shop_id}
```
Returns sales analytics for a specific shop.

#### Get Sales Analytics by Period
```
GET /api/analytics/sales/?period=weekly
```
Returns sales analytics for a specific period (daily, weekly, monthly).

#### Get Inventory Analytics
```
GET /api/analytics/inventory/
```
Returns inventory analytics data.

#### Get Executive Performance
```
GET /api/analytics/executive-performance/
```
Returns performance analytics for executives.

### SaaS Admin Module

#### System Settings
```
GET /api/saas/settings/
```
Returns system-wide settings.

```
PATCH /api/saas/settings/
```
Updates system-wide settings.

**Request Body (partial):**
```json
{
    "site_name": "Liquor Shop Management",
    "support_email": "support@liquorshop.com",
    "enable_notifications": true
}
```

#### Email Templates
```
GET /api/saas/email-templates/
```
Returns a list of email templates.

```
GET /api/saas/email-templates/{template_id}/
```
Returns a specific email template.

```
PATCH /api/saas/email-templates/{template_id}/
```
Updates an email template.

**Request Body (partial):**
```json
{
    "subject": "Welcome to Liquor Shop Management",
    "body": "Dear {{name}},\n\nWelcome to our platform..."
}
```

#### Maintenance Mode
```
POST /api/saas/maintenance/start/
```
Puts the system in maintenance mode.

**Request Body:**
```json
{
    "message": "System maintenance in progress. Please check back in 2 hours.",
    "estimated_duration": 120
}
```

```
POST /api/saas/maintenance/end/
```
Ends maintenance mode.

#### System Health
```
GET /api/saas/health/
```
Returns system health information.

## Common Workflows

### Executive Daily Workflow

1. Executive logs in to the system
2. Executive records daily login with opening cash
3. Executive creates sales throughout the day
4. At end of day, executive logs out with closing cash
5. Manager reviews and approves daily sales record
6. Manager deposits cash to bank and records deposit

### Inventory Management Workflow

1. Add brands to the system
2. Add stock for each brand and shop
3. Update stock quantities as needed
4. Create stock adjustments for damaged/lost items
5. Manager approves or rejects adjustments
6. Transfer stock between shops as needed

### Reporting Workflow

1. Generate reports as needed (sales, inventory, etc.)
2. Set up scheduled reports to run automatically
3. View and download reports
4. Analyze data using the analytics dashboards

## Error Handling

The API returns appropriate HTTP status codes for different error conditions:

- `400 Bad Request`: Invalid input or validation error
- `401 Unauthorized`: Authentication required or invalid token
- `403 Forbidden`: Authenticated user doesn't have permission
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

Error responses include a message explaining the error:

```json
{
    "detail": "Not found."
}
```

For validation errors, the response includes field-specific errors:

```json
{
    "email": ["This field is required."],
    "password": ["This field must be at least 8 characters long."]
}
```

## Pagination

List endpoints support pagination with the following query parameters:

- `page`: Page number (default: 1)
- `page_size`: Number of items per page (default: 10, max: 100)

Paginated response format:

```json
{
    "count": 100,
    "next": "https://api.example.com/api/users/?page=2",
    "previous": null,
    "results": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "email": "user@example.com",
            ...
        },
        ...
    ]
}
```

## Filtering and Sorting

Most list endpoints support filtering and sorting:

### Filtering

Use query parameters to filter results:

```
GET /api/sales/?date=2023-05-15&payment_method=cash
```

Multiple values for the same field use comma separation:

```
GET /api/inventory/stock/?category=whiskey,beer
```

### Sorting

Use the `ordering` query parameter to sort results:

```
GET /api/sales/?ordering=-total_amount
```

Prefix the field name with `-` for descending order.

Multiple fields can be specified:

```
GET /api/sales/?ordering=-date,total_amount
``` 