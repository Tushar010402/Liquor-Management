import { useContext } from 'react';
import { useTheme as useMuiTheme } from '@mui/material/styles';
import { ThemeContext } from '../theme/ThemeProvider';
import { ThemeMode } from '../theme';
import { useAppSelector } from '../store';

/**
 * Custom hook for using the theme
 * @returns Theme context and MUI theme
 */
const useTheme = () => {
  const { toggleColorMode, setMode } = useContext(ThemeContext);
  const muiTheme = useMuiTheme();
  const { themeMode } = useAppSelector((state) => state.userPreferences);

  /**
   * Check if the current theme is dark
   * @returns True if the theme is dark
   */
  const isDarkMode = muiTheme.palette.mode === 'dark';

  /**
   * Check if the current theme is light
   * @returns True if the theme is light
   */
  const isLightMode = muiTheme.palette.mode === 'light';

  /**
   * Check if the current theme is system
   * @returns True if the theme is system
   */
  const isSystemMode = themeMode === 'system';

  /**
   * Toggle between light and dark mode
   */
  const toggleTheme = toggleColorMode;

  /**
   * Set the theme mode
   * @param mode Theme mode
   */
  const setTheme = (mode: ThemeMode) => {
    setMode(mode);
  };

  return {
    theme: muiTheme,
    themeMode,
    isDarkMode,
    isLightMode,
    isSystemMode,
    toggleTheme,
    setTheme,
  };
};

export default useTheme;