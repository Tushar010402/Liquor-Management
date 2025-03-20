import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  Button,
  Divider,
  Avatar,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  IconButton,
  Paper,
  Chip,
  useTheme,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  Store,
  People,
  Inventory,
  Warning,
  MoreVert,
  ArrowUpward,
  ArrowDownward,
  CheckCircle,
  Error,
  Add,
  LocalShipping,
  MonetizationOn,
  Receipt,
  Business,
  AssignmentReturn,
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
  LineChart,
  Line,
  AreaChart,
  Area,
  PieChart,
  Pie,
  Cell,
  Legend,
} from 'recharts';

// Mock data for charts
const salesData = [
  { name: 'Jan', sales: 4000 },
  { name: 'Feb', sales: 5000 },
  { name: 'Mar', sales: 6000 },
  { name: 'Apr', sales: 7000 },
  { name: 'May', sales: 8500 },
  { name: 'Jun', sales: 9800 },
  { name: 'Jul', sales: 11000 },
  { name: 'Aug', sales: 12500 },
  { name: 'Sep', sales: 14000 },
  { name: 'Oct', sales: 16000 },
  { name: 'Nov', sales: 18000 },
  { name: 'Dec', sales: 21000 },
];

const shopPerformanceData = [
  { name: 'Downtown Shop', sales: 35000, profit: 12500 },
  { name: 'Uptown Shop', sales: 28000, profit: 9800 },
  { name: 'Westside Shop', sales: 22000, profit: 7500 },
  { name: 'Eastside Shop', sales: 18000, profit: 6200 },
  { name: 'Northside Shop', sales: 15000, profit: 5100 },
];

const topBrandsData = [
  { name: 'Johnnie Walker', value: 25 },
  { name: 'Jack Daniels', value: 20 },
  { name: 'Absolut', value: 15 },
  { name: 'Hennessy', value: 12 },
  { name: 'Others', value: 28 },
];

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

const pendingApprovalsData = [
  { type: 'Sales', count: 12, icon: <Receipt color="primary" /> },
  { type: 'Stock Adjustments', count: 8, icon: <Inventory color="secondary" /> },
  { type: 'Returns', count: 5, icon: <AssignmentReturn color="error" /> },
  { type: 'Expenses', count: 3, icon: <MonetizationOn color="warning" /> },
];

const recentActivities = [
  { id: 1, user: 'John Doe', action: 'Approved sales #12345', time: '5 minutes ago', avatar: '/static/images/avatar/1.jpg' },
  { id: 2, user: 'Jane Smith', action: 'Added new product', time: '30 minutes ago', avatar: '/static/images/avatar/2.jpg' },
  { id: 3, user: 'Mike Johnson', action: 'Updated inventory', time: '1 hour ago', avatar: '/static/images/avatar/3.jpg' },
  { id: 4, user: 'Sarah Williams', action: 'Processed return #5678', time: '2 hours ago', avatar: '/static/images/avatar/4.jpg' },
  { id: 5, user: 'David Brown', action: 'Created purchase order', time: '3 hours ago', avatar: '/static/images/avatar/5.jpg' },
];

const TenantAdminDashboard: React.FC = () => {
  const theme = useTheme();

  return (
    <Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 700 }}>
          Tenant Admin Dashboard
        </Typography>
        <Typography variant="subtitle1" color="textSecondary">
          Welcome back! Here's what's happening with your business today.
        </Typography>
      </Box>

      {/* Key Metrics */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                  <Typography variant="subtitle2" color="textSecondary">
                    Total Shops
                  </Typography>
                  <Avatar sx={{ bgcolor: 'primary.light' }}>
                    <Store />
                  </Avatar>
                </Box>
                <Typography variant="h4" component="div" sx={{ fontWeight: 700 }}>
                  5
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                  <ArrowUpward fontSize="small" color="success" />
                  <Typography variant="body2" color="success.main" sx={{ ml: 0.5 }}>
                    1 new
                  </Typography>
                  <Typography variant="body2" color="textSecondary" sx={{ ml: 1 }}>
                    this month
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.1 }}
          >
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                  <Typography variant="subtitle2" color="textSecondary">
                    Total Sales (MTD)
                  </Typography>
                  <Avatar sx={{ bgcolor: 'secondary.light' }}>
                    <Receipt />
                  </Avatar>
                </Box>
                <Typography variant="h4" component="div" sx={{ fontWeight: 700 }}>
                  ₹21.5L
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                  <ArrowUpward fontSize="small" color="success" />
                  <Typography variant="body2" color="success.main" sx={{ ml: 0.5 }}>
                    18% increase
                  </Typography>
                  <Typography variant="body2" color="textSecondary" sx={{ ml: 1 }}>
                    vs last month
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.2 }}
          >
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                  <Typography variant="subtitle2" color="textSecondary">
                    Inventory Value
                  </Typography>
                  <Avatar sx={{ bgcolor: 'success.light' }}>
                    <Inventory />
                  </Avatar>
                </Box>
                <Typography variant="h4" component="div" sx={{ fontWeight: 700 }}>
                  ₹1.2Cr
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                  <ArrowUpward fontSize="small" color="success" />
                  <Typography variant="body2" color="success.main" sx={{ ml: 0.5 }}>
                    5% increase
                  </Typography>
                  <Typography variant="body2" color="textSecondary" sx={{ ml: 1 }}>
                    vs last month
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.3 }}
          >
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                  <Typography variant="subtitle2" color="textSecondary">
                    Team Members
                  </Typography>
                  <Avatar sx={{ bgcolor: 'warning.light' }}>
                    <People />
                  </Avatar>
                </Box>
                <Typography variant="h4" component="div" sx={{ fontWeight: 700 }}>
                  32
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                  <ArrowUpward fontSize="small" color="success" />
                  <Typography variant="body2" color="success.main" sx={{ ml: 0.5 }}>
                    3 new
                  </Typography>
                  <Typography variant="body2" color="textSecondary" sx={{ ml: 1 }}>
                    this month
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>
      </Grid>

      {/* Charts */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={8}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.4 }}
          >
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                  <Typography variant="h6" component="h2">
                    Sales Trend
                  </Typography>
                  <Button variant="outlined" size="small">
                    View Details
                  </Button>
                </Box>
                <Box sx={{ height: 300 }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart
                      data={salesData}
                      margin={{
                        top: 5,
                        right: 30,
                        left: 20,
                        bottom: 5,
                      }}
                    >
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis />
                      <Tooltip />
                      <Area type="monotone" dataKey="sales" stroke={theme.palette.primary.main} fill={theme.palette.primary.light} />
                    </AreaChart>
                  </ResponsiveContainer>
                </Box>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        <Grid item xs={12} md={4}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.5 }}
          >
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                  <Typography variant="h6" component="h2">
                    Top Brands
                  </Typography>
                  <IconButton size="small">
                    <MoreVert fontSize="small" />
                  </IconButton>
                </Box>
                <Box sx={{ height: 250, display: 'flex', justifyContent: 'center' }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={topBrandsData}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                        label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                      >
                        {topBrandsData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </Box>
                <Divider sx={{ my: 2 }} />
                <Grid container spacing={2}>
                  {topBrandsData.map((brand, index) => (
                    <Grid item xs={6} key={brand.name}>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Box
                          sx={{
                            width: 12,
                            height: 12,
                            borderRadius: '50%',
                            bgcolor: COLORS[index % COLORS.length],
                            mr: 1,
                          }}
                        />
                        <Typography variant="body2" noWrap>
                          {brand.name}
                        </Typography>
                        <Typography variant="body2" sx={{ ml: 'auto', fontWeight: 600 }}>
                          {brand.value}%
                        </Typography>
                      </Box>
                    </Grid>
                  ))}
                </Grid>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.6 }}
          >
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h6" component="h2">
                    Shop Performance
                  </Typography>
                  <Button variant="text" size="small" color="primary">
                    View All
                  </Button>
                </Box>
                <Box sx={{ height: 300 }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={shopPerformanceData}
                      margin={{
                        top: 5,
                        right: 30,
                        left: 20,
                        bottom: 5,
                      }}
                    >
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Bar dataKey="sales" name="Sales" fill={theme.palette.primary.main} />
                      <Bar dataKey="profit" name="Profit" fill={theme.palette.secondary.main} />
                    </BarChart>
                  </ResponsiveContainer>
                </Box>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        <Grid item xs={12} md={6}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: 0.7 }}
              >
                <Card>
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                      <Typography variant="h6" component="h2">
                        Pending Approvals
                      </Typography>
                      <Button variant="text" size="small" color="primary">
                        View All
                      </Button>
                    </Box>
                    <Grid container spacing={2}>
                      {pendingApprovalsData.map((item) => (
                        <Grid item xs={6} sm={3} key={item.type}>
                          <Paper
                            elevation={0}
                            sx={{
                              p: 2,
                              textAlign: 'center',
                              borderRadius: 2,
                              bgcolor: 'background.default',
                              border: '1px solid',
                              borderColor: 'divider',
                            }}
                          >
                            <Avatar
                              sx={{
                                bgcolor: 'background.paper',
                                color: 'primary.main',
                                width: 40,
                                height: 40,
                                mb: 1,
                                mx: 'auto',
                              }}
                            >
                              {item.icon}
                            </Avatar>
                            <Typography variant="h5" component="div" sx={{ fontWeight: 700 }}>
                              {item.count}
                            </Typography>
                            <Typography variant="body2" color="textSecondary" noWrap>
                              {item.type}
                            </Typography>
                          </Paper>
                        </Grid>
                      ))}
                    </Grid>
                  </CardContent>
                </Card>
              </motion.div>
            </Grid>
            <Grid item xs={12}>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: 0.8 }}
              >
                <Card>
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                      <Typography variant="h6" component="h2">
                        Recent Activities
                      </Typography>
                      <Button variant="text" size="small" color="primary">
                        View All
                      </Button>
                    </Box>
                    <List>
                      {recentActivities.slice(0, 3).map((activity, index) => (
                        <React.Fragment key={activity.id}>
                          <ListItem alignItems="flex-start" sx={{ px: 0 }}>
                            <ListItemAvatar>
                              <Avatar alt={activity.user} src={activity.avatar} />
                            </ListItemAvatar>
                            <ListItemText
                              primary={activity.user}
                              secondary={
                                <React.Fragment>
                                  <Typography
                                    sx={{ display: 'inline' }}
                                    component="span"
                                    variant="body2"
                                    color="text.primary"
                                  >
                                    {activity.action}
                                  </Typography>
                                  {` — ${activity.time}`}
                                </React.Fragment>
                              }
                            />
                          </ListItem>
                          {index < 2 && <Divider variant="inset" component="li" />}
                        </React.Fragment>
                      ))}
                    </List>
                  </CardContent>
                </Card>
              </motion.div>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </Box>
  );
};

export default TenantAdminDashboard;