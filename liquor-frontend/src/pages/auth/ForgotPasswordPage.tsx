import React, { useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Container,
  TextField,
  Typography,
  Alert,
  Paper,
  Grid,
  Link,
  InputAdornment,
  CircularProgress,
} from '@mui/material';
import { EmailOutlined, ArrowBack } from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { Link as RouterLink } from 'react-router-dom';
import useAuth from '../../hooks/useAuth';

// Validation schema
const validationSchema = Yup.object({
  email: Yup.string()
    .email('Enter a valid email')
    .required('Email is required'),
});

const ForgotPasswordPage: React.FC = () => {
  const { forgotPassword } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const formik = useFormik({
    initialValues: {
      email: '',
    },
    validationSchema: validationSchema,
    onSubmit: async (values) => {
      setIsLoading(true);
      setError(null);
      try {
        await forgotPassword(values.email);
        setSuccess(true);
      } catch (err: any) {
        setError(err.message || 'Failed to send password reset email');
      } finally {
        setIsLoading(false);
      }
    },
  });

  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '100vh',
        }}
      >
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <Paper 
            elevation={3}
            sx={{ 
              borderRadius: 2,
              overflow: 'hidden',
              width: '100%',
            }}
          >
            <Box 
              sx={{ 
                bgcolor: 'primary.main', 
                color: 'primary.contrastText',
                p: 3,
                textAlign: 'center',
              }}
            >
              <Typography component="h1" variant="h5">
                Liquor Shop Management
              </Typography>
            </Box>
            <CardContent sx={{ p: 4 }}>
              <Typography component="h2" variant="h5" align="center" gutterBottom>
                Forgot Password
              </Typography>
              <Typography variant="body2" color="text.secondary" align="center" sx={{ mb: 3 }}>
                Enter your email address and we'll send you a link to reset your password
              </Typography>

              {error && (
                <Alert severity="error" sx={{ mb: 3 }}>
                  {error}
                </Alert>
              )}

              {success ? (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.5 }}
                >
                  <Alert severity="success" sx={{ mb: 3 }}>
                    Password reset link has been sent to your email address. Please check your inbox.
                  </Alert>
                  <Box sx={{ textAlign: 'center', mt: 3 }}>
                    <Button
                      component={RouterLink}
                      to="/login"
                      variant="contained"
                      startIcon={<ArrowBack />}
                    >
                      Back to Login
                    </Button>
                  </Box>
                </motion.div>
              ) : (
                <form onSubmit={formik.handleSubmit}>
                  <TextField
                    margin="normal"
                    fullWidth
                    id="email"
                    label="Email Address"
                    name="email"
                    autoComplete="email"
                    autoFocus
                    value={formik.values.email}
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    error={formik.touched.email && Boolean(formik.errors.email)}
                    helperText={formik.touched.email && formik.errors.email}
                    disabled={isLoading}
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <EmailOutlined color="action" />
                        </InputAdornment>
                      ),
                    }}
                  />
                  <Button
                    type="submit"
                    fullWidth
                    variant="contained"
                    sx={{ mt: 3, mb: 2, py: 1.5 }}
                    disabled={isLoading}
                  >
                    {isLoading ? (
                      <>
                        <CircularProgress size={24} sx={{ mr: 1 }} color="inherit" />
                        Sending...
                      </>
                    ) : (
                      'Send Reset Link'
                    )}
                  </Button>
                  <Grid container justifyContent="center">
                    <Grid item>
                      <Link component={RouterLink} to="/login" variant="body2">
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          <ArrowBack fontSize="small" sx={{ mr: 0.5 }} />
                          Back to Login
                        </Box>
                      </Link>
                    </Grid>
                  </Grid>
                </form>
              )}
            </CardContent>
          </Paper>
        </motion.div>
        <Box sx={{ mt: 4, textAlign: 'center' }}>
          <Typography variant="body2" color="text.secondary">
            &copy; {new Date().getFullYear()} Liquor Shop Management System
          </Typography>
        </Box>
      </Box>
    </Container>
  );
};

export default ForgotPasswordPage;