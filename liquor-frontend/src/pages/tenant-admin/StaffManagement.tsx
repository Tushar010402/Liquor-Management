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
  Store as StoreIcon,
} from '@mui/icons-material';
import { DataTable, PageHeader } from '../../components/common';
import { useTranslations, useFormValidation, useGlobalConfirmDialog } from '../../hooks';
import * as Yup from 'yup';
import { stringUtils } from '../../utils';

// Mock data for staff
const mockStaff = [
  {
    id: 1,
    name: 'John Doe',
    email: 'john.doe@abcliquors.com',
    phone: '9876543210',
    role: 'manager',
    shop: 'Downtown Liquor Store',
    status: 'active',
    created_at: '2023-01-15',
    last_login: '2023-06-15',
  },
  {
    id: 2,
    name: 'Jane Smith',
    email: 'jane.smith@abcliquors.com',
    phone: '9876543211',
    role: 'manager',
    shop: 'Uptown Wine Shop',
    status: 'active',
    created_at: '2023-02-20',
    last_login: '2023-06-10',
  },
  {
    id: 3,
    name: 'Robert Johnson',
    email: 'robert.johnson@abcliquors.com',
    phone: '9876543212',
    role: 'cashier',
    shop: 'Downtown Liquor Store',
    status: 'active',
    created_at: '2023-03-10',
    last_login: '2023-06-12',
  },
  {
    id: 4,
    name: 'Emily Davis',
    email: 'emily.davis@abcliquors.com',
    phone: '9876543213',
    role: 'cashier',
    shop: 'Uptown Wine Shop',
    status: 'active',
    created_at: '2023-04-05',
    last_login: '2023-06-14',
  },
  {
    id: 5,
    name: 'Michael Wilson',
    email: 'michael.wilson@abcliquors.com',
    phone: '9876543214',
    role: 'sales_associate',
    shop: 'Midtown Spirits',
    status: 'inactive',
    created_at: '2023-05-15',
    last_login: '2023-05-20',
  },
  {
    id: 6,
    name: 'Sarah Brown',
    email: 'sarah.brown@abcliquors.com',
    phone: '9876543215',
    role: 'manager',
    shop: 'Midtown Spirits',
    status: 'active',
    created_at: '2023-06-10',
    last_login: '2023-06-13',
  },
  {
    id: 7,
    name: 'David Miller',
    email: 'david.miller@abcliquors.com',
    phone: '9876543216',
    role: 'inventory_clerk',
    shop: 'Suburban Liquors',
    status: 'active',
    created_at: '2023-07-05',
    last_login: '2023-06-11',
  },
];

// Mock data for shops (for dropdown)
const mockShops = [
  { id: 1, name: 'Downtown Liquor Store' },
  { id: 2, name: 'Uptown Wine Shop' },
  { id: 3, name: 'Midtown Spirits' },
  { id: 4, name: 'Suburban Liquors' },
  { id: 5, name: 'Beachside Beverages' },
];

// Validation schema for staff form
const staffValidationSchema = Yup.object({
  name: Yup.string().required('Name is required'),
  email: Yup.string().email('Invalid email address').required('Email is required'),
  phone: Yup.string()
    .matches(/^\d{10}$/, 'Phone number must be 10 digits')
    .required('Phone number is required'),
  role: Yup.string().required('Role is required'),
  shop_id: Yup.number().required('Shop is required'),
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
});

// Validation schema for editing a staff (password is optional)
const staffEditValidationSchema = Yup.object({
  name: Yup.string().required('Name is required'),
  email: Yup.string().email('Invalid email address').required('Email is required'),
  phone: Yup.string()
    .matches(/^\d{10}$/, 'Phone number must be 10 digits')
    .required('Phone number is required'),
  role: Yup.string().required('Role is required'),
  shop_id: Yup.number().required('Shop is required'),
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
});

/**
 * Staff Management component for Tenant Admin
 */
const StaffManagement: React.FC = () => {
  const { common, users, roles } = useTranslations();
  const theme = useTheme();
  const { confirm } = useGlobalConfirmDialog();
  const [searchQuery, setSearchQuery] = useState('');
  const [filterAnchorEl, setFilterAnchorEl] = useState<null | HTMLElement>(null);
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [roleFilter, setRoleFilter] = useState<string>('all');
  const [shopFilter, setShopFilter] = useState<string>('all');
  const [openStaffDialog, setOpenStaffDialog] = useState(false);
  const [selectedStaff, setSelectedStaff] = useState<any | null>(null);
  const [actionAnchorEl, setActionAnchorEl] = useState<{ [key: number]: HTMLElement | null }>({});
  const [tabValue, setTabValue] = useState(0);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  // Form validation for staff dialog
  const { formik } = useFormValidation({
    initialValues: {
      name: '',
      email: '',
      phone: '',
      role: 'cashier',
      shop_id: null as number | null,
      password: '',
      confirmPassword: '',
      address: '',
      emergency_contact: '',
      joining_date: '',
      id_proof_type: '',
      id_proof_number: '',
    },
    validationSchema: selectedStaff ? staffEditValidationSchema : staffValidationSchema,
    onSubmit: (values) => {
      console.log('Form submitted:', values);
      handleCloseStaffDialog();
      // In a real app, you would make an API call to create/update the staff
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

  // Handle opening the action menu for a staff
  const handleActionClick = (event: React.MouseEvent<HTMLElement>, staffId: number) => {
    setActionAnchorEl({ ...actionAnchorEl, [staffId]: event.currentTarget });
  };

  // Handle closing the action menu for a staff
  const handleActionClose = (staffId: number) => {
    setActionAnchorEl({ ...actionAnchorEl, [staffId]: null });
  };

  // Handle opening the staff dialog for creating a new staff
  const handleOpenCreateStaffDialog = () => {
    setSelectedStaff(null);
    formik.resetForm();
    setOpenStaffDialog(true);
  };

  // Handle opening the staff dialog for editing an existing staff
  const handleOpenEditStaffDialog = (staff: any) => {
    setSelectedStaff(staff);
    formik.setValues({
      name: staff.name,
      email: staff.email,
      phone: staff.phone,
      role: staff.role,
      shop_id: mockShops.find(s => s.name === staff.shop)?.id || null,
      password: '',
      confirmPassword: '',
      address: staff.address || '',
      emergency_contact: staff.emergency_contact || '',
      joining_date: staff.joining_date || '',
      id_proof_type: staff.id_proof_type || '',
      id_proof_number: staff.id_proof_number || '',
    });
    setOpenStaffDialog(true);
    handleActionClose(staff.id);
  };

  // Handle closing the staff dialog
  const handleCloseStaffDialog = () => {
    setOpenStaffDialog(false);
    setShowPassword(false);
    setShowConfirmPassword(false);
  };

  // Handle deleting a staff
  const handleDeleteStaff = async (staff: any) => {
    const confirmed = await confirm({
      title: users('deleteUser'),
      message: `${users('confirmDeleteUser')} "${staff.name}"?`,
      confirmButtonColor: 'error',
      confirmText: common('delete'),
      cancelText: common('cancel'),
    });

    if (confirmed) {
      console.log('Deleting staff:', staff);
      // In a real app, you would make an API call to delete the staff
    }

    handleActionClose(staff.id);
  };

  // Handle changing the status of a staff
  const handleToggleStaffStatus = async (staff: any) => {
    const newStatus = staff.status === 'active' ? 'inactive' : 'active';
    const confirmed = await confirm({
      title: newStatus === 'active' ? users('activateUser') : users('deactivateUser'),
      message: newStatus === 'active'
        ? `${users('confirmActivateUser')} "${staff.name}"?`
        : `${users('confirmDeactivateUser')} "${staff.name}"?`,
      confirmButtonColor: newStatus === 'active' ? 'success' : 'warning',
      confirmText: newStatus === 'active' ? common('activate') : common('deactivate'),
      cancelText: common('cancel'),
    });

    if (confirmed) {
      console.log('Toggling staff status:', staff, newStatus);
      // In a real app, you would make an API call to update the staff status
    }

    handleActionClose(staff.id);
  };

  // Handle tab change
  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  // Get unique shops for filter
  const uniqueShops = Array.from(new Set(mockStaff.map(staff => staff.shop)));

  // Filter staff based on search query and filters
  const filteredStaff = mockStaff.filter((staff) => {
    const matchesSearch = staff.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      staff.email.toLowerCase().includes(searchQuery.toLowerCase()) ||
      staff.phone.includes(searchQuery);
    
    const matchesStatus = statusFilter === 'all' || staff.status === statusFilter;
    const matchesRole = roleFilter === 'all' || staff.role === roleFilter;
    const matchesShop = shopFilter === 'all' || staff.shop === shopFilter;
    
    return matchesSearch && matchesStatus && matchesRole && matchesShop;
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
      field: 'phone',
      headerName: common('phone'),
      flex: 0.7,
    },
    {
      field: 'role',
      headerName: users('role'),
      flex: 0.7,
      renderCell: (params: any) => (
        <Chip
          label={
            params.role === 'manager'
              ? roles('manager')
              : params.role === 'cashier'
              ? roles('cashier')
              : params.role === 'sales_associate'
              ? roles('salesAssociate')
              : params.role === 'inventory_clerk'
              ? roles('inventoryClerk')
              : params.role
          }
          color={
            params.role === 'manager'
              ? 'primary'
              : params.role === 'cashier'
              ? 'secondary'
              : 'default'
          }
          size="small"
          variant="outlined"
        />
      ),
    },
    {
      field: 'shop',
      headerName: common('shop'),
      flex: 0.7,
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
            <MenuItem onClick={() => handleOpenEditStaffDialog(params)}>
              <EditIcon fontSize="small" sx={{ mr: 1 }} />
              {common('edit')}
            </MenuItem>
            <MenuItem
              onClick={() => handleToggleStaffStatus(params)}
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
            <MenuItem onClick={() => handleDeleteStaff(params)} sx={{ color: 'error.main' }}>
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
        title={users('staff')}
        subtitle={users('manageStaff')}
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
            aria-label="staff tabs"
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
                      setRoleFilter('manager');
                      handleFilterClose();
                    }}
                    selected={roleFilter === 'manager'}
                  >
                    {roles('manager')}
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setRoleFilter('cashier');
                      handleFilterClose();
                    }}
                    selected={roleFilter === 'cashier'}
                  >
                    {roles('cashier')}
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setRoleFilter('sales_associate');
                      handleFilterClose();
                    }}
                    selected={roleFilter === 'sales_associate'}
                  >
                    {roles('salesAssociate')}
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setRoleFilter('inventory_clerk');
                      handleFilterClose();
                    }}
                    selected={roleFilter === 'inventory_clerk'}
                  >
                    {roles('inventoryClerk')}
                  </MenuItem>
                  <Divider />
                  <MenuItem sx={{ pointerEvents: 'none' }}>
                    <Typography variant="subtitle2">{common('shop')}</Typography>
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setShopFilter('all');
                      handleFilterClose();
                    }}
                    selected={shopFilter === 'all'}
                  >
                    {common('all')}
                  </MenuItem>
                  {uniqueShops.map((shop) => (
                    <MenuItem
                      key={shop}
                      onClick={() => {
                        setShopFilter(shop);
                        handleFilterClose();
                      }}
                      selected={shopFilter === shop}
                    >
                      {shop}
                    </MenuItem>
                  ))}
                </Menu>
              </Box>
            </Grid>
            <Grid item xs={12} sm={12} md={4} sx={{ display: 'flex', justifyContent: 'flex-end' }}>
              <Button
                variant="contained"
                color="primary"
                startIcon={<AddIcon />}
                onClick={handleOpenCreateStaffDialog}
              >
                {users('addStaff')}
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <DataTable
        columns={columns}
        data={filteredStaff}
        keyField="id"
        pagination
        paginationPerPage={10}
        paginationTotalRows={filteredStaff.length}
      />

      {/* Staff Dialog */}
      <Dialog open={openStaffDialog} onClose={handleCloseStaffDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          {selectedStaff ? users('editStaff') : users('addStaff')}
        </DialogTitle>
        <form onSubmit={formik.handleSubmit}>
          <DialogContent>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <Typography variant="subtitle1" gutterBottom>
                  {users('basicInfo')}
                </Typography>
              </Grid>
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
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  id="address"
                  name="address"
                  label={common('address')}
                  value={formik.values.address}
                  onChange={formik.handleChange}
                  margin="normal"
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  id="emergency_contact"
                  name="emergency_contact"
                  label={users('emergencyContact')}
                  value={formik.values.emergency_contact}
                  onChange={formik.handleChange}
                  margin="normal"
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  id="joining_date"
                  name="joining_date"
                  label={users('joiningDate')}
                  type="date"
                  value={formik.values.joining_date}
                  onChange={formik.handleChange}
                  margin="normal"
                  InputLabelProps={{
                    shrink: true,
                  }}
                />
              </Grid>
              <Grid item xs={12}>
                <Typography variant="subtitle1" gutterBottom sx={{ mt: 2 }}>
                  {users('roleAndShop')}
                </Typography>
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
                    <MenuItem value="manager">{roles('manager')}</MenuItem>
                    <MenuItem value="cashier">{roles('cashier')}</MenuItem>
                    <MenuItem value="sales_associate">{roles('salesAssociate')}</MenuItem>
                    <MenuItem value="inventory_clerk">{roles('inventoryClerk')}</MenuItem>
                  </Select>
                  {formik.touched.role && formik.errors.role && (
                    <FormHelperText error>{formik.errors.role}</FormHelperText>
                  )}
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth margin="normal">
                  <InputLabel id="shop-label">{common('shop')}</InputLabel>
                  <Select
                    labelId="shop-label"
                    id="shop_id"
                    name="shop_id"
                    value={formik.values.shop_id}
                    onChange={formik.handleChange}
                    error={formik.touched.shop_id && Boolean(formik.errors.shop_id)}
                    label={common('shop')}
                  >
                    {mockShops.map((shop) => (
                      <MenuItem key={shop.id} value={shop.id}>
                        {shop.name}
                      </MenuItem>
                    ))}
                  </Select>
                  {formik.touched.shop_id && formik.errors.shop_id && (
                    <FormHelperText error>{formik.errors.shop_id}</FormHelperText>
                  )}
                </FormControl>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="subtitle1" gutterBottom sx={{ mt: 2 }}>
                  {users('identificationInfo')}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth margin="normal">
                  <InputLabel id="id-proof-type-label">{users('idProofType')}</InputLabel>
                  <Select
                    labelId="id-proof-type-label"
                    id="id_proof_type"
                    name="id_proof_type"
                    value={formik.values.id_proof_type}
                    onChange={formik.handleChange}
                    label={users('idProofType')}
                  >
                    <MenuItem value="aadhar">Aadhar Card</MenuItem>
                    <MenuItem value="pan">PAN Card</MenuItem>
                    <MenuItem value="voter">Voter ID</MenuItem>
                    <MenuItem value="driving">Driving License</MenuItem>
                    <MenuItem value="passport">Passport</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  id="id_proof_number"
                  name="id_proof_number"
                  label={users('idProofNumber')}
                  value={formik.values.id_proof_number}
                  onChange={formik.handleChange}
                  margin="normal"
                />
              </Grid>
              <Grid item xs={12}>
                <Typography variant="subtitle1" gutterBottom sx={{ mt: 2 }}>
                  {users('accountInfo')}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  id="password"
                  name="password"
                  label={selectedStaff ? users('newPassword') : common('password')}
                  type={showPassword ? 'text' : 'password'}
                  value={formik.values.password}
                  onChange={formik.handleChange}
                  error={formik.touched.password && Boolean(formik.errors.password)}
                  helperText={
                    (formik.touched.password && formik.errors.password) ||
                    (selectedStaff ? users('leaveBlankToKeepCurrent') : '')
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
            <Button onClick={handleCloseStaffDialog}>{common('cancel')}</Button>
            <Button type="submit" variant="contained" color="primary">
              {selectedStaff ? common('save') : common('add')}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Container>
  );
};

export default StaffManagement;