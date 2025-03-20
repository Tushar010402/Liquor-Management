import React, { useState } from 'react';
import {
  Box,
  Grid,
  Typography,
  Card,
  CardContent,
  Divider,
  Button,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  IconButton,
  Paper,
  useTheme,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import {
  LocalAtm,
  AccountBalance,
  CreditCard,
  ArrowUpward,
  ArrowDownward,
  Print,
  Share,
  Download,
  Receipt,
  MonetizationOn,
  Inventory,
  AssignmentReturn,
  CalendarToday,
  CheckCircle,
  Error,
} from '@mui/icons-material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
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
import { PageHeader, StatCard, ChartCard } from '../../../components/common';

// Mock data for sales summary
const salesSummaryData = {
  date: '2023-11-25',
  totalSales: 45000,
  totalItems: 78,
  totalTransactions: 32,
  cashSales: 20250,
  upiSales: 15750,
  cardSales: 9000,
  expenses: 4000,
  deposits: 40000,
  openingBalance: 15000,
  closingBalance: 15250,
  topSellingItems: [
    { id: 1, name: 'Johnnie Walker Black Label', quantity: 8, amount: 28000 },
    { id: 2, name: 'Absolut Vodka', quantity: 12, amount: 21600 },
    { id: 3, name: 'Jack Daniels', quantity: 6, amount: 16800 },
    { id: 4, name: 'Bacardi White Rum', quantity: 10, amount: 12000 },
    { id: 5, name: 'Beefeater Gin', quantity: 5, amount: 11000 },
  ],
  salesByHour: [
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
  ],
  paymentMethods: [
    { name: 'Cash', value: 45 },
    { name: 'UPI', value: 35 },
    { name: 'Card', value: 20 },
  ],
  transactions: [
    { id: 1, type: 'Sale', reference: 'INV-2023-1234', amount: 3500, method: 'Cash', time: '10:30 AM' },
    { id: 2, type: 'Sale', reference: 'INV-2023-1235', amount: 2800, method: 'UPI', time: '11:45 AM' },
    { id: 3, type: 'Sale', reference: 'INV-2023-1236', amount: 5200, method: 'Card', time: '12:20 PM' },
    { id: 4, type: 'Sale', reference: 'INV-2023-1237', amount: 1800, method: 'Cash', time: '01:10 PM' },
    { id: 5, type: 'Expense', reference: 'EXP-2023-056', amount: -500, method: 'Cash', time: '02:15 PM', category: 'Utilities' },
    { id: 6, type: 'Deposit', reference: 'DEP-2023-023', amount: -10000, method: 'Bank Transfer', time: '03:30 PM', bank: 'HDFC Bank' },
    { id: 7, type: 'Sale', reference: 'INV-2023-1238', amount: 4200, method: 'Cash', time: '04:45 PM' },
    { id: 8, type: 'Sale', reference: 'INV-2023-1239', amount: 3100, method: 'UPI', time: '05:30 PM' },
    { id: 9, type: 'Expense', reference: 'EXP-2023-057', amount: -800, method: 'Cash', time: '06:15 PM', category: 'Supplies' },
    { id: 10, type: 'Sale', reference: 'INV-2023-1240', amount: 2500, method: 'Cash', time: '07:20 PM' },
  ],
  stockAdjustments: [
    { id: 1, product: 'Johnnie Walker Black Label', type: 'decrease', quantity: 2, reason: 'Damaged' },
    { id: 2, product: 'Absolut Vodka', type: 'increase', quantity: 5, reason: 'Received from supplier' },
  ],
};

const COLORS = ['#4CAF50', '#2196F3', '#FF9800'];

const DailySummary: React.FC = () => {
  const theme = useTheme();
  const navigate = useNavigate();
  const [selectedDate, setSelectedDate] = useState<Date | null>(new Date());
  const [printDialogOpen, setPrintDialogOpen] = useState(false);

  const handleDateChange = (date: Date | null) => {
    setSelectedDate(date);
    // In a real app, this would fetch data for the selected date
  };

  const handlePrintDialogOpen = () => {
    setPrintDialogOpen(true);
  };

  const handlePrintDialogClose = () => {
    setPrintDialogOpen(false);
  };

  const handlePrintSummary = () => {
    // In a real app, this would generate and print the summary
    console.log('Printing summary for', selectedDate);
    handlePrintDialogClose();
    alert('Summary sent to printer!');
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Box>
        <PageHeader
          title="Daily Summary"
          subtitle="View and print daily sales and cash summary"
        />

        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={12} sm={6} md={4}>
                <DatePicker
                  label="Select Date"
                  value={selectedDate}
                  onChange={handleDateChange}
                  slotProps={{ textField: { fullWidth: true } }}
                />
              </Grid>
              <Grid item xs={12} sm={6} md={8}>
                <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
                  <Button
                    variant="outlined"
                    startIcon={<Download />}
                    onClick={() => {}}
                  >
                    Download PDF
                  </Button>
                  <Button
                    variant="outlined"
                    startIcon={<Share />}
                    onClick={() => {}}
                  >
                    Share
                  </Button>
                  <Button
                    variant="contained"
                    startIcon={<Print />}
                    onClick={handlePrintDialogOpen}
                  >
                    Print
                  </Button>
                </Box>
              </Grid>
            </Grid>
          </CardContent>
        </Card>

        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} sm={6} md={3}>
            <StatCard
              title="Total Sales"
              value={`₹${salesSummaryData.totalSales.toLocaleString()}`}
              icon={<Receipt />}
              trend={{ value: "32 transactions", isPositive: true, text: "" }}
              color="primary"
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <StatCard
              title="Cash Sales"
              value={`₹${salesSummaryData.cashSales.toLocaleString()}`}
              icon={<LocalAtm />}
              trend={{ value: "45% of total", isPositive: true, text: "" }}
              color="success"
              delay={0.1}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <StatCard
              title="UPI Sales"
              value={`₹${salesSummaryData.upiSales.toLocaleString()}`}
              icon={<CreditCard />}
              trend={{ value: "35% of total", isPositive: true, text: "" }}
              color="secondary"
              delay={0.2}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <StatCard
              title="Card Sales"
              value={`₹${salesSummaryData.cardSales.toLocaleString()}`}
              icon={<CreditCard />}
              trend={{ value: "20% of total", isPositive: true, text: "" }}
              color="info"
              delay={0.3}
            />
          </Grid>
        </Grid>

        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} md={8}>
            <ChartCard
              title="Sales by Hour"
              action="none"
              delay={0.4}
            >
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={salesSummaryData.salesByHour}
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
              action="none"
              delay={0.5}
            >
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={salesSummaryData.paymentMethods}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  >
                    {salesSummaryData.paymentMethods.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </ChartCard>
          </Grid>
        </Grid>

        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Top Selling Items
                </Typography>
                <TableContainer>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>Product</TableCell>
                        <TableCell align="center">Quantity</TableCell>
                        <TableCell align="right">Amount</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {salesSummaryData.topSellingItems.map((item) => (
                        <TableRow key={item.id}>
                          <TableCell>{item.name}</TableCell>
                          <TableCell align="center">{item.quantity}</TableCell>
                          <TableCell align="right">₹{item.amount.toLocaleString()}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Cash Summary
                </Typography>
                <List>
                  <ListItem sx={{ px: 0 }}>
                    <ListItemText primary="Opening Balance" />
                    <Typography variant="body1" sx={{ fontWeight: 500 }}>
                      ₹{salesSummaryData.openingBalance.toLocaleString()}
                    </Typography>
                  </ListItem>
                  <Divider component="li" />
                  <ListItem sx={{ px: 0 }}>
                    <ListItemText primary="Cash Sales" />
                    <Typography variant="body1" sx={{ fontWeight: 500, color: 'success.main' }}>
                      +₹{salesSummaryData.cashSales.toLocaleString()}
                    </Typography>
                  </ListItem>
                  <Divider component="li" />
                  <ListItem sx={{ px: 0 }}>
                    <ListItemText primary="Expenses" />
                    <Typography variant="body1" sx={{ fontWeight: 500, color: 'error.main' }}>
                      -₹{salesSummaryData.expenses.toLocaleString()}
                    </Typography>
                  </ListItem>
                  <Divider component="li" />
                  <ListItem sx={{ px: 0 }}>
                    <ListItemText primary="Deposits" />
                    <Typography variant="body1" sx={{ fontWeight: 500, color: 'error.main' }}>
                      -₹{salesSummaryData.deposits.toLocaleString()}
                    </Typography>
                  </ListItem>
                  <Divider component="li" />
                  <ListItem sx={{ px: 0, bgcolor: 'background.default', borderRadius: 1 }}>
                    <ListItemText 
                      primary={
                        <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                          Closing Balance
                        </Typography>
                      } 
                    />
                    <Typography variant="subtitle1" sx={{ fontWeight: 600, color: 'success.main' }}>
                      ₹{salesSummaryData.closingBalance.toLocaleString()}
                    </Typography>
                  </ListItem>
                </List>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Transactions
                </Typography>
                <TableContainer>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Time</TableCell>
                        <TableCell>Type</TableCell>
                        <TableCell>Reference</TableCell>
                        <TableCell>Method</TableCell>
                        <TableCell align="right">Amount</TableCell>
                        <TableCell>Details</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {salesSummaryData.transactions.map((transaction) => (
                        <TableRow key={transaction.id}>
                          <TableCell>{transaction.time}</TableCell>
                          <TableCell>
                            <Chip 
                              label={transaction.type} 
                              size="small" 
                              color={
                                transaction.type === 'Sale' ? 'primary' : 
                                transaction.type === 'Expense' ? 'error' : 
                                'info'
                              }
                            />
                          </TableCell>
                          <TableCell>{transaction.reference}</TableCell>
                          <TableCell>{transaction.method}</TableCell>
                          <TableCell align="right">
                            <Typography 
                              variant="body2" 
                              sx={{ 
                                fontWeight: 500, 
                                color: transaction.amount < 0 ? 'error.main' : 'success.main',
                              }}
                            >
                              {transaction.amount < 0 ? '-' : ''}₹{Math.abs(transaction.amount).toLocaleString()}
                            </Typography>
                          </TableCell>
                          <TableCell>
                            {transaction.category && `Category: ${transaction.category}`}
                            {transaction.bank && `Bank: ${transaction.bank}`}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Stock Adjustments
                </Typography>
                {salesSummaryData.stockAdjustments.length > 0 ? (
                  <TableContainer>
                    <Table>
                      <TableHead>
                        <TableRow>
                          <TableCell>Product</TableCell>
                          <TableCell>Type</TableCell>
                          <TableCell align="center">Quantity</TableCell>
                          <TableCell>Reason</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {salesSummaryData.stockAdjustments.map((adjustment) => (
                          <TableRow key={adjustment.id}>
                            <TableCell>{adjustment.product}</TableCell>
                            <TableCell>
                              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                {adjustment.type === 'increase' ? (
                                  <>
                                    <ArrowUpward fontSize="small" sx={{ color: 'success.main', mr: 0.5 }} />
                                    <Typography variant="body2" color="success.main">
                                      Increase
                                    </Typography>
                                  </>
                                ) : (
                                  <>
                                    <ArrowDownward fontSize="small" sx={{ color: 'error.main', mr: 0.5 }} />
                                    <Typography variant="body2" color="error.main">
                                      Decrease
                                    </Typography>
                                  </>
                                )}
                              </Box>
                            </TableCell>
                            <TableCell align="center">{adjustment.quantity}</TableCell>
                            <TableCell>{adjustment.reason}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                ) : (
                  <Box sx={{ p: 2, textAlign: 'center' }}>
                    <Typography variant="body1" color="textSecondary">
                      No stock adjustments recorded for this day
                    </Typography>
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Print Dialog */}
        <Dialog open={printDialogOpen} onClose={handlePrintDialogClose} maxWidth="sm" fullWidth>
          <DialogTitle>Print Daily Summary</DialogTitle>
          <DialogContent>
            <Typography variant="body1" gutterBottom>
              You are about to print the daily summary for:
            </Typography>
            <Typography variant="h6" gutterBottom>
              {selectedDate?.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
            </Typography>
            <Typography variant="body2" color="textSecondary" paragraph>
              This will print a complete summary of all transactions, sales, and cash movements for the selected date.
            </Typography>
            <Box sx={{ mt: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                Summary includes:
              </Typography>
              <List dense>
                <ListItem>
                  <ListItemIcon>
                    <CheckCircle fontSize="small" color="success" />
                  </ListItemIcon>
                  <ListItemText primary="Sales summary by payment method" />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <CheckCircle fontSize="small" color="success" />
                  </ListItemIcon>
                  <ListItemText primary="Cash flow details" />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <CheckCircle fontSize="small" color="success" />
                  </ListItemIcon>
                  <ListItemText primary="Top selling products" />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <CheckCircle fontSize="small" color="success" />
                  </ListItemIcon>
                  <ListItemText primary="All transactions with details" />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <CheckCircle fontSize="small" color="success" />
                  </ListItemIcon>
                  <ListItemText primary="Stock adjustments" />
                </ListItem>
              </List>
            </Box>
          </DialogContent>
          <DialogActions>
            <Button onClick={handlePrintDialogClose}>Cancel</Button>
            <Button 
              onClick={handlePrintSummary} 
              variant="contained" 
              color="primary"
              startIcon={<Print />}
            >
              Print Summary
            </Button>
          </DialogActions>
        </Dialog>
      </Box>
    </LocalizationProvider>
  );
};

export default DailySummary;