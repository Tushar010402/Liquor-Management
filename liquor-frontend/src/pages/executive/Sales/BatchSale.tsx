import React, { useState } from 'react';
import {
  Box,
  Grid,
  Typography,
  TextField,
  Button,
  Card,
  CardContent,
  Divider,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Paper,
  InputAdornment,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Autocomplete,
  Chip,
  Alert,
  SelectChangeEvent,
} from '@mui/material';
import {
  Add as AddIcon,
  Delete as DeleteIcon,
  Save as SaveIcon,
  ShoppingCart as CartIcon,
  Search as SearchIcon,
  Receipt as ReceiptIcon,
  LocalOffer as DiscountIcon,
  Edit as EditIcon,
} from '@mui/icons-material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { PageHeader, FormLayout } from '../../../components/common';

// Mock product data
const products = [
  { id: 1, name: 'Johnnie Walker Black Label', category: 'Whisky', price: 3500, stock: 45 },
  { id: 2, name: 'Absolut Vodka', category: 'Vodka', price: 1800, stock: 32 },
  { id: 3, name: 'Jack Daniels', category: 'Whisky', price: 2800, stock: 28 },
  { id: 4, name: 'Bacardi White Rum', category: 'Rum', price: 1200, stock: 50 },
  { id: 5, name: 'Beefeater Gin', category: 'Gin', price: 2200, stock: 15 },
  { id: 6, name: 'Chivas Regal 12 Year', category: 'Whisky', price: 3200, stock: 20 },
  { id: 7, name: 'Grey Goose Vodka', category: 'Vodka', price: 4500, stock: 12 },
  { id: 8, name: 'Bombay Sapphire Gin', category: 'Gin', price: 2500, stock: 18 },
  { id: 9, name: 'Captain Morgan Spiced Rum', category: 'Rum', price: 1400, stock: 25 },
  { id: 10, name: 'Jameson Irish Whiskey', category: 'Whisky', price: 2200, stock: 30 },
];

// Mock customer data
const customers = [
  { id: 1, name: 'Raj Kumar', phone: '9876543210', email: 'raj@example.com' },
  { id: 2, name: 'Priya Sharma', phone: '8765432109', email: 'priya@example.com' },
  { id: 3, name: 'Amit Singh', phone: '7654321098', email: 'amit@example.com' },
  { id: 4, name: 'Neha Patel', phone: '6543210987', email: 'neha@example.com' },
  { id: 5, name: 'Vikram Mehta', phone: '5432109876', email: 'vikram@example.com' },
];

// Payment methods
const paymentMethods = [
  { id: 'cash', name: 'Cash' },
  { id: 'upi', name: 'UPI' },
  { id: 'card', name: 'Card' },
  { id: 'mixed', name: 'Mixed Payment' },
];

interface CartItem {
  id: number;
  name: string;
  price: number;
  quantity: number;
  total: number;
}

const BatchSale: React.FC = () => {
  const navigate = useNavigate();
  const [cart, setCart] = useState<CartItem[]>([]);
  const [selectedProduct, setSelectedProduct] = useState<any | null>(null);
  const [quantity, setQuantity] = useState<number>(1);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedCustomer, setSelectedCustomer] = useState<any | null>(null);
  const [paymentMethod, setPaymentMethod] = useState<string>('cash');
  const [discount, setDiscount] = useState<number>(0);
  const [note, setNote] = useState<string>('');
  const [saleDate, setSaleDate] = useState<Date | null>(new Date());
  const [confirmDialogOpen, setConfirmDialogOpen] = useState<boolean>(false);
  const [mixedPaymentDialogOpen, setMixedPaymentDialogOpen] = useState<boolean>(false);
  const [cashAmount, setCashAmount] = useState<number>(0);
  const [upiAmount, setUpiAmount] = useState<number>(0);
  const [cardAmount, setCardAmount] = useState<number>(0);
  const [upiReference, setUpiReference] = useState<string>('');
  const [cardReference, setCardReference] = useState<string>('');
  const [showSuccess, setShowSuccess] = useState<boolean>(false);

  // Calculate totals
  const subtotal = cart.reduce((sum, item) => sum + item.total, 0);
  const discountAmount = (subtotal * discount) / 100;
  const total = subtotal - discountAmount;

  const handleAddToCart = () => {
    if (selectedProduct && quantity > 0) {
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
            price: selectedProduct.price,
            quantity: quantity,
            total: selectedProduct.price * quantity,
          },
        ]);
      }
      
      // Reset selection
      setSelectedProduct(null);
      setQuantity(1);
    }
  };

  const handleRemoveFromCart = (id: number) => {
    setCart(cart.filter(item => item.id !== id));
  };

  const handleQuantityChange = (id: number, newQuantity: number) => {
    if (newQuantity > 0) {
      setCart(
        cart.map(item =>
          item.id === id
            ? { ...item, quantity: newQuantity, total: item.price * newQuantity }
            : item
        )
      );
    }
  };

  const handlePaymentMethodChange = (event: SelectChangeEvent) => {
    setPaymentMethod(event.target.value);
    
    if (event.target.value === 'mixed') {
      setMixedPaymentDialogOpen(true);
      // Initialize mixed payment with total amount in cash
      setCashAmount(total);
      setUpiAmount(0);
      setCardAmount(0);
    }
  };

  const handleMixedPaymentConfirm = () => {
    // Validate that the sum equals the total
    if (Math.abs((cashAmount + upiAmount + cardAmount) - total) < 0.01) {
      setMixedPaymentDialogOpen(false);
    } else {
      alert('The sum of all payment methods must equal the total amount.');
    }
  };

  const handleConfirmSale = () => {
    // In a real app, this would send the sale data to the backend
    console.log({
      customer: selectedCustomer,
      items: cart,
      subtotal,
      discount,
      discountAmount,
      total,
      paymentMethod,
      paymentDetails: paymentMethod === 'mixed' 
        ? { cash: cashAmount, upi: { amount: upiAmount, reference: upiReference }, card: { amount: cardAmount, reference: cardReference } }
        : {},
      note,
      saleDate,
      timestamp: new Date().toISOString(),
    });
    
    setConfirmDialogOpen(false);
    setShowSuccess(true);
    
    // Reset form after success
    setTimeout(() => {
      setCart([]);
      setSelectedCustomer(null);
      setPaymentMethod('cash');
      setDiscount(0);
      setNote('');
      setSaleDate(new Date());
      setShowSuccess(false);
    }, 3000);
  };

  const filteredProducts = products.filter(product => 
    product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    product.category.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Box>
        <PageHeader
          title="Batch Sale Entry"
          subtitle="Create multiple sales in a batch"
        />

        {showSuccess && (
          <Alert 
            severity="success" 
            sx={{ mb: 3 }}
            onClose={() => setShowSuccess(false)}
          >
            Sale has been successfully recorded!
          </Alert>
        )}

        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <Card sx={{ mb: 3 }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Add Products
                  </Typography>
                  <Grid container spacing={2} alignItems="center">
                    <Grid item xs={12} md={5}>
                      <Autocomplete
                        options={filteredProducts}
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
                            InputProps={{
                              ...params.InputProps,
                              startAdornment: (
                                <>
                                  <InputAdornment position="start">
                                    <SearchIcon />
                                  </InputAdornment>
                                  {params.InputProps.startAdornment}
                                </>
                              ),
                            }}
                            onChange={(e) => setSearchQuery(e.target.value)}
                          />
                        )}
                      />
                    </Grid>
                    <Grid item xs={6} md={3}>
                      <TextField
                        label="Quantity"
                        type="number"
                        value={quantity}
                        onChange={(e) => setQuantity(parseInt(e.target.value) || 0)}
                        fullWidth
                        variant="outlined"
                        InputProps={{
                          inputProps: { min: 1 },
                        }}
                      />
                    </Grid>
                    <Grid item xs={6} md={2}>
                      <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
                        {selectedProduct ? `₹${selectedProduct.price}` : '₹0'}
                      </Typography>
                      <Typography variant="caption" color="textSecondary">
                        {selectedProduct ? `Stock: ${selectedProduct.stock}` : 'Price'}
                      </Typography>
                    </Grid>
                    <Grid item xs={12} md={2}>
                      <Button
                        variant="contained"
                        color="primary"
                        startIcon={<AddIcon />}
                        onClick={handleAddToCart}
                        disabled={!selectedProduct}
                        fullWidth
                      >
                        Add
                      </Button>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>

              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Cart Items
                  </Typography>
                  {cart.length > 0 ? (
                    <TableContainer>
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
                              <TableCell>{item.name}</TableCell>
                              <TableCell align="right">₹{item.price}</TableCell>
                              <TableCell align="center">
                                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                  <IconButton
                                    size="small"
                                    onClick={() => handleQuantityChange(item.id, item.quantity - 1)}
                                    disabled={item.quantity <= 1}
                                  >
                                    -
                                  </IconButton>
                                  <Typography sx={{ mx: 1 }}>{item.quantity}</Typography>
                                  <IconButton
                                    size="small"
                                    onClick={() => handleQuantityChange(item.id, item.quantity + 1)}
                                  >
                                    +
                                  </IconButton>
                                </Box>
                              </TableCell>
                              <TableCell align="right">₹{item.total}</TableCell>
                              <TableCell align="center">
                                <IconButton
                                  color="error"
                                  size="small"
                                  onClick={() => handleRemoveFromCart(item.id)}
                                >
                                  <DeleteIcon />
                                </IconButton>
                              </TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </TableContainer>
                  ) : (
                    <Paper
                      sx={{
                        p: 3,
                        textAlign: 'center',
                        backgroundColor: 'background.default',
                      }}
                    >
                      <CartIcon sx={{ fontSize: 40, color: 'text.secondary', mb: 1 }} />
                      <Typography variant="h6" color="textSecondary">
                        Your cart is empty
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        Add products to create a sale
                      </Typography>
                    </Paper>
                  )}
                </CardContent>
              </Card>
            </motion.div>
          </Grid>

          <Grid item xs={12} md={4}>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: 0.1 }}
            >
              <Card sx={{ mb: 3 }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Customer Information
                  </Typography>
                  <Autocomplete
                    options={customers}
                    getOptionLabel={(option) => `${option.name} (${option.phone})`}
                    value={selectedCustomer}
                    onChange={(event, newValue) => {
                      setSelectedCustomer(newValue);
                    }}
                    renderInput={(params) => (
                      <TextField
                        {...params}
                        label="Select Customer"
                        variant="outlined"
                        fullWidth
                        margin="normal"
                      />
                    )}
                  />
                  <DatePicker
                    label="Sale Date"
                    value={saleDate}
                    onChange={(newValue) => setSaleDate(newValue)}
                    slotProps={{ textField: { fullWidth: true, margin: 'normal' } }}
                  />
                  <TextField
                    label="Note"
                    multiline
                    rows={3}
                    fullWidth
                    margin="normal"
                    value={note}
                    onChange={(e) => setNote(e.target.value)}
                  />
                </CardContent>
              </Card>

              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Payment Details
                  </Typography>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" color="textSecondary">
                      Subtotal
                    </Typography>
                    <Typography variant="h6">₹{subtotal.toFixed(2)}</Typography>
                  </Box>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" color="textSecondary">
                      Discount
                    </Typography>
                    <Grid container spacing={2} alignItems="center">
                      <Grid item xs={6}>
                        <TextField
                          label="Discount %"
                          type="number"
                          value={discount}
                          onChange={(e) => setDiscount(parseFloat(e.target.value) || 0)}
                          fullWidth
                          variant="outlined"
                          size="small"
                          InputProps={{
                            inputProps: { min: 0, max: 100 },
                            startAdornment: (
                              <InputAdornment position="start">
                                <DiscountIcon fontSize="small" />
                              </InputAdornment>
                            ),
                          }}
                        />
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="body1" color="error">
                          - ₹{discountAmount.toFixed(2)}
                        </Typography>
                      </Grid>
                    </Grid>
                  </Box>
                  <Divider sx={{ my: 2 }} />
                  <Box sx={{ mb: 3 }}>
                    <Typography variant="subtitle1">
                      Total Amount
                    </Typography>
                    <Typography variant="h5" color="primary" sx={{ fontWeight: 'bold' }}>
                      ₹{total.toFixed(2)}
                    </Typography>
                  </Box>
                  <FormControl fullWidth margin="normal">
                    <InputLabel id="payment-method-label">Payment Method</InputLabel>
                    <Select
                      labelId="payment-method-label"
                      value={paymentMethod}
                      onChange={handlePaymentMethodChange}
                      label="Payment Method"
                    >
                      {paymentMethods.map((method) => (
                        <MenuItem key={method.id} value={method.id}>
                          {method.name}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>

                  {paymentMethod === 'upi' && (
                    <TextField
                      label="UPI Reference"
                      fullWidth
                      margin="normal"
                      value={upiReference}
                      onChange={(e) => setUpiReference(e.target.value)}
                    />
                  )}

                  {paymentMethod === 'card' && (
                    <TextField
                      label="Card Reference"
                      fullWidth
                      margin="normal"
                      value={cardReference}
                      onChange={(e) => setCardReference(e.target.value)}
                    />
                  )}

                  {paymentMethod === 'mixed' && (
                    <Box sx={{ mt: 2 }}>
                      <Typography variant="body2" color="textSecondary" gutterBottom>
                        Mixed payment details:
                      </Typography>
                      <Grid container spacing={1}>
                        <Grid item xs={4}>
                          <Chip 
                            label={`Cash: ₹${cashAmount}`} 
                            color="default" 
                            size="small" 
                            onClick={() => setMixedPaymentDialogOpen(true)}
                          />
                        </Grid>
                        <Grid item xs={4}>
                          <Chip 
                            label={`UPI: ₹${upiAmount}`} 
                            color="primary" 
                            size="small" 
                            onClick={() => setMixedPaymentDialogOpen(true)}
                          />
                        </Grid>
                        <Grid item xs={4}>
                          <Chip 
                            label={`Card: ₹${cardAmount}`} 
                            color="secondary" 
                            size="small" 
                            onClick={() => setMixedPaymentDialogOpen(true)}
                          />
                        </Grid>
                      </Grid>
                      <Button
                        size="small"
                        startIcon={<EditIcon />}
                        onClick={() => setMixedPaymentDialogOpen(true)}
                        sx={{ mt: 1 }}
                      >
                        Edit Payment Split
                      </Button>
                    </Box>
                  )}

                  <Button
                    variant="contained"
                    color="primary"
                    fullWidth
                    size="large"
                    startIcon={<ReceiptIcon />}
                    sx={{ mt: 3 }}
                    disabled={cart.length === 0}
                    onClick={() => setConfirmDialogOpen(true)}
                  >
                    Complete Sale
                  </Button>
                </CardContent>
              </Card>
            </motion.div>
          </Grid>
        </Grid>

        {/* Mixed Payment Dialog */}
        <Dialog open={mixedPaymentDialogOpen} onClose={() => setMixedPaymentDialogOpen(false)}>
          <DialogTitle>Mixed Payment Details</DialogTitle>
          <DialogContent>
            <Typography variant="body2" color="textSecondary" gutterBottom>
              Total Amount: ₹{total.toFixed(2)}
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <TextField
                  label="Cash Amount"
                  type="number"
                  fullWidth
                  margin="normal"
                  value={cashAmount}
                  onChange={(e) => setCashAmount(parseFloat(e.target.value) || 0)}
                  InputProps={{
                    startAdornment: <InputAdornment position="start">₹</InputAdornment>,
                  }}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  label="UPI Amount"
                  type="number"
                  fullWidth
                  margin="normal"
                  value={upiAmount}
                  onChange={(e) => setUpiAmount(parseFloat(e.target.value) || 0)}
                  InputProps={{
                    startAdornment: <InputAdornment position="start">₹</InputAdornment>,
                  }}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  label="UPI Reference"
                  fullWidth
                  margin="normal"
                  value={upiReference}
                  onChange={(e) => setUpiReference(e.target.value)}
                  disabled={upiAmount <= 0}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  label="Card Amount"
                  type="number"
                  fullWidth
                  margin="normal"
                  value={cardAmount}
                  onChange={(e) => setCardAmount(parseFloat(e.target.value) || 0)}
                  InputProps={{
                    startAdornment: <InputAdornment position="start">₹</InputAdornment>,
                  }}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  label="Card Reference"
                  fullWidth
                  margin="normal"
                  value={cardReference}
                  onChange={(e) => setCardReference(e.target.value)}
                  disabled={cardAmount <= 0}
                />
              </Grid>
            </Grid>
            <Typography 
              variant="body2" 
              color={Math.abs((cashAmount + upiAmount + cardAmount) - total) < 0.01 ? 'success.main' : 'error.main'}
              sx={{ mt: 2 }}
            >
              Total Split: ₹{(cashAmount + upiAmount + cardAmount).toFixed(2)}
              {Math.abs((cashAmount + upiAmount + cardAmount) - total) < 0.01 ? 
                ' (Matches total amount)' : 
                ' (Does not match total amount)'}
            </Typography>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setMixedPaymentDialogOpen(false)}>Cancel</Button>
            <Button 
              onClick={handleMixedPaymentConfirm} 
              variant="contained" 
              color="primary"
              disabled={Math.abs((cashAmount + upiAmount + cardAmount) - total) >= 0.01}
            >
              Confirm
            </Button>
          </DialogActions>
        </Dialog>

        {/* Confirm Sale Dialog */}
        <Dialog open={confirmDialogOpen} onClose={() => setConfirmDialogOpen(false)}>
          <DialogTitle>Confirm Sale</DialogTitle>
          <DialogContent>
            <Typography variant="body1" gutterBottom>
              Are you sure you want to complete this sale?
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Total Items: {cart.length}
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Total Amount: ₹{total.toFixed(2)}
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Payment Method: {paymentMethods.find(m => m.id === paymentMethod)?.name}
            </Typography>
            {selectedCustomer && (
              <Typography variant="body2" color="textSecondary">
                Customer: {selectedCustomer.name}
              </Typography>
            )}
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setConfirmDialogOpen(false)}>Cancel</Button>
            <Button 
              onClick={handleConfirmSale} 
              variant="contained" 
              color="primary"
            >
              Complete Sale
            </Button>
          </DialogActions>
        </Dialog>
      </Box>
    </LocalizationProvider>
  );
};

export default BatchSale;