import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Divider,
  Stack,
  IconButton,
} from '@mui/material';
import { ArrowBack } from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

interface FormLayoutProps {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  submitText?: string;
  cancelText?: string;
  onSubmit?: () => void;
  onCancel?: () => void;
  isSubmitting?: boolean;
  showBackButton?: boolean;
  backButtonPath?: string;
  maxWidth?: string | number;
  delay?: number;
}

const FormLayout: React.FC<FormLayoutProps> = ({
  title,
  subtitle,
  children,
  submitText = 'Submit',
  cancelText = 'Cancel',
  onSubmit,
  onCancel,
  isSubmitting = false,
  showBackButton = true,
  backButtonPath,
  maxWidth = 800,
  delay = 0,
}) => {
  const navigate = useNavigate();

  const handleBack = () => {
    if (backButtonPath) {
      navigate(backButtonPath);
    } else {
      navigate(-1);
    }
  };

  const handleCancel = () => {
    if (onCancel) {
      onCancel();
    } else {
      navigate(-1);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay }}
    >
      <Box sx={{ maxWidth, mx: 'auto' }}>
        <Box sx={{ mb: 3, display: 'flex', alignItems: 'center' }}>
          {showBackButton && (
            <IconButton onClick={handleBack} sx={{ mr: 1 }}>
              <ArrowBack />
            </IconButton>
          )}
          <Box>
            <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 700 }}>
              {title}
            </Typography>
            {subtitle && (
              <Typography variant="subtitle1" color="textSecondary">
                {subtitle}
              </Typography>
            )}
          </Box>
        </Box>

        <Card>
          <CardContent sx={{ p: 3 }}>
            {children}
          </CardContent>
          <Divider />
          <Box sx={{ p: 2, display: 'flex', justifyContent: 'flex-end' }}>
            <Stack direction="row" spacing={2}>
              <Button
                variant="outlined"
                onClick={handleCancel}
                disabled={isSubmitting}
              >
                {cancelText}
              </Button>
              {onSubmit && (
                <Button
                  variant="contained"
                  onClick={onSubmit}
                  disabled={isSubmitting}
                >
                  {isSubmitting ? 'Submitting...' : submitText}
                </Button>
              )}
            </Stack>
          </Box>
        </Card>
      </Box>
    </motion.div>
  );
};

export default FormLayout;