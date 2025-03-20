import React from 'react';
import {
  Box,
  Typography,
  Button,
  Paper,
  SvgIconProps,
} from '@mui/material';
import { motion } from 'framer-motion';

interface EmptyStateProps {
  title: string;
  description?: string;
  icon?: React.ReactElement<SvgIconProps>;
  actionText?: string;
  onActionClick?: () => void;
  height?: number | string;
}

const EmptyState: React.FC<EmptyStateProps> = ({
  title,
  description,
  icon,
  actionText,
  onActionClick,
  height = 400,
}) => {
  return (
    <Paper
      elevation={0}
      sx={{
        height,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        p: 4,
        borderRadius: 2,
        border: '1px dashed',
        borderColor: 'divider',
      }}
    >
      <motion.div
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.3 }}
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          textAlign: 'center',
        }}
      >
        {icon && (
          <Box
            sx={{
              mb: 2,
              color: 'text.secondary',
              '& svg': {
                fontSize: 60,
              },
            }}
          >
            {icon}
          </Box>
        )}
        
        <Typography variant="h6" gutterBottom>
          {title}
        </Typography>
        
        {description && (
          <Typography variant="body2" color="textSecondary" sx={{ mb: 3, maxWidth: 400 }}>
            {description}
          </Typography>
        )}
        
        {actionText && onActionClick && (
          <Button
            variant="contained"
            color="primary"
            onClick={onActionClick}
          >
            {actionText}
          </Button>
        )}
      </motion.div>
    </Paper>
  );
};

export default EmptyState;