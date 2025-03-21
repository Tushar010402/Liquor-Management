import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Button,
  Card,
  CardContent,
  Grid,
  TextField,
  InputAdornment,
  IconButton,
  Chip,
  Menu,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  FormHelperText,
  Tabs,
  Tab,
  Divider,
  Avatar,
  useTheme,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  Search as SearchIcon,
  Add as AddIcon,
  FilterList as FilterListIcon,
  MoreVert as MoreVertIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Block as BlockIcon,
  CheckCircle as CheckCircleIcon,
  People as PeopleIcon,
  Visibility as VisibilityIcon,
  VisibilityOff as VisibilityOffIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';
import { DataTable, PageHeader } from '../../components/common';
import { useTranslations, useFormValidation, useGlobalConfirmDialog, useNotification } from '../../hooks';
import * as Yup from 'yup';
import { stringUtils } from '../../utils';
import { userService, tenantService, User, UserRole, UserStatus, CreateUserRequest, UpdateUserRequest, Tenant } from '../../services/api';

// Validation schema for user form
const userValidationSchema = Yup.object({
  first_name: Yup.string().required('First name is required'),
  last_name: Yup.string().required('Last name is required'),
  username: Yup.string().required('Username is required'),
  email: Yup.string().email('Invalid email address').required('Email is required'),
  phone: Yup.string().nullable(),
  role: Yup.string().required('Role is required'),
  password: Yup.string()
    .min(8, 'Password must be at least 8 characters')
    .matches(
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/,
      'Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character'
    )
    .required('Password is required'),
  confirmPassword: Yup.string()
    .oneOf([Yup.ref('password')], 'Passwords must match')
    .required('Confirm password is required'),
  tenant_id: Yup.number().when('role', {
    is: (role: string) => role === 'tenant_admin',
    then: Yup.number().required('Tenant is required for tenant admin'),
    otherwise: Yup.number().nullable(),
  }),
  shop_ids: Yup.array().when('role', {
    is: (role: string) => role === 'shop_manager' || role === 'assistant_manager' || role === 'executive',
    then: Yup.array().min(1, 'At least one shop must be selected'),
    otherwise: Yup.array().nullable(),
  }),
});

// Validation schema for editing a user (password is optional)
const userEditValidationSchema = Yup.object({
  first_name: Yup.string().required('First name is required'),
  last_name: Yup.string().required('Last name is required'),
  username: Yup.string().required('Username is required'),
  email: Yup.string().email('Invalid email address').required('Email is required'),
  phone: Yup.string().nullable(),
  role: Yup.string().required('Role is required'),
  password: Yup.string()
    .nullable()
    .transform((value) => (value === '' ? null : value))
    .test(
      'password-validation',
      'Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character',
      (value) => {
        if (!value) return true; // Skip validation if password is empty
        return /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/.test(value);
      }
    ),
  confirmPassword: Yup.string().when('password', {
    is: (val: string | null) => val && val.length > 0,
    then: Yup.string()
      .oneOf([Yup.ref('password')], 'Passwords must match')
      .required('Confirm password is required'),
    otherwise: Yup.string().nullable(),
  }),
  tenant_id: Yup.number().when('role', {
    is: (role: string) => role === 'tenant_admin',
    then: Yup.number().required('Tenant is required for tenant admin'),
    otherwise: Yup.number().nullable(),
  }),
  shop_ids: Yup.array().when('role', {
    is: (role: string) => role === 'shop_manager' || role === 'assistant_manager' || role === 'executive',
    then: Yup.array().min(1, 'At least one shop must be selected'),
    otherwise: Yup.array().nullable(),
  }),
});

/**
 * Users Management component for SaaS Admin
 */
const UsersManagement: React.FC = () => {
  const { common, users, roles } = useTranslations();
  const theme = useTheme();
  const { confirm } = useGlobalConfirmDialog();
  const { showNotification } = useNotification();
  
  // State for users and loading
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [usersList, setUsersList] = useState<User[]>([]);
  const [tenantsList, setTenantsList] = useState<Tenant[]>([]);
  
  // UI state
  const [searchQuery, setSearchQuery] = useState('');
  const [filterAnchorEl, setFilterAnchorEl] = useState<null | HTMLElement>(null);
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [roleFilter, setRoleFilter] = useState<string>('all');
  const [openUserDialog, setOpenUserDialog] = useState(false);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [actionAnchorEl, setActionAnchorEl] = useState<{ [key: number]: HTMLElement | null }>({});
  const [tabValue, setTabValue] = useState(0);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  // Fetch users and tenants
  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      setError(null);
      
      try {
        if (process.env.NODE_ENV === 'production') {
          // Fetch users
          const usersData = await userService.getUsers();
          setUsersList(usersData);
          
          // Fetch tenants
          const tenantsData = await tenantService.getTenants();
          setTenantsList(tenantsData);
        } else {
          // For development/demo purposes
          await new Promise(resolve => setTimeout(resolve, 1000));
          
          // Mock users
          setUsersList([
            {
              id: 1,
              username: 'johndoe',
              email: 'john.doe@example.com',
              first_name: 'John',
              last_name: 'Doe',
              role: 'saas_admin',
              status: 'active',
              tenant_id: undefined,
              created_at: '2023-01-10T00:00:00Z',
              updated_at: '2023-01-10T00:00:00Z',
              last_login: '2023-06-15T00:00:00Z',
            },
            {
              id: 2,
              username: 'janesmith',
              email: 'jane.smith@example.com',
              first_name: 'Jane',
              last_name: 'Smith',
              role: 'saas_admin',
              status: 'active',
              tenant_id: undefined,
              created_at: '2023-02-15T00:00:00Z',
              updated_at: '2023-02-15T00:00:00Z',
              last_login: '2023-06-10T00:00:00Z',
            },
            {
              id: 3,
              username: 'robertjohnson',
              email: 'robert.johnson@abcliquors.com',
              first_name: 'Robert',
              last_name: 'Johnson',
              role: 'tenant_admin',
              status: 'active',
              tenant_id: 1,
              created_at: '2023-01-20T00:00:00Z',
              updated_at: '2023-01-20T00:00:00Z',
              last_login: '2023-06-12T00:00:00Z',
            },
            {
              id: 4,
              username: 'emilydavis',
              email: 'emily.davis@xyzwines.com',
              first_name: 'Emily',
              last_name: 'Davis',
              role: 'tenant_admin',
              status: 'active',
              tenant_id: 2,
              created_at: '2023-02-25T00:00:00Z',
              updated_at: '2023-02-25T00:00:00Z',
              last_login: '2023-06-14T00:00:00Z',
            },
            {
              id: 5,
              username: 'michaelwilson',
              email: 'michael.wilson@cityspirits.com',
              first_name: 'Michael',
              last_name: 'Wilson',
              role: 'tenant_admin',
              status: 'inactive',
              tenant_id: 3,
              created_at: '2023-03-05T00:00:00Z',
              updated_at: '2023-03-05T00:00:00Z',
              last_login: '2023-05-20T00:00:00Z',
            },
          ]);
          
          // Mock tenants
          setTenantsList([
            { id: 1, name: 'ABC Liquors', status: 'active', contact_email: 'contact@abcliquors.com', contact_phone: '1234567890', address: '123 Main St', city: 'New York', state: 'NY', zip: '10001', country: 'USA', created_at: '2023-01-01T00:00:00Z', updated_at: '2023-01-01T00:00:00Z' },
            { id: 2, name: 'XYZ Wines', status: 'active', contact_email: 'contact@xyzwines.com', contact_phone: '2345678901', address: '456 Oak St', city: 'Los Angeles', state: 'CA', zip: '90001', country: 'USA', created_at: '2023-01-02T00:00:00Z', updated_at: '2023-01-02T00:00:00Z' },
            { id: 3, name: 'City Spirits', status: 'active', contact_email: 'contact@cityspirits.com', contact_phone: '3456789012', address: '789 Pine St', city: 'Chicago', state: 'IL', zip: '60001', country: 'USA', created_at: '2023-01-03T00:00:00Z', updated_at: '2023-01-03T00:00:00Z' },
            { id: 4, name: 'Metro Beverages', status: 'active', contact_email: 'contact@metrobeverages.com', contact_phone: '4567890123', address: '101 Elm St', city: 'Houston', state: 'TX', zip: '70001', country: 'USA', created_at: '2023-01-04T00:00:00Z', updated_at: '2023-01-04T00:00:00Z' },
            { id: 5, name: 'Downtown Drinks', status: 'inactive', contact_email: 'contact@downtowndrinks.com', contact_phone: '5678901234', address: '202 Maple St', city: 'Phoenix', state: 'AZ', zip: '80001', country: 'USA', created_at: '2023-01-05T00:00:00Z', updated_at: '2023-01-05T00:00:00Z' },
          ]);
        }
      } catch (err: any) {
        console.error('Error fetching data:', err);
        setError(err.message || 'Failed to fetch data');
        showNotification({
          message: 'Failed to fetch data. Please try again later.',
          variant: 'error',
        });
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchData();
  }, [showNotification]);
  
  // Update tab value based on status filter
  useEffect(() => {
    if (statusFilter === 'all') {
      setTabValue(0);
    } else if (statusFilter === 'active') {
      setTabValue(1);
    } else if (statusFilter === 'inactive') {
      setTabValue(2);
    }
  }, [statusFilter]);

  // Form validation for user dialog
  const { formik } = useFormValidation({
    initialValues: {
      username: '',
      first_name: '',
      last_name: '',
      email: '',
      phone: '',
      role: 'saas_admin' as UserRole,
      password: '',
      confirmPassword: '',
      tenant_id: null as number | null,
      shop_ids: [] as number[],
    },
    validationSchema: selectedUser ? userEditValidationSchema : userValidationSchema,
    onSubmit: async (values) => {
      setIsSubmitting(true);
      
      try {
        if (selectedUser) {
          // Update existing user
          const updateData: UpdateUserRequest = {
            email: values.email,
            first_name: values.first_name,
            last_name: values.last_name,
            phone: values.phone || undefined,
            role: values.role,
            tenant_id: values.tenant_id || undefined,
            shop_ids: values.shop_ids.length > 0 ? values.shop_ids : undefined,
          };
          
          if (process.env.NODE_ENV === 'production') {
            await userService.updateUser(selectedUser.id, updateData);
            
            // If password is provided, change password
            if (values.password) {
              await userService.changePassword(selectedUser.id, {
                current_password: '', // Admin doesn't need to provide current password
                new_password: values.password,
                confirm_password: values.confirmPassword,
              });
            }
            
            // Refresh users list
            const usersData = await userService.getUsers();
            setUsersList(usersData);
          } else {
            // For development/demo purposes
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            // Update user in mock data
            setUsersList(prevUsers => 
              prevUsers.map(user => 
                user.id === selectedUser.id 
                  ? { 
                      ...user, 
                      username: values.username,
                      email: values.email,
                      first_name: values.first_name,
                      last_name: values.last_name,
                      role: values.role,
                      tenant_id: values.tenant_id || undefined,
                      updated_at: new Date().toISOString(),
                    } 
                  : user
              )
            );
          }
          
          showNotification({
            message: `User ${values.first_name} ${values.last_name} updated successfully`,
            variant: 'success',
          });
        } else {
          // Create new user
          const createData: CreateUserRequest = {
            username: values.username,
            email: values.email,
            password: values.password,
            first_name: values.first_name,
            last_name: values.last_name,
            phone: values.phone || undefined,
            role: values.role,
            tenant_id: values.tenant_id || undefined,
            shop_ids: values.shop_ids.length > 0 ? values.shop_ids : undefined,
          };
          
          if (process.env.NODE_ENV === 'production') {
            const newUser = await userService.createUser(createData);
            
            // Refresh users list
            const usersData = await userService.getUsers();
            setUsersList(usersData);
          } else {
            // For development/demo purposes
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            // Add user to mock data
            const newUser: User = {
              id: Math.max(...usersList.map(u => u.id)) + 1,
              username: values.username,
              email: values.email,
              first_name: values.first_name,
              last_name: values.last_name,
              phone: values.phone,
              role: values.role,
              status: 'active',
              tenant_id: values.tenant_id || undefined,
              created_at: new Date().toISOString(),
              updated_at: new Date().toISOString(),
            };
            
            setUsersList(prevUsers => [...prevUsers, newUser]);
          }
          
          showNotification({
            message: `User ${values.first_name} ${values.last_name} created successfully`,
            variant: 'success',
          });
        }
        
        handleCloseUserDialog();
      } catch (err: any) {
        console.error('Error saving user:', err);
        showNotification({
          message: err.message || 'Failed to save user',
          variant: 'error',
        });
      } finally {
        setIsSubmitting(false);
      }
    },
  });

  // Handle opening the filter menu
  const handleFilterClick = (event: React.MouseEvent<HTMLElement>) => {
    setFilterAnchorEl(event.currentTarget);
  };

  // Handle closing the filter menu
  const handleFilterClose = () => {
    setFilterAnchorEl(null);
  };

  // Handle opening the action menu for a user
  const handleActionClick = (event: React.MouseEvent<HTMLElement>, userId: number) => {
    setActionAnchorEl({ ...actionAnchorEl, [userId]: event.currentTarget });
  };

  // Handle closing the action menu for a user
  const handleActionClose = (userId: number) => {
    setActionAnchorEl({ ...actionAnchorEl, [userId]: null });
  };

  // Refresh users data
  const handleRefreshData = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      if (process.env.NODE_ENV === 'production') {
        // Fetch users
        const usersData = await userService.getUsers();
        setUsersList(usersData);
        
        // Fetch tenants
        const tenantsData = await tenantService.getTenants();
        setTenantsList(tenantsData);
      } else {
        // For development/demo purposes
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
      
      showNotification({
        message: 'Data refreshed successfully',
        variant: 'success',
      });
    } catch (err: any) {
      console.error('Error refreshing data:', err);
      setError(err.message || 'Failed to refresh data');
      showNotification({
        message: 'Failed to refresh data. Please try again later.',
        variant: 'error',
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Handle opening the user dialog for creating a new user
  const handleOpenCreateUserDialog = () => {
    setSelectedUser(null);
    formik.resetForm();
    setOpenUserDialog(true);
  };

  // Handle opening the user dialog for editing an existing user
  const handleOpenEditUserDialog = (user: User) => {
    setSelectedUser(user);
    formik.setValues({
      username: user.username,
      first_name: user.first_name,
      last_name: user.last_name,
      email: user.email,
      phone: user.phone || '',
      role: user.role,
      password: '',
      confirmPassword: '',
      tenant_id: user.tenant_id || null,
      shop_ids: user.assigned_shops ? user.assigned_shops.map(shop => parseInt(shop.id)) : [],
    });
    setOpenUserDialog(true);
    handleActionClose(user.id);
  };

  // Handle closing the user dialog
  const handleCloseUserDialog = () => {
    setOpenUserDialog(false);
    setShowPassword(false);
    setShowConfirmPassword(false);
  };

  // Handle deleting a user
  const handleDeleteUser = async (user: User) => {
    const confirmed = await confirm({
      title: users('deleteUser'),
      message: `${users('confirmDeleteUser')} "${user.first_name} ${user.last_name}"?`,
      confirmButtonColor: 'error',
      confirmText: common('delete'),
      cancelText: common('cancel'),
    });

    if (confirmed) {
      setIsLoading(true);
      
      try {
        if (process.env.NODE_ENV === 'production') {
          await userService.deleteUser(user.id);
          
          // Refresh users list
          const usersData = await userService.getUsers();
          setUsersList(usersData);
        } else {
          // For development/demo purposes
          await new Promise(resolve => setTimeout(resolve, 1000));
          
          // Remove user from mock data
          setUsersList(prevUsers => prevUsers.filter(u => u.id !== user.id));
        }
        
        showNotification({
          message: `User ${user.first_name} ${user.last_name} deleted successfully`,
          variant: 'success',
        });
      } catch (err: any) {
        console.error('Error deleting user:', err);
        showNotification({
          message: err.message || 'Failed to delete user',
          variant: 'error',
        });
      } finally {
        setIsLoading(false);
      }
    }

    handleActionClose(user.id);
  };

  // Handle changing the status of a user
  const handleToggleUserStatus = async (user: User) => {
    const newStatus = user.status === 'active' ? 'inactive' : 'active';
    const confirmed = await confirm({
      title: newStatus === 'active' ? users('activateUser') : users('deactivateUser'),
      message: newStatus === 'active'
        ? `${users('confirmActivateUser')} "${user.first_name} ${user.last_name}"?`
        : `${users('confirmDeactivateUser')} "${user.first_name} ${user.last_name}"?`,
      confirmButtonColor: newStatus === 'active' ? 'success' : 'warning',
      confirmText: newStatus === 'active' ? common('activate') : common('deactivate'),
      cancelText: common('cancel'),
    });

    if (confirmed) {
      setIsLoading(true);
      
      try {
        if (process.env.NODE_ENV === 'production') {
          await userService.updateUser(user.id, { status: newStatus as UserStatus });
          
          // Refresh users list
          const usersData = await userService.getUsers();
          setUsersList(usersData);
        } else {
          // For development/demo purposes
          await new Promise(resolve => setTimeout(resolve, 1000));
          
          // Update user status in mock data
          setUsersList(prevUsers => 
            prevUsers.map(u => 
              u.id === user.id 
                ? { ...u, status: newStatus as UserStatus } 
                : u
            )
          );
        }
        
        showNotification({
          message: `User ${user.first_name} ${user.last_name} ${newStatus === 'active' ? 'activated' : 'deactivated'} successfully`,
          variant: 'success',
        });
      } catch (err: any) {
        console.error('Error updating user status:', err);
        showNotification({
          message: err.message || 'Failed to update user status',
          variant: 'error',
        });
      } finally {
        setIsLoading(false);
      }
    }

    handleActionClose(user.id);
  };

  // Handle tab change
  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  // Filter users based on search query and filters
  const filteredUsers = usersList.filter((user) => {
    const fullName = `${user.first_name} ${user.last_name}`;
    const matchesSearch = 
      fullName.toLowerCase().includes(searchQuery.toLowerCase()) ||
      user.email.toLowerCase().includes(searchQuery.toLowerCase()) ||
      user.username.toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesStatus = statusFilter === 'all' || user.status === statusFilter;
    const matchesRole = roleFilter === 'all' || user.role === roleFilter;
    
    return matchesSearch && matchesStatus && matchesRole;
  });

  // Get tenant name by ID
  const getTenantName = (tenantId?: number) => {
    if (!tenantId) return null;
    const tenant = tenantsList.find(t => t.id === tenantId);
    return tenant ? tenant.name : null;
  };

  // Format date
  const formatDate = (dateString?: string) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString();
  };

  // Define columns for the data table
  const columns = [
    {
      field: 'name',
      headerName: common('name'),
      flex: 1,
      renderCell: (params: User) => (
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Avatar sx={{ mr: 2, bgcolor: theme.palette.primary.main }}>
            {stringUtils.getInitials(`${params.first_name} ${params.last_name}`)}
          </Avatar>
          <Box>
            <Typography variant="body1" fontWeight={500}>
              {params.first_name} {params.last_name}
            </Typography>
            <Typography variant="body2" color="textSecondary">
              {params.email}
            </Typography>
          </Box>
        </Box>
      ),
    },
    {
      field: 'role',
      headerName: users('role'),
      flex: 0.7,
      renderCell: (params: User) => (
        <Chip
          label={
            params.role === 'saas_admin'
              ? roles('saasAdmin')
              : params.role === 'tenant_admin'
              ? roles('tenantAdmin')
              : params.role === 'shop_manager'
              ? roles('shopManager')
              : params.role === 'assistant_manager'
              ? roles('assistantManager')
              : params.role === 'executive'
              ? roles('executive')
              : params.role
          }
          color={
            params.role === 'saas_admin'
              ? 'primary'
              : params.role === 'tenant_admin'
              ? 'secondary'
              : params.role === 'shop_manager'
              ? 'info'
              : params.role === 'assistant_manager'
              ? 'success'
              : 'default'
          }
          size="small"
          variant="outlined"
        />
      ),
    },
    {
      field: 'tenant',
      headerName: common('tenant'),
      flex: 0.7,
      renderCell: (params: User) => {
        const tenantName = getTenantName(params.tenant_id);
        return tenantName ? (
          <Typography variant="body2">{tenantName}</Typography>
        ) : (
          <Typography variant="body2" color="textSecondary">
            {common('none')}
          </Typography>
        );
      },
    },
    {
      field: 'status',
      headerName: common('status'),
      flex: 0.5,
      renderCell: (params: User) => (
        <Chip
          label={params.status === 'active' ? common('active') : common('inactive')}
          color={params.status === 'active' ? 'success' : 'error'}
          size="small"
        />
      ),
    },
    {
      field: 'created_at',
      headerName: users('createdAt'),
      flex: 0.7,
      renderCell: (params: User) => (
        <Typography variant="body2">{formatDate(params.created_at)}</Typography>
      ),
    },
    {
      field: 'last_login',
      headerName: users('lastLogin'),
      flex: 0.7,
      renderCell: (params: User) => (
        <Typography variant="body2">{formatDate(params.last_login)}</Typography>
      ),
    },
    {
      field: 'actions',
      headerName: common('actions'),
      flex: 0.5,
      renderCell: (params: User) => (
        <>
          <IconButton
            size="small"
            onClick={(e) => handleActionClick(e, params.id)}
            aria-label="actions"
            disabled={isLoading}
          >
            <MoreVertIcon fontSize="small" />
          </IconButton>
          <Menu
            anchorEl={actionAnchorEl[params.id]}
            open={Boolean(actionAnchorEl[params.id])}
            onClose={() => handleActionClose(params.id)}
          >
            <MenuItem onClick={() => handleOpenEditUserDialog(params)}>
              <EditIcon fontSize="small" sx={{ mr: 1 }} />
              {common('edit')}
            </MenuItem>
            <MenuItem
              onClick={() => handleToggleUserStatus(params)}
              sx={{ color: params.status === 'active' ? 'error.main' : 'success.main' }}
            >
              {params.status === 'active' ? (
                <>
                  <BlockIcon fontSize="small" sx={{ mr: 1 }} />
                  {common('deactivate')}
                </>
              ) : (
                <>
                  <CheckCircleIcon fontSize="small" sx={{ mr: 1 }} />
                  {common('activate')}
                </>
              )}
            </MenuItem>
            <MenuItem onClick={() => handleDeleteUser(params)} sx={{ color: 'error.main' }}>
              <DeleteIcon fontSize="small" sx={{ mr: 1 }} />
              {common('delete')}
            </MenuItem>
          </Menu>
        </>
      ),
    },
  ];

  return (
    <Container maxWidth="xl">
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <PageHeader
          title={users('users')}
          subtitle={users('manageUsers')}
          icon={<PeopleIcon fontSize="large" />}
        />
        <Button
          variant="outlined"
          startIcon={isLoading ? <CircularProgress size={20} /> : <RefreshIcon />}
          onClick={handleRefreshData}
          disabled={isLoading}
        >
          {isLoading ? common('loading') : common('refresh')}
        </Button>
      </Box>

      {error && (
        <Alert 
          severity="error" 
          sx={{ mb: 3 }}
          action={
            <Button color="inherit" size="small" onClick={handleRefreshData}>
              {common('retry')}
            </Button>
          }
        >
          {error}
        </Alert>
      )}

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Tabs
            value={tabValue}
            onChange={handleTabChange}
            indicatorColor="primary"
            textColor="primary"
            variant="fullWidth"
            aria-label="user tabs"
          >
            <Tab label={common('all')} />
            <Tab label={common('active')} />
            <Tab label={common('inactive')} />
          </Tabs>
          <Divider sx={{ my: 2 }} />
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} sm={6} md={4}>
              <TextField
                fullWidth
                placeholder={common('search')}
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <SearchIcon />
                    </InputAdornment>
                  ),
                }}
                size="small"
                disabled={isLoading}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={4}>
              <Box sx={{ display: 'flex', gap: 1 }}>
                <Button
                  variant="outlined"
                  startIcon={<FilterListIcon />}
                  onClick={handleFilterClick}
                  size="small"
                  disabled={isLoading}
                >
                  {common('filter')}
                </Button>
                <Menu
                  anchorEl={filterAnchorEl}
                  open={Boolean(filterAnchorEl)}
                  onClose={handleFilterClose}
                >
                  <MenuItem sx={{ pointerEvents: 'none' }}>
                    <Typography variant="subtitle2">{common('status')}</Typography>
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setStatusFilter('all');
                      handleFilterClose();
                    }}
                    selected={statusFilter === 'all'}
                  >
                    {common('all')}
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setStatusFilter('active');
                      handleFilterClose();
                    }}
                    selected={statusFilter === 'active'}
                  >
                    {common('active')}
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setStatusFilter('inactive');
                      handleFilterClose();
                    }}
                    selected={statusFilter === 'inactive'}
                  >
                    {common('inactive')}
                  </MenuItem>
                  <Divider />
                  <MenuItem sx={{ pointerEvents: 'none' }}>
                    <Typography variant="subtitle2">{users('role')}</Typography>
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setRoleFilter('all');
                      handleFilterClose();
                    }}
                    selected={roleFilter === 'all'}
                  >
                    {common('all')}
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setRoleFilter('saas_admin');
                      handleFilterClose();
                    }}
                    selected={roleFilter === 'saas_admin'}
                  >
                    {roles('saasAdmin')}
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setRoleFilter('tenant_admin');
                      handleFilterClose();
                    }}
                    selected={roleFilter === 'tenant_admin'}
                  >
                    {roles('tenantAdmin')}
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setRoleFilter('shop_manager');
                      handleFilterClose();
                    }}
                    selected={roleFilter === 'shop_manager'}
                  >
                    {roles('shopManager')}
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setRoleFilter('assistant_manager');
                      handleFilterClose();
                    }}
                    selected={roleFilter === 'assistant_manager'}
                  >
                    {roles('assistantManager')}
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setRoleFilter('executive');
                      handleFilterClose();
                    }}
                    selected={roleFilter === 'executive'}
                  >
                    {roles('executive')}
                  </MenuItem>
                </Menu>
              </Box>
            </Grid>
            <Grid item xs={12} sm={12} md={4} sx={{ display: 'flex', justifyContent: 'flex-end' }}>
              <Button
                variant="contained"
                color="primary"
                startIcon={<AddIcon />}
                onClick={handleOpenCreateUserDialog}
                disabled={isLoading}
              >
                {users('addUser')}
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {isLoading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', py: 5 }}>
          <CircularProgress size={40} />
          <Typography variant="h6" sx={{ ml: 2 }}>
            {common('loading')}
          </Typography>
        </Box>
      ) : filteredUsers.length === 0 ? (
        <Box sx={{ textAlign: 'center', py: 5 }}>
          <Typography variant="h6" color="textSecondary">
            {users('noUsersFound')}
          </Typography>
          <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
            {users('tryDifferentFilters')}
          </Typography>
        </Box>
      ) : (
        <DataTable
          columns={columns}
          data={filteredUsers}
          keyField="id"
          pagination
          paginationPerPage={10}
          paginationTotalRows={filteredUsers.length}
          progressPending={isLoading}
        />
      )

      {/* User Dialog */}
      <Dialog open={openUserDialog} onClose={handleCloseUserDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          {selectedUser ? users('editUser') : users('addUser')}
        </DialogTitle>
        <form onSubmit={formik.handleSubmit}>
          <DialogContent>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  id="username"
                  name="username"
                  label={users('username')}
                  value={formik.values.username}
                  onChange={formik.handleChange}
                  error={formik.touched.username && Boolean(formik.errors.username)}
                  helperText={formik.touched.username && formik.errors.username}
                  margin="normal"
                  disabled={isSubmitting || (selectedUser && selectedUser.username === 'admin')}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  id="email"
                  name="email"
                  label={common('email')}
                  value={formik.values.email}
                  onChange={formik.handleChange}
                  error={formik.touched.email && Boolean(formik.errors.email)}
                  helperText={formik.touched.email && formik.errors.email}
                  margin="normal"
                  disabled={isSubmitting}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  id="first_name"
                  name="first_name"
                  label={users('firstName')}
                  value={formik.values.first_name}
                  onChange={formik.handleChange}
                  error={formik.touched.first_name && Boolean(formik.errors.first_name)}
                  helperText={formik.touched.first_name && formik.errors.first_name}
                  margin="normal"
                  disabled={isSubmitting}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  id="last_name"
                  name="last_name"
                  label={users('lastName')}
                  value={formik.values.last_name}
                  onChange={formik.handleChange}
                  error={formik.touched.last_name && Boolean(formik.errors.last_name)}
                  helperText={formik.touched.last_name && formik.errors.last_name}
                  margin="normal"
                  disabled={isSubmitting}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  id="phone"
                  name="phone"
                  label={common('phone')}
                  value={formik.values.phone}
                  onChange={formik.handleChange}
                  error={formik.touched.phone && Boolean(formik.errors.phone)}
                  helperText={formik.touched.phone && formik.errors.phone}
                  margin="normal"
                  disabled={isSubmitting}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth margin="normal" disabled={isSubmitting || (selectedUser && selectedUser.username === 'admin')}>
                  <InputLabel id="role-label">{users('role')}</InputLabel>
                  <Select
                    labelId="role-label"
                    id="role"
                    name="role"
                    value={formik.values.role}
                    onChange={formik.handleChange}
                    error={formik.touched.role && Boolean(formik.errors.role)}
                    label={users('role')}
                  >
                    <MenuItem value="saas_admin">{roles('saasAdmin')}</MenuItem>
                    <MenuItem value="tenant_admin">{roles('tenantAdmin')}</MenuItem>
                    <MenuItem value="shop_manager">{roles('shopManager')}</MenuItem>
                    <MenuItem value="assistant_manager">{roles('assistantManager')}</MenuItem>
                    <MenuItem value="executive">{roles('executive')}</MenuItem>
                  </Select>
                  {formik.touched.role && formik.errors.role && (
                    <FormHelperText error>{formik.errors.role}</FormHelperText>
                  )}
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                {formik.values.role === 'tenant_admin' && (
                  <FormControl fullWidth margin="normal" disabled={isSubmitting}>
                    <InputLabel id="tenant-label">{common('tenant')}</InputLabel>
                    <Select
                      labelId="tenant-label"
                      id="tenant_id"
                      name="tenant_id"
                      value={formik.values.tenant_id}
                      onChange={formik.handleChange}
                      error={formik.touched.tenant_id && Boolean(formik.errors.tenant_id)}
                      label={common('tenant')}
                    >
                      {tenantsList.map((tenant) => (
                        <MenuItem key={tenant.id} value={tenant.id}>
                          {tenant.name}
                        </MenuItem>
                      ))}
                    </Select>
                    {formik.touched.tenant_id && formik.errors.tenant_id && (
                      <FormHelperText error>{formik.errors.tenant_id}</FormHelperText>
                    )}
                  </FormControl>
                )}
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  id="password"
                  name="password"
                  label={selectedUser ? users('newPassword') : common('password')}
                  type={showPassword ? 'text' : 'password'}
                  value={formik.values.password}
                  onChange={formik.handleChange}
                  error={formik.touched.password && Boolean(formik.errors.password)}
                  helperText={
                    (formik.touched.password && formik.errors.password) ||
                    (selectedUser ? users('leaveBlankToKeepCurrent') : '')
                  }
                  margin="normal"
                  disabled={isSubmitting}
                  InputProps={{
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton
                          aria-label="toggle password visibility"
                          onClick={() => setShowPassword(!showPassword)}
                          edge="end"
                          disabled={isSubmitting}
                        >
                          {showPassword ? <VisibilityOffIcon /> : <VisibilityIcon />}
                        </IconButton>
                      </InputAdornment>
                    ),
                  }}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  id="confirmPassword"
                  name="confirmPassword"
                  label={common('confirmPassword')}
                  type={showConfirmPassword ? 'text' : 'password'}
                  value={formik.values.confirmPassword}
                  onChange={formik.handleChange}
                  error={formik.touched.confirmPassword && Boolean(formik.errors.confirmPassword)}
                  helperText={formik.touched.confirmPassword && formik.errors.confirmPassword}
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
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseUserDialog} disabled={isSubmitting}>
              {common('cancel')}
            </Button>
            <Button 
              type="submit" 
              variant="contained" 
              color="primary"
              disabled={isSubmitting || !formik.isValid || !formik.dirty}
              startIcon={isSubmitting ? <CircularProgress size={20} color="inherit" /> : null}
            >
              {isSubmitting ? common('saving') : selectedUser ? common('save') : common('add')}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Container>
  );
};

export default UsersManagement;