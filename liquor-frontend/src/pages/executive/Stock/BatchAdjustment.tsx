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
  Inventory as InventoryIcon,
  Search as SearchIcon,
  ArrowUpward as ArrowUpwardIcon,
  ArrowDownward as ArrowDownwardIcon,
  PhotoCamera as PhotoCameraIcon,
  AttachFile as AttachFileIcon,
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

// Adjustment reasons
const adjustmentReasons = [
  { value: 'damaged', label: 'Damaged Product', type: 'decrease' },
  { value: 'expired', label: 'Expired Product', type: 'decrease' },
  { value: 'theft', label: 'Theft/Loss', type: 'decrease' },
  { value: 'return_to_supplier', label: 'Return to Supplier', type: 'decrease' },
  { value: 'inventory_count', label: 'Inventory Count Adjustment', type: 'both' },
  { value: 'received_from_supplier', label: 'Received from Supplier', type: 'increase' },
  { value: 'return_from_customer', label: 'Return from Customer', type: 'increase' },
  { value: 'found', label: 'Found Items', type: 'increase' },
  { value: 'other', label: 'Other', type: 'both' },
];

interface AdjustmentItem {
  id: number;
  productId: number;
  productName: string;
  currentStock: number;
  adjustmentType: 'increase' | 'decrease';
  adjustmentQuantity: number;
  reason: string;
  notes: string;
}

const BatchAdjustment: React.FC = () => {
  const navigate = useNavigate();
  const [adjustments, setAdjustments] = useState<AdjustmentItem[]>([]);
  const [selectedProduct, setSelectedProduct] = useState<any | null>(null);
  const [adjustmentType, setAdjustmentType] = useState<'increase' | 'decrease'>('decrease');
  const [adjustmentQuantity, setAdjustmentQuantity] = useState<number>(1);
  const [reason, setReason] = useState<string>('');
  const [notes, setNotes] = useState<string>('');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [adjustmentDate, setAdjustmentDate] = useState<Date | null>(new Date());
  const [confirmDialogOpen, setConfirmDialogOpen] = useState<boolean>(false);
  const [receiptImage, setReceiptImage] = useState<string | null>(null);
  const [showSuccess, setShowSuccess] = useState<boolean>(false);

  const handleAddAdjustment = () => {
    if (selectedProduct && adjustmentQuantity > 0 && reason) {
      const newAdjustment: AdjustmentItem = {
        id: Date.now(), // Use timestamp as temporary ID
        productId: selectedProduct.id,
        productName: selectedProduct.name,
        currentStock: selectedProduct.stock,
        adjustmentType,
        adjustmentQuantity,
        reason,
        notes,
      };
      
      setAdjustments([...adjustments, newAdjustment]);
      
      // Reset form
      setSelectedProduct(null);
      setAdjustmentQuantity(1);
      setNotes('');
    }
  };

  const handleRemoveAdjustment = (id: number) => {
    setAdjustments(adjustments.filter(item => item.id !== id));
  };

  const handleReasonChange = (event: SelectChangeEvent) => {
    setReason(event.target.value);
    
    // Auto-select adjustment type based on reason
    const reasonData = adjustmentReasons.find(r => r.value === event.target.value);
    if (reasonData && reasonData.type !== 'both') {
      setAdjustmentType(reasonData.type as 'increase' | 'decrease');
    }
  };

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        setReceiptImage(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmitAdjustments = () => {
    // In a real app, this would send the adjustments data to the backend
    console.log({
      adjustments,
      adjustmentDate,
      receiptImage,
      timestamp: new Date().toISOString(),
    });
    
    setConfirmDialogOpen(false);
    setShowSuccess(true);
    
    // Reset form after success
    setTimeout(() => {
      setAdjustments([]);
      setAdjustmentDate(new Date());
      setReceiptImage(null);
      setShowSuccess(false);
    }, 3000);
  };

  const filteredProducts = products.filter(product => 
    product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    product.category.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const filteredReasons = adjustmentReasons.filter(r => 
    r.type === 'both' || r.type === adjustmentType
  );

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Box>
        <PageHeader
          title="Batch Stock Adjustment"
          subtitle="Adjust stock levels for multiple products"
        />

        {showSuccess && (
          <Alert 
            severity="success" 
            sx={{ mb: 3 }}
            onClose={() => setShowSuccess(false)}
          >
            Stock adjustments have been successfully submitted for approval!
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
                    Add Stock Adjustment
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={6}>
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
                    <Grid item xs={12} md={6}>
                      {selectedProduct && (
                        <Box sx={{ p: 2, border: '1px solid', borderColor: 'divider', borderRadius: 1 }}>
                          <Typography variant="subtitle2" color="textSecondary">
                            Current Stock
                          </Typography>
                          <Typography variant="h6">
                            {selectedProduct.stock} units
                          </Typography>
                          <Typography variant="caption" color="textSecondary">
                            {selectedProduct.category} | ₹{selectedProduct.price} per unit
                          </Typography>
                        </Box>
                      )}
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <FormControl fullWidth>
                        <InputLabel id="adjustment-type-label">Adjustment Type</InputLabel>
                        <Select
                          labelId="adjustment-type-label"
                          value={adjustmentType}
                          onChange={(e) => setAdjustmentType(e.target.value as 'increase' | 'decrease')}
                          label="Adjustment Type"
                        >
                          <MenuItem value="increase">
                            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                              <ArrowUpwardIcon color="success" sx={{ mr: 1 }} />
                              Increase Stock
                            </Box>
                          </MenuItem>
                          <MenuItem value="decrease">
                            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                              <ArrowDownwardIcon color="error" sx={{ mr: 1 }} />
                              Decrease Stock
                            </Box>
                          </MenuItem>
                        </Select>
                      </FormControl>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <TextField
                        label="Adjustment Quantity"
                        type="number"
                        value={adjustmentQuantity}
                        onChange={(e) => setAdjustmentQuantity(parseInt(e.target.value) || 0)}
                        fullWidth
                        variant="outlined"
                        InputProps={{
                          inputProps: { min: 1 },
                        }}
                      />
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <FormControl fullWidth>
                        <InputLabel id="reason-label">Reason</InputLabel>
                        <Select
                          labelId="reason-label"
                          value={reason}
                          onChange={handleReasonChange}
                          label="Reason"
                        >
                          {filteredReasons.map((reason) => (
                            <MenuItem key={reason.value} value={reason.value}>
                              {reason.label}
                            </MenuItem>
                          ))}
                        </Select>
                      </FormControl>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <TextField
                        label="Notes"
                        value={notes}
                        onChange={(e) => setNotes(e.target.value)}
                        fullWidth
                        variant="outlined"
                        multiline
                        rows={1}
                      />
                    </Grid>
                    <Grid item xs={12}>
                      <Button
                        variant="contained"
                        color="primary"
                        startIcon={<AddIcon />}
                        onClick={handleAddAdjustment}
                        disabled={!selectedProduct || adjustmentQuantity <= 0 || !reason}
                      >
                        Add to Batch
                      </Button>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>

              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Adjustment Batch
                  </Typography>
                  {adjustments.length > 0 ? (
                    <TableContainer>
                      <Table>
                        <TableHead>
                          <TableRow>
                            <TableCell>Product</TableCell>
                            <TableCell align="center">Current Stock</TableCell>
                            <TableCell align="center">Type</TableCell>
                            <TableCell align="center">Quantity</TableCell>
                            <TableCell>Reason</TableCell>
                            <TableCell>Notes</TableCell>
                            <TableCell align="center">Actions</TableCell>
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {adjustments.map((item) => (
                            <TableRow key={item.id}>
                              <TableCell>{item.productName}</TableCell>
                              <TableCell align="center">{item.currentStock}</TableCell>
                              <TableCell align="center">
                                {item.adjustmentType === 'increase' ? (
                                  <Chip
                                    icon={<ArrowUpwardIcon />}
                                    label="Increase"
                                    color="success"
                                    size="small"
                                  />
                                ) : (
                                  <Chip
                                    icon={<ArrowDownwardIcon />}
                                    label="Decrease"
                                    color="error"
                                    size="small"
                                  />
                                )}
                              </TableCell>
                              <TableCell align="center">{item.adjustmentQuantity}</TableCell>
                              <TableCell>
                                {adjustmentReasons.find(r => r.value === item.reason)?.label}
                              </TableCell>
                              <TableCell>{item.notes || '-'}</TableCell>
                              <TableCell align="center">
                                <IconButton
                                  color="error"
                                  size="small"
                                  onClick={() => handleRemoveAdjustment(item.id)}
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
                      <InventoryIcon sx={{ fontSize: 40, color: 'text.secondary', mb: 1 }} />
                      <Typography variant="h6" color="textSecondary">
                        No adjustments added yet
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        Add products to create a batch adjustment
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
                    Adjustment Details
                  </Typography>
                  <DatePicker
                    label="Adjustment Date"
                    value={adjustmentDate}
                    onChange={(newValue) => setAdjustmentDate(newValue)}
                    slotProps={{ textField: { fullWidth: true, margin: 'normal' } }}
                  />
                  <Box sx={{ mt: 3 }}>
                    <Typography variant="subtitle2" gutterBottom>
                      Supporting Document (Optional)
                    </Typography>
                    <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
                      <input
                        accept="image/*"
                        style={{ display: 'none' }}
                        id="upload-image"
                        type="file"
                        onChange={handleImageUpload}
                      />
                      <label htmlFor="upload-image">
                        <Button
                          variant="outlined"
                          component="span"
                          startIcon={<AttachFileIcon />}
                        >
                          Upload File
                        </Button>
                      </label>
                      <Button
                        variant="outlined"
                        startIcon={<PhotoCameraIcon />}
                        onClick={() => {
                          // In a real app, this would open the camera
                          alert('Camera functionality would open here');
                        }}
                      >
                        Take Photo
                      </Button>
                    </Box>
                    {receiptImage && (
                      <Box sx={{ mt: 2, textAlign: 'center' }}>
                        <img
                          src={receiptImage}
                          alt="Document"
                          style={{
                            maxWidth: '100%',
                            maxHeight: 200,
                            objectFit: 'contain',
                            borderRadius: 4,
                          }}
                        />
                        <Typography variant="caption" color="textSecondary" display="block">
                          Document uploaded
                        </Typography>
                      </Box>
                    )}
                  </Box>
                </CardContent>
                <Divider />
                <Box sx={{ p: 2 }}>
                  <Button
                    variant="contained"
                    color="primary"
                    fullWidth
                    size="large"
                    startIcon={<SaveIcon />}
                    onClick={() => setConfirmDialogOpen(true)}
                    disabled={adjustments.length === 0}
                  >
                    Submit Adjustments
                  </Button>
                </Box>
              </Card>

              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Batch Summary
                  </Typography>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" color="textSecondary">
                      Total Adjustments
                    </Typography>
                    <Typography variant="h5">
                      {adjustments.length}
                    </Typography>
                  </Box>
                  <Divider sx={{ my: 2 }} />
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" color="textSecondary">
                      Increases
                    </Typography>
                    <Typography variant="body1" color="success.main">
                      {adjustments.filter(a => a.adjustmentType === 'increase').length} items
                      {' / '}
                      {adjustments
                        .filter(a => a.adjustmentType === 'increase')
                        .reduce((sum, item) => sum + item.adjustmentQuantity, 0)} units
                    </Typography>
                  </Box>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" color="textSecondary">
                      Decreases
                    </Typography>
                    <Typography variant="body1" color="error.main">
                      {adjustments.filter(a => a.adjustmentType === 'decrease').length} items
                      {' / '}
                      {adjustments
                        .filter(a => a.adjustmentType === 'decrease')
                        .reduce((sum, item) => sum + item.adjustmentQuantity, 0)} units
                    </Typography>
                  </Box>
                  <Divider sx={{ my: 2 }} />
                  <Typography variant="body2" color="textSecondary">
                    All stock adjustments require manager approval before they are applied to inventory.
                  </Typography>
                </CardContent>
              </Card>
            </motion.div>
          </Grid>
        </Grid>

        {/* Confirm Dialog */}
        <Dialog open={confirmDialogOpen} onClose={() => setConfirmDialogOpen(false)}>
          <DialogTitle>Confirm Stock Adjustments</DialogTitle>
          <DialogContent>
            <Typography variant="body1" gutterBottom>
              Are you sure you want to submit these stock adjustments for approval?
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Total Adjustments: {adjustments.length}
            </Typography>
            <Typography variant="body2" color="success.main">
              Increases: {adjustments.filter(a => a.adjustmentType === 'increase').length} items
            </Typography>
            <Typography variant="body2" color="error.main">
              Decreases: {adjustments.filter(a => a.adjustmentType === 'decrease').length} items
            </Typography>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setConfirmDialogOpen(false)}>Cancel</Button>
            <Button 
              onClick={handleSubmitAdjustments} 
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

export default BatchAdjustment;