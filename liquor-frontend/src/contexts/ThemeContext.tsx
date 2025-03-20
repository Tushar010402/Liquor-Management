import React, { createContext, useState, useEffect, useCallback, ReactNode } from 'react';
import { ThemeProvider as MuiThemeProvider, createTheme, Theme, PaletteMode } from '@mui/material';
import { lightTheme, darkTheme } from '../theme';

// Define theme context interface
interface ThemeContextType {
  theme: Theme;
  isDarkMode: boolean;
  toggleTheme: () => void;
  setThemeMode: (mode: PaletteMode) => void;
}

// Create the theme context
export const ThemeContext = createContext<ThemeContextType>({
  theme: lightTheme,
  isDarkMode: false,
  toggleTheme: () => {},
  setThemeMode: () => {},
});

interface ThemeProviderProps {
  children: ReactNode;
}

/**
 * ThemeProvider component that provides theme context to the application
 */
export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  // Get the initial theme mode from localStorage or default to 'light'
  const [mode, setMode] = useState<PaletteMode>(() => {
    const savedMode = localStorage.getItem('themeMode');
    return (savedMode as PaletteMode) || 'light';
  });

  // Create the theme based on the mode
  const theme = mode === 'dark' ? darkTheme : lightTheme;
  const isDarkMode = mode === 'dark';

  // Update localStorage when the theme mode changes
  useEffect(() => {
    localStorage.setItem('themeMode', mode);
  }, [mode]);

  /**
   * Toggle between light and dark mode
   */
  const toggleTheme = useCallback(() => {
    setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
  }, []);

  /**
   * Set the theme mode
   * @param newMode - The new theme mode
   */
  const setThemeMode = useCallback((newMode: PaletteMode) => {
    setMode(newMode);
  }, []);

  return (
    <ThemeContext.Provider
      value={{
        theme,
        isDarkMode,
        toggleTheme,
        setThemeMode,
      }}
    >
      <MuiThemeProvider theme={theme}>{children}</MuiThemeProvider>
    </ThemeContext.Provider>
  );
};

export default ThemeProvider;