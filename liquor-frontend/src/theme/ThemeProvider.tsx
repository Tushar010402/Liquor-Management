import React, { createContext, useState, useMemo, ReactNode } from 'react';
import { ThemeProvider as MuiThemeProvider, CssBaseline } from '@mui/material';
import { SnackbarProvider } from 'notistack';
import theme from './theme';

type ThemeContextType = {
  toggleColorMode: () => void;
};

export const ThemeContext = createContext<ThemeContextType>({
  toggleColorMode: () => {},
});

interface ThemeProviderProps {
  children: ReactNode;
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  const [mode, setMode] = useState<'light' | 'dark'>('light');

  const colorMode = useMemo(
    () => ({
      toggleColorMode: () => {
        setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
      },
    }),
    []
  );

  // For now, we're only using the light theme
  // In the future, we can implement dark mode by creating a darkTheme

  return (
    <ThemeContext.Provider value={colorMode}>
      <MuiThemeProvider theme={theme}>
        <CssBaseline />
        <SnackbarProvider
          maxSnack={3}
          anchorOrigin={{
            vertical: 'top',
            horizontal: 'right',
          }}
          autoHideDuration={5000}
        >
          {children}
        </SnackbarProvider>
      </MuiThemeProvider>
    </ThemeContext.Provider>
  );
};

export default ThemeProvider;