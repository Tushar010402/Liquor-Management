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
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { PageHeader, FormLayout } from '../../../components/common';

// Mock data for products
const productsData = [
  { id: 1, name: 'Johnnie Walker Black Label', category: 'Whisky', price: 3500, stock: 15, barcode: '8901234567890' },
  { id: 2, name: 'Absolut Vodka', category: 'Vodka', price: 1800, stock: 20, barcode: '8901234567891' },
  { id: 3, name: 'Jack Daniels', category: 'Whisky', price: 2800, stock: 12, barcode: '8901234567892' },
  { id: 4, name: 'Bacardi White Rum', category: 'Rum', price: 1200, stock: 18, barcode: '8901234567893' },
  { id: 5, name: 'Beefeater Gin', category: 'Gin', price: 2200, stock: 10, barcode: '8901234567894' },
  { id: 6, name: 'Hennessy VS', category: 'Brandy', price: 4500, stock: 8, barcode: '8901234567895' },
  { id: 7, name: 'Jameson Irish Whiskey', category: 'Whisky', price: 2500, stock: 14, barcode: '8901234567896' },
  { id: 8, name: 'Smirnoff Vodka', category: 'Vodka', price: 1200, stock: 25, barcode: '8901234567897' },
  { id: 9, name: 'Chivas Regal 12 Year', category: 'Whisky', price: 3200, stock: 9, barcode: '8901234567898' },
  { id: 10, name: 'Grey Goose Vodka', category: 'Vodka', price: 3800, stock: 7, barcode: '8901234567899' },
];

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
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedProduct, setSelectedProduct] = useState<any | null>(null);
  const [quantity, setQuantity] = useState(1);
  const [cart, setCart] = useState<CartItem[]>([]);
  const [paymentMethod, setPaymentMethod] = useState('cash');
  const [paymentAmount, setPaymentAmount] = useState('');
  const [customerName, setCustomerName] = useState('');
  const [customerPhone, setCustomerPhone] = useState('');
  const [discount, setDiscount] = useState('');
  const [paymentDialog, setPaymentDialog] = useState(false);
  const [barcodeInput, setBarcodeInput] = useState('');

  // Calculate totals
  const subtotal = cart.reduce((sum, item) => sum + item.total, 0);
  const discountAmount = discount ? parseFloat(discount) : 0;
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
  const handleBarcodeSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const product = productsData.find(p => p.barcode === barcodeInput);
    
    if (product) {
      setSelectedProduct(product);
      setBarcodeInput('');
      
      // Auto-add to cart after a short delay
      setTimeout(() => {
        handleAddToCart();
      }, 500);
    }
  };

  // Handle quantity change for cart item
  const handleCartItemQuantity = (id: number, newQuantity: number) => {
    if (newQuantity < 1) return;

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
    setPaymentAmount(total.toString());
    setPaymentDialog(true);
  };

  const handlePaymentDialogClose = () => {
    setPaymentDialog(false);
  };

  // Handle completing the sale
  const handleCompleteSale = () => {
    // In a real app, this would send the sale data to the backend
    console.log({
      items: cart,
      subtotal,
      discount: discountAmount,
      total,
      paymentMethod,
      paymentAmount: parseFloat(paymentAmount),
      change,
      customer: {
        name: customerName,
        phone: customerPhone,
      },
      timestamp: new Date().toISOString(),
    });

    // Close dialog and navigate to dashboard
    handlePaymentDialogClose();
    
    // Show success message and redirect
    alert('Sale completed successfully!');
    navigate('/executive/dashboard');
  };

  // Handle saving as draft
  const handleSaveAsDraft = () => {
    // In a real app, this would save the sale as a draft
    console.log('Saving as draft', {
      items: cart,
      subtotal,
      discount: discountAmount,
      customer: {
        name: customerName,
        phone: customerPhone,
      },
    });
    
    alert('Sale saved as draft!');
    navigate('/executive/draft-sales');
  };

  return (
    <Box>
      <PageHeader
        title="New Sale"
        subtitle="Create a new sale transaction"
      />

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <form onSubmit={handleBarcodeSubmit}>
                    <TextField
                      fullWidth
                      label="Scan Barcode"
                      variant="outlined"
                      value={barcodeInput}
                      onChange={(e) => setBarcodeInput(e.target.value)}
                      InputProps={{
                        endAdornment: (
                          <InputAdornment position="end">
                            <IconButton type="submit" edge="end">
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
                    options={productsData}
                    getOptionLabel={(option) => option.name}
                    value={selectedProduct}
                    onChange={(event, newValue) => {
                      setSelectedProduct(newValue);
                    }}
                    renderInput={(params) => (
                      <TextField
                        {...params}
                        label="Search Products"
                        variant="outlined"
                        fullWidth
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
                {cart.length > 0 ? (
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
                            <TableCell align="right">₹{item.price}</TableCell>
                            <TableCell align="center">
                              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                <IconButton 
                                  size="small" 
                                  onClick={() => handleCartItemQuantity(item.id, item.quantity - 1)}
                                >
                                  <Remove fontSize="small" />
                                </IconButton>
                                <Typography sx={{ mx: 1, minWidth: 20, textAlign: 'center' }}>
                                  {item.quantity}
                                </Typography>
                                <IconButton 
                                  size="small" 
                                  onClick={() => handleCartItemQuantity(item.id, item.quantity + 1)}
                                >
                                  <Add fontSize="small" />
                                </IconButton>
                              </Box>
                            </TableCell>
                            <TableCell align="right">₹{item.total}</TableCell>
                            <TableCell align="center">
                              <IconButton 
                                color="error" 
                                size="small"
                                onClick={() => handleRemoveItem(item.id)}
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
                    <TextField
                      size="small"
                      value={discount}
                      onChange={(e) => setDiscount(e.target.value)}
                      InputProps={{
                        startAdornment: <InputAdornment position="start">₹</InputAdornment>,
                      }}
                      sx={{ width: '100%' }}
                    />
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
                  startIcon={<Receipt />}
                  onClick={handlePaymentDialogOpen}
                  disabled={cart.length === 0}
                >
                  Proceed to Payment
                </Button>
                
                <Button
                  variant="outlined"
                  color="secondary"
                  fullWidth
                  startIcon={<Save />}
                  onClick={handleSaveAsDraft}
                  disabled={cart.length === 0}
                >
                  Save as Draft
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
              Total Amount: ₹{total}
            </Typography>
          </Box>
          
          <FormControl fullWidth margin="normal">
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
              />
              
              {parseFloat(paymentAmount) >= total && (
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
            />
          )}
          
          {paymentMethod === 'card' && (
            <TextField
              fullWidth
              label="Card Transaction ID"
              variant="outlined"
              margin="normal"
            />
          )}
          
          {paymentMethod === 'bank_transfer' && (
            <TextField
              fullWidth
              label="Bank Reference Number"
              variant="outlined"
              margin="normal"
            />
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handlePaymentDialogClose}>Cancel</Button>
          <Button 
            onClick={handleCompleteSale} 
            variant="contained" 
            color="primary"
            disabled={
              (paymentMethod === 'cash' && parseFloat(paymentAmount) < total) ||
              cart.length === 0
            }
          >
            Complete Sale
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default NewSale;