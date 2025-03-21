import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Typography,
  TextField,
  Button,
  Card,
  CardContent,
  Divider,
  IconButton,
  Autocomplete,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  InputAdornment,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Chip,
  useTheme,
  CircularProgress,
  Alert,
  Snackbar,
} from '@mui/material';
import {
  Add,
  Remove,
  Delete,
  Search,
  ShoppingCart,
  Save,
  Print,
  Receipt,
  LocalAtm,
  CreditCard,
  AccountBalance,
  Refresh,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { PageHeader, FormLayout } from '../../../components/common';
import { productService, saleService, Product, CreateSaleRequest, SaleItemRequest } from '../../../services/api';
import { useAuth, useNotification } from '../../../hooks';

interface CartItem {
  id: number;
  name: string;
  category: string;
  price: number;
  quantity: number;
  total: number;
}

const NewSale: React.FC = () => {
  const theme = useTheme();
  const navigate = useNavigate();
  const { user } = useAuth();
  const { showNotification } = useNotification();
  
  // State for products and loading
  const [products, setProducts] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  
  // State for sale
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [quantity, setQuantity] = useState(1);
  const [cart, setCart] = useState<CartItem[]>([]);
  const [paymentMethod, setPaymentMethod] = useState('cash');
  const [paymentAmount, setPaymentAmount] = useState('');
  const [customerName, setCustomerName] = useState('');
  const [customerPhone, setCustomerPhone] = useState('');
  const [discount, setDiscount] = useState('');
  const [discountType, setDiscountType] = useState<'fixed' | 'percentage'>('fixed');
  const [paymentDialog, setPaymentDialog] = useState(false);
  const [barcodeInput, setBarcodeInput] = useState('');
  const [transactionId, setTransactionId] = useState('');
  const [notes, setNotes] = useState('');
  
  // Get shop ID from user
  const shopId = user?.assigned_shops && user.assigned_shops.length > 0 
    ? parseInt(user.assigned_shops[0].id) 
    : undefined;

  // Fetch products
  useEffect(() => {
    const fetchProducts = async () => {
      setIsLoading(true);
      setError(null);
      
      try {
        if (process.env.NODE_ENV === 'production') {
          const productsData = await productService.getProducts(shopId);
          setProducts(productsData);
        } else {
          // For development/demo purposes
          await new Promise(resolve => setTimeout(resolve, 1000));
          
          // Mock products
          setProducts([
            { id: 1, name: 'Johnnie Walker Black Label', category: 'Whisky', brand: 'Johnnie Walker', price: 3500, cost_price: 3000, stock: 15, threshold: 5, barcode: '8901234567890', status: 'in_stock', created_at: '2023-01-01', updated_at: '2023-01-01' },
            { id: 2, name: 'Absolut Vodka', category: 'Vodka', brand: 'Absolut', price: 1800, cost_price: 1500, stock: 20, threshold: 5, barcode: '8901234567891', status: 'in_stock', created_at: '2023-01-01', updated_at: '2023-01-01' },
            { id: 3, name: 'Jack Daniels', category: 'Whisky', brand: 'Jack Daniels', price: 2800, cost_price: 2400, stock: 12, threshold: 5, barcode: '8901234567892', status: 'in_stock', created_at: '2023-01-01', updated_at: '2023-01-01' },
            { id: 4, name: 'Bacardi White Rum', category: 'Rum', brand: 'Bacardi', price: 1200, cost_price: 1000, stock: 18, threshold: 5, barcode: '8901234567893', status: 'in_stock', created_at: '2023-01-01', updated_at: '2023-01-01' },
            { id: 5, name: 'Beefeater Gin', category: 'Gin', brand: 'Beefeater', price: 2200, cost_price: 1800, stock: 10, threshold: 5, barcode: '8901234567894', status: 'in_stock', created_at: '2023-01-01', updated_at: '2023-01-01' },
            { id: 6, name: 'Hennessy VS', category: 'Brandy', brand: 'Hennessy', price: 4500, cost_price: 3800, stock: 8, threshold: 5, barcode: '8901234567895', status: 'in_stock', created_at: '2023-01-01', updated_at: '2023-01-01' },
            { id: 7, name: 'Jameson Irish Whiskey', category: 'Whisky', brand: 'Jameson', price: 2500, cost_price: 2100, stock: 14, threshold: 5, barcode: '8901234567896', status: 'in_stock', created_at: '2023-01-01', updated_at: '2023-01-01' },
            { id: 8, name: 'Smirnoff Vodka', category: 'Vodka', brand: 'Smirnoff', price: 1200, cost_price: 1000, stock: 25, threshold: 5, barcode: '8901234567897', status: 'in_stock', created_at: '2023-01-01', updated_at: '2023-01-01' },
            { id: 9, name: 'Chivas Regal 12 Year', category: 'Whisky', brand: 'Chivas Regal', price: 3200, cost_price: 2700, stock: 9, threshold: 5, barcode: '8901234567898', status: 'in_stock', created_at: '2023-01-01', updated_at: '2023-01-01' },
            { id: 10, name: 'Grey Goose Vodka', category: 'Vodka', brand: 'Grey Goose', price: 3800, cost_price: 3200, stock: 7, threshold: 5, barcode: '8901234567899', status: 'in_stock', created_at: '2023-01-01', updated_at: '2023-01-01' },
          ]);
        }
      } catch (err: any) {
        console.error('Error fetching products:', err);
        setError(err.message || 'Failed to fetch products');
        showNotification({
          message: 'Failed to fetch products. Please try again later.',
          variant: 'error',
        });
      } finally {
        setIsLoading(false);
      }
    };

    fetchProducts();
  }, [shopId, showNotification]);

  // Filter products based on search term
  const filteredProducts = products.filter(product => 
    product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    product.category.toLowerCase().includes(searchTerm.toLowerCase()) ||
    product.brand.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Calculate totals
  const subtotal = cart.reduce((sum, item) => sum + item.total, 0);
  let discountAmount = 0;
  
  if (discount) {
    if (discountType === 'fixed') {
      discountAmount = parseFloat(discount);
    } else {
      // Calculate percentage discount
      discountAmount = subtotal * (parseFloat(discount) / 100);
    }
  }
  
  const total = subtotal - discountAmount;
  const change = paymentAmount ? parseFloat(paymentAmount) - total : 0;

  // Handle adding product to cart
  const handleAddToCart = () => {
    if (!selectedProduct) return;

    const existingItemIndex = cart.findIndex(item => item.id === selectedProduct.id);

    if (existingItemIndex >= 0) {
      // Update existing item
      const updatedCart = [...cart];
      updatedCart[existingItemIndex].quantity += quantity;
      updatedCart[existingItemIndex].total = updatedCart[existingItemIndex].price * updatedCart[existingItemIndex].quantity;
      setCart(updatedCart);
    } else {
      // Add new item
      setCart([
        ...cart,
        {
          id: selectedProduct.id,
          name: selectedProduct.name,
          category: selectedProduct.category,
          price: selectedProduct.price,
          quantity: quantity,
          total: selectedProduct.price * quantity,
        },
      ]);
    }

    // Reset selection
    setSelectedProduct(null);
    setQuantity(1);
  };

  // Handle barcode scan
  const handleBarcodeSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!barcodeInput) return;
    
    setIsLoading(true);
    
    try {
      if (process.env.NODE_ENV === 'production') {
        // Search for product by barcode
        const product = await productService.searchByBarcode(barcodeInput);
        setSelectedProduct(product);
      } else {
        // For development/demo purposes
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Find product in mock data
        const product = products.find(p => p.barcode === barcodeInput);
        
        if (product) {
          setSelectedProduct(product);
        } else {
          showNotification({
            message: 'Product not found with this barcode',
            variant: 'warning',
          });
        }
      }
      
      setBarcodeInput('');
      
      // Auto-add to cart after a short delay if product found
      if (selectedProduct) {
        setTimeout(() => {
          handleAddToCart();
        }, 500);
      }
    } catch (err: any) {
      console.error('Error searching product by barcode:', err);
      showNotification({
        message: err.message || 'Failed to find product with this barcode',
        variant: 'error',
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Handle quantity change for cart item
  const handleCartItemQuantity = (id: number, newQuantity: number) => {
    if (newQuantity < 1) return;
    
    // Check if we have enough stock
    const product = products.find(p => p.id === id);
    if (product && newQuantity > product.stock) {
      showNotification({
        message: `Only ${product.stock} items available in stock`,
        variant: 'warning',
      });
      return;
    }

    const updatedCart = cart.map(item => {
      if (item.id === id) {
        return {
          ...item,
          quantity: newQuantity,
          total: item.price * newQuantity,
        };
      }
      return item;
    });

    setCart(updatedCart);
  };

  // Handle removing item from cart
  const handleRemoveItem = (id: number) => {
    setCart(cart.filter(item => item.id !== id));
  };

  // Handle payment dialog
  const handlePaymentDialogOpen = () => {
    if (cart.length === 0) {
      showNotification({
        message: 'Please add at least one product to the cart',
        variant: 'warning',
      });
      return;
    }
    
    setPaymentAmount(total.toString());
    setPaymentDialog(true);
  };

  const handlePaymentDialogClose = () => {
    setPaymentDialog(false);
  };

  // Handle completing the sale
  const handleCompleteSale = async () => {
    if (cart.length === 0) {
      showNotification({
        message: 'Please add at least one product to the cart',
        variant: 'warning',
      });
      return;
    }
    
    if (paymentMethod === 'cash' && (!paymentAmount || parseFloat(paymentAmount) < total)) {
      showNotification({
        message: 'Payment amount must be at least equal to the total amount',
        variant: 'warning',
      });
      return;
    }
    
    setIsSubmitting(true);
    
    try {
      // Prepare sale data
      const saleData: CreateSaleRequest = {
        customer_name: customerName || undefined,
        customer_phone: customerPhone || undefined,
        payment_method: paymentMethod,
        items: cart.map(item => ({
          product_id: item.id,
          quantity: item.quantity,
          price: item.price,
        })),
        discount_type: discountType,
        discount_value: discount ? parseFloat(discount) : undefined,
        notes: notes || undefined,
      };
      
      if (process.env.NODE_ENV === 'production') {
        // Create sale in the backend
        const createdSale = await saleService.createSale(saleData, shopId);
        
        // Show success message
        showNotification({
          message: `Sale completed successfully! Invoice #${createdSale.invoice_number}`,
          variant: 'success',
        });
        
        // Close dialog and navigate to dashboard
        handlePaymentDialogClose();
        navigate('/executive/sales/my-sales');
      } else {
        // For development/demo purposes
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Show success message
        showNotification({
          message: 'Sale completed successfully! Invoice #INV-2023-1234',
          variant: 'success',
        });
        
        // Close dialog and navigate to dashboard
        handlePaymentDialogClose();
        navigate('/executive/sales/my-sales');
      }
    } catch (err: any) {
      console.error('Error completing sale:', err);
      showNotification({
        message: err.message || 'Failed to complete sale',
        variant: 'error',
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  // Handle saving as draft
  const handleSaveAsDraft = async () => {
    if (cart.length === 0) {
      showNotification({
        message: 'Please add at least one product to the cart',
        variant: 'warning',
      });
      return;
    }
    
    setIsSubmitting(true);
    
    try {
      // In a real app, this would save the sale as a draft
      // This would require a separate API endpoint for draft sales
      
      if (process.env.NODE_ENV === 'production') {
        // This is a placeholder - in a real app, you would call a specific API endpoint
        // For now, we'll just simulate a successful draft save
        await new Promise(resolve => setTimeout(resolve, 1000));
      } else {
        // For development/demo purposes
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
      
      showNotification({
        message: 'Sale saved as draft!',
        variant: 'success',
      });
      
      navigate('/executive/sales/draft-sales');
    } catch (err: any) {
      console.error('Error saving draft:', err);
      showNotification({
        message: err.message || 'Failed to save draft',
        variant: 'error',
      });
    } finally {
      setIsSubmitting(false);
    }
  };
  
  // Refresh products
  const handleRefreshProducts = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      if (process.env.NODE_ENV === 'production') {
        const productsData = await productService.getProducts(shopId);
        setProducts(productsData);
      } else {
        // For development/demo purposes
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
      
      showNotification({
        message: 'Products refreshed successfully',
        variant: 'success',
      });
    } catch (err: any) {
      console.error('Error refreshing products:', err);
      setError(err.message || 'Failed to refresh products');
      showNotification({
        message: 'Failed to refresh products. Please try again later.',
        variant: 'error',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box>
      <PageHeader
        title="New Sale"
        subtitle="Create a new sale transaction"
      />

      {error && (
        <Alert 
          severity="error" 
          sx={{ mb: 3 }}
          action={
            <Button color="inherit" size="small" onClick={handleRefreshProducts}>
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
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">Products</Typography>
                <Button
                  startIcon={<Refresh />}
                  size="small"
                  onClick={handleRefreshProducts}
                  disabled={isLoading}
                >
                  Refresh
                </Button>
              </Box>
              
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <form onSubmit={handleBarcodeSubmit}>
                    <TextField
                      fullWidth
                      label="Scan Barcode"
                      variant="outlined"
                      value={barcodeInput}
                      onChange={(e) => setBarcodeInput(e.target.value)}
                      disabled={isLoading}
                      InputProps={{
                        endAdornment: (
                          <InputAdornment position="end">
                            <IconButton type="submit" edge="end" disabled={isLoading || !barcodeInput}>
                              <Search />
                            </IconButton>
                          </InputAdornment>
                        ),
                      }}
                    />
                  </form>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Autocomplete
                    options={products}
                    getOptionLabel={(option) => option.name}
                    value={selectedProduct}
                    onChange={(event, newValue) => {
                      setSelectedProduct(newValue);
                    }}
                    disabled={isLoading}
                    loading={isLoading}
                    renderInput={(params) => (
                      <TextField
                        {...params}
                        label="Search Products"
                        variant="outlined"
                        fullWidth
                        InputProps={{
                          ...params.InputProps,
                          endAdornment: (
                            <>
                              {isLoading ? <CircularProgress color="inherit" size={20} /> : null}
                              {params.InputProps.endAdornment}
                            </>
                          ),
                        }}
                      />
                    )}
                  />
                </Grid>
              </Grid>

              {selectedProduct && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <Box sx={{ mt: 3, p: 2, bgcolor: 'background.default', borderRadius: 1 }}>
                    <Grid container spacing={2} alignItems="center">
                      <Grid item xs={12} sm={6}>
                        <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                          {selectedProduct.name}
                        </Typography>
                        <Typography variant="body2" color="textSecondary">
                          Category: {selectedProduct.category} • Stock: {selectedProduct.stock}
                        </Typography>
                      </Grid>
                      <Grid item xs={12} sm={2}>
                        <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                          ₹{selectedProduct.price}
                        </Typography>
                      </Grid>
                      <Grid item xs={12} sm={2}>
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          <IconButton 
                            size="small" 
                            onClick={() => setQuantity(Math.max(1, quantity - 1))}
                          >
                            <Remove fontSize="small" />
                          </IconButton>
                          <TextField
                            size="small"
                            value={quantity}
                            onChange={(e) => {
                              const value = parseInt(e.target.value);
                              if (!isNaN(value) && value > 0) {
                                setQuantity(value);
                              }
                            }}
                            inputProps={{ 
                              min: 1, 
                              style: { textAlign: 'center' } 
                            }}
                            sx={{ width: 60, mx: 1 }}
                          />
                          <IconButton 
                            size="small" 
                            onClick={() => setQuantity(quantity + 1)}
                          >
                            <Add fontSize="small" />
                          </IconButton>
                        </Box>
                      </Grid>
                      <Grid item xs={12} sm={2}>
                        <Button
                          variant="contained"
                          color="primary"
                          fullWidth
                          onClick={handleAddToCart}
                          startIcon={<Add />}
                        >
                          Add
                        </Button>
                      </Grid>
                    </Grid>
                  </Box>
                </motion.div>
              )}

              <Box sx={{ mt: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Cart Items
                </Typography>
                {isLoading ? (
                  <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', py: 5 }}>
                    <CircularProgress size={30} />
                    <Typography variant="body1" sx={{ ml: 2 }}>
                      Loading...
                    </Typography>
                  </Box>
                ) : cart.length > 0 ? (
                  <TableContainer component={Paper} variant="outlined">
                    <Table>
                      <TableHead>
                        <TableRow>
                          <TableCell>Product</TableCell>
                          <TableCell align="right">Price</TableCell>
                          <TableCell align="center">Quantity</TableCell>
                          <TableCell align="right">Total</TableCell>
                          <TableCell align="center">Actions</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {cart.map((item) => (
                          <TableRow key={item.id}>
                            <TableCell>
                              <Typography variant="body2" sx={{ fontWeight: 500 }}>
                                {item.name}
                              </Typography>
                              <Typography variant="caption" color="textSecondary">
                                {item.category}
                              </Typography>
                            </TableCell>
                            <TableCell align="right">₹{item.price.toFixed(2)}</TableCell>
                            <TableCell align="center">
                              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                <IconButton 
                                  size="small" 
                                  onClick={() => handleCartItemQuantity(item.id, item.quantity - 1)}
                                  disabled={isLoading || isSubmitting}
                                >
                                  <Remove fontSize="small" />
                                </IconButton>
                                <Typography sx={{ mx: 1, minWidth: 20, textAlign: 'center' }}>
                                  {item.quantity}
                                </Typography>
                                <IconButton 
                                  size="small" 
                                  onClick={() => handleCartItemQuantity(item.id, item.quantity + 1)}
                                  disabled={isLoading || isSubmitting}
                                >
                                  <Add fontSize="small" />
                                </IconButton>
                              </Box>
                            </TableCell>
                            <TableCell align="right">₹{item.total.toFixed(2)}</TableCell>
                            <TableCell align="center">
                              <IconButton 
                                color="error" 
                                size="small"
                                onClick={() => handleRemoveItem(item.id)}
                                disabled={isLoading || isSubmitting}
                              >
                                <Delete fontSize="small" />
                              </IconButton>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                ) : (
                  <Box 
                    sx={{ 
                      p: 3, 
                      textAlign: 'center', 
                      bgcolor: 'background.default',
                      borderRadius: 1,
                      border: '1px dashed',
                      borderColor: 'divider',
                    }}
                  >
                    <ShoppingCart sx={{ fontSize: 40, color: 'text.secondary', mb: 1 }} />
                    <Typography variant="subtitle1" color="textSecondary">
                      Cart is empty
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Search for products or scan barcode to add items
                    </Typography>
                  </Box>
                )}
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card sx={{ position: 'sticky', top: 88 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Sale Summary
              </Typography>
              
              <Box sx={{ mb: 3 }}>
                <TextField
                  fullWidth
                  label="Customer Name"
                  variant="outlined"
                  value={customerName}
                  onChange={(e) => setCustomerName(e.target.value)}
                  margin="normal"
                />
                <TextField
                  fullWidth
                  label="Customer Phone"
                  variant="outlined"
                  value={customerPhone}
                  onChange={(e) => setCustomerPhone(e.target.value)}
                  margin="normal"
                />
              </Box>
              
              <Divider sx={{ my: 2 }} />
              
              <Box sx={{ mb: 2 }}>
                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <Typography variant="body1">Subtotal:</Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="body1" align="right">₹{subtotal}</Typography>
                  </Grid>
                  
                  <Grid item xs={6}>
                    <Typography variant="body1">Discount:</Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <TextField
                        size="small"
                        value={discount}
                        onChange={(e) => setDiscount(e.target.value)}
                        InputProps={{
                          startAdornment: (
                            <InputAdornment position="start">
                              {discountType === 'fixed' ? '₹' : ''}
                            </InputAdornment>
                          ),
                          endAdornment: (
                            <InputAdornment position="end">
                              {discountType === 'percentage' ? '%' : ''}
                            </InputAdornment>
                          ),
                        }}
                        sx={{ width: '70%' }}
                        disabled={isSubmitting}
                      />
                      <FormControl size="small" sx={{ width: '30%', ml: 1 }}>
                        <Select
                          value={discountType}
                          onChange={(e) => setDiscountType(e.target.value as 'fixed' | 'percentage')}
                          disabled={isSubmitting}
                        >
                          <MenuItem value="fixed">₹</MenuItem>
                          <MenuItem value="percentage">%</MenuItem>
                        </Select>
                      </FormControl>
                    </Box>
                  </Grid>
                </Grid>
              </Box>
              
              <Divider sx={{ my: 2 }} />
              
              <Box sx={{ mb: 3 }}>
                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <Typography variant="h6">Total:</Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="h6" align="right">₹{total}</Typography>
                  </Grid>
                </Grid>
              </Box>
              
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <Button
                  variant="contained"
                  color="primary"
                  size="large"
                  fullWidth
                  startIcon={isSubmitting ? <CircularProgress size={20} color="inherit" /> : <Receipt />}
                  onClick={handlePaymentDialogOpen}
                  disabled={isLoading || isSubmitting || cart.length === 0}
                >
                  {isSubmitting ? 'Processing...' : 'Proceed to Payment'}
                </Button>
                
                <Button
                  variant="outlined"
                  color="secondary"
                  fullWidth
                  startIcon={isSubmitting ? <CircularProgress size={20} color="inherit" /> : <Save />}
                  onClick={handleSaveAsDraft}
                  disabled={isLoading || isSubmitting || cart.length === 0}
                >
                  {isSubmitting ? 'Saving...' : 'Save as Draft'}
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Payment Dialog */}
      <Dialog open={paymentDialog} onClose={handlePaymentDialogClose} maxWidth="sm" fullWidth>
        <DialogTitle>Complete Payment</DialogTitle>
        <DialogContent>
          <Box sx={{ mb: 3 }}>
            <Typography variant="h5" align="center" gutterBottom>
              Total Amount: ₹{total.toFixed(2)}
            </Typography>
          </Box>
          
          <FormControl fullWidth margin="normal" disabled={isSubmitting}>
            <InputLabel id="payment-method-label">Payment Method</InputLabel>
            <Select
              labelId="payment-method-label"
              id="payment-method"
              value={paymentMethod}
              label="Payment Method"
              onChange={(e) => setPaymentMethod(e.target.value)}
            >
              <MenuItem value="cash">
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <LocalAtm sx={{ mr: 1 }} />
                  Cash
                </Box>
              </MenuItem>
              <MenuItem value="upi">
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <CreditCard sx={{ mr: 1 }} />
                  UPI
                </Box>
              </MenuItem>
              <MenuItem value="card">
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <CreditCard sx={{ mr: 1 }} />
                  Card
                </Box>
              </MenuItem>
              <MenuItem value="bank_transfer">
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <AccountBalance sx={{ mr: 1 }} />
                  Bank Transfer
                </Box>
              </MenuItem>
            </Select>
          </FormControl>
          
          {paymentMethod === 'cash' && (
            <>
              <TextField
                fullWidth
                label="Amount Received"
                variant="outlined"
                type="number"
                value={paymentAmount}
                onChange={(e) => setPaymentAmount(e.target.value)}
                InputProps={{
                  startAdornment: <InputAdornment position="start">₹</InputAdornment>,
                }}
                margin="normal"
                disabled={isSubmitting}
                error={paymentAmount !== '' && parseFloat(paymentAmount) < total}
                helperText={paymentAmount !== '' && parseFloat(paymentAmount) < total ? 'Amount must be at least equal to the total' : ''}
              />
              
              {paymentAmount !== '' && parseFloat(paymentAmount) >= total && (
                <Box sx={{ mt: 2, p: 2, bgcolor: 'success.light', borderRadius: 1 }}>
                  <Typography variant="subtitle1" sx={{ color: 'white' }}>
                    Change to return: ₹{change.toFixed(2)}
                  </Typography>
                </Box>
              )}
            </>
          )}
          
          {paymentMethod === 'upi' && (
            <TextField
              fullWidth
              label="UPI Transaction ID"
              variant="outlined"
              margin="normal"
              value={transactionId}
              onChange={(e) => setTransactionId(e.target.value)}
              disabled={isSubmitting}
              required
            />
          )}
          
          {paymentMethod === 'card' && (
            <TextField
              fullWidth
              label="Card Transaction ID"
              variant="outlined"
              margin="normal"
              value={transactionId}
              onChange={(e) => setTransactionId(e.target.value)}
              disabled={isSubmitting}
              required
            />
          )}
          
          {paymentMethod === 'bank_transfer' && (
            <TextField
              fullWidth
              label="Bank Reference Number"
              variant="outlined"
              margin="normal"
              value={transactionId}
              onChange={(e) => setTransactionId(e.target.value)}
              disabled={isSubmitting}
              required
            />
          )}
          
          <TextField
            fullWidth
            label="Notes"
            variant="outlined"
            multiline
            rows={2}
            margin="normal"
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            disabled={isSubmitting}
            placeholder="Add any additional notes about this sale"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handlePaymentDialogClose} disabled={isSubmitting}>Cancel</Button>
          <Button 
            onClick={handleCompleteSale} 
            variant="contained" 
            color="primary"
            disabled={
              isSubmitting ||
              (paymentMethod === 'cash' && (!paymentAmount || parseFloat(paymentAmount) < total)) ||
              ((paymentMethod === 'upi' || paymentMethod === 'card' || paymentMethod === 'bank_transfer') && !transactionId) ||
              cart.length === 0
            }
            startIcon={isSubmitting ? <CircularProgress size={20} color="inherit" /> : null}
          >
            {isSubmitting ? 'Processing...' : 'Complete Sale'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default NewSale;