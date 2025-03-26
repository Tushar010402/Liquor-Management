import { createTheme, alpha } from '@mui/material';
import { baseThemeOptions, createShadows } from '../base';

// Define primary and secondary colors
const primaryColor = {
  light: '#6573c3',
  main: '#3f51b5',
  dark: '#2c387e',
  contrastText: '#ffffff',
};

const secondaryColor = {
  light: '#33c9dc',
  main: '#00bcd4',
  dark: '#008394',
  contrastText: '#ffffff',
};

// Create the light theme
const lightTheme = createTheme({
  ...baseThemeOptions,
  palette: {
    mode: 'light',
    background: {
      default: '#f8f9fa',
      paper: '#ffffff',
    },
    primary: primaryColor,
    secondary: secondaryColor,
    tertiary: {
      main: '#9c27b0',
      light: '#ba68c8',
      dark: '#7b1fa2',
      contrastText: '#ffffff',
    },
    neutral: {
      main: '#757575',
      light: '#9e9e9e',
      dark: '#616161',
      contrastText: '#ffffff',
    },
    text: {
      primary: 'rgba(0, 0, 0, 0.87)',
      secondary: 'rgba(0, 0, 0, 0.6)',
      disabled: 'rgba(0, 0, 0, 0.38)',
    },
    divider: 'rgba(0, 0, 0, 0.12)',
    action: {
      active: 'rgba(0, 0, 0, 0.54)',
      hover: 'rgba(0, 0, 0, 0.04)',
      selected: 'rgba(0, 0, 0, 0.08)',
      disabled: 'rgba(0, 0, 0, 0.26)',
      disabledBackground: 'rgba(0, 0, 0, 0.12)',
      focus: 'rgba(0, 0, 0, 0.12)',
    },
    success: {
      light: '#81c784',
      main: '#4caf50',
      dark: '#388e3c',
      contrastText: '#ffffff',
    },
    warning: {
      light: '#ffb74d',
      main: '#ff9800',
      dark: '#f57c00',
      contrastText: 'rgba(0, 0, 0, 0.87)',
    },
    error: {
      light: '#e57373',
      main: '#f44336',
      dark: '#d32f2f',
      contrastText: '#ffffff',
    },
    info: {
      light: '#64b5f6',
      main: '#2196f3',
      dark: '#1976d2',
      contrastText: '#ffffff',
    },
  },
  shadows: createShadows('light') as ["none", string, string, string, string, string, string, string, string, string, string, string, string, string, string, string, string, string, string, string, string, string, string, string, string],
  components: {
    ...baseThemeOptions.components,
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: '#ffffff',
          color: 'rgba(0, 0, 0, 0.87)',
          boxShadow: '0px 1px 3px rgba(0, 0, 0, 0.1)',
        },
      },
      defaultProps: {
        elevation: 0,
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          backgroundColor: '#ffffff',
          borderRight: '1px solid rgba(0, 0, 0, 0.12)',
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0px 1px 3px rgba(0, 0, 0, 0.1), 0px 2px 6px rgba(0, 0, 0, 0.05)',
          borderRadius: 12,
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
        },
        elevation1: {
          boxShadow: '0px 1px 3px rgba(0, 0, 0, 0.1), 0px 2px 6px rgba(0, 0, 0, 0.05)',
        },
      },
    },
    MuiTableHead: {
      styleOverrides: {
        root: {
          backgroundColor: alpha(primaryColor.main, 0.05),
          '& .MuiTableCell-root': {
            color: 'rgba(0, 0, 0, 0.87)',
            fontWeight: 600,
          },
        },
      },
    },
    MuiTableRow: {
      styleOverrides: {
        root: {
          '&:nth-of-type(even)': {
            backgroundColor: alpha(primaryColor.main, 0.02),
          },
          '&:hover': {
            backgroundColor: alpha(primaryColor.main, 0.05),
          },
        },
      },
    },
    MuiListItemButton: {
      styleOverrides: {
        root: {
          '&.Mui-selected': {
            backgroundColor: alpha(primaryColor.main, 0.1),
            color: primaryColor.main,
            '&:hover': {
              backgroundColor: alpha(primaryColor.main, 0.15),
            },
            '& .MuiListItemIcon-root': {
              color: primaryColor.main,
            },
          },
          '&:hover': {
            backgroundColor: alpha(primaryColor.main, 0.05),
          },
        },
      },
    },
  },
});

export default lightTheme;