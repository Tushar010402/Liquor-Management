import { useState, useCallback } from 'react';
import useNotification from './useNotification';

interface UseFormSubmitOptions<T, R> {
  submitFunction: (data: T) => Promise<R>;
  onSuccess?: (result: R) => void;
  onError?: (error: any) => void;
  successMessage?: string;
  errorMessage?: string;
  showSuccessNotification?: boolean;
  showErrorNotification?: boolean;
}

/**
 * Custom hook for handling form submissions with optimistic updates
 * @param options Form submit options
 * @returns Submit function and state
 */
function useFormSubmit<T, R>({
  submitFunction,
  onSuccess,
  onError,
  successMessage = 'Operation completed successfully',
  errorMessage = 'An error occurred',
  showSuccessNotification = true,
  showErrorNotification = true,
}: UseFormSubmitOptions<T, R>) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<R | null>(null);
  const { showSuccess, showError } = useNotification();

  const submit = useCallback(
    async (data: T) => {
      setIsSubmitting(true);
      setError(null);

      try {
        const response = await submitFunction(data);
        setResult(response);
        
        if (showSuccessNotification) {
          showSuccess(successMessage);
        }
        
        if (onSuccess) {
          onSuccess(response);
        }
        
        return response;
      } catch (err: any) {
        const errorMsg = err.response?.data?.message || err.message || errorMessage;
        setError(errorMsg);
        
        if (showErrorNotification) {
          showError(errorMsg);
        }
        
        if (onError) {
          onError(err);
        }
        
        throw err;
      } finally {
        setIsSubmitting(false);
      }
    },
    [
      submitFunction,
      onSuccess,
      onError,
      successMessage,
      errorMessage,
      showSuccessNotification,
      showErrorNotification,
      showSuccess,
      showError,
    ]
  );

  return {
    submit,
    isSubmitting,
    error,
    result,
    setError,
    setResult,
  };
}

export default useFormSubmit;