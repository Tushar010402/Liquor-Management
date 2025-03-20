import React, { createContext, useState, useCallback, ReactNode } from 'react';
import { Snackbar, Alert, AlertColor } from '@mui/material';

// Define notification interface
export interface Notification {
  message: string;
  variant: AlertColor;
  duration?: number;
}

// Define notification context interface
interface NotificationContextType {
  showNotification: (notification: Notification) => void;
  hideNotification: () => void;
}

// Create the notification context
export const NotificationContext = createContext<NotificationContextType>({
  showNotification: () => {},
  hideNotification: () => {},
});

interface NotificationProviderProps {
  children: ReactNode;
}

/**
 * NotificationProvider component that provides notification context to the application
 */
export const NotificationProvider: React.FC<NotificationProviderProps> = ({ children }) => {
  const [open, setOpen] = useState<boolean>(false);
  const [message, setMessage] = useState<string>('');
  const [variant, setVariant] = useState<AlertColor>('info');
  const [duration, setDuration] = useState<number>(6000);

  /**
   * Show a notification
   * @param notification - Notification object
   */
  const showNotification = useCallback((notification: Notification) => {
    setMessage(notification.message);
    setVariant(notification.variant);
    setDuration(notification.duration || 6000);
    setOpen(true);
  }, []);

  /**
   * Hide the notification
   */
  const hideNotification = useCallback(() => {
    setOpen(false);
  }, []);

  /**
   * Handle notification close
   */
  const handleClose = useCallback((event?: React.SyntheticEvent | Event, reason?: string) => {
    if (reason === 'clickaway') {
      return;
    }
    setOpen(false);
  }, []);

  return (
    <NotificationContext.Provider
      value={{
        showNotification,
        hideNotification,
      }}
    >
      {children}
      <Snackbar
        open={open}
        autoHideDuration={duration}
        onClose={handleClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert onClose={handleClose} severity={variant} sx={{ width: '100%' }}>
          {message}
        </Alert>
      </Snackbar>
    </NotificationContext.Provider>
  );
};

export default NotificationProvider;