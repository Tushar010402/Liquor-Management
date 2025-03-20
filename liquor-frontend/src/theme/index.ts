import { Theme } from '@mui/material';
import lightTheme from './schemes/lightTheme';
import darkTheme from './schemes/darkTheme';

export type ThemeMode = 'light' | 'dark' | 'system';

/**
 * Get the appropriate theme based on the mode
 * @param mode Theme mode
 * @returns Theme object
 */
export const getTheme = (mode: ThemeMode): Theme => {
  // If mode is system, use the system preference
  if (mode === 'system') {
    const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
    return prefersDarkMode ? darkTheme : lightTheme;
  }

  // Otherwise, use the specified mode
  return mode === 'dark' ? darkTheme : lightTheme;
};

export { lightTheme, darkTheme };