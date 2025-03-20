import { useState, useEffect, useCallback } from 'react';
import useNotification from './useNotification';

interface UseDataFetchingOptions<T> {
  fetchFunction: () => Promise<T>;
  dependencies?: any[];
  initialData?: T;
  showErrorNotification?: boolean;
  loadingMessage?: string;
  skipInitialFetch?: boolean;
}

/**
 * Custom hook for data fetching with error handling and loading state
 * @param options Data fetching options
 * @returns Data, loading state, error, and refetch function
 */
function useDataFetching<T>({
  fetchFunction,
  dependencies = [],
  initialData,
  showErrorNotification = true,
  loadingMessage,
  skipInitialFetch = false,
}: UseDataFetchingOptions<T>) {
  const [data, setData] = useState<T | undefined>(initialData);
  const [isLoading, setIsLoading] = useState(!skipInitialFetch);
  const [error, setError] = useState<string | null>(null);
  const { showError } = useNotification();

  const fetchData = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const result = await fetchFunction();
      setData(result);
      return result;
    } catch (err: any) {
      const errorMessage = err.response?.data?.message || err.message || 'Failed to fetch data';
      setError(errorMessage);
      if (showErrorNotification) {
        showError(errorMessage);
      }
      return undefined;
    } finally {
      setIsLoading(false);
    }
  }, [fetchFunction, showError, showErrorNotification]);

  useEffect(() => {
    if (!skipInitialFetch) {
      fetchData();
    }
  }, [...dependencies, fetchData]);

  return {
    data,
    isLoading,
    error,
    refetch: fetchData,
    setData,
  };
}

export default useDataFetching;