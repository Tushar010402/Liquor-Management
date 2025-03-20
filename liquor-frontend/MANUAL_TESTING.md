# Manual Testing Guide for Liquor Shop Management System

This document provides a comprehensive guide for manually testing the Liquor Shop Management System frontend application.

## Prerequisites

- The application should be running locally (npm start) or deployed to a test environment
- Modern web browser (Chrome, Firefox, Safari, or Edge)
- Mobile device or browser developer tools for mobile testing

## Test Environments

Test the application in the following environments:

1. Desktop browsers (Chrome, Firefox, Safari, Edge)
2. Mobile browsers (iOS Safari, Android Chrome)
3. Different screen sizes (use browser developer tools to simulate various devices)

## Test Accounts

Use the following test accounts to access different roles:

- SaaS Admin: saas@example.com / password
- Tenant Admin: tenant@example.com / password
- Manager: manager@example.com / password
- Assistant Manager: assistant@example.com / password
- Executive: executive@example.com / password

## Test Cases

### 1. Authentication

#### 1.1 Login

- [ ] Verify that the login page loads correctly
- [ ] Test login with valid credentials for each role
- [ ] Test login with invalid credentials (should show error message)
- [ ] Test login with empty fields (should show validation errors)
- [ ] Verify that the "Remember me" checkbox works as expected
- [ ] Test the "Forgot password" link

#### 1.2 Logout

- [ ] Verify that the logout button is accessible from all pages
- [ ] Test logout functionality (should redirect to login page)
- [ ] Verify that after logout, protected routes are not accessible

### 2. Navigation and Layout

- [ ] Verify that the header displays correctly with user information
- [ ] Test the sidebar navigation menu for each role
- [ ] Verify that the sidebar can be collapsed and expanded
- [ ] Test that the active menu item is highlighted
- [ ] Verify that the navigation works correctly on mobile devices
- [ ] Test that the responsive layout adjusts properly for different screen sizes

### 3. Executive Role Features

#### 3.1 Dashboard

- [ ] Verify that the dashboard loads correctly with all widgets
- [ ] Test that the charts and graphs display data correctly
- [ ] Verify that the summary cards show the correct information
- [ ] Test the date range selector (if applicable)

#### 3.2 Sales Management

- [ ] Test creating a new sale
- [ ] Verify that products can be added to the sale
- [ ] Test applying discounts
- [ ] Verify that the total amount is calculated correctly
- [ ] Test different payment methods
- [ ] Verify that the sale is recorded correctly
- [ ] Test viewing sales history
- [ ] Verify that sales can be filtered and sorted

#### 3.3 Cash Management

- [ ] Test viewing the cash balance
- [ ] Verify that the cash flow chart displays correctly
- [ ] Test recording a deposit
  - [ ] Fill in all required fields
  - [ ] Upload a receipt image
  - [ ] Submit the form
  - [ ] Verify that the deposit is recorded
- [ ] Test recording an expense
  - [ ] Fill in all required fields
  - [ ] Select different expense categories
  - [ ] Upload a receipt image
  - [ ] Submit the form
  - [ ] Verify that the expense is recorded
- [ ] Test viewing the daily summary
  - [ ] Verify that all sections display correctly
  - [ ] Test changing the date
  - [ ] Test the print functionality

#### 3.4 Stock Management

- [ ] Test viewing stock levels
- [ ] Verify that stock items can be filtered and sorted
- [ ] Test recording a stock adjustment
- [ ] Verify that the adjustment is reflected in the stock levels

### 4. Manager Role Features

- [ ] Test approval workflows
- [ ] Verify that pending items are displayed correctly
- [ ] Test approving and rejecting items
- [ ] Test creating purchase orders
- [ ] Verify that analytics and reports display correctly

### 5. Assistant Manager Role Features

- [ ] Test inventory management features
- [ ] Verify that stock transfers can be created
- [ ] Test receiving inventory
- [ ] Verify that reports are accessible

### 6. Tenant Admin Role Features

- [ ] Test shop management features
- [ ] Verify that team members can be added and managed
- [ ] Test brand and supplier management
- [ ] Verify that financial reports are accessible

### 7. SaaS Admin Role Features

- [ ] Test tenant management features
- [ ] Verify that new tenants can be added
- [ ] Test system configuration settings
- [ ] Verify that platform analytics are displayed correctly

### 8. Cross-Cutting Concerns

#### 8.1 Error Handling

- [ ] Test behavior when the server is unavailable
- [ ] Verify that appropriate error messages are displayed
- [ ] Test form validation error messages
- [ ] Verify that the application recovers gracefully from errors

#### 8.2 Performance

- [ ] Verify that pages load quickly
- [ ] Test the application with a large dataset
- [ ] Verify that charts and tables render efficiently

#### 8.3 Accessibility

- [ ] Test keyboard navigation
- [ ] Verify that screen readers can interpret the content
- [ ] Test color contrast for readability
- [ ] Verify that form elements have appropriate labels

## Reporting Issues

When reporting issues, please include:

1. Test environment (browser, device, screen size)
2. Steps to reproduce the issue
3. Expected behavior
4. Actual behavior
5. Screenshots or videos (if applicable)

## Test Completion Checklist

- [ ] All test cases have been executed
- [ ] All critical issues have been resolved
- [ ] The application works correctly in all supported browsers
- [ ] The application is responsive on mobile devices
- [ ] All features are accessible and usable