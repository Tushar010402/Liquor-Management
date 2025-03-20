import React from 'react';
import usePermissions from '../../hooks/usePermissions';

interface ShopGuardProps {
  shopId: string;
  fallback?: React.ReactNode;
  children: React.ReactNode;
}

/**
 * Component that conditionally renders children based on shop assignment
 */
const ShopGuard: React.FC<ShopGuardProps> = ({ shopId, fallback = null, children }) => {
  const { isAssignedToShop } = usePermissions();

  return <>{isAssignedToShop(shopId) ? children : fallback}</>;
};

export default ShopGuard;