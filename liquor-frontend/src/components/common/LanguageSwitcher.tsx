import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import {
  Button,
  Menu,
  MenuItem,
  ListItemIcon,
  ListItemText,
  Typography,
} from '@mui/material';
import { Language as LanguageIcon } from '@mui/icons-material';
import { languages } from '../../i18n';
import { useAppDispatch, useAppSelector } from '../../store';
import { setLanguage } from '../../store/slices/userPreferencesSlice';

/**
 * Language switcher component
 */
const LanguageSwitcher: React.FC = () => {
  const { i18n } = useTranslation();
  const dispatch = useAppDispatch();
  const { language } = useAppSelector((state) => state.userPreferences);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLanguageChange = (lng: string) => {
    i18n.changeLanguage(lng);
    dispatch(setLanguage(lng));
    handleClose();
  };

  return (
    <>
      <Button
        color="inherit"
        onClick={handleClick}
        startIcon={<LanguageIcon />}
        aria-controls={open ? 'language-menu' : undefined}
        aria-haspopup="true"
        aria-expanded={open ? 'true' : undefined}
      >
        {language ? languages[language as keyof typeof languages]?.nativeName : 'Language'}
      </Button>
      <Menu
        id="language-menu"
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        MenuListProps={{
          'aria-labelledby': 'language-button',
        }}
      >
        {Object.entries(languages).map(([code, { name, nativeName }]) => (
          <MenuItem
            key={code}
            onClick={() => handleLanguageChange(code)}
            selected={i18n.language === code}
          >
            <ListItemIcon>
              <LanguageIcon fontSize="small" />
            </ListItemIcon>
            <ListItemText>
              <Typography variant="body1">{name}</Typography>
              <Typography variant="caption" color="text.secondary">
                {nativeName}
              </Typography>
            </ListItemText>
          </MenuItem>
        ))}
      </Menu>
    </>
  );
};

export default LanguageSwitcher;