import React, { createContext, useEffect, useMemo, ReactNode } from 'react';
import { ThemeProvider as MuiThemeProvider } from '@mui/material';
import { useAppDispatch, useAppSelector } from '../store';
import { setThemeMode } from '../store/slices/userPreferencesSlice';
import { getTheme, ThemeMode } from './index';

type ThemeContextType = {
  toggleColorMode: () => void;
  setMode: (mode: ThemeMode) => void;
};

export const ThemeContext = createContext<ThemeContextType>({
  toggleColorMode: () => {},
  setMode: () => {},
});

interface ThemeProviderProps {
  children: ReactNode;
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  const dispatch = useAppDispatch();
  const { themeMode } = useAppSelector((state) => state.userPreferences);

  // Listen for system theme changes
  useEffect(() => {
    if (themeMode === 'system') {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      
      const handleChange = () => {
        // Force a re-render when system theme changes
        dispatch(setThemeMode('system'));
      };
      
      mediaQuery.addEventListener('change', handleChange);
      
      return () => {
        mediaQuery.removeEventListener('change', handleChange);
      };
    }
  }, [themeMode, dispatch]);

  // Create theme context value
  const colorMode = useMemo(
    () => ({
      toggleColorMode: () => {
        const newMode = themeMode === 'light' ? 'dark' : 'light';
        dispatch(setThemeMode(newMode));
      },
      setMode: (mode: ThemeMode) => {
        dispatch(setThemeMode(mode));
      },
    }),
    [themeMode, dispatch]
  );

  // Get the current theme
  const theme = useMemo(() => getTheme(themeMode), [themeMode]);

  return (
    <ThemeContext.Provider value={colorMode}>
      <MuiThemeProvider theme={theme}>
        {children}
      </MuiThemeProvider>
    </ThemeContext.Provider>
  );
};

export default ThemeProvider;