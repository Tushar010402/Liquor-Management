import React from 'react';
import {
  Box,
  Typography,
  Button,
  Breadcrumbs,
  Link,
  SvgIconProps,
} from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import { motion } from 'framer-motion';

interface BreadcrumbItem {
  label: string;
  path?: string;
}

interface PageHeaderProps {
  title: string;
  subtitle?: string;
  breadcrumbs?: BreadcrumbItem[];
  actionText?: string;
  actionIcon?: React.ReactElement<SvgIconProps>;
  onActionClick?: () => void;
}

const PageHeader: React.FC<PageHeaderProps> = ({
  title,
  subtitle,
  breadcrumbs,
  actionText,
  actionIcon,
  onActionClick,
}) => {
  return (
    <Box sx={{ mb: 4 }}>
      {breadcrumbs && breadcrumbs.length > 0 && (
        <Breadcrumbs sx={{ mb: 2 }}>
          {breadcrumbs.map((item, index) => {
            const isLast = index === breadcrumbs.length - 1;
            
            return isLast ? (
              <Typography key={item.label} color="text.primary">
                {item.label}
              </Typography>
            ) : (
              <Link
                key={item.label}
                component={RouterLink}
                to={item.path || '#'}
                underline="hover"
                color="inherit"
              >
                {item.label}
              </Link>
            );
          })}
        </Breadcrumbs>
      )}
      
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.3 }}
        >
          <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 700 }}>
            {title}
          </Typography>
          {subtitle && (
            <Typography variant="subtitle1" color="textSecondary">
              {subtitle}
            </Typography>
          )}
        </motion.div>
        
        {actionText && onActionClick && (
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3, delay: 0.1 }}
          >
            <Button
              variant="contained"
              color="primary"
              onClick={onActionClick}
              startIcon={actionIcon}
            >
              {actionText}
            </Button>
          </motion.div>
        )}
      </Box>
    </Box>
  );
};

export default PageHeader;