import React, { ReactNode } from 'react';
import { Box, Typography, Breadcrumbs, Link } from '@mui/material';
import { useLocation } from 'react-router-dom';

interface PageContainerProps {
  title: string;
  children: ReactNode;
  breadcrumbs?: { label: string; path?: string }[];
}

export const PageContainer: React.FC<PageContainerProps> = ({ 
  title, 
  children, 
  breadcrumbs 
}) => {
  const location = useLocation();
  
  // Generate breadcrumbs based on route if not provided
  const routeBreadcrumbs = breadcrumbs || generateBreadcrumbs(location.pathname);

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          {title}
        </Typography>
        
        {routeBreadcrumbs.length > 0 && (
          <Breadcrumbs aria-label="breadcrumb">
            {routeBreadcrumbs.map((crumb, index) => {
              const isLast = index === routeBreadcrumbs.length - 1;
              
              return isLast ? (
                <Typography key={index} color="text.primary">
                  {crumb.label}
                </Typography>
              ) : (
                <Link 
                  key={index} 
                  color="inherit" 
                  href={crumb.path} 
                  underline="hover"
                >
                  {crumb.label}
                </Link>
              );
            })}
          </Breadcrumbs>
        )}
      </Box>
      
      {children}
    </Box>
  );
};

// Helper function to generate breadcrumbs from a path
const generateBreadcrumbs = (path: string) => {
  const segments = path.split('/').filter(Boolean);
  
  if (segments.length === 0) {
    return [];
  }
  
  return [
    { label: 'Home', path: '/' },
    ...segments.map((segment, index) => {
      const formattedLabel = segment
        .split('-')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
      
      return {
        label: formattedLabel,
        path: index < segments.length - 1 ? `/${segments.slice(0, index + 1).join('/')}` : undefined
      };
    })
  ];
}; 