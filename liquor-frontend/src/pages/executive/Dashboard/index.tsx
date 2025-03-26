import React, { useState } from 'react';
import {
  Box,
  Grid,
  Typography,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  Chip,
  Button,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
  useTheme,
  LinearProgress,
  Paper,
  SelectChangeEvent,
} from '@mui/material';
import {
  Store,
  Inventory,
  Receipt,
  AssignmentReturn,
  MonetizationOn,
  Add,
  TrendingUp,
  ShoppingCart,
  LocalAtm,
  AccountBalance,
  CreditCard,
  Summarize,
  Approval,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from 'recharts';
import { useNavigate } from 'react-router-dom';
import { StatCard, ChartCard, ActivityList, PageHeader } from '../../../components/common';
import useAuth from '../../../hooks/useAuth';

// Mock data for charts
const salesByHourData = [
  { hour: '10 AM', sales: 2500 },
  { hour: '11 AM', sales: 3800 },
  { hour: '12 PM', sales: 5200 },
  { hour: '1 PM', sales: 4500 },
  { hour: '2 PM', sales: 3900 },
  { hour: '3 PM', sales: 4200 },
  { hour: '4 PM', sales: 5800 },
  { hour: '5 PM', sales: 6500 },
  { hour: '6 PM', sales: 7200 },
  { hour: '7 PM', sales: 8500 },
  { hour: '8 PM', sales: 9200 },
  { hour: '9 PM', sales: 7800 },
];

const paymentMethodsData = [
  { name: 'Cash', value: 45 },
  { name: 'UPI', value: 35 },
  { name: 'Card', value: 15 },
  { name: 'Other', value: 5 },
];

const COLORS = ['#4CAF50', '#2196F3', '#FF9800', '#9C27B0'];

const topSellingBrandsData = [
  { name: 'Johnnie Walker', sales: 12500 },
  { name: 'Jack Daniels', sales: 9800 },
  { name: 'Absolut', sales: 8500 },
  { name: 'Bacardi', sales: 7200 },
  { name: 'Smirnoff', sales: 6500 },
];

const recentSalesData = [
  { id: 1, invoice: 'INV-2023-1234', amount: '₹3,500', items: 5, time: '10 minutes ago', paymentMethod: 'Cash' },
  { id: 2, invoice: 'INV-2023-1235', amount: '₹2,800', items: 3, time: '25 minutes ago', paymentMethod: 'UPI' },
  { id: 3, invoice: 'INV-2023-1236', amount: '₹5,200', items: 7, time: '45 minutes ago', paymentMethod: 'Card' },
  { id: 4, invoice: 'INV-2023-1237', amount: '₹1,800', items: 2, time: '1 hour ago', paymentMethod: 'Cash' },
];

const pendingApprovalsData = [
  { id: 1, type: 'Sale', number: 'S-2023-1234', amount: '₹12,500', status: 'Pending', time: '2 hours ago' },
  { id: 2, type: 'Stock Adjustment', number: 'ADJ-2023-567', items: '15 items', status: 'Pending', time: '3 hours ago' },
  { id: 3, type: 'Return', number: 'R-2023-089', amount: '₹5,200', status: 'Rejected', time: '1 day ago', reason: 'Missing documentation' },
];

const ExecutiveDashboard: React.FC = () => {
  const theme = useTheme();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [selectedShop, setSelectedShop] = useState(user?.assigned_shops?.[0]?.id || '');

  const handleShopChange = (event: SelectChangeEvent) => {
    setSelectedShop(event.target.value);
  };

  // Calculate daily target progress
  const dailyTarget = 50000;
  const currentSales = 28500;
  const targetProgress = (currentSales / dailyTarget) * 100;

  return (
    <Box>
      <PageHeader
        title="Executive Dashboard"
        subtitle="Welcome back! Here's what's happening in your shop today."
      />

      {/* Shop Selector */}
      {user?.assigned_shops && user.assigned_shops.length > 0 && (
        <Card sx={{ mb: 3 }}>
          <CardContent sx={{ p: 2 }}>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={12} sm={6} md={3}>
                <FormControl fullWidth size="small">
                  <InputLabel id="shop-select-label">Active Shop</InputLabel>
                  <Select
                    labelId="shop-select-label"
                    id="shop-select"
                    value={selectedShop}
                    label="Active Shop"
                    onChange={handleShopChange}
                  >
                    {user.assigned_shops.map((shop) => (
                      <MenuItem key={shop.id} value={shop.id}>
                        {shop.name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6} md={9}>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <Typography variant="body2" color="textSecondary" sx={{ mr: 2 }}>
                    Daily Target: ₹{dailyTarget.toLocaleString()}
                  </Typography>
                  <Box sx={{ flexGrow: 1, mr: 1 }}>
                    <LinearProgress 
                      variant="determinate" 
                      value={targetProgress} 
                      color={targetProgress < 50 ? "error" : targetProgress < 80 ? "warning" : "success"}
                      sx={{ height: 8, borderRadius: 4 }}
                    />
                  </Box>
                  <Typography variant="body2" color="textSecondary">
                    {targetProgress.toFixed(0)}%
                  </Typography>
                </Box>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      )}

      {/* Key Metrics */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Today's Sales"
            value="₹28,500"
            icon={<Receipt />}
            trend={{ value: "12% increase", isPositive: true, text: "vs yesterday" }}
            color="primary"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Cash Balance"
            value="₹15,200"
            icon={<MonetizationOn />}
            trend={{ value: "₹3,500", isPositive: true, text: "deposits pending" }}
            color="success"
            delay={0.1}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Items Sold"
            value="42"
            icon={<ShoppingCart />}
            trend={{ value: "8 more", isPositive: true, text: "vs yesterday" }}
            color="secondary"
            delay={0.2}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Pending Approvals"
            value="3"
            icon={<Approval />}
            trend={{ value: "1 rejected", isPositive: false, text: "needs attention" }}
            color="warning"
            delay={0.3}
          />
        </Grid>
      </Grid>

      {/* Quick Actions */}
      <Grid container spacing={2} sx={{ mb: 4 }}>
        <Grid item xs={6} sm={3}>
          <Paper
            elevation={0}
            sx={{
              p: 2,
              textAlign: 'center',
              borderRadius: 2,
              bgcolor: 'background.default',
              border: '1px solid',
              borderColor: 'divider',
              height: '100%',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer',
              transition: 'all 0.2s',
              '&:hover': {
                bgcolor: 'primary.light',
                color: 'white',
                transform: 'translateY(-4px)',
                boxShadow: 3,
              },
            }}
            onClick={() => navigate('/executive/new-sale')}
          >
            <Receipt sx={{ fontSize: 40, mb: 1 }} />
            <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
              New Sale
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Paper
            elevation={0}
            sx={{
              p: 2,
              textAlign: 'center',
              borderRadius: 2,
              bgcolor: 'background.default',
              border: '1px solid',
              borderColor: 'divider',
              height: '100%',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer',
              transition: 'all 0.2s',
              '&:hover': {
                bgcolor: 'secondary.light',
                color: 'white',
                transform: 'translateY(-4px)',
                boxShadow: 3,
              },
            }}
            onClick={() => navigate('/executive/single-adjustment')}
          >
            <Inventory sx={{ fontSize: 40, mb: 1 }} />
            <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
              Stock Adjustment
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Paper
            elevation={0}
            sx={{
              p: 2,
              textAlign: 'center',
              borderRadius: 2,
              bgcolor: 'background.default',
              border: '1px solid',
              borderColor: 'divider',
              height: '100%',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer',
              transition: 'all 0.2s',
              '&:hover': {
                bgcolor: 'success.light',
                color: 'white',
                transform: 'translateY(-4px)',
                boxShadow: 3,
              },
            }}
            onClick={() => navigate('/executive/record-deposit')}
          >
            <AccountBalance sx={{ fontSize: 40, mb: 1 }} />
            <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
              Record Deposit
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Paper
            elevation={0}
            sx={{
              p: 2,
              textAlign: 'center',
              borderRadius: 2,
              bgcolor: 'background.default',
              border: '1px solid',
              borderColor: 'divider',
              height: '100%',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer',
              transition: 'all 0.2s',
              '&:hover': {
                bgcolor: 'warning.light',
                color: 'white',
                transform: 'translateY(-4px)',
                boxShadow: 3,
              },
            }}
            onClick={() => navigate('/executive/today-summary')}
          >
            <Summarize sx={{ fontSize: 40, mb: 1 }} />
            <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
              Daily Summary
            </Typography>
          </Paper>
        </Grid>
      </Grid>

      {/* Charts */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={8}>
          <ChartCard
            title="Sales by Hour"
            action="button"
            actionText="View Details"
            onActionClick={() => navigate('/executive/my-sales')}
            delay={0.4}
          >
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={salesByHourData}
                margin={{
                  top: 5,
                  right: 30,
                  left: 20,
                  bottom: 5,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="hour" />
                <YAxis />
                <Tooltip 
                  formatter={(value) => [`₹${value}`, 'Sales']}
                  labelFormatter={(label) => `Time: ${label}`}
                />
                <Bar dataKey="sales" fill={theme.palette.primary.main} />
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>
        </Grid>

        <Grid item xs={12} md={4}>
          <ChartCard
            title="Payment Methods"
            action="button"
            actionText="View Details"
            onActionClick={() => navigate('/executive/payment-breakdown')}
            delay={0.5}
          >
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={paymentMethodsData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                >
                  {paymentMethodsData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </ChartCard>
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6" component="h2">
                  Recent Sales
                </Typography>
                <Button 
                  variant="text" 
                  size="small" 
                  color="primary"
                  onClick={() => navigate('/executive/my-sales')}
                >
                  View All
                </Button>
              </Box>
              <List>
                {recentSalesData.map((item, index) => (
                  <React.Fragment key={item.id}>
                    <ListItem 
                      sx={{ 
                        px: 2, 
                        py: 1.5, 
                        borderRadius: 1,
                        '&:hover': {
                          bgcolor: 'background.default',
                        },
                        cursor: 'pointer',
                      }}
                      onClick={() => navigate('/executive/my-sales')}
                    >
                      <ListItemIcon>
                        {item.paymentMethod === 'Cash' && <LocalAtm color="success" />}
                        {item.paymentMethod === 'UPI' && <CreditCard color="primary" />}
                        {item.paymentMethod === 'Card' && <CreditCard color="secondary" />}
                      </ListItemIcon>
                      <ListItemText
                        primary={
                          <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            <Typography variant="body1" sx={{ fontWeight: 500 }}>
                              {item.invoice}
                            </Typography>
                            <Chip 
                              label={item.paymentMethod} 
                              size="small" 
                              color={
                                item.paymentMethod === 'Cash' ? 'success' : 
                                item.paymentMethod === 'UPI' ? 'primary' : 
                                'secondary'
                              }
                              sx={{ ml: 1 }}
                            />
                          </Box>
                        }
                        secondary={
                          <Typography variant="body2" color="textSecondary">
                            {item.amount} • {item.items} items • {item.time}
                          </Typography>
                        }
                      />
                    </ListItem>
                    {index < recentSalesData.length - 1 && <Divider component="li" />}
                  </React.Fragment>
                ))}
              </List>
              <Box sx={{ mt: 2, display: 'flex', justifyContent: 'center' }}>
                <Button 
                  variant="contained" 
                  color="primary"
                  startIcon={<Add />}
                  onClick={() => navigate('/executive/new-sale')}
                >
                  New Sale
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6" component="h2">
                  Top Selling Brands
                </Typography>
                <Button 
                  variant="text" 
                  size="small" 
                  color="primary"
                  onClick={() => navigate('/executive/brand-sales')}
                >
                  View All
                </Button>
              </Box>
              <List>
                {topSellingBrandsData.map((item, index) => (
                  <React.Fragment key={item.name}>
                    <ListItem 
                      sx={{ 
                        px: 2, 
                        py: 1.5, 
                        borderRadius: 1,
                      }}
                    >
                      <ListItemText
                        primary={
                          <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            <Typography variant="body1" sx={{ fontWeight: 500 }}>
                              {index + 1}. {item.name}
                            </Typography>
                          </Box>
                        }
                        secondary={
                          <Box sx={{ mt: 1 }}>
                            <Box sx={{ display: 'flex', alignItems: 'center', mb: 0.5 }}>
                              <Box sx={{ flexGrow: 1, mr: 1 }}>
                                <LinearProgress 
                                  variant="determinate" 
                                  value={(item.sales / topSellingBrandsData[0].sales) * 100} 
                                  color="primary"
                                  sx={{ height: 6, borderRadius: 3 }}
                                />
                              </Box>
                              <Typography variant="body2" color="textSecondary">
                                ₹{item.sales.toLocaleString()}
                              </Typography>
                            </Box>
                          </Box>
                        }
                      />
                    </ListItem>
                    {index < topSellingBrandsData.length - 1 && <Divider component="li" />}
                  </React.Fragment>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6" component="h2">
                  Pending Approvals
                </Typography>
                <Button 
                  variant="text" 
                  size="small" 
                  color="primary"
                  onClick={() => navigate('/executive/pending-approvals')}
                >
                  View All
                </Button>
              </Box>
              <List>
                {pendingApprovalsData.map((item, index) => (
                  <React.Fragment key={item.id}>
                    <ListItem 
                      sx={{ 
                        px: 2, 
                        py: 1.5, 
                        borderRadius: 1,
                        '&:hover': {
                          bgcolor: 'background.default',
                        },
                        cursor: 'pointer',
                      }}
                      onClick={() => navigate('/executive/pending-approvals')}
                    >
                      <ListItemIcon>
                        {item.type === 'Sale' && <Receipt color="primary" />}
                        {item.type === 'Stock Adjustment' && <Inventory color="secondary" />}
                        {item.type === 'Return' && <AssignmentReturn color="error" />}
                      </ListItemIcon>
                      <ListItemText
                        primary={
                          <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            <Typography variant="body1" sx={{ fontWeight: 500 }}>
                              {item.type} {item.number}
                            </Typography>
                            <Chip 
                              label={item.status} 
                              size="small" 
                              color={item.status === 'Pending' ? 'warning' : 'error'}
                              sx={{ ml: 1 }}
                            />
                          </Box>
                        }
                        secondary={
                          <Typography variant="body2" color="textSecondary">
                            {item.amount || item.items} • {item.time}
                            {item.reason && ` • Reason: ${item.reason}`}
                          </Typography>
                        }
                      />
                    </ListItem>
                    {index < pendingApprovalsData.length - 1 && <Divider component="li" />}
                  </React.Fragment>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ExecutiveDashboard;