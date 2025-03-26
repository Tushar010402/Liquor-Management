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
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormHelperText,
  InputAdornment,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Paper,
  Stepper,
  Step,
  StepLabel,
} from '@mui/material';
import {
  AttachFile,
  PhotoCamera,
} from '@mui/icons-material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { motion } from 'framer-motion';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { PageHeader } from '../../../components/common';
import { useNavigate } from 'react-router-dom';

// Validation schema
const validationSchema = Yup.object({
  amount: Yup.number()
    .required('Amount is required')
    .positive('Amount must be positive')
    .max(50000, 'Amount cannot exceed ₹50,000'),
  category: Yup.string()
    .required('Category is required'),
  paidTo: Yup.string()
    .required('Recipient name is required')
    .max(100, 'Name cannot exceed 100 characters'),
  expenseDate: Yup.date()
    .required('Expense date is required')
    .max(new Date(), 'Expense date cannot be in the future'),
  notes: Yup.string()
    .max(500, 'Notes cannot exceed 500 characters'),
});

// Expense categories
const expenseCategories = [
  { value: 'utilities', label: 'Utilities' },
  { value: 'supplies', label: 'Supplies' },
  { value: 'maintenance', label: 'Maintenance' },
  { value: 'transport', label: 'Transportation' },
  { value: 'salary', label: 'Salary/Wages' },
  { value: 'rent', label: 'Rent' },
  { value: 'marketing', label: 'Marketing' },
  { value: 'other', label: 'Other' },
];

const RecordExpense: React.FC = () => {
  const navigate = useNavigate();
  const [activeStep, setActiveStep] = useState(0);
  const [confirmDialogOpen, setConfirmDialogOpen] = useState(false);
  const [receiptImage, setReceiptImage] = useState<string | null>(null);

  const formik = useFormik({
    initialValues: {
      amount: '',
      category: '',
      paidTo: '',
      expenseDate: new Date(),
      notes: '',
    },
    validationSchema: validationSchema,
    onSubmit: (values) => {
      setConfirmDialogOpen(true);
    },
  });

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleConfirmExpense = () => {
    // In a real app, this would send the expense data to the backend
    console.log({
      ...formik.values,
      receiptImage,
      timestamp: new Date().toISOString(),
    });

    // Close dialog and navigate to cash balance
    setConfirmDialogOpen(false);
    
    // Show success message and redirect
    alert('Expense submitted for approval!');
    navigate('/executive/cash-balance');
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

  const steps = ['Enter Expense Details', 'Upload Receipt', 'Review & Submit'];

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Box>
        <PageHeader
          title="Record Expense"
          subtitle="Submit expense details for approval"
        />

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

        <form onSubmit={formik.handleSubmit}>
          {activeStep === 0 && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Expense Details
                  </Typography>
                  <Grid container spacing={3}>
                    <Grid item xs={12} md={6}>
                      <TextField
                        fullWidth
                        id="amount"
                        name="amount"
                        label="Amount"
                        variant="outlined"
                        type="number"
                        InputProps={{
                          startAdornment: <InputAdornment position="start">₹</InputAdornment>,
                        }}
                        value={formik.values.amount}
                        onChange={formik.handleChange}
                        onBlur={formik.handleBlur}
                        error={formik.touched.amount && Boolean(formik.errors.amount)}
                        helperText={formik.touched.amount && formik.errors.amount}
                      />
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <FormControl 
                        fullWidth
                        error={formik.touched.category && Boolean(formik.errors.category)}
                      >
                        <InputLabel id="category-label">Expense Category</InputLabel>
                        <Select
                          labelId="category-label"
                          id="category"
                          name="category"
                          label="Expense Category"
                          value={formik.values.category}
                          onChange={formik.handleChange}
                          onBlur={formik.handleBlur}
                        >
                          {expenseCategories.map((category) => (
                            <MenuItem key={category.value} value={category.value}>
                              {category.label}
                            </MenuItem>
                          ))}
                        </Select>
                        {formik.touched.category && formik.errors.category && (
                          <FormHelperText>{formik.errors.category}</FormHelperText>
                        )}
                      </FormControl>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <TextField
                        fullWidth
                        id="paidTo"
                        name="paidTo"
                        label="Paid To"
                        variant="outlined"
                        placeholder="Enter name of recipient"
                        value={formik.values.paidTo}
                        onChange={formik.handleChange}
                        onBlur={formik.handleBlur}
                        error={formik.touched.paidTo && Boolean(formik.errors.paidTo)}
                        helperText={formik.touched.paidTo && formik.errors.paidTo}
                      />
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <DatePicker
                        label="Expense Date"
                        value={formik.values.expenseDate}
                        onChange={(newValue) => formik.setFieldValue('expenseDate', newValue)}
                        slotProps={{ 
                          textField: { 
                            fullWidth: true,
                            error: formik.touched.expenseDate && Boolean(formik.errors.expenseDate),
                            helperText: formik.touched.expenseDate && formik.errors.expenseDate 
                              ? String(formik.errors.expenseDate) 
                              : '',
                          } 
                        }}
                      />
                    </Grid>
                    <Grid item xs={12}>
                      <TextField
                        fullWidth
                        id="notes"
                        name="notes"
                        label="Notes"
                        variant="outlined"
                        multiline
                        rows={3}
                        placeholder="Enter expense details..."
                        value={formik.values.notes}
                        onChange={formik.handleChange}
                        onBlur={formik.handleBlur}
                        error={formik.touched.notes && Boolean(formik.errors.notes)}
                        helperText={formik.touched.notes && formik.errors.notes}
                      />
                    </Grid>
                  </Grid>
                </CardContent>
                <Divider />
                <Box sx={{ display: 'flex', justifyContent: 'flex-end', p: 2 }}>
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={handleNext}
                    disabled={
                      !formik.values.amount ||
                      !formik.values.category ||
                      !formik.values.paidTo ||
                      !formik.values.expenseDate
                    }
                  >
                    Next
                  </Button>
                </Box>
              </Card>
            </motion.div>
          )}

          {activeStep === 1 && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Upload Receipt
                  </Typography>
                  <Typography variant="body2" color="textSecondary" paragraph>
                    Please upload a photo or scan of the receipt or invoice for this expense.
                  </Typography>

                  <Box sx={{ mt: 3, mb: 3 }}>
                    <input
                      accept="image/*"
                      style={{ display: 'none' }}
                      id="receipt-image-upload"
                      type="file"
                      onChange={handleImageUpload}
                    />
                    <label htmlFor="receipt-image-upload">
                      <Button
                        variant="outlined"
                        component="span"
                        startIcon={<AttachFile />}
                        sx={{ mr: 2 }}
                      >
                        Select File
                      </Button>
                      <Button
                        variant="outlined"
                        component="span"
                        startIcon={<PhotoCamera />}
                        color="secondary"
                      >
                        Take Photo
                      </Button>
                    </label>
                  </Box>

                  {receiptImage ? (
                    <Box sx={{ mt: 2, textAlign: 'center' }}>
                      <Paper 
                        elevation={2} 
                        sx={{ 
                          p: 1, 
                          maxWidth: 400, 
                          mx: 'auto',
                          borderRadius: 2,
                          overflow: 'hidden',
                        }}
                      >
                        <img 
                          src={receiptImage} 
                          alt="Receipt" 
                          style={{ 
                            width: '100%', 
                            height: 'auto',
                            borderRadius: 8,
                          }} 
                        />
                      </Paper>
                      <Typography variant="body2" color="success.main" sx={{ mt: 1 }}>
                        Image uploaded successfully
                      </Typography>
                    </Box>
                  ) : (
                    <Box 
                      sx={{ 
                        mt: 2, 
                        p: 4, 
                        border: '2px dashed', 
                        borderColor: 'divider',
                        borderRadius: 2,
                        textAlign: 'center',
                      }}
                    >
                      <Typography variant="body1" color="textSecondary">
                        No image uploaded yet
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        Upload a clear image of your receipt or invoice
                      </Typography>
                    </Box>
                  )}
                </CardContent>
                <Divider />
                <Box sx={{ display: 'flex', justifyContent: 'space-between', p: 2 }}>
                  <Button onClick={handleBack}>
                    Back
                  </Button>
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={handleNext}
                  >
                    Next
                  </Button>
                </Box>
              </Card>
            </motion.div>
          )}

          {activeStep === 2 && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Review Expense Details
                  </Typography>
                  <Typography variant="body2" color="textSecondary" paragraph>
                    Please review the expense details before submitting for approval.
                  </Typography>

                  <Grid container spacing={2} sx={{ mt: 2 }}>
                    <Grid item xs={12} md={6}>
                      <Typography variant="subtitle2" color="textSecondary">
                        Amount
                      </Typography>
                      <Typography variant="body1" sx={{ fontWeight: 500 }}>
                        ₹{formik.values.amount}
                      </Typography>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Typography variant="subtitle2" color="textSecondary">
                        Category
                      </Typography>
                      <Typography variant="body1" sx={{ fontWeight: 500 }}>
                        {expenseCategories.find(c => c.value === formik.values.category)?.label}
                      </Typography>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Typography variant="subtitle2" color="textSecondary">
                        Paid To
                      </Typography>
                      <Typography variant="body1" sx={{ fontWeight: 500 }}>
                        {formik.values.paidTo}
                      </Typography>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Typography variant="subtitle2" color="textSecondary">
                        Expense Date
                      </Typography>
                      <Typography variant="body1" sx={{ fontWeight: 500 }}>
                        {formik.values.expenseDate.toLocaleDateString()}
                      </Typography>
                    </Grid>
                    <Grid item xs={12}>
                      <Typography variant="subtitle2" color="textSecondary">
                        Notes
                      </Typography>
                      <Typography variant="body1" sx={{ fontWeight: 500 }}>
                        {formik.values.notes || 'No notes provided'}
                      </Typography>
                    </Grid>
                  </Grid>

                  {receiptImage && (
                    <Box sx={{ mt: 3 }}>
                      <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                        Receipt
                      </Typography>
                      <Paper 
                        elevation={2} 
                        sx={{ 
                          p: 1, 
                          maxWidth: 200, 
                          borderRadius: 2,
                          overflow: 'hidden',
                        }}
                      >
                        <img 
                          src={receiptImage} 
                          alt="Receipt" 
                          style={{ 
                            width: '100%', 
                            height: 'auto',
                            borderRadius: 8,
                          }} 
                        />
                      </Paper>
                    </Box>
                  )}
                </CardContent>
                <Divider />
                <Box sx={{ display: 'flex', justifyContent: 'space-between', p: 2 }}>
                  <Button onClick={handleBack}>
                    Back
                  </Button>
                  <Button
                    type="submit"
                    variant="contained"
                    color="primary"
                  >
                    Submit for Approval
                  </Button>
                </Box>
              </Card>
            </motion.div>
          )}
        </form>

        {/* Confirmation Dialog */}
        <Dialog open={confirmDialogOpen} onClose={() => setConfirmDialogOpen(false)}>
          <DialogTitle>Confirm Expense Submission</DialogTitle>
          <DialogContent>
            <Typography variant="body1" gutterBottom>
              Are you sure you want to submit this expense for approval?
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Amount: ₹{formik.values.amount}
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Category: {expenseCategories.find(c => c.value === formik.values.category)?.label}
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Paid To: {formik.values.paidTo}
            </Typography>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setConfirmDialogOpen(false)}>Cancel</Button>
            <Button 
              onClick={handleConfirmExpense} 
              variant="contained" 
              color="primary"
            >
              Confirm
            </Button>
          </DialogActions>
        </Dialog>
      </Box>
    </LocalizationProvider>
  );
};

export default RecordExpense;