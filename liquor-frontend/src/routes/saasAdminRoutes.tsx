import React from 'react';
import { RouteObject } from 'react-router-dom';
import ProtectedRoute from '../components/auth/ProtectedRoute';
import SaasAdminLayout from '../layouts/SaasAdminLayout';
import Dashboard from '../pages/saas-admin/Dashboard';
import TenantsManagement from '../pages/saas-admin/TenantsManagement';
import UsersManagement from '../pages/saas-admin/UsersManagement';
import SystemSettings from '../pages/saas-admin/SystemSettings';
import NotFoundPage from '../pages/NotFoundPage';

const saasAdminRoutes: RouteObject[] = [
  {
    path: '/saas-admin',
    element: (
      <ProtectedRoute allowedRoles={['saas_admin']}>
        <SaasAdminLayout />
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
        path: 'tenants',
        element: <TenantsManagement />,
      },
      {
        path: 'users',
        element: <UsersManagement />,
      },
      {
        path: 'settings',
        element: <SystemSettings />,
      },
      {
        path: '*',
        element: <NotFoundPage />,
      },
    ],
  },
];

export default saasAdminRoutes;