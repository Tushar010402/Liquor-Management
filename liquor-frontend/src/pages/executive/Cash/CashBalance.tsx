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
  Tab,
  Tabs,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  InputAdornment,
} from '@mui/material';
import {
  LocalAtm,
  AccountBalance,
  CreditCard,
  ArrowUpward,
  ArrowDownward,
  Add,
  Receipt,
  MonetizationOn,
  Visibility,
  Print,
  CalendarToday,
  AttachMoney,
  ReceiptLong,
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
  LineChart,
  Line,
} from 'recharts';
import { PageHeader, StatCard, ChartCard } from '../../../components/common';

// Mock data for cash transactions
const cashTransactionsData = [
  { id: 1, type: 'Sale', reference: 'INV-2023-1234', amount: 3500, method: 'Cash', time: '10:30 AM', date: '2023-11-25' },
  { id: 2, type: 'Sale', reference: 'INV-2023-1235', amount: 2800, method: 'UPI', time: '11:45 AM', date: '2023-11-25' },
  { id: 3, type: 'Sale', reference: 'INV-2023-1236', amount: 5200, method: 'Card', time: '12:20 PM', date: '2023-11-25' },
  { id: 4, type: 'Sale', reference: 'INV-2023-1237', amount: 1800, method: 'Cash', time: '01:10 PM', date: '2023-11-25' },
  { id: 5, type: 'Expense', reference: 'EXP-2023-056', amount: -500, method: 'Cash', time: '02:15 PM', date: '2023-11-25', category: 'Utilities' },
  { id: 6, type: 'Deposit', reference: 'DEP-2023-023', amount: -10000, method: 'Bank Transfer', time: '03:30 PM', date: '2023-11-25', bank: 'HDFC Bank' },
  { id: 7, type: 'Sale', reference: 'INV-2023-1238', amount: 4200, method: 'Cash', time: '04:45 PM', date: '2023-11-25' },
  { id: 8, type: 'Sale', reference: 'INV-2023-1239', amount: 3100, method: 'UPI', time: '05:30 PM', date: '2023-11-25' },
  { id: 9, type: 'Expense', reference: 'EXP-2023-057', amount: -800, method: 'Cash', time: '06:15 PM', date: '2023-11-25', category: 'Supplies' },
  { id: 10, type: 'Sale', reference: 'INV-2023-1240', amount: 2500, method: 'Cash', time: '07:20 PM', date: '2023-11-25' },
];

// Mock data for cash flow chart
const cashFlowData = [
  { date: '11/19', sales: 32000, expenses: 2500, deposits: 25000 },
  { date: '11/20', sales: 28000, expenses: 1800, deposits: 20000 },
  { date: '11/21', sales: 35000, expenses: 3200, deposits: 30000 },
  { date: '11/22', sales: 30000, expenses: 2200, deposits: 25000 },
  { date: '11/23', sales: 38000, expenses: 2800, deposits: 30000 },
  { date: '11/24', sales: 42000, expenses: 3500, deposits: 35000 },
  { date: '11/25', sales: 45000, expenses: 4000, deposits: 40000 },
];

// Mock data for payment methods
const paymentMethodsData = [
  { name: 'Cash', value: 45 },
  { name: 'UPI', value: 35 },
  { name: 'Card', value: 15 },
  { name: 'Other', value: 5 },
];

const COLORS = ['#4CAF50', '#2196F3', '#FF9800', '#9C27B0'];

const CashBalance: React.FC = () => {
  const theme = useTheme();
  const navigate = useNavigate();
  const [tabValue, setTabValue] = useState(0);
  const [selectedDate, setSelectedDate] = useState<Date | null>(new Date());
  const [depositDialogOpen, setDepositDialogOpen] = useState(false);
  const [expenseDialogOpen, setExpenseDialogOpen] = useState(false);

  // Calculate totals
  const totalCashSales = cashTransactionsData
    .filter(t => t.method === 'Cash' && t.type === 'Sale')
    .reduce((sum, t) => sum + t.amount, 0);
  
  const totalUpiSales = cashTransactionsData
    .filter(t => t.method === 'UPI' && t.type === 'Sale')
    .reduce((sum, t) => sum + t.amount, 0);
  
  const totalCardSales = cashTransactionsData
    .filter(t => t.method === 'Card' && t.type === 'Sale')
    .reduce((sum, t) => sum + t.amount, 0);
  
  const totalExpenses = cashTransactionsData
    .filter(t => t.type === 'Expense')
    .reduce((sum, t) => sum + t.amount, 0);
  
  const totalDeposits = cashTransactionsData
    .filter(t => t.type === 'Deposit')
    .reduce((sum, t) => sum + t.amount, 0);
  
  const cashInHand = totalCashSales + totalExpenses + totalDeposits;

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleOpenDepositDialog = () => {
    setDepositDialogOpen(true);
  };

  const handleCloseDepositDialog = () => {
    setDepositDialogOpen(false);
  };

  const handleOpenExpenseDialog = () => {
    setExpenseDialogOpen(true);
  };

  const handleCloseExpenseDialog = () => {
    setExpenseDialogOpen(false);
  };

  const handleSubmitDeposit = () => {
    // In a real app, this would send the deposit data to the backend
    console.log('Deposit submitted');
    handleCloseDepositDialog();
    alert('Deposit submitted for approval!');
  };

  const handleSubmitExpense = () => {
    // In a real app, this would send the expense data to the backend
    console.log('Expense submitted');
    handleCloseExpenseDialog();
    alert('Expense submitted for approval!');
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Box>
        <PageHeader
          title="Cash Management"
          subtitle="Track and manage cash transactions"
        />

        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} sm={6} md={3}>
            <StatCard
              title="Cash in Hand"
              value={`₹${cashInHand.toLocaleString()}`}
              icon={<LocalAtm />}
              trend={{ value: "Updated just now", isPositive: true, text: "" }}
              color="success"
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <StatCard
              title="Today's Cash Sales"
              value={`₹${totalCashSales.toLocaleString()}`}
              icon={<Receipt />}
              trend={{ value: "12% increase", isPositive: true, text: "vs yesterday" }}
              color="primary"
              delay={0.1}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <StatCard
              title="Today's UPI Sales"
              value={`₹${totalUpiSales.toLocaleString()}`}
              icon={<CreditCard />}
              trend={{ value: "8% increase", isPositive: true, text: "vs yesterday" }}
              color="secondary"
              delay={0.2}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <StatCard
              title="Today's Card Sales"
              value={`₹${totalCardSales.toLocaleString()}`}
              icon={<CreditCard />}
              trend={{ value: "5% increase", isPositive: true, text: "vs yesterday" }}
              color="info"
              delay={0.3}
            />
          </Grid>
        </Grid>

        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} md={8}>
            <ChartCard
              title="Cash Flow (Last 7 Days)"
              action="button"
              actionText="View Details"
              onActionClick={() => navigate('/executive/cash-history')}
              delay={0.4}
            >
              <ResponsiveContainer width="100%" height="100%">
                <LineChart
                  data={cashFlowData}
                  margin={{
                    top: 5,
                    right: 30,
                    left: 20,
                    bottom: 5,
                  }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip formatter={(value) => [`₹${value}`, '']} />
                  <Legend />
                  <Line type="monotone" dataKey="sales" name="Sales" stroke={theme.palette.primary.main} activeDot={{ r: 8 }} />
                  <Line type="monotone" dataKey="expenses" name="Expenses" stroke={theme.palette.error.main} />
                  <Line type="monotone" dataKey="deposits" name="Deposits" stroke={theme.palette.success.main} />
                </LineChart>
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
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h6" component="h2">
                    Cash Transactions
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <DatePicker
                      label="Select Date"
                      value={selectedDate}
                      onChange={(newValue) => setSelectedDate(newValue)}
                      slotProps={{ textField: { size: 'small', sx: { mr: 2 } } }}
                    />
                    <Button 
                      variant="outlined" 
                      size="small" 
                      color="primary"
                      onClick={() => navigate('/executive/cash-history')}
                    >
                      View All
                    </Button>
                  </Box>
                </Box>

                <Box sx={{ mb: 2 }}>
                  <Tabs 
                    value={tabValue} 
                    onChange={handleTabChange}
                    variant="scrollable"
                    scrollButtons="auto"
                  >
                    <Tab label="All Transactions" />
                    <Tab label="Cash Sales" />
                    <Tab label="UPI Sales" />
                    <Tab label="Card Sales" />
                    <Tab label="Expenses" />
                    <Tab label="Deposits" />
                  </Tabs>
                </Box>

                <List>
                  {cashTransactionsData.map((transaction, index) => (
                    <React.Fragment key={transaction.id}>
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
                          {transaction.type === 'Sale' && transaction.method === 'Cash' && <LocalAtm color="success" />}
                          {transaction.type === 'Sale' && transaction.method === 'UPI' && <CreditCard color="primary" />}
                          {transaction.type === 'Sale' && transaction.method === 'Card' && <CreditCard color="secondary" />}
                          {transaction.type === 'Expense' && <ArrowDownward color="error" />}
                          {transaction.type === 'Deposit' && <AccountBalance color="info" />}
                        </ListItemIcon>
                        <ListItemText
                          primary={
                            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                              <Typography variant="body1" sx={{ fontWeight: 500 }}>
                                {transaction.type} {transaction.reference}
                              </Typography>
                              <Chip 
                                label={transaction.method} 
                                size="small" 
                                color={
                                  transaction.method === 'Cash' ? 'success' : 
                                  transaction.method === 'UPI' ? 'primary' : 
                                  transaction.method === 'Card' ? 'secondary' :
                                  'info'
                                }
                                sx={{ ml: 1 }}
                              />
                            </Box>
                          }
                          secondary={
                            <Typography variant="body2" color="textSecondary">
                              {transaction.date} {transaction.time}
                              {transaction.category && ` • Category: ${transaction.category}`}
                              {transaction.bank && ` • Bank: ${transaction.bank}`}
                            </Typography>
                          }
                        />
                        <Typography 
                          variant="body1" 
                          sx={{ 
                            fontWeight: 500, 
                            color: transaction.amount < 0 ? 'error.main' : 'success.main',
                            ml: 2,
                          }}
                        >
                          {transaction.amount < 0 ? '-' : ''}₹{Math.abs(transaction.amount).toLocaleString()}
                        </Typography>
                      </ListItem>
                      {index < cashTransactionsData.length - 1 && <Divider component="li" />}
                    </React.Fragment>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Quick Actions
                    </Typography>
                    <Grid container spacing={2}>
                      <Grid item xs={6}>
                        <Button
                          variant="outlined"
                          color="primary"
                          fullWidth
                          startIcon={<AccountBalance />}
                          onClick={handleOpenDepositDialog}
                          sx={{ py: 1.5 }}
                        >
                          Record Deposit
                        </Button>
                      </Grid>
                      <Grid item xs={6}>
                        <Button
                          variant="outlined"
                          color="error"
                          fullWidth
                          startIcon={<MonetizationOn />}
                          onClick={handleOpenExpenseDialog}
                          sx={{ py: 1.5 }}
                        >
                          Record Expense
                        </Button>
                      </Grid>
                      <Grid item xs={12}>
                        <Button
                          variant="contained"
                          color="primary"
                          fullWidth
                          startIcon={<ReceiptLong />}
                          onClick={() => navigate('/executive/today-summary')}
                          sx={{ py: 1.5 }}
                        >
                          Generate Daily Summary
                        </Button>
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Cash Summary
                    </Typography>
                    <List>
                      <ListItem sx={{ px: 0 }}>
                        <ListItemText primary="Opening Balance" />
                        <Typography variant="body1" sx={{ fontWeight: 500 }}>
                          ₹15,000
                        </Typography>
                      </ListItem>
                      <Divider component="li" />
                      <ListItem sx={{ px: 0 }}>
                        <ListItemText primary="Cash Sales" />
                        <Typography variant="body1" sx={{ fontWeight: 500, color: 'success.main' }}>
                          +₹{totalCashSales.toLocaleString()}
                        </Typography>
                      </ListItem>
                      <Divider component="li" />
                      <ListItem sx={{ px: 0 }}>
                        <ListItemText primary="Expenses" />
                        <Typography variant="body1" sx={{ fontWeight: 500, color: 'error.main' }}>
                          ₹{totalExpenses.toLocaleString()}
                        </Typography>
                      </ListItem>
                      <Divider component="li" />
                      <ListItem sx={{ px: 0 }}>
                        <ListItemText primary="Deposits" />
                        <Typography variant="body1" sx={{ fontWeight: 500, color: 'error.main' }}>
                          ₹{totalDeposits.toLocaleString()}
                        </Typography>
                      </ListItem>
                      <Divider component="li" />
                      <ListItem sx={{ px: 0, bgcolor: 'background.default', borderRadius: 1 }}>
                        <ListItemText 
                          primary={
                            <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                              Cash in Hand
                            </Typography>
                          } 
                        />
                        <Typography variant="subtitle1" sx={{ fontWeight: 600, color: 'success.main' }}>
                          ₹{cashInHand.toLocaleString()}
                        </Typography>
                      </ListItem>
                    </List>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Pending Approvals
                    </Typography>
                    <List>
                      <ListItem sx={{ px: 0 }}>
                        <ListItemIcon>
                          <AccountBalance color="info" />
                        </ListItemIcon>
                        <ListItemText 
                          primary="Bank Deposit DEP-2023-022" 
                          secondary="₹15,000 • Submitted 1 hour ago"
                        />
                        <Chip label="Pending" size="small" color="warning" />
                      </ListItem>
                      <Divider component="li" />
                      <ListItem sx={{ px: 0 }}>
                        <ListItemIcon>
                          <MonetizationOn color="error" />
                        </ListItemIcon>
                        <ListItemText 
                          primary="Expense EXP-2023-055" 
                          secondary="₹1,200 • Submitted 3 hours ago"
                        />
                        <Chip label="Pending" size="small" color="warning" />
                      </ListItem>
                    </List>
                    <Box sx={{ mt: 2, display: 'flex', justifyContent: 'center' }}>
                      <Button 
                        variant="text" 
                        color="primary"
                        onClick={() => navigate('/executive/pending-approvals')}
                      >
                        View All Pending Approvals
                      </Button>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </Grid>
        </Grid>

        {/* Deposit Dialog */}
        <Dialog open={depositDialogOpen} onClose={handleCloseDepositDialog} maxWidth="sm" fullWidth>
          <DialogTitle>Record Bank Deposit</DialogTitle>
          <DialogContent>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Amount"
                  variant="outlined"
                  type="number"
                  InputProps={{
                    startAdornment: <InputAdornment position="start">₹</InputAdornment>,
                  }}
                />
              </Grid>
              <Grid item xs={12}>
                <FormControl fullWidth>
                  <InputLabel>Bank Account</InputLabel>
                  <Select
                    label="Bank Account"
                    defaultValue="hdfc"
                  >
                    <MenuItem value="hdfc">HDFC Bank - XXXX1234</MenuItem>
                    <MenuItem value="sbi">SBI - XXXX5678</MenuItem>
                    <MenuItem value="icici">ICICI Bank - XXXX9012</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Reference Number"
                  variant="outlined"
                  placeholder="Enter deposit slip number or reference"
                />
              </Grid>
              <Grid item xs={12}>
                <DatePicker
                  label="Deposit Date"
                  defaultValue={new Date()}
                  slotProps={{ textField: { fullWidth: true } }}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Notes"
                  variant="outlined"
                  multiline
                  rows={3}
                  placeholder="Enter any additional details..."
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseDepositDialog}>Cancel</Button>
            <Button 
              onClick={handleSubmitDeposit} 
              variant="contained" 
              color="primary"
            >
              Submit for Approval
            </Button>
          </DialogActions>
        </Dialog>

        {/* Expense Dialog */}
        <Dialog open={expenseDialogOpen} onClose={handleCloseExpenseDialog} maxWidth="sm" fullWidth>
          <DialogTitle>Record Expense</DialogTitle>
          <DialogContent>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Amount"
                  variant="outlined"
                  type="number"
                  InputProps={{
                    startAdornment: <InputAdornment position="start">₹</InputAdornment>,
                  }}
                />
              </Grid>
              <Grid item xs={12}>
                <FormControl fullWidth>
                  <InputLabel>Expense Category</InputLabel>
                  <Select
                    label="Expense Category"
                    defaultValue="utilities"
                  >
                    <MenuItem value="utilities">Utilities</MenuItem>
                    <MenuItem value="supplies">Supplies</MenuItem>
                    <MenuItem value="maintenance">Maintenance</MenuItem>
                    <MenuItem value="transport">Transportation</MenuItem>
                    <MenuItem value="salary">Salary/Wages</MenuItem>
                    <MenuItem value="other">Other</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Paid To"
                  variant="outlined"
                  placeholder="Enter name of recipient"
                />
              </Grid>
              <Grid item xs={12}>
                <DatePicker
                  label="Expense Date"
                  defaultValue={new Date()}
                  slotProps={{ textField: { fullWidth: true } }}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Notes"
                  variant="outlined"
                  multiline
                  rows={3}
                  placeholder="Enter expense details..."
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseExpenseDialog}>Cancel</Button>
            <Button 
              onClick={handleSubmitExpense} 
              variant="contained" 
              color="primary"
            >
              Submit for Approval
            </Button>
          </DialogActions>
        </Dialog>
      </Box>
    </LocalizationProvider>
  );
};

export default CashBalance;