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
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  useTheme,
} from '@mui/material';
import {
  Search as SearchIcon,
  Add as AddIcon,
  FilterList as FilterListIcon,
  MoreVert as MoreVertIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Inventory as InventoryIcon,
  LocalShipping as LocalShippingIcon,
  Warning as WarningIcon,
  Print as PrintIcon,
  Visibility as VisibilityIcon,
  SwapHoriz as SwapHorizIcon,
  Download as DownloadIcon,
  Upload as UploadIcon,
} from '@mui/icons-material';
import { DataTable, PageHeader } from '../../components/common';
import { useTranslations, useFormValidation, useGlobalConfirmDialog } from '../../hooks';
import * as Yup from 'yup';

// Mock data for inventory
const mockInventory = [
  {
    id: 1,
    name: 'Jack Daniels Whiskey',
    category: 'Whiskey',
    brand: 'Jack Daniels',
    size: '750ml',
    price: 2500,
    cost_price: 2000,
    stock: 15,
    threshold: 10,
    status: 'in_stock',
  },
  {
    id: 2,
    name: 'Absolut Vodka',
    category: 'Vodka',
    brand: 'Absolut',
    size: '750ml',
    price: 1800,
    cost_price: 1500,
    stock: 8,
    threshold: 8,
    status: 'low_stock',
  },
  {
    id: 3,
    name: 'Corona Beer (6-pack)',
    category: 'Beer',
    brand: 'Corona',
    size: '330ml x 6',
    price: 600,
    cost_price: 450,
    stock: 24,
    threshold: 12,
    status: 'in_stock',
  },
  {
    id: 4,
    name: 'Bacardi Rum',
    category: 'Rum',
    brand: 'Bacardi',
    size: '750ml',
    price: 1200,
    cost_price: 950,
    stock: 12,
    threshold: 8,
    status: 'in_stock',
  },
  {
    id: 5,
    name: 'Johnnie Walker Black Label',
    category: 'Whiskey',
    brand: 'Johnnie Walker',
    size: '750ml',
    price: 3500,
    cost_price: 2800,
    stock: 5,
    threshold: 6,
    status: 'low_stock',
  },
  {
    id: 6,
    name: 'Smirnoff Vodka',
    category: 'Vodka',
    brand: 'Smirnoff',
    size: '750ml',
    price: 1200,
    cost_price: 900,
    stock: 18,
    threshold: 10,
    status: 'in_stock',
  },
  {
    id: 7,
    name: 'Kingfisher Beer (6-pack)',
    category: 'Beer',
    brand: 'Kingfisher',
    size: '330ml x 6',
    price: 500,
    cost_price: 380,
    stock: 36,
    threshold: 15,
    status: 'in_stock',
  },
  {
    id: 8,
    name: 'Old Monk Rum',
    category: 'Rum',
    brand: 'Old Monk',
    size: '750ml',
    price: 800,
    cost_price: 600,
    stock: 3,
    threshold: 5,
    status: 'low_stock',
  },
  {
    id: 9,
    name: 'Blenders Pride Whiskey',
    category: 'Whiskey',
    brand: 'Blenders Pride',
    size: '750ml',
    price: 1500,
    cost_price: 1200,
    stock: 10,
    threshold: 8,
    status: 'in_stock',
  },
  {
    id: 10,
    name: 'Bira White Beer (6-pack)',
    category: 'Beer',
    brand: 'Bira',
    size: '330ml x 6',
    price: 700,
    cost_price: 550,
    stock: 28,
    threshold: 12,
    status: 'in_stock',
  },
];

// Mock data for categories
const mockCategories = [
  { id: 1, name: 'Whiskey' },
  { id: 2, name: 'Vodka' },
  { id: 3, name: 'Rum' },
  { id: 4, name: 'Beer' },
  { id: 5, name: 'Wine' },
  { id: 6, name: 'Gin' },
];

// Mock data for brands
const mockBrands = [
  { id: 1, name: 'Jack Daniels', category_id: 1 },
  { id: 2, name: 'Johnnie Walker', category_id: 1 },
  { id: 3, name: 'Blenders Pride', category_id: 1 },
  { id: 4, name: 'Absolut', category_id: 2 },
  { id: 5, name: 'Smirnoff', category_id: 2 },
  { id: 6, name: 'Bacardi', category_id: 3 },
  { id: 7, name: 'Old Monk', category_id: 3 },
  { id: 8, name: 'Corona', category_id: 4 },
  { id: 9, name: 'Kingfisher', category_id: 4 },
  { id: 10, name: 'Bira', category_id: 4 },
];

// Validation schema for stock adjustment
const stockAdjustmentSchema = Yup.object({
  product_id: Yup.number().required('Product is required'),
  adjustment_type: Yup.string().oneOf(['increase', 'decrease']).required('Adjustment type is required'),
  quantity: Yup.number().positive('Quantity must be positive').required('Quantity is required'),
  reason: Yup.string().required('Reason is required'),
  notes: Yup.string(),
});

// Validation schema for stock transfer
const stockTransferSchema = Yup.object({
  product_id: Yup.number().required('Product is required'),
  from_shop_id: Yup.number().required('Source shop is required'),
  to_shop_id: Yup.number().required('Destination shop is required'),
  quantity: Yup.number().positive('Quantity must be positive').required('Quantity is required'),
  notes: Yup.string(),
});

/**
 * Inventory Management component for Assistant Manager
 */
const InventoryManagement: React.FC = () => {
  const { common, inventory } = useTranslations();
  const theme = useTheme();
  const { confirm } = useGlobalConfirmDialog();
  const [searchQuery, setSearchQuery] = useState('');
  const [filterAnchorEl, setFilterAnchorEl] = useState<null | HTMLElement>(null);
  const [categoryFilter, setCategoryFilter] = useState<string>('all');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [openStockAdjustmentDialog, setOpenStockAdjustmentDialog] = useState(false);
  const [openStockTransferDialog, setOpenStockTransferDialog] = useState(false);
  const [actionAnchorEl, setActionAnchorEl] = useState<{ [key: number]: HTMLElement | null }>({});
  const [tabValue, setTabValue] = useState(0);

  // Form validation for stock adjustment
  const stockAdjustmentForm = useFormValidation({
    initialValues: {
      product_id: '',
      adjustment_type: 'increase',
      quantity: '',
      reason: '',
      notes: '',
    },
    validationSchema: stockAdjustmentSchema,
    onSubmit: (values) => {
      console.log('Stock adjustment submitted:', values);
      // In a real app, you would make an API call to adjust the stock
      handleCloseStockAdjustmentDialog();
    },
  });

  // Form validation for stock transfer
  const stockTransferForm = useFormValidation({
    initialValues: {
      product_id: '',
      from_shop_id: '',
      to_shop_id: '',
      quantity: '',
      notes: '',
    },
    validationSchema: stockTransferSchema,
    onSubmit: (values) => {
      console.log('Stock transfer submitted:', values);
      // In a real app, you would make an API call to transfer the stock
      handleCloseStockTransferDialog();
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

  // Handle opening the action menu for a product
  const handleActionClick = (event: React.MouseEvent<HTMLElement>, productId: number) => {
    setActionAnchorEl({ ...actionAnchorEl, [productId]: event.currentTarget });
  };

  // Handle closing the action menu for a product
  const handleActionClose = (productId: number) => {
    setActionAnchorEl({ ...actionAnchorEl, [productId]: null });
  };

  // Handle opening the stock adjustment dialog
  const handleOpenStockAdjustmentDialog = (product?: any) => {
    if (product) {
      stockAdjustmentForm.formik.setFieldValue('product_id', product.id);
    }
    setOpenStockAdjustmentDialog(true);
  };

  // Handle closing the stock adjustment dialog
  const handleCloseStockAdjustmentDialog = () => {
    stockAdjustmentForm.formik.resetForm();
    setOpenStockAdjustmentDialog(false);
  };

  // Handle opening the stock transfer dialog
  const handleOpenStockTransferDialog = (product?: any) => {
    if (product) {
      stockTransferForm.formik.setFieldValue('product_id', product.id);
    }
    setOpenStockTransferDialog(true);
  };

  // Handle closing the stock transfer dialog
  const handleCloseStockTransferDialog = () => {
    stockTransferForm.formik.resetForm();
    setOpenStockTransferDialog(false);
  };

  // Handle tab change
  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  // Filter inventory based on search query and filters
  const filteredInventory = mockInventory.filter((product) => {
    const matchesSearch = product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      product.brand.toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesCategory = categoryFilter === 'all' || product.category === categoryFilter;
    const matchesStatus = statusFilter === 'all' || product.status === statusFilter;
    
    return matchesSearch && matchesCategory && matchesStatus;
  });

  // Define columns for the data table
  const columns = [
    {
      field: 'name',
      headerName: common('product'),
      flex: 1.5,
      renderCell: (params: any) => (
        <Box>
          <Typography variant="body1" fontWeight={500}>
            {params.name}
          </Typography>
          <Typography variant="body2" color="textSecondary">
            {params.brand} • {params.size}
          </Typography>
        </Box>
      ),
    },
    {
      field: 'category',
      headerName: common('category'),
      flex: 0.8,
    },
    {
      field: 'price',
      headerName: common('price'),
      flex: 0.8,
      renderCell: (params: any) => (
        <Box>
          <Typography variant="body2" fontWeight={500}>
            ₹{params.price.toLocaleString()}
          </Typography>
          <Typography variant="caption" color="textSecondary">
            Cost: ₹{params.cost_price.toLocaleString()}
          </Typography>
        </Box>
      ),
    },
    {
      field: 'stock',
      headerName: common('stock'),
      flex: 0.8,
      renderCell: (params: any) => (
        <Box>
          <Typography
            variant="body2"
            fontWeight={500}
            color={
              params.stock === 0
                ? 'error.main'
                : params.stock < params.threshold
                ? 'warning.main'
                : 'text.primary'
            }
          >
            {params.stock} {common('units')}
          </Typography>
          <Typography variant="caption" color="textSecondary">
            {inventory('threshold')}: {params.threshold}
          </Typography>
        </Box>
      ),
    },
    {
      field: 'status',
      headerName: common('status'),
      flex: 0.8,
      renderCell: (params: any) => (
        <Chip
          label={
            params.status === 'in_stock'
              ? inventory('inStock')
              : params.status === 'low_stock'
              ? inventory('lowStock')
              : inventory('outOfStock')
          }
          color={
            params.status === 'in_stock'
              ? 'success'
              : params.status === 'low_stock'
              ? 'warning'
              : 'error'
          }
          size="small"
        />
      ),
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
            <MenuItem onClick={() => {
              handleActionClose(params.id);
              handleOpenStockAdjustmentDialog(params);
            }}>
              <InventoryIcon fontSize="small" sx={{ mr: 1 }} />
              {inventory('adjustStock')}
            </MenuItem>
            <MenuItem onClick={() => {
              handleActionClose(params.id);
              handleOpenStockTransferDialog(params);
            }}>
              <SwapHorizIcon fontSize="small" sx={{ mr: 1 }} />
              {inventory('transferStock')}
            </MenuItem>
            <MenuItem onClick={() => {
              handleActionClose(params.id);
              console.log('View product details', params.id);
            }}>
              <VisibilityIcon fontSize="small" sx={{ mr: 1 }} />
              {common('view')}
            </MenuItem>
          </Menu>
        </>
      ),
    },
  ];

  return (
    <Container maxWidth="xl">
      <PageHeader
        title={inventory('inventoryManagement')}
        subtitle={inventory('manageInventory')}
        icon={<InventoryIcon fontSize="large" />}
      />

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Tabs
            value={tabValue}
            onChange={handleTabChange}
            indicatorColor="primary"
            textColor="primary"
            variant="fullWidth"
            aria-label="inventory tabs"
          >
            <Tab label={common('all')} />
            <Tab label={inventory('lowStock')} />
            <Tab label={inventory('outOfStock')} />
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
                    <Typography variant="subtitle2">{common('category')}</Typography>
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setCategoryFilter('all');
                      handleFilterClose();
                    }}
                    selected={categoryFilter === 'all'}
                  >
                    {common('all')}
                  </MenuItem>
                  {mockCategories.map((category) => (
                    <MenuItem
                      key={category.id}
                      onClick={() => {
                        setCategoryFilter(category.name);
                        handleFilterClose();
                      }}
                      selected={categoryFilter === category.name}
                    >
                      {category.name}
                    </MenuItem>
                  ))}
                  <Divider />
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
                      setStatusFilter('in_stock');
                      handleFilterClose();
                    }}
                    selected={statusFilter === 'in_stock'}
                  >
                    {inventory('inStock')}
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setStatusFilter('low_stock');
                      handleFilterClose();
                    }}
                    selected={statusFilter === 'low_stock'}
                  >
                    {inventory('lowStock')}
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setStatusFilter('out_of_stock');
                      handleFilterClose();
                    }}
                    selected={statusFilter === 'out_of_stock'}
                  >
                    {inventory('outOfStock')}
                  </MenuItem>
                </Menu>
              </Box>
            </Grid>
            <Grid item xs={12} sm={12} md={4} sx={{ display: 'flex', justifyContent: 'flex-end', gap: 1 }}>
              <Button
                variant="outlined"
                color="primary"
                startIcon={<DownloadIcon />}
                onClick={() => console.log('Export inventory')}
              >
                {common('export')}
              </Button>
              <Button
                variant="outlined"
                color="primary"
                startIcon={<InventoryIcon />}
                onClick={() => handleOpenStockAdjustmentDialog()}
              >
                {inventory('adjustStock')}
              </Button>
              <Button
                variant="contained"
                color="primary"
                startIcon={<SwapHorizIcon />}
                onClick={() => handleOpenStockTransferDialog()}
              >
                {inventory('transferStock')}
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <DataTable
        columns={columns}
        data={filteredInventory}
        keyField="id"
        pagination
        paginationPerPage={10}
        paginationTotalRows={filteredInventory.length}
      />

      {/* Stock Adjustment Dialog */}
      <Dialog open={openStockAdjustmentDialog} onClose={handleCloseStockAdjustmentDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {inventory('adjustStock')}
        </DialogTitle>
        <form onSubmit={stockAdjustmentForm.formik.handleSubmit}>
          <DialogContent>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <FormControl fullWidth margin="normal" error={stockAdjustmentForm.formik.touched.product_id && Boolean(stockAdjustmentForm.formik.errors.product_id)}>
                  <InputLabel id="product-label">{common('product')}</InputLabel>
                  <Select
                    labelId="product-label"
                    id="product_id"
                    name="product_id"
                    value={stockAdjustmentForm.formik.values.product_id}
                    onChange={stockAdjustmentForm.formik.handleChange}
                    label={common('product')}
                  >
                    {mockInventory.map((product) => (
                      <MenuItem key={product.id} value={product.id}>
                        {product.name} ({product.brand})
                      </MenuItem>
                    ))}
                  </Select>
                  {stockAdjustmentForm.formik.touched.product_id && stockAdjustmentForm.formik.errors.product_id && (
                    <FormHelperText>{stockAdjustmentForm.formik.errors.product_id}</FormHelperText>
                  )}
                </FormControl>
              </Grid>
              <Grid item xs={12}>
                <FormControl fullWidth margin="normal" error={stockAdjustmentForm.formik.touched.adjustment_type && Boolean(stockAdjustmentForm.formik.errors.adjustment_type)}>
                  <InputLabel id="adjustment-type-label">{inventory('adjustmentType')}</InputLabel>
                  <Select
                    labelId="adjustment-type-label"
                    id="adjustment_type"
                    name="adjustment_type"
                    value={stockAdjustmentForm.formik.values.adjustment_type}
                    onChange={stockAdjustmentForm.formik.handleChange}
                    label={inventory('adjustmentType')}
                  >
                    <MenuItem value="increase">{inventory('increase')}</MenuItem>
                    <MenuItem value="decrease">{inventory('decrease')}</MenuItem>
                  </Select>
                  {stockAdjustmentForm.formik.touched.adjustment_type && stockAdjustmentForm.formik.errors.adjustment_type && (
                    <FormHelperText>{stockAdjustmentForm.formik.errors.adjustment_type}</FormHelperText>
                  )}
                </FormControl>
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  id="quantity"
                  name="quantity"
                  label={common('quantity')}
                  type="number"
                  value={stockAdjustmentForm.formik.values.quantity}
                  onChange={stockAdjustmentForm.formik.handleChange}
                  error={stockAdjustmentForm.formik.touched.quantity && Boolean(stockAdjustmentForm.formik.errors.quantity)}
                  helperText={stockAdjustmentForm.formik.touched.quantity && stockAdjustmentForm.formik.errors.quantity}
                  margin="normal"
                />
              </Grid>
              <Grid item xs={12}>
                <FormControl fullWidth margin="normal" error={stockAdjustmentForm.formik.touched.reason && Boolean(stockAdjustmentForm.formik.errors.reason)}>
                  <InputLabel id="reason-label">{inventory('reason')}</InputLabel>
                  <Select
                    labelId="reason-label"
                    id="reason"
                    name="reason"
                    value={stockAdjustmentForm.formik.values.reason}
                    onChange={stockAdjustmentForm.formik.handleChange}
                    label={inventory('reason')}
                  >
                    <MenuItem value="damaged">{inventory('damaged')}</MenuItem>
                    <MenuItem value="expired">{inventory('expired')}</MenuItem>
                    <MenuItem value="theft">{inventory('theft')}</MenuItem>
                    <MenuItem value="correction">{inventory('correction')}</MenuItem>
                    <MenuItem value="other">{common('other')}</MenuItem>
                  </Select>
                  {stockAdjustmentForm.formik.touched.reason && stockAdjustmentForm.formik.errors.reason && (
                    <FormHelperText>{stockAdjustmentForm.formik.errors.reason}</FormHelperText>
                  )}
                </FormControl>
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  id="notes"
                  name="notes"
                  label={common('notes')}
                  multiline
                  rows={3}
                  value={stockAdjustmentForm.formik.values.notes}
                  onChange={stockAdjustmentForm.formik.handleChange}
                  error={stockAdjustmentForm.formik.touched.notes && Boolean(stockAdjustmentForm.formik.errors.notes)}
                  helperText={stockAdjustmentForm.formik.touched.notes && stockAdjustmentForm.formik.errors.notes}
                  margin="normal"
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseStockAdjustmentDialog}>{common('cancel')}</Button>
            <Button type="submit" variant="contained" color="primary">
              {common('submit')}
            </Button>
          </DialogActions>
        </form>
      </Dialog>

      {/* Stock Transfer Dialog */}
      <Dialog open={openStockTransferDialog} onClose={handleCloseStockTransferDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {inventory('transferStock')}
        </DialogTitle>
        <form onSubmit={stockTransferForm.formik.handleSubmit}>
          <DialogContent>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <FormControl fullWidth margin="normal" error={stockTransferForm.formik.touched.product_id && Boolean(stockTransferForm.formik.errors.product_id)}>
                  <InputLabel id="product-label">{common('product')}</InputLabel>
                  <Select
                    labelId="product-label"
                    id="product_id"
                    name="product_id"
                    value={stockTransferForm.formik.values.product_id}
                    onChange={stockTransferForm.formik.handleChange}
                    label={common('product')}
                  >
                    {mockInventory.map((product) => (
                      <MenuItem key={product.id} value={product.id}>
                        {product.name} ({product.brand}) - {product.stock} {common('units')}
                      </MenuItem>
                    ))}
                  </Select>
                  {stockTransferForm.formik.touched.product_id && stockTransferForm.formik.errors.product_id && (
                    <FormHelperText>{stockTransferForm.formik.errors.product_id}</FormHelperText>
                  )}
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth margin="normal" error={stockTransferForm.formik.touched.from_shop_id && Boolean(stockTransferForm.formik.errors.from_shop_id)}>
                  <InputLabel id="from-shop-label">{inventory('fromShop')}</InputLabel>
                  <Select
                    labelId="from-shop-label"
                    id="from_shop_id"
                    name="from_shop_id"
                    value={stockTransferForm.formik.values.from_shop_id}
                    onChange={stockTransferForm.formik.handleChange}
                    label={inventory('fromShop')}
                  >
                    <MenuItem value={1}>Downtown Store</MenuItem>
                    <MenuItem value={2}>Uptown Store</MenuItem>
                    <MenuItem value={3}>Central Store</MenuItem>
                  </Select>
                  {stockTransferForm.formik.touched.from_shop_id && stockTransferForm.formik.errors.from_shop_id && (
                    <FormHelperText>{stockTransferForm.formik.errors.from_shop_id}</FormHelperText>
                  )}
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth margin="normal" error={stockTransferForm.formik.touched.to_shop_id && Boolean(stockTransferForm.formik.errors.to_shop_id)}>
                  <InputLabel id="to-shop-label">{inventory('toShop')}</InputLabel>
                  <Select
                    labelId="to-shop-label"
                    id="to_shop_id"
                    name="to_shop_id"
                    value={stockTransferForm.formik.values.to_shop_id}
                    onChange={stockTransferForm.formik.handleChange}
                    label={inventory('toShop')}
                  >
                    <MenuItem value={1}>Downtown Store</MenuItem>
                    <MenuItem value={2}>Uptown Store</MenuItem>
                    <MenuItem value={3}>Central Store</MenuItem>
                  </Select>
                  {stockTransferForm.formik.touched.to_shop_id && stockTransferForm.formik.errors.to_shop_id && (
                    <FormHelperText>{stockTransferForm.formik.errors.to_shop_id}</FormHelperText>
                  )}
                </FormControl>
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  id="quantity"
                  name="quantity"
                  label={common('quantity')}
                  type="number"
                  value={stockTransferForm.formik.values.quantity}
                  onChange={stockTransferForm.formik.handleChange}
                  error={stockTransferForm.formik.touched.quantity && Boolean(stockTransferForm.formik.errors.quantity)}
                  helperText={stockTransferForm.formik.touched.quantity && stockTransferForm.formik.errors.quantity}
                  margin="normal"
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
                  value={stockTransferForm.formik.values.notes}
                  onChange={stockTransferForm.formik.handleChange}
                  error={stockTransferForm.formik.touched.notes && Boolean(stockTransferForm.formik.errors.notes)}
                  helperText={stockTransferForm.formik.touched.notes && stockTransferForm.formik.errors.notes}
                  margin="normal"
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseStockTransferDialog}>{common('cancel')}</Button>
            <Button type="submit" variant="contained" color="primary">
              {common('submit')}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Container>
  );
};

export default InventoryManagement;