import React from 'react';
import { RouteObject } from 'react-router-dom';
import ProtectedRoute from '../components/auth/ProtectedRoute';
import UserProfile from '../pages/common/UserProfile';
import HelpCenter from '../pages/common/HelpCenter';
import NotificationsCenter from '../pages/common/NotificationsCenter';
import { UserRole } from '../services/api';

// Common routes accessible to all authenticated users
const commonRoutes: RouteObject[] = [
  {
    path: '/profile',
    element: (
      <ProtectedRoute allowedRoles={['saas_admin', 'tenant_admin', 'shop_manager', 'assistant_manager', 'executive'] as UserRole[]}>
        <UserProfile />
      </ProtectedRoute>
    ),
  },
  {
    path: '/help',
    element: (
      <ProtectedRoute allowedRoles={['saas_admin', 'tenant_admin', 'shop_manager', 'assistant_manager', 'executive'] as UserRole[]}>
        <HelpCenter />
      </ProtectedRoute>
    ),
  },
  {
    path: '/notifications',
    element: (
      <ProtectedRoute allowedRoles={['saas_admin', 'tenant_admin', 'shop_manager', 'assistant_manager', 'executive'] as UserRole[]}>
        <NotificationsCenter />
      </ProtectedRoute>
    ),
  },
];

export default commonRoutes;