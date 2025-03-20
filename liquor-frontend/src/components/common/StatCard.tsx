import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Avatar,
  SvgIconProps,
} from '@mui/material';
import { motion } from 'framer-motion';

interface StatCardProps {
  title: string;
  value: string | number;
  icon: React.ReactElement<SvgIconProps>;
  trend?: {
    value: string;
    isPositive: boolean;
    text: string;
  };
  color?: 'primary' | 'secondary' | 'success' | 'error' | 'warning' | 'info';
  delay?: number;
}

const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  icon,
  trend,
  color = 'primary',
  delay = 0,
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay }}
    >
      <Card sx={{ height: '100%' }}>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
            <Typography variant="subtitle2" color="textSecondary">
              {title}
            </Typography>
            <Avatar sx={{ bgcolor: `${color}.light` }}>
              {icon}
            </Avatar>
          </Box>
          <Typography variant="h4" component="div" sx={{ fontWeight: 700 }}>
            {value}
          </Typography>
          {trend && (
            <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
              {trend.isPositive ? (
                <motion.div
                  initial={{ rotate: -45 }}
                  animate={{ rotate: 0 }}
                  transition={{ duration: 0.5, delay: delay + 0.3 }}
                >
                  <Box
                    component="span"
                    sx={{
                      color: 'success.main',
                      display: 'flex',
                      alignItems: 'center',
                    }}
                  >
                    ↑
                  </Box>
                </motion.div>
              ) : (
                <motion.div
                  initial={{ rotate: 45 }}
                  animate={{ rotate: 0 }}
                  transition={{ duration: 0.5, delay: delay + 0.3 }}
                >
                  <Box
                    component="span"
                    sx={{
                      color: 'error.main',
                      display: 'flex',
                      alignItems: 'center',
                    }}
                  >
                    ↓
                  </Box>
                </motion.div>
              )}
              <Typography
                variant="body2"
                color={trend.isPositive ? 'success.main' : 'error.main'}
                sx={{ ml: 0.5 }}
              >
                {trend.value}
              </Typography>
              <Typography variant="body2" color="textSecondary" sx={{ ml: 1 }}>
                {trend.text}
              </Typography>
            </Box>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default StatCard;