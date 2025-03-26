import React from 'react';
import { Box, Card, CardContent, Typography, Avatar, Grid, TextField, Button, Divider } from '@mui/material';
import { PageContainer } from '../../components/common/PageContainer';
import useAuth from '../../hooks/useAuth';

const Profile: React.FC = () => {
  const { user } = useAuth();

  return (
    <PageContainer title="My Profile">
      <Box sx={{ p: 2 }}>
        <Card>
          <CardContent>
            <Grid container spacing={4}>
              <Grid item xs={12} md={4} display="flex" flexDirection="column" alignItems="center">
                <Avatar 
                  sx={{ 
                    width: 120, 
                    height: 120, 
                    mb: 2,
                    bgcolor: 'primary.main'
                  }}
                >
                  {user?.full_name?.charAt(0) || ''}
                </Avatar>
                <Typography variant="h5" fontWeight="bold" gutterBottom>
                  {user?.full_name || 'User'}
                </Typography>
                <Typography variant="body1" color="text.secondary">
                  {user?.role?.replace('_', ' ').toUpperCase() || 'Role'}
                </Typography>
                <Button 
                  variant="outlined" 
                  sx={{ mt: 2 }}
                >
                  Change Avatar
                </Button>
              </Grid>
              
              <Grid item xs={12} md={8}>
                <Typography variant="h5" gutterBottom>
                  Personal Information
                </Typography>
                <Divider sx={{ mb: 3 }} />
                
                <Grid container spacing={3}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Full Name"
                      defaultValue={user?.full_name || ''}
                      InputProps={{
                        readOnly: true,
                      }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Email"
                      defaultValue={user?.email || ''}
                      InputProps={{
                        readOnly: true,
                      }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Role"
                      defaultValue={user?.role?.replace('_', ' ').toUpperCase() || ''}
                      InputProps={{
                        readOnly: true,
                      }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Tenant ID"
                      defaultValue={user?.tenant_id || 'N/A'}
                      InputProps={{
                        readOnly: true,
                      }}
                    />
                  </Grid>
                  
                  <Grid item xs={12}>
                    <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 2 }}>
                      <Button 
                        variant="contained" 
                        color="primary"
                        sx={{ mr: 1 }}
                      >
                        Request Information Update
                      </Button>
                      <Button 
                        variant="outlined"
                      >
                        Change Password
                      </Button>
                    </Box>
                  </Grid>
                </Grid>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      </Box>
    </PageContainer>
  );
};

export default Profile; 