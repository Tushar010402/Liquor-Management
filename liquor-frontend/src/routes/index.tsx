import React from 'react';
import { Navigate, RouteObject } from 'react-router-dom';
import LoginPage from '../pages/auth/LoginPage';
import ForgotPasswordPage from '../pages/auth/ForgotPasswordPage';
import ResetPasswordPage from '../pages/auth/ResetPasswordPage';
import ProtectedRoute from '../components/auth/ProtectedRoute';
import executiveRoutes from './executiveRoutes';

// Import other role routes as they are implemented
// import saasAdminRoutes from './saasAdminRoutes';
// import tenantAdminRoutes from './tenantAdminRoutes';
// import managerRoutes from './managerRoutes';
// import assistantManagerRoutes from './assistantManagerRoutes';

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
  
  // Add other role routes as they are implemented
  // ...saasAdminRoutes,
  // ...tenantAdminRoutes,
  // ...managerRoutes,
  // ...assistantManagerRoutes,
  
  // Catch-all route for 404
  {
    path: '*',
    element: <Navigate to="/login" replace />,
  },
];

export default routes;