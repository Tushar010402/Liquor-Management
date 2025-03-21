import React, { useState } from 'react';
import {
  AppBar,
  Toolbar,
  IconButton,
  Typography,
  Badge,
  Menu,
  MenuItem,
  Box,
  Avatar,
  Tooltip,
  Divider,
  ListItemIcon,
  useTheme,
  useMediaQuery,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Notifications as NotificationsIcon,
  AccountCircle,
  Settings as SettingsIcon,
  Logout as LogoutIcon,
  Person as PersonIcon,
  Store as StoreIcon,
  Help as HelpIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import useAuth from '../../hooks/useAuth';

interface HeaderProps {
  onSidebarToggle: () => void;
}

const Header: React.FC<HeaderProps> = ({ onSidebarToggle }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const [anchorElUser, setAnchorElUser] = useState<null | HTMLElement>(null);
  const [anchorElNotifications, setAnchorElNotifications] = useState<null | HTMLElement>(null);
  const [anchorElShops, setAnchorElShops] = useState<null | HTMLElement>(null);

  const handleOpenUserMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
  };

  const handleOpenNotificationsMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElNotifications(event.currentTarget);
  };

  const handleCloseNotificationsMenu = () => {
    setAnchorElNotifications(null);
  };

  const handleOpenShopsMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElShops(event.currentTarget);
  };

  const handleCloseShopsMenu = () => {
    setAnchorElShops(null);
  };

  const handleLogout = () => {
    handleCloseUserMenu();
    logout();
  };

  const handleProfile = () => {
    handleCloseUserMenu();
    // Navigate to common profile page
    navigate('/profile');
  };

  const handleSettings = () => {
    handleCloseUserMenu();

    // Navigate to settings based on user role
    if (user) {
      switch (user.role) {
        case 'saas_admin':
          navigate('/saas-admin/settings');
          break;
        case 'tenant_admin':
          navigate('/tenant-admin/settings');
          break;
        case 'shop_manager':
          navigate('/shop-manager/settings');
          break;
        case 'assistant_manager':
          navigate('/assistant-manager/settings');
          break;
        case 'executive':
          navigate('/executive/settings');
          break;
        default:
          navigate('/settings');
      }
    }
  };

  const handleHelp = () => {
    handleCloseUserMenu();
    navigate('/help');
  };

  const handleViewAllNotifications = () => {
    handleCloseNotificationsMenu();
    navigate('/notifications');
  };

  const handleShopSelect = (shopId: string) => {
    handleCloseShopsMenu();
    // In a real app, you would update the current shop in context
    console.log(`Selected shop: ${shopId}`);
  };

  // Mock notifications
  const notifications = [
    { id: 1, message: 'New sale requires approval', unread: true },
    { id: 2, message: 'Stock level below threshold', unread: true },
    { id: 3, message: 'Purchase order received', unread: false },
    { id: 4, message: 'Daily summary generated', unread: false },
  ];

  const unreadCount = notifications.filter(n => n.unread).length;

  return (
    <AppBar
      position="fixed"
      sx={{
        zIndex: theme.zIndex.drawer + 1,
        backgroundColor: 'background.paper',
        color: 'text.primary',
      }}
      elevation={0}
    >
      <Toolbar>
        {isMobile && (
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={onSidebarToggle}
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
        )}

        <Typography
          variant="h6"
          noWrap
          component="div"
          sx={{ display: { xs: 'none', sm: 'block' }, fontWeight: 600 }}
        >
          {user?.role === 'saas_admin' && 'SaaS Admin Portal'}
          {user?.role === 'tenant_admin' && 'Tenant Admin Portal'}
          {user?.role === 'shop_manager' && 'Shop Manager Portal'}
          {user?.role === 'assistant_manager' && 'Assistant Manager Portal'}
          {user?.role === 'executive' && 'Executive Portal'}
        </Typography>

        <Box sx={{ flexGrow: 1 }} />

        {/* Shop selector for roles that can access multiple shops */}
        {user && ['shop_manager', 'assistant_manager', 'executive'].includes(user.role) && user.assigned_shops && user.assigned_shops.length > 0 && (
          <Box sx={{ ml: 2 }}>
            <Tooltip title="Select shop">
              <IconButton
                onClick={handleOpenShopsMenu}
                sx={{
                  p: 1,
                  border: '1px solid',
                  borderColor: 'divider',
                  borderRadius: 1,
                  mr: 1,
                }}
              >
                <StoreIcon sx={{ mr: 1 }} />
                <Typography variant="body2" sx={{ mr: 1 }}>
                  {user.assigned_shops[0].name}
                </Typography>
              </IconButton>
            </Tooltip>
            <Menu
              sx={{ mt: '45px' }}
              id="menu-shops"
              anchorEl={anchorElShops}
              anchorOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              open={Boolean(anchorElShops)}
              onClose={handleCloseShopsMenu}
            >
              {user.assigned_shops.map((shop) => (
                <MenuItem key={shop.id} onClick={() => handleShopSelect(shop.id)}>
                  <ListItemIcon>
                    <StoreIcon fontSize="small" />
                  </ListItemIcon>
                  <Typography textAlign="center">{shop.name}</Typography>
                </MenuItem>
              ))}
            </Menu>
          </Box>
        )}

        {/* Notifications */}
        <Box sx={{ ml: 2 }}>
          <Tooltip title="Show notifications">
            <IconButton
              size="large"
              aria-label="show new notifications"
              color="inherit"
              onClick={handleOpenNotificationsMenu}
            >
              <Badge badgeContent={unreadCount} color="error">
                <NotificationsIcon />
              </Badge>
            </IconButton>
          </Tooltip>
          <Menu
            sx={{ mt: '45px' }}
            id="menu-notifications"
            anchorEl={anchorElNotifications}
            anchorOrigin={{
              vertical: 'top',
              horizontal: 'right',
            }}
            keepMounted
            transformOrigin={{
              vertical: 'top',
              horizontal: 'right',
            }}
            open={Boolean(anchorElNotifications)}
            onClose={handleCloseNotificationsMenu}
          >
            {notifications.length > 0 ? (
              notifications.map((notification) => (
                <MenuItem
                  key={notification.id}
                  onClick={handleCloseNotificationsMenu}
                  sx={{
                    backgroundColor: notification.unread ? 'rgba(94, 53, 177, 0.08)' : 'inherit',
                    '&:hover': {
                      backgroundColor: notification.unread ? 'rgba(94, 53, 177, 0.12)' : 'rgba(0, 0, 0, 0.04)',
                    },
                  }}
                >
                  <Typography variant="body2">{notification.message}</Typography>
                </MenuItem>
              ))
            ) : (
              <MenuItem onClick={handleCloseNotificationsMenu}>
                <Typography variant="body2">No notifications</Typography>
              </MenuItem>
            )}
            <Divider />
            <MenuItem onClick={handleViewAllNotifications}>
              <Typography variant="body2" color="primary">View all notifications</Typography>
            </MenuItem>
          </Menu>
        </Box>

        {/* User menu */}
        <Box sx={{ ml: 2 }}>
          <Tooltip title="Open settings">
            <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
              <Avatar alt={user?.full_name || 'User'} src="/static/images/avatar/2.jpg" />
            </IconButton>
          </Tooltip>
          <Menu
            sx={{ mt: '45px' }}
            id="menu-appbar"
            anchorEl={anchorElUser}
            anchorOrigin={{
              vertical: 'top',
              horizontal: 'right',
            }}
            keepMounted
            transformOrigin={{
              vertical: 'top',
              horizontal: 'right',
            }}
            open={Boolean(anchorElUser)}
            onClose={handleCloseUserMenu}
          >
            <MenuItem onClick={handleCloseUserMenu}>
              <Box sx={{ py: 0.5 }}>
                <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                  {user?.full_name}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  {user?.email}
                </Typography>
              </Box>
            </MenuItem>
            <Divider />
            <MenuItem onClick={handleProfile}>
              <ListItemIcon>
                <PersonIcon fontSize="small" />
              </ListItemIcon>
              <Typography textAlign="center">Profile</Typography>
            </MenuItem>
            <MenuItem onClick={handleSettings}>
              <ListItemIcon>
                <SettingsIcon fontSize="small" />
              </ListItemIcon>
              <Typography textAlign="center">Settings</Typography>
            </MenuItem>
            <MenuItem onClick={handleHelp}>
              <ListItemIcon>
                <HelpIcon fontSize="small" />
              </ListItemIcon>
              <Typography textAlign="center">Help</Typography>
            </MenuItem>
            <Divider />
            <MenuItem onClick={handleLogout}>
              <ListItemIcon>
                <LogoutIcon fontSize="small" color="error" />
              </ListItemIcon>
              <Typography textAlign="center" color="error">Logout</Typography>
            </MenuItem>
          </Menu>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;