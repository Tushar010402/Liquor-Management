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

// Validation schema
const validationSchema = Yup.object({
  amount: Yup.number()
    .required('Amount is required')
    .positive('Amount must be positive')
    .max(100000, 'Amount cannot exceed ₹100,000'),
  bankAccount: Yup.string()
    .required('Bank account is required'),
  referenceNumber: Yup.string()
    .required('Reference number is required'),
  depositDate: Yup.date()
    .required('Deposit date is required')
    .max(new Date(), 'Deposit date cannot be in the future'),
  notes: Yup.string()
    .max(500, 'Notes cannot exceed 500 characters'),
});

const RecordDeposit: React.FC = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [confirmDialogOpen, setConfirmDialogOpen] = useState(false);
  const [depositImage, setDepositImage] = useState<string | null>(null);

  const formik = useFormik({
    initialValues: {
      amount: '',
      bankAccount: '',
      referenceNumber: '',
      depositDate: new Date(),
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

  const handleConfirmDeposit = () => {
    // In a real app, this would send the deposit data to the backend
    console.log({
      ...formik.values,
      depositImage,
      timestamp: new Date().toISOString(),
    });

    // Close dialog and navigate to cash balance
    setConfirmDialogOpen(false);
    
    // Show success message and redirect
    alert('Deposit submitted for approval!');
  };

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        setDepositImage(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const steps = ['Enter Deposit Details', 'Upload Proof', 'Review & Submit'];

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Box>
        <PageHeader
          title="Record Bank Deposit"
          subtitle="Submit cash deposit details for approval"
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
                    Deposit Details
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
                        error={formik.touched.bankAccount && Boolean(formik.errors.bankAccount)}
                      >
                        <InputLabel id="bank-account-label">Bank Account</InputLabel>
                        <Select
                          labelId="bank-account-label"
                          id="bankAccount"
                          name="bankAccount"
                          label="Bank Account"
                          value={formik.values.bankAccount}
                          onChange={formik.handleChange}
                          onBlur={formik.handleBlur}
                        >
                          <MenuItem value="hdfc">HDFC Bank - XXXX1234</MenuItem>
                          <MenuItem value="sbi">SBI - XXXX5678</MenuItem>
                          <MenuItem value="icici">ICICI Bank - XXXX9012</MenuItem>
                        </Select>
                        {formik.touched.bankAccount && formik.errors.bankAccount && (
                          <FormHelperText>{formik.errors.bankAccount}</FormHelperText>
                        )}
                      </FormControl>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <TextField
                        fullWidth
                        id="referenceNumber"
                        name="referenceNumber"
                        label="Reference Number"
                        variant="outlined"
                        placeholder="Enter deposit slip number or reference"
                        value={formik.values.referenceNumber}
                        onChange={formik.handleChange}
                        onBlur={formik.handleBlur}
                        error={formik.touched.referenceNumber && Boolean(formik.errors.referenceNumber)}
                        helperText={formik.touched.referenceNumber && formik.errors.referenceNumber}
                      />
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <DatePicker
                        label="Deposit Date"
                        value={formik.values.depositDate}
                        onChange={(newValue) => formik.setFieldValue('depositDate', newValue)}
                        slotProps={{ 
                          textField: { 
                            fullWidth: true,
                            error: formik.touched.depositDate && Boolean(formik.errors.depositDate),
                            helperText: formik.touched.depositDate && formik.errors.depositDate ? String(formik.errors.depositDate) : '',
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
                        placeholder="Enter any additional details..."
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
                      !formik.values.bankAccount ||
                      !formik.values.referenceNumber ||
                      !formik.values.depositDate
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
                    Upload Deposit Proof
                  </Typography>
                  <Typography variant="body2" color="textSecondary" paragraph>
                    Please upload a photo or scan of the deposit slip or screenshot of the bank transaction.
                  </Typography>

                  <Box sx={{ mt: 3, mb: 3 }}>
                    <input
                      accept="image/*"
                      style={{ display: 'none' }}
                      id="deposit-image-upload"
                      type="file"
                      onChange={handleImageUpload}
                    />
                    <label htmlFor="deposit-image-upload">
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

                  {depositImage ? (
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
                          src={depositImage} 
                          alt="Deposit proof" 
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
                        Upload a clear image of your deposit slip or transaction screenshot
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
                    Review Deposit Details
                  </Typography>
                  <Typography variant="body2" color="textSecondary" paragraph>
                    Please review the deposit details before submitting for approval.
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
                        Bank Account
                      </Typography>
                      <Typography variant="body1" sx={{ fontWeight: 500 }}>
                        {formik.values.bankAccount === 'hdfc' && 'HDFC Bank - XXXX1234'}
                        {formik.values.bankAccount === 'sbi' && 'SBI - XXXX5678'}
                        {formik.values.bankAccount === 'icici' && 'ICICI Bank - XXXX9012'}
                      </Typography>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Typography variant="subtitle2" color="textSecondary">
                        Reference Number
                      </Typography>
                      <Typography variant="body1" sx={{ fontWeight: 500 }}>
                        {formik.values.referenceNumber}
                      </Typography>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Typography variant="subtitle2" color="textSecondary">
                        Deposit Date
                      </Typography>
                      <Typography variant="body1" sx={{ fontWeight: 500 }}>
                        {formik.values.depositDate.toLocaleDateString()}
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

                  {depositImage && (
                    <Box sx={{ mt: 3 }}>
                      <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                        Deposit Proof
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
                          src={depositImage} 
                          alt="Deposit proof" 
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
          <DialogTitle>Confirm Deposit Submission</DialogTitle>
          <DialogContent>
            <Typography variant="body1" gutterBottom>
              Are you sure you want to submit this deposit for approval?
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Amount: ₹{formik.values.amount}
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Bank: {formik.values.bankAccount === 'hdfc' ? 'HDFC Bank' : formik.values.bankAccount === 'sbi' ? 'SBI' : 'ICICI Bank'}
            </Typography>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setConfirmDialogOpen(false)}>Cancel</Button>
            <Button 
              onClick={handleConfirmDeposit} 
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

export default RecordDeposit;