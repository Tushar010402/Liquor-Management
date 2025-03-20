import React from 'react';
import { Navigate, RouteObject } from 'react-router-dom';
import ExecutiveLayout from '../layouts/ExecutiveLayout';

// Dashboard
import Dashboard from '../pages/executive/Dashboard';

// Sales
import NewSale from '../pages/executive/Sales/NewSale';
import BatchSale from '../pages/executive/Sales/BatchSale';
import MySales from '../pages/executive/Sales/MySales';
import DraftSales from '../pages/executive/Sales/DraftSales';
import BrandSales from '../pages/executive/Sales/BrandSales';

// Stock
import SingleAdjustment from '../pages/executive/Stock/SingleAdjustment';
import BatchAdjustment from '../pages/executive/Stock/BatchAdjustment';
import MyAdjustments from '../pages/executive/Stock/MyAdjustments';
import CreateReturn from '../pages/executive/Stock/CreateReturn';
import MyReturns from '../pages/executive/Stock/MyReturns';

// Cash
import CashBalance from '../pages/executive/Cash/CashBalance';
import RecordDeposit from '../pages/executive/Cash/RecordDeposit';
import RecordExpense from '../pages/executive/Cash/RecordExpense';
import DailySummary from '../pages/executive/Cash/DailySummary';
import CashHistory from '../pages/executive/Cash/CashHistory';
import PaymentBreakdown from '../pages/executive/Cash/PaymentBreakdown';

// Profile & Settings
import Profile from '../pages/profile/Profile';
import Settings from '../pages/settings/Settings';

const executiveRoutes: RouteObject[] = [
  {
    path: '/executive',
    element: <ExecutiveLayout />,
    children: [
      {
        index: true,
        element: <Navigate to="/executive/dashboard" replace />,
      },
      {
        path: 'dashboard',
        element: <Dashboard />,
      },
      // Sales routes
      {
        path: 'new-sale',
        element: <NewSale />,
      },
      {
        path: 'batch-sale',
        element: <BatchSale />,
      },
      {
        path: 'my-sales',
        element: <MySales />,
      },
      {
        path: 'draft-sales',
        element: <DraftSales />,
      },
      {
        path: 'brand-sales',
        element: <BrandSales />,
      },
      // Stock routes
      {
        path: 'single-adjustment',
        element: <SingleAdjustment />,
      },
      {
        path: 'batch-adjustment',
        element: <BatchAdjustment />,
      },
      {
        path: 'my-adjustments',
        element: <MyAdjustments />,
      },
      {
        path: 'create-return',
        element: <CreateReturn />,
      },
      {
        path: 'my-returns',
        element: <MyReturns />,
      },
      // Cash routes
      {
        path: 'cash-balance',
        element: <CashBalance />,
      },
      {
        path: 'record-deposit',
        element: <RecordDeposit />,
      },
      {
        path: 'record-expense',
        element: <RecordExpense />,
      },
      {
        path: 'daily-summary',
        element: <DailySummary />,
      },
      {
        path: 'cash-history',
        element: <CashHistory />,
      },
      {
        path: 'payment-breakdown',
        element: <PaymentBreakdown />,
      },
      // Profile & Settings
      {
        path: 'profile',
        element: <Profile />,
      },
      {
        path: 'settings',
        element: <Settings />,
      },
    ],
  },
];

export default executiveRoutes;