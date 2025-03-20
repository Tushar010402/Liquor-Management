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
  Business as BusinessIcon,
  People as PeopleIcon,
  Store as StoreIcon,
  AttachMoney as MoneyIcon,
} from '@mui/icons-material';
import { DataTable, PageHeader } from '../../components/common';
import { useTranslations, useFormValidation, useGlobalConfirmDialog } from '../../hooks';
import * as Yup from 'yup';

// Mock data for tenants
const mockTenants = [
  {
    id: 1,
    name: 'ABC Liquors',
    email: 'admin@abcliquors.com',
    plan: 'Premium',
    status: 'active',
    shops: 5,
    users: 25,
    created_at: '2023-01-15',
    subscription_ends: '2024-01-15',
  },
  {
    id: 2,
    name: 'XYZ Wines',
    email: 'admin@xyzwines.com',
    plan: 'Standard',
    status: 'active',
    shops: 3,
    users: 15,
    created_at: '2023-02-20',
    subscription_ends: '2024-02-20',
  },
  {
    id: 3,
    name: 'City Spirits',
    email: 'admin@cityspirits.com',
    plan: 'Basic',
    status: 'active',
    shops: 2,
    users: 10,
    created_at: '2023-03-10',
    subscription_ends: '2024-03-10',
  },
  {
    id: 4,
    name: 'Metro Beverages',
    email: 'admin@metrobeverages.com',
    plan: 'Premium',
    status: 'active',
    shops: 4,
    users: 20,
    created_at: '2023-04-05',
    subscription_ends: '2024-04-05',
  },
  {
    id: 5,
    name: 'Downtown Drinks',
    email: 'admin@downtowndrinks.com',
    plan: 'Basic',
    status: 'inactive',
    shops: 1,
    users: 5,
    created_at: '2023-05-15',
    subscription_ends: '2023-11-15',
  },
  {
    id: 6,
    name: 'Uptown Liquors',
    email: 'admin@uptownliquors.com',
    plan: 'Standard',
    status: 'active',
    shops: 2,
    users: 12,
    created_at: '2023-06-20',
    subscription_ends: '2024-06-20',
  },
  {
    id: 7,
    name: 'Coastal Wines',
    email: 'admin@coastalwines.com',
    plan: 'Premium',
    status: 'active',
    shops: 3,
    users: 18,
    created_at: '2023-07-10',
    subscription_ends: '2024-07-10',
  },
  {
    id: 8,
    name: 'Highland Spirits',
    email: 'admin@highlandspirits.com',
    plan: 'Basic',
    status: 'inactive',
    shops: 1,
    users: 6,
    created_at: '2023-08-05',
    subscription_ends: '2023-11-05',
  },
];

// Validation schema for tenant form
const tenantValidationSchema = Yup.object({
  name: Yup.string().required('Tenant name is required'),
  email: Yup.string().email('Invalid email address').required('Email is required'),
  plan: Yup.string().required('Subscription plan is required'),
  maxShops: Yup.number()
    .positive('Must be a positive number')
    .integer('Must be an integer')
    .required('Maximum shops is required'),
  maxUsers: Yup.number()
    .positive('Must be a positive number')
    .integer('Must be an integer')
    .required('Maximum users is required'),
  subscriptionPeriod: Yup.number()
    .positive('Must be a positive number')
    .integer('Must be an integer')
    .required('Subscription period is required'),
});

/**
 * Tenants Management component for SaaS Admin
 */
const TenantsManagement: React.FC = () => {
  const { common, tenants } = useTranslations();
  const theme = useTheme();
  const { confirm } = useGlobalConfirmDialog();
  const [searchQuery, setSearchQuery] = useState('');
  const [filterAnchorEl, setFilterAnchorEl] = useState<null | HTMLElement>(null);
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [planFilter, setPlanFilter] = useState<string>('all');
  const [openTenantDialog, setOpenTenantDialog] = useState(false);
  const [selectedTenant, setSelectedTenant] = useState<any | null>(null);
  const [actionAnchorEl, setActionAnchorEl] = useState<{ [key: number]: HTMLElement | null }>({});
  const [tabValue, setTabValue] = useState(0);

  // Form validation for tenant dialog
  const { formik } = useFormValidation({
    initialValues: {
      name: '',
      email: '',
      plan: 'Standard',
      maxShops: 3,
      maxUsers: 15,
      subscriptionPeriod: 12,
    },
    validationSchema: tenantValidationSchema,
    onSubmit: (values) => {
      console.log('Form submitted:', values);
      handleCloseTenantDialog();
      // In a real app, you would make an API call to create/update the tenant
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

  // Handle opening the action menu for a tenant
  const handleActionClick = (event: React.MouseEvent<HTMLElement>, tenantId: number) => {
    setActionAnchorEl({ ...actionAnchorEl, [tenantId]: event.currentTarget });
  };

  // Handle closing the action menu for a tenant
  const handleActionClose = (tenantId: number) => {
    setActionAnchorEl({ ...actionAnchorEl, [tenantId]: null });
  };

  // Handle opening the tenant dialog for creating a new tenant
  const handleOpenCreateTenantDialog = () => {
    setSelectedTenant(null);
    formik.resetForm();
    setOpenTenantDialog(true);
  };

  // Handle opening the tenant dialog for editing an existing tenant
  const handleOpenEditTenantDialog = (tenant: any) => {
    setSelectedTenant(tenant);
    formik.setValues({
      name: tenant.name,
      email: tenant.email,
      plan: tenant.plan,
      maxShops: tenant.shops,
      maxUsers: tenant.users,
      subscriptionPeriod: 12, // Assuming 12 months
    });
    setOpenTenantDialog(true);
    handleActionClose(tenant.id);
  };

  // Handle closing the tenant dialog
  const handleCloseTenantDialog = () => {
    setOpenTenantDialog(false);
  };

  // Handle deleting a tenant
  const handleDeleteTenant = async (tenant: any) => {
    const confirmed = await confirm({
      title: tenants('deleteTenant'),
      message: `${tenants('confirmDeleteTenant')} "${tenant.name}"?`,
      confirmButtonColor: 'error',
      confirmText: common('delete'),
      cancelText: common('cancel'),
    });

    if (confirmed) {
      console.log('Deleting tenant:', tenant);
      // In a real app, you would make an API call to delete the tenant
    }

    handleActionClose(tenant.id);
  };

  // Handle changing the status of a tenant
  const handleToggleTenantStatus = async (tenant: any) => {
    const newStatus = tenant.status === 'active' ? 'inactive' : 'active';
    const confirmed = await confirm({
      title: newStatus === 'active' ? tenants('activateTenant') : tenants('deactivateTenant'),
      message: newStatus === 'active'
        ? `${tenants('confirmActivateTenant')} "${tenant.name}"?`
        : `${tenants('confirmDeactivateTenant')} "${tenant.name}"?`,
      confirmButtonColor: newStatus === 'active' ? 'success' : 'warning',
      confirmText: newStatus === 'active' ? common('activate') : common('deactivate'),
      cancelText: common('cancel'),
    });

    if (confirmed) {
      console.log('Toggling tenant status:', tenant, newStatus);
      // In a real app, you would make an API call to update the tenant status
    }

    handleActionClose(tenant.id);
  };

  // Handle tab change
  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  // Filter tenants based on search query and filters
  const filteredTenants = mockTenants.filter((tenant) => {
    const matchesSearch = tenant.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      tenant.email.toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesStatus = statusFilter === 'all' || tenant.status === statusFilter;
    const matchesPlan = planFilter === 'all' || tenant.plan === planFilter;
    
    return matchesSearch && matchesStatus && matchesPlan;
  });

  // Define columns for the data table
  const columns = [
    {
      field: 'name',
      headerName: common('name'),
      flex: 1,
      renderCell: (params: any) => (
        <Box>
          <Typography variant="body1" fontWeight={500}>
            {params.name}
          </Typography>
          <Typography variant="body2" color="textSecondary">
            {params.email}
          </Typography>
        </Box>
      ),
    },
    {
      field: 'plan',
      headerName: tenants('subscriptionPlan'),
      flex: 0.7,
      renderCell: (params: any) => (
        <Chip
          label={params.plan}
          color={
            params.plan === 'Premium'
              ? 'primary'
              : params.plan === 'Standard'
              ? 'info'
              : 'default'
          }
          size="small"
          variant="outlined"
        />
      ),
    },
    {
      field: 'status',
      headerName: common('status'),
      flex: 0.7,
      renderCell: (params: any) => (
        <Chip
          label={params.status === 'active' ? common('active') : common('inactive')}
          color={params.status === 'active' ? 'success' : 'error'}
          size="small"
        />
      ),
    },
    {
      field: 'shops',
      headerName: common('shops'),
      flex: 0.5,
      align: 'center',
    },
    {
      field: 'users',
      headerName: common('users'),
      flex: 0.5,
      align: 'center',
    },
    {
      field: 'created_at',
      headerName: tenants('createdAt'),
      flex: 0.7,
    },
    {
      field: 'subscription_ends',
      headerName: tenants('subscriptionEnds'),
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
            <MenuItem onClick={() => handleOpenEditTenantDialog(params)}>
              <EditIcon fontSize="small" sx={{ mr: 1 }} />
              {common('edit')}
            </MenuItem>
            <MenuItem
              onClick={() => handleToggleTenantStatus(params)}
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
            <MenuItem onClick={() => handleDeleteTenant(params)} sx={{ color: 'error.main' }}>
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
        title={tenants('tenants')}
        subtitle={tenants('manageTenants')}
        icon={<BusinessIcon fontSize="large" />}
      />

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Tabs
            value={tabValue}
            onChange={handleTabChange}
            indicatorColor="primary"
            textColor="primary"
            variant="fullWidth"
            aria-label="tenant tabs"
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
                    <Typography variant="subtitle2">{tenants('subscriptionPlan')}</Typography>
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setPlanFilter('all');
                      handleFilterClose();
                    }}
                    selected={planFilter === 'all'}
                  >
                    {common('all')}
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setPlanFilter('Basic');
                      handleFilterClose();
                    }}
                    selected={planFilter === 'Basic'}
                  >
                    Basic
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setPlanFilter('Standard');
                      handleFilterClose();
                    }}
                    selected={planFilter === 'Standard'}
                  >
                    Standard
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setPlanFilter('Premium');
                      handleFilterClose();
                    }}
                    selected={planFilter === 'Premium'}
                  >
                    Premium
                  </MenuItem>
                </Menu>
              </Box>
            </Grid>
            <Grid item xs={12} sm={12} md={4} sx={{ display: 'flex', justifyContent: 'flex-end' }}>
              <Button
                variant="contained"
                color="primary"
                startIcon={<AddIcon />}
                onClick={handleOpenCreateTenantDialog}
              >
                {tenants('addTenant')}
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <DataTable
        columns={columns}
        data={filteredTenants}
        keyField="id"
        pagination
        paginationPerPage={10}
        paginationTotalRows={filteredTenants.length}
      />

      {/* Tenant Dialog */}
      <Dialog open={openTenantDialog} onClose={handleCloseTenantDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          {selectedTenant ? tenants('editTenant') : tenants('addTenant')}
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
                  <InputLabel id="plan-label">{tenants('subscriptionPlan')}</InputLabel>
                  <Select
                    labelId="plan-label"
                    id="plan"
                    name="plan"
                    value={formik.values.plan}
                    onChange={formik.handleChange}
                    error={formik.touched.plan && Boolean(formik.errors.plan)}
                    label={tenants('subscriptionPlan')}
                  >
                    <MenuItem value="Basic">Basic</MenuItem>
                    <MenuItem value="Standard">Standard</MenuItem>
                    <MenuItem value="Premium">Premium</MenuItem>
                  </Select>
                  {formik.touched.plan && formik.errors.plan && (
                    <FormHelperText error>{formik.errors.plan}</FormHelperText>
                  )}
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  id="subscriptionPeriod"
                  name="subscriptionPeriod"
                  label={tenants('subscriptionPeriod')}
                  type="number"
                  value={formik.values.subscriptionPeriod}
                  onChange={formik.handleChange}
                  error={formik.touched.subscriptionPeriod && Boolean(formik.errors.subscriptionPeriod)}
                  helperText={formik.touched.subscriptionPeriod && formik.errors.subscriptionPeriod}
                  margin="normal"
                  InputProps={{
                    endAdornment: <InputAdornment position="end">{common('months')}</InputAdornment>,
                  }}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  id="maxShops"
                  name="maxShops"
                  label={tenants('maxShops')}
                  type="number"
                  value={formik.values.maxShops}
                  onChange={formik.handleChange}
                  error={formik.touched.maxShops && Boolean(formik.errors.maxShops)}
                  helperText={formik.touched.maxShops && formik.errors.maxShops}
                  margin="normal"
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  id="maxUsers"
                  name="maxUsers"
                  label={tenants('maxUsers')}
                  type="number"
                  value={formik.values.maxUsers}
                  onChange={formik.handleChange}
                  error={formik.touched.maxUsers && Boolean(formik.errors.maxUsers)}
                  helperText={formik.touched.maxUsers && formik.errors.maxUsers}
                  margin="normal"
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseTenantDialog}>{common('cancel')}</Button>
            <Button type="submit" variant="contained" color="primary">
              {selectedTenant ? common('save') : common('add')}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Container>
  );
};

export default TenantsManagement;