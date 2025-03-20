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
  Stepper,
  Step,
  StepLabel,
} from '@mui/material';
import {
  Add as AddIcon,
  Delete as DeleteIcon,
  Save as SaveIcon,
  AssignmentReturn as ReturnIcon,
  Search as SearchIcon,
  PhotoCamera as PhotoCameraIcon,
  AttachFile as AttachFileIcon,
  LocalShipping as SupplierIcon,
  ArrowBack as ArrowBackIcon,
  ArrowForward as ArrowForwardIcon,
} from '@mui/icons-material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { PageHeader } from '../../../components/common';

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

// Mock supplier data
const suppliers = [
  { id: 1, name: 'ABC Distributors', contact: 'Rajesh Kumar', phone: '9876543210', email: 'rajesh@abcdist.com' },
  { id: 2, name: 'XYZ Beverages', contact: 'Priya Sharma', phone: '8765432109', email: 'priya@xyzbev.com' },
  { id: 3, name: 'Premium Spirits', contact: 'Amit Singh', phone: '7654321098', email: 'amit@premiumspirits.com' },
  { id: 4, name: 'Global Wines & Spirits', contact: 'Neha Patel', phone: '6543210987', email: 'neha@globalws.com' },
  { id: 5, name: 'Metro Liquors', contact: 'Vikram Mehta', phone: '5432109876', email: 'vikram@metroliquors.com' },
];

// Return reasons
const returnReasons = [
  { value: 'damaged', label: 'Damaged Product' },
  { value: 'expired', label: 'Expired Product' },
  { value: 'quality_issue', label: 'Quality Issue' },
  { value: 'wrong_delivery', label: 'Wrong Product Delivered' },
  { value: 'excess_inventory', label: 'Excess Inventory' },
  { value: 'recall', label: 'Product Recall' },
  { value: 'other', label: 'Other' },
];

interface ReturnItem {
  id: number;
  productId: number;
  productName: string;
  price: number;
  quantity: number;
  total: number;
  reason: string;
  notes: string;
}

const CreateReturn: React.FC = () => {
  const navigate = useNavigate();
  const [activeStep, setActiveStep] = useState(0);
  const [returnItems, setReturnItems] = useState<ReturnItem[]>([]);
  const [selectedProduct, setSelectedProduct] = useState<any | null>(null);
  const [quantity, setQuantity] = useState<number>(1);
  const [reason, setReason] = useState<string>('');
  const [notes, setNotes] = useState<string>('');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedSupplier, setSelectedSupplier] = useState<any | null>(null);
  const [returnDate, setReturnDate] = useState<Date | null>(new Date());
  const [referenceNumber, setReferenceNumber] = useState<string>('');
  const [confirmDialogOpen, setConfirmDialogOpen] = useState<boolean>(false);
  const [documentImage, setDocumentImage] = useState<string | null>(null);
  const [showSuccess, setShowSuccess] = useState<boolean>(false);

  const steps = ['Select Supplier', 'Add Return Items', 'Upload Documents', 'Review & Submit'];

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleAddReturnItem = () => {
    if (selectedProduct && quantity > 0 && reason) {
      const newItem: ReturnItem = {
        id: Date.now(), // Use timestamp as temporary ID
        productId: selectedProduct.id,
        productName: selectedProduct.name,
        price: selectedProduct.price,
        quantity,
        total: selectedProduct.price * quantity,
        reason,
        notes,
      };
      
      setReturnItems([...returnItems, newItem]);
      
      // Reset form
      setSelectedProduct(null);
      setQuantity(1);
      setReason('');
      setNotes('');
    }
  };

  const handleRemoveReturnItem = (id: number) => {
    setReturnItems(returnItems.filter(item => item.id !== id));
  };

  const handleDocumentUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        setDocumentImage(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmitReturn = () => {
    // In a real app, this would send the return data to the backend
    console.log({
      supplier: selectedSupplier,
      items: returnItems,
      returnDate,
      referenceNumber,
      documentImage,
      totalAmount: returnItems.reduce((sum, item) => sum + item.total, 0),
      timestamp: new Date().toISOString(),
    });
    
    setConfirmDialogOpen(false);
    setShowSuccess(true);
    
    // Reset form after success
    setTimeout(() => {
      navigate('/executive/my-returns');
    }, 3000);
  };

  const filteredProducts = products.filter(product => 
    product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    product.category.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const totalReturnAmount = returnItems.reduce((sum, item) => sum + item.total, 0);

  const isStepValid = (step: number) => {
    switch (step) {
      case 0: // Select Supplier
        return !!selectedSupplier;
      case 1: // Add Return Items
        return returnItems.length > 0;
      case 2: // Upload Documents
        return true; // Document upload is optional
      case 3: // Review & Submit
        return true;
      default:
        return false;
    }
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Box>
        <PageHeader
          title="Create Return"
          subtitle="Return products to supplier"
        />

        {showSuccess && (
          <Alert 
            severity="success" 
            sx={{ mb: 3 }}
            onClose={() => setShowSuccess(false)}
          >
            Return has been successfully submitted for approval!
          </Alert>
        )}

        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Stepper activeStep={activeStep} alternativeLabel>
              {steps.map((label) => (
                <Step key={label}>
                  <StepLabel>{label}</StepLabel>
                </Step>
              ))}
            </Stepper>
          </CardContent>
        </Card>

        <motion.div
          key={activeStep}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -20 }}
          transition={{ duration: 0.3 }}
        >
          {activeStep === 0 && (
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Select Supplier
                </Typography>
                <Grid container spacing={3}>
                  <Grid item xs={12} md={6}>
                    <Autocomplete
                      options={suppliers}
                      getOptionLabel={(option) => option.name}
                      value={selectedSupplier}
                      onChange={(event, newValue) => {
                        setSelectedSupplier(newValue);
                      }}
                      renderInput={(params) => (
                        <TextField
                          {...params}
                          label="Select Supplier"
                          variant="outlined"
                          fullWidth
                          required
                        />
                      )}
                      renderOption={(props, option) => (
                        <li {...props}>
                          <Box>
                            <Typography variant="body1">{option.name}</Typography>
                            <Typography variant="caption" color="textSecondary">
                              Contact: {option.contact} | {option.phone}
                            </Typography>
                          </Box>
                        </li>
                      )}
                    />
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <DatePicker
                      label="Return Date"
                      value={returnDate}
                      onChange={(newValue) => setReturnDate(newValue)}
                      slotProps={{ textField: { fullWidth: true, required: true } }}
                    />
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <TextField
                      label="Reference Number"
                      value={referenceNumber}
                      onChange={(e) => setReferenceNumber(e.target.value)}
                      fullWidth
                      variant="outlined"
                      placeholder="Invoice or PO number"
                      helperText="Optional: Enter a reference number for this return"
                    />
                  </Grid>
                  {selectedSupplier && (
                    <Grid item xs={12}>
                      <Paper variant="outlined" sx={{ p: 2, mt: 2, backgroundColor: 'background.default' }}>
                        <Typography variant="subtitle2" gutterBottom>
                          Supplier Details
                        </Typography>
                        <Grid container spacing={2}>
                          <Grid item xs={12} md={6}>
                            <Typography variant="body2" color="textSecondary">
                              Contact Person
                            </Typography>
                            <Typography variant="body1">
                              {selectedSupplier.contact}
                            </Typography>
                          </Grid>
                          <Grid item xs={12} md={6}>
                            <Typography variant="body2" color="textSecondary">
                              Contact Number
                            </Typography>
                            <Typography variant="body1">
                              {selectedSupplier.phone}
                            </Typography>
                          </Grid>
                          <Grid item xs={12}>
                            <Typography variant="body2" color="textSecondary">
                              Email
                            </Typography>
                            <Typography variant="body1">
                              {selectedSupplier.email}
                            </Typography>
                          </Grid>
                        </Grid>
                      </Paper>
                    </Grid>
                  )}
                </Grid>
              </CardContent>
              <Divider />
              <Box sx={{ display: 'flex', justifyContent: 'flex-end', p: 2 }}>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleNext}
                  disabled={!isStepValid(0)}
                  endIcon={<ArrowForwardIcon />}
                >
                  Next
                </Button>
              </Box>
            </Card>
          )}

          {activeStep === 1 && (
            <Grid container spacing={3}>
              <Grid item xs={12} md={8}>
                <Card sx={{ mb: 3 }}>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Add Return Items
                    </Typography>
                    <Grid container spacing={2}>
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
                      <Grid item xs={6} md={2}>
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
                      <Grid item xs={12} md={3}>
                        <FormControl fullWidth>
                          <InputLabel id="reason-label">Return Reason</InputLabel>
                          <Select
                            labelId="reason-label"
                            value={reason}
                            onChange={(e) => setReason(e.target.value)}
                            label="Return Reason"
                          >
                            {returnReasons.map((reason) => (
                              <MenuItem key={reason.value} value={reason.value}>
                                {reason.label}
                              </MenuItem>
                            ))}
                          </Select>
                        </FormControl>
                      </Grid>
                      <Grid item xs={12}>
                        <TextField
                          label="Notes"
                          value={notes}
                          onChange={(e) => setNotes(e.target.value)}
                          fullWidth
                          variant="outlined"
                          multiline
                          rows={2}
                          placeholder="Enter any additional details about this return item"
                        />
                      </Grid>
                      <Grid item xs={12}>
                        <Button
                          variant="contained"
                          color="primary"
                          startIcon={<AddIcon />}
                          onClick={handleAddReturnItem}
                          disabled={!selectedProduct || quantity <= 0 || !reason}
                        >
                          Add Item
                        </Button>
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>

                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Return Items
                    </Typography>
                    {returnItems.length > 0 ? (
                      <TableContainer>
                        <Table>
                          <TableHead>
                            <TableRow>
                              <TableCell>Product</TableCell>
                              <TableCell align="right">Price</TableCell>
                              <TableCell align="center">Quantity</TableCell>
                              <TableCell align="right">Total</TableCell>
                              <TableCell>Reason</TableCell>
                              <TableCell align="center">Actions</TableCell>
                            </TableRow>
                          </TableHead>
                          <TableBody>
                            {returnItems.map((item) => (
                              <TableRow key={item.id}>
                                <TableCell>{item.productName}</TableCell>
                                <TableCell align="right">₹{item.price}</TableCell>
                                <TableCell align="center">{item.quantity}</TableCell>
                                <TableCell align="right">₹{item.total}</TableCell>
                                <TableCell>
                                  {returnReasons.find(r => r.value === item.reason)?.label}
                                </TableCell>
                                <TableCell align="center">
                                  <IconButton
                                    color="error"
                                    size="small"
                                    onClick={() => handleRemoveReturnItem(item.id)}
                                  >
                                    <DeleteIcon />
                                  </IconButton>
                                </TableCell>
                              </TableRow>
                            ))}
                            <TableRow>
                              <TableCell colSpan={3} align="right" sx={{ fontWeight: 'bold' }}>
                                Total Return Value:
                              </TableCell>
                              <TableCell align="right" sx={{ fontWeight: 'bold' }}>
                                ₹{totalReturnAmount}
                              </TableCell>
                              <TableCell colSpan={2}></TableCell>
                            </TableRow>
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
                        <ReturnIcon sx={{ fontSize: 40, color: 'text.secondary', mb: 1 }} />
                        <Typography variant="h6" color="textSecondary">
                          No return items added yet
                        </Typography>
                        <Typography variant="body2" color="textSecondary">
                          Add products to create a return
                        </Typography>
                      </Paper>
                    )}
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12} md={4}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Return Summary
                    </Typography>
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="subtitle2" color="textSecondary">
                        Supplier
                      </Typography>
                      <Typography variant="body1">
                        {selectedSupplier?.name}
                      </Typography>
                    </Box>
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="subtitle2" color="textSecondary">
                        Return Date
                      </Typography>
                      <Typography variant="body1">
                        {returnDate?.toLocaleDateString()}
                      </Typography>
                    </Box>
                    {referenceNumber && (
                      <Box sx={{ mb: 2 }}>
                        <Typography variant="subtitle2" color="textSecondary">
                          Reference Number
                        </Typography>
                        <Typography variant="body1">
                          {referenceNumber}
                        </Typography>
                      </Box>
                    )}
                    <Divider sx={{ my: 2 }} />
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="subtitle2" color="textSecondary">
                        Total Items
                      </Typography>
                      <Typography variant="body1">
                        {returnItems.length} items / {returnItems.reduce((sum, item) => sum + item.quantity, 0)} units
                      </Typography>
                    </Box>
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="subtitle2" color="textSecondary">
                        Total Return Value
                      </Typography>
                      <Typography variant="h6" color="primary">
                        ₹{totalReturnAmount}
                      </Typography>
                    </Box>
                  </CardContent>
                  <Divider />
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', p: 2 }}>
                    <Button
                      onClick={handleBack}
                      startIcon={<ArrowBackIcon />}
                    >
                      Back
                    </Button>
                    <Button
                      variant="contained"
                      color="primary"
                      onClick={handleNext}
                      disabled={!isStepValid(1)}
                      endIcon={<ArrowForwardIcon />}
                    >
                      Next
                    </Button>
                  </Box>
                </Card>
              </Grid>
            </Grid>
          )}

          {activeStep === 2 && (
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Upload Supporting Documents
                </Typography>
                <Typography variant="body2" color="textSecondary" paragraph>
                  Upload any supporting documents for this return, such as original invoices, quality reports, or correspondence with the supplier.
                </Typography>

                <Grid container spacing={3}>
                  <Grid item xs={12} md={6}>
                    <Box sx={{ border: '1px dashed', borderColor: 'divider', borderRadius: 1, p: 3, textAlign: 'center' }}>
                      <input
                        accept="image/*,application/pdf"
                        style={{ display: 'none' }}
                        id="upload-document"
                        type="file"
                        onChange={handleDocumentUpload}
                      />
                      <label htmlFor="upload-document">
                        <Button
                          variant="outlined"
                          component="span"
                          startIcon={<AttachFileIcon />}
                          sx={{ mb: 2 }}
                        >
                          Upload Document
                        </Button>
                      </label>
                      <Typography variant="caption" display="block" color="textSecondary">
                        Supported formats: JPG, PNG, PDF (Max size: 5MB)
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <Box sx={{ border: '1px dashed', borderColor: 'divider', borderRadius: 1, p: 3, textAlign: 'center' }}>
                      <Button
                        variant="outlined"
                        startIcon={<PhotoCameraIcon />}
                        sx={{ mb: 2 }}
                        onClick={() => {
                          // In a real app, this would open the camera
                          alert('Camera functionality would open here');
                        }}
                      >
                        Take Photo
                      </Button>
                      <Typography variant="caption" display="block" color="textSecondary">
                        Take a photo of the document using your device's camera
                      </Typography>
                    </Box>
                  </Grid>
                </Grid>

                {documentImage && (
                  <Box sx={{ mt: 3 }}>
                    <Typography variant="subtitle2" gutterBottom>
                      Uploaded Document
                    </Typography>
                    <Paper variant="outlined" sx={{ p: 2, mt: 1 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Box sx={{ flexGrow: 1 }}>
                          <Typography variant="body2">
                            Document uploaded successfully
                          </Typography>
                          <Typography variant="caption" color="textSecondary">
                            {new Date().toLocaleString()}
                          </Typography>
                        </Box>
                        <Box>
                          <IconButton
                            color="error"
                            size="small"
                            onClick={() => setDocumentImage(null)}
                          >
                            <DeleteIcon />
                          </IconButton>
                        </Box>
                      </Box>
                      <Box sx={{ mt: 2, textAlign: 'center' }}>
                        <img
                          src={documentImage}
                          alt="Document"
                          style={{
                            maxWidth: '100%',
                            maxHeight: 200,
                            objectFit: 'contain',
                            borderRadius: 4,
                          }}
                        />
                      </Box>
                    </Paper>
                  </Box>
                )}

                <Typography variant="body2" color="textSecondary" sx={{ mt: 3 }}>
                  Note: Document upload is optional but recommended for faster approval.
                </Typography>
              </CardContent>
              <Divider />
              <Box sx={{ display: 'flex', justifyContent: 'space-between', p: 2 }}>
                <Button
                  onClick={handleBack}
                  startIcon={<ArrowBackIcon />}
                >
                  Back
                </Button>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleNext}
                  endIcon={<ArrowForwardIcon />}
                >
                  Next
                </Button>
              </Box>
            </Card>
          )}

          {activeStep === 3 && (
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Review & Submit
                </Typography>
                <Typography variant="body2" color="textSecondary" paragraph>
                  Please review the return details before submitting for approval.
                </Typography>

                <Grid container spacing={3}>
                  <Grid item xs={12} md={6}>
                    <Paper variant="outlined" sx={{ p: 2 }}>
                      <Typography variant="subtitle2" gutterBottom>
                        Supplier Information
                      </Typography>
                      <Typography variant="body1">
                        {selectedSupplier?.name}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        Contact: {selectedSupplier?.contact}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        Phone: {selectedSupplier?.phone}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        Email: {selectedSupplier?.email}
                      </Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <Paper variant="outlined" sx={{ p: 2 }}>
                      <Typography variant="subtitle2" gutterBottom>
                        Return Details
                      </Typography>
                      <Typography variant="body2">
                        <strong>Return Date:</strong> {returnDate?.toLocaleDateString()}
                      </Typography>
                      {referenceNumber && (
                        <Typography variant="body2">
                          <strong>Reference Number:</strong> {referenceNumber}
                        </Typography>
                      )}
                      <Typography variant="body2">
                        <strong>Total Items:</strong> {returnItems.length} items / {returnItems.reduce((sum, item) => sum + item.quantity, 0)} units
                      </Typography>
                      <Typography variant="body2">
                        <strong>Total Return Value:</strong> ₹{totalReturnAmount}
                      </Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={12}>
                    <Typography variant="subtitle2" gutterBottom>
                      Return Items
                    </Typography>
                    <TableContainer component={Paper} variant="outlined">
                      <Table size="small">
                        <TableHead>
                          <TableRow>
                            <TableCell>Product</TableCell>
                            <TableCell align="right">Price</TableCell>
                            <TableCell align="center">Quantity</TableCell>
                            <TableCell align="right">Total</TableCell>
                            <TableCell>Reason</TableCell>
                            <TableCell>Notes</TableCell>
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {returnItems.map((item) => (
                            <TableRow key={item.id}>
                              <TableCell>{item.productName}</TableCell>
                              <TableCell align="right">₹{item.price}</TableCell>
                              <TableCell align="center">{item.quantity}</TableCell>
                              <TableCell align="right">₹{item.total}</TableCell>
                              <TableCell>
                                {returnReasons.find(r => r.value === item.reason)?.label}
                              </TableCell>
                              <TableCell>{item.notes || '-'}</TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </TableContainer>
                  </Grid>
                  {documentImage && (
                    <Grid item xs={12} md={6}>
                      <Typography variant="subtitle2" gutterBottom>
                        Supporting Document
                      </Typography>
                      <Paper variant="outlined" sx={{ p: 2 }}>
                        <Box sx={{ textAlign: 'center' }}>
                          <img
                            src={documentImage}
                            alt="Document"
                            style={{
                              maxWidth: '100%',
                              maxHeight: 150,
                              objectFit: 'contain',
                              borderRadius: 4,
                            }}
                          />
                        </Box>
                      </Paper>
                    </Grid>
                  )}
                </Grid>

                <Alert severity="info" sx={{ mt: 3 }}>
                  This return will be submitted for approval. You will be notified once it is approved or rejected.
                </Alert>
              </CardContent>
              <Divider />
              <Box sx={{ display: 'flex', justifyContent: 'space-between', p: 2 }}>
                <Button
                  onClick={handleBack}
                  startIcon={<ArrowBackIcon />}
                >
                  Back
                </Button>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={() => setConfirmDialogOpen(true)}
                  startIcon={<ReturnIcon />}
                >
                  Submit Return
                </Button>
              </Box>
            </Card>
          )}
        </motion.div>

        {/* Confirm Dialog */}
        <Dialog open={confirmDialogOpen} onClose={() => setConfirmDialogOpen(false)}>
          <DialogTitle>Confirm Return Submission</DialogTitle>
          <DialogContent>
            <Typography variant="body1" gutterBottom>
              Are you sure you want to submit this return for approval?
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Supplier: {selectedSupplier?.name}
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Total Items: {returnItems.length} items / {returnItems.reduce((sum, item) => sum + item.quantity, 0)} units
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Total Return Value: ₹{totalReturnAmount}
            </Typography>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setConfirmDialogOpen(false)}>Cancel</Button>
            <Button 
              onClick={handleSubmitReturn} 
              variant="contained" 
              color="primary"
            >
              Submit for Approval
            </Button>
          </DialogActions>
        </Dialog>
      </Box>
    </LocalizationProvider>
  );
};

export default CreateReturn;