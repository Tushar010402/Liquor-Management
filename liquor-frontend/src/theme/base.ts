import { Theme, ThemeOptions } from '@mui/material';

/**
 * Base theme options that are common to all themes
 */
export const baseThemeOptions: ThemeOptions = {
  typography: {
    fontFamily: '"Inter", "Helvetica", "Arial", sans-serif',
    fontSize: 14,
    fontWeightLight: 300,
    fontWeightRegular: 400,
    fontWeightMedium: 500,
    fontWeightBold: 700,
    h1: {
      fontWeight: 700,
      fontSize: '2.5rem',
      lineHeight: 1.2,
    },
    h2: {
      fontWeight: 700,
      fontSize: '2rem',
      lineHeight: 1.2,
    },
    h3: {
      fontWeight: 700,
      fontSize: '1.75rem',
      lineHeight: 1.2,
    },
    h4: {
      fontWeight: 700,
      fontSize: '1.5rem',
      lineHeight: 1.2,
    },
    h5: {
      fontWeight: 600,
      fontSize: '1.25rem',
      lineHeight: 1.2,
    },
    h6: {
      fontWeight: 600,
      fontSize: '1rem',
      lineHeight: 1.2,
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.5,
    },
    body2: {
      fontSize: '0.875rem',
      lineHeight: 1.5,
    },
    subtitle1: {
      fontSize: '1rem',
      fontWeight: 500,
      lineHeight: 1.5,
    },
    subtitle2: {
      fontSize: '0.875rem',
      fontWeight: 500,
      lineHeight: 1.5,
    },
    button: {
      fontWeight: 600,
      textTransform: 'none',
    },
    caption: {
      fontSize: '0.75rem',
      lineHeight: 1.5,
    },
    overline: {
      fontSize: '0.75rem',
      fontWeight: 600,
      textTransform: 'uppercase',
      letterSpacing: '0.5px',
      lineHeight: 1.5,
    },
  },
  shape: {
    borderRadius: 8,
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        '*': {
          boxSizing: 'border-box',
        },
        html: {
          margin: 0,
          padding: 0,
          width: '100%',
          height: '100%',
          WebkitOverflowScrolling: 'touch',
        },
        body: {
          margin: 0,
          padding: 0,
          width: '100%',
          height: '100%',
        },
        '#root': {
          width: '100%',
          height: '100%',
        },
        input: {
          '&[type=number]': {
            MozAppearance: 'textfield',
            '&::-webkit-outer-spin-button': {
              margin: 0,
              WebkitAppearance: 'none',
            },
            '&::-webkit-inner-spin-button': {
              margin: 0,
              WebkitAppearance: 'none',
            },
          },
        },
        img: {
          display: 'block',
          maxWidth: '100%',
        },
        a: {
          textDecoration: 'none',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 600,
          borderRadius: 8,
        },
        sizeSmall: {
          padding: '6px 16px',
        },
        sizeMedium: {
          padding: '8px 20px',
        },
        sizeLarge: {
          padding: '11px 24px',
        },
        textSizeSmall: {
          padding: '7px 12px',
        },
        textSizeMedium: {
          padding: '9px 16px',
        },
        textSizeLarge: {
          padding: '12px 16px',
        },
      },
    },
    MuiButtonBase: {
      defaultProps: {
        disableRipple: false,
      },
    },
    MuiCardContent: {
      styleOverrides: {
        root: {
          padding: '32px 24px',
          '&:last-child': {
            paddingBottom: '32px',
          },
        },
      },
    },
    MuiCardHeader: {
      defaultProps: {
        titleTypographyProps: {
          variant: 'h6',
        },
        subheaderTypographyProps: {
          variant: 'body2',
        },
      },
      styleOverrides: {
        root: {
          padding: '32px 24px 16px',
        },
      },
    },
    MuiOutlinedInput: {
      styleOverrides: {
        notchedOutline: {
          borderColor: 'rgba(0, 0, 0, 0.23)',
        },
      },
    },
    MuiTab: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 500,
          fontSize: '0.875rem',
        },
      },
    },
    MuiTabs: {
      styleOverrides: {
        indicator: {
          height: 3,
          borderTopLeftRadius: 3,
          borderTopRightRadius: 3,
        },
      },
    },
    MuiTableCell: {
      styleOverrides: {
        root: {
          padding: '16px',
          borderBottom: '1px solid rgba(0, 0, 0, 0.12)',
        },
        head: {
          color: 'rgba(0, 0, 0, 0.87)',
          fontWeight: 600,
        },
        body: {
          color: 'rgba(0, 0, 0, 0.87)',
        },
      },
    },
    MuiTableRow: {
      styleOverrides: {
        root: {
          '&:last-child td': {
            borderBottom: 0,
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
        },
        rounded: {
          borderRadius: 8,
        },
      },
    },
    MuiListItemButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          '&.Mui-selected': {
            fontWeight: 600,
          },
        },
      },
    },
    MuiListItemIcon: {
      styleOverrides: {
        root: {
          minWidth: 40,
        },
      },
    },
    MuiListItemText: {
      styleOverrides: {
        primary: {
          fontWeight: 500,
        },
      },
    },
    MuiInputBase: {
      styleOverrides: {
        input: {
          '&::placeholder': {
            opacity: 0.7,
          },
        },
      },
    },
    MuiMenuItem: {
      styleOverrides: {
        root: {
          borderRadius: 4,
        },
      },
    },
    MuiCheckbox: {
      styleOverrides: {
        root: {
          padding: 10,
        },
      },
    },
    MuiRadio: {
      styleOverrides: {
        root: {
          padding: 10,
        },
      },
    },
    MuiSwitch: {
      styleOverrides: {
        root: {
          padding: 8,
        },
        track: {
          borderRadius: 10,
        },
        thumb: {
          borderRadius: 8,
        },
      },
    },
    MuiAvatar: {
      styleOverrides: {
        root: {
          fontSize: '1rem',
          fontWeight: 600,
        },
      },
    },
  },
};

/**
 * Create shadows for a theme
 * @param mode Theme mode
 * @returns Shadows array
 */
export const createShadows = (mode: 'light' | 'dark') => {
  const shadowColor = mode === 'light' ? 'rgba(0, 0, 0, 0.1)' : 'rgba(0, 0, 0, 0.3)';
  const shadowColorStrong = mode === 'light' ? 'rgba(0, 0, 0, 0.15)' : 'rgba(0, 0, 0, 0.5)';

  return [
    'none',
    `0px 1px 2px ${shadowColor}`,
    `0px 1px 2px ${shadowColor}, 0px 2px 4px ${shadowColor}`,
    `0px 1px 3px ${shadowColor}, 0px 2px 6px ${shadowColor}`,
    `0px 1px 3px ${shadowColor}, 0px 3px 8px ${shadowColor}`,
    `0px 1px 3px ${shadowColor}, 0px 4px 12px ${shadowColor}`,
    `0px 2px 4px ${shadowColor}, 0px 6px 16px ${shadowColor}`,
    `0px 2px 5px ${shadowColor}, 0px 8px 20px ${shadowColor}`,
    `0px 3px 6px ${shadowColor}, 0px 10px 24px ${shadowColor}`,
    `0px 3px 8px ${shadowColor}, 0px 12px 28px ${shadowColor}`,
    `0px 4px 10px ${shadowColor}, 0px 14px 32px ${shadowColor}`,
    `0px 5px 12px ${shadowColor}, 0px 16px 36px ${shadowColor}`,
    `0px 6px 14px ${shadowColor}, 0px 18px 40px ${shadowColor}`,
    `0px 7px 16px ${shadowColor}, 0px 20px 44px ${shadowColor}`,
    `0px 8px 18px ${shadowColor}, 0px 22px 48px ${shadowColor}`,
    `0px 9px 20px ${shadowColor}, 0px 24px 52px ${shadowColor}`,
    `0px 10px 22px ${shadowColor}, 0px 26px 56px ${shadowColor}`,
    `0px 11px 24px ${shadowColor}, 0px 28px 60px ${shadowColor}`,
    `0px 12px 26px ${shadowColor}, 0px 30px 64px ${shadowColor}`,
    `0px 13px 28px ${shadowColor}, 0px 32px 68px ${shadowColor}`,
    `0px 14px 30px ${shadowColor}, 0px 34px 72px ${shadowColor}`,
    `0px 15px 32px ${shadowColor}, 0px 36px 76px ${shadowColor}`,
    `0px 16px 34px ${shadowColor}, 0px 38px 80px ${shadowColor}`,
    `0px 17px 36px ${shadowColor}, 0px 40px 84px ${shadowColor}`,
    `0px 18px 38px ${shadowColorStrong}, 0px 42px 88px ${shadowColorStrong}`,
  ];
};