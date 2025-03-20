/**
 * Error tracking utility
 * 
 * This utility can be used to track errors throughout the application.
 * In a production environment, you would integrate with an error tracking service
 * like Sentry, LogRocket, etc.
 */

interface ErrorDetails {
  message: string;
  stack?: string;
  componentName?: string;
  additionalData?: Record<string, any>;
}

/**
 * Track an error
 * @param error Error object or message
 * @param componentName Optional component name where the error occurred
 * @param additionalData Optional additional data to include with the error
 */
export const trackError = (
  error: Error | string,
  componentName?: string,
  additionalData?: Record<string, any>
): void => {
  const errorDetails: ErrorDetails = {
    message: typeof error === 'string' ? error : error.message,
    stack: typeof error === 'string' ? undefined : error.stack,
    componentName,
    additionalData,
  };

  // In development, log to console
  if (process.env.NODE_ENV === 'development') {
    console.error('Error tracked:', errorDetails);
  }

  // In production, you would send to an error tracking service
  // For example, with Sentry:
  // if (process.env.NODE_ENV === 'production') {
  //   Sentry.captureException(error, {
  //     tags: { component: componentName },
  //     extra: additionalData,
  //   });
  // }
};

/**
 * Track a warning
 * @param message Warning message
 * @param componentName Optional component name where the warning occurred
 * @param additionalData Optional additional data to include with the warning
 */
export const trackWarning = (
  message: string,
  componentName?: string,
  additionalData?: Record<string, any>
): void => {
  const warningDetails = {
    message,
    componentName,
    additionalData,
  };

  // In development, log to console
  if (process.env.NODE_ENV === 'development') {
    console.warn('Warning tracked:', warningDetails);
  }

  // In production, you would send to an error tracking service
  // For example, with Sentry:
  // if (process.env.NODE_ENV === 'production') {
  //   Sentry.captureMessage(message, {
  //     level: 'warning',
  //     tags: { component: componentName },
  //     extra: additionalData,
  //   });
  // }
};

/**
 * Create an error handler function for async operations
 * @param componentName Component name for tracking
 * @returns Error handler function
 */
export const createErrorHandler = (componentName: string) => {
  return (error: any, additionalData?: Record<string, any>) => {
    trackError(error, componentName, additionalData);
    return error;
  };
};

export default {
  trackError,
  trackWarning,
  createErrorHandler,
};