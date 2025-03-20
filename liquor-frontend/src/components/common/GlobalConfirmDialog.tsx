import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import ConfirmDialog from './ConfirmDialog';

interface ConfirmDialogOptions {
  title?: string;
  message: string;
  confirmText?: string;
  cancelText?: string;
  confirmButtonColor?: 'primary' | 'secondary' | 'error' | 'info' | 'success' | 'warning';
}

interface ConfirmDialogContextType {
  confirm: (options: ConfirmDialogOptions) => Promise<boolean>;
}

const ConfirmDialogContext = createContext<ConfirmDialogContextType | undefined>(undefined);

export const useGlobalConfirmDialog = (): ConfirmDialogContextType => {
  const context = useContext(ConfirmDialogContext);
  if (!context) {
    throw new Error('useGlobalConfirmDialog must be used within a GlobalConfirmDialogProvider');
  }
  return context;
};

interface GlobalConfirmDialogProviderProps {
  children: ReactNode;
}

export const GlobalConfirmDialogProvider: React.FC<GlobalConfirmDialogProviderProps> = ({ children }) => {
  const [dialogOpen, setDialogOpen] = useState(false);
  const [dialogConfig, setDialogConfig] = useState<ConfirmDialogOptions>({
    title: 'Confirm',
    message: 'Are you sure?',
    confirmText: 'Confirm',
    cancelText: 'Cancel',
    confirmButtonColor: 'primary',
  });
  const [resolveRef, setResolveRef] = useState<((value: boolean) => void) | null>(null);

  const confirm = useCallback(
    (options: ConfirmDialogOptions): Promise<boolean> => {
      return new Promise<boolean>((resolve) => {
        setDialogConfig({
          title: options.title || 'Confirm',
          message: options.message,
          confirmText: options.confirmText || 'Confirm',
          cancelText: options.cancelText || 'Cancel',
          confirmButtonColor: options.confirmButtonColor || 'primary',
        });
        setDialogOpen(true);
        setResolveRef(() => resolve);
      });
    },
    []
  );

  const handleConfirm = useCallback(() => {
    setDialogOpen(false);
    if (resolveRef) {
      resolveRef(true);
      setResolveRef(null);
    }
  }, [resolveRef]);

  const handleCancel = useCallback(() => {
    setDialogOpen(false);
    if (resolveRef) {
      resolveRef(false);
      setResolveRef(null);
    }
  }, [resolveRef]);

  return (
    <ConfirmDialogContext.Provider value={{ confirm }}>
      {children}
      <ConfirmDialog
        open={dialogOpen}
        title={dialogConfig.title || 'Confirm'}
        message={dialogConfig.message}
        confirmText={dialogConfig.confirmText || 'Confirm'}
        cancelText={dialogConfig.cancelText || 'Cancel'}
        confirmButtonColor={dialogConfig.confirmButtonColor}
        onConfirm={handleConfirm}
        onCancel={handleCancel}
      />
    </ConfirmDialogContext.Provider>
  );
};

export default GlobalConfirmDialogProvider;