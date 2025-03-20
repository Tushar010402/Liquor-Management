import React from 'react';
import { ShopGuard } from '../components/common';

interface WithShopGuardOptions {
  shopId: string;
  fallback?: React.ReactNode;
}

/**
 * Higher-order component that wraps a component with shop assignment checks
 * @param Component Component to wrap
 * @param options Shop guard options
 * @returns Wrapped component
 */
function withShopGuard<P extends object>(
  Component: React.ComponentType<P>,
  options: WithShopGuardOptions
): React.FC<P> {
  const { shopId, fallback } = options;

  const WithShopGuard: React.FC<P> = (props) => {
    return (
      <ShopGuard shopId={shopId} fallback={fallback}>
        <Component {...props} />
      </ShopGuard>
    );
  };

  // Set display name for debugging
  const displayName = Component.displayName || Component.name || 'Component';
  WithShopGuard.displayName = `withShopGuard(${displayName})`;

  return WithShopGuard;
}

export default withShopGuard;