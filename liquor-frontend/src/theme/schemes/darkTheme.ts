import { createTheme, alpha } from '@mui/material';
import { baseThemeOptions, createShadows } from '../base';

// Define primary and secondary colors
const primaryColor = {
  light: '#7986cb',
  main: '#5c6bc0',
  dark: '#3f51b5',
  contrastText: '#ffffff',
};

const secondaryColor = {
  light: '#4dd0e1',
  main: '#26c6da',
  dark: '#00bcd4',
  contrastText: '#ffffff',
};

// Create the dark theme
const darkTheme = createTheme({
  ...baseThemeOptions,
  palette: {
    mode: 'dark',
    background: {
      default: '#121212',
      paper: '#1e1e1e',
    },
    primary: primaryColor,
    secondary: secondaryColor,
    text: {
      primary: '#ffffff',
      secondary: 'rgba(255, 255, 255, 0.7)',
      disabled: 'rgba(255, 255, 255, 0.5)',
    },
    divider: 'rgba(255, 255, 255, 0.12)',
    action: {
      active: '#ffffff',
      hover: 'rgba(255, 255, 255, 0.08)',
      selected: 'rgba(255, 255, 255, 0.16)',
      disabled: 'rgba(255, 255, 255, 0.3)',
      disabledBackground: 'rgba(255, 255, 255, 0.12)',
      focus: 'rgba(255, 255, 255, 0.12)',
    },
    success: {
      light: '#81c784',
      main: '#4caf50',
      dark: '#388e3c',
      contrastText: 'rgba(0, 0, 0, 0.87)',
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
  shadows: createShadows('dark'),
  components: {
    ...baseThemeOptions.components,
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: '#1e1e1e',
          boxShadow: '0px 1px 3px rgba(0, 0, 0, 0.3)',
        },
      },
      defaultProps: {
        elevation: 0,
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          backgroundColor: '#1e1e1e',
          borderRight: '1px solid rgba(255, 255, 255, 0.12)',
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0px 1px 3px rgba(0, 0, 0, 0.3), 0px 2px 6px rgba(0, 0, 0, 0.15)',
          borderRadius: 12,
          backgroundColor: '#1e1e1e',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          backgroundColor: '#1e1e1e',
        },
        elevation1: {
          boxShadow: '0px 1px 3px rgba(0, 0, 0, 0.3), 0px 2px 6px rgba(0, 0, 0, 0.15)',
        },
      },
    },
    MuiTableHead: {
      styleOverrides: {
        root: {
          backgroundColor: alpha(primaryColor.main, 0.15),
          '& .MuiTableCell-root': {
            color: '#ffffff',
            fontWeight: 600,
          },
        },
      },
    },
    MuiTableRow: {
      styleOverrides: {
        root: {
          '&:nth-of-type(even)': {
            backgroundColor: alpha(primaryColor.main, 0.05),
          },
          '&:hover': {
            backgroundColor: alpha(primaryColor.main, 0.1),
          },
        },
      },
    },
    MuiTableCell: {
      styleOverrides: {
        root: {
          borderBottom: '1px solid rgba(255, 255, 255, 0.12)',
        },
      },
    },
    MuiListItemButton: {
      styleOverrides: {
        root: {
          '&.Mui-selected': {
            backgroundColor: alpha(primaryColor.main, 0.2),
            color: primaryColor.light,
            '&:hover': {
              backgroundColor: alpha(primaryColor.main, 0.25),
            },
            '& .MuiListItemIcon-root': {
              color: primaryColor.light,
            },
          },
          '&:hover': {
            backgroundColor: alpha(primaryColor.main, 0.1),
          },
        },
      },
    },
    MuiOutlinedInput: {
      styleOverrides: {
        notchedOutline: {
          borderColor: 'rgba(255, 255, 255, 0.23)',
        },
      },
    },
    MuiSwitch: {
      styleOverrides: {
        switchBase: {
          color: '#ffffff',
        },
        track: {
          backgroundColor: 'rgba(255, 255, 255, 0.3)',
        },
      },
    },
    MuiInputBase: {
      styleOverrides: {
        input: {
          '&::placeholder': {
            color: 'rgba(255, 255, 255, 0.5)',
            opacity: 1,
          },
        },
      },
    },
    MuiCheckbox: {
      styleOverrides: {
        root: {
          color: 'rgba(255, 255, 255, 0.7)',
        },
      },
    },
    MuiRadio: {
      styleOverrides: {
        root: {
          color: 'rgba(255, 255, 255, 0.7)',
        },
      },
    },
    MuiDivider: {
      styleOverrides: {
        root: {
          backgroundColor: 'rgba(255, 255, 255, 0.12)',
        },
      },
    },
  },
});

export default darkTheme;