import { useCallback } from 'react';
import useAuth from './useAuth';

/**
 * Custom hook for checking user permissions
 * @returns Permission checking functions
 */
function usePermissions() {
  const { user } = useAuth();

  /**
   * Check if user has a specific permission
   * @param permission Permission to check
   * @returns True if user has permission
   */
  const hasPermission = useCallback(
    (permission: string): boolean => {
      if (!user) return false;

      // SaaS admin has all permissions
      if (user.role === 'saas_admin' && user.permissions?.includes('all')) {
        return true;
      }

      // Tenant admin has all tenant permissions
      if (user.role === 'tenant_admin' && user.permissions?.includes('tenant_all')) {
        return permission.startsWith('tenant_') || permission.startsWith('shop_');
      }

      // Check specific permission
      return user.permissions?.includes(permission) || false;
    },
    [user]
  );

  /**
   * Check if user has any of the specified permissions
   * @param permissions Permissions to check
   * @returns True if user has any of the permissions
   */
  const hasAnyPermission = useCallback(
    (permissions: string[]): boolean => {
      return permissions.some((permission) => hasPermission(permission));
    },
    [hasPermission]
  );

  /**
   * Check if user has all of the specified permissions
   * @param permissions Permissions to check
   * @returns True if user has all of the permissions
   */
  const hasAllPermissions = useCallback(
    (permissions: string[]): boolean => {
      return permissions.every((permission) => hasPermission(permission));
    },
    [hasPermission]
  );

  /**
   * Check if user is assigned to a specific shop
   * @param shopId Shop ID to check
   * @returns True if user is assigned to the shop
   */
  const isAssignedToShop = useCallback(
    (shopId: string): boolean => {
      if (!user) return false;

      // SaaS admin and tenant admin have access to all shops
      if (
        (user.role === 'saas_admin' && user.permissions?.includes('all')) ||
        (user.role === 'tenant_admin' && user.permissions?.includes('tenant_all'))
      ) {
        return true;
      }

      // Check if user is assigned to the shop
      return user.assigned_shops?.some((shop) => shop.id === shopId) || false;
    },
    [user]
  );

  return {
    hasPermission,
    hasAnyPermission,
    hasAllPermissions,
    isAssignedToShop,
  };
}

export default usePermissions;