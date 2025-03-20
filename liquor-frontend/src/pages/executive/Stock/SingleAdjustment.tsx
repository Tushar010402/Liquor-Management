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
  useTheme,
} from '@mui/material';
import {
  Add,
  Remove,
  Delete,
  Search,
  Inventory,
  Save,
  ArrowUpward,
  ArrowDownward,
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

// Adjustment reasons
const adjustmentReasons = [
  { value: 'physical_count', label: 'Physical Count' },
  { value: 'damaged', label: 'Damaged/Broken' },
  { value: 'expired', label: 'Expired' },
  { value: 'theft', label: 'Theft/Loss' },
  { value: 'return_to_supplier', label: 'Return to Supplier' },
  { value: 'received_from_supplier', label: 'Received from Supplier' },
  { value: 'internal_use', label: 'Internal Use' },
  { value: 'correction', label: 'Correction' },
];

interface AdjustmentItem {
  id: number;
  name: string;
  category: string;
  currentStock: number;
  newStock: number;
  adjustmentType: 'increase' | 'decrease';
  adjustmentQuantity: number;
}

const SingleAdjustment: React.FC = () => {
  const theme = useTheme();
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedProduct, setSelectedProduct] = useState<any | null>(null);
  const [adjustmentType, setAdjustmentType] = useState<'increase' | 'decrease'>('increase');
  const [adjustmentQuantity, setAdjustmentQuantity] = useState(1);
  const [adjustmentReason, setAdjustmentReason] = useState('physical_count');
  const [adjustmentNote, setAdjustmentNote] = useState('');
  const [adjustmentItems, setAdjustmentItems] = useState<AdjustmentItem[]>([]);
  const [barcodeInput, setBarcodeInput] = useState('');
  const [confirmDialogOpen, setConfirmDialogOpen] = useState(false);

  // Handle adding product to adjustment
  const handleAddToAdjustment = () => {
    if (!selectedProduct) return;

    const newStock = adjustmentType === 'increase' 
      ? selectedProduct.stock + adjustmentQuantity 
      : selectedProduct.stock - adjustmentQuantity;

    // Don't allow negative stock
    if (newStock < 0) {
      alert('Adjustment would result in negative stock. Please check the quantity.');
      return;
    }

    const existingItemIndex = adjustmentItems.findIndex(item => item.id === selectedProduct.id);

    if (existingItemIndex >= 0) {
      // Update existing item
      const updatedItems = [...adjustmentItems];
      updatedItems[existingItemIndex] = {
        ...updatedItems[existingItemIndex],
        adjustmentType,
        adjustmentQuantity,
        newStock,
      };
      setAdjustmentItems(updatedItems);
    } else {
      // Add new item
      setAdjustmentItems([
        ...adjustmentItems,
        {
          id: selectedProduct.id,
          name: selectedProduct.name,
          category: selectedProduct.category,
          currentStock: selectedProduct.stock,
          newStock,
          adjustmentType,
          adjustmentQuantity,
        },
      ]);
    }

    // Reset selection
    setSelectedProduct(null);
    setAdjustmentQuantity(1);
  };

  // Handle barcode scan
  const handleBarcodeSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const product = productsData.find(p => p.barcode === barcodeInput);
    
    if (product) {
      setSelectedProduct(product);
      setBarcodeInput('');
    }
  };

  // Handle removing item from adjustment
  const handleRemoveItem = (id: number) => {
    setAdjustmentItems(adjustmentItems.filter(item => item.id !== id));
  };

  // Handle submit adjustment
  const handleSubmitAdjustment = () => {
    if (adjustmentItems.length === 0) {
      alert('Please add at least one item to the adjustment.');
      return;
    }

    setConfirmDialogOpen(true);
  };

  // Handle confirm adjustment
  const handleConfirmAdjustment = () => {
    // In a real app, this would send the adjustment data to the backend
    console.log({
      items: adjustmentItems,
      reason: adjustmentReason,
      note: adjustmentNote,
      timestamp: new Date().toISOString(),
    });

    // Close dialog and navigate to dashboard
    setConfirmDialogOpen(false);
    
    // Show success message and redirect
    alert('Stock adjustment submitted for approval!');
    navigate('/executive/my-adjustments');
  };

  // Handle save as draft
  const handleSaveAsDraft = () => {
    // In a real app, this would save the adjustment as a draft
    console.log('Saving as draft', {
      items: adjustmentItems,
      reason: adjustmentReason,
      note: adjustmentNote,
    });
    
    alert('Adjustment saved as draft!');
    navigate('/executive/my-adjustments');
  };

  return (
    <Box>
      <PageHeader
        title="Stock Adjustment"
        subtitle="Adjust inventory stock levels"
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
                      <Grid item xs={12} sm={4}>
                        <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                          {selectedProduct.name}
                        </Typography>
                        <Typography variant="body2" color="textSecondary">
                          Category: {selectedProduct.category}
                        </Typography>
                        <Typography variant="body2" color="textSecondary">
                          Current Stock: {selectedProduct.stock}
                        </Typography>
                      </Grid>
                      <Grid item xs={12} sm={3}>
                        <FormControl fullWidth size="small">
                          <InputLabel id="adjustment-type-label">Type</InputLabel>
                          <Select
                            labelId="adjustment-type-label"
                            id="adjustment-type"
                            value={adjustmentType}
                            label="Type"
                            onChange={(e) => setAdjustmentType(e.target.value as 'increase' | 'decrease')}
                          >
                            <MenuItem value="increase">
                              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                <ArrowUpward fontSize="small" sx={{ color: 'success.main', mr: 1 }} />
                                Increase
                              </Box>
                            </MenuItem>
                            <MenuItem value="decrease">
                              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                <ArrowDownward fontSize="small" sx={{ color: 'error.main', mr: 1 }} />
                                Decrease
                              </Box>
                            </MenuItem>
                          </Select>
                        </FormControl>
                      </Grid>
                      <Grid item xs={12} sm={3}>
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          <IconButton 
                            size="small" 
                            onClick={() => setAdjustmentQuantity(Math.max(1, adjustmentQuantity - 1))}
                          >
                            <Remove fontSize="small" />
                          </IconButton>
                          <TextField
                            size="small"
                            value={adjustmentQuantity}
                            onChange={(e) => {
                              const value = parseInt(e.target.value);
                              if (!isNaN(value) && value > 0) {
                                setAdjustmentQuantity(value);
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
                            onClick={() => setAdjustmentQuantity(adjustmentQuantity + 1)}
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
                          onClick={handleAddToAdjustment}
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
                  Adjustment Items
                </Typography>
                {adjustmentItems.length > 0 ? (
                  <TableContainer component={Paper} variant="outlined">
                    <Table>
                      <TableHead>
                        <TableRow>
                          <TableCell>Product</TableCell>
                          <TableCell align="center">Current Stock</TableCell>
                          <TableCell align="center">Adjustment</TableCell>
                          <TableCell align="center">New Stock</TableCell>
                          <TableCell align="center">Actions</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {adjustmentItems.map((item) => (
                          <TableRow key={item.id}>
                            <TableCell>
                              <Typography variant="body2" sx={{ fontWeight: 500 }}>
                                {item.name}
                              </Typography>
                              <Typography variant="caption" color="textSecondary">
                                {item.category}
                              </Typography>
                            </TableCell>
                            <TableCell align="center">{item.currentStock}</TableCell>
                            <TableCell align="center">
                              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                {item.adjustmentType === 'increase' ? (
                                  <ArrowUpward fontSize="small" sx={{ color: 'success.main', mr: 0.5 }} />
                                ) : (
                                  <ArrowDownward fontSize="small" sx={{ color: 'error.main', mr: 0.5 }} />
                                )}
                                {item.adjustmentQuantity}
                              </Box>
                            </TableCell>
                            <TableCell align="center">{item.newStock}</TableCell>
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
                    <Inventory sx={{ fontSize: 40, color: 'text.secondary', mb: 1 }} />
                    <Typography variant="subtitle1" color="textSecondary">
                      No items added
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
                Adjustment Details
              </Typography>
              
              <FormControl fullWidth margin="normal">
                <InputLabel id="adjustment-reason-label">Adjustment Reason</InputLabel>
                <Select
                  labelId="adjustment-reason-label"
                  id="adjustment-reason"
                  value={adjustmentReason}
                  label="Adjustment Reason"
                  onChange={(e) => setAdjustmentReason(e.target.value)}
                >
                  {adjustmentReasons.map((reason) => (
                    <MenuItem key={reason.value} value={reason.value}>
                      {reason.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
              
              <TextField
                fullWidth
                label="Notes"
                variant="outlined"
                multiline
                rows={4}
                value={adjustmentNote}
                onChange={(e) => setAdjustmentNote(e.target.value)}
                margin="normal"
                placeholder="Enter any additional details about this adjustment..."
              />
              
              <Divider sx={{ my: 3 }} />
              
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="textSecondary" gutterBottom>
                  Summary
                </Typography>
                <Grid container spacing={1}>
                  <Grid item xs={8}>
                    <Typography variant="body2">Total Items:</Typography>
                  </Grid>
                  <Grid item xs={4}>
                    <Typography variant="body2" align="right">{adjustmentItems.length}</Typography>
                  </Grid>
                  
                  <Grid item xs={8}>
                    <Typography variant="body2">Increases:</Typography>
                  </Grid>
                  <Grid item xs={4}>
                    <Typography variant="body2" align="right">
                      {adjustmentItems.filter(item => item.adjustmentType === 'increase').length}
                    </Typography>
                  </Grid>
                  
                  <Grid item xs={8}>
                    <Typography variant="body2">Decreases:</Typography>
                  </Grid>
                  <Grid item xs={4}>
                    <Typography variant="body2" align="right">
                      {adjustmentItems.filter(item => item.adjustmentType === 'decrease').length}
                    </Typography>
                  </Grid>
                </Grid>
              </Box>
              
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <Button
                  variant="contained"
                  color="primary"
                  size="large"
                  fullWidth
                  startIcon={<Inventory />}
                  onClick={handleSubmitAdjustment}
                  disabled={adjustmentItems.length === 0}
                >
                  Submit for Approval
                </Button>
                
                <Button
                  variant="outlined"
                  color="secondary"
                  fullWidth
                  startIcon={<Save />}
                  onClick={handleSaveAsDraft}
                  disabled={adjustmentItems.length === 0}
                >
                  Save as Draft
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Confirmation Dialog */}
      <Dialog open={confirmDialogOpen} onClose={() => setConfirmDialogOpen(false)}>
        <DialogTitle>Confirm Stock Adjustment</DialogTitle>
        <DialogContent>
          <Typography variant="body1" gutterBottom>
            Are you sure you want to submit this stock adjustment for approval?
          </Typography>
          <Typography variant="body2" color="textSecondary">
            This will adjust the stock levels for {adjustmentItems.length} items.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setConfirmDialogOpen(false)}>Cancel</Button>
          <Button 
            onClick={handleConfirmAdjustment} 
            variant="contained" 
            color="primary"
          >
            Confirm
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default SingleAdjustment;