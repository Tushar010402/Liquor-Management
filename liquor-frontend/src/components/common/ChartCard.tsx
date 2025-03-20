import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  IconButton,
  Divider,
} from '@mui/material';
import { MoreVert } from '@mui/icons-material';
import { motion } from 'framer-motion';

interface ChartCardProps {
  title: string;
  children: React.ReactNode;
  action?: 'button' | 'icon' | 'none';
  actionText?: string;
  onActionClick?: () => void;
  height?: number | string;
  delay?: number;
}

const ChartCard: React.FC<ChartCardProps> = ({
  title,
  children,
  action = 'button',
  actionText = 'View Details',
  onActionClick,
  height = 300,
  delay = 0,
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay }}
    >
      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
            <Typography variant="h6" component="h2">
              {title}
            </Typography>
            {action === 'button' && (
              <Button variant="outlined" size="small" onClick={onActionClick}>
                {actionText}
              </Button>
            )}
            {action === 'icon' && (
              <IconButton size="small" onClick={onActionClick}>
                <MoreVert fontSize="small" />
              </IconButton>
            )}
          </Box>
          <Box sx={{ height }}>
            {children}
          </Box>
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default ChartCard;