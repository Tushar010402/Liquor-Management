import React, { useState, useEffect } from 'react';
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
  CircularProgress,
  Alert,
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
  Refresh as RefreshIcon,
} from '@mui/icons-material';
import { PageHeader, StatCard, ChartCard } from '../../components/common';
import { useTranslations, useAuth, useNotification } from '../../hooks';
import { 
  dashboardService, 
  DashboardStats, 
  SalesOverTime, 
  SalesByCategory, 
  RecentSale, 
  LowStockItem 
} from '../../services/api';
import { useNavigate } from 'react-router-dom';

/**
 * Shop Manager Dashboard component
 */
const Dashboard: React.FC = () => {
  const { dashboard, common, products } = useTranslations();
  const theme = useTheme();
  const { user } = useAuth();
  const { showNotification } = useNotification();
  const navigate = useNavigate();
  const [tabValue, setTabValue] = useState(0);
  
  // State for dashboard data
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [salesOverTime, setSalesOverTime] = useState<SalesOverTime | null>(null);
  const [salesByCategory, setSalesByCategory] = useState<SalesByCategory | null>(null);
  const [recentSales, setRecentSales] = useState<RecentSale[]>([]);
  const [lowStockItems, setLowStockItems] = useState<LowStockItem[]>([]);
  const [period, setPeriod] = useState<'day' | 'week' | 'month' | 'year'>('day');
  
  // Get shop ID from user
  const shopId = user?.assigned_shops && user.assigned_shops.length > 0 
    ? parseInt(user.assigned_shops[0].id) 
    : undefined;
  
  // Fetch dashboard data
  useEffect(() => {
    const fetchDashboardData = async () => {
      setIsLoading(true);
      setError(null);
      
      try {
        if (process.env.NODE_ENV === 'production') {
          // Fetch dashboard stats
          const statsData = await dashboardService.getStats(shopId);
          setStats(statsData);
          
          // Fetch sales over time
          const salesOverTimeData = await dashboardService.getSalesOverTime(shopId, period);
          setSalesOverTime(salesOverTimeData);
          
          // Fetch sales by category
          const salesByCategoryData = await dashboardService.getSalesByCategory(shopId, period);
          setSalesByCategory(salesByCategoryData);
          
          // Fetch recent sales
          const recentSalesData = await dashboardService.getRecentSales(shopId);
          setRecentSales(recentSalesData);
          
          // Fetch low stock items
          const lowStockItemsData = await dashboardService.getLowStockItems(shopId);
          setLowStockItems(lowStockItemsData);
        } else {
          // For development/demo purposes
          await new Promise(resolve => setTimeout(resolve, 1000));
          
          // Mock stats
          setStats({
            today_sales: 45000,
            total_items: 156,
            total_orders: 38,
            total_customers: 24,
            low_stock_count: 5,
            sales_growth: 15,
            orders_growth: 8,
            customers_growth: 4,
          });
          
          // Mock sales over time
          setSalesOverTime({
            labels: ['9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', '4PM', '5PM', '6PM', '7PM', '8PM'],
            data: [5000, 7500, 12000, 15000, 10000, 8000, 9000, 11000, 14000, 18000, 20000, 15000],
          });
          
          // Mock sales by category
          setSalesByCategory({
            labels: ['Whiskey', 'Vodka', 'Rum', 'Beer', 'Wine', 'Gin'],
            data: [35, 25, 15, 10, 10, 5],
          });
          
          // Mock recent sales
          setRecentSales([
            { id: 1, invoice_number: 'INV-2023-001', customer_name: 'John Doe', items_count: 3, total_amount: 2500, created_at: '2023-01-01T10:00:00Z', time_ago: '15 minutes ago' },
            { id: 2, invoice_number: 'INV-2023-002', customer_name: 'Jane Smith', items_count: 2, total_amount: 1800, created_at: '2023-01-01T09:30:00Z', time_ago: '45 minutes ago' },
            { id: 3, invoice_number: 'INV-2023-003', customer_name: 'Robert Johnson', items_count: 5, total_amount: 4200, created_at: '2023-01-01T09:00:00Z', time_ago: '1 hour ago' },
            { id: 4, invoice_number: 'INV-2023-004', customer_name: 'Emily Davis', items_count: 1, total_amount: 950, created_at: '2023-01-01T08:00:00Z', time_ago: '2 hours ago' },
            { id: 5, invoice_number: 'INV-2023-005', customer_name: 'Michael Wilson', items_count: 4, total_amount: 3100, created_at: '2023-01-01T07:00:00Z', time_ago: '3 hours ago' },
          ]);
          
          // Mock low stock items
          setLowStockItems([
            { id: 1, name: 'Jack Daniels Whiskey', stock: 5, threshold: 10, category: 'Whiskey' },
            { id: 2, name: 'Absolut Vodka', stock: 3, threshold: 8, category: 'Vodka' },
            { id: 3, name: 'Corona Beer', stock: 6, threshold: 12, category: 'Beer' },
            { id: 4, name: 'Bacardi Rum', stock: 4, threshold: 8, category: 'Rum' },
            { id: 5, name: 'Johnnie Walker Black Label', stock: 2, threshold: 5, category: 'Whiskey' },
          ]);
        }
      } catch (err: any) {
        console.error('Error fetching dashboard data:', err);
        setError(err.message || 'Failed to fetch dashboard data');
        showNotification({
          message: 'Failed to fetch dashboard data. Please try again later.',
          variant: 'error',
        });
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchDashboardData();
  }, [shopId, period, showNotification]);
  
  // Handle tab change
  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
    
    // Set period based on tab
    switch (newValue) {
      case 0: // Today
        setPeriod('day');
        break;
      case 1: // This Week
        setPeriod('week');
        break;
      case 2: // This Month
        setPeriod('month');
        break;
      case 3: // This Year
        setPeriod('year');
        break;
      default:
        setPeriod('day');
    }
  };
  
  // Refresh dashboard data
  const handleRefreshData = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      if (process.env.NODE_ENV === 'production') {
        // Fetch dashboard stats
        const statsData = await dashboardService.getStats(shopId);
        setStats(statsData);
        
        // Fetch sales over time
        const salesOverTimeData = await dashboardService.getSalesOverTime(shopId, period);
        setSalesOverTime(salesOverTimeData);
        
        // Fetch sales by category
        const salesByCategoryData = await dashboardService.getSalesByCategory(shopId, period);
        setSalesByCategory(salesByCategoryData);
        
        // Fetch recent sales
        const recentSalesData = await dashboardService.getRecentSales(shopId);
        setRecentSales(recentSalesData);
        
        // Fetch low stock items
        const lowStockItemsData = await dashboardService.getLowStockItems(shopId);
        setLowStockItems(lowStockItemsData);
      } else {
        // For development/demo purposes
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
      
      showNotification({
        message: 'Dashboard data refreshed successfully',
        variant: 'success',
      });
    } catch (err: any) {
      console.error('Error refreshing dashboard data:', err);
      setError(err.message || 'Failed to refresh dashboard data');
      showNotification({
        message: 'Failed to refresh dashboard data. Please try again later.',
        variant: 'error',
      });
    } finally {
      setIsLoading(false);
    }
  };
  
  // Navigate to new sale page
  const handleNewSale = () => {
    navigate('/shop-manager/point-of-sale');
  };
  
  // Navigate to inventory management page
  const handleManageInventory = () => {
    navigate('/shop-manager/inventory');
  };
  
  // Navigate to reports page
  const handleViewReports = () => {
    navigate('/shop-manager/reports');
  };
  
  // Format currency
  const formatCurrency = (amount: number) => {
    return `₹${amount.toLocaleString()}`;
  };

  return (
    <Container maxWidth="xl">
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <PageHeader
          title={dashboard('dashboard')}
          subtitle={dashboard('welcome')}
          icon={<TrendingUpIcon fontSize="large" />}
        />
        <Button
          variant="outlined"
          startIcon={isLoading ? <CircularProgress size={20} /> : <RefreshIcon />}
          onClick={handleRefreshData}
          disabled={isLoading}
        >
          {isLoading ? common('loading') : common('refresh')}
        </Button>
      </Box>
      
      {error && (
        <Alert 
          severity="error" 
          sx={{ mb: 3 }}
          action={
            <Button color="inherit" size="small" onClick={handleRefreshData}>
              {common('retry')}
            </Button>
          }
        >
          {error}
        </Alert>
      )}
      
      <Box sx={{ mb: 3 }}>
        <Tabs
          value={tabValue}
          onChange={handleTabChange}
          indicatorColor="primary"
          textColor="primary"
          variant="fullWidth"
        >
          <Tab label={dashboard('today')} />
          <Tab label={dashboard('thisWeek')} />
          <Tab label={dashboard('thisMonth')} />
          <Tab label={dashboard('thisYear')} />
        </Tabs>
      </Box>

      <Grid container spacing={3}>
        {/* Statistics Cards */}
        <Grid item xs={12} sm={6} md={4} lg={2.4}>
          <StatCard
            title={dashboard('todaySales')}
            value={isLoading ? '-' : stats ? formatCurrency(stats.today_sales) : '₹0'}
            icon={<MoneyIcon />}
            color={theme.palette.primary.main}
            subtitle={isLoading ? common('loading') : stats && stats.sales_growth > 0 
              ? `+${stats.sales_growth}% vs yesterday` 
              : stats && stats.sales_growth < 0 
                ? `${stats.sales_growth}% vs yesterday` 
                : 'Same as yesterday'}
            trend={isLoading ? 'neutral' : stats && stats.sales_growth > 0 
              ? 'up' 
              : stats && stats.sales_growth < 0 
                ? 'down' 
                : 'neutral'}
            isLoading={isLoading}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4} lg={2.4}>
          <StatCard
            title={dashboard('totalItems')}
            value={isLoading ? '-' : stats ? stats.total_items.toString() : '0'}
            icon={<InventoryIcon />}
            color={theme.palette.secondary.main}
            subtitle={isLoading ? common('loading') : stats ? `${stats.low_stock_count} low stock items` : 'No low stock items'}
            trend="neutral"
            isLoading={isLoading}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4} lg={2.4}>
          <StatCard
            title={dashboard('totalOrders')}
            value={isLoading ? '-' : stats ? stats.total_orders.toString() : '0'}
            icon={<ShoppingCartIcon />}
            color={theme.palette.success.main}
            subtitle={isLoading ? common('loading') : stats && stats.orders_growth > 0 
              ? `+${stats.orders_growth}% vs yesterday` 
              : stats && stats.orders_growth < 0 
                ? `${stats.orders_growth}% vs yesterday` 
                : 'Same as yesterday'}
            trend={isLoading ? 'neutral' : stats && stats.orders_growth > 0 
              ? 'up' 
              : stats && stats.orders_growth < 0 
                ? 'down' 
                : 'neutral'}
            isLoading={isLoading}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={6} lg={2.4}>
          <StatCard
            title={dashboard('totalCustomers')}
            value={isLoading ? '-' : stats ? stats.total_customers.toString() : '0'}
            icon={<PeopleIcon />}
            color={theme.palette.info.main}
            subtitle={isLoading ? common('loading') : stats && stats.customers_growth > 0 
              ? `+${stats.customers_growth}% vs yesterday` 
              : stats && stats.customers_growth < 0 
                ? `${stats.customers_growth}% vs yesterday` 
                : 'Same as yesterday'}
            trend={isLoading ? 'neutral' : stats && stats.customers_growth > 0 
              ? 'up' 
              : stats && stats.customers_growth < 0 
                ? 'down' 
                : 'neutral'}
            isLoading={isLoading}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={6} lg={2.4}>
          <StatCard
            title={dashboard('lowStock')}
            value={isLoading ? '-' : stats ? stats.low_stock_count.toString() : '0'}
            icon={<WarningIcon />}
            color={theme.palette.warning.main}
            subtitle={isLoading ? common('loading') : stats && stats.low_stock_count > 0 ? 'Needs attention' : 'Stock levels good'}
            trend={isLoading ? 'neutral' : stats && stats.low_stock_count > 0 ? 'down' : 'up'}
            isLoading={isLoading}
          />
        </Grid>

        {/* Charts */}
        <Grid item xs={12} md={8}>
          <ChartCard
            title={dashboard('todaySalesOverTime')}
            subtitle={
              period === 'day' ? dashboard('hourlyBreakdown') :
              period === 'week' ? dashboard('dailyBreakdown') :
              period === 'month' ? dashboard('weeklyBreakdown') :
              dashboard('monthlyBreakdown')
            }
            chart={{
              type: 'line',
              data: {
                labels: salesOverTime?.labels || [],
                datasets: [
                  {
                    label: 'Sales',
                    data: salesOverTime?.data || [],
                    backgroundColor: 'rgba(63, 81, 181, 0.2)',
                    borderColor: 'rgba(63, 81, 181, 1)',
                    borderWidth: 2,
                    fill: true,
                  },
                ],
              },
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
            isLoading={isLoading}
            actions={
              <Button
                variant="outlined"
                size="small"
                startIcon={<PrintIcon />}
                onClick={handleViewReports}
                disabled={isLoading}
              >
                {common('viewReports')}
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
              data: {
                labels: salesByCategory?.labels || [],
                datasets: [
                  {
                    label: 'Sales by Category',
                    data: salesByCategory?.data || [],
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
              },
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
            isLoading={isLoading}
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
                  onClick={handleNewSale}
                  disabled={isLoading}
                >
                  {common('newSale')}
                </Button>
              </Box>
              
              {isLoading ? (
                <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', py: 5 }}>
                  <CircularProgress size={30} />
                </Box>
              ) : recentSales.length > 0 ? (
                <List>
                  {recentSales.map((sale, index) => (
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
                                {sale.customer_name || 'Walk-in Customer'}
                              </Typography>
                              <Typography variant="body1" fontWeight={600}>
                                ₹{sale.total_amount.toLocaleString()}
                              </Typography>
                            </Box>
                          }
                          secondary={
                            <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                              <Typography variant="body2" color="textSecondary">
                                {sale.items_count} {sale.items_count === 1 ? 'item' : 'items'}
                              </Typography>
                              <Typography variant="body2" color="textSecondary">
                                {sale.time_ago}
                              </Typography>
                            </Box>
                          }
                        />
                      </ListItem>
                      {index < recentSales.length - 1 && <Divider variant="inset" component="li" />}
                    </React.Fragment>
                  ))}
                </List>
              ) : (
                <Box sx={{ py: 5, textAlign: 'center' }}>
                  <Typography variant="body1" color="textSecondary">
                    {dashboard('noRecentSales')}
                  </Typography>
                </Box>
              )}
              
              <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
                <Button 
                  color="primary"
                  onClick={() => navigate('/shop-manager/sales')}
                  disabled={isLoading}
                >
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
                  onClick={handleManageInventory}
                  disabled={isLoading}
                >
                  {products('manageStock')}
                </Button>
              </Box>
              
              {isLoading ? (
                <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', py: 5 }}>
                  <CircularProgress size={30} />
                </Box>
              ) : lowStockItems.length > 0 ? (
                <List>
                  {lowStockItems.map((item, index) => (
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
                      {index < lowStockItems.length - 1 && <Divider variant="inset" component="li" />}
                    </React.Fragment>
                  ))}
                </List>
              ) : (
                <Box sx={{ py: 5, textAlign: 'center' }}>
                  <Typography variant="body1" color="textSecondary">
                    {products('noLowStockItems')}
                  </Typography>
                </Box>
              )}
              
              <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
                <Button 
                  color="primary"
                  onClick={handleManageInventory}
                  disabled={isLoading}
                >
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
                  <Button 
                    variant="contained" 
                    color="primary" 
                    startIcon={<ShoppingCartIcon />}
                    onClick={handleNewSale}
                    disabled={isLoading}
                  >
                    {common('newSale')}
                  </Button>
                </Grid>
                <Grid item>
                  <Button 
                    variant="contained" 
                    color="secondary" 
                    startIcon={<InventoryIcon />}
                    onClick={() => navigate('/shop-manager/inventory/add-product')}
                    disabled={isLoading}
                  >
                    {products('addProduct')}
                  </Button>
                </Grid>
                <Grid item>
                  <Button 
                    variant="contained" 
                    color="warning" 
                    startIcon={<WarningIcon />}
                    onClick={handleManageInventory}
                    disabled={isLoading}
                  >
                    {products('manageStock')}
                  </Button>
                </Grid>
                <Grid item>
                  <Button 
                    variant="contained" 
                    color="info" 
                    startIcon={<TrendingUpIcon />}
                    onClick={handleViewReports}
                    disabled={isLoading}
                  >
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