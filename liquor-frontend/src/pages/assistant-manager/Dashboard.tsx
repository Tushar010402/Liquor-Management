import React, { useState } from 'react';
import {
  Box,
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  IconButton,
  Chip,
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
  Inventory as InventoryIcon,
  ShoppingCart as ShoppingCartIcon,
  LocalShipping as LocalShippingIcon,
  Approval as ApprovalIcon,
  Warning as WarningIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Visibility as VisibilityIcon,
  CheckCircle as CheckCircleIcon,
  Cancel as CancelIcon,
  Person as PersonIcon,
  CalendarToday as CalendarTodayIcon,
} from '@mui/icons-material';
import { PageHeader } from '../../components/common';
import { useTranslations } from '../../hooks';

// Mock data for pending approvals
const mockPendingApprovals = [
  {
    id: 1,
    type: 'sale',
    title: 'Sale #INV-2023-0045',
    amount: 3500,
    submitted_by: 'John Doe',
    submitted_at: '2023-06-15 14:30',
    status: 'pending',
  },
  {
    id: 2,
    type: 'adjustment',
    title: 'Stock Adjustment #ADJ-2023-0032',
    items: 5,
    submitted_by: 'Jane Smith',
    submitted_at: '2023-06-15 15:45',
    status: 'pending',
  },
  {
    id: 3,
    type: 'return',
    title: 'Return #RET-2023-0012',
    amount: 1200,
    submitted_by: 'Michael Wilson',
    submitted_at: '2023-06-15 16:20',
    status: 'pending',
  },
];

// Mock data for low stock items
const mockLowStockItems = [
  {
    id: 1,
    name: 'Jack Daniels Whiskey',
    category: 'Whiskey',
    current_stock: 5,
    threshold: 10,
    status: 'low',
  },
  {
    id: 2,
    name: 'Absolut Vodka',
    category: 'Vodka',
    current_stock: 3,
    threshold: 8,
    status: 'low',
  },
  {
    id: 3,
    name: 'Corona Beer (6-pack)',
    category: 'Beer',
    current_stock: 2,
    threshold: 12,
    status: 'critical',
  },
  {
    id: 4,
    name: 'Johnnie Walker Black Label',
    category: 'Whiskey',
    current_stock: 4,
    threshold: 6,
    status: 'low',
  },
];

// Mock data for purchase orders
const mockPurchaseOrders = [
  {
    id: 1,
    po_number: 'PO-2023-0025',
    supplier: 'ABC Distributors',
    items: 8,
    total: 25000,
    status: 'pending',
    created_at: '2023-06-14',
  },
  {
    id: 2,
    po_number: 'PO-2023-0024',
    supplier: 'XYZ Beverages',
    items: 5,
    total: 18000,
    status: 'approved',
    created_at: '2023-06-13',
  },
  {
    id: 3,
    po_number: 'PO-2023-0023',
    supplier: 'Premium Spirits Inc.',
    items: 3,
    total: 12000,
    status: 'received',
    created_at: '2023-06-12',
  },
];

// Mock data for recent activities
const mockRecentActivities = [
  {
    id: 1,
    action: 'Approved sale',
    details: 'Sale #INV-2023-0044 for ₹4,200',
    user: 'You',
    timestamp: '30 minutes ago',
  },
  {
    id: 2,
    action: 'Created purchase order',
    details: 'PO-2023-0025 for ABC Distributors',
    user: 'You',
    timestamp: '2 hours ago',
  },
  {
    id: 3,
    action: 'Rejected stock adjustment',
    details: 'Adjustment #ADJ-2023-0031',
    user: 'You',
    timestamp: '3 hours ago',
  },
  {
    id: 4,
    action: 'Updated inventory',
    details: 'Added 24 items to stock',
    user: 'Jane Smith',
    timestamp: '5 hours ago',
  },
];

/**
 * Assistant Manager Dashboard component
 */
const Dashboard: React.FC = () => {
  const { common, dashboard } = useTranslations();
  const theme = useTheme();

  return (
    <Container maxWidth="xl">
      <PageHeader
        title={dashboard('assistantManagerDashboard')}
        subtitle={dashboard('welcomeBack')}
        icon={<PersonIcon fontSize="large" />}
      />

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Avatar sx={{ bgcolor: theme.palette.primary.main, mr: 2 }}>
                  <ApprovalIcon />
                </Avatar>
                <Typography variant="h6" component="div">
                  {dashboard('pendingApprovals')}
                </Typography>
              </Box>
              <Typography variant="h3" component="div" color="primary.main" gutterBottom>
                3
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <TrendingDownIcon color="success" fontSize="small" sx={{ mr: 0.5 }} />
                <Typography variant="body2" color="text.secondary">
                  {dashboard('downFromYesterday')}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Avatar sx={{ bgcolor: theme.palette.warning.main, mr: 2 }}>
                  <InventoryIcon />
                </Avatar>
                <Typography variant="h6" component="div">
                  {dashboard('lowStockItems')}
                </Typography>
              </Box>
              <Typography variant="h3" component="div" color="warning.main" gutterBottom>
                4
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <TrendingUpIcon color="error" fontSize="small" sx={{ mr: 0.5 }} />
                <Typography variant="body2" color="text.secondary">
                  {dashboard('upFromYesterday')}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Avatar sx={{ bgcolor: theme.palette.success.main, mr: 2 }}>
                  <ShoppingCartIcon />
                </Avatar>
                <Typography variant="h6" component="div">
                  {dashboard('todaySales')}
                </Typography>
              </Box>
              <Typography variant="h3" component="div" color="success.main" gutterBottom>
                ₹15,200
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <TrendingUpIcon color="success" fontSize="small" sx={{ mr: 0.5 }} />
                <Typography variant="body2" color="text.secondary">
                  {dashboard('upFromYesterday')}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Avatar sx={{ bgcolor: theme.palette.info.main, mr: 2 }}>
                  <LocalShippingIcon />
                </Avatar>
                <Typography variant="h6" component="div">
                  {dashboard('pendingOrders')}
                </Typography>
              </Box>
              <Typography variant="h3" component="div" color="info.main" gutterBottom>
                1
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <TrendingDownIcon color="success" fontSize="small" sx={{ mr: 0.5 }} />
                <Typography variant="body2" color="text.secondary">
                  {dashboard('downFromYesterday')}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Main Content */}
      <Grid container spacing={3}>
        {/* Pending Approvals */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6" component="div">
                  {dashboard('pendingApprovals')}
                </Typography>
                <Button
                  variant="outlined"
                  size="small"
                  onClick={() => console.log('View all approvals')}
                >
                  {common('viewAll')}
                </Button>
              </Box>
              <Divider sx={{ mb: 2 }} />
              <List disablePadding>
                {mockPendingApprovals.map((approval) => (
                  <ListItem
                    key={approval.id}
                    secondaryAction={
                      <Box>
                        <IconButton
                          edge="end"
                          aria-label="approve"
                          color="success"
                          onClick={() => console.log('Approve', approval.id)}
                        >
                          <CheckCircleIcon />
                        </IconButton>
                        <IconButton
                          edge="end"
                          aria-label="reject"
                          color="error"
                          onClick={() => console.log('Reject', approval.id)}
                        >
                          <CancelIcon />
                        </IconButton>
                      </Box>
                    }
                    sx={{ py: 1.5 }}
                  >
                    <ListItemAvatar>
                      <Avatar
                        sx={{
                          bgcolor:
                            approval.type === 'sale'
                              ? theme.palette.success.main
                              : approval.type === 'adjustment'
                              ? theme.palette.warning.main
                              : theme.palette.error.main,
                        }}
                      >
                        {approval.type === 'sale' ? (
                          <ShoppingCartIcon />
                        ) : approval.type === 'adjustment' ? (
                          <InventoryIcon />
                        ) : (
                          <LocalShippingIcon />
                        )}
                      </Avatar>
                    </ListItemAvatar>
                    <ListItemText
                      primary={approval.title}
                      secondary={
                        <>
                          <Typography variant="body2" component="span">
                            {approval.submitted_by} • {approval.submitted_at}
                          </Typography>
                          <br />
                          <Typography variant="body2" component="span" fontWeight={500}>
                            {approval.amount
                              ? `₹${approval.amount.toLocaleString()}`
                              : `${approval.items} items`}
                          </Typography>
                        </>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Low Stock Items */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6" component="div">
                  {dashboard('lowStockItems')}
                </Typography>
                <Button
                  variant="outlined"
                  size="small"
                  onClick={() => console.log('View all low stock items')}
                >
                  {common('viewAll')}
                </Button>
              </Box>
              <Divider sx={{ mb: 2 }} />
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>{common('product')}</TableCell>
                      <TableCell>{common('category')}</TableCell>
                      <TableCell align="center">{common('stock')}</TableCell>
                      <TableCell align="center">{common('status')}</TableCell>
                      <TableCell align="right">{common('actions')}</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {mockLowStockItems.map((item) => (
                      <TableRow key={item.id}>
                        <TableCell>{item.name}</TableCell>
                        <TableCell>{item.category}</TableCell>
                        <TableCell align="center">
                          {item.current_stock} / {item.threshold}
                        </TableCell>
                        <TableCell align="center">
                          <Chip
                            label={item.status === 'critical' ? common('critical') : common('low')}
                            color={item.status === 'critical' ? 'error' : 'warning'}
                            size="small"
                          />
                        </TableCell>
                        <TableCell align="right">
                          <Button
                            variant="text"
                            size="small"
                            onClick={() => console.log('Create purchase order', item.id)}
                          >
                            {dashboard('createPO')}
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Purchase Orders */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6" component="div">
                  {dashboard('recentPurchaseOrders')}
                </Typography>
                <Button
                  variant="outlined"
                  size="small"
                  onClick={() => console.log('View all purchase orders')}
                >
                  {common('viewAll')}
                </Button>
              </Box>
              <Divider sx={{ mb: 2 }} />
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>{dashboard('poNumber')}</TableCell>
                      <TableCell>{common('supplier')}</TableCell>
                      <TableCell align="right">{common('total')}</TableCell>
                      <TableCell align="center">{common('status')}</TableCell>
                      <TableCell align="right">{common('actions')}</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {mockPurchaseOrders.map((order) => (
                      <TableRow key={order.id}>
                        <TableCell>
                          <Box sx={{ display: 'flex', flexDirection: 'column' }}>
                            <Typography variant="body2" fontWeight={500}>
                              {order.po_number}
                            </Typography>
                            <Typography variant="caption" color="textSecondary">
                              {order.created_at}
                            </Typography>
                          </Box>
                        </TableCell>
                        <TableCell>{order.supplier}</TableCell>
                        <TableCell align="right">₹{order.total.toLocaleString()}</TableCell>
                        <TableCell align="center">
                          <Chip
                            label={
                              order.status === 'pending'
                                ? common('pending')
                                : order.status === 'approved'
                                ? common('approved')
                                : common('received')
                            }
                            color={
                              order.status === 'pending'
                                ? 'warning'
                                : order.status === 'approved'
                                ? 'info'
                                : 'success'
                            }
                            size="small"
                          />
                        </TableCell>
                        <TableCell align="right">
                          <IconButton
                            size="small"
                            onClick={() => console.log('View purchase order', order.id)}
                          >
                            <VisibilityIcon fontSize="small" />
                          </IconButton>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Activities */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6" component="div">
                  {dashboard('recentActivities')}
                </Typography>
              </Box>
              <Divider sx={{ mb: 2 }} />
              <List disablePadding>
                {mockRecentActivities.map((activity) => (
                  <ListItem key={activity.id} sx={{ py: 1 }}>
                    <ListItemAvatar>
                      <Avatar
                        sx={{
                          bgcolor:
                            activity.action.includes('Approved')
                              ? theme.palette.success.main
                              : activity.action.includes('Rejected')
                              ? theme.palette.error.main
                              : activity.action.includes('Created')
                              ? theme.palette.info.main
                              : theme.palette.warning.main,
                        }}
                      >
                        {activity.action.includes('Approved') ? (
                          <CheckCircleIcon />
                        ) : activity.action.includes('Rejected') ? (
                          <CancelIcon />
                        ) : activity.action.includes('Created') ? (
                          <LocalShippingIcon />
                        ) : (
                          <InventoryIcon />
                        )}
                      </Avatar>
                    </ListItemAvatar>
                    <ListItemText
                      primary={
                        <Typography variant="body2" fontWeight={500}>
                          {activity.action}
                        </Typography>
                      }
                      secondary={
                        <>
                          <Typography variant="body2" component="span">
                            {activity.details}
                          </Typography>
                          <br />
                          <Typography variant="caption" color="textSecondary">
                            {activity.user} • {activity.timestamp}
                          </Typography>
                        </>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;