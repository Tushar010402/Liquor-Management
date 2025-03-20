import React from 'react';
import { Backdrop, CircularProgress, Typography, Box } from '@mui/material';
import { useAppSelector } from '../../store';

const GlobalLoader: React.FC = () => {
  const { isLoading, loadingText } = useAppSelector((state) => state.loading);

  return (
    <Backdrop
      sx={{
        color: '#fff',
        zIndex: (theme) => theme.zIndex.drawer + 1,
        flexDirection: 'column',
      }}
      open={isLoading}
    >
      <CircularProgress color="inherit" size={60} />
      {loadingText && (
        <Box sx={{ mt: 2 }}>
          <Typography variant="h6" color="inherit">
            {loadingText}
          </Typography>
        </Box>
      )}
    </Backdrop>
  );
};

export default GlobalLoader;