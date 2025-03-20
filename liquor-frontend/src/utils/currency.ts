import { useAppSelector } from '../store';

/**
 * Format a number as currency
 * @param amount Amount to format
 * @param currencyCode Currency code (e.g., 'INR', 'USD')
 * @param locale Locale for formatting (e.g., 'en-IN', 'en-US')
 * @returns Formatted currency string
 */
export const formatCurrency = (
  amount: number,
  currencyCode: string = 'INR',
  locale: string = 'en-IN'
): string => {
  try {
    return new Intl.NumberFormat(locale, {
      style: 'currency',
      currency: currencyCode,
    }).format(amount);
  } catch (error) {
    console.error('Error formatting currency:', error);
    return `${currencyCode} ${amount.toFixed(2)}`;
  }
};

/**
 * Format a number as currency using user preferences
 * @param amount Amount to format
 * @returns Formatted currency string
 */
export const formatCurrencyFromPreferences = (amount: number): string => {
  try {
    const currencyCode = localStorage.getItem('currency') || 'INR';
    const locale = localStorage.getItem('language') || 'en-IN';
    
    return formatCurrency(amount, currencyCode, locale);
  } catch (error) {
    console.error('Error formatting currency from preferences:', error);
    return `INR ${amount.toFixed(2)}`;
  }
};

/**
 * Custom hook for currency formatting according to user preferences
 * @returns Function to format currency
 */
export const useCurrencyFormat = () => {
  const { currency, language } = useAppSelector((state) => state.userPreferences);
  
  return {
    formatCurrency: (amount: number, customCurrency?: string, customLocale?: string) => {
      try {
        return new Intl.NumberFormat(customLocale || language || 'en-IN', {
          style: 'currency',
          currency: customCurrency || currency || 'INR',
        }).format(amount);
      } catch (error) {
        console.error('Error formatting currency:', error);
        return `${customCurrency || currency || 'INR'} ${amount.toFixed(2)}`;
      }
    },
  };
};

export default {
  formatCurrency,
  formatCurrencyFromPreferences,
  useCurrencyFormat,
};