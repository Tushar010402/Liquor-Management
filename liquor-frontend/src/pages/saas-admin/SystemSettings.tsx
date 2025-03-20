import React, { useState } from 'react';
import {
  Box,
  Container,
  Typography,
  Button,
  Card,
  CardContent,
  Grid,
  TextField,
  Switch,
  FormControlLabel,
  Divider,
  Tabs,
  Tab,
  Alert,
  Snackbar,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormHelperText,
  IconButton,
  InputAdornment,
  useTheme,
} from '@mui/material';
import {
  Settings as SettingsIcon,
  Save as SaveIcon,
  Refresh as RefreshIcon,
  Security as SecurityIcon,
  Notifications as NotificationsIcon,
  Email as EmailIcon,
  Storage as StorageIcon,
  CloudUpload as CloudUploadIcon,
  CloudDownload as CloudDownloadIcon,
  Delete as DeleteIcon,
  Backup as BackupIcon,
  Restore as RestoreIcon,
  Visibility as VisibilityIcon,
  VisibilityOff as VisibilityOffIcon,
} from '@mui/icons-material';
import { PageHeader } from '../../components/common';
import { useTranslations, useFormValidation } from '../../hooks';
import * as Yup from 'yup';

// Validation schema for general settings
const generalSettingsSchema = Yup.object({
  appName: Yup.string().required('Application name is required'),
  supportEmail: Yup.string().email('Invalid email address').required('Support email is required'),
  defaultLanguage: Yup.string().required('Default language is required'),
  defaultCurrency: Yup.string().required('Default currency is required'),
  defaultDateFormat: Yup.string().required('Default date format is required'),
  defaultTimeFormat: Yup.string().required('Default time format is required'),
  sessionTimeout: Yup.number()
    .positive('Must be a positive number')
    .integer('Must be an integer')
    .required('Session timeout is required'),
});

// Validation schema for email settings
const emailSettingsSchema = Yup.object({
  smtpHost: Yup.string().required('SMTP host is required'),
  smtpPort: Yup.number()
    .positive('Must be a positive number')
    .integer('Must be an integer')
    .required('SMTP port is required'),
  smtpUsername: Yup.string().required('SMTP username is required'),
  smtpPassword: Yup.string().required('SMTP password is required'),
  smtpFromEmail: Yup.string().email('Invalid email address').required('From email is required'),
  smtpFromName: Yup.string().required('From name is required'),
});

// Validation schema for storage settings
const storageSettingsSchema = Yup.object({
  storageProvider: Yup.string().required('Storage provider is required'),
  bucketName: Yup.string().when('storageProvider', {
    is: (val: string) => val !== 'local',
    then: Yup.string().required('Bucket name is required'),
    otherwise: Yup.string().nullable(),
  }),
  accessKey: Yup.string().when('storageProvider', {
    is: (val: string) => val !== 'local',
    then: Yup.string().required('Access key is required'),
    otherwise: Yup.string().nullable(),
  }),
  secretKey: Yup.string().when('storageProvider', {
    is: (val: string) => val !== 'local',
    then: Yup.string().required('Secret key is required'),
    otherwise: Yup.string().nullable(),
  }),
  region: Yup.string().when('storageProvider', {
    is: (val: string) => val !== 'local',
    then: Yup.string().required('Region is required'),
    otherwise: Yup.string().nullable(),
  }),
  endpoint: Yup.string().when('storageProvider', {
    is: (val: string) => val === 'other',
    then: Yup.string().required('Endpoint is required'),
    otherwise: Yup.string().nullable(),
  }),
});

// Validation schema for security settings
const securitySettingsSchema = Yup.object({
  passwordMinLength: Yup.number()
    .positive('Must be a positive number')
    .integer('Must be an integer')
    .required('Minimum password length is required'),
  passwordRequireUppercase: Yup.boolean(),
  passwordRequireLowercase: Yup.boolean(),
  passwordRequireNumbers: Yup.boolean(),
  passwordRequireSpecialChars: Yup.boolean(),
  passwordExpiryDays: Yup.number()
    .positive('Must be a positive number')
    .integer('Must be an integer')
    .required('Password expiry days is required'),
  maxLoginAttempts: Yup.number()
    .positive('Must be a positive number')
    .integer('Must be an integer')
    .required('Maximum login attempts is required'),
  twoFactorAuthEnabled: Yup.boolean(),
  twoFactorAuthRequired: Yup.boolean(),
});

/**
 * System Settings component for SaaS Admin
 */
const SystemSettings: React.FC = () => {
  const { common, settings } = useTranslations();
  const theme = useTheme();
  const [tabValue, setTabValue] = useState(0);
  const [showSmtpPassword, setShowSmtpPassword] = useState(false);
  const [showAccessKey, setShowAccessKey] = useState(false);
  const [showSecretKey, setShowSecretKey] = useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [snackbarSeverity, setSnackbarSeverity] = useState<'success' | 'error'>('success');

  // Form validation for general settings
  const generalForm = useFormValidation({
    initialValues: {
      appName: 'Liquor Management System',
      supportEmail: 'support@liquormanagementsystem.com',
      defaultLanguage: 'en',
      defaultCurrency: 'INR',
      defaultDateFormat: 'MM/dd/yyyy',
      defaultTimeFormat: 'hh:mm a',
      sessionTimeout: 30,
      enableUserRegistration: false,
      requireEmailVerification: true,
      enableMaintenanceMode: false,
    },
    validationSchema: generalSettingsSchema,
    onSubmit: (values) => {
      console.log('General settings submitted:', values);
      showSnackbar('General settings saved successfully', 'success');
      // In a real app, you would make an API call to save the settings
    },
  });

  // Form validation for email settings
  const emailForm = useFormValidation({
    initialValues: {
      smtpHost: 'smtp.example.com',
      smtpPort: 587,
      smtpUsername: 'smtp_user',
      smtpPassword: 'smtp_password',
      smtpFromEmail: 'noreply@liquormanagementsystem.com',
      smtpFromName: 'Liquor Management System',
      smtpSecure: true,
      enableEmailNotifications: true,
    },
    validationSchema: emailSettingsSchema,
    onSubmit: (values) => {
      console.log('Email settings submitted:', values);
      showSnackbar('Email settings saved successfully', 'success');
      // In a real app, you would make an API call to save the settings
    },
  });

  // Form validation for storage settings
  const storageForm = useFormValidation({
    initialValues: {
      storageProvider: 'local',
      bucketName: '',
      accessKey: '',
      secretKey: '',
      region: '',
      endpoint: '',
      publicUrlPrefix: '',
      maxUploadSize: 10,
    },
    validationSchema: storageSettingsSchema,
    onSubmit: (values) => {
      console.log('Storage settings submitted:', values);
      showSnackbar('Storage settings saved successfully', 'success');
      // In a real app, you would make an API call to save the settings
    },
  });

  // Form validation for security settings
  const securityForm = useFormValidation({
    initialValues: {
      passwordMinLength: 8,
      passwordRequireUppercase: true,
      passwordRequireLowercase: true,
      passwordRequireNumbers: true,
      passwordRequireSpecialChars: true,
      passwordExpiryDays: 90,
      maxLoginAttempts: 5,
      twoFactorAuthEnabled: true,
      twoFactorAuthRequired: false,
      jwtSecret: 'your-jwt-secret-key',
      jwtExpiryMinutes: 60,
      corsAllowedOrigins: '*',
      rateLimitRequests: 100,
      rateLimitWindowMinutes: 15,
    },
    validationSchema: securitySettingsSchema,
    onSubmit: (values) => {
      console.log('Security settings submitted:', values);
      showSnackbar('Security settings saved successfully', 'success');
      // In a real app, you would make an API call to save the settings
    },
  });

  // Handle tab change
  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  // Show snackbar
  const showSnackbar = (message: string, severity: 'success' | 'error') => {
    setSnackbarMessage(message);
    setSnackbarSeverity(severity);
    setSnackbarOpen(true);
  };

  // Handle snackbar close
  const handleSnackbarClose = () => {
    setSnackbarOpen(false);
  };

  // Handle test email
  const handleTestEmail = () => {
    if (emailForm.formik.isValid) {
      console.log('Sending test email...');
      showSnackbar('Test email sent successfully', 'success');
      // In a real app, you would make an API call to send a test email
    } else {
      emailForm.formik.validateForm();
      showSnackbar('Please fix the errors in the form', 'error');
    }
  };

  // Handle database backup
  const handleDatabaseBackup = () => {
    console.log('Creating database backup...');
    showSnackbar('Database backup created successfully', 'success');
    // In a real app, you would make an API call to create a database backup
  };

  // Handle database restore
  const handleDatabaseRestore = () => {
    console.log('Restoring database...');
    showSnackbar('Database restored successfully', 'success');
    // In a real app, you would make an API call to restore the database
  };

  // Handle clear cache
  const handleClearCache = () => {
    console.log('Clearing cache...');
    showSnackbar('Cache cleared successfully', 'success');
    // In a real app, you would make an API call to clear the cache
  };

  return (
    <Container maxWidth="xl">
      <PageHeader
        title={settings('settings')}
        subtitle={settings('systemSettings')}
        icon={<SettingsIcon fontSize="large" />}
      />

      <Card>
        <CardContent>
          <Tabs
            value={tabValue}
            onChange={handleTabChange}
            indicatorColor="primary"
            textColor="primary"
            variant="scrollable"
            scrollButtons="auto"
            aria-label="settings tabs"
          >
            <Tab
              label={settings('general')}
              icon={<SettingsIcon />}
              iconPosition="start"
            />
            <Tab
              label={settings('email')}
              icon={<EmailIcon />}
              iconPosition="start"
            />
            <Tab
              label={settings('storage')}
              icon={<StorageIcon />}
              iconPosition="start"
            />
            <Tab
              label={settings('security')}
              icon={<SecurityIcon />}
              iconPosition="start"
            />
          </Tabs>

          <Divider sx={{ my: 2 }} />

          {/* General Settings */}
          {tabValue === 0 && (
            <form onSubmit={generalForm.formik.handleSubmit}>
              <Grid container spacing={3}>
                <Grid item xs={12}>
                  <Typography variant="h6" gutterBottom>
                    {settings('generalSettings')}
                  </Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    id="appName"
                    name="appName"
                    label={settings('appName')}
                    value={generalForm.formik.values.appName}
                    onChange={generalForm.formik.handleChange}
                    error={generalForm.formik.touched.appName && Boolean(generalForm.formik.errors.appName)}
                    helperText={generalForm.formik.touched.appName && generalForm.formik.errors.appName}
                    margin="normal"
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    id="supportEmail"
                    name="supportEmail"
                    label={settings('supportEmail')}
                    value={generalForm.formik.values.supportEmail}
                    onChange={generalForm.formik.handleChange}
                    error={generalForm.formik.touched.supportEmail && Boolean(generalForm.formik.errors.supportEmail)}
                    helperText={generalForm.formik.touched.supportEmail && generalForm.formik.errors.supportEmail}
                    margin="normal"
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <FormControl fullWidth margin="normal">
                    <InputLabel id="defaultLanguage-label">{settings('defaultLanguage')}</InputLabel>
                    <Select
                      labelId="defaultLanguage-label"
                      id="defaultLanguage"
                      name="defaultLanguage"
                      value={generalForm.formik.values.defaultLanguage}
                      onChange={generalForm.formik.handleChange}
                      error={generalForm.formik.touched.defaultLanguage && Boolean(generalForm.formik.errors.defaultLanguage)}
                      label={settings('defaultLanguage')}
                    >
                      <MenuItem value="en">English</MenuItem>
                      <MenuItem value="hi">Hindi</MenuItem>
                      <MenuItem value="es">Spanish</MenuItem>
                      <MenuItem value="fr">French</MenuItem>
                    </Select>
                    {generalForm.formik.touched.defaultLanguage && generalForm.formik.errors.defaultLanguage && (
                      <FormHelperText error>{generalForm.formik.errors.defaultLanguage}</FormHelperText>
                    )}
                  </FormControl>
                </Grid>
                <Grid item xs={12} md={6}>
                  <FormControl fullWidth margin="normal">
                    <InputLabel id="defaultCurrency-label">{settings('defaultCurrency')}</InputLabel>
                    <Select
                      labelId="defaultCurrency-label"
                      id="defaultCurrency"
                      name="defaultCurrency"
                      value={generalForm.formik.values.defaultCurrency}
                      onChange={generalForm.formik.handleChange}
                      error={generalForm.formik.touched.defaultCurrency && Boolean(generalForm.formik.errors.defaultCurrency)}
                      label={settings('defaultCurrency')}
                    >
                      <MenuItem value="INR">Indian Rupee (₹)</MenuItem>
                      <MenuItem value="USD">US Dollar ($)</MenuItem>
                      <MenuItem value="EUR">Euro (€)</MenuItem>
                      <MenuItem value="GBP">British Pound (£)</MenuItem>
                    </Select>
                    {generalForm.formik.touched.defaultCurrency && generalForm.formik.errors.defaultCurrency && (
                      <FormHelperText error>{generalForm.formik.errors.defaultCurrency}</FormHelperText>
                    )}
                  </FormControl>
                </Grid>
                <Grid item xs={12} md={6}>
                  <FormControl fullWidth margin="normal">
                    <InputLabel id="defaultDateFormat-label">{settings('defaultDateFormat')}</InputLabel>
                    <Select
                      labelId="defaultDateFormat-label"
                      id="defaultDateFormat"
                      name="defaultDateFormat"
                      value={generalForm.formik.values.defaultDateFormat}
                      onChange={generalForm.formik.handleChange}
                      error={generalForm.formik.touched.defaultDateFormat && Boolean(generalForm.formik.errors.defaultDateFormat)}
                      label={settings('defaultDateFormat')}
                    >
                      <MenuItem value="MM/dd/yyyy">MM/DD/YYYY</MenuItem>
                      <MenuItem value="dd/MM/yyyy">DD/MM/YYYY</MenuItem>
                      <MenuItem value="yyyy-MM-dd">YYYY-MM-DD</MenuItem>
                      <MenuItem value="dd-MMM-yyyy">DD-MMM-YYYY</MenuItem>
                    </Select>
                    {generalForm.formik.touched.defaultDateFormat && generalForm.formik.errors.defaultDateFormat && (
                      <FormHelperText error>{generalForm.formik.errors.defaultDateFormat}</FormHelperText>
                    )}
                  </FormControl>
                </Grid>
                <Grid item xs={12} md={6}>
                  <FormControl fullWidth margin="normal">
                    <InputLabel id="defaultTimeFormat-label">{settings('defaultTimeFormat')}</InputLabel>
                    <Select
                      labelId="defaultTimeFormat-label"
                      id="defaultTimeFormat"
                      name="defaultTimeFormat"
                      value={generalForm.formik.values.defaultTimeFormat}
                      onChange={generalForm.formik.handleChange}
                      error={generalForm.formik.touched.defaultTimeFormat && Boolean(generalForm.formik.errors.defaultTimeFormat)}
                      label={settings('defaultTimeFormat')}
                    >
                      <MenuItem value="hh:mm a">12-hour (01:30 PM)</MenuItem>
                      <MenuItem value="HH:mm">24-hour (13:30)</MenuItem>
                      <MenuItem value="hh:mm:ss a">12-hour with seconds (01:30:00 PM)</MenuItem>
                      <MenuItem value="HH:mm:ss">24-hour with seconds (13:30:00)</MenuItem>
                    </Select>
                    {generalForm.formik.touched.defaultTimeFormat && generalForm.formik.errors.defaultTimeFormat && (
                      <FormHelperText error>{generalForm.formik.errors.defaultTimeFormat}</FormHelperText>
                    )}
                  </FormControl>
                </Grid>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    id="sessionTimeout"
                    name="sessionTimeout"
                    label={settings('sessionTimeout')}
                    type="number"
                    value={generalForm.formik.values.sessionTimeout}
                    onChange={generalForm.formik.handleChange}
                    error={generalForm.formik.touched.sessionTimeout && Boolean(generalForm.formik.errors.sessionTimeout)}
                    helperText={
                      (generalForm.formik.touched.sessionTimeout && generalForm.formik.errors.sessionTimeout) ||
                      settings('sessionTimeoutHelp')
                    }
                    margin="normal"
                    InputProps={{
                      endAdornment: <InputAdornment position="end">{settings('minutes')}</InputAdornment>,
                    }}
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={generalForm.formik.values.enableUserRegistration}
                        onChange={generalForm.formik.handleChange}
                        name="enableUserRegistration"
                        color="primary"
                      />
                    }
                    label={settings('enableUserRegistration')}
                    sx={{ mt: 2 }}
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={generalForm.formik.values.requireEmailVerification}
                        onChange={generalForm.formik.handleChange}
                        name="requireEmailVerification"
                        color="primary"
                      />
                    }
                    label={settings('requireEmailVerification')}
                    sx={{ mt: 2 }}
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={generalForm.formik.values.enableMaintenanceMode}
                        onChange={generalForm.formik.handleChange}
                        name="enableMaintenanceMode"
                        color="primary"
                      />
                    }
                    label={settings('enableMaintenanceMode')}
                    sx={{ mt: 2 }}
                  />
                </Grid>
                <Grid item xs={12}>
                  <Divider sx={{ my: 2 }} />
                  <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
                    <Button
                      variant="outlined"
                      startIcon={<RefreshIcon />}
                      onClick={() => generalForm.formik.resetForm()}
                    >
                      {common('reset')}
                    </Button>
                    <Button
                      type="submit"
                      variant="contained"
                      color="primary"
                      startIcon={<SaveIcon />}
                    >
                      {common('save')}
                    </Button>
                  </Box>
                </Grid>
              </Grid>
            </form>
          )}

          {/* Email Settings */}
          {tabValue === 1 && (
            <form onSubmit={emailForm.formik.handleSubmit}>
              <Grid container spacing={3}>
                <Grid item xs={12}>
                  <Typography variant="h6" gutterBottom>
                    {settings('emailSettings')}
                  </Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    id="smtpHost"
                    name="smtpHost"
                    label={settings('smtpHost')}
                    value={emailForm.formik.values.smtpHost}
                    onChange={emailForm.formik.handleChange}
                    error={emailForm.formik.touched.smtpHost && Boolean(emailForm.formik.errors.smtpHost)}
                    helperText={emailForm.formik.touched.smtpHost && emailForm.formik.errors.smtpHost}
                    margin="normal"
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    id="smtpPort"
                    name="smtpPort"
                    label={settings('smtpPort')}
                    type="number"
                    value={emailForm.formik.values.smtpPort}
                    onChange={emailForm.formik.handleChange}
                    error={emailForm.formik.touched.smtpPort && Boolean(emailForm.formik.errors.smtpPort)}
                    helperText={emailForm.formik.touched.smtpPort && emailForm.formik.errors.smtpPort}
                    margin="normal"
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    id="smtpUsername"
                    name="smtpUsername"
                    label={settings('smtpUsername')}
                    value={emailForm.formik.values.smtpUsername}
                    onChange={emailForm.formik.handleChange}
                    error={emailForm.formik.touched.smtpUsername && Boolean(emailForm.formik.errors.smtpUsername)}
                    helperText={emailForm.formik.touched.smtpUsername && emailForm.formik.errors.smtpUsername}
                    margin="normal"
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    id="smtpPassword"
                    name="smtpPassword"
                    label={settings('smtpPassword')}
                    type={showSmtpPassword ? 'text' : 'password'}
                    value={emailForm.formik.values.smtpPassword}
                    onChange={emailForm.formik.handleChange}
                    error={emailForm.formik.touched.smtpPassword && Boolean(emailForm.formik.errors.smtpPassword)}
                    helperText={emailForm.formik.touched.smtpPassword && emailForm.formik.errors.smtpPassword}
                    margin="normal"
                    InputProps={{
                      endAdornment: (
                        <InputAdornment position="end">
                          <IconButton
                            aria-label="toggle password visibility"
                            onClick={() => setShowSmtpPassword(!showSmtpPassword)}
                            edge="end"
                          >
                            {showSmtpPassword ? <VisibilityOffIcon /> : <VisibilityIcon />}
                          </IconButton>
                        </InputAdornment>
                      ),
                    }}
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    id="smtpFromEmail"
                    name="smtpFromEmail"
                    label={settings('smtpFromEmail')}
                    value={emailForm.formik.values.smtpFromEmail}
                    onChange={emailForm.formik.handleChange}
                    error={emailForm.formik.touched.smtpFromEmail && Boolean(emailForm.formik.errors.smtpFromEmail)}
                    helperText={emailForm.formik.touched.smtpFromEmail && emailForm.formik.errors.smtpFromEmail}
                    margin="normal"
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    id="smtpFromName"
                    name="smtpFromName"
                    label={settings('smtpFromName')}
                    value={emailForm.formik.values.smtpFromName}
                    onChange={emailForm.formik.handleChange}
                    error={emailForm.formik.touched.smtpFromName && Boolean(emailForm.formik.errors.smtpFromName)}
                    helperText={emailForm.formik.touched.smtpFromName && emailForm.formik.errors.smtpFromName}
                    margin="normal"
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={emailForm.formik.values.smtpSecure}
                        onChange={emailForm.formik.handleChange}
                        name="smtpSecure"
                        color="primary"
                      />
                    }
                    label={settings('smtpSecure')}
                    sx={{ mt: 2 }}
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={emailForm.formik.values.enableEmailNotifications}
                        onChange={emailForm.formik.handleChange}
                        name="enableEmailNotifications"
                        color="primary"
                      />
                    }
                    label={settings('enableEmailNotifications')}
                    sx={{ mt: 2 }}
                  />
                </Grid>
                <Grid item xs={12}>
                  <Divider sx={{ my: 2 }} />
                  <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
                    <Button
                      variant="outlined"
                      color="info"
                      onClick={handleTestEmail}
                    >
                      {settings('testEmail')}
                    </Button>
                    <Button
                      variant="outlined"
                      startIcon={<RefreshIcon />}
                      onClick={() => emailForm.formik.resetForm()}
                    >
                      {common('reset')}
                    </Button>
                    <Button
                      type="submit"
                      variant="contained"
                      color="primary"
                      startIcon={<SaveIcon />}
                    >
                      {common('save')}
                    </Button>
                  </Box>
                </Grid>
              </Grid>
            </form>
          )}

          {/* Storage Settings */}
          {tabValue === 2 && (
            <form onSubmit={storageForm.formik.handleSubmit}>
              <Grid container spacing={3}>
                <Grid item xs={12}>
                  <Typography variant="h6" gutterBottom>
                    {settings('storageSettings')}
                  </Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <FormControl fullWidth margin="normal">
                    <InputLabel id="storageProvider-label">{settings('storageProvider')}</InputLabel>
                    <Select
                      labelId="storageProvider-label"
                      id="storageProvider"
                      name="storageProvider"
                      value={storageForm.formik.values.storageProvider}
                      onChange={storageForm.formik.handleChange}
                      error={storageForm.formik.touched.storageProvider && Boolean(storageForm.formik.errors.storageProvider)}
                      label={settings('storageProvider')}
                    >
                      <MenuItem value="local">{settings('localStorage')}</MenuItem>
                      <MenuItem value="s3">{settings('amazonS3')}</MenuItem>
                      <MenuItem value="gcs">{settings('googleCloudStorage')}</MenuItem>
                      <MenuItem value="azure">{settings('azureBlobStorage')}</MenuItem>
                      <MenuItem value="other">{settings('otherS3Compatible')}</MenuItem>
                    </Select>
                    {storageForm.formik.touched.storageProvider && storageForm.formik.errors.storageProvider && (
                      <FormHelperText error>{storageForm.formik.errors.storageProvider}</FormHelperText>
                    )}
                  </FormControl>
                </Grid>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    id="maxUploadSize"
                    name="maxUploadSize"
                    label={settings('maxUploadSize')}
                    type="number"
                    value={storageForm.formik.values.maxUploadSize}
                    onChange={storageForm.formik.handleChange}
                    margin="normal"
                    InputProps={{
                      endAdornment: <InputAdornment position="end">MB</InputAdornment>,
                    }}
                  />
                </Grid>

                {storageForm.formik.values.storageProvider !== 'local' && (
                  <>
                    <Grid item xs={12} md={6}>
                      <TextField
                        fullWidth
                        id="bucketName"
                        name="bucketName"
                        label={settings('bucketName')}
                        value={storageForm.formik.values.bucketName}
                        onChange={storageForm.formik.handleChange}
                        error={storageForm.formik.touched.bucketName && Boolean(storageForm.formik.errors.bucketName)}
                        helperText={storageForm.formik.touched.bucketName && storageForm.formik.errors.bucketName}
                        margin="normal"
                      />
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <TextField
                        fullWidth
                        id="region"
                        name="region"
                        label={settings('region')}
                        value={storageForm.formik.values.region}
                        onChange={storageForm.formik.handleChange}
                        error={storageForm.formik.touched.region && Boolean(storageForm.formik.errors.region)}
                        helperText={storageForm.formik.touched.region && storageForm.formik.errors.region}
                        margin="normal"
                      />
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <TextField
                        fullWidth
                        id="accessKey"
                        name="accessKey"
                        label={settings('accessKey')}
                        type={showAccessKey ? 'text' : 'password'}
                        value={storageForm.formik.values.accessKey}
                        onChange={storageForm.formik.handleChange}
                        error={storageForm.formik.touched.accessKey && Boolean(storageForm.formik.errors.accessKey)}
                        helperText={storageForm.formik.touched.accessKey && storageForm.formik.errors.accessKey}
                        margin="normal"
                        InputProps={{
                          endAdornment: (
                            <InputAdornment position="end">
                              <IconButton
                                aria-label="toggle access key visibility"
                                onClick={() => setShowAccessKey(!showAccessKey)}
                                edge="end"
                              >
                                {showAccessKey ? <VisibilityOffIcon /> : <VisibilityIcon />}
                              </IconButton>
                            </InputAdornment>
                          ),
                        }}
                      />
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <TextField
                        fullWidth
                        id="secretKey"
                        name="secretKey"
                        label={settings('secretKey')}
                        type={showSecretKey ? 'text' : 'password'}
                        value={storageForm.formik.values.secretKey}
                        onChange={storageForm.formik.handleChange}
                        error={storageForm.formik.touched.secretKey && Boolean(storageForm.formik.errors.secretKey)}
                        helperText={storageForm.formik.touched.secretKey && storageForm.formik.errors.secretKey}
                        margin="normal"
                        InputProps={{
                          endAdornment: (
                            <InputAdornment position="end">
                              <IconButton
                                aria-label="toggle secret key visibility"
                                onClick={() => setShowSecretKey(!showSecretKey)}
                                edge="end"
                              >
                                {showSecretKey ? <VisibilityOffIcon /> : <VisibilityIcon />}
                              </IconButton>
                            </InputAdornment>
                          ),
                        }}
                      />
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <TextField
                        fullWidth
                        id="publicUrlPrefix"
                        name="publicUrlPrefix"
                        label={settings('publicUrlPrefix')}
                        value={storageForm.formik.values.publicUrlPrefix}
                        onChange={storageForm.formik.handleChange}
                        margin="normal"
                      />
                    </Grid>
                    {storageForm.formik.values.storageProvider === 'other' && (
                      <Grid item xs={12} md={6}>
                        <TextField
                          fullWidth
                          id="endpoint"
                          name="endpoint"
                          label={settings('endpoint')}
                          value={storageForm.formik.values.endpoint}
                          onChange={storageForm.formik.handleChange}
                          error={storageForm.formik.touched.endpoint && Boolean(storageForm.formik.errors.endpoint)}
                          helperText={storageForm.formik.touched.endpoint && storageForm.formik.errors.endpoint}
                          margin="normal"
                        />
                      </Grid>
                    )}
                  </>
                )}

                <Grid item xs={12}>
                  <Divider sx={{ my: 2 }} />
                  <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
                    <Button
                      variant="outlined"
                      startIcon={<RefreshIcon />}
                      onClick={() => storageForm.formik.resetForm()}
                    >
                      {common('reset')}
                    </Button>
                    <Button
                      type="submit"
                      variant="contained"
                      color="primary"
                      startIcon={<SaveIcon />}
                    >
                      {common('save')}
                    </Button>
                  </Box>
                </Grid>
              </Grid>
            </form>
          )}

          {/* Security Settings */}
          {tabValue === 3 && (
            <form onSubmit={securityForm.formik.handleSubmit}>
              <Grid container spacing={3}>
                <Grid item xs={12}>
                  <Typography variant="h6" gutterBottom>
                    {settings('securitySettings')}
                  </Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    id="passwordMinLength"
                    name="passwordMinLength"
                    label={settings('passwordMinLength')}
                    type="number"
                    value={securityForm.formik.values.passwordMinLength}
                    onChange={securityForm.formik.handleChange}
                    error={securityForm.formik.touched.passwordMinLength && Boolean(securityForm.formik.errors.passwordMinLength)}
                    helperText={securityForm.formik.touched.passwordMinLength && securityForm.formik.errors.passwordMinLength}
                    margin="normal"
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    id="passwordExpiryDays"
                    name="passwordExpiryDays"
                    label={settings('passwordExpiryDays')}
                    type="number"
                    value={securityForm.formik.values.passwordExpiryDays}
                    onChange={securityForm.formik.handleChange}
                    error={securityForm.formik.touched.passwordExpiryDays && Boolean(securityForm.formik.errors.passwordExpiryDays)}
                    helperText={
                      (securityForm.formik.touched.passwordExpiryDays && securityForm.formik.errors.passwordExpiryDays) ||
                      settings('passwordExpiryDaysHelp')
                    }
                    margin="normal"
                    InputProps={{
                      endAdornment: <InputAdornment position="end">{settings('days')}</InputAdornment>,
                    }}
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    id="maxLoginAttempts"
                    name="maxLoginAttempts"
                    label={settings('maxLoginAttempts')}
                    type="number"
                    value={securityForm.formik.values.maxLoginAttempts}
                    onChange={securityForm.formik.handleChange}
                    error={securityForm.formik.touched.maxLoginAttempts && Boolean(securityForm.formik.errors.maxLoginAttempts)}
                    helperText={securityForm.formik.touched.maxLoginAttempts && securityForm.formik.errors.maxLoginAttempts}
                    margin="normal"
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    id="jwtExpiryMinutes"
                    name="jwtExpiryMinutes"
                    label={settings('jwtExpiryMinutes')}
                    type="number"
                    value={securityForm.formik.values.jwtExpiryMinutes}
                    onChange={securityForm.formik.handleChange}
                    margin="normal"
                    InputProps={{
                      endAdornment: <InputAdornment position="end">{settings('minutes')}</InputAdornment>,
                    }}
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={securityForm.formik.values.passwordRequireUppercase}
                        onChange={securityForm.formik.handleChange}
                        name="passwordRequireUppercase"
                        color="primary"
                      />
                    }
                    label={settings('passwordRequireUppercase')}
                    sx={{ mt: 2 }}
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={securityForm.formik.values.passwordRequireLowercase}
                        onChange={securityForm.formik.handleChange}
                        name="passwordRequireLowercase"
                        color="primary"
                      />
                    }
                    label={settings('passwordRequireLowercase')}
                    sx={{ mt: 2 }}
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={securityForm.formik.values.passwordRequireNumbers}
                        onChange={securityForm.formik.handleChange}
                        name="passwordRequireNumbers"
                        color="primary"
                      />
                    }
                    label={settings('passwordRequireNumbers')}
                    sx={{ mt: 2 }}
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={securityForm.formik.values.passwordRequireSpecialChars}
                        onChange={securityForm.formik.handleChange}
                        name="passwordRequireSpecialChars"
                        color="primary"
                      />
                    }
                    label={settings('passwordRequireSpecialChars')}
                    sx={{ mt: 2 }}
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={securityForm.formik.values.twoFactorAuthEnabled}
                        onChange={securityForm.formik.handleChange}
                        name="twoFactorAuthEnabled"
                        color="primary"
                      />
                    }
                    label={settings('twoFactorAuthEnabled')}
                    sx={{ mt: 2 }}
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={securityForm.formik.values.twoFactorAuthRequired}
                        onChange={securityForm.formik.handleChange}
                        name="twoFactorAuthRequired"
                        color="primary"
                        disabled={!securityForm.formik.values.twoFactorAuthEnabled}
                      />
                    }
                    label={settings('twoFactorAuthRequired')}
                    sx={{ mt: 2 }}
                  />
                </Grid>
                <Grid item xs={12}>
                  <Divider sx={{ my: 2 }} />
                  <Typography variant="h6" gutterBottom>
                    {settings('maintenanceTools')}
                  </Typography>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Button
                    fullWidth
                    variant="outlined"
                    color="primary"
                    startIcon={<BackupIcon />}
                    onClick={handleDatabaseBackup}
                  >
                    {settings('databaseBackup')}
                  </Button>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Button
                    fullWidth
                    variant="outlined"
                    color="warning"
                    startIcon={<RestoreIcon />}
                    onClick={handleDatabaseRestore}
                  >
                    {settings('databaseRestore')}
                  </Button>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Button
                    fullWidth
                    variant="outlined"
                    color="error"
                    startIcon={<DeleteIcon />}
                    onClick={handleClearCache}
                  >
                    {settings('clearCache')}
                  </Button>
                </Grid>
                <Grid item xs={12}>
                  <Divider sx={{ my: 2 }} />
                  <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
                    <Button
                      variant="outlined"
                      startIcon={<RefreshIcon />}
                      onClick={() => securityForm.formik.resetForm()}
                    >
                      {common('reset')}
                    </Button>
                    <Button
                      type="submit"
                      variant="contained"
                      color="primary"
                      startIcon={<SaveIcon />}
                    >
                      {common('save')}
                    </Button>
                  </Box>
                </Grid>
              </Grid>
            </form>
          )}
        </CardContent>
      </Card>

      {/* Snackbar for notifications */}
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={6000}
        onClose={handleSnackbarClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert
          onClose={handleSnackbarClose}
          severity={snackbarSeverity}
          variant="filled"
          sx={{ width: '100%' }}
        >
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default SystemSettings;