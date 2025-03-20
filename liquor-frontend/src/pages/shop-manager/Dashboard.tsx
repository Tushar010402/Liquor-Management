import React, { useState } from 'react';
import {
  Box,
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Tabs,
  Tab,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  IconButton,
  useTheme,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  AttachMoney as MoneyIcon,
  Inventory as InventoryIcon,
  ShoppingCart as ShoppingCartIcon,
  People as PeopleIcon,
  Warning as WarningIcon,
  ArrowUpward as ArrowUpwardIcon,
  ArrowDownward as ArrowDownwardIcon,
  MoreVert as MoreVertIcon,
  Add as AddIcon,
  Print as PrintIcon,
} from '@mui/icons-material';
import { PageHeader, StatCard, ChartCard } from '../../components/common';
import { useTranslations } from '../../hooks';

// Mock data for sales
const mockSalesData = {
  labels: ['9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', '4PM', '5PM', '6PM', '7PM', '8PM'],
  datasets: [
    {
      label: 'Sales',
      data: [5000, 7500, 12000, 15000, 10000, 8000, 9000, 11000, 14000, 18000, 20000, 15000],
      backgroundColor: 'rgba(63, 81, 181, 0.2)',
      borderColor: 'rgba(63, 81, 181, 1)',
      borderWidth: 2,
      fill: true,
    },
  ],
};

// Mock data for product categories
const mockCategoryData = {
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

// Mock data for recent sales
const mockRecentSales = [
  { id: 1, customer: 'John Doe', items: 3, total: 2500, time: '15 minutes ago' },
  { id: 2, customer: 'Jane Smith', items: 2, total: 1800, time: '45 minutes ago' },
  { id: 3, customer: 'Robert Johnson', items: 5, total: 4200, time: '1 hour ago' },
  { id: 4, customer: 'Emily Davis', items: 1, total: 950, time: '2 hours ago' },
  { id: 5, customer: 'Michael Wilson', items: 4, total: 3100, time: '3 hours ago' },
];

// Mock data for low stock items
const mockLowStockItems = [
  { id: 1, name: 'Jack Daniels Whiskey', stock: 5, threshold: 10 },
  { id: 2, name: 'Absolut Vodka', stock: 3, threshold: 8 },
  { id: 3, name: 'Corona Beer', stock: 6, threshold: 12 },
  { id: 4, name: 'Bacardi Rum', stock: 4, threshold: 8 },
  { id: 5, name: 'Johnnie Walker Black Label', stock: 2, threshold: 5 },
];

/**
 * Shop Manager Dashboard component
 */
const Dashboard: React.FC = () => {
  const { dashboard, common, products } = useTranslations();
  const theme = useTheme();
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  return (
    <Container maxWidth="xl">
      <PageHeader
        title={dashboard('dashboard')}
        subtitle={dashboard('welcome')}
        icon={<TrendingUpIcon fontSize="large" />}
      />

      <Grid container spacing={3}>
        {/* Statistics Cards */}
        <Grid item xs={12} sm={6} md={4} lg={2.4}>
          <StatCard
            title={dashboard('todaySales')}
            value="₹45,000"
            icon={<MoneyIcon />}
            color={theme.palette.primary.main}
            subtitle="+15% vs yesterday"
            trend="up"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4} lg={2.4}>
          <StatCard
            title={dashboard('totalItems')}
            value="156"
            icon={<InventoryIcon />}
            color={theme.palette.secondary.main}
            subtitle="5 low stock items"
            trend="neutral"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4} lg={2.4}>
          <StatCard
            title={dashboard('totalOrders')}
            value="38"
            icon={<ShoppingCartIcon />}
            color={theme.palette.success.main}
            subtitle="+8% vs yesterday"
            trend="up"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={6} lg={2.4}>
          <StatCard
            title={dashboard('totalCustomers')}
            value="24"
            icon={<PeopleIcon />}
            color={theme.palette.info.main}
            subtitle="+4% vs yesterday"
            trend="up"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={6} lg={2.4}>
          <StatCard
            title={dashboard('lowStock')}
            value="5"
            icon={<WarningIcon />}
            color={theme.palette.warning.main}
            subtitle="Needs attention"
            trend="down"
          />
        </Grid>

        {/* Charts */}
        <Grid item xs={12} md={8}>
          <ChartCard
            title={dashboard('todaySalesOverTime')}
            subtitle={dashboard('hourlyBreakdown')}
            chart={{
              type: 'line',
              data: mockSalesData,
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
            actions={
              <Button
                variant="outlined"
                size="small"
                startIcon={<PrintIcon />}
                onClick={() => console.log('Print report')}
              >
                {common('printReport')}
              </Button>
            }
          />
        </Grid>
        <Grid item xs={12} md={4}>
          <ChartCard
            title={dashboard('salesByCategory')}
            subtitle={dashboard('productCategoryBreakdown')}
            chart={{
              type: 'pie',
              data: mockCategoryData,
              options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                  legend: {
                    position: 'bottom',
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

        {/* Recent Sales and Low Stock */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6" component="h2">
                  {dashboard('recentSales')}
                </Typography>
                <Button
                  variant="contained"
                  size="small"
                  startIcon={<AddIcon />}
                  onClick={() => console.log('New sale')}
                >
                  {common('newSale')}
                </Button>
              </Box>
              <List>
                {mockRecentSales.map((sale) => (
                  <React.Fragment key={sale.id}>
                    <ListItem
                      secondaryAction={
                        <IconButton edge="end" aria-label="more">
                          <MoreVertIcon />
                        </IconButton>
                      }
                    >
                      <ListItemAvatar>
                        <Avatar sx={{ bgcolor: theme.palette.primary.main }}>
                          <ShoppingCartIcon />
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText
                        primary={
                          <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                            <Typography variant="body1" fontWeight={500}>
                              {sale.customer}
                            </Typography>
                            <Typography variant="body1" fontWeight={600}>
                              ₹{sale.total.toLocaleString()}
                            </Typography>
                          </Box>
                        }
                        secondary={
                          <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                            <Typography variant="body2" color="textSecondary">
                              {sale.items} {sale.items === 1 ? 'item' : 'items'}
                            </Typography>
                            <Typography variant="body2" color="textSecondary">
                              {sale.time}
                            </Typography>
                          </Box>
                        }
                      />
                    </ListItem>
                    {sale.id < mockRecentSales.length && <Divider variant="inset" component="li" />}
                  </React.Fragment>
                ))}
              </List>
              <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
                <Button color="primary">
                  {common('viewAll')}
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
                  {products('lowStock')}
                </Typography>
                <Button
                  variant="outlined"
                  size="small"
                  color="warning"
                  onClick={() => console.log('Restock items')}
                >
                  {products('restockItems')}
                </Button>
              </Box>
              <List>
                {mockLowStockItems.map((item) => (
                  <React.Fragment key={item.id}>
                    <ListItem
                      secondaryAction={
                        <IconButton edge="end" aria-label="more">
                          <MoreVertIcon />
                        </IconButton>
                      }
                    >
                      <ListItemAvatar>
                        <Avatar sx={{ bgcolor: theme.palette.warning.main }}>
                          <InventoryIcon />
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText
                        primary={
                          <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                            <Typography variant="body1" fontWeight={500}>
                              {item.name}
                            </Typography>
                            <Typography
                              variant="body1"
                              fontWeight={600}
                              color={item.stock < item.threshold / 2 ? 'error.main' : 'warning.main'}
                            >
                              {item.stock} left
                            </Typography>
                          </Box>
                        }
                        secondary={
                          <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                            <Typography variant="body2" color="textSecondary">
                              {products('threshold')}: {item.threshold}
                            </Typography>
                            <Typography variant="body2" color="error">
                              {products('needsRestock')}
                            </Typography>
                          </Box>
                        }
                      />
                    </ListItem>
                    {item.id < mockLowStockItems.length && <Divider variant="inset" component="li" />}
                  </React.Fragment>
                ))}
              </List>
              <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
                <Button color="primary">
                  {common('viewAll')}
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Quick Actions */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                {common('quickActions')}
              </Typography>
              <Grid container spacing={2} sx={{ mt: 1 }}>
                <Grid item>
                  <Button variant="contained" color="primary" startIcon={<ShoppingCartIcon />}>
                    {common('newSale')}
                  </Button>
                </Grid>
                <Grid item>
                  <Button variant="contained" color="secondary" startIcon={<InventoryIcon />}>
                    {products('addProduct')}
                  </Button>
                </Grid>
                <Grid item>
                  <Button variant="contained" color="warning" startIcon={<WarningIcon />}>
                    {products('manageStock')}
                  </Button>
                </Grid>
                <Grid item>
                  <Button variant="contained" color="info" startIcon={<TrendingUpIcon />}>
                    {common('viewReports')}
                  </Button>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;