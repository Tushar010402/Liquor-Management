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
  Inventory as InventoryIcon,
  ArrowUpward as ArrowUpwardIcon,
  ArrowDownward as ArrowDownwardIcon,
  Warning as WarningIcon,
  QrCode as QrCodeIcon,
  Upload as UploadIcon,
  Download as DownloadIcon,
} from '@mui/icons-material';
import { DataTable, PageHeader } from '../../components/common';
import { useTranslations, useFormValidation, useGlobalConfirmDialog } from '../../hooks';
import * as Yup from 'yup';

// Mock data for products
const mockProducts = [
  {
    id: 1,
    name: 'Jack Daniels Whiskey',
    category: 'Whiskey',
    brand: 'Jack Daniels',
    price: 2500,
    cost_price: 2000,
    stock: 15,
    threshold: 10,
    barcode: '8901234567890',
    status: 'active',
    created_at: '2023-01-15',
  },
  {
    id: 2,
    name: 'Absolut Vodka',
    category: 'Vodka',
    brand: 'Absolut',
    price: 1800,
    cost_price: 1400,
    stock: 8,
    threshold: 8,
    barcode: '8901234567891',
    status: 'active',
    created_at: '2023-02-20',
  },
  {
    id: 3,
    name: 'Corona Beer',
    category: 'Beer',
    brand: 'Corona',
    price: 250,
    cost_price: 180,
    stock: 24,
    threshold: 20,
    barcode: '8901234567892',
    status: 'active',
    created_at: '2023-03-10',
  },
  {
    id: 4,
    name: 'Bacardi Rum',
    category: 'Rum',
    brand: 'Bacardi',
    price: 1200,
    cost_price: 900,
    stock: 12,
    threshold: 10,
    barcode: '8901234567893',
    status: 'active',
    created_at: '2023-04-05',
  },
  {
    id: 5,
    name: 'Johnnie Walker Black Label',
    category: 'Whiskey',
    brand: 'Johnnie Walker',
    price: 3500,
    cost_price: 2800,
    stock: 5,
    threshold: 5,
    barcode: '8901234567894',
    status: 'active',
    created_at: '2023-05-15',
  },
  {
    id: 6,
    name: 'Smirnoff Vodka',
    category: 'Vodka',
    brand: 'Smirnoff',
    price: 1200,
    cost_price: 900,
    stock: 18,
    threshold: 12,
    barcode: '8901234567895',
    status: 'active',
    created_at: '2023-06-10',
  },
  {
    id: 7,
    name: 'Kingfisher Beer',
    category: 'Beer',
    brand: 'Kingfisher',
    price: 150,
    cost_price: 100,
    stock: 36,
    threshold: 24,
    barcode: '8901234567896',
    status: 'active',
    created_at: '2023-07-05',
  },
  {
    id: 8,
    name: 'Old Monk Rum',
    category: 'Rum',
    brand: 'Old Monk',
    price: 800,
    cost_price: 600,
    stock: 3,
    threshold: 10,
    barcode: '8901234567897',
    status: 'active',
    created_at: '2023-08-15',
  },
  {
    id: 9,
    name: 'Blenders Pride Whiskey',
    category: 'Whiskey',
    brand: 'Blenders Pride',
    price: 1500,
    cost_price: 1200,
    stock: 0,
    threshold: 8,
    barcode: '8901234567898',
    status: 'inactive',
    created_at: '2023-09-20',
  },
  {
    id: 10,
    name: 'Bira White Beer',
    category: 'Beer',
    brand: 'Bira',
    price: 180,
    cost_price: 130,
    stock: 28,
    threshold: 20,
    barcode: '8901234567899',
    status: 'active',
    created_at: '2023-10-05',
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
  { id: 1, name: 'Jack Daniels' },
  { id: 2, name: 'Absolut' },
  { id: 3, name: 'Corona' },
  { id: 4, name: 'Bacardi' },
  { id: 5, name: 'Johnnie Walker' },
  { id: 6, name: 'Smirnoff' },
  { id: 7, name: 'Kingfisher' },
  { id: 8, name: 'Old Monk' },
  { id: 9, name: 'Blenders Pride' },
  { id: 10, name: 'Bira' },
];

// Validation schema for product form
const productValidationSchema = Yup.object({
  name: Yup.string().required('Product name is required'),
  category_id: Yup.number().required('Category is required'),
  brand_id: Yup.number().required('Brand is required'),
  price: Yup.number()
    .positive('Price must be positive')
    .required('Price is required'),
  cost_price: Yup.number()
    .positive('Cost price must be positive')
    .required('Cost price is required'),
  stock: Yup.number()
    .min(0, 'Stock cannot be negative')
    .integer('Stock must be an integer')
    .required('Stock is required'),
  threshold: Yup.number()
    .min(0, 'Threshold cannot be negative')
    .integer('Threshold must be an integer')
    .required('Threshold is required'),
  barcode: Yup.string()
    .matches(/^\d{13}$/, 'Barcode must be 13 digits')
    .required('Barcode is required'),
});

// Validation schema for stock adjustment form
const stockAdjustmentValidationSchema = Yup.object({
  product_id: Yup.number().required('Product is required'),
  adjustment_type: Yup.string()
    .oneOf(['increase', 'decrease'], 'Invalid adjustment type')
    .required('Adjustment type is required'),
  quantity: Yup.number()
    .positive('Quantity must be positive')
    .integer('Quantity must be an integer')
    .required('Quantity is required'),
  reason: Yup.string().required('Reason is required'),
});

/**
 * Inventory Management component for Shop Manager
 */
const InventoryManagement: React.FC = () => {
  const { common, products } = useTranslations();
  const theme = useTheme();
  const { confirm } = useGlobalConfirmDialog();
  const [searchQuery, setSearchQuery] = useState('');
  const [filterAnchorEl, setFilterAnchorEl] = useState<null | HTMLElement>(null);
  const [categoryFilter, setCategoryFilter] = useState<string>('all');
  const [stockFilter, setStockFilter] = useState<string>('all');
  const [openProductDialog, setOpenProductDialog] = useState(false);
  const [openStockAdjustmentDialog, setOpenStockAdjustmentDialog] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState<any | null>(null);
  const [actionAnchorEl, setActionAnchorEl] = useState<{ [key: number]: HTMLElement | null }>({});
  const [tabValue, setTabValue] = useState(0);

  // Form validation for product dialog
  const productForm = useFormValidation({
    initialValues: {
      name: '',
      category_id: null as number | null,
      brand_id: null as number | null,
      price: '',
      cost_price: '',
      stock: 0,
      threshold: 10,
      barcode: '',
      description: '',
      image: null,
      status: 'active',
    },
    validationSchema: productValidationSchema,
    onSubmit: (values) => {
      console.log('Product form submitted:', values);
      handleCloseProductDialog();
      // In a real app, you would make an API call to create/update the product
    },
  });

  // Form validation for stock adjustment dialog
  const stockAdjustmentForm = useFormValidation({
    initialValues: {
      product_id: null as number | null,
      adjustment_type: 'increase',
      quantity: 1,
      reason: '',
      notes: '',
    },
    validationSchema: stockAdjustmentValidationSchema,
    onSubmit: (values) => {
      console.log('Stock adjustment form submitted:', values);
      handleCloseStockAdjustmentDialog();
      // In a real app, you would make an API call to adjust the stock
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

  // Handle opening the product dialog for creating a new product
  const handleOpenCreateProductDialog = () => {
    setSelectedProduct(null);
    productForm.formik.resetForm();
    setOpenProductDialog(true);
  };

  // Handle opening the product dialog for editing an existing product
  const handleOpenEditProductDialog = (product: any) => {
    setSelectedProduct(product);
    productForm.formik.setValues({
      name: product.name,
      category_id: mockCategories.find(c => c.name === product.category)?.id || null,
      brand_id: mockBrands.find(b => b.name === product.brand)?.id || null,
      price: product.price,
      cost_price: product.cost_price,
      stock: product.stock,
      threshold: product.threshold,
      barcode: product.barcode,
      description: product.description || '',
      image: null,
      status: product.status,
    });
    setOpenProductDialog(true);
    handleActionClose(product.id);
  };

  // Handle closing the product dialog
  const handleCloseProductDialog = () => {
    setOpenProductDialog(false);
  };

  // Handle opening the stock adjustment dialog
  const handleOpenStockAdjustmentDialog = (product: any = null) => {
    if (product) {
      stockAdjustmentForm.formik.setValues({
        product_id: product.id,
        adjustment_type: 'increase',
        quantity: 1,
        reason: '',
        notes: '',
      });
      handleActionClose(product.id);
    } else {
      stockAdjustmentForm.formik.resetForm();
    }
    setOpenStockAdjustmentDialog(true);
  };

  // Handle closing the stock adjustment dialog
  const handleCloseStockAdjustmentDialog = () => {
    setOpenStockAdjustmentDialog(false);
  };

  // Handle deleting a product
  const handleDeleteProduct = async (product: any) => {
    const confirmed = await confirm({
      title: products('deleteProduct'),
      message: `${products('confirmDeleteProduct')} "${product.name}"?`,
      confirmButtonColor: 'error',
      confirmText: common('delete'),
      cancelText: common('cancel'),
    });

    if (confirmed) {
      console.log('Deleting product:', product);
      // In a real app, you would make an API call to delete the product
    }

    handleActionClose(product.id);
  };

  // Handle changing the status of a product
  const handleToggleProductStatus = async (product: any) => {
    const newStatus = product.status === 'active' ? 'inactive' : 'active';
    const confirmed = await confirm({
      title: newStatus === 'active' ? products('activateProduct') : products('deactivateProduct'),
      message: newStatus === 'active'
        ? `${products('confirmActivateProduct')} "${product.name}"?`
        : `${products('confirmDeactivateProduct')} "${product.name}"?`,
      confirmButtonColor: newStatus === 'active' ? 'success' : 'warning',
      confirmText: newStatus === 'active' ? common('activate') : common('deactivate'),
      cancelText: common('cancel'),
    });

    if (confirmed) {
      console.log('Toggling product status:', product, newStatus);
      // In a real app, you would make an API call to update the product status
    }

    handleActionClose(product.id);
  };

  // Handle tab change
  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  // Get unique categories for filter
  const uniqueCategories = Array.from(new Set(mockProducts.map(product => product.category)));

  // Filter products based on search query and filters
  const filteredProducts = mockProducts.filter((product) => {
    const matchesSearch = product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      product.brand.toLowerCase().includes(searchQuery.toLowerCase()) ||
      product.barcode.includes(searchQuery);
    
    const matchesCategory = categoryFilter === 'all' || product.category === categoryFilter;
    
    const matchesStock = stockFilter === 'all' ||
      (stockFilter === 'low' && product.stock <= product.threshold) ||
      (stockFilter === 'out' && product.stock === 0) ||
      (stockFilter === 'normal' && product.stock > product.threshold);
    
    return matchesSearch && matchesCategory && matchesStock;
  });

  // Define columns for the data table
  const columns = [
    {
      field: 'name',
      headerName: common('name'),
      flex: 1.5,
      renderCell: (params: any) => (
        <Box>
          <Typography variant="body1" fontWeight={500}>
            {params.name}
          </Typography>
          <Typography variant="body2" color="textSecondary">
            {params.brand}
          </Typography>
        </Box>
      ),
    },
    {
      field: 'category',
      headerName: common('category'),
      flex: 0.7,
    },
    {
      field: 'price',
      headerName: common('price'),
      flex: 0.7,
      renderCell: (params: any) => (
        <Typography variant="body2">
          ₹{params.price.toLocaleString()}
        </Typography>
      ),
    },
    {
      field: 'stock',
      headerName: common('stock'),
      flex: 0.7,
      renderCell: (params: any) => (
        <Box>
          <Typography
            variant="body2"
            fontWeight={500}
            color={
              params.stock === 0
                ? 'error.main'
                : params.stock <= params.threshold
                ? 'warning.main'
                : 'success.main'
            }
          >
            {params.stock} {params.stock === 1 ? 'unit' : 'units'}
          </Typography>
          <Typography variant="caption" color="textSecondary">
            {products('threshold')}: {params.threshold}
          </Typography>
        </Box>
      ),
    },
    {
      field: 'barcode',
      headerName: common('barcode'),
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
            <MenuItem onClick={() => handleOpenEditProductDialog(params)}>
              <EditIcon fontSize="small" sx={{ mr: 1 }} />
              {common('edit')}
            </MenuItem>
            <MenuItem onClick={() => handleOpenStockAdjustmentDialog(params)}>
              <InventoryIcon fontSize="small" sx={{ mr: 1 }} />
              {products('adjustStock')}
            </MenuItem>
            <MenuItem
              onClick={() => handleToggleProductStatus(params)}
              sx={{ color: params.status === 'active' ? 'error.main' : 'success.main' }}
            >
              {params.status === 'active' ? (
                <>
                  <ArrowDownwardIcon fontSize="small" sx={{ mr: 1 }} />
                  {common('deactivate')}
                </>
              ) : (
                <>
                  <ArrowUpwardIcon fontSize="small" sx={{ mr: 1 }} />
                  {common('activate')}
                </>
              )}
            </MenuItem>
            <MenuItem onClick={() => handleDeleteProduct(params)} sx={{ color: 'error.main' }}>
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
        title={products('inventory')}
        subtitle={products('manageInventory')}
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
            <Tab 
              label={
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <Typography>{products('lowStock')}</Typography>
                  <Chip 
                    label={mockProducts.filter(p => p.stock <= p.threshold && p.stock > 0).length} 
                    color="warning" 
                    size="small" 
                    sx={{ ml: 1 }}
                  />
                </Box>
              } 
            />
            <Tab 
              label={
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <Typography>{products('outOfStock')}</Typography>
                  <Chip 
                    label={mockProducts.filter(p => p.stock === 0).length} 
                    color="error" 
                    size="small" 
                    sx={{ ml: 1 }}
                  />
                </Box>
              } 
            />
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
                  {uniqueCategories.map((category) => (
                    <MenuItem
                      key={category}
                      onClick={() => {
                        setCategoryFilter(category);
                        handleFilterClose();
                      }}
                      selected={categoryFilter === category}
                    >
                      {category}
                    </MenuItem>
                  ))}
                  <Divider />
                  <MenuItem sx={{ pointerEvents: 'none' }}>
                    <Typography variant="subtitle2">{common('stock')}</Typography>
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setStockFilter('all');
                      handleFilterClose();
                    }}
                    selected={stockFilter === 'all'}
                  >
                    {common('all')}
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setStockFilter('normal');
                      handleFilterClose();
                    }}
                    selected={stockFilter === 'normal'}
                  >
                    {products('normalStock')}
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setStockFilter('low');
                      handleFilterClose();
                    }}
                    selected={stockFilter === 'low'}
                  >
                    {products('lowStock')}
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setStockFilter('out');
                      handleFilterClose();
                    }}
                    selected={stockFilter === 'out'}
                  >
                    {products('outOfStock')}
                  </MenuItem>
                </Menu>
              </Box>
            </Grid>
            <Grid item xs={12} sm={12} md={4} sx={{ display: 'flex', justifyContent: 'flex-end', gap: 1 }}>
              <Button
                variant="outlined"
                color="primary"
                startIcon={<InventoryIcon />}
                onClick={() => handleOpenStockAdjustmentDialog()}
              >
                {products('adjustStock')}
              </Button>
              <Button
                variant="contained"
                color="primary"
                startIcon={<AddIcon />}
                onClick={handleOpenCreateProductDialog}
              >
                {products('addProduct')}
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <DataTable
        columns={columns}
        data={filteredProducts}
        keyField="id"
        pagination
        paginationPerPage={10}
        paginationTotalRows={filteredProducts.length}
      />

      {/* Product Dialog */}
      <Dialog open={openProductDialog} onClose={handleCloseProductDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          {selectedProduct ? products('editProduct') : products('addProduct')}
        </DialogTitle>
        <form onSubmit={productForm.formik.handleSubmit}>
          <DialogContent>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <Typography variant="subtitle1" gutterBottom>
                  {products('basicInfo')}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  id="name"
                  name="name"
                  label={common('name')}
                  value={productForm.formik.values.name}
                  onChange={productForm.formik.handleChange}
                  error={productForm.formik.touched.name && Boolean(productForm.formik.errors.name)}
                  helperText={productForm.formik.touched.name && productForm.formik.errors.name}
                  margin="normal"
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  id="barcode"
                  name="barcode"
                  label={common('barcode')}
                  value={productForm.formik.values.barcode}
                  onChange={productForm.formik.handleChange}
                  error={productForm.formik.touched.barcode && Boolean(productForm.formik.errors.barcode)}
                  helperText={productForm.formik.touched.barcode && productForm.formik.errors.barcode}
                  margin="normal"
                  InputProps={{
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton>
                          <QrCodeIcon />
                        </IconButton>
                      </InputAdornment>
                    ),
                  }}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth margin="normal">
                  <InputLabel id="category-label">{common('category')}</InputLabel>
                  <Select
                    labelId="category-label"
                    id="category_id"
                    name="category_id"
                    value={productForm.formik.values.category_id}
                    onChange={productForm.formik.handleChange}
                    error={productForm.formik.touched.category_id && Boolean(productForm.formik.errors.category_id)}
                    label={common('category')}
                  >
                    {mockCategories.map((category) => (
                      <MenuItem key={category.id} value={category.id}>
                        {category.name}
                      </MenuItem>
                    ))}
                  </Select>
                  {productForm.formik.touched.category_id && productForm.formik.errors.category_id && (
                    <FormHelperText error>{productForm.formik.errors.category_id}</FormHelperText>
                  )}
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth margin="normal">
                  <InputLabel id="brand-label">{common('brand')}</InputLabel>
                  <Select
                    labelId="brand-label"
                    id="brand_id"
                    name="brand_id"
                    value={productForm.formik.values.brand_id}
                    onChange={productForm.formik.handleChange}
                    error={productForm.formik.touched.brand_id && Boolean(productForm.formik.errors.brand_id)}
                    label={common('brand')}
                  >
                    {mockBrands.map((brand) => (
                      <MenuItem key={brand.id} value={brand.id}>
                        {brand.name}
                      </MenuItem>
                    ))}
                  </Select>
                  {productForm.formik.touched.brand_id && productForm.formik.errors.brand_id && (
                    <FormHelperText error>{productForm.formik.errors.brand_id}</FormHelperText>
                  )}
                </FormControl>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="subtitle1" gutterBottom sx={{ mt: 2 }}>
                  {products('pricingAndStock')}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  id="price"
                  name="price"
                  label={common('price')}
                  type="number"
                  value={productForm.formik.values.price}
                  onChange={productForm.formik.handleChange}
                  error={productForm.formik.touched.price && Boolean(productForm.formik.errors.price)}
                  helperText={productForm.formik.touched.price && productForm.formik.errors.price}
                  margin="normal"
                  InputProps={{
                    startAdornment: <InputAdornment position="start">₹</InputAdornment>,
                  }}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  id="cost_price"
                  name="cost_price"
                  label={products('costPrice')}
                  type="number"
                  value={productForm.formik.values.cost_price}
                  onChange={productForm.formik.handleChange}
                  error={productForm.formik.touched.cost_price && Boolean(productForm.formik.errors.cost_price)}
                  helperText={productForm.formik.touched.cost_price && productForm.formik.errors.cost_price}
                  margin="normal"
                  InputProps={{
                    startAdornment: <InputAdornment position="start">₹</InputAdornment>,
                  }}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  id="stock"
                  name="stock"
                  label={common('stock')}
                  type="number"
                  value={productForm.formik.values.stock}
                  onChange={productForm.formik.handleChange}
                  error={productForm.formik.touched.stock && Boolean(productForm.formik.errors.stock)}
                  helperText={productForm.formik.touched.stock && productForm.formik.errors.stock}
                  margin="normal"
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  id="threshold"
                  name="threshold"
                  label={products('threshold')}
                  type="number"
                  value={productForm.formik.values.threshold}
                  onChange={productForm.formik.handleChange}
                  error={productForm.formik.touched.threshold && Boolean(productForm.formik.errors.threshold)}
                  helperText={
                    (productForm.formik.touched.threshold && productForm.formik.errors.threshold) ||
                    products('thresholdHelp')
                  }
                  margin="normal"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  id="description"
                  name="description"
                  label={common('description')}
                  multiline
                  rows={3}
                  value={productForm.formik.values.description}
                  onChange={productForm.formik.handleChange}
                  margin="normal"
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseProductDialog}>{common('cancel')}</Button>
            <Button type="submit" variant="contained" color="primary">
              {selectedProduct ? common('save') : common('add')}
            </Button>
          </DialogActions>
        </form>
      </Dialog>

      {/* Stock Adjustment Dialog */}
      <Dialog open={openStockAdjustmentDialog} onClose={handleCloseStockAdjustmentDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {products('adjustStock')}
        </DialogTitle>
        <form onSubmit={stockAdjustmentForm.formik.handleSubmit}>
          <DialogContent>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <FormControl fullWidth margin="normal">
                  <InputLabel id="product-label">{common('product')}</InputLabel>
                  <Select
                    labelId="product-label"
                    id="product_id"
                    name="product_id"
                    value={stockAdjustmentForm.formik.values.product_id}
                    onChange={stockAdjustmentForm.formik.handleChange}
                    error={stockAdjustmentForm.formik.touched.product_id && Boolean(stockAdjustmentForm.formik.errors.product_id)}
                    label={common('product')}
                  >
                    {mockProducts.map((product) => (
                      <MenuItem key={product.id} value={product.id}>
                        {product.name} ({product.stock} in stock)
                      </MenuItem>
                    ))}
                  </Select>
                  {stockAdjustmentForm.formik.touched.product_id && stockAdjustmentForm.formik.errors.product_id && (
                    <FormHelperText error>{stockAdjustmentForm.formik.errors.product_id}</FormHelperText>
                  )}
                </FormControl>
              </Grid>
              <Grid item xs={12}>
                <FormControl fullWidth margin="normal">
                  <InputLabel id="adjustment-type-label">{products('adjustmentType')}</InputLabel>
                  <Select
                    labelId="adjustment-type-label"
                    id="adjustment_type"
                    name="adjustment_type"
                    value={stockAdjustmentForm.formik.values.adjustment_type}
                    onChange={stockAdjustmentForm.formik.handleChange}
                    error={stockAdjustmentForm.formik.touched.adjustment_type && Boolean(stockAdjustmentForm.formik.errors.adjustment_type)}
                    label={products('adjustmentType')}
                  >
                    <MenuItem value="increase">
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <ArrowUpwardIcon color="success" sx={{ mr: 1 }} />
                        {common('increase')}
                      </Box>
                    </MenuItem>
                    <MenuItem value="decrease">
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <ArrowDownwardIcon color="error" sx={{ mr: 1 }} />
                        {common('decrease')}
                      </Box>
                    </MenuItem>
                  </Select>
                  {stockAdjustmentForm.formik.touched.adjustment_type && stockAdjustmentForm.formik.errors.adjustment_type && (
                    <FormHelperText error>{stockAdjustmentForm.formik.errors.adjustment_type}</FormHelperText>
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
                <FormControl fullWidth margin="normal">
                  <InputLabel id="reason-label">{products('adjustmentReason')}</InputLabel>
                  <Select
                    labelId="reason-label"
                    id="reason"
                    name="reason"
                    value={stockAdjustmentForm.formik.values.reason}
                    onChange={stockAdjustmentForm.formik.handleChange}
                    error={stockAdjustmentForm.formik.touched.reason && Boolean(stockAdjustmentForm.formik.errors.reason)}
                    label={products('adjustmentReason')}
                  >
                    <MenuItem value="new_stock">New Stock Received</MenuItem>
                    <MenuItem value="damaged">Damaged/Broken</MenuItem>
                    <MenuItem value="expired">Expired</MenuItem>
                    <MenuItem value="theft">Theft/Loss</MenuItem>
                    <MenuItem value="return">Customer Return</MenuItem>
                    <MenuItem value="correction">Inventory Correction</MenuItem>
                    <MenuItem value="other">Other</MenuItem>
                  </Select>
                  {stockAdjustmentForm.formik.touched.reason && stockAdjustmentForm.formik.errors.reason && (
                    <FormHelperText error>{stockAdjustmentForm.formik.errors.reason}</FormHelperText>
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
                  rows={2}
                  value={stockAdjustmentForm.formik.values.notes}
                  onChange={stockAdjustmentForm.formik.handleChange}
                  margin="normal"
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseStockAdjustmentDialog}>{common('cancel')}</Button>
            <Button type="submit" variant="contained" color="primary">
              {products('adjustStock')}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Container>
  );
};

export default InventoryManagement;