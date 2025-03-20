import React from 'react';
import { PermissionGuard } from '../components/common';

interface WithPermissionOptions {
  permission?: string;
  permissions?: string[];
  requireAll?: boolean;
  fallback?: React.ReactNode;
}

/**
 * Higher-order component that wraps a component with permission checks
 * @param Component Component to wrap
 * @param options Permission options
 * @returns Wrapped component
 */
function withPermission<P extends object>(
  Component: React.ComponentType<P>,
  options: WithPermissionOptions
): React.FC<P> {
  const { permission, permissions, requireAll, fallback } = options;

  const WithPermission: React.FC<P> = (props) => {
    return (
      <PermissionGuard
        permission={permission}
        permissions={permissions}
        requireAll={requireAll}
        fallback={fallback}
      >
        <Component {...props} />
      </PermissionGuard>
    );
  };

  // Set display name for debugging
  const displayName = Component.displayName || Component.name || 'Component';
  WithPermission.displayName = `withPermission(${displayName})`;

  return WithPermission;
}

export default withPermission;