import { useCallback } from 'react';
import { useAppDispatch, useAppSelector } from '../store';
import {
  startLoading,
  stopLoading,
  startProcess,
  stopProcess,
  resetLoading,
} from '../store/slices/loadingSlice';

interface UseLoadingReturn {
  isLoading: boolean;
  loadingText: string;
  showLoading: (text?: string) => void;
  hideLoading: () => void;
  startProcess: (processId: string) => void;
  stopProcess: (processId: string) => void;
  isProcessRunning: (processId: string) => boolean;
  resetLoading: () => void;
}

/**
 * Custom hook for managing loading state
 * @returns Object with loading state and methods
 */
const useLoading = (): UseLoadingReturn => {
  const dispatch = useAppDispatch();
  const { isLoading, loadingText, processes } = useAppSelector((state) => state.loading);

  const showLoadingFn = useCallback(
    (text?: string) => {
      dispatch(startLoading(text));
    },
    [dispatch]
  );

  const hideLoadingFn = useCallback(() => {
    dispatch(stopLoading());
  }, [dispatch]);

  const startProcessFn = useCallback(
    (processId: string) => {
      dispatch(startProcess(processId));
    },
    [dispatch]
  );

  const stopProcessFn = useCallback(
    (processId: string) => {
      dispatch(stopProcess(processId));
    },
    [dispatch]
  );

  const isProcessRunning = useCallback(
    (processId: string) => {
      return !!processes[processId];
    },
    [processes]
  );

  const resetLoadingFn = useCallback(() => {
    dispatch(resetLoading());
  }, [dispatch]);

  return {
    isLoading,
    loadingText,
    showLoading: showLoadingFn,
    hideLoading: hideLoadingFn,
    startProcess: startProcessFn,
    stopProcess: stopProcessFn,
    isProcessRunning,
    resetLoading: resetLoadingFn,
  };
};

export default useLoading;