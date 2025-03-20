import { useCallback } from 'react';
import { useAppDispatch } from '../store';
import { addNotification, NotificationType } from '../store/slices/notificationSlice';

interface UseNotificationReturn {
  showNotification: (message: string, type: NotificationType, duration?: number) => void;
  showSuccess: (message: string, duration?: number) => void;
  showError: (message: string, duration?: number) => void;
  showInfo: (message: string, duration?: number) => void;
  showWarning: (message: string, duration?: number) => void;
}

/**
 * Custom hook for showing notifications
 * @returns Object with notification methods
 */
const useNotification = (): UseNotificationReturn => {
  const dispatch = useAppDispatch();

  const showNotification = useCallback(
    (message: string, type: NotificationType, duration?: number) => {
      dispatch(
        addNotification({
          message,
          type,
          autoHideDuration: duration,
        })
      );
    },
    [dispatch]
  );

  const showSuccess = useCallback(
    (message: string, duration?: number) => {
      showNotification(message, 'success', duration);
    },
    [showNotification]
  );

  const showError = useCallback(
    (message: string, duration?: number) => {
      showNotification(message, 'error', duration);
    },
    [showNotification]
  );

  const showInfo = useCallback(
    (message: string, duration?: number) => {
      showNotification(message, 'info', duration);
    },
    [showNotification]
  );

  const showWarning = useCallback(
    (message: string, duration?: number) => {
      showNotification(message, 'warning', duration);
    },
    [showNotification]
  );

  return {
    showNotification,
    showSuccess,
    showError,
    showInfo,
    showWarning,
  };
};

export default useNotification;