import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Avatar,
  Divider,
  Button,
  IconButton,
  Tabs,
  Tab,
  Badge,
  Chip,
  Switch,
  FormControlLabel,
  FormGroup,
  Alert,
  CircularProgress,
  Menu,
  MenuItem,
  useTheme,
} from '@mui/material';
import {
  Notifications as NotificationsIcon,
  Delete as DeleteIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
  Error as ErrorIcon,
  MoreVert as MoreVertIcon,
  Settings as SettingsIcon,
  FilterList as FilterListIcon,
  Refresh as RefreshIcon,
  NotificationsActive as NotificationsActiveIcon,
  NotificationsOff as NotificationsOffIcon,
} from '@mui/icons-material';
import { PageHeader } from '../../components/common';
import { useTranslations, useNotification } from '../../hooks';

// Mock notification types
type NotificationType = 'info' | 'success' | 'warning' | 'error';

// Mock notification interface
interface Notification {
  id: number;
  title: string;
  message: string;
  type: NotificationType;
  isRead: boolean;
  timestamp: string;
  category: string;
}

// Mock notifications data
const mockNotifications: Notification[] = [
  {
    id: 1,
    title: 'Low Stock Alert',
    message: 'Several products are running low on stock. Please check the inventory.',
    type: 'warning',
    isRead: false,
    timestamp: new Date(Date.now() - 1000 * 60 * 30).toISOString(), // 30 minutes ago
    category: 'inventory',
  },
  {
    id: 2,
    title: 'Sales Target Achieved',
    message: 'Congratulations! You have achieved your monthly sales target.',
    type: 'success',
    isRead: false,
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(), // 2 hours ago
    category: 'sales',
  },
  {
    id: 3,
    title: 'New Product Added',
    message: 'A new product "Premium Whiskey" has been added to the inventory.',
    type: 'info',
    isRead: true,
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 5).toISOString(), // 5 hours ago
    category: 'inventory',
  },
  {
    id: 4,
    title: 'Cash Deposit Required',
    message: 'Cash balance is exceeding the safe limit. Please make a deposit.',
    type: 'warning',
    isRead: true,
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 8).toISOString(), // 8 hours ago
    category: 'cash',
  },
  {
    id: 5,
    title: 'System Update',
    message: 'The system will be updated tonight at 2:00 AM. Please save your work before that time.',
    type: 'info',
    isRead: false,
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 12).toISOString(), // 12 hours ago
    category: 'system',
  },
  {
    id: 6,
    title: 'Payment Failed',
    message: 'A customer payment has failed. Transaction ID: TRX-12345.',
    type: 'error',
    isRead: false,
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(), // 1 day ago
    category: 'sales',
  },
  {
    id: 7,
    title: 'New Staff Added',
    message: 'A new staff member "John Doe" has been added to your shop.',
    type: 'info',
    isRead: true,
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 36).toISOString(), // 1.5 days ago
    category: 'staff',
  },
  {
    id: 8,
    title: 'Expiring Products',
    message: '5 products are approaching their expiry date. Please check the inventory.',
    type: 'warning',
    isRead: true,
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 48).toISOString(), // 2 days ago
    category: 'inventory',
  },
  {
    id: 9,
    title: 'Monthly Report Generated',
    message: 'The monthly sales report for last month is now available.',
    type: 'success',
    isRead: true,
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 72).toISOString(), // 3 days ago
    category: 'reports',
  },
  {
    id: 10,
    title: 'License Renewal',
    message: 'Your liquor license will expire in 30 days. Please renew it.',
    type: 'warning',
    isRead: true,
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 96).toISOString(), // 4 days ago
    category: 'admin',
  },
];

// Notification settings
const notificationSettings = [
  {
    category: 'Inventory',
    settings: [
      { name: 'Low Stock Alerts', enabled: true },
      { name: 'New Product Additions', enabled: true },
      { name: 'Expiry Alerts', enabled: true },
      { name: 'Price Changes', enabled: false },
    ],
  },
  {
    category: 'Sales',
    settings: [
      { name: 'New Sales', enabled: false },
      { name: 'Sales Targets', enabled: true },
      { name: 'Payment Issues', enabled: true },
      { name: 'Returns', enabled: true },
    ],
  },
  {
    category: 'Cash',
    settings: [
      { name: 'Cash Deposit Reminders', enabled: true },
      { name: 'Cash Discrepancies', enabled: true },
      { name: 'Daily Summary', enabled: false },
      { name: 'Expense Approvals', enabled: true },
    ],
  },
  {
    category: 'System',
    settings: [
      { name: 'System Updates', enabled: true },
      { name: 'Maintenance Alerts', enabled: true },
      { name: 'Security Alerts', enabled: true },
      { name: 'Data Backup', enabled: false },
    ],
  },
];

/**
 * Notifications Center component
 */
const NotificationsCenter: React.FC = () => {
  const { common } = useTranslations();
  const theme = useTheme();
  const { showNotification } = useNotification();
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [tabValue, setTabValue] = useState(0);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [selectedNotification, setSelectedNotification] = useState<Notification | null>(null);
  const [actionAnchorEl, setActionAnchorEl] = useState<{ [key: number]: HTMLElement | null }>({});
  const [filterAnchorEl, setFilterAnchorEl] = useState<null | HTMLElement>(null);
  const [categoryFilter, setCategoryFilter] = useState<string | null>(null);
  const [settings, setSettings] = useState(notificationSettings);

  // Fetch notifications
  useEffect(() => {
    const fetchNotifications = async () => {
      setIsLoading(true);
      setError(null);
      
      try {
        // In a real app, you would fetch notifications from an API
        await new Promise(resolve => setTimeout(resolve, 1000));
        setNotifications(mockNotifications);
      } catch (err: any) {
        console.error('Error fetching notifications:', err);
        setError(err.message || 'Failed to fetch notifications');
        showNotification({
          message: 'Failed to fetch notifications. Please try again later.',
          variant: 'error',
        });
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchNotifications();
  }, [showNotification]);

  // Handle tab change
  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  // Handle opening the action menu for a notification
  const handleActionClick = (event: React.MouseEvent<HTMLElement>, notificationId: number) => {
    setActionAnchorEl({ ...actionAnchorEl, [notificationId]: event.currentTarget });
  };

  // Handle closing the action menu for a notification
  const handleActionClose = (notificationId: number) => {
    setActionAnchorEl({ ...actionAnchorEl, [notificationId]: null });
  };

  // Handle opening the filter menu
  const handleFilterClick = (event: React.MouseEvent<HTMLElement>) => {
    setFilterAnchorEl(event.currentTarget);
  };

  // Handle closing the filter menu
  const handleFilterClose = () => {
    setFilterAnchorEl(null);
  };

  // Handle marking a notification as read
  const handleMarkAsRead = (notificationId: number) => {
    setNotifications(prevNotifications =>
      prevNotifications.map(notification =>
        notification.id === notificationId
          ? { ...notification, isRead: true }
          : notification
      )
    );
    handleActionClose(notificationId);
  };

  // Handle deleting a notification
  const handleDeleteNotification = (notificationId: number) => {
    setNotifications(prevNotifications =>
      prevNotifications.filter(notification => notification.id !== notificationId)
    );
    handleActionClose(notificationId);
  };

  // Handle marking all notifications as read
  const handleMarkAllAsRead = () => {
    setNotifications(prevNotifications =>
      prevNotifications.map(notification => ({ ...notification, isRead: true }))
    );
    showNotification({
      message: 'All notifications marked as read',
      variant: 'success',
    });
  };

  // Handle deleting all notifications
  const handleDeleteAllNotifications = () => {
    setNotifications([]);
    showNotification({
      message: 'All notifications deleted',
      variant: 'success',
    });
  };

  // Handle refreshing notifications
  const handleRefreshNotifications = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      // In a real app, you would fetch notifications from an API
      await new Promise(resolve => setTimeout(resolve, 1000));
      setNotifications(mockNotifications);
      showNotification({
        message: 'Notifications refreshed',
        variant: 'success',
      });
    } catch (err: any) {
      console.error('Error refreshing notifications:', err);
      setError(err.message || 'Failed to refresh notifications');
      showNotification({
        message: 'Failed to refresh notifications. Please try again later.',
        variant: 'error',
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Handle toggling a notification setting
  const handleToggleSetting = (categoryIndex: number, settingIndex: number) => {
    const newSettings = [...settings];
    newSettings[categoryIndex].settings[settingIndex].enabled = !newSettings[categoryIndex].settings[settingIndex].enabled;
    setSettings(newSettings);
  };

  // Get notification icon based on type
  const getNotificationIcon = (type: NotificationType) => {
    switch (type) {
      case 'info':
        return <InfoIcon sx={{ color: theme.palette.info.main }} />;
      case 'success':
        return <CheckCircleIcon sx={{ color: theme.palette.success.main }} />;
      case 'warning':
        return <WarningIcon sx={{ color: theme.palette.warning.main }} />;
      case 'error':
        return <ErrorIcon sx={{ color: theme.palette.error.main }} />;
      default:
        return <InfoIcon />;
    }
  };

  // Format timestamp
  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / (1000 * 60));
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
    
    if (diffMins < 60) {
      return `${diffMins} minute${diffMins !== 1 ? 's' : ''} ago`;
    } else if (diffHours < 24) {
      return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`;
    } else {
      return `${diffDays} day${diffDays !== 1 ? 's' : ''} ago`;
    }
  };

  // Filter notifications based on tab and category filter
  const filteredNotifications = notifications.filter(notification => {
    // Filter by tab (All, Unread, Read)
    const matchesTab = 
      tabValue === 0 || // All
      (tabValue === 1 && !notification.isRead) || // Unread
      (tabValue === 2 && notification.isRead); // Read
    
    // Filter by category
    const matchesCategory = !categoryFilter || notification.category === categoryFilter;
    
    return matchesTab && matchesCategory;
  });

  // Get unique categories from notifications
  const categories = Array.from(new Set(notifications.map(notification => notification.category)));

  return (
    <Container maxWidth="lg">
      <PageHeader
        title="Notifications"
        subtitle="View and manage your notifications"
        icon={<NotificationsIcon fontSize="large" />}
      />

      {error && (
        <Alert 
          severity="error" 
          sx={{ mb: 3 }}
          action={
            <Button color="inherit" size="small" onClick={handleRefreshNotifications}>
              Retry
            </Button>
          }
        >
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Card sx={{ mb: 3 }}>
            <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
              <Tabs
                value={tabValue}
                onChange={handleTabChange}
                indicatorColor="primary"
                textColor="primary"
                variant="fullWidth"
              >
                <Tab 
                  label={
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <Typography>All</Typography>
                      <Chip 
                        label={notifications.length} 
                        size="small" 
                        sx={{ ml: 1, height: 20, fontSize: '0.75rem' }}
                      />
                    </Box>
                  } 
                />
                <Tab 
                  label={
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <Typography>Unread</Typography>
                      <Badge 
                        badgeContent={notifications.filter(n => !n.isRead).length} 
                        color="error"
                        sx={{ ml: 1 }}
                      >
                        <Box />
                      </Badge>
                    </Box>
                  } 
                />
                <Tab 
                  label={
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <Typography>Read</Typography>
                      <Chip 
                        label={notifications.filter(n => n.isRead).length} 
                        size="small" 
                        sx={{ ml: 1, height: 20, fontSize: '0.75rem' }}
                      />
                    </Box>
                  } 
                />
              </Tabs>
            </Box>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <Button
                    variant="outlined"
                    startIcon={<FilterListIcon />}
                    onClick={handleFilterClick}
                    size="small"
                    disabled={isLoading || notifications.length === 0}
                    sx={{ mr: 1 }}
                  >
                    {categoryFilter || 'Filter'}
                  </Button>
                  <Menu
                    anchorEl={filterAnchorEl}
                    open={Boolean(filterAnchorEl)}
                    onClose={handleFilterClose}
                  >
                    <MenuItem
                      onClick={() => {
                        setCategoryFilter(null);
                        handleFilterClose();
                      }}
                      selected={categoryFilter === null}
                    >
                      All Categories
                    </MenuItem>
                    <Divider />
                    {categories.map((category) => (
                      <MenuItem
                        key={category}
                        onClick={() => {
                          setCategoryFilter(category);
                          handleFilterClose();
                        }}
                        selected={categoryFilter === category}
                      >
                        {category.charAt(0).toUpperCase() + category.slice(1)}
                      </MenuItem>
                    ))}
                  </Menu>
                  {categoryFilter && (
                    <Chip
                      label={`Category: ${categoryFilter}`}
                      onDelete={() => setCategoryFilter(null)}
                      size="small"
                    />
                  )}
                </Box>
                <Box>
                  <IconButton 
                    onClick={handleRefreshNotifications} 
                    disabled={isLoading}
                    size="small"
                    sx={{ mr: 1 }}
                  >
                    {isLoading ? <CircularProgress size={20} /> : <RefreshIcon />}
                  </IconButton>
                  <Button
                    variant="text"
                    size="small"
                    onClick={handleMarkAllAsRead}
                    disabled={isLoading || notifications.filter(n => !n.isRead).length === 0}
                    sx={{ mr: 1 }}
                  >
                    Mark All as Read
                  </Button>
                  <Button
                    variant="text"
                    color="error"
                    size="small"
                    onClick={handleDeleteAllNotifications}
                    disabled={isLoading || notifications.length === 0}
                  >
                    Clear All
                  </Button>
                </Box>
              </Box>

              {isLoading ? (
                <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', py: 5 }}>
                  <CircularProgress size={40} />
                  <Typography variant="body1" sx={{ ml: 2 }}>
                    Loading notifications...
                  </Typography>
                </Box>
              ) : filteredNotifications.length === 0 ? (
                <Box sx={{ textAlign: 'center', py: 5 }}>
                  <NotificationsOffIcon sx={{ fontSize: 60, color: 'text.secondary', mb: 2 }} />
                  <Typography variant="h6" color="textSecondary">
                    No notifications
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    {tabValue === 0
                      ? 'You don\'t have any notifications yet'
                      : tabValue === 1
                      ? 'You don\'t have any unread notifications'
                      : 'You don\'t have any read notifications'}
                  </Typography>
                </Box>
              ) : (
                <List>
                  {filteredNotifications.map((notification, index) => (
                    <React.Fragment key={notification.id}>
                      <ListItem
                        alignItems="flex-start"
                        sx={{
                          bgcolor: notification.isRead ? 'transparent' : 'action.hover',
                          borderRadius: 1,
                        }}
                        secondaryAction={
                          <IconButton
                            edge="end"
                            aria-label="actions"
                            onClick={(e) => handleActionClick(e, notification.id)}
                          >
                            <MoreVertIcon />
                          </IconButton>
                        }
                      >
                        <ListItemAvatar>
                          <Avatar sx={{ bgcolor: 'background.paper' }}>
                            {getNotificationIcon(notification.type)}
                          </Avatar>
                        </ListItemAvatar>
                        <ListItemText
                          primary={
                            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                              <Typography
                                variant="subtitle1"
                                sx={{ fontWeight: notification.isRead ? 'normal' : 'bold' }}
                              >
                                {notification.title}
                              </Typography>
                              {!notification.isRead && (
                                <Box
                                  sx={{
                                    width: 8,
                                    height: 8,
                                    borderRadius: '50%',
                                    bgcolor: 'primary.main',
                                    ml: 1,
                                  }}
                                />
                              )}
                            </Box>
                          }
                          secondary={
                            <React.Fragment>
                              <Typography
                                variant="body2"
                                color="textPrimary"
                                component="span"
                                sx={{ display: 'block', mb: 0.5 }}
                              >
                                {notification.message}
                              </Typography>
                              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                <Chip
                                  label={notification.category}
                                  size="small"
                                  sx={{ mr: 1, height: 20, fontSize: '0.7rem' }}
                                />
                                <Typography
                                  variant="caption"
                                  color="textSecondary"
                                  component="span"
                                >
                                  {formatTimestamp(notification.timestamp)}
                                </Typography>
                              </Box>
                            </React.Fragment>
                          }
                        />
                        <Menu
                          anchorEl={actionAnchorEl[notification.id]}
                          open={Boolean(actionAnchorEl[notification.id])}
                          onClose={() => handleActionClose(notification.id)}
                        >
                          {!notification.isRead && (
                            <MenuItem onClick={() => handleMarkAsRead(notification.id)}>
                              <CheckCircleIcon fontSize="small" sx={{ mr: 1 }} />
                              Mark as read
                            </MenuItem>
                          )}
                          <MenuItem onClick={() => handleDeleteNotification(notification.id)}>
                            <DeleteIcon fontSize="small" sx={{ mr: 1 }} />
                            Delete
                          </MenuItem>
                        </Menu>
                      </ListItem>
                      {index < filteredNotifications.length - 1 && <Divider variant="inset" component="li" />}
                    </React.Fragment>
                  ))}
                </List>
              )}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <SettingsIcon sx={{ mr: 1 }} />
                <Typography variant="h6">Notification Settings</Typography>
              </Box>
              <Typography variant="body2" color="textSecondary" paragraph>
                Configure which notifications you want to receive
              </Typography>
              
              {settings.map((category, categoryIndex) => (
                <Box key={categoryIndex} sx={{ mb: 3 }}>
                  <Typography variant="subtitle1" gutterBottom>
                    {category.category}
                  </Typography>
                  <FormGroup>
                    {category.settings.map((setting, settingIndex) => (
                      <FormControlLabel
                        key={settingIndex}
                        control={
                          <Switch
                            checked={setting.enabled}
                            onChange={() => handleToggleSetting(categoryIndex, settingIndex)}
                            size="small"
                          />
                        }
                        label={
                          <Typography variant="body2">
                            {setting.name}
                          </Typography>
                        }
                      />
                    ))}
                  </FormGroup>
                  {categoryIndex < settings.length - 1 && <Divider sx={{ my: 2 }} />}
                </Box>
              ))}
              
              <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 2 }}>
                <Button variant="contained" color="primary">
                  Save Settings
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
};

export default NotificationsCenter;