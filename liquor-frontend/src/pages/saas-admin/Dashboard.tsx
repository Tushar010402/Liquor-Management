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
  useTheme,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  Business,
  People,
  Storage,
  Warning,
  MoreVert,
  ArrowUpward,
  ArrowDownward,
  CheckCircle,
  Error,
  Add,
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
} from 'recharts';

// Mock data for charts
const tenantGrowthData = [
  { month: 'Jan', tenants: 12 },
  { month: 'Feb', tenants: 19 },
  { month: 'Mar', tenants: 25 },
  { month: 'Apr', tenants: 32 },
  { month: 'May', tenants: 38 },
  { month: 'Jun', tenants: 42 },
  { month: 'Jul', tenants: 47 },
  { month: 'Aug', tenants: 53 },
  { month: 'Sep', tenants: 60 },
  { month: 'Oct', tenants: 68 },
  { month: 'Nov', tenants: 75 },
  { month: 'Dec', tenants: 82 },
];

const apiUsageData = [
  { name: 'Mon', calls: 4000 },
  { name: 'Tue', calls: 3000 },
  { name: 'Wed', calls: 5000 },
  { name: 'Thu', calls: 2780 },
  { name: 'Fri', calls: 1890 },
  { name: 'Sat', calls: 2390 },
  { name: 'Sun', calls: 3490 },
];

const revenueData = [
  { name: 'Jan', revenue: 4000 },
  { name: 'Feb', revenue: 5000 },
  { name: 'Mar', revenue: 6000 },
  { name: 'Apr', revenue: 7000 },
  { name: 'May', revenue: 8500 },
  { name: 'Jun', revenue: 9800 },
  { name: 'Jul', revenue: 11000 },
  { name: 'Aug', revenue: 12500 },
  { name: 'Sep', revenue: 14000 },
  { name: 'Oct', revenue: 16000 },
  { name: 'Nov', revenue: 18000 },
  { name: 'Dec', revenue: 21000 },
];

const planDistributionData = [
  { name: 'Basic', value: 30 },
  { name: 'Standard', value: 45 },
  { name: 'Premium', value: 25 },
];

const COLORS = ['#0088FE', '#00C49F', '#FFBB28'];

const systemHealthData = [
  { name: 'Database', status: 'Healthy', uptime: '99.99%', icon: <CheckCircle color="success" /> },
  { name: 'API Gateway', status: 'Healthy', uptime: '99.95%', icon: <CheckCircle color="success" /> },
  { name: 'Auth Service', status: 'Healthy', uptime: '99.98%', icon: <CheckCircle color="success" /> },
  { name: 'Storage', status: 'Warning', uptime: '99.90%', icon: <Warning color="warning" /> },
  { name: 'Cache', status: 'Healthy', uptime: '99.97%', icon: <CheckCircle color="success" /> },
];

const recentActivities = [
  { id: 1, user: 'John Doe', action: 'Created a new tenant', time: '5 minutes ago', avatar: '/static/images/avatar/1.jpg' },
  { id: 2, user: 'Jane Smith', action: 'Updated billing plan', time: '30 minutes ago', avatar: '/static/images/avatar/2.jpg' },
  { id: 3, user: 'Mike Johnson', action: 'Added team member', time: '1 hour ago', avatar: '/static/images/avatar/3.jpg' },
  { id: 4, user: 'Sarah Williams', action: 'System backup completed', time: '2 hours ago', avatar: '/static/images/avatar/4.jpg' },
  { id: 5, user: 'David Brown', action: 'Updated system settings', time: '3 hours ago', avatar: '/static/images/avatar/5.jpg' },
];

const SaasAdminDashboard: React.FC = () => {
  const theme = useTheme();

  return (
    <Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 700 }}>
          SaaS Admin Dashboard
        </Typography>
        <Typography variant="subtitle1" color="textSecondary">
          Welcome back! Here's what's happening with your platform today.
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
                    Total Tenants
                  </Typography>
                  <Avatar sx={{ bgcolor: 'primary.light' }}>
                    <Business />
                  </Avatar>
                </Box>
                <Typography variant="h4" component="div" sx={{ fontWeight: 700 }}>
                  82
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                  <ArrowUpward fontSize="small" color="success" />
                  <Typography variant="body2" color="success.main" sx={{ ml: 0.5 }}>
                    12% increase
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
            transition={{ duration: 0.3, delay: 0.1 }}
          >
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                  <Typography variant="subtitle2" color="textSecondary">
                    New Registrations
                  </Typography>
                  <Avatar sx={{ bgcolor: 'secondary.light' }}>
                    <People />
                  </Avatar>
                </Box>
                <Typography variant="h4" component="div" sx={{ fontWeight: 700 }}>
                  24
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
                    Monthly Revenue
                  </Typography>
                  <Avatar sx={{ bgcolor: 'success.light' }}>
                    <TrendingUp />
                  </Avatar>
                </Box>
                <Typography variant="h4" component="div" sx={{ fontWeight: 700 }}>
                  $21,000
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                  <ArrowUpward fontSize="small" color="success" />
                  <Typography variant="body2" color="success.main" sx={{ ml: 0.5 }}>
                    15% increase
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
                    System Health
                  </Typography>
                  <Avatar sx={{ bgcolor: 'warning.light' }}>
                    <Storage />
                  </Avatar>
                </Box>
                <Typography variant="h4" component="div" sx={{ fontWeight: 700 }}>
                  98.5%
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                  <ArrowDownward fontSize="small" color="error" />
                  <Typography variant="body2" color="error.main" sx={{ ml: 0.5 }}>
                    0.5% decrease
                  </Typography>
                  <Typography variant="body2" color="textSecondary" sx={{ ml: 1 }}>
                    vs last week
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
                    Tenant Growth
                  </Typography>
                  <Button variant="outlined" size="small">
                    View Details
                  </Button>
                </Box>
                <Box sx={{ height: 300 }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart
                      data={tenantGrowthData}
                      margin={{
                        top: 5,
                        right: 30,
                        left: 20,
                        bottom: 5,
                      }}
                    >
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="month" />
                      <YAxis />
                      <Tooltip />
                      <Area type="monotone" dataKey="tenants" stroke={theme.palette.primary.main} fill={theme.palette.primary.light} />
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
                    Plan Distribution
                  </Typography>
                  <IconButton size="small">
                    <MoreVert fontSize="small" />
                  </IconButton>
                </Box>
                <Box sx={{ height: 250, display: 'flex', justifyContent: 'center' }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={planDistributionData}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                        label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                      >
                        {planDistributionData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </Box>
                <Divider sx={{ my: 2 }} />
                <Grid container spacing={2}>
                  {planDistributionData.map((plan, index) => (
                    <Grid item xs={4} key={plan.name}>
                      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                        <Box
                          sx={{
                            width: 12,
                            height: 12,
                            borderRadius: '50%',
                            bgcolor: COLORS[index % COLORS.length],
                            mb: 0.5,
                          }}
                        />
                        <Typography variant="body2" align="center">
                          {plan.name}
                        </Typography>
                        <Typography variant="subtitle2" align="center" sx={{ fontWeight: 600 }}>
                          {plan.value}%
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
                    System Health Status
                  </Typography>
                  <Button variant="text" size="small" color="primary">
                    View All
                  </Button>
                </Box>
                <List>
                  {systemHealthData.map((item, index) => (
                    <React.Fragment key={item.name}>
                      <ListItem
                        secondaryAction={
                          <Typography variant="body2" color="textSecondary">
                            {item.uptime}
                          </Typography>
                        }
                      >
                        <ListItemAvatar>
                          <Avatar
                            sx={{
                              bgcolor: item.status === 'Healthy' ? 'success.light' : 'warning.light',
                              color: 'white',
                            }}
                          >
                            {item.icon}
                          </Avatar>
                        </ListItemAvatar>
                        <ListItemText
                          primary={item.name}
                          secondary={item.status}
                          primaryTypographyProps={{ fontWeight: 500 }}
                          secondaryTypographyProps={{
                            color: item.status === 'Healthy' ? 'success.main' : 'warning.main',
                          }}
                        />
                      </ListItem>
                      {index < systemHealthData.length - 1 && <Divider variant="inset" component="li" />}
                    </React.Fragment>
                  ))}
                </List>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        <Grid item xs={12} md={6}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.7 }}
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
                  {recentActivities.map((activity, index) => (
                    <React.Fragment key={activity.id}>
                      <ListItem alignItems="flex-start">
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
                      {index < recentActivities.length - 1 && <Divider variant="inset" component="li" />}
                    </React.Fragment>
                  ))}
                </List>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>
      </Grid>
    </Box>
  );
};

export default SaasAdminDashboard;