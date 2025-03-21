import React, { useState, useEffect } from 'react';
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
  CircularProgress,
  Alert,
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
  Refresh,
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
import { cashService, saleService, CashTransaction, CashBalance as CashBalanceType, DailySummary } from '../../../services/api';
import { useAuth, useNotification } from '../../../hooks';
import { format, subDays, parseISO } from 'date-fns';

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
  const { user } = useAuth();
  const { showNotification } = useNotification();
  const [tabValue, setTabValue] = useState(0);
  const [selectedDate, setSelectedDate] = useState<Date | null>(new Date());
  const [depositDialogOpen, setDepositDialogOpen] = useState(false);
  const [expenseDialogOpen, setExpenseDialogOpen] = useState(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [cashTransactions, setCashTransactions] = useState<CashTransaction[]>([]);
  const [cashBalance, setCashBalance] = useState<CashBalanceType | null>(null);
  const [dailySummary, setDailySummary] = useState<DailySummary | null>(null);
  const [cashFlowData, setCashFlowData] = useState<any[]>([]);
  const [paymentMethodsData, setPaymentMethodsData] = useState<any[]>([]);
  
  // Form state for deposit dialog
  const [depositAmount, setDepositAmount] = useState<string>('');
  const [depositReference, setDepositReference] = useState<string>('');
  const [depositNotes, setDepositNotes] = useState<string>('');
  
  // Form state for expense dialog
  const [expenseAmount, setExpenseAmount] = useState<string>('');
  const [expenseCategory, setExpenseCategory] = useState<string>('');
  const [expenseReason, setExpenseReason] = useState<string>('');
  const [expenseNotes, setExpenseNotes] = useState<string>('');

  // Get shop ID from user
  const shopId = user?.assigned_shops && user.assigned_shops.length > 0 
    ? parseInt(user.assigned_shops[0].id) 
    : undefined;

  // Fetch cash data
  useEffect(() => {
    const fetchCashData = async () => {
      if (!selectedDate) return;
      
      setIsLoading(true);
      setError(null);
      
      try {
        const dateString = format(selectedDate, 'yyyy-MM-dd');
        
        // In production environment
        if (process.env.NODE_ENV === 'production') {
          // Fetch cash transactions for the selected date
          const transactions = await cashService.getCashTransactions(
            shopId,
            { start_date: dateString, end_date: dateString }
          );
          setCashTransactions(transactions);
          
          // Fetch cash balance
          const balance = await cashService.getCashBalance(shopId);
          setCashBalance(balance);
          
          // Fetch daily summary
          try {
            const summary = await cashService.getDailySummary(dateString, shopId);
            setDailySummary(summary);
          } catch (err) {
            // Daily summary might not exist yet for today
            setDailySummary(null);
          }
          
          // Fetch cash flow data for the last 7 days
          const cashFlowArray = [];
          for (let i = 6; i >= 0; i--) {
            const date = subDays(selectedDate, i);
            const dateStr = format(date, 'yyyy-MM-dd');
            
            try {
              const daySummary = await cashService.getDailySummary(dateStr, shopId);
              cashFlowArray.push({
                date: format(date, 'MM/dd'),
                sales: daySummary.total_sales,
                expenses: daySummary.expenses,
                deposits: daySummary.deposits,
              });
            } catch (err) {
              // If no summary exists for this day, add zeros
              cashFlowArray.push({
                date: format(date, 'MM/dd'),
                sales: 0,
                expenses: 0,
                deposits: 0,
              });
            }
          }
          setCashFlowData(cashFlowArray);
          
          // Fetch payment methods breakdown
          const salesStats = await saleService.getSalesStats(
            shopId,
            { start_date: dateString, end_date: dateString }
          );
          
          const methodsData = salesStats.sales_by_payment_method.map(item => ({
            name: item.method,
            value: item.percentage,
          }));
          setPaymentMethodsData(methodsData);
        } else {
          // For development/demo purposes, we'll use mock data
          await new Promise(resolve => setTimeout(resolve, 1000));
          
          // Use the mock data
          setCashTransactions(cashTransactionsData);
          
          // Mock cash balance
          setCashBalance({
            shop_id: 1,
            shop_name: 'Downtown Store',
            opening_balance: 15000,
            closing_balance: 25000,
            total_deposits: 10000,
            total_expenses: 1300,
            total_upi: 5900,
            total_collections: 0,
            last_updated: new Date().toISOString(),
          });
          
          // Mock daily summary
          setDailySummary({
            date: dateString,
            shop_id: 1,
            shop_name: 'Downtown Store',
            total_sales: 23100,
            cash_sales: 12000,
            upi_sales: 5900,
            card_sales: 5200,
            other_sales: 0,
            expenses: 1300,
            deposits: 10000,
            opening_balance: 15000,
            closing_balance: 25000,
            status: 'pending',
            created_by: 'John Doe',
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
          });
          
          // Use mock cash flow data
          setCashFlowData(cashFlowData);
          
          // Use mock payment methods data
          setPaymentMethodsData(paymentMethodsData);
        }
      } catch (err: any) {
        console.error('Error fetching cash data:', err);
        setError(err.message || 'Failed to fetch cash data');
        showNotification({
          message: 'Failed to fetch cash data. Please try again later.',
          variant: 'error',
        });
      } finally {
        setIsLoading(false);
      }
    };

    fetchCashData();
  }, [selectedDate, shopId, showNotification]);

  // Calculate totals from transactions
  const totalCashSales = dailySummary?.cash_sales || 0;
  const totalUpiSales = dailySummary?.upi_sales || 0;
  const totalCardSales = dailySummary?.card_sales || 0;
  const totalExpenses = dailySummary?.expenses || 0;
  const totalDeposits = dailySummary?.deposits || 0;
  const cashInHand = cashBalance?.closing_balance || 0;

  // Filter transactions based on tab
  const filteredTransactions = cashTransactions.filter(transaction => {
    switch (tabValue) {
      case 0: // All Transactions
        return true;
      case 1: // Cash Sales
        return transaction.transaction_type === 'sale' && transaction.payment_method === 'cash';
      case 2: // UPI Sales
        return transaction.transaction_type === 'sale' && transaction.payment_method === 'upi';
      case 3: // Card Sales
        return transaction.transaction_type === 'sale' && transaction.payment_method === 'card';
      case 4: // Expenses
        return transaction.transaction_type === 'expense';
      case 5: // Deposits
        return transaction.transaction_type === 'deposit';
      default:
        return true;
    }
  });

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleOpenDepositDialog = () => {
    setDepositDialogOpen(true);
  };

  const handleCloseDepositDialog = () => {
    setDepositAmount('');
    setDepositReference('');
    setDepositNotes('');
    setDepositDialogOpen(false);
  };

  const handleOpenExpenseDialog = () => {
    setExpenseDialogOpen(true);
  };

  const handleCloseExpenseDialog = () => {
    setExpenseAmount('');
    setExpenseCategory('');
    setExpenseReason('');
    setExpenseNotes('');
    setExpenseDialogOpen(false);
  };

  const handleSubmitDeposit = async () => {
    if (!depositAmount || parseFloat(depositAmount) <= 0) {
      showNotification({
        message: 'Please enter a valid amount',
        variant: 'error',
      });
      return;
    }
    
    try {
      setIsLoading(true);
      
      if (process.env.NODE_ENV === 'production') {
        await cashService.recordDeposit({
          amount: parseFloat(depositAmount),
          reference_number: depositReference,
          notes: depositNotes,
          shop_id: shopId,
        });
      } else {
        // For development/demo purposes
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
      
      showNotification({
        message: 'Deposit submitted for approval',
        variant: 'success',
      });
      
      handleCloseDepositDialog();
      
      // Refresh data
      if (selectedDate) {
        const dateString = format(selectedDate, 'yyyy-MM-dd');
        const transactions = await cashService.getCashTransactions(
          shopId,
          { start_date: dateString, end_date: dateString }
        );
        setCashTransactions(transactions);
        
        const balance = await cashService.getCashBalance(shopId);
        setCashBalance(balance);
      }
    } catch (err: any) {
      console.error('Error submitting deposit:', err);
      showNotification({
        message: err.message || 'Failed to submit deposit',
        variant: 'error',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmitExpense = async () => {
    if (!expenseAmount || parseFloat(expenseAmount) <= 0) {
      showNotification({
        message: 'Please enter a valid amount',
        variant: 'error',
      });
      return;
    }
    
    if (!expenseCategory) {
      showNotification({
        message: 'Please select a category',
        variant: 'error',
      });
      return;
    }
    
    if (!expenseReason) {
      showNotification({
        message: 'Please enter a reason',
        variant: 'error',
      });
      return;
    }
    
    try {
      setIsLoading(true);
      
      if (process.env.NODE_ENV === 'production') {
        await cashService.recordExpense({
          amount: parseFloat(expenseAmount),
          category: expenseCategory,
          reason: expenseReason,
          notes: expenseNotes,
          shop_id: shopId,
        });
      } else {
        // For development/demo purposes
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
      
      showNotification({
        message: 'Expense submitted for approval',
        variant: 'success',
      });
      
      handleCloseExpenseDialog();
      
      // Refresh data
      if (selectedDate) {
        const dateString = format(selectedDate, 'yyyy-MM-dd');
        const transactions = await cashService.getCashTransactions(
          shopId,
          { start_date: dateString, end_date: dateString }
        );
        setCashTransactions(transactions);
        
        const balance = await cashService.getCashBalance(shopId);
        setCashBalance(balance);
      }
    } catch (err: any) {
      console.error('Error submitting expense:', err);
      showNotification({
        message: err.message || 'Failed to submit expense',
        variant: 'error',
      });
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleRefreshData = async () => {
    if (!selectedDate) return;
    
    setIsLoading(true);
    setError(null);
    
    try {
      const dateString = format(selectedDate, 'yyyy-MM-dd');
      
      if (process.env.NODE_ENV === 'production') {
        // Refresh cash transactions
        const transactions = await cashService.getCashTransactions(
          shopId,
          { start_date: dateString, end_date: dateString }
        );
        setCashTransactions(transactions);
        
        // Refresh cash balance
        const balance = await cashService.getCashBalance(shopId);
        setCashBalance(balance);
        
        // Refresh daily summary
        try {
          const summary = await cashService.getDailySummary(dateString, shopId);
          setDailySummary(summary);
        } catch (err) {
          setDailySummary(null);
        }
      } else {
        // For development/demo purposes
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
      
      showNotification({
        message: 'Data refreshed successfully',
        variant: 'success',
      });
    } catch (err: any) {
      console.error('Error refreshing data:', err);
      setError(err.message || 'Failed to refresh data');
      showNotification({
        message: 'Failed to refresh data. Please try again later.',
        variant: 'error',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Box>
        <PageHeader
          title="Cash Management"
          subtitle="Track and manage cash transactions"
        />

        {isLoading && !cashBalance ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', py: 10 }}>
            <CircularProgress />
            <Typography variant="h6" sx={{ ml: 2 }}>
              Loading cash data...
            </Typography>
          </Box>
        ) : error ? (
          <Alert 
            severity="error" 
            sx={{ mb: 3 }}
            action={
              <Button color="inherit" size="small" onClick={handleRefreshData}>
                Retry
              </Button>
            }
          >
            {error}
          </Alert>
        ) : (
          <>
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
                  trend={{ value: dailySummary ? "From today's summary" : "No data available", isPositive: true, text: "" }}
                  color="primary"
                  delay={0.1}
                />
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <StatCard
                  title="Today's UPI Sales"
                  value={`₹${totalUpiSales.toLocaleString()}`}
                  icon={<CreditCard />}
                  trend={{ value: dailySummary ? "From today's summary" : "No data available", isPositive: true, text: "" }}
                  color="secondary"
                  delay={0.2}
                />
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <StatCard
                  title="Today's Card Sales"
                  value={`₹${totalCardSales.toLocaleString()}`}
                  icon={<CreditCard />}
                  trend={{ value: dailySummary ? "From today's summary" : "No data available", isPositive: true, text: "" }}
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
                  {cashFlowData.length > 0 ? (
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
                  ) : (
                    <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
                      <Typography variant="body1" color="textSecondary">
                        No cash flow data available
                      </Typography>
                    </Box>
                  )}
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
                  {paymentMethodsData.length > 0 ? (
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
                  ) : (
                    <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
                      <Typography variant="body1" color="textSecondary">
                        No payment methods data available
                      </Typography>
                    </Box>
                  )}
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
                          onClick={handleRefreshData}
                          startIcon={<Refresh />}
                          disabled={isLoading}
                        >
                          Refresh
                        </Button>
                        <Button 
                          variant="outlined" 
                          size="small" 
                          color="primary"
                          onClick={() => navigate('/executive/cash-history')}
                          sx={{ ml: 1 }}
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

                    {isLoading ? (
                      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', py: 5 }}>
                        <CircularProgress size={30} />
                        <Typography variant="body1" sx={{ ml: 2 }}>
                          Loading transactions...
                        </Typography>
                      </Box>
                    ) : filteredTransactions.length === 0 ? (
                      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', py: 5 }}>
                        <Typography variant="body1" color="textSecondary">
                          No transactions found for the selected date and filter
                        </Typography>
                      </Box>
                    ) : (
                      <List>
                        {filteredTransactions.map((transaction, index) => (
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
                                {transaction.transaction_type === 'sale' && transaction.payment_method === 'cash' && <LocalAtm color="success" />}
                                {transaction.transaction_type === 'sale' && transaction.payment_method === 'upi' && <CreditCard color="primary" />}
                                {transaction.transaction_type === 'sale' && transaction.payment_method === 'card' && <CreditCard color="secondary" />}
                                {transaction.transaction_type === 'expense' && <ArrowDownward color="error" />}
                                {transaction.transaction_type === 'deposit' && <AccountBalance color="info" />}
                                {transaction.transaction_type === 'collection' && <AttachMoney color="warning" />}
                              </ListItemIcon>
                              <ListItemText
                                primary={
                                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                    <Typography variant="body1" sx={{ fontWeight: 500 }}>
                                      {transaction.transaction_type.charAt(0).toUpperCase() + transaction.transaction_type.slice(1)} 
                                      {transaction.reference_number && ` ${transaction.reference_number}`}
                                    </Typography>
                                    <Chip 
                                      label={transaction.payment_method} 
                                      size="small" 
                                      color={
                                        transaction.payment_method === 'cash' ? 'success' : 
                                        transaction.payment_method === 'upi' ? 'primary' : 
                                        transaction.payment_method === 'card' ? 'secondary' :
                                        'info'
                                      }
                                      sx={{ ml: 1 }}
                                    />
                                    <Chip 
                                      label={transaction.status} 
                                      size="small" 
                                      color={
                                        transaction.status === 'approved' ? 'success' : 
                                        transaction.status === 'pending' ? 'warning' : 
                                        'error'
                                      }
                                      sx={{ ml: 1 }}
                                    />
                                  </Box>
                                }
                                secondary={
                                  <Typography variant="body2" color="textSecondary">
                                    {format(new Date(transaction.created_at), 'yyyy-MM-dd HH:mm')}
                                    {transaction.notes && ` • ${transaction.notes}`}
                                  </Typography>
                                }
                              />
                              <Typography 
                                variant="body1" 
                                sx={{ 
                                  fontWeight: 500, 
                                  color: transaction.transaction_type === 'expense' ? 'error.main' : 'success.main',
                                  ml: 2,
                                }}
                              >
                                {transaction.transaction_type === 'expense' ? '-' : ''}₹{transaction.amount.toLocaleString()}
                              </Typography>
                            </ListItem>
                            {index < filteredTransactions.length - 1 && <Divider component="li" />}
                          </React.Fragment>
                        ))}
                      </List>
                    )}
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
                  value={depositAmount}
                  onChange={(e) => setDepositAmount(e.target.value)}
                  InputProps={{
                    startAdornment: <InputAdornment position="start">₹</InputAdornment>,
                  }}
                  disabled={isLoading}
                  required
                  error={depositAmount !== '' && parseFloat(depositAmount) <= 0}
                  helperText={depositAmount !== '' && parseFloat(depositAmount) <= 0 ? 'Amount must be greater than 0' : ''}
                />
              </Grid>
              <Grid item xs={12}>
                <FormControl fullWidth disabled={isLoading}>
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
                  value={depositReference}
                  onChange={(e) => setDepositReference(e.target.value)}
                  disabled={isLoading}
                />
              </Grid>
              <Grid item xs={12}>
                <DatePicker
                  label="Deposit Date"
                  defaultValue={new Date()}
                  slotProps={{ textField: { fullWidth: true, disabled: isLoading } }}
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
                  value={depositNotes}
                  onChange={(e) => setDepositNotes(e.target.value)}
                  disabled={isLoading}
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseDepositDialog} disabled={isLoading}>Cancel</Button>
            <Button 
              onClick={handleSubmitDeposit} 
              variant="contained" 
              color="primary"
              disabled={isLoading || !depositAmount || parseFloat(depositAmount) <= 0}
            >
              {isLoading ? 'Submitting...' : 'Submit for Approval'}
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
                  value={expenseAmount}
                  onChange={(e) => setExpenseAmount(e.target.value)}
                  InputProps={{
                    startAdornment: <InputAdornment position="start">₹</InputAdornment>,
                  }}
                  disabled={isLoading}
                  required
                  error={expenseAmount !== '' && parseFloat(expenseAmount) <= 0}
                  helperText={expenseAmount !== '' && parseFloat(expenseAmount) <= 0 ? 'Amount must be greater than 0' : ''}
                />
              </Grid>
              <Grid item xs={12}>
                <FormControl fullWidth disabled={isLoading} required>
                  <InputLabel>Expense Category</InputLabel>
                  <Select
                    label="Expense Category"
                    value={expenseCategory}
                    onChange={(e) => setExpenseCategory(e.target.value)}
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
                  label="Reason"
                  variant="outlined"
                  placeholder="Brief reason for the expense"
                  value={expenseReason}
                  onChange={(e) => setExpenseReason(e.target.value)}
                  disabled={isLoading}
                  required
                  error={expenseReason === ''}
                  helperText={expenseReason === '' ? 'Reason is required' : ''}
                />
              </Grid>
              <Grid item xs={12}>
                <DatePicker
                  label="Expense Date"
                  defaultValue={new Date()}
                  slotProps={{ textField: { fullWidth: true, disabled: isLoading } }}
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
                  value={expenseNotes}
                  onChange={(e) => setExpenseNotes(e.target.value)}
                  disabled={isLoading}
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseExpenseDialog} disabled={isLoading}>Cancel</Button>
            <Button 
              onClick={handleSubmitExpense} 
              variant="contained" 
              color="primary"
              disabled={
                isLoading || 
                !expenseAmount || 
                parseFloat(expenseAmount) <= 0 || 
                !expenseCategory || 
                !expenseReason
              }
            >
              {isLoading ? 'Submitting...' : 'Submit for Approval'}
            </Button>
          </DialogActions>
        </Dialog>
      </Box>
    </LocalizationProvider>
  );
};

export default CashBalance;