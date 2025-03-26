import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Divider,
  Switch,
  List,
  ListItem,
  ListItemText,
  FormControlLabel,
  TextField,
  MenuItem,
  Button,
  Grid,
  Tabs,
  Tab,
  IconButton,
  Alert
} from '@mui/material';
import {
  Save as SaveIcon,
  Notifications as NotificationsIcon,
  Security as SecurityIcon,
  Language as LanguageIcon,
  Palette as PaletteIcon,
} from '@mui/icons-material';
import { PageContainer } from '../../components/common/PageContainer';
import useTranslations from '../../hooks/useTranslations';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`settings-tabpanel-${index}`}
      aria-labelledby={`settings-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

function a11yProps(index: number) {
  return {
    id: `settings-tab-${index}`,
    'aria-controls': `settings-tabpanel-${index}`,
  };
}

const Settings: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [notificationSettings, setNotificationSettings] = useState({
    emailNotifications: true,
    pushNotifications: false,
    smsNotifications: false,
    dailyReports: true,
    weeklyReports: true,
    monthlyReports: true,
  });
  const [securitySettings, setSecuritySettings] = useState({
    twoFactorAuth: false,
    passwordReset: false,
    logoutOnInactive: true,
  });
  const [theme, setTheme] = useState('light');
  const [language, setLanguage] = useState('en');
  const [showSaveSuccess, setShowSaveSuccess] = useState(false);
  
  const { translate } = useTranslations();

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleNotificationChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setNotificationSettings({
      ...notificationSettings,
      [event.target.name]: event.target.checked,
    });
  };

  const handleSecurityChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSecuritySettings({
      ...securitySettings,
      [event.target.name]: event.target.checked,
    });
  };

  const handleThemeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setTheme(event.target.value);
  };

  const handleLanguageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setLanguage(event.target.value);
  };

  const handleSave = () => {
    // Here you would save the settings to your backend
    console.log('Saving settings:', {
      notifications: notificationSettings,
      security: securitySettings,
      theme,
      language,
    });
    setShowSaveSuccess(true);
    setTimeout(() => setShowSaveSuccess(false), 3000);
  };

  return (
    <PageContainer title={translate('settings', 'title')}>
      <Card>
        <CardContent>
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs 
              value={tabValue} 
              onChange={handleTabChange} 
              aria-label="settings tabs"
              indicatorColor="primary"
              textColor="primary"
            >
              <Tab icon={<NotificationsIcon />} label="Notifications" {...a11yProps(0)} />
              <Tab icon={<SecurityIcon />} label="Security" {...a11yProps(1)} />
              <Tab icon={<PaletteIcon />} label="Appearance" {...a11yProps(2)} />
              <Tab icon={<LanguageIcon />} label="Language" {...a11yProps(3)} />
            </Tabs>
          </Box>

          {showSaveSuccess && (
            <Alert 
              severity="success" 
              sx={{ mt: 2 }}
              onClose={() => setShowSaveSuccess(false)}
            >
              Settings saved successfully!
            </Alert>
          )}

          <TabPanel value={tabValue} index={0}>
            <Typography variant="h6" gutterBottom>
              Notification Preferences
            </Typography>
            <Divider sx={{ mb: 2 }} />
            
            <List>
              <ListItem>
                <ListItemText 
                  primary="Email Notifications" 
                  secondary="Receive notifications via email"
                />
                <FormControlLabel
                  control={
                    <Switch 
                      checked={notificationSettings.emailNotifications} 
                      onChange={handleNotificationChange}
                      name="emailNotifications"
                      color="primary"
                    />
                  }
                  label=""
                />
              </ListItem>
              <Divider component="li" />
              
              <ListItem>
                <ListItemText 
                  primary="Push Notifications" 
                  secondary="Receive notifications in-app"
                />
                <FormControlLabel
                  control={
                    <Switch 
                      checked={notificationSettings.pushNotifications} 
                      onChange={handleNotificationChange}
                      name="pushNotifications"
                      color="primary"
                    />
                  }
                  label=""
                />
              </ListItem>
              <Divider component="li" />
              
              <ListItem>
                <ListItemText 
                  primary="SMS Notifications" 
                  secondary="Receive notifications via SMS"
                />
                <FormControlLabel
                  control={
                    <Switch 
                      checked={notificationSettings.smsNotifications} 
                      onChange={handleNotificationChange}
                      name="smsNotifications"
                      color="primary"
                    />
                  }
                  label=""
                />
              </ListItem>
              <Divider component="li" />
              
              <ListItem>
                <ListItemText 
                  primary="Daily Reports" 
                  secondary="Receive daily sales reports"
                />
                <FormControlLabel
                  control={
                    <Switch 
                      checked={notificationSettings.dailyReports} 
                      onChange={handleNotificationChange}
                      name="dailyReports"
                      color="primary"
                    />
                  }
                  label=""
                />
              </ListItem>
              <Divider component="li" />
              
              <ListItem>
                <ListItemText 
                  primary="Weekly Reports" 
                  secondary="Receive weekly summary reports"
                />
                <FormControlLabel
                  control={
                    <Switch 
                      checked={notificationSettings.weeklyReports} 
                      onChange={handleNotificationChange}
                      name="weeklyReports"
                      color="primary"
                    />
                  }
                  label=""
                />
              </ListItem>
              <Divider component="li" />
              
              <ListItem>
                <ListItemText 
                  primary="Monthly Reports" 
                  secondary="Receive monthly analytics reports"
                />
                <FormControlLabel
                  control={
                    <Switch 
                      checked={notificationSettings.monthlyReports} 
                      onChange={handleNotificationChange}
                      name="monthlyReports"
                      color="primary"
                    />
                  }
                  label=""
                />
              </ListItem>
            </List>
          </TabPanel>

          <TabPanel value={tabValue} index={1}>
            <Typography variant="h6" gutterBottom>
              Security Settings
            </Typography>
            <Divider sx={{ mb: 2 }} />
            
            <List>
              <ListItem>
                <ListItemText 
                  primary="Two-Factor Authentication" 
                  secondary="Enable 2FA for additional security"
                />
                <FormControlLabel
                  control={
                    <Switch 
                      checked={securitySettings.twoFactorAuth} 
                      onChange={handleSecurityChange}
                      name="twoFactorAuth"
                      color="primary"
                    />
                  }
                  label=""
                />
              </ListItem>
              <Divider component="li" />
              
              <ListItem>
                <ListItemText 
                  primary="Periodic Password Reset" 
                  secondary="Prompt for password reset every 90 days"
                />
                <FormControlLabel
                  control={
                    <Switch 
                      checked={securitySettings.passwordReset} 
                      onChange={handleSecurityChange}
                      name="passwordReset"
                      color="primary"
                    />
                  }
                  label=""
                />
              </ListItem>
              <Divider component="li" />
              
              <ListItem>
                <ListItemText 
                  primary="Auto-Logout" 
                  secondary="Automatically log out after 30 minutes of inactivity"
                />
                <FormControlLabel
                  control={
                    <Switch 
                      checked={securitySettings.logoutOnInactive} 
                      onChange={handleSecurityChange}
                      name="logoutOnInactive"
                      color="primary"
                    />
                  }
                  label=""
                />
              </ListItem>
            </List>
            
            <Box sx={{ mt: 4 }}>
              <Button variant="outlined" color="primary">
                Change Password
              </Button>
            </Box>
          </TabPanel>

          <TabPanel value={tabValue} index={2}>
            <Typography variant="h6" gutterBottom>
              Appearance Settings
            </Typography>
            <Divider sx={{ mb: 2 }} />
            
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <TextField
                  select
                  fullWidth
                  label="Theme"
                  value={theme}
                  onChange={handleThemeChange}
                >
                  <MenuItem value="light">Light</MenuItem>
                  <MenuItem value="dark">Dark</MenuItem>
                  <MenuItem value="system">System Default</MenuItem>
                </TextField>
              </Grid>
            </Grid>
          </TabPanel>

          <TabPanel value={tabValue} index={3}>
            <Typography variant="h6" gutterBottom>
              Language Settings
            </Typography>
            <Divider sx={{ mb: 2 }} />
            
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <TextField
                  select
                  fullWidth
                  label="Language"
                  value={language}
                  onChange={handleLanguageChange}
                >
                  <MenuItem value="en">English</MenuItem>
                  <MenuItem value="es">Español</MenuItem>
                  <MenuItem value="fr">Français</MenuItem>
                  <MenuItem value="de">Deutsch</MenuItem>
                </TextField>
              </Grid>
            </Grid>
          </TabPanel>

          <Box sx={{ display: 'flex', justifyContent: 'flex-end', p: 2 }}>
            <Button
              variant="contained"
              color="primary"
              startIcon={<SaveIcon />}
              onClick={handleSave}
            >
              Save Settings
            </Button>
          </Box>
        </CardContent>
      </Card>
    </PageContainer>
  );
};

export default Settings; 