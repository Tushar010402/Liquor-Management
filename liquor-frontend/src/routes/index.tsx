import React from 'react';
import { Navigate, RouteObject } from 'react-router-dom';
import LoginPage from '../pages/auth/LoginPage';
import ForgotPasswordPage from '../pages/auth/ForgotPasswordPage';
import ResetPasswordPage from '../pages/auth/ResetPasswordPage';
import ProtectedRoute from '../components/auth/ProtectedRoute';
import executiveRoutes from './executiveRoutes';
import saasAdminRoutes from './saasAdminRoutes';
import tenantAdminRoutes from './tenantAdminRoutes';
import shopManagerRoutes from './shopManagerRoutes';
import assistantManagerRoutes from './assistantManagerRoutes';

const routes: RouteObject[] = [
  {
    path: '/',
    element: <Navigate to="/login" replace />,
  },
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    path: '/forgot-password',
    element: <ForgotPasswordPage />,
  },
  {
    path: '/reset-password/:token',
    element: <ResetPasswordPage />,
  },
  
  // Protected routes for different roles
  // Executive routes
  ...executiveRoutes,
  
  // SaaS Admin routes
  ...saasAdminRoutes,
  
  // Tenant Admin routes
  ...tenantAdminRoutes,
  
  // Shop Manager routes
  ...shopManagerRoutes,
  
  // Assistant Manager routes
  ...assistantManagerRoutes,
  
  // Catch-all route for 404
  {
    path: '*',
    element: <Navigate to="/login" replace />,
  },
];

export default routes;