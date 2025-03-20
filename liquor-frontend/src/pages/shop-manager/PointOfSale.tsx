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
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormHelperText,
  Divider,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Avatar,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  ListItemSecondaryAction,
  Tabs,
  Tab,
  useTheme,
} from '@mui/material';
import {
  Search as SearchIcon,
  Add as AddIcon,
  Remove as RemoveIcon,
  Delete as DeleteIcon,
  ShoppingCart as ShoppingCartIcon,
  Person as PersonIcon,
  Receipt as ReceiptIcon,
  Print as PrintIcon,
  Save as SaveIcon,
  Clear as ClearIcon,
  QrCode as QrCodeIcon,
  AttachMoney as AttachMoneyIcon,
  CreditCard as CreditCardIcon,
  AccountBalance as AccountBalanceIcon,
  LocalOffer as LocalOfferIcon,
  Inventory as InventoryIcon,
} from '@mui/icons-material';
import { PageHeader } from '../../components/common';
import { useTranslations, useFormValidation, useGlobalConfirmDialog, useNotification } from '../../hooks';
import * as Yup from 'yup';
import { stringUtils } from '../../utils';

// Mock data for products
const mockProducts = [
  {
    id: 1,
    name: 'Jack Daniels Whiskey',
    category: 'Whiskey',
    brand: 'Jack Daniels',
    price: 2500,
    stock: 15,
    barcode: '8901234567890',
  },
  {
    id: 2,
    name: 'Absolut Vodka',
    category: 'Vodka',
    brand: 'Absolut',
    price: 1800,
    stock: 8,
    barcode: '8901234567891',
  },
  {
    id: 3,
    name: 'Corona Beer (6-pack)',
    category: 'Beer',
    brand: 'Corona',
    price: 600,
    stock: 24,
    barcode: '8901234567892',
  },
  {
    id: 4,
    name: 'Bacardi Rum',
    category: 'Rum',
    brand: 'Bacardi',
    price: 1200,
    stock: 12,
    barcode: '8901234567893',
  },
  {
    id: 5,
    name: 'Johnnie Walker Black Label',
    category: 'Whiskey',
    brand: 'Johnnie Walker',
    price: 3500,
    stock: 5,
    barcode: '8901234567894',
  },
  {
    id: 6,
    name: 'Smirnoff Vodka',
    category: 'Vodka',
    brand: 'Smirnoff',
    price: 1200,
    stock: 18,
    barcode: '8901234567895',
  },
  {
    id: 7,
    name: 'Kingfisher Beer (6-pack)',
    category: 'Beer',
    brand: 'Kingfisher',
    price: 500,
    stock: 36,
    barcode: '8901234567896',
  },
  {
    id: 8,
    name: 'Old Monk Rum',
    category: 'Rum',
    brand: 'Old Monk',
    price: 800,
    stock: 3,
    barcode: '8901234567897',
  },
  {
    id: 9,
    name: 'Blenders Pride Whiskey',
    category: 'Whiskey',
    brand: 'Blenders Pride',
    price: 1500,
    stock: 10,
    barcode: '8901234567898',
  },
  {
    id: 10,
    name: 'Bira White Beer (6-pack)',
    category: 'Beer',
    brand: 'Bira',
    price: 700,
    stock: 28,
    barcode: '8901234567899',
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

// Mock data for customers
const mockCustomers = [
  { id: 1, name: 'John Doe', phone: '9876543210', email: 'john.doe@example.com' },
  { id: 2, name: 'Jane Smith', phone: '9876543211', email: 'jane.smith@example.com' },
  { id: 3, name: 'Michael Wilson', phone: '9876543212', email: 'michael.wilson@example.com' },
  { id: 4, name: 'Emily Davis', phone: '9876543213', email: 'emily.davis@example.com' },
  { id: 5, name: 'Robert Johnson', phone: '9876543214', email: 'robert.johnson@example.com' },
];

// Validation schema for customer form
const customerValidationSchema = Yup.object({
  name: Yup.string().required('Name is required'),
  phone: Yup.string()
    .matches(/^\d{10}$/, 'Phone number must be 10 digits')
    .required('Phone number is required'),
  email: Yup.string().email('Invalid email address'),
});

// Validation schema for payment form
const paymentValidationSchema = Yup.object({
  payment_method: Yup.string()
    .oneOf(['cash', 'card', 'upi'], 'Invalid payment method')
    .required('Payment method is required'),
  amount_paid: Yup.number()
    .positive('Amount must be positive')
    .required('Amount paid is required'),
});

/**
 * Point of Sale component for Shop Manager
 */
const PointOfSale: React.FC = () => {
  const { common, sales, products: productsTranslation } = useTranslations();
  const theme = useTheme();
  const { confirm } = useGlobalConfirmDialog();
  const { showNotification } = useNotification();
  const [searchQuery, setSearchQuery] = useState('');
  const [barcodeInput, setBarcodeInput] = useState('');
  const [categoryFilter, setCategoryFilter] = useState<number | 'all'>('all');
  const [cartItems, setCartItems] = useState<any[]>([]);
  const [openCustomerDialog, setOpenCustomerDialog] = useState(false);
  const [openPaymentDialog, setOpenPaymentDialog] = useState(false);
  const [selectedCustomer, setSelectedCustomer] = useState<any | null>(null);
  const [tabValue, setTabValue] = useState(0);
  const [discountAmount, setDiscountAmount] = useState<number>(0);
  const [discountType, setDiscountType] = useState<'percentage' | 'fixed'>('percentage');
  const [discountValue, setDiscountValue] = useState<number>(0);

  // Form validation for customer dialog
  const customerForm = useFormValidation({
    initialValues: {
      name: '',
      phone: '',
      email: '',
      address: '',
    },
    validationSchema: customerValidationSchema,
    onSubmit: (values) => {
      console.log('Customer form submitted:', values);
      // In a real app, you would make an API call to create/update the customer
      // For now, we'll just simulate adding a new customer
      const newCustomer = {
        id: mockCustomers.length + 1,
        name: values.name,
        phone: values.phone,
        email: values.email || '',
      };
      setSelectedCustomer(newCustomer);
      handleCloseCustomerDialog();
      showNotification({
        message: 'Customer added successfully',
        variant: 'success',
      });
    },
  });

  // Form validation for payment dialog
  const paymentForm = useFormValidation({
    initialValues: {
      payment_method: 'cash',
      amount_paid: calculateTotal(),
      change_amount: 0,
      card_number: '',
      card_holder: '',
      upi_id: '',
      notes: '',
    },
    validationSchema: paymentValidationSchema,
    onSubmit: (values) => {
      console.log('Payment form submitted:', values);
      // In a real app, you would make an API call to process the payment and create the sale
      handleClosePaymentDialog();
      handleCompleteSale();
    },
  });

  // Calculate subtotal
  const calculateSubtotal = () => {
    return cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  };

  // Calculate discount
  const calculateDiscount = () => {
    const subtotal = calculateSubtotal();
    if (discountType === 'percentage') {
      return (subtotal * discountValue) / 100;
    } else {
      return discountValue;
    }
  };

  // Calculate total
  const calculateTotal = () => {
    return calculateSubtotal() - calculateDiscount();
  };

  // Update change amount when amount paid changes
  useEffect(() => {
    const total = calculateTotal();
    const amountPaid = parseFloat(paymentForm.formik.values.amount_paid as any) || 0;
    const changeAmount = amountPaid - total;
    
    paymentForm.formik.setFieldValue('change_amount', changeAmount > 0 ? changeAmount : 0);
  }, [paymentForm.formik.values.amount_paid, cartItems, discountValue, discountType]);

  // Update amount paid when total changes
  useEffect(() => {
    const total = calculateTotal();
    paymentForm.formik.setFieldValue('amount_paid', total);
  }, [cartItems, discountValue, discountType]);

  // Handle adding a product to the cart
  const handleAddToCart = (product: any) => {
    const existingItemIndex = cartItems.findIndex(item => item.id === product.id);
    
    if (existingItemIndex !== -1) {
      // Product already in cart, increase quantity
      const updatedItems = [...cartItems];
      if (updatedItems[existingItemIndex].quantity < product.stock) {
        updatedItems[existingItemIndex].quantity += 1;
        setCartItems(updatedItems);
      } else {
        showNotification({
          message: 'Cannot add more items. Stock limit reached.',
          variant: 'warning',
        });
      }
    } else {
      // Add new product to cart
      if (product.stock > 0) {
        setCartItems([...cartItems, { ...product, quantity: 1 }]);
      } else {
        showNotification({
          message: 'Product is out of stock',
          variant: 'error',
        });
      }
    }
  };

  // Handle removing a product from the cart
  const handleRemoveFromCart = (productId: number) => {
    const existingItemIndex = cartItems.findIndex(item => item.id === productId);
    
    if (existingItemIndex !== -1) {
      const updatedItems = [...cartItems];
      if (updatedItems[existingItemIndex].quantity > 1) {
        // Decrease quantity
        updatedItems[existingItemIndex].quantity -= 1;
        setCartItems(updatedItems);
      } else {
        // Remove item from cart
        setCartItems(cartItems.filter(item => item.id !== productId));
      }
    }
  };

  // Handle deleting a product from the cart
  const handleDeleteFromCart = (productId: number) => {
    setCartItems(cartItems.filter(item => item.id !== productId));
  };

  // Handle clearing the cart
  const handleClearCart = async () => {
    if (cartItems.length === 0) return;
    
    const confirmed = await confirm({
      title: sales('clearCart'),
      message: sales('confirmClearCart'),
      confirmButtonColor: 'error',
      confirmText: common('clear'),
      cancelText: common('cancel'),
    });

    if (confirmed) {
      setCartItems([]);
      setSelectedCustomer(null);
      setDiscountValue(0);
    }
  };

  // Handle barcode input
  const handleBarcodeSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!barcodeInput) return;
    
    const product = mockProducts.find(p => p.barcode === barcodeInput);
    if (product) {
      handleAddToCart(product);
      setBarcodeInput('');
    } else {
      showNotification({
        message: 'Product not found',
        variant: 'error',
      });
    }
  };

  // Handle opening the customer dialog
  const handleOpenCustomerDialog = () => {
    customerForm.formik.resetForm();
    setOpenCustomerDialog(true);
  };

  // Handle closing the customer dialog
  const handleCloseCustomerDialog = () => {
    setOpenCustomerDialog(false);
  };

  // Handle selecting an existing customer
  const handleSelectCustomer = (customer: any) => {
    setSelectedCustomer(customer);
    handleCloseCustomerDialog();
  };

  // Handle opening the payment dialog
  const handleOpenPaymentDialog = () => {
    if (cartItems.length === 0) {
      showNotification({
        message: 'Cart is empty',
        variant: 'warning',
      });
      return;
    }
    
    paymentForm.formik.resetForm();
    paymentForm.formik.setFieldValue('amount_paid', calculateTotal());
    setOpenPaymentDialog(true);
  };

  // Handle closing the payment dialog
  const handleClosePaymentDialog = () => {
    setOpenPaymentDialog(false);
  };

  // Handle completing the sale
  const handleCompleteSale = () => {
    // In a real app, you would make an API call to create the sale
    showNotification({
      message: 'Sale completed successfully',
      variant: 'success',
    });
    
    // Clear the cart and reset the form
    setCartItems([]);
    setSelectedCustomer(null);
    setDiscountValue(0);
    
    // In a real app, you would print the receipt or redirect to the receipt page
    console.log('Sale completed');
  };

  // Handle tab change
  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  // Filter products based on search query and category filter
  const filteredProducts = mockProducts.filter((product) => {
    const matchesSearch = product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      product.brand.toLowerCase().includes(searchQuery.toLowerCase()) ||
      product.barcode.includes(searchQuery);
    
    const matchesCategory = categoryFilter === 'all' || product.category === mockCategories.find(c => c.id === categoryFilter)?.name;
    
    return matchesSearch && matchesCategory;
  });

  return (
    <Container maxWidth="xl">
      <PageHeader
        title={sales('pointOfSale')}
        subtitle={sales('processSales')}
        icon={<ShoppingCartIcon fontSize="large" />}
      />

      <Grid container spacing={3}>
        {/* Left Side - Products */}
        <Grid item xs={12} md={8}>
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Grid container spacing={2} alignItems="center">
                <Grid item xs={12} sm={6}>
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
                <Grid item xs={12} sm={6}>
                  <form onSubmit={handleBarcodeSubmit}>
                    <TextField
                      fullWidth
                      placeholder={productsTranslation('scanBarcode')}
                      value={barcodeInput}
                      onChange={(e) => setBarcodeInput(e.target.value)}
                      InputProps={{
                        startAdornment: (
                          <InputAdornment position="start">
                            <QrCodeIcon />
                          </InputAdornment>
                        ),
                        endAdornment: (
                          <InputAdornment position="end">
                            <IconButton type="submit" edge="end">
                              <SearchIcon />
                            </IconButton>
                          </InputAdornment>
                        ),
                      }}
                      size="small"
                    />
                  </form>
                </Grid>
              </Grid>
            </CardContent>
          </Card>

          <Card>
            <CardContent sx={{ pb: 1 }}>
              <Tabs
                value={tabValue}
                onChange={handleTabChange}
                indicatorColor="primary"
                textColor="primary"
                variant="scrollable"
                scrollButtons="auto"
                aria-label="product category tabs"
              >
                <Tab label={common('all')} />
                {mockCategories.map((category) => (
                  <Tab key={category.id} label={category.name} />
                ))}
              </Tabs>
            </CardContent>
            <Divider />
            <CardContent>
              <Grid container spacing={2}>
                {filteredProducts.map((product) => (
                  <Grid item xs={12} sm={6} md={4} key={product.id}>
                    <Card
                      variant="outlined"
                      sx={{
                        cursor: 'pointer',
                        transition: 'all 0.2s',
                        '&:hover': {
                          transform: 'translateY(-4px)',
                          boxShadow: theme.shadows[4],
                        },
                        position: 'relative',
                      }}
                      onClick={() => handleAddToCart(product)}
                    >
                      <CardContent sx={{ p: 2 }}>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                          <Typography variant="subtitle1" fontWeight={600} gutterBottom noWrap>
                            {product.name}
                          </Typography>
                          <Chip
                            label={product.category}
                            size="small"
                            color="primary"
                            variant="outlined"
                          />
                        </Box>
                        <Typography variant="body2" color="textSecondary" gutterBottom>
                          {product.brand}
                        </Typography>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 1 }}>
                          <Typography variant="h6" color="primary.main">
                            ₹{product.price.toLocaleString()}
                          </Typography>
                          <Chip
                            label={`${product.stock} ${common('inStock')}`}
                            size="small"
                            color={product.stock > 0 ? 'success' : 'error'}
                          />
                        </Box>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
                {filteredProducts.length === 0 && (
                  <Grid item xs={12}>
                    <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', py: 4 }}>
                      <Typography variant="body1" color="textSecondary">
                        {common('noProductsFound')}
                      </Typography>
                    </Box>
                  </Grid>
                )}
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Right Side - Cart */}
        <Grid item xs={12} md={4}>
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6" component="h2">
                  {sales('cart')}
                </Typography>
                <Button
                  variant="outlined"
                  color="error"
                  size="small"
                  startIcon={<ClearIcon />}
                  onClick={handleClearCart}
                  disabled={cartItems.length === 0}
                >
                  {common('clear')}
                </Button>
              </Box>
              <Divider sx={{ mb: 2 }} />
              
              {/* Customer Selection */}
              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" gutterBottom>
                  {common('customer')}
                </Typography>
                {selectedCustomer ? (
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <Avatar sx={{ mr: 1, bgcolor: theme.palette.primary.main }}>
                        {stringUtils.getInitials(selectedCustomer.name)}
                      </Avatar>
                      <Box>
                        <Typography variant="body1">
                          {selectedCustomer.name}
                        </Typography>
                        <Typography variant="body2" color="textSecondary">
                          {selectedCustomer.phone}
                        </Typography>
                      </Box>
                    </Box>
                    <Button
                      variant="outlined"
                      size="small"
                      onClick={() => setSelectedCustomer(null)}
                    >
                      {common('change')}
                    </Button>
                  </Box>
                ) : (
                  <Button
                    variant="outlined"
                    color="primary"
                    fullWidth
                    startIcon={<PersonIcon />}
                    onClick={handleOpenCustomerDialog}
                  >
                    {sales('selectCustomer')}
                  </Button>
                )}
              </Box>
              <Divider sx={{ mb: 2 }} />
              
              {/* Cart Items */}
              <Box sx={{ maxHeight: 300, overflowY: 'auto', mb: 2 }}>
                {cartItems.length === 0 ? (
                  <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', py: 4 }}>
                    <Typography variant="body1" color="textSecondary">
                      {sales('emptyCart')}
                    </Typography>
                  </Box>
                ) : (
                  <List disablePadding>
                    {cartItems.map((item) => (
                      <ListItem
                        key={item.id}
                        disablePadding
                        sx={{ py: 1, px: 0 }}
                        secondaryAction={
                          <IconButton
                            edge="end"
                            aria-label="delete"
                            onClick={() => handleDeleteFromCart(item.id)}
                          >
                            <DeleteIcon />
                          </IconButton>
                        }
                      >
                        <ListItemText
                          primary={item.name}
                          secondary={`₹${item.price.toLocaleString()} × ${item.quantity}`}
                          primaryTypographyProps={{ variant: 'body2', noWrap: true }}
                          secondaryTypographyProps={{ variant: 'body2' }}
                          sx={{ mr: 2 }}
                        />
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          <IconButton
                            size="small"
                            onClick={() => handleRemoveFromCart(item.id)}
                          >
                            <RemoveIcon fontSize="small" />
                          </IconButton>
                          <Typography variant="body2" sx={{ mx: 1 }}>
                            {item.quantity}
                          </Typography>
                          <IconButton
                            size="small"
                            onClick={() => handleAddToCart(item)}
                            disabled={item.quantity >= item.stock}
                          >
                            <AddIcon fontSize="small" />
                          </IconButton>
                        </Box>
                      </ListItem>
                    ))}
                  </List>
                )}
              </Box>
              <Divider sx={{ mb: 2 }} />
              
              {/* Discount */}
              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" gutterBottom>
                  {sales('discount')}
                </Typography>
                <Grid container spacing={2} alignItems="center">
                  <Grid item xs={5}>
                    <FormControl fullWidth size="small">
                      <Select
                        value={discountType}
                        onChange={(e) => setDiscountType(e.target.value as 'percentage' | 'fixed')}
                      >
                        <MenuItem value="percentage">%</MenuItem>
                        <MenuItem value="fixed">₹</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item xs={7}>
                    <TextField
                      fullWidth
                      type="number"
                      size="small"
                      value={discountValue}
                      onChange={(e) => {
                        const value = parseFloat(e.target.value);
                        if (discountType === 'percentage') {
                          setDiscountValue(Math.min(100, Math.max(0, value || 0)));
                        } else {
                          setDiscountValue(Math.max(0, value || 0));
                        }
                      }}
                      InputProps={{
                        startAdornment: (
                          <InputAdornment position="start">
                            <LocalOfferIcon fontSize="small" />
                          </InputAdornment>
                        ),
                      }}
                    />
                  </Grid>
                </Grid>
              </Box>
              <Divider sx={{ mb: 2 }} />
              
              {/* Totals */}
              <Box sx={{ mb: 3 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body1">
                    {sales('subtotal')}
                  </Typography>
                  <Typography variant="body1">
                    ₹{calculateSubtotal().toLocaleString()}
                  </Typography>
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body1">
                    {sales('discount')}
                  </Typography>
                  <Typography variant="body1">
                    - ₹{calculateDiscount().toLocaleString()}
                  </Typography>
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="h6" fontWeight={600}>
                    {common('total')}
                  </Typography>
                  <Typography variant="h6" fontWeight={600} color="primary.main">
                    ₹{calculateTotal().toLocaleString()}
                  </Typography>
                </Box>
              </Box>
              
              {/* Checkout Button */}
              <Button
                variant="contained"
                color="primary"
                fullWidth
                size="large"
                startIcon={<AttachMoneyIcon />}
                onClick={handleOpenPaymentDialog}
                disabled={cartItems.length === 0}
              >
                {sales('checkout')}
              </Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Customer Dialog */}
      <Dialog open={openCustomerDialog} onClose={handleCloseCustomerDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {sales('selectCustomer')}
        </DialogTitle>
        <DialogContent>
          <Tabs
            value={tabValue}
            onChange={handleTabChange}
            indicatorColor="primary"
            textColor="primary"
            variant="fullWidth"
            aria-label="customer tabs"
            sx={{ mb: 2 }}
          >
            <Tab label={sales('existingCustomer')} />
            <Tab label={sales('newCustomer')} />
          </Tabs>
          
          {tabValue === 0 ? (
            // Existing Customers
            <Box>
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
                sx={{ mb: 2 }}
              />
              <List>
                {mockCustomers.map((customer) => (
                  <ListItem
                    key={customer.id}
                    button
                    onClick={() => handleSelectCustomer(customer)}
                    sx={{ borderRadius: 1, mb: 1 }}
                  >
                    <ListItemAvatar>
                      <Avatar sx={{ bgcolor: theme.palette.primary.main }}>
                        {stringUtils.getInitials(customer.name)}
                      </Avatar>
                    </ListItemAvatar>
                    <ListItemText
                      primary={customer.name}
                      secondary={customer.phone}
                    />
                  </ListItem>
                ))}
              </List>
            </Box>
          ) : (
            // New Customer Form
            <form onSubmit={customerForm.formik.handleSubmit}>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    id="name"
                    name="name"
                    label={common('name')}
                    value={customerForm.formik.values.name}
                    onChange={customerForm.formik.handleChange}
                    error={customerForm.formik.touched.name && Boolean(customerForm.formik.errors.name)}
                    helperText={customerForm.formik.touched.name && customerForm.formik.errors.name}
                    margin="normal"
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    id="phone"
                    name="phone"
                    label={common('phone')}
                    value={customerForm.formik.values.phone}
                    onChange={customerForm.formik.handleChange}
                    error={customerForm.formik.touched.phone && Boolean(customerForm.formik.errors.phone)}
                    helperText={customerForm.formik.touched.phone && customerForm.formik.errors.phone}
                    margin="normal"
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    id="email"
                    name="email"
                    label={common('email')}
                    value={customerForm.formik.values.email}
                    onChange={customerForm.formik.handleChange}
                    error={customerForm.formik.touched.email && Boolean(customerForm.formik.errors.email)}
                    helperText={customerForm.formik.touched.email && customerForm.formik.errors.email}
                    margin="normal"
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    id="address"
                    name="address"
                    label={common('address')}
                    multiline
                    rows={2}
                    value={customerForm.formik.values.address}
                    onChange={customerForm.formik.handleChange}
                    margin="normal"
                  />
                </Grid>
              </Grid>
              <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 2 }}>
                <Button
                  type="submit"
                  variant="contained"
                  color="primary"
                >
                  {common('add')}
                </Button>
              </Box>
            </form>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseCustomerDialog}>{common('cancel')}</Button>
        </DialogActions>
      </Dialog>

      {/* Payment Dialog */}
      <Dialog open={openPaymentDialog} onClose={handleClosePaymentDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {sales('payment')}
        </DialogTitle>
        <form onSubmit={paymentForm.formik.handleSubmit}>
          <DialogContent>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>
                  {common('total')}: ₹{calculateTotal().toLocaleString()}
                </Typography>
              </Grid>
              <Grid item xs={12}>
                <FormControl fullWidth margin="normal">
                  <InputLabel id="payment-method-label">{sales('paymentMethod')}</InputLabel>
                  <Select
                    labelId="payment-method-label"
                    id="payment_method"
                    name="payment_method"
                    value={paymentForm.formik.values.payment_method}
                    onChange={paymentForm.formik.handleChange}
                    error={paymentForm.formik.touched.payment_method && Boolean(paymentForm.formik.errors.payment_method)}
                    label={sales('paymentMethod')}
                  >
                    <MenuItem value="cash">
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <AttachMoneyIcon sx={{ mr: 1 }} />
                        {common('cash')}
                      </Box>
                    </MenuItem>
                    <MenuItem value="card">
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <CreditCardIcon sx={{ mr: 1 }} />
                        {common('card')}
                      </Box>
                    </MenuItem>
                    <MenuItem value="upi">
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <AccountBalanceIcon sx={{ mr: 1 }} />
                        {common('upi')}
                      </Box>
                    </MenuItem>
                  </Select>
                  {paymentForm.formik.touched.payment_method && paymentForm.formik.errors.payment_method && (
                    <FormHelperText error>{paymentForm.formik.errors.payment_method}</FormHelperText>
                  )}
                </FormControl>
              </Grid>
              
              {paymentForm.formik.values.payment_method === 'cash' && (
                <>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      id="amount_paid"
                      name="amount_paid"
                      label={sales('amountPaid')}
                      type="number"
                      value={paymentForm.formik.values.amount_paid}
                      onChange={paymentForm.formik.handleChange}
                      error={paymentForm.formik.touched.amount_paid && Boolean(paymentForm.formik.errors.amount_paid)}
                      helperText={paymentForm.formik.touched.amount_paid && paymentForm.formik.errors.amount_paid}
                      margin="normal"
                      InputProps={{
                        startAdornment: <InputAdornment position="start">₹</InputAdornment>,
                      }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      id="change_amount"
                      name="change_amount"
                      label={sales('change')}
                      type="number"
                      value={paymentForm.formik.values.change_amount}
                      InputProps={{
                        readOnly: true,
                        startAdornment: <InputAdornment position="start">₹</InputAdornment>,
                      }}
                      margin="normal"
                    />
                  </Grid>
                </>
              )}
              
              {paymentForm.formik.values.payment_method === 'card' && (
                <>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      id="card_number"
                      name="card_number"
                      label={sales('cardNumber')}
                      value={paymentForm.formik.values.card_number}
                      onChange={paymentForm.formik.handleChange}
                      margin="normal"
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      id="card_holder"
                      name="card_holder"
                      label={sales('cardHolder')}
                      value={paymentForm.formik.values.card_holder}
                      onChange={paymentForm.formik.handleChange}
                      margin="normal"
                    />
                  </Grid>
                </>
              )}
              
              {paymentForm.formik.values.payment_method === 'upi' && (
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    id="upi_id"
                    name="upi_id"
                    label={sales('upiId')}
                    value={paymentForm.formik.values.upi_id}
                    onChange={paymentForm.formik.handleChange}
                    margin="normal"
                  />
                </Grid>
              )}
              
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  id="notes"
                  name="notes"
                  label={common('notes')}
                  multiline
                  rows={2}
                  value={paymentForm.formik.values.notes}
                  onChange={paymentForm.formik.handleChange}
                  margin="normal"
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleClosePaymentDialog}>{common('cancel')}</Button>
            <Button
              type="submit"
              variant="contained"
              color="primary"
              startIcon={<ReceiptIcon />}
            >
              {sales('completePayment')}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Container>
  );
};

export default PointOfSale;