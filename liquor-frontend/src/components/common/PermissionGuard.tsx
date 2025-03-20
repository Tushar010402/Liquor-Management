import React from 'react';
import usePermissions from '../../hooks/usePermissions';

interface PermissionGuardProps {
  permission?: string;
  permissions?: string[];
  requireAll?: boolean;
  fallback?: React.ReactNode;
  children: React.ReactNode;
}

/**
 * Component that conditionally renders children based on user permissions
 */
const PermissionGuard: React.FC<PermissionGuardProps> = ({
  permission,
  permissions = [],
  requireAll = false,
  fallback = null,
  children,
}) => {
  const { hasPermission, hasAnyPermission, hasAllPermissions } = usePermissions();

  // Check if user has the required permissions
  const hasRequiredPermissions = (): boolean => {
    if (permission) {
      return hasPermission(permission);
    }

    if (permissions.length > 0) {
      return requireAll ? hasAllPermissions(permissions) : hasAnyPermission(permissions);
    }

    return true;
  };

  return <>{hasRequiredPermissions() ? children : fallback}</>;
};

export default PermissionGuard;