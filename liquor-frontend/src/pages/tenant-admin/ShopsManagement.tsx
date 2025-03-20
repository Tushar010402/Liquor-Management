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
  Store as StoreIcon,
  LocationOn as LocationOnIcon,
  Phone as PhoneIcon,
  Email as EmailIcon,
  Person as PersonIcon,
} from '@mui/icons-material';
import { DataTable, PageHeader } from '../../components/common';
import { useTranslations, useFormValidation, useGlobalConfirmDialog } from '../../hooks';
import * as Yup from 'yup';
import { stringUtils } from '../../utils';

// Mock data for shops
const mockShops = [
  {
    id: 1,
    name: 'Downtown Liquor Store',
    address: '123 Main St, Downtown',
    city: 'Mumbai',
    state: 'Maharashtra',
    pincode: '400001',
    phone: '9876543210',
    email: 'downtown@abcliquors.com',
    manager: 'John Doe',
    status: 'active',
    created_at: '2023-01-15',
  },
  {
    id: 2,
    name: 'Uptown Wine Shop',
    address: '456 Park Ave, Uptown',
    city: 'Mumbai',
    state: 'Maharashtra',
    pincode: '400002',
    phone: '9876543211',
    email: 'uptown@abcliquors.com',
    manager: 'Jane Smith',
    status: 'active',
    created_at: '2023-02-20',
  },
  {
    id: 3,
    name: 'Midtown Spirits',
    address: '789 Broadway, Midtown',
    city: 'Delhi',
    state: 'Delhi',
    pincode: '110001',
    phone: '9876543212',
    email: 'midtown@abcliquors.com',
    manager: 'Robert Johnson',
    status: 'active',
    created_at: '2023-03-10',
  },
  {
    id: 4,
    name: 'Suburban Liquors',
    address: '101 Suburb Rd, Suburbs',
    city: 'Bangalore',
    state: 'Karnataka',
    pincode: '560001',
    phone: '9876543213',
    email: 'suburban@abcliquors.com',
    manager: 'Emily Davis',
    status: 'inactive',
    created_at: '2023-04-05',
  },
  {
    id: 5,
    name: 'Beachside Beverages',
    address: '202 Beach Rd, Beachside',
    city: 'Goa',
    state: 'Goa',
    pincode: '403001',
    phone: '9876543214',
    email: 'beachside@abcliquors.com',
    manager: 'Michael Wilson',
    status: 'active',
    created_at: '2023-05-15',
  },
];

// Mock data for managers (for dropdown)
const mockManagers = [
  { id: 1, name: 'John Doe' },
  { id: 2, name: 'Jane Smith' },
  { id: 3, name: 'Robert Johnson' },
  { id: 4, name: 'Emily Davis' },
  { id: 5, name: 'Michael Wilson' },
  { id: 6, name: 'Sarah Brown' },
  { id: 7, name: 'David Miller' },
];

// Validation schema for shop form
const shopValidationSchema = Yup.object({
  name: Yup.string().required('Shop name is required'),
  address: Yup.string().required('Address is required'),
  city: Yup.string().required('City is required'),
  state: Yup.string().required('State is required'),
  pincode: Yup.string()
    .matches(/^\d{6}$/, 'Pincode must be 6 digits')
    .required('Pincode is required'),
  phone: Yup.string()
    .matches(/^\d{10}$/, 'Phone number must be 10 digits')
    .required('Phone number is required'),
  email: Yup.string().email('Invalid email address').required('Email is required'),
  manager_id: Yup.number().required('Manager is required'),
});

/**
 * Shops Management component for Tenant Admin
 */
const ShopsManagement: React.FC = () => {
  const { common, shops } = useTranslations();
  const theme = useTheme();
  const { confirm } = useGlobalConfirmDialog();
  const [searchQuery, setSearchQuery] = useState('');
  const [filterAnchorEl, setFilterAnchorEl] = useState<null | HTMLElement>(null);
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [cityFilter, setCityFilter] = useState<string>('all');
  const [openShopDialog, setOpenShopDialog] = useState(false);
  const [selectedShop, setSelectedShop] = useState<any | null>(null);
  const [actionAnchorEl, setActionAnchorEl] = useState<{ [key: number]: HTMLElement | null }>({});
  const [tabValue, setTabValue] = useState(0);

  // Form validation for shop dialog
  const { formik } = useFormValidation({
    initialValues: {
      name: '',
      address: '',
      city: '',
      state: '',
      pincode: '',
      phone: '',
      email: '',
      manager_id: null as number | null,
      license_number: '',
      opening_time: '09:00',
      closing_time: '21:00',
      is_24_hours: false,
      has_parking: false,
      notes: '',
    },
    validationSchema: shopValidationSchema,
    onSubmit: (values) => {
      console.log('Form submitted:', values);
      handleCloseShopDialog();
      // In a real app, you would make an API call to create/update the shop
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

  // Handle opening the action menu for a shop
  const handleActionClick = (event: React.MouseEvent<HTMLElement>, shopId: number) => {
    setActionAnchorEl({ ...actionAnchorEl, [shopId]: event.currentTarget });
  };

  // Handle closing the action menu for a shop
  const handleActionClose = (shopId: number) => {
    setActionAnchorEl({ ...actionAnchorEl, [shopId]: null });
  };

  // Handle opening the shop dialog for creating a new shop
  const handleOpenCreateShopDialog = () => {
    setSelectedShop(null);
    formik.resetForm();
    setOpenShopDialog(true);
  };

  // Handle opening the shop dialog for editing an existing shop
  const handleOpenEditShopDialog = (shop: any) => {
    setSelectedShop(shop);
    formik.setValues({
      name: shop.name,
      address: shop.address,
      city: shop.city,
      state: shop.state,
      pincode: shop.pincode,
      phone: shop.phone,
      email: shop.email,
      manager_id: mockManagers.find(m => m.name === shop.manager)?.id || null,
      license_number: shop.license_number || '',
      opening_time: shop.opening_time || '09:00',
      closing_time: shop.closing_time || '21:00',
      is_24_hours: shop.is_24_hours || false,
      has_parking: shop.has_parking || false,
      notes: shop.notes || '',
    });
    setOpenShopDialog(true);
    handleActionClose(shop.id);
  };

  // Handle closing the shop dialog
  const handleCloseShopDialog = () => {
    setOpenShopDialog(false);
  };

  // Handle deleting a shop
  const handleDeleteShop = async (shop: any) => {
    const confirmed = await confirm({
      title: shops('deleteShop'),
      message: `${shops('confirmDeleteShop')} "${shop.name}"?`,
      confirmButtonColor: 'error',
      confirmText: common('delete'),
      cancelText: common('cancel'),
    });

    if (confirmed) {
      console.log('Deleting shop:', shop);
      // In a real app, you would make an API call to delete the shop
    }

    handleActionClose(shop.id);
  };

  // Handle changing the status of a shop
  const handleToggleShopStatus = async (shop: any) => {
    const newStatus = shop.status === 'active' ? 'inactive' : 'active';
    const confirmed = await confirm({
      title: newStatus === 'active' ? shops('activateShop') : shops('deactivateShop'),
      message: newStatus === 'active'
        ? `${shops('confirmActivateShop')} "${shop.name}"?`
        : `${shops('confirmDeactivateShop')} "${shop.name}"?`,
      confirmButtonColor: newStatus === 'active' ? 'success' : 'warning',
      confirmText: newStatus === 'active' ? common('activate') : common('deactivate'),
      cancelText: common('cancel'),
    });

    if (confirmed) {
      console.log('Toggling shop status:', shop, newStatus);
      // In a real app, you would make an API call to update the shop status
    }

    handleActionClose(shop.id);
  };

  // Handle tab change
  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  // Get unique cities for filter
  const uniqueCities = Array.from(new Set(mockShops.map(shop => shop.city)));

  // Filter shops based on search query and filters
  const filteredShops = mockShops.filter((shop) => {
    const matchesSearch = shop.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      shop.address.toLowerCase().includes(searchQuery.toLowerCase()) ||
      shop.manager.toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesStatus = statusFilter === 'all' || shop.status === statusFilter;
    const matchesCity = cityFilter === 'all' || shop.city === cityFilter;
    
    return matchesSearch && matchesStatus && matchesCity;
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
      field: 'address',
      headerName: common('address'),
      flex: 1.5,
      renderCell: (params: any) => (
        <Box>
          <Typography variant="body2">
            {params.address}
          </Typography>
          <Typography variant="body2" color="textSecondary">
            {`${params.city}, ${params.state} - ${params.pincode}`}
          </Typography>
        </Box>
      ),
    },
    {
      field: 'phone',
      headerName: common('phone'),
      flex: 0.7,
    },
    {
      field: 'manager',
      headerName: shops('manager'),
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
      field: 'created_at',
      headerName: shops('createdAt'),
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
            <MenuItem onClick={() => handleOpenEditShopDialog(params)}>
              <EditIcon fontSize="small" sx={{ mr: 1 }} />
              {common('edit')}
            </MenuItem>
            <MenuItem
              onClick={() => handleToggleShopStatus(params)}
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
            <MenuItem onClick={() => handleDeleteShop(params)} sx={{ color: 'error.main' }}>
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
        title={shops('shops')}
        subtitle={shops('manageShops')}
        icon={<StoreIcon fontSize="large" />}
      />

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Tabs
            value={tabValue}
            onChange={handleTabChange}
            indicatorColor="primary"
            textColor="primary"
            variant="fullWidth"
            aria-label="shop tabs"
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
                    <Typography variant="subtitle2">{common('city')}</Typography>
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setCityFilter('all');
                      handleFilterClose();
                    }}
                    selected={cityFilter === 'all'}
                  >
                    {common('all')}
                  </MenuItem>
                  {uniqueCities.map((city) => (
                    <MenuItem
                      key={city}
                      onClick={() => {
                        setCityFilter(city);
                        handleFilterClose();
                      }}
                      selected={cityFilter === city}
                    >
                      {city}
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
                onClick={handleOpenCreateShopDialog}
              >
                {shops('addShop')}
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <DataTable
        columns={columns}
        data={filteredShops}
        keyField="id"
        pagination
        paginationPerPage={10}
        paginationTotalRows={filteredShops.length}
      />

      {/* Shop Dialog */}
      <Dialog open={openShopDialog} onClose={handleCloseShopDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          {selectedShop ? shops('editShop') : shops('addShop')}
        </DialogTitle>
        <form onSubmit={formik.handleSubmit}>
          <DialogContent>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <Typography variant="subtitle1" gutterBottom>
                  {shops('basicInfo')}
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
                  id="license_number"
                  name="license_number"
                  label={shops('licenseNumber')}
                  value={formik.values.license_number}
                  onChange={formik.handleChange}
                  margin="normal"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  id="address"
                  name="address"
                  label={common('address')}
                  value={formik.values.address}
                  onChange={formik.handleChange}
                  error={formik.touched.address && Boolean(formik.errors.address)}
                  helperText={formik.touched.address && formik.errors.address}
                  margin="normal"
                />
              </Grid>
              <Grid item xs={12} sm={4}>
                <TextField
                  fullWidth
                  id="city"
                  name="city"
                  label={common('city')}
                  value={formik.values.city}
                  onChange={formik.handleChange}
                  error={formik.touched.city && Boolean(formik.errors.city)}
                  helperText={formik.touched.city && formik.errors.city}
                  margin="normal"
                />
              </Grid>
              <Grid item xs={12} sm={4}>
                <TextField
                  fullWidth
                  id="state"
                  name="state"
                  label={common('state')}
                  value={formik.values.state}
                  onChange={formik.handleChange}
                  error={formik.touched.state && Boolean(formik.errors.state)}
                  helperText={formik.touched.state && formik.errors.state}
                  margin="normal"
                />
              </Grid>
              <Grid item xs={12} sm={4}>
                <TextField
                  fullWidth
                  id="pincode"
                  name="pincode"
                  label={common('pincode')}
                  value={formik.values.pincode}
                  onChange={formik.handleChange}
                  error={formik.touched.pincode && Boolean(formik.errors.pincode)}
                  helperText={formik.touched.pincode && formik.errors.pincode}
                  margin="normal"
                />
              </Grid>
              <Grid item xs={12}>
                <Typography variant="subtitle1" gutterBottom sx={{ mt: 2 }}>
                  {shops('contactInfo')}
                </Typography>
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
                  <InputLabel id="manager-label">{shops('manager')}</InputLabel>
                  <Select
                    labelId="manager-label"
                    id="manager_id"
                    name="manager_id"
                    value={formik.values.manager_id}
                    onChange={formik.handleChange}
                    error={formik.touched.manager_id && Boolean(formik.errors.manager_id)}
                    label={shops('manager')}
                  >
                    {mockManagers.map((manager) => (
                      <MenuItem key={manager.id} value={manager.id}>
                        {manager.name}
                      </MenuItem>
                    ))}
                  </Select>
                  {formik.touched.manager_id && formik.errors.manager_id && (
                    <FormHelperText error>{formik.errors.manager_id}</FormHelperText>
                  )}
                </FormControl>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="subtitle1" gutterBottom sx={{ mt: 2 }}>
                  {shops('operationalInfo')}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  id="opening_time"
                  name="opening_time"
                  label={shops('openingTime')}
                  type="time"
                  value={formik.values.opening_time}
                  onChange={formik.handleChange}
                  margin="normal"
                  InputLabelProps={{
                    shrink: true,
                  }}
                  inputProps={{
                    step: 300, // 5 min
                  }}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  id="closing_time"
                  name="closing_time"
                  label={shops('closingTime')}
                  type="time"
                  value={formik.values.closing_time}
                  onChange={formik.handleChange}
                  margin="normal"
                  InputLabelProps={{
                    shrink: true,
                  }}
                  inputProps={{
                    step: 300, // 5 min
                  }}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  id="notes"
                  name="notes"
                  label={common('notes')}
                  multiline
                  rows={3}
                  value={formik.values.notes}
                  onChange={formik.handleChange}
                  margin="normal"
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseShopDialog}>{common('cancel')}</Button>
            <Button type="submit" variant="contained" color="primary">
              {selectedShop ? common('save') : common('add')}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Container>
  );
};

export default ShopsManagement;