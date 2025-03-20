import React, { useState } from 'react';
import {
  Box,
  Container,
  Typography,
  Button,
  Card,
  CardContent,
  Grid,
  TextField,
  InputAdornment,
  IconButton,
  Tabs,
  Tab,
  Divider,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  useTheme,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  DateRange as DateRangeIcon,
  Download as DownloadIcon,
  Print as PrintIcon,
  Refresh as RefreshIcon,
  BarChart as BarChartIcon,
  PieChart as PieChartIcon,
  Timeline as TimelineIcon,
  Inventory as InventoryIcon,
  ShoppingCart as ShoppingCartIcon,
  AttachMoney as AttachMoneyIcon,
  Category as CategoryIcon,
  Person as PersonIcon,
} from '@mui/icons-material';
import { PageHeader, ChartCard } from '../../components/common';
import { useTranslations } from '../../hooks';
import { format, subDays, startOfMonth, endOfMonth } from 'date-fns';

// Mock data for sales by date
const mockSalesByDateData = {
  labels: Array.from({ length: 30 }, (_, i) => format(subDays(new Date(), 29 - i), 'MMM dd')),
  datasets: [
    {
      label: 'Sales',
      data: [
        12000, 15000, 18000, 14000, 16000, 19000, 22000,
        20000, 18000, 16000, 15000, 17000, 19000, 21000,
        23000, 25000, 24000, 22000, 20000, 18000, 19000,
        21000, 23000, 25000, 27000, 29000, 28000, 26000,
        24000, 22000
      ],
      backgroundColor: 'rgba(63, 81, 181, 0.2)',
      borderColor: 'rgba(63, 81, 181, 1)',
      borderWidth: 2,
      fill: true,
    },
  ],
};

// Mock data for sales by category
const mockSalesByCategoryData = {
  labels: ['Whiskey', 'Vodka', 'Rum', 'Beer', 'Wine', 'Gin'],
  datasets: [
    {
      label: 'Sales by Category',
      data: [35, 25, 15, 10, 10, 5],
      backgroundColor: [
        'rgba(63, 81, 181, 0.7)',
        'rgba(0, 188, 212, 0.7)',
        'rgba(76, 175, 80, 0.7)',
        'rgba(255, 152, 0, 0.7)',
        'rgba(244, 67, 54, 0.7)',
        'rgba(156, 39, 176, 0.7)',
      ],
      borderWidth: 1,
    },
  ],
};

// Mock data for sales by payment method
const mockSalesByPaymentMethodData = {
  labels: ['Cash', 'Card', 'UPI'],
  datasets: [
    {
      label: 'Sales by Payment Method',
      data: [50, 30, 20],
      backgroundColor: [
        'rgba(76, 175, 80, 0.7)',
        'rgba(63, 81, 181, 0.7)',
        'rgba(156, 39, 176, 0.7)',
      ],
      borderWidth: 1,
    },
  ],
};

// Mock data for top selling products
const mockTopSellingProducts = [
  { id: 1, name: 'Jack Daniels Whiskey', category: 'Whiskey', quantity: 45, revenue: 112500 },
  { id: 2, name: 'Absolut Vodka', category: 'Vodka', quantity: 38, revenue: 68400 },
  { id: 3, name: 'Corona Beer (6-pack)', category: 'Beer', quantity: 32, revenue: 19200 },
  { id: 4, name: 'Johnnie Walker Black Label', category: 'Whiskey', quantity: 28, revenue: 98000 },
  { id: 5, name: 'Bacardi Rum', category: 'Rum', quantity: 25, revenue: 30000 },
];

// Mock data for top customers
const mockTopCustomers = [
  { id: 1, name: 'John Doe', purchases: 12, revenue: 35000 },
  { id: 2, name: 'Jane Smith', purchases: 10, revenue: 28000 },
  { id: 3, name: 'Michael Wilson', purchases: 8, revenue: 22000 },
  { id: 4, name: 'Emily Davis', purchases: 7, revenue: 19000 },
  { id: 5, name: 'Robert Johnson', purchases: 6, revenue: 15000 },
];

// Mock data for inventory value
const mockInventoryValueData = {
  labels: Array.from({ length: 6 }, (_, i) => format(subDays(new Date(), (5 - i) * 30), 'MMM yyyy')),
  datasets: [
    {
      label: 'Inventory Value',
      data: [250000, 280000, 310000, 290000, 320000, 350000],
      backgroundColor: 'rgba(0, 188, 212, 0.2)',
      borderColor: 'rgba(0, 188, 212, 1)',
      borderWidth: 2,
      fill: true,
    },
  ],
};

// Date range options
const dateRangeOptions = [
  { label: 'Today', value: 'today' },
  { label: 'Yesterday', value: 'yesterday' },
  { label: 'Last 7 Days', value: 'last7days' },
  { label: 'Last 30 Days', value: 'last30days' },
  { label: 'This Month', value: 'thisMonth' },
  { label: 'Last Month', value: 'lastMonth' },
  { label: 'Custom Range', value: 'custom' },
];

/**
 * Reports component for Shop Manager
 */
const Reports: React.FC = () => {
  const { common, reports } = useTranslations();
  const theme = useTheme();
  const [tabValue, setTabValue] = useState(0);
  const [dateRange, setDateRange] = useState('last30days');
  const [startDate, setStartDate] = useState(format(subDays(new Date(), 30), 'yyyy-MM-dd'));
  const [endDate, setEndDate] = useState(format(new Date(), 'yyyy-MM-dd'));
  const [showCustomDateRange, setShowCustomDateRange] = useState(false);

  // Handle tab change
  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  // Handle date range change
  const handleDateRangeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const value = event.target.value;
    setDateRange(value);
    
    // Set start and end dates based on selected range
    const today = new Date();
    
    if (value === 'today') {
      setStartDate(format(today, 'yyyy-MM-dd'));
      setEndDate(format(today, 'yyyy-MM-dd'));
      setShowCustomDateRange(false);
    } else if (value === 'yesterday') {
      const yesterday = subDays(today, 1);
      setStartDate(format(yesterday, 'yyyy-MM-dd'));
      setEndDate(format(yesterday, 'yyyy-MM-dd'));
      setShowCustomDateRange(false);
    } else if (value === 'last7days') {
      setStartDate(format(subDays(today, 7), 'yyyy-MM-dd'));
      setEndDate(format(today, 'yyyy-MM-dd'));
      setShowCustomDateRange(false);
    } else if (value === 'last30days') {
      setStartDate(format(subDays(today, 30), 'yyyy-MM-dd'));
      setEndDate(format(today, 'yyyy-MM-dd'));
      setShowCustomDateRange(false);
    } else if (value === 'thisMonth') {
      setStartDate(format(startOfMonth(today), 'yyyy-MM-dd'));
      setEndDate(format(today, 'yyyy-MM-dd'));
      setShowCustomDateRange(false);
    } else if (value === 'lastMonth') {
      const lastMonth = subDays(startOfMonth(today), 1);
      setStartDate(format(startOfMonth(lastMonth), 'yyyy-MM-dd'));
      setEndDate(format(endOfMonth(lastMonth), 'yyyy-MM-dd'));
      setShowCustomDateRange(false);
    } else if (value === 'custom') {
      setShowCustomDateRange(true);
    }
  };

  return (
    <Container maxWidth="xl">
      <PageHeader
        title={reports('reports')}
        subtitle={reports('analyzeData')}
        icon={<BarChartIcon fontSize="large" />}
      />

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} sm={6} md={4}>
              <TextField
                select
                fullWidth
                label={reports('dateRange')}
                value={dateRange}
                onChange={handleDateRangeChange}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <DateRangeIcon />
                    </InputAdornment>
                  ),
                }}
                size="small"
              >
                {dateRangeOptions.map((option) => (
                  <MenuItem key={option.value} value={option.value}>
                    {option.label}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            
            {showCustomDateRange && (
              <>
                <Grid item xs={12} sm={6} md={3}>
                  <TextField
                    fullWidth
                    label={reports('startDate')}
                    type="date"
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                    InputLabelProps={{
                      shrink: true,
                    }}
                    size="small"
                  />
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <TextField
                    fullWidth
                    label={reports('endDate')}
                    type="date"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                    InputLabelProps={{
                      shrink: true,
                    }}
                    size="small"
                  />
                </Grid>
              </>
            )}
            
            <Grid item xs={12} sm={6} md={showCustomDateRange ? 2 : 8} sx={{ display: 'flex', justifyContent: 'flex-end', gap: 1 }}>
              <Button
                variant="outlined"
                startIcon={<RefreshIcon />}
                onClick={() => console.log('Refresh report')}
              >
                {common('refresh')}
              </Button>
              <Button
                variant="outlined"
                startIcon={<DownloadIcon />}
                onClick={() => console.log('Export report')}
              >
                {common('export')}
              </Button>
              <Button
                variant="outlined"
                startIcon={<PrintIcon />}
                onClick={() => console.log('Print report')}
              >
                {common('print')}
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <Card>
        <CardContent sx={{ pb: 1 }}>
          <Tabs
            value={tabValue}
            onChange={handleTabChange}
            indicatorColor="primary"
            textColor="primary"
            variant="scrollable"
            scrollButtons="auto"
            aria-label="report tabs"
          >
            <Tab icon={<TimelineIcon />} label={reports('salesOverview')} />
            <Tab icon={<CategoryIcon />} label={reports('productAnalysis')} />
            <Tab icon={<PersonIcon />} label={reports('customerAnalysis')} />
            <Tab icon={<InventoryIcon />} label={reports('inventoryAnalysis')} />
          </Tabs>
        </CardContent>
        <Divider />
        
        {/* Sales Overview Tab */}
        {tabValue === 0 && (
          <CardContent>
            <Grid container spacing={3}>
              <Grid item xs={12} md={4}>
                <Card variant="outlined">
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <AttachMoneyIcon color="primary" sx={{ mr: 1 }} />
                      <Typography variant="h6">
                        {reports('totalSales')}
                      </Typography>
                    </Box>
                    <Typography variant="h4" color="primary.main" gutterBottom>
                      ₹3,45,000
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      {reports('comparedToPrevious')}: +12%
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={4}>
                <Card variant="outlined">
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <ShoppingCartIcon color="secondary" sx={{ mr: 1 }} />
                      <Typography variant="h6">
                        {reports('totalOrders')}
                      </Typography>
                    </Box>
                    <Typography variant="h4" color="secondary.main" gutterBottom>
                      245
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      {reports('comparedToPrevious')}: +8%
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={4}>
                <Card variant="outlined">
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <TrendingUpIcon color="success" sx={{ mr: 1 }} />
                      <Typography variant="h6">
                        {reports('averageOrderValue')}
                      </Typography>
                    </Box>
                    <Typography variant="h4" color="success.main" gutterBottom>
                      ₹1,408
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      {reports('comparedToPrevious')}: +3%
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              
              <Grid item xs={12}>
                <ChartCard
                  title={reports('salesTrend')}
                  subtitle={reports('last30Days')}
                  chart={{
                    type: 'line',
                    data: mockSalesByDateData,
                    options: {
                      responsive: true,
                      maintainAspectRatio: false,
                      scales: {
                        y: {
                          beginAtZero: true,
                          ticks: {
                            callback: (value: any) => `₹${value / 1000}K`,
                          },
                        },
                      },
                      plugins: {
                        tooltip: {
                          callbacks: {
                            label: (context: any) => `Sales: ₹${context.raw.toLocaleString()}`,
                          },
                        },
                      },
                    },
                  }}
                  height={300}
                />
              </Grid>
              
              <Grid item xs={12} md={6}>
                <ChartCard
                  title={reports('salesByCategory')}
                  subtitle={reports('percentageDistribution')}
                  chart={{
                    type: 'pie',
                    data: mockSalesByCategoryData,
                    options: {
                      responsive: true,
                      maintainAspectRatio: false,
                      plugins: {
                        legend: {
                          position: 'right',
                        },
                        tooltip: {
                          callbacks: {
                            label: (context: any) => `${context.label}: ${context.raw}%`,
                          },
                        },
                      },
                    },
                  }}
                  height={300}
                />
              </Grid>
              
              <Grid item xs={12} md={6}>
                <ChartCard
                  title={reports('salesByPaymentMethod')}
                  subtitle={reports('percentageDistribution')}
                  chart={{
                    type: 'pie',
                    data: mockSalesByPaymentMethodData,
                    options: {
                      responsive: true,
                      maintainAspectRatio: false,
                      plugins: {
                        legend: {
                          position: 'right',
                        },
                        tooltip: {
                          callbacks: {
                            label: (context: any) => `${context.label}: ${context.raw}%`,
                          },
                        },
                      },
                    },
                  }}
                  height={300}
                />
              </Grid>
            </Grid>
          </CardContent>
        )}
        
        {/* Product Analysis Tab */}
        {tabValue === 1 && (
          <CardContent>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>
                  {reports('topSellingProducts')}
                </Typography>
                <TableContainer component={Paper} variant="outlined">
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>{common('product')}</TableCell>
                        <TableCell>{common('category')}</TableCell>
                        <TableCell align="right">{common('quantity')}</TableCell>
                        <TableCell align="right">{common('revenue')}</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {mockTopSellingProducts.map((product) => (
                        <TableRow key={product.id}>
                          <TableCell>{product.name}</TableCell>
                          <TableCell>{product.category}</TableCell>
                          <TableCell align="right">{product.quantity}</TableCell>
                          <TableCell align="right">₹{product.revenue.toLocaleString()}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </Grid>
              
              <Grid item xs={12}>
                <ChartCard
                  title={reports('salesByCategory')}
                  subtitle={reports('percentageDistribution')}
                  chart={{
                    type: 'pie',
                    data: mockSalesByCategoryData,
                    options: {
                      responsive: true,
                      maintainAspectRatio: false,
                      plugins: {
                        legend: {
                          position: 'right',
                        },
                        tooltip: {
                          callbacks: {
                            label: (context: any) => `${context.label}: ${context.raw}%`,
                          },
                        },
                      },
                    },
                  }}
                  height={300}
                />
              </Grid>
            </Grid>
          </CardContent>
        )}
        
        {/* Customer Analysis Tab */}
        {tabValue === 2 && (
          <CardContent>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>
                  {reports('topCustomers')}
                </Typography>
                <TableContainer component={Paper} variant="outlined">
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>{common('customer')}</TableCell>
                        <TableCell align="right">{reports('purchases')}</TableCell>
                        <TableCell align="right">{common('revenue')}</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {mockTopCustomers.map((customer) => (
                        <TableRow key={customer.id}>
                          <TableCell>{customer.name}</TableCell>
                          <TableCell align="right">{customer.purchases}</TableCell>
                          <TableCell align="right">₹{customer.revenue.toLocaleString()}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </Grid>
            </Grid>
          </CardContent>
        )}
        
        {/* Inventory Analysis Tab */}
        {tabValue === 3 && (
          <CardContent>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Card variant="outlined">
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <InventoryIcon color="primary" sx={{ mr: 1 }} />
                      <Typography variant="h6">
                        {reports('currentInventoryValue')}
                      </Typography>
                    </Box>
                    <Typography variant="h4" color="primary.main" gutterBottom>
                      ₹3,50,000
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      {reports('comparedToPrevious')}: +9%
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={6}>
                <Card variant="outlined">
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <InventoryIcon color="error" sx={{ mr: 1 }} />
                      <Typography variant="h6">
                        {reports('lowStockItems')}
                      </Typography>
                    </Box>
                    <Typography variant="h4" color="error.main" gutterBottom>
                      5
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      {reports('needsAttention')}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              
              <Grid item xs={12}>
                <ChartCard
                  title={reports('inventoryValueTrend')}
                  subtitle={reports('last6Months')}
                  chart={{
                    type: 'line',
                    data: mockInventoryValueData,
                    options: {
                      responsive: true,
                      maintainAspectRatio: false,
                      scales: {
                        y: {
                          beginAtZero: true,
                          ticks: {
                            callback: (value: any) => `₹${value / 1000}K`,
                          },
                        },
                      },
                      plugins: {
                        tooltip: {
                          callbacks: {
                            label: (context: any) => `Value: ₹${context.raw.toLocaleString()}`,
                          },
                        },
                      },
                    },
                  }}
                  height={300}
                />
              </Grid>
            </Grid>
          </CardContent>
        )}
      </Card>
    </Container>
  );
};

export default Reports;