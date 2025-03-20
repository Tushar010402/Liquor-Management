import React, { useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Container,
  TextField,
  Typography,
  InputAdornment,
  IconButton,
  Alert,
  Paper,
  Grid,
  Divider,
  useTheme,
  useMediaQuery,
} from '@mui/material';
import { Visibility, VisibilityOff, LockOutlined, EmailOutlined } from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import useAuth from '../../hooks/useAuth';

// Validation schema
const validationSchema = Yup.object({
  email: Yup.string()
    .email('Enter a valid email')
    .required('Email is required'),
  password: Yup.string()
    .min(8, 'Password should be of minimum 8 characters length')
    .required('Password is required'),
});

const LoginPage: React.FC = () => {
  const { login, error, isLoading } = useAuth();
  const [showPassword, setShowPassword] = useState(false);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  const formik = useFormik({
    initialValues: {
      email: '',
      password: '',
    },
    validationSchema: validationSchema,
    onSubmit: async (values) => {
      await login(values.email, values.password);
    },
  });

  const handleClickShowPassword = () => {
    setShowPassword(!showPassword);
  };

  return (
    <Container component="main" maxWidth="lg" sx={{ height: '100vh' }}>
      <Grid
        container
        spacing={0}
        sx={{
          height: '100%',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
        {!isMobile && (
          <Grid item xs={12} md={6}>
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5 }}
            >
              <Box
                sx={{
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center',
                  p: 4,
                  height: '100%',
                }}
              >
                <Typography
                  variant="h3"
                  component="h1"
                  gutterBottom
                  color="primary"
                  sx={{ fontWeight: 700, mb: 2 }}
                >
                  Liquor Shop Management System
                </Typography>
                <Typography variant="h6" color="textSecondary" sx={{ mb: 4, textAlign: 'center' }}>
                  Streamline your operations, maximize profits, and make data-driven decisions
                </Typography>
                <Paper
                  elevation={0}
                  sx={{
                    p: 3,
                    backgroundColor: theme.palette.primary.main,
                    color: 'white',
                    borderRadius: 2,
                    width: '100%',
                    maxWidth: 450,
                  }}
                >
                  <Typography variant="h6" gutterBottom>
                    Key Features:
                  </Typography>
                  <Typography variant="body2" paragraph>
                    • Comprehensive inventory management
                  </Typography>
                  <Typography variant="body2" paragraph>
                    • Real-time sales tracking and analytics
                  </Typography>
                  <Typography variant="body2" paragraph>
                    • Multi-store management capabilities
                  </Typography>
                  <Typography variant="body2" paragraph>
                    • Robust financial reporting
                  </Typography>
                  <Typography variant="body2">
                    • Role-based access control
                  </Typography>
                </Paper>
              </Box>
            </motion.div>
          </Grid>
        )}

        <Grid item xs={12} md={6}>
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <Box
              sx={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                p: 4,
              }}
            >
              <Card
                elevation={6}
                sx={{
                  width: '100%',
                  maxWidth: 450,
                  borderRadius: 3,
                  overflow: 'hidden',
                }}
              >
                <CardContent sx={{ p: 4 }}>
                  <Box
                    sx={{
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'center',
                      mb: 3,
                    }}
                  >
                    <Typography
                      component="h1"
                      variant="h4"
                      gutterBottom
                      sx={{ fontWeight: 600 }}
                    >
                      Sign In
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Enter your credentials to access your account
                    </Typography>
                  </Box>

                  {error && (
                    <Alert severity="error" sx={{ mb: 3 }}>
                      {error}
                    </Alert>
                  )}

                  <form onSubmit={formik.handleSubmit}>
                    <TextField
                      margin="normal"
                      fullWidth
                      id="email"
                      name="email"
                      label="Email Address"
                      value={formik.values.email}
                      onChange={formik.handleChange}
                      onBlur={formik.handleBlur}
                      error={formik.touched.email && Boolean(formik.errors.email)}
                      helperText={formik.touched.email && formik.errors.email}
                      InputProps={{
                        startAdornment: (
                          <InputAdornment position="start">
                            <EmailOutlined color="action" />
                          </InputAdornment>
                        ),
                      }}
                      sx={{ mb: 2 }}
                    />

                    <TextField
                      margin="normal"
                      fullWidth
                      id="password"
                      name="password"
                      label="Password"
                      type={showPassword ? 'text' : 'password'}
                      value={formik.values.password}
                      onChange={formik.handleChange}
                      onBlur={formik.handleBlur}
                      error={formik.touched.password && Boolean(formik.errors.password)}
                      helperText={formik.touched.password && formik.errors.password}
                      InputProps={{
                        startAdornment: (
                          <InputAdornment position="start">
                            <LockOutlined color="action" />
                          </InputAdornment>
                        ),
                        endAdornment: (
                          <InputAdornment position="end">
                            <IconButton
                              aria-label="toggle password visibility"
                              onClick={handleClickShowPassword}
                              edge="end"
                            >
                              {showPassword ? <VisibilityOff /> : <Visibility />}
                            </IconButton>
                          </InputAdornment>
                        ),
                      }}
                      sx={{ mb: 3 }}
                    />

                    <Button
                      type="submit"
                      fullWidth
                      variant="contained"
                      color="primary"
                      size="large"
                      disabled={isLoading}
                      sx={{
                        py: 1.5,
                        mt: 1,
                        mb: 3,
                        fontWeight: 600,
                      }}
                    >
                      {isLoading ? 'Signing in...' : 'Sign In'}
                    </Button>

                    <Divider sx={{ my: 2 }}>
                      <Typography variant="body2" color="textSecondary">
                        Demo Accounts
                      </Typography>
                    </Divider>

                    <Box sx={{ mt: 2 }}>
                      <Typography variant="body2" color="textSecondary" gutterBottom>
                        Use these emails with any password to test different roles:
                      </Typography>
                      <Typography variant="body2" color="primary">
                        saas@example.com (SaaS Admin)
                      </Typography>
                      <Typography variant="body2" color="primary">
                        tenant@example.com (Tenant Admin)
                      </Typography>
                      <Typography variant="body2" color="primary">
                        manager@example.com (Manager)
                      </Typography>
                      <Typography variant="body2" color="primary">
                        assistant@example.com (Assistant Manager)
                      </Typography>
                      <Typography variant="body2" color="primary">
                        executive@example.com (Executive)
                      </Typography>
                    </Box>
                  </form>
                </CardContent>
              </Card>
            </Box>
          </motion.div>
        </Grid>
      </Grid>
    </Container>
  );
};

export default LoginPage;