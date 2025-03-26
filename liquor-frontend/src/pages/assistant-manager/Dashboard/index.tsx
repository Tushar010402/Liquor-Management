import React from 'react';
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
  useTheme,
} from '@mui/material';
import {
  Store,
  Inventory,
  Receipt,
  AssignmentReturn,
  Warning,
  LocalShipping,
  Approval,
  TrendingUp,
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
  PieChart,
  Pie,
  Cell,
  Legend,
} from 'recharts';
import { useNavigate } from 'react-router-dom';
import { StatCard, ChartCard, ActivityList, PageHeader } from '../../../components/common';

// Mock data for charts
const dailySalesData = [
  { name: 'Mon', sales: 12000 },
  { name: 'Tue', sales: 19000 },
  { name: 'Wed', sales: 15000 },
  { name: 'Thu', sales: 21000 },
  { name: 'Fri', sales: 25000 },
  { name: 'Sat', sales: 32000 },
  { name: 'Sun', sales: 28000 },
];

const inventoryStatusData = [
  { name: 'In Stock', value: 65 },
  { name: 'Low Stock', value: 25 },
  { name: 'Out of Stock', value: 10 },
];

const COLORS = ['#4CAF50', '#FFC107', '#F44336'];

const pendingApprovalsData = [
  { id: 1, type: 'Sale', number: 'S-2023-1234', amount: '₹12,500', status: 'Pending', time: '10 minutes ago' },
  { id: 2, type: 'Stock Adjustment', number: 'ADJ-2023-567', items: '15 items', status: 'Pending', time: '30 minutes ago' },
  { id: 3, type: 'Return', number: 'R-2023-089', amount: '₹5,200', status: 'Pending', time: '1 hour ago' },
];

const lowStockItemsData = [
  { id: 1, name: 'Johnnie Walker Black Label', current: 5, minimum: 10, status: 'Low' },
  { id: 2, name: 'Absolut Vodka', current: 3, minimum: 12, status: 'Low' },
  { id: 3, name: 'Jack Daniels', current: 2, minimum: 8, status: 'Low' },
];

const purchaseOrdersData = [
  { id: 1, number: 'PO-2023-456', supplier: 'ABC Distributors', items: 12, status: 'Pending', date: '2023-11-25' },
  { id: 2, number: 'PO-2023-457', supplier: 'XYZ Beverages', items: 8, status: 'Approved', date: '2023-11-24' },
  { id: 3, number: 'PO-2023-458', supplier: 'Premium Spirits', items: 15, status: 'Shipped', date: '2023-11-23' },
];

const recentActivities = [
  { id: 1, user: 'John Doe', action: 'Approved sale #12345', time: '5 minutes ago', avatar: '/static/images/avatar/1.jpg' },
  { id: 2, user: 'Jane Smith', action: 'Created purchase order #789', time: '30 minutes ago', avatar: '/static/images/avatar/2.jpg' },
  { id: 3, user: 'Mike Johnson', action: 'Updated inventory count', time: '1 hour ago', avatar: '/static/images/avatar/3.jpg' },
  { id: 4, user: 'Sarah Williams', action: 'Processed return #456', time: '2 hours ago', avatar: '/static/images/avatar/4.jpg' },
];

const AssistantManagerDashboard: React.FC = () => {
  const theme = useTheme();
  const navigate = useNavigate();

  return (
    <Box>
      <PageHeader
        title="Assistant Manager Dashboard"
        subtitle="Welcome back! Here's what's happening in your shop today."
      />

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
            title="Pending Approvals"
            value="18"
            icon={<Approval />}
            trend={{ value: "3 new", isPositive: false, text: "since yesterday" }}
            color="warning"
            delay={0.1}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Low Stock Items"
            value="12"
            icon={<Inventory />}
            trend={{ value: "2 critical", isPositive: false, text: "need attention" }}
            color="error"
            delay={0.2}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Purchase Orders"
            value="6"
            icon={<LocalShipping />}
            trend={{ value: "1 received", isPositive: true, text: "today" }}
            color="success"
            delay={0.3}
          />
        </Grid>
      </Grid>

      {/* Charts */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={8}>
          <ChartCard
            title="Daily Sales"
            action="button"
            actionText="View Details"
            onActionClick={() => navigate('/assistant-manager/sales-analytics')}
            delay={0.4}
          >
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={dailySalesData}
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
                <Tooltip 
                  formatter={(value) => [`₹${value}`, 'Sales']}
                  labelFormatter={(label) => `Day: ${label}`}
                />
                <Bar dataKey="sales" fill={theme.palette.primary.main} />
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>
        </Grid>

        <Grid item xs={12} md={4}>
          <ChartCard
            title="Inventory Status"
            action="button"
            actionText="View Inventory"
            onActionClick={() => navigate('/assistant-manager/stock-levels')}
            delay={0.5}
          >
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={inventoryStatusData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                >
                  {inventoryStatusData.map((entry, index) => (
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
                  Pending Approvals
                </Typography>
                <Button 
                  variant="text" 
                  size="small" 
                  color="primary"
                  onClick={() => navigate('/assistant-manager/sales-approvals')}
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
                      onClick={() => {
                        if (item.type === 'Sale') navigate('/assistant-manager/sales-approvals');
                        else if (item.type === 'Stock Adjustment') navigate('/assistant-manager/adjustment-approvals');
                        else if (item.type === 'Return') navigate('/assistant-manager/return-approvals');
                      }}
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
                              color={item.status === 'Pending' ? 'warning' : 'success'}
                              sx={{ ml: 1 }}
                            />
                          </Box>
                        }
                        secondary={
                          <Typography variant="body2" color="textSecondary">
                            {item.amount || item.items} • {item.time}
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

        <Grid item xs={12} md={6}>
          <ActivityList
            title="Recent Activities"
            activities={recentActivities}
            actionText="View All"
            onActionClick={() => {}}
            maxItems={4}
            delay={0.6}
          />
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6" component="h2">
                  Low Stock Items
                </Typography>
                <Button 
                  variant="text" 
                  size="small" 
                  color="primary"
                  onClick={() => navigate('/assistant-manager/stock-levels')}
                >
                  View All
                </Button>
              </Box>
              <List>
                {lowStockItemsData.map((item, index) => (
                  <React.Fragment key={item.id}>
                    <ListItem 
                      sx={{ 
                        px: 2, 
                        py: 1.5, 
                        borderRadius: 1,
                        '&:hover': {
                          bgcolor: 'background.default',
                        },
                      }}
                    >
                      <ListItemIcon>
                        {item.status === 'Out' ? (
                          <Warning color="error" />
                        ) : (
                          <Warning color="warning" />
                        )}
                      </ListItemIcon>
                      <ListItemText
                        primary={
                          <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            <Typography variant="body1" sx={{ fontWeight: 500 }}>
                              {item.name}
                            </Typography>
                            <Chip 
                              label={item.status === 'Out' ? 'Out of Stock' : 'Low Stock'} 
                              size="small" 
                              color={item.status === 'Out' ? 'error' : 'warning'}
                              sx={{ ml: 1 }}
                            />
                          </Box>
                        }
                        secondary={
                          <Typography variant="body2" color="textSecondary">
                            Current: {item.current} • Minimum: {item.minimum}
                          </Typography>
                        }
                      />
                      <Button 
                        variant="outlined" 
                        size="small"
                        onClick={() => navigate('/assistant-manager/create-purchase-order')}
                      >
                        Order
                      </Button>
                    </ListItem>
                    {index < lowStockItemsData.length - 1 && <Divider component="li" />}
                  </React.Fragment>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6" component="h2">
                  Purchase Orders
                </Typography>
                <Button 
                  variant="text" 
                  size="small" 
                  color="primary"
                  onClick={() => navigate('/assistant-manager/track-purchase-orders')}
                >
                  View All
                </Button>
              </Box>
              <List>
                {purchaseOrdersData.map((item, index) => (
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
                      onClick={() => navigate('/assistant-manager/track-purchase-orders')}
                    >
                      <ListItemIcon>
                        <LocalShipping color="primary" />
                      </ListItemIcon>
                      <ListItemText
                        primary={
                          <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            <Typography variant="body1" sx={{ fontWeight: 500 }}>
                              {item.number}
                            </Typography>
                            <Chip 
                              label={item.status} 
                              size="small" 
                              color={
                                item.status === 'Pending' ? 'warning' : 
                                item.status === 'Approved' ? 'info' : 
                                'success'
                              }
                              sx={{ ml: 1 }}
                            />
                          </Box>
                        }
                        secondary={
                          <Typography variant="body2" color="textSecondary">
                            {item.supplier} • {item.items} items • {item.date}
                          </Typography>
                        }
                      />
                    </ListItem>
                    {index < purchaseOrdersData.length - 1 && <Divider component="li" />}
                  </React.Fragment>
                ))}
              </List>
              <Box sx={{ mt: 2, display: 'flex', justifyContent: 'center' }}>
                <Button 
                  variant="contained" 
                  color="primary"
                  startIcon={<Add />}
                  onClick={() => navigate('/assistant-manager/create-purchase-order')}
                >
                  Create Purchase Order
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default AssistantManagerDashboard;