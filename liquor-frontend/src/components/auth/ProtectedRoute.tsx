import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { CircularProgress, Box } from '@mui/material';
import useAuth from '../../hooks/useAuth';
import { UserRole } from '../../contexts/AuthContext';

interface ProtectedRouteProps {
  allowedRoles?: UserRole[];
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ allowedRoles }) => {
  const { isAuthenticated, isLoading, user } = useAuth();

  // Show loading spinner while checking authentication
  if (isLoading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
      >
        <CircularProgress />
      </Box>
    );
  }

  // Redirect to login if not authenticated
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // Check if user has the required role
  if (allowedRoles && user && !allowedRoles.includes(user.role)) {
    // Redirect to appropriate dashboard based on user role
    switch (user.role) {
      case 'saas_admin':
        return <Navigate to="/saas-admin/dashboard" replace />;
      case 'tenant_admin':
        return <Navigate to="/tenant-admin/dashboard" replace />;
      case 'manager':
        return <Navigate to="/manager/dashboard" replace />;
      case 'assistant_manager':
        return <Navigate to="/assistant-manager/dashboard" replace />;
      case 'executive':
        return <Navigate to="/executive/dashboard" replace />;
      default:
        return <Navigate to="/dashboard" replace />;
    }
  }

  // Render the protected component
  return <Outlet />;
};

export default ProtectedRoute;