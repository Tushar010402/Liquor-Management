import { useState, useCallback } from 'react';

interface ConfirmDialogState {
  open: boolean;
  title: string;
  message: string;
  confirmText: string;
  cancelText: string;
  confirmButtonColor?: 'primary' | 'secondary' | 'error' | 'info' | 'success' | 'warning';
  onConfirm: () => void;
  onCancel?: () => void;
}

const initialState: ConfirmDialogState = {
  open: false,
  title: 'Confirm',
  message: 'Are you sure?',
  confirmText: 'Confirm',
  cancelText: 'Cancel',
  confirmButtonColor: 'primary',
  onConfirm: () => {},
};

/**
 * Custom hook for handling confirmation dialogs
 * @returns Confirm dialog state and handlers
 */
function useConfirmDialog() {
  const [dialogState, setDialogState] = useState<ConfirmDialogState>(initialState);

  const openConfirmDialog = useCallback(
    (options: Partial<ConfirmDialogState> & { onConfirm: () => void }) => {
      setDialogState({
        ...initialState,
        ...options,
        open: true,
      });
    },
    []
  );

  const closeConfirmDialog = useCallback(() => {
    setDialogState((prev) => ({
      ...prev,
      open: false,
    }));
  }, []);

  const handleConfirm = useCallback(() => {
    dialogState.onConfirm();
    closeConfirmDialog();
  }, [dialogState, closeConfirmDialog]);

  const handleCancel = useCallback(() => {
    if (dialogState.onCancel) {
      dialogState.onCancel();
    }
    closeConfirmDialog();
  }, [dialogState, closeConfirmDialog]);

  return {
    confirmDialogState: dialogState,
    openConfirmDialog,
    closeConfirmDialog,
    handleConfirm,
    handleCancel,
  };
}

export default useConfirmDialog;