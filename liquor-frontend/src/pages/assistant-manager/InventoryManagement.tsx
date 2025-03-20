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
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
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
  Inventory as InventoryIcon,
  LocalShipping as LocalShippingIcon,
  Warning as WarningIcon,
  Print as PrintIcon,
  Visibility as VisibilityIcon,
  SwapHoriz as SwapHorizIcon,
  Download as DownloadIcon,
  Upload as UploadIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';
import { DataTable, PageHeader } from '../../components/common';
import { useTranslations, useFormValidation, useGlobalConfirmDialog, useNotification, useAuth } from '../../hooks';
import { inventoryService, productService, Product, StockAdjustmentRequest, StockTransferRequest } from '../../services/api';
import * as Yup from 'yup';

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
  const { showNotification } = useNotification();
  const { user } = useAuth();
  const [searchQuery, setSearchQuery] = useState('');
  const [filterAnchorEl, setFilterAnchorEl] = useState<null | HTMLElement>(null);
  const [categoryFilter, setCategoryFilter] = useState<string>('all');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [openStockAdjustmentDialog, setOpenStockAdjustmentDialog] = useState(false);
  const [openStockTransferDialog, setOpenStockTransferDialog] = useState(false);
  const [actionAnchorEl, setActionAnchorEl] = useState<{ [key: number]: HTMLElement | null }>({});
  const [tabValue, setTabValue] = useState(0);
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<{ id: number; name: string }[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedShopId, setSelectedShopId] = useState<number | undefined>(
    user?.assigned_shops && user.assigned_shops.length > 0 
      ? parseInt(user.assigned_shops[0].id) 
      : undefined
  );

  // Fetch products and categories
  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      setError(null);
      
      try {
        // In production environment
        if (process.env.NODE_ENV === 'production') {
          // Fetch products
          const productsData = await inventoryService.getProducts(selectedShopId);
          setProducts(productsData);
          
          // Fetch categories
          // This would be a separate API call in a real app
          // For now, we'll extract unique categories from the products
          const uniqueCategories = Array.from(
            new Set(productsData.map(product => product.category))
          ).map(category => ({
            id: category.toLowerCase().replace(/\s+/g, '_'),
            name: category,
          }));
          
          setCategories(uniqueCategories);
        } else {
          // For development/demo purposes, we'll use mock data
          await new Promise(resolve => setTimeout(resolve, 1000));
          
          // Mock products
          setProducts([
            {
              id: 1,
              name: 'Jack Daniels Whiskey',
              category: 'Whiskey',
              brand: 'Jack Daniels',
              price: 2500,
              cost_price: 2000,
              stock: 15,
              threshold: 10,
              barcode: '123456789',
              status: 'in_stock',
              created_at: '2023-01-15',
              updated_at: '2023-01-15',
              description: '750ml bottle',
            },
            {
              id: 2,
              name: 'Absolut Vodka',
              category: 'Vodka',
              brand: 'Absolut',
              price: 1800,
              cost_price: 1500,
              stock: 8,
              threshold: 8,
              barcode: '234567890',
              status: 'low_stock',
              created_at: '2023-01-15',
              updated_at: '2023-01-15',
              description: '750ml bottle',
            },
            {
              id: 3,
              name: 'Corona Beer (6-pack)',
              category: 'Beer',
              brand: 'Corona',
              price: 600,
              cost_price: 450,
              stock: 24,
              threshold: 12,
              barcode: '345678901',
              status: 'in_stock',
              created_at: '2023-01-15',
              updated_at: '2023-01-15',
              description: '330ml x 6',
            },
            {
              id: 4,
              name: 'Bacardi Rum',
              category: 'Rum',
              brand: 'Bacardi',
              price: 1200,
              cost_price: 950,
              stock: 12,
              threshold: 8,
              barcode: '456789012',
              status: 'in_stock',
              created_at: '2023-01-15',
              updated_at: '2023-01-15',
              description: '750ml bottle',
            },
            {
              id: 5,
              name: 'Johnnie Walker Black Label',
              category: 'Whiskey',
              brand: 'Johnnie Walker',
              price: 3500,
              cost_price: 2800,
              stock: 5,
              threshold: 6,
              barcode: '567890123',
              status: 'low_stock',
              created_at: '2023-01-15',
              updated_at: '2023-01-15',
              description: '750ml bottle',
            },
            {
              id: 6,
              name: 'Smirnoff Vodka',
              category: 'Vodka',
              brand: 'Smirnoff',
              price: 1200,
              cost_price: 900,
              stock: 18,
              threshold: 10,
              barcode: '678901234',
              status: 'in_stock',
              created_at: '2023-01-15',
              updated_at: '2023-01-15',
              description: '750ml bottle',
            },
            {
              id: 7,
              name: 'Kingfisher Beer (6-pack)',
              category: 'Beer',
              brand: 'Kingfisher',
              price: 500,
              cost_price: 380,
              stock: 36,
              threshold: 15,
              barcode: '789012345',
              status: 'in_stock',
              created_at: '2023-01-15',
              updated_at: '2023-01-15',
              description: '330ml x 6',
            },
            {
              id: 8,
              name: 'Old Monk Rum',
              category: 'Rum',
              brand: 'Old Monk',
              price: 800,
              cost_price: 600,
              stock: 3,
              threshold: 5,
              barcode: '890123456',
              status: 'low_stock',
              created_at: '2023-01-15',
              updated_at: '2023-01-15',
              description: '750ml bottle',
            },
            {
              id: 9,
              name: 'Blenders Pride Whiskey',
              category: 'Whiskey',
              brand: 'Blenders Pride',
              price: 1500,
              cost_price: 1200,
              stock: 10,
              threshold: 8,
              barcode: '901234567',
              status: 'in_stock',
              created_at: '2023-01-15',
              updated_at: '2023-01-15',
              description: '750ml bottle',
            },
            {
              id: 10,
              name: 'Bira White Beer (6-pack)',
              category: 'Beer',
              brand: 'Bira',
              price: 700,
              cost_price: 550,
              stock: 28,
              threshold: 12,
              barcode: '012345678',
              status: 'in_stock',
              created_at: '2023-01-15',
              updated_at: '2023-01-15',
              description: '330ml x 6',
            },
          ]);
          
          // Mock categories
          setCategories([
            { id: 1, name: 'Whiskey' },
            { id: 2, name: 'Vodka' },
            { id: 3, name: 'Rum' },
            { id: 4, name: 'Beer' },
            { id: 5, name: 'Wine' },
            { id: 6, name: 'Gin' },
          ]);
        }
      } catch (err: any) {
        console.error('Error fetching inventory data:', err);
        setError(err.message || 'Failed to fetch inventory data');
        showNotification({
          message: 'Failed to fetch inventory data. Please try again later.',
          variant: 'error',
        });
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [selectedShopId, showNotification]);

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
    onSubmit: async (values) => {
      try {
        const adjustmentData: StockAdjustmentRequest = {
          product_id: Number(values.product_id),
          adjustment_type: values.adjustment_type as 'increase' | 'decrease',
          quantity: Number(values.quantity),
          reason: values.reason,
          notes: values.notes,
        };
        
        if (process.env.NODE_ENV === 'production') {
          // Make API call to adjust stock
          const updatedProduct = await inventoryService.adjustStock(adjustmentData);
          
          // Update the product in the local state
          setProducts(prevProducts => 
            prevProducts.map(product => 
              product.id === updatedProduct.id ? updatedProduct : product
            )
          );
        } else {
          // For development/demo purposes
          await new Promise(resolve => setTimeout(resolve, 500));
          
          // Update the product in the local state
          setProducts(prevProducts => 
            prevProducts.map(product => {
              if (product.id === Number(values.product_id)) {
                const newStock = values.adjustment_type === 'increase'
                  ? product.stock + Number(values.quantity)
                  : product.stock - Number(values.quantity);
                
                return {
                  ...product,
                  stock: newStock,
                  status: newStock <= 0 ? 'out_of_stock' : newStock <= product.threshold ? 'low_stock' : 'in_stock',
                };
              }
              return product;
            })
          );
        }
        
        showNotification({
          message: `Stock adjustment submitted successfully`,
          variant: 'success',
        });
        
        handleCloseStockAdjustmentDialog();
      } catch (err: any) {
        console.error('Error adjusting stock:', err);
        showNotification({
          message: err.message || 'Failed to adjust stock',
          variant: 'error',
        });
      }
    },
  });

  // Form validation for stock transfer
  const stockTransferForm = useFormValidation({
    initialValues: {
      product_id: '',
      from_shop_id: selectedShopId?.toString() || '',
      to_shop_id: '',
      quantity: '',
      notes: '',
    },
    validationSchema: stockTransferSchema,
    onSubmit: async (values) => {
      try {
        const transferData: StockTransferRequest = {
          product_id: Number(values.product_id),
          from_shop_id: Number(values.from_shop_id),
          to_shop_id: Number(values.to_shop_id),
          quantity: Number(values.quantity),
          notes: values.notes,
        };
        
        if (process.env.NODE_ENV === 'production') {
          // Make API call to transfer stock
          await inventoryService.transferStock(transferData);
          
          // Refresh products to get updated stock levels
          const updatedProducts = await inventoryService.getProducts(selectedShopId);
          setProducts(updatedProducts);
        } else {
          // For development/demo purposes
          await new Promise(resolve => setTimeout(resolve, 500));
          
          // Update the product in the local state
          setProducts(prevProducts => 
            prevProducts.map(product => {
              if (product.id === Number(values.product_id)) {
                const newStock = product.stock - Number(values.quantity);
                
                return {
                  ...product,
                  stock: newStock,
                  status: newStock <= 0 ? 'out_of_stock' : newStock <= product.threshold ? 'low_stock' : 'in_stock',
                };
              }
              return product;
            })
          );
        }
        
        showNotification({
          message: `Stock transfer submitted successfully`,
          variant: 'success',
        });
        
        handleCloseStockTransferDialog();
      } catch (err: any) {
        console.error('Error transferring stock:', err);
        showNotification({
          message: err.message || 'Failed to transfer stock',
          variant: 'error',
        });
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

  // Handle opening the action menu for a product
  const handleActionClick = (event: React.MouseEvent<HTMLElement>, productId: number) => {
    setActionAnchorEl({ ...actionAnchorEl, [productId]: event.currentTarget });
  };

  // Handle closing the action menu for a product
  const handleActionClose = (productId: number) => {
    setActionAnchorEl({ ...actionAnchorEl, [productId]: null });
  };

  // Handle opening the stock adjustment dialog
  const handleOpenStockAdjustmentDialog = (product?: Product) => {
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
  const handleOpenStockTransferDialog = (product?: Product) => {
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
    
    // Set status filter based on tab
    switch (newValue) {
      case 0: // All
        setStatusFilter('all');
        break;
      case 1: // Low Stock
        setStatusFilter('low_stock');
        break;
      case 2: // Out of Stock
        setStatusFilter('out_of_stock');
        break;
      default:
        setStatusFilter('all');
    }
  };

  // Refresh inventory data
  const handleRefreshInventory = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      if (process.env.NODE_ENV === 'production') {
        const productsData = await inventoryService.getProducts(selectedShopId);
        setProducts(productsData);
      } else {
        // For development/demo purposes
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
      
      showNotification({
        message: 'Inventory data refreshed successfully',
        variant: 'success',
      });
    } catch (err: any) {
      console.error('Error refreshing inventory data:', err);
      setError(err.message || 'Failed to refresh inventory data');
      showNotification({
        message: 'Failed to refresh inventory data. Please try again later.',
        variant: 'error',
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Filter inventory based on search query and filters
  const filteredInventory = products.filter((product) => {
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
            disabled={isLoading}
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
                  {categories.map((category) => (
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
                <Button
                  variant="outlined"
                  startIcon={<RefreshIcon />}
                  onClick={handleRefreshInventory}
                  size="small"
                  disabled={isLoading}
                >
                  {common('refresh')}
                </Button>
              </Box>
            </Grid>
            <Grid item xs={12} sm={12} md={4} sx={{ display: 'flex', justifyContent: 'flex-end', gap: 1 }}>
              <Button
                variant="outlined"
                color="primary"
                startIcon={<DownloadIcon />}
                onClick={() => {
                  if (process.env.NODE_ENV === 'production') {
                    // In a real app, this would trigger a file download
                    productService.exportProducts(selectedShopId);
                  } else {
                    showNotification({
                      message: 'Export functionality is not available in demo mode',
                      variant: 'info',
                    });
                  }
                }}
                disabled={isLoading}
              >
                {common('export')}
              </Button>
              <Button
                variant="outlined"
                color="primary"
                startIcon={<InventoryIcon />}
                onClick={() => handleOpenStockAdjustmentDialog()}
                disabled={isLoading}
              >
                {inventory('adjustStock')}
              </Button>
              <Button
                variant="contained"
                color="primary"
                startIcon={<SwapHorizIcon />}
                onClick={() => handleOpenStockTransferDialog()}
                disabled={isLoading}
              >
                {inventory('transferStock')}
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {isLoading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', py: 5 }}>
          <CircularProgress />
          <Typography variant="body1" sx={{ ml: 2 }}>
            {common('loading')}
          </Typography>
        </Box>
      ) : error ? (
        <Card>
          <CardContent>
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', py: 3 }}>
              <Typography variant="h6" color="error" gutterBottom>
                {error}
              </Typography>
              <Button
                variant="contained"
                color="primary"
                onClick={handleRefreshInventory}
                sx={{ mt: 2 }}
              >
                {common('retry')}
              </Button>
            </Box>
          </CardContent>
        </Card>
      ) : filteredInventory.length === 0 ? (
        <Card>
          <CardContent>
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', py: 3 }}>
              <Typography variant="h6" gutterBottom>
                {inventory('noProductsFound')}
              </Typography>
              <Typography variant="body2" color="textSecondary" align="center" sx={{ mb: 2 }}>
                {searchQuery || categoryFilter !== 'all' || statusFilter !== 'all'
                  ? inventory('noProductsMatchFilter')
                  : inventory('noProductsYet')}
              </Typography>
              {searchQuery || categoryFilter !== 'all' || statusFilter !== 'all' ? (
                <Button
                  variant="outlined"
                  color="primary"
                  onClick={() => {
                    setSearchQuery('');
                    setCategoryFilter('all');
                    setStatusFilter('all');
                    setTabValue(0);
                  }}
                >
                  {common('clearFilters')}
                </Button>
              ) : (
                <Button
                  variant="contained"
                  color="primary"
                  startIcon={<RefreshIcon />}
                  onClick={handleRefreshInventory}
                >
                  {common('refresh')}
                </Button>
              )}
            </Box>
          </CardContent>
        </Card>
      ) : (
        <DataTable
          columns={columns}
          data={filteredInventory}
          keyField="id"
          pagination
          paginationPerPage={10}
          paginationTotalRows={filteredInventory.length}
        />
      )}

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