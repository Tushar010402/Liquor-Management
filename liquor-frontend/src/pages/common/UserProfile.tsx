import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Avatar,
  Divider,
  IconButton,
  InputAdornment,
  FormControl,
  FormHelperText,
  Alert,
  CircularProgress,
  Paper,
  Tabs,
  Tab,
  Chip,
} from '@mui/material';
import {
  Person as PersonIcon,
  Edit as EditIcon,
  Save as SaveIcon,
  Visibility as VisibilityIcon,
  VisibilityOff as VisibilityOffIcon,
  Lock as LockIcon,
  History as HistoryIcon,
  Notifications as NotificationsIcon,
} from '@mui/icons-material';
import { PageHeader } from '../../components/common';
import { useAuth, useFormValidation, useNotification } from '../../hooks';
import { userService, User, ChangePasswordRequest } from '../../services/api';
import * as Yup from 'yup';
import { stringUtils } from '../../utils';

// Validation schema for profile form
const profileValidationSchema = Yup.object({
  first_name: Yup.string().required('First name is required'),
  last_name: Yup.string().required('Last name is required'),
  email: Yup.string().email('Invalid email address').required('Email is required'),
  phone: Yup.string().nullable(),
});

// Validation schema for password change form
const passwordValidationSchema = Yup.object({
  current_password: Yup.string().required('Current password is required'),
  new_password: Yup.string()
    .min(8, 'Password must be at least 8 characters')
    .matches(
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/,
      'Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character'
    )
    .required('New password is required'),
  confirm_password: Yup.string()
    .oneOf([Yup.ref('new_password')], 'Passwords must match')
    .required('Confirm password is required'),
});

/**
 * User Profile component
 */
const UserProfile: React.FC = () => {
  const { user, updateUserInContext } = useAuth();
  const { showNotification } = useNotification();
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [tabValue, setTabValue] = useState(0);
  const [showCurrentPassword, setShowCurrentPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [userProfile, setUserProfile] = useState<User | null>(null);
  const [editMode, setEditMode] = useState(false);

  // Fetch user profile
  useEffect(() => {
    const fetchUserProfile = async () => {
      if (!user) return;
      
      setIsLoading(true);
      setError(null);
      
      try {
        if (process.env.NODE_ENV === 'production') {
          const profileData = await userService.getProfile();
          setUserProfile(profileData);
        } else {
          // For development/demo purposes
          await new Promise(resolve => setTimeout(resolve, 1000));
          
          // Use the user from context as mock data
          setUserProfile(user);
        }
      } catch (err: any) {
        console.error('Error fetching user profile:', err);
        setError(err.message || 'Failed to fetch user profile');
        showNotification({
          message: 'Failed to fetch user profile. Please try again later.',
          variant: 'error',
        });
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchUserProfile();
  }, [user, showNotification]);

  // Profile form validation
  const profileFormik = useFormValidation({
    initialValues: {
      first_name: userProfile?.first_name || '',
      last_name: userProfile?.last_name || '',
      email: userProfile?.email || '',
      phone: userProfile?.phone || '',
    },
    validationSchema: profileValidationSchema,
    onSubmit: async (values) => {
      if (!userProfile) return;
      
      setIsSubmitting(true);
      
      try {
        if (process.env.NODE_ENV === 'production') {
          const updatedProfile = await userService.updateProfile({
            first_name: values.first_name,
            last_name: values.last_name,
            email: values.email,
            phone: values.phone || undefined,
          });
          
          setUserProfile(updatedProfile);
          updateUserInContext(updatedProfile);
        } else {
          // For development/demo purposes
          await new Promise(resolve => setTimeout(resolve, 1000));
          
          // Update user profile in state
          const updatedProfile = {
            ...userProfile,
            first_name: values.first_name,
            last_name: values.last_name,
            email: values.email,
            phone: values.phone,
          };
          
          setUserProfile(updatedProfile);
          updateUserInContext(updatedProfile);
        }
        
        showNotification({
          message: 'Profile updated successfully',
          variant: 'success',
        });
        
        setEditMode(false);
      } catch (err: any) {
        console.error('Error updating profile:', err);
        showNotification({
          message: err.message || 'Failed to update profile',
          variant: 'error',
        });
      } finally {
        setIsSubmitting(false);
      }
    },
    enableReinitialize: true,
  });

  // Password form validation
  const passwordFormik = useFormValidation({
    initialValues: {
      current_password: '',
      new_password: '',
      confirm_password: '',
    },
    validationSchema: passwordValidationSchema,
    onSubmit: async (values) => {
      if (!userProfile) return;
      
      setIsSubmitting(true);
      
      try {
        if (process.env.NODE_ENV === 'production') {
          await userService.changePassword(userProfile.id, {
            current_password: values.current_password,
            new_password: values.new_password,
            confirm_password: values.confirm_password,
          });
        } else {
          // For development/demo purposes
          await new Promise(resolve => setTimeout(resolve, 1000));
        }
        
        showNotification({
          message: 'Password changed successfully',
          variant: 'success',
        });
        
        // Reset form
        passwordFormik.resetForm();
      } catch (err: any) {
        console.error('Error changing password:', err);
        showNotification({
          message: err.message || 'Failed to change password',
          variant: 'error',
        });
      } finally {
        setIsSubmitting(false);
      }
    },
  });

  // Handle tab change
  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  // Toggle edit mode
  const handleToggleEditMode = () => {
    if (editMode) {
      // Cancel edit mode
      profileFormik.resetForm();
      setEditMode(false);
    } else {
      // Enter edit mode
      setEditMode(true);
    }
  };

  // Get role display name
  const getRoleDisplayName = (role: string) => {
    switch (role) {
      case 'saas_admin':
        return 'SaaS Admin';
      case 'tenant_admin':
        return 'Tenant Admin';
      case 'shop_manager':
        return 'Shop Manager';
      case 'assistant_manager':
        return 'Assistant Manager';
      case 'executive':
        return 'Executive';
      default:
        return role;
    }
  };

  return (
    <Container maxWidth="lg">
      <PageHeader
        title="My Profile"
        subtitle="View and manage your profile information"
        icon={<PersonIcon fontSize="large" />}
      />

      {error && (
        <Alert 
          severity="error" 
          sx={{ mb: 3 }}
          action={
            <Button color="inherit" size="small" onClick={() => window.location.reload()}>
              Retry
            </Button>
          }
        >
          {error}
        </Alert>
      )}

      {isLoading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', py: 5 }}>
          <CircularProgress size={40} />
          <Typography variant="h6" sx={{ ml: 2 }}>
            Loading profile...
          </Typography>
        </Box>
      ) : userProfile ? (
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent sx={{ textAlign: 'center', py: 4 }}>
                <Avatar
                  sx={{
                    width: 100,
                    height: 100,
                    mx: 'auto',
                    mb: 2,
                    fontSize: 40,
                    bgcolor: 'primary.main',
                  }}
                >
                  {stringUtils.getInitials(`${userProfile.first_name} ${userProfile.last_name}`)}
                </Avatar>
                <Typography variant="h5" gutterBottom>
                  {userProfile.first_name} {userProfile.last_name}
                </Typography>
                <Typography variant="body1" color="textSecondary" gutterBottom>
                  {userProfile.email}
                </Typography>
                <Chip
                  label={getRoleDisplayName(userProfile.role)}
                  color="primary"
                  sx={{ mt: 1 }}
                />
                {userProfile.tenant_id && (
                  <Typography variant="body2" color="textSecondary" sx={{ mt: 2 }}>
                    Tenant: {userProfile.tenant_id}
                  </Typography>
                )}
                {userProfile.assigned_shops && userProfile.assigned_shops.length > 0 && (
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="body2" color="textSecondary">
                      Assigned Shops:
                    </Typography>
                    {userProfile.assigned_shops.map((shop) => (
                      <Chip
                        key={shop.id}
                        label={shop.name}
                        size="small"
                        sx={{ m: 0.5 }}
                      />
                    ))}
                  </Box>
                )}
              </CardContent>
            </Card>

            <Card sx={{ mt: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Account Information
                </Typography>
                <Divider sx={{ my: 1 }} />
                <Box sx={{ py: 1 }}>
                  <Typography variant="body2" color="textSecondary">
                    Username
                  </Typography>
                  <Typography variant="body1">
                    {userProfile.username}
                  </Typography>
                </Box>
                <Divider sx={{ my: 1 }} />
                <Box sx={{ py: 1 }}>
                  <Typography variant="body2" color="textSecondary">
                    Status
                  </Typography>
                  <Chip
                    label={userProfile.status === 'active' ? 'Active' : 'Inactive'}
                    color={userProfile.status === 'active' ? 'success' : 'error'}
                    size="small"
                    sx={{ mt: 0.5 }}
                  />
                </Box>
                <Divider sx={{ my: 1 }} />
                <Box sx={{ py: 1 }}>
                  <Typography variant="body2" color="textSecondary">
                    Last Login
                  </Typography>
                  <Typography variant="body1">
                    {userProfile.last_login ? new Date(userProfile.last_login).toLocaleString() : 'Never'}
                  </Typography>
                </Box>
                <Divider sx={{ my: 1 }} />
                <Box sx={{ py: 1 }}>
                  <Typography variant="body2" color="textSecondary">
                    Account Created
                  </Typography>
                  <Typography variant="body1">
                    {new Date(userProfile.created_at).toLocaleDateString()}
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={8}>
            <Paper sx={{ mb: 3 }}>
              <Tabs
                value={tabValue}
                onChange={handleTabChange}
                indicatorColor="primary"
                textColor="primary"
                variant="fullWidth"
              >
                <Tab icon={<PersonIcon />} label="Personal Info" />
                <Tab icon={<LockIcon />} label="Security" />
                <Tab icon={<HistoryIcon />} label="Activity" />
                <Tab icon={<NotificationsIcon />} label="Notifications" />
              </Tabs>
            </Paper>

            {tabValue === 0 && (
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                    <Typography variant="h6">Personal Information</Typography>
                    <Button
                      startIcon={editMode ? <SaveIcon /> : <EditIcon />}
                      variant={editMode ? 'contained' : 'outlined'}
                      color={editMode ? 'primary' : 'secondary'}
                      onClick={editMode ? profileFormik.submitForm : handleToggleEditMode}
                      disabled={isSubmitting}
                    >
                      {editMode ? 'Save Changes' : 'Edit Profile'}
                    </Button>
                  </Box>

                  <form onSubmit={profileFormik.handleSubmit}>
                    <Grid container spacing={2}>
                      <Grid item xs={12} sm={6}>
                        <TextField
                          fullWidth
                          id="first_name"
                          name="first_name"
                          label="First Name"
                          value={profileFormik.values.first_name}
                          onChange={profileFormik.handleChange}
                          error={profileFormik.touched.first_name && Boolean(profileFormik.errors.first_name)}
                          helperText={profileFormik.touched.first_name && profileFormik.errors.first_name}
                          margin="normal"
                          disabled={!editMode || isSubmitting}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <TextField
                          fullWidth
                          id="last_name"
                          name="last_name"
                          label="Last Name"
                          value={profileFormik.values.last_name}
                          onChange={profileFormik.handleChange}
                          error={profileFormik.touched.last_name && Boolean(profileFormik.errors.last_name)}
                          helperText={profileFormik.touched.last_name && profileFormik.errors.last_name}
                          margin="normal"
                          disabled={!editMode || isSubmitting}
                        />
                      </Grid>
                      <Grid item xs={12}>
                        <TextField
                          fullWidth
                          id="email"
                          name="email"
                          label="Email Address"
                          value={profileFormik.values.email}
                          onChange={profileFormik.handleChange}
                          error={profileFormik.touched.email && Boolean(profileFormik.errors.email)}
                          helperText={profileFormik.touched.email && profileFormik.errors.email}
                          margin="normal"
                          disabled={!editMode || isSubmitting}
                        />
                      </Grid>
                      <Grid item xs={12}>
                        <TextField
                          fullWidth
                          id="phone"
                          name="phone"
                          label="Phone Number"
                          value={profileFormik.values.phone}
                          onChange={profileFormik.handleChange}
                          error={profileFormik.touched.phone && Boolean(profileFormik.errors.phone)}
                          helperText={profileFormik.touched.phone && profileFormik.errors.phone}
                          margin="normal"
                          disabled={!editMode || isSubmitting}
                        />
                      </Grid>
                    </Grid>

                    {editMode && (
                      <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
                        <Button
                          variant="outlined"
                          color="secondary"
                          onClick={handleToggleEditMode}
                          disabled={isSubmitting}
                        >
                          Cancel
                        </Button>
                        <Button
                          type="submit"
                          variant="contained"
                          color="primary"
                          disabled={isSubmitting || !profileFormik.isValid || !profileFormik.dirty}
                          startIcon={isSubmitting ? <CircularProgress size={20} color="inherit" /> : null}
                        >
                          {isSubmitting ? 'Saving...' : 'Save Changes'}
                        </Button>
                      </Box>
                    )}
                  </form>
                </CardContent>
              </Card>
            )}

            {tabValue === 1 && (
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Change Password
                  </Typography>
                  <form onSubmit={passwordFormik.handleSubmit}>
                    <TextField
                      fullWidth
                      id="current_password"
                      name="current_password"
                      label="Current Password"
                      type={showCurrentPassword ? 'text' : 'password'}
                      value={passwordFormik.values.current_password}
                      onChange={passwordFormik.handleChange}
                      error={passwordFormik.touched.current_password && Boolean(passwordFormik.errors.current_password)}
                      helperText={passwordFormik.touched.current_password && passwordFormik.errors.current_password}
                      margin="normal"
                      disabled={isSubmitting}
                      InputProps={{
                        endAdornment: (
                          <InputAdornment position="end">
                            <IconButton
                              aria-label="toggle current password visibility"
                              onClick={() => setShowCurrentPassword(!showCurrentPassword)}
                              edge="end"
                              disabled={isSubmitting}
                            >
                              {showCurrentPassword ? <VisibilityOffIcon /> : <VisibilityIcon />}
                            </IconButton>
                          </InputAdornment>
                        ),
                      }}
                    />
                    <TextField
                      fullWidth
                      id="new_password"
                      name="new_password"
                      label="New Password"
                      type={showNewPassword ? 'text' : 'password'}
                      value={passwordFormik.values.new_password}
                      onChange={passwordFormik.handleChange}
                      error={passwordFormik.touched.new_password && Boolean(passwordFormik.errors.new_password)}
                      helperText={passwordFormik.touched.new_password && passwordFormik.errors.new_password}
                      margin="normal"
                      disabled={isSubmitting}
                      InputProps={{
                        endAdornment: (
                          <InputAdornment position="end">
                            <IconButton
                              aria-label="toggle new password visibility"
                              onClick={() => setShowNewPassword(!showNewPassword)}
                              edge="end"
                              disabled={isSubmitting}
                            >
                              {showNewPassword ? <VisibilityOffIcon /> : <VisibilityIcon />}
                            </IconButton>
                          </InputAdornment>
                        ),
                      }}
                    />
                    <TextField
                      fullWidth
                      id="confirm_password"
                      name="confirm_password"
                      label="Confirm New Password"
                      type={showConfirmPassword ? 'text' : 'password'}
                      value={passwordFormik.values.confirm_password}
                      onChange={passwordFormik.handleChange}
                      error={passwordFormik.touched.confirm_password && Boolean(passwordFormik.errors.confirm_password)}
                      helperText={passwordFormik.touched.confirm_password && passwordFormik.errors.confirm_password}
                      margin="normal"
                      disabled={isSubmitting}
                      InputProps={{
                        endAdornment: (
                          <InputAdornment position="end">
                            <IconButton
                              aria-label="toggle confirm password visibility"
                              onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                              edge="end"
                              disabled={isSubmitting}
                            >
                              {showConfirmPassword ? <VisibilityOffIcon /> : <VisibilityIcon />}
                            </IconButton>
                          </InputAdornment>
                        ),
                      }}
                    />
                    <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
                      <Button
                        type="submit"
                        variant="contained"
                        color="primary"
                        disabled={isSubmitting || !passwordFormik.isValid || !passwordFormik.dirty}
                        startIcon={isSubmitting ? <CircularProgress size={20} color="inherit" /> : null}
                      >
                        {isSubmitting ? 'Changing Password...' : 'Change Password'}
                      </Button>
                    </Box>
                  </form>
                </CardContent>
              </Card>
            )}

            {tabValue === 2 && (
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Recent Activity
                  </Typography>
                  <Alert severity="info" sx={{ mb: 2 }}>
                    This feature is coming soon. You will be able to see your recent activity here.
                  </Alert>
                  <Box sx={{ py: 5, textAlign: 'center' }}>
                    <HistoryIcon sx={{ fontSize: 60, color: 'text.secondary', mb: 2 }} />
                    <Typography variant="h6" color="textSecondary">
                      No activity to display
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Your recent activities will appear here
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            )}

            {tabValue === 3 && (
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Notification Settings
                  </Typography>
                  <Alert severity="info" sx={{ mb: 2 }}>
                    This feature is coming soon. You will be able to manage your notification settings here.
                  </Alert>
                  <Box sx={{ py: 5, textAlign: 'center' }}>
                    <NotificationsIcon sx={{ fontSize: 60, color: 'text.secondary', mb: 2 }} />
                    <Typography variant="h6" color="textSecondary">
                      Notification settings
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      You will be able to customize your notification preferences here
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            )}
          </Grid>
        </Grid>
      ) : (
        <Alert severity="warning">
          User profile not found. Please try again later.
        </Alert>
      )}
    </Container>
  );
};

export default UserProfile;