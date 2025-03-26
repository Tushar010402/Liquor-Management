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
  Paper,
  Stepper,
  Step,
  StepLabel,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { useNavigate } from 'react-router-dom';
import { PageHeader } from '../../../components/common';

const validationSchema = Yup.object({
  amount: Yup.number()
    .required('Amount is required')
    .positive('Amount must be positive')
    .typeError('Please enter a valid number'),
  fromAccount: Yup.string().required('Source account is required'),
  toAccount: Yup.string().required('Destination account is required'),
  reference: Yup.string().required('Reference number is required'),
  transferDate: Yup.date().required('Transfer date is required'),
  notes: Yup.string(),
});

const steps = ['Transfer Details', 'Review', 'Complete'];

const RecordTransfer = () => {
  const navigate = useNavigate();
  const [activeStep, setActiveStep] = useState(0);
  const [confirmDialogOpen, setConfirmDialogOpen] = useState(false);

  const formik = useFormik({
    initialValues: {
      amount: '',
      fromAccount: '',
      toAccount: '',
      reference: '',
      transferDate: new Date(),
      notes: '',
    },
    validationSchema,
    onSubmit: (values) => {
      if (activeStep === steps.length - 2) {
        setConfirmDialogOpen(true);
      } else {
        handleNext();
      }
    },
  });

  const handleNext = () => {
    if (activeStep === 0 && !formik.isValid) {
      formik.validateForm();
      return;
    }
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleReset = () => {
    setActiveStep(0);
    formik.resetForm();
  };

  const handleCloseConfirmDialog = () => {
    setConfirmDialogOpen(false);
  };

  const handleConfirmSubmit = () => {
    // Submit logic here
    setConfirmDialogOpen(false);
    setActiveStep(steps.length - 1);
    // In a real app, you'd make an API call here
    setTimeout(() => {
      alert('Transfer recorded successfully!');
      navigate('/executive/cash-balance');
    }, 1500);
  };

  const availableAccounts = [
    { id: 'hdfc', name: 'HDFC Bank - XXXX1234', type: 'bank' },
    { id: 'sbi', name: 'SBI - XXXX5678', type: 'bank' },
    { id: 'icici', name: 'ICICI Bank - XXXX9012', type: 'bank' },
    { id: 'cash', name: 'Cash Register', type: 'cash' },
    { id: 'petty', name: 'Petty Cash', type: 'cash' },
  ];

  const renderStepContent = (step: number) => {
    switch (step) {
      case 0:
        return (
          <form onSubmit={formik.handleSubmit}>
            <Card>
              <CardContent>
                <Grid container spacing={3}>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      id="amount"
                      name="amount"
                      label="Amount"
                      variant="outlined"
                      type="number"
                      value={formik.values.amount}
                      onChange={formik.handleChange}
                      onBlur={formik.handleBlur}
                      error={formik.touched.amount && Boolean(formik.errors.amount)}
                      helperText={formik.touched.amount && formik.errors.amount}
                      InputProps={{
                        startAdornment: <InputAdornment position="start">₹</InputAdornment>,
                      }}
                    />
                  </Grid>
                  
                  <Grid item xs={12} md={6}>
                    <FormControl 
                      fullWidth 
                      error={formik.touched.fromAccount && Boolean(formik.errors.fromAccount)}
                    >
                      <InputLabel id="fromAccount-label">From Account</InputLabel>
                      <Select
                        labelId="fromAccount-label"
                        id="fromAccount"
                        name="fromAccount"
                        label="From Account"
                        value={formik.values.fromAccount}
                        onChange={formik.handleChange}
                        onBlur={formik.handleBlur}
                      >
                        {availableAccounts.map((account) => (
                          <MenuItem 
                            key={account.id} 
                            value={account.id}
                            disabled={account.id === formik.values.toAccount}
                          >
                            {account.name}
                          </MenuItem>
                        ))}
                      </Select>
                      {formik.touched.fromAccount && formik.errors.fromAccount && (
                        <FormHelperText>{formik.errors.fromAccount}</FormHelperText>
                      )}
                    </FormControl>
                  </Grid>
                  
                  <Grid item xs={12} md={6}>
                    <FormControl 
                      fullWidth 
                      error={formik.touched.toAccount && Boolean(formik.errors.toAccount)}
                    >
                      <InputLabel id="toAccount-label">To Account</InputLabel>
                      <Select
                        labelId="toAccount-label"
                        id="toAccount"
                        name="toAccount"
                        label="To Account"
                        value={formik.values.toAccount}
                        onChange={formik.handleChange}
                        onBlur={formik.handleBlur}
                      >
                        {availableAccounts.map((account) => (
                          <MenuItem 
                            key={account.id} 
                            value={account.id}
                            disabled={account.id === formik.values.fromAccount}
                          >
                            {account.name}
                          </MenuItem>
                        ))}
                      </Select>
                      {formik.touched.toAccount && formik.errors.toAccount && (
                        <FormHelperText>{formik.errors.toAccount}</FormHelperText>
                      )}
                    </FormControl>
                  </Grid>
                  
                  <Grid item xs={12} md={6}>
                    <TextField
                      fullWidth
                      id="reference"
                      name="reference"
                      label="Reference Number"
                      variant="outlined"
                      placeholder="Enter transaction reference"
                      value={formik.values.reference}
                      onChange={formik.handleChange}
                      onBlur={formik.handleBlur}
                      error={formik.touched.reference && Boolean(formik.errors.reference)}
                      helperText={formik.touched.reference && formik.errors.reference}
                    />
                  </Grid>
                  
                  <Grid item xs={12} md={6}>
                    <LocalizationProvider dateAdapter={AdapterDateFns}>
                      <DatePicker
                        label="Transfer Date"
                        value={formik.values.transferDate}
                        onChange={(newValue) => {
                          formik.setFieldValue('transferDate', newValue);
                        }}
                        slotProps={{ 
                          textField: { 
                            fullWidth: true,
                            error: formik.touched.transferDate && Boolean(formik.errors.transferDate),
                            helperText: formik.touched.transferDate && formik.errors.transferDate ? String(formik.errors.transferDate) : '',
                          } 
                        }}
                      />
                    </LocalizationProvider>
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
                      value={formik.values.notes}
                      onChange={formik.handleChange}
                      onBlur={formik.handleBlur}
                      error={formik.touched.notes && Boolean(formik.errors.notes)}
                      helperText={formik.touched.notes && formik.errors.notes}
                    />
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </form>
        );
      
      case 1:
        // Review step
        const fromAccount = availableAccounts.find(a => a.id === formik.values.fromAccount);
        const toAccount = availableAccounts.find(a => a.id === formik.values.toAccount);
        
        return (
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Review Transfer Details
              </Typography>
              <Box sx={{ mt: 2 }}>
                <Grid container spacing={2}>
                  <Grid item xs={12}>
                    <Paper sx={{ p: 2, bgcolor: 'background.default' }}>
                      <Grid container spacing={2}>
                        <Grid item xs={6}>
                          <Typography variant="subtitle2">Amount:</Typography>
                        </Grid>
                        <Grid item xs={6}>
                          <Typography variant="body1" fontWeight="medium">
                            ₹{parseFloat(formik.values.amount as string).toLocaleString('en-IN')}
                          </Typography>
                        </Grid>
                        
                        <Grid item xs={12}>
                          <Divider sx={{ my: 1 }} />
                        </Grid>
                        
                        <Grid item xs={6}>
                          <Typography variant="subtitle2">From Account:</Typography>
                        </Grid>
                        <Grid item xs={6}>
                          <Typography variant="body1">{fromAccount?.name}</Typography>
                        </Grid>
                        
                        <Grid item xs={6}>
                          <Typography variant="subtitle2">To Account:</Typography>
                        </Grid>
                        <Grid item xs={6}>
                          <Typography variant="body1">{toAccount?.name}</Typography>
                        </Grid>
                        
                        <Grid item xs={12}>
                          <Divider sx={{ my: 1 }} />
                        </Grid>
                        
                        <Grid item xs={6}>
                          <Typography variant="subtitle2">Reference Number:</Typography>
                        </Grid>
                        <Grid item xs={6}>
                          <Typography variant="body1">{formik.values.reference}</Typography>
                        </Grid>
                        
                        <Grid item xs={6}>
                          <Typography variant="subtitle2">Transfer Date:</Typography>
                        </Grid>
                        <Grid item xs={6}>
                          <Typography variant="body1">
                            {formik.values.transferDate instanceof Date
                              ? formik.values.transferDate.toLocaleDateString('en-IN', {
                                  day: '2-digit',
                                  month: 'short',
                                  year: 'numeric',
                                })
                              : 'Invalid date'}
                          </Typography>
                        </Grid>
                        
                        {formik.values.notes && (
                          <>
                            <Grid item xs={12}>
                              <Divider sx={{ my: 1 }} />
                            </Grid>
                            <Grid item xs={6}>
                              <Typography variant="subtitle2">Notes:</Typography>
                            </Grid>
                            <Grid item xs={6}>
                              <Typography variant="body1">{formik.values.notes}</Typography>
                            </Grid>
                          </>
                        )}
                      </Grid>
                    </Paper>
                  </Grid>
                </Grid>
              </Box>
            </CardContent>
          </Card>
        );
      
      case 2:
        // Complete step
        return (
          <Card>
            <CardContent>
              <Box sx={{ textAlign: 'center', py: 3 }}>
                <Typography variant="h6" color="success.main" gutterBottom>
                  Transfer Recorded Successfully!
                </Typography>
                <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
                  The transfer has been recorded and is awaiting approval.
                </Typography>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={() => navigate('/executive/cash-balance')}
                  sx={{ mt: 2 }}
                >
                  View Cash Balance
                </Button>
              </Box>
            </CardContent>
          </Card>
        );
      
      default:
        return <div>Unknown step</div>;
    }
  };

  return (
    <Box sx={{ padding: 3 }}>
      <PageHeader title="Record Fund Transfer" />
      
      <Box sx={{ my: 4 }}>
        <Stepper activeStep={activeStep} alternativeLabel>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>
      </Box>
      
      <Box sx={{ mt: 4 }}>
        {renderStepContent(activeStep)}
      </Box>
      
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 3 }}>
        <Button
          color="inherit"
          disabled={activeStep === 0 || activeStep === steps.length - 1}
          onClick={handleBack}
          variant="outlined"
        >
          Back
        </Button>
        <Box>
          {activeStep !== steps.length - 1 && (
            <Button
              variant="contained"
              color="primary"
              onClick={activeStep === steps.length - 2 ? formik.submitForm : handleNext}
            >
              {activeStep === steps.length - 2 ? 'Submit for Approval' : 'Next'}
            </Button>
          )}
        </Box>
      </Box>
      
      <Dialog open={confirmDialogOpen} onClose={handleCloseConfirmDialog}>
        <DialogTitle>Confirm Transfer Submission</DialogTitle>
        <DialogContent>
          <Typography variant="body1">
            Are you sure you want to submit this transfer for approval?
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            Amount: ₹{parseFloat(formik.values.amount as string).toLocaleString('en-IN')}
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseConfirmDialog} color="inherit">
            Cancel
          </Button>
          <Button onClick={handleConfirmSubmit} color="primary" variant="contained">
            Confirm
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default RecordTransfer;
 