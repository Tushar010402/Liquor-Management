import { useFormik, FormikConfig, FormikValues, FormikHelpers } from 'formik';
import * as Yup from 'yup';
import { useState } from 'react';
import useNotification from './useNotification';

interface UseFormValidationOptions<Values> {
  initialValues: Values;
  validationSchema: Yup.Schema<any>;
  onSubmit: (values: Values, formikHelpers: FormikHelpers<Values>) => void | Promise<any>;
  showSuccessNotification?: boolean;
  successMessage?: string;
  showErrorNotification?: boolean;
}

/**
 * Custom hook for form validation using Formik and Yup
 * @param options Form validation options
 * @returns Formik instance and additional state
 */
function useFormValidation<Values extends FormikValues>({
  initialValues,
  validationSchema,
  onSubmit,
  showSuccessNotification = true,
  successMessage = 'Operation completed successfully',
  showErrorNotification = true,
}: UseFormValidationOptions<Values>) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);
  const [formSuccess, setFormSuccess] = useState(false);
  const { showSuccess, showError } = useNotification();

  const handleSubmit = async (values: Values, formikHelpers: FormikHelpers<Values>) => {
    setIsSubmitting(true);
    setFormError(null);
    setFormSuccess(false);

    try {
      await onSubmit(values, formikHelpers);
      setFormSuccess(true);
      if (showSuccessNotification) {
        showSuccess(successMessage);
      }
    } catch (err: any) {
      const errorMessage = err.response?.data?.message || err.message || 'An error occurred';
      setFormError(errorMessage);
      if (showErrorNotification) {
        showError(errorMessage);
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const formik = useFormik<Values>({
    initialValues,
    validationSchema,
    onSubmit: handleSubmit,
    validateOnChange: true,
    validateOnBlur: true,
  });

  return {
    formik,
    isSubmitting,
    formError,
    formSuccess,
    setFormError,
    setFormSuccess,
  };
}

export default useFormValidation;