import { format, parseISO, isValid } from 'date-fns';
import { useAppSelector } from '../store';

/**
 * Format a date string according to the user's preferences
 * @param dateString Date string to format
 * @param formatString Optional format string (overrides user preference)
 * @returns Formatted date string
 */
export const formatDate = (dateString: string, formatString?: string): string => {
  try {
    const date = parseISO(dateString);
    if (!isValid(date)) {
      return 'Invalid date';
    }
    
    // If format string is provided, use it
    if (formatString) {
      return format(date, formatString);
    }
    
    // Otherwise, get format from localStorage or use default
    const userDateFormat = localStorage.getItem('dateFormat') || 'MM/dd/yyyy';
    return format(date, userDateFormat);
  } catch (error) {
    console.error('Error formatting date:', error);
    return 'Invalid date';
  }
};

/**
 * Format a time string according to the user's preferences
 * @param timeString Time string to format
 * @param formatString Optional format string (overrides user preference)
 * @returns Formatted time string
 */
export const formatTime = (timeString: string, formatString?: string): string => {
  try {
    const date = parseISO(timeString);
    if (!isValid(date)) {
      return 'Invalid time';
    }
    
    // If format string is provided, use it
    if (formatString) {
      return format(date, formatString);
    }
    
    // Otherwise, get format from localStorage or use default
    const userTimeFormat = localStorage.getItem('timeFormat') || 'hh:mm a';
    return format(date, userTimeFormat);
  } catch (error) {
    console.error('Error formatting time:', error);
    return 'Invalid time';
  }
};

/**
 * Format a date and time string according to the user's preferences
 * @param dateTimeString Date and time string to format
 * @param formatString Optional format string (overrides user preference)
 * @returns Formatted date and time string
 */
export const formatDateTime = (dateTimeString: string, formatString?: string): string => {
  try {
    const date = parseISO(dateTimeString);
    if (!isValid(date)) {
      return 'Invalid date/time';
    }
    
    // If format string is provided, use it
    if (formatString) {
      return format(date, formatString);
    }
    
    // Otherwise, get format from localStorage or use default
    const userDateFormat = localStorage.getItem('dateFormat') || 'MM/dd/yyyy';
    const userTimeFormat = localStorage.getItem('timeFormat') || 'hh:mm a';
    return format(date, `${userDateFormat} ${userTimeFormat}`);
  } catch (error) {
    console.error('Error formatting date/time:', error);
    return 'Invalid date/time';
  }
};

/**
 * Custom hook for date and time formatting according to user preferences
 * @returns Object with formatting functions
 */
export const useDateTimeFormat = () => {
  const { dateFormat, timeFormat } = useAppSelector((state) => state.userPreferences);
  
  return {
    formatDate: (dateString: string, customFormat?: string) => {
      try {
        const date = parseISO(dateString);
        if (!isValid(date)) {
          return 'Invalid date';
        }
        return format(date, customFormat || dateFormat);
      } catch (error) {
        console.error('Error formatting date:', error);
        return 'Invalid date';
      }
    },
    
    formatTime: (timeString: string, customFormat?: string) => {
      try {
        const date = parseISO(timeString);
        if (!isValid(date)) {
          return 'Invalid time';
        }
        return format(date, customFormat || timeFormat);
      } catch (error) {
        console.error('Error formatting time:', error);
        return 'Invalid time';
      }
    },
    
    formatDateTime: (dateTimeString: string, customFormat?: string) => {
      try {
        const date = parseISO(dateTimeString);
        if (!isValid(date)) {
          return 'Invalid date/time';
        }
        return format(date, customFormat || `${dateFormat} ${timeFormat}`);
      } catch (error) {
        console.error('Error formatting date/time:', error);
        return 'Invalid date/time';
      }
    },
  };
};

export default {
  formatDate,
  formatTime,
  formatDateTime,
  useDateTimeFormat,
};