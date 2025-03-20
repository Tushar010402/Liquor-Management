import React from 'react';
import { RouteObject } from 'react-router-dom';
import ProtectedRoute from '../components/auth/ProtectedRoute';
import TenantAdminLayout from '../layouts/TenantAdminLayout';
import Dashboard from '../pages/tenant-admin/Dashboard';
import ShopsManagement from '../pages/tenant-admin/ShopsManagement';
import StaffManagement from '../pages/tenant-admin/StaffManagement';
import NotFoundPage from '../pages/NotFoundPage';

const tenantAdminRoutes: RouteObject[] = [
  {
    path: '/tenant-admin',
    element: (
      <ProtectedRoute allowedRoles={['tenant_admin']}>
        <TenantAdminLayout />
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
        path: 'shops',
        element: <ShopsManagement />,
      },
      {
        path: 'staff',
        element: <StaffManagement />,
      },
      {
        path: '*',
        element: <NotFoundPage />,
      },
    ],
  },
];

export default tenantAdminRoutes;