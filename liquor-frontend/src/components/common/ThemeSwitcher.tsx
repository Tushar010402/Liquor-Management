import React, { useState } from 'react';
import {
  Button,
  Menu,
  MenuItem,
  ListItemIcon,
  ListItemText,
  Typography,
} from '@mui/material';
import {
  Brightness4 as DarkModeIcon,
  Brightness7 as LightModeIcon,
  BrightnessAuto as SystemModeIcon,
  Palette as PaletteIcon,
} from '@mui/icons-material';
import { useTheme, useTranslations } from '../../hooks';
import { ThemeMode } from '../../theme';

/**
 * Theme switcher component
 */
const ThemeSwitcher: React.FC = () => {
  const { themeMode, setTheme } = useTheme();
  const { settings } = useTranslations();
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleThemeChange = (mode: ThemeMode) => {
    setTheme(mode);
    handleClose();
  };

  // Get the icon for the current theme mode
  const getThemeIcon = () => {
    switch (themeMode) {
      case 'dark':
        return <DarkModeIcon />;
      case 'light':
        return <LightModeIcon />;
      case 'system':
        return <SystemModeIcon />;
      default:
        return <PaletteIcon />;
    }
  };

  // Get the label for the current theme mode
  const getThemeLabel = () => {
    switch (themeMode) {
      case 'dark':
        return settings('darkMode');
      case 'light':
        return settings('lightMode');
      case 'system':
        return settings('systemMode');
      default:
        return settings('theme');
    }
  };

  return (
    <>
      <Button
        color="inherit"
        onClick={handleClick}
        startIcon={getThemeIcon()}
        aria-controls={open ? 'theme-menu' : undefined}
        aria-haspopup="true"
        aria-expanded={open ? 'true' : undefined}
      >
        {getThemeLabel()}
      </Button>
      <Menu
        id="theme-menu"
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        MenuListProps={{
          'aria-labelledby': 'theme-button',
        }}
      >
        <MenuItem
          onClick={() => handleThemeChange('light')}
          selected={themeMode === 'light'}
        >
          <ListItemIcon>
            <LightModeIcon fontSize="small" />
          </ListItemIcon>
          <ListItemText>
            <Typography variant="body1">{settings('lightMode')}</Typography>
          </ListItemText>
        </MenuItem>
        <MenuItem
          onClick={() => handleThemeChange('dark')}
          selected={themeMode === 'dark'}
        >
          <ListItemIcon>
            <DarkModeIcon fontSize="small" />
          </ListItemIcon>
          <ListItemText>
            <Typography variant="body1">{settings('darkMode')}</Typography>
          </ListItemText>
        </MenuItem>
        <MenuItem
          onClick={() => handleThemeChange('system')}
          selected={themeMode === 'system'}
        >
          <ListItemIcon>
            <SystemModeIcon fontSize="small" />
          </ListItemIcon>
          <ListItemText>
            <Typography variant="body1">{settings('systemMode')}</Typography>
          </ListItemText>
        </MenuItem>
      </Menu>
    </>
  );
};

export default ThemeSwitcher;