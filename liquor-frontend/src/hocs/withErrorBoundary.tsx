import React from 'react';
import ErrorBoundary from '../components/common/ErrorBoundary';

interface WithErrorBoundaryOptions {
  fallback?: React.ReactNode;
  onReset?: () => void;
}

/**
 * Higher-order component that wraps a component with an error boundary
 * @param Component Component to wrap
 * @param options Error boundary options
 * @returns Wrapped component
 */
function withErrorBoundary<P extends object>(
  Component: React.ComponentType<P>,
  options: WithErrorBoundaryOptions = {}
): React.FC<P> {
  const { fallback, onReset } = options;

  const WithErrorBoundary: React.FC<P> = (props) => {
    return (
      <ErrorBoundary fallback={fallback} onReset={onReset}>
        <Component {...props} />
      </ErrorBoundary>
    );
  };

  // Set display name for debugging
  const displayName = Component.displayName || Component.name || 'Component';
  WithErrorBoundary.displayName = `withErrorBoundary(${displayName})`;

  return WithErrorBoundary;
}

export default withErrorBoundary;