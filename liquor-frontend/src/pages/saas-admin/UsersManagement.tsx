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
} from '@mui/icons-material';
import { DataTable, PageHeader } from '../../components/common';
import { useTranslations, useFormValidation, useGlobalConfirmDialog } from '../../hooks';
import * as Yup from 'yup';
import { stringUtils } from '../../utils';

// Mock data for users
const mockUsers = [
  {
    id: 1,
    name: 'John Doe',
    email: 'john.doe@example.com',
    role: 'saas_admin',
    status: 'active',
    tenant: null,
    created_at: '2023-01-10',
    last_login: '2023-06-15',
  },
  {
    id: 2,
    name: 'Jane Smith',
    email: 'jane.smith@example.com',
    role: 'saas_admin',
    status: 'active',
    tenant: null,
    created_at: '2023-02-15',
    last_login: '2023-06-10',
  },
  {
    id: 3,
    name: 'Robert Johnson',
    email: 'robert.johnson@abcliquors.com',
    role: 'tenant_admin',
    status: 'active',
    tenant: 'ABC Liquors',
    created_at: '2023-01-20',
    last_login: '2023-06-12',
  },
  {
    id: 4,
    name: 'Emily Davis',
    email: 'emily.davis@xyzwines.com',
    role: 'tenant_admin',
    status: 'active',
    tenant: 'XYZ Wines',
    created_at: '2023-02-25',
    last_login: '2023-06-14',
  },
  {
    id: 5,
    name: 'Michael Wilson',
    email: 'michael.wilson@cityspirits.com',
    role: 'tenant_admin',
    status: 'inactive',
    tenant: 'City Spirits',
    created_at: '2023-03-05',
    last_login: '2023-05-20',
  },
  {
    id: 6,
    name: 'Sarah Brown',
    email: 'sarah.brown@metrobeverages.com',
    role: 'tenant_admin',
    status: 'active',
    tenant: 'Metro Beverages',
    created_at: '2023-04-10',
    last_login: '2023-06-13',
  },
  {
    id: 7,
    name: 'David Miller',
    email: 'david.miller@downtowndrinks.com',
    role: 'tenant_admin',
    status: 'inactive',
    tenant: 'Downtown Drinks',
    created_at: '2023-05-15',
    last_login: '2023-05-25',
  },
];

// Mock data for tenants (for dropdown)
const mockTenants = [
  { id: 1, name: 'ABC Liquors' },
  { id: 2, name: 'XYZ Wines' },
  { id: 3, name: 'City Spirits' },
  { id: 4, name: 'Metro Beverages' },
  { id: 5, name: 'Downtown Drinks' },
];

// Validation schema for user form
const userValidationSchema = Yup.object({
  name: Yup.string().required('Name is required'),
  email: Yup.string().email('Invalid email address').required('Email is required'),
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
});

// Validation schema for editing a user (password is optional)
const userEditValidationSchema = Yup.object({
  name: Yup.string().required('Name is required'),
  email: Yup.string().email('Invalid email address').required('Email is required'),
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
});

/**
 * Users Management component for SaaS Admin
 */
const UsersManagement: React.FC = () => {
  const { common, users, roles } = useTranslations();
  const theme = useTheme();
  const { confirm } = useGlobalConfirmDialog();
  const [searchQuery, setSearchQuery] = useState('');
  const [filterAnchorEl, setFilterAnchorEl] = useState<null | HTMLElement>(null);
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [roleFilter, setRoleFilter] = useState<string>('all');
  const [openUserDialog, setOpenUserDialog] = useState(false);
  const [selectedUser, setSelectedUser] = useState<any | null>(null);
  const [actionAnchorEl, setActionAnchorEl] = useState<{ [key: number]: HTMLElement | null }>({});
  const [tabValue, setTabValue] = useState(0);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  // Form validation for user dialog
  const { formik } = useFormValidation({
    initialValues: {
      name: '',
      email: '',
      role: 'saas_admin',
      password: '',
      confirmPassword: '',
      tenant_id: null as number | null,
    },
    validationSchema: selectedUser ? userEditValidationSchema : userValidationSchema,
    onSubmit: (values) => {
      console.log('Form submitted:', values);
      handleCloseUserDialog();
      // In a real app, you would make an API call to create/update the user
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

  // Handle opening the user dialog for creating a new user
  const handleOpenCreateUserDialog = () => {
    setSelectedUser(null);
    formik.resetForm();
    setOpenUserDialog(true);
  };

  // Handle opening the user dialog for editing an existing user
  const handleOpenEditUserDialog = (user: any) => {
    setSelectedUser(user);
    formik.setValues({
      name: user.name,
      email: user.email,
      role: user.role,
      password: '',
      confirmPassword: '',
      tenant_id: user.tenant ? mockTenants.find(t => t.name === user.tenant)?.id || null : null,
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
  const handleDeleteUser = async (user: any) => {
    const confirmed = await confirm({
      title: users('deleteUser'),
      message: `${users('confirmDeleteUser')} "${user.name}"?`,
      confirmButtonColor: 'error',
      confirmText: common('delete'),
      cancelText: common('cancel'),
    });

    if (confirmed) {
      console.log('Deleting user:', user);
      // In a real app, you would make an API call to delete the user
    }

    handleActionClose(user.id);
  };

  // Handle changing the status of a user
  const handleToggleUserStatus = async (user: any) => {
    const newStatus = user.status === 'active' ? 'inactive' : 'active';
    const confirmed = await confirm({
      title: newStatus === 'active' ? users('activateUser') : users('deactivateUser'),
      message: newStatus === 'active'
        ? `${users('confirmActivateUser')} "${user.name}"?`
        : `${users('confirmDeactivateUser')} "${user.name}"?`,
      confirmButtonColor: newStatus === 'active' ? 'success' : 'warning',
      confirmText: newStatus === 'active' ? common('activate') : common('deactivate'),
      cancelText: common('cancel'),
    });

    if (confirmed) {
      console.log('Toggling user status:', user, newStatus);
      // In a real app, you would make an API call to update the user status
    }

    handleActionClose(user.id);
  };

  // Handle tab change
  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  // Filter users based on search query and filters
  const filteredUsers = mockUsers.filter((user) => {
    const matchesSearch = user.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      user.email.toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesStatus = statusFilter === 'all' || user.status === statusFilter;
    const matchesRole = roleFilter === 'all' || user.role === roleFilter;
    
    return matchesSearch && matchesStatus && matchesRole;
  });

  // Define columns for the data table
  const columns = [
    {
      field: 'name',
      headerName: common('name'),
      flex: 1,
      renderCell: (params: any) => (
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Avatar sx={{ mr: 2, bgcolor: theme.palette.primary.main }}>
            {stringUtils.getInitials(params.name)}
          </Avatar>
          <Box>
            <Typography variant="body1" fontWeight={500}>
              {params.name}
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
      renderCell: (params: any) => (
        <Chip
          label={
            params.role === 'saas_admin'
              ? roles('saasAdmin')
              : params.role === 'tenant_admin'
              ? roles('tenantAdmin')
              : params.role
          }
          color={params.role === 'saas_admin' ? 'primary' : 'info'}
          size="small"
          variant="outlined"
        />
      ),
    },
    {
      field: 'tenant',
      headerName: common('tenant'),
      flex: 0.7,
      renderCell: (params: any) => (
        params.tenant ? (
          <Typography variant="body2">{params.tenant}</Typography>
        ) : (
          <Typography variant="body2" color="textSecondary">
            {common('none')}
          </Typography>
        )
      ),
    },
    {
      field: 'status',
      headerName: common('status'),
      flex: 0.5,
      renderCell: (params: any) => (
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
    },
    {
      field: 'last_login',
      headerName: users('lastLogin'),
      flex: 0.7,
    },
    {
      field: 'actions',
      headerName: common('actions'),
      flex: 0.5,
      renderCell: (params: any) => (
        <>
          <IconButton
            size="small"
            onClick={(e) => handleActionClick(e, params.id)}
            aria-label="actions"
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
      <PageHeader
        title={users('users')}
        subtitle={users('manageUsers')}
        icon={<PeopleIcon fontSize="large" />}
      />

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
              />
            </Grid>
            <Grid item xs={12} sm={6} md={4}>
              <Box sx={{ display: 'flex', gap: 1 }}>
                <Button
                  variant="outlined"
                  startIcon={<FilterListIcon />}
                  onClick={handleFilterClick}
                  size="small"
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
                </Menu>
              </Box>
            </Grid>
            <Grid item xs={12} sm={12} md={4} sx={{ display: 'flex', justifyContent: 'flex-end' }}>
              <Button
                variant="contained"
                color="primary"
                startIcon={<AddIcon />}
                onClick={handleOpenCreateUserDialog}
              >
                {users('addUser')}
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <DataTable
        columns={columns}
        data={filteredUsers}
        keyField="id"
        pagination
        paginationPerPage={10}
        paginationTotalRows={filteredUsers.length}
      />

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
                  id="name"
                  name="name"
                  label={common('name')}
                  value={formik.values.name}
                  onChange={formik.handleChange}
                  error={formik.touched.name && Boolean(formik.errors.name)}
                  helperText={formik.touched.name && formik.errors.name}
                  margin="normal"
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
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth margin="normal">
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
                  </Select>
                  {formik.touched.role && formik.errors.role && (
                    <FormHelperText error>{formik.errors.role}</FormHelperText>
                  )}
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                {formik.values.role === 'tenant_admin' && (
                  <FormControl fullWidth margin="normal">
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
                      {mockTenants.map((tenant) => (
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
                  InputProps={{
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton
                          aria-label="toggle password visibility"
                          onClick={() => setShowPassword(!showPassword)}
                          edge="end"
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
                  InputProps={{
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton
                          aria-label="toggle confirm password visibility"
                          onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                          edge="end"
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
            <Button onClick={handleCloseUserDialog}>{common('cancel')}</Button>
            <Button type="submit" variant="contained" color="primary">
              {selectedUser ? common('save') : common('add')}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Container>
  );
};

export default UsersManagement;