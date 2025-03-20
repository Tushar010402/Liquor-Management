import React from 'react';
import { RouteObject } from 'react-router-dom';
import ProtectedRoute from '../components/auth/ProtectedRoute';
import AssistantManagerLayout from '../layouts/AssistantManagerLayout';
import Dashboard from '../pages/assistant-manager/Dashboard';
import InventoryManagement from '../pages/assistant-manager/InventoryManagement';
import PendingApprovals from '../pages/assistant-manager/PendingApprovals';
import NotFoundPage from '../pages/NotFoundPage';

const assistantManagerRoutes: RouteObject[] = [
  {
    path: '/assistant-manager',
    element: (
      <ProtectedRoute allowedRoles={['assistant_manager']}>
        <AssistantManagerLayout />
      </ProtectedRoute>
    ),
    children: [
      {
        path: '',
        element: <Dashboard />,
      },
      {
        path: 'dashboard',
        element: <Dashboard />,
      },
      {
        path: 'inventory',
        element: <InventoryManagement />,
      },
      {
        path: 'approvals',
        element: <PendingApprovals />,
      },
      {
        path: '*',
        element: <NotFoundPage />,
      },
    ],
  },
];

export default assistantManagerRoutes;