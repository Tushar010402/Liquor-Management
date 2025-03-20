import React, { useState } from 'react';
import {
  Box,
  Grid,
  Typography,
  Card,
  CardContent,
  Divider,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Chip,
  TextField,
  InputAdornment,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Menu,
  MenuItem,
  ListItemIcon,
  ListItemText,
  Tooltip,
  Tab,
  Tabs,
  FormControl,
  InputLabel,
  Select,
} from '@mui/material';
import {
  Search as SearchIcon,
  Visibility as ViewIcon,
  FilterList as FilterIcon,
  Print as PrintIcon,
  Share as ShareIcon,
  FileDownload as DownloadIcon,
  LocalAtm as CashIcon,
  AccountBalance as BankIcon,
  Receipt as ReceiptIcon,
  MonetizationOn as ExpenseIcon,
  ArrowUpward as IncomeIcon,
  ArrowDownward as OutcomeIcon,
  CalendarToday as CalendarIcon,
} from '@mui/icons-material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { PageHeader } from '../../../components/common';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';

// Mock transaction data
const mockTransactions = [
  {
    id: 'TRX-001',
    date: '2023-11-25T10:30:00Z',
    type: 'sale',
    typeText: 'Sale',
    reference: 'INV-2023-1234',
    amount: 3500,
    method: 'cash',
    methodText: 'Cash',
    details: {
      customer: 'Walk-in Customer',
      items: [
        { name: 'Johnnie Walker Black Label', quantity: 1, price: 3500 }
      ],
      cashier: 'Vikram Mehta',
    },
  },
  {
    id: 'TRX-002',
    date: '2023-11-25T11:45:00Z',
    type: 'sale',
    typeText: 'Sale',
    reference: 'INV-2023-1235',
    amount: 2800,
    method: 'upi',
    methodText: 'UPI',
    details: {
      customer: 'Raj Kumar',
      items: [
        { name: 'Jack Daniels', quantity: 1, price: 2800 }
      ],
      cashier: 'Vikram Mehta',
      upiReference: 'UPI123456789',
    },
  },
  {
    id: 'TRX-003',
    date: '2023-11-25T12:20:00Z',
    type: 'sale',
    typeText: 'Sale',
    reference: 'INV-2023-1236',
    amount: 5200,
    method: 'card',
    methodText: 'Card',
    details: {
      customer: 'Priya Sharma',
      items: [
        { name: 'Grey Goose Vodka', quantity: 1, price: 4500 },
        { name: 'Tonic Water', quantity: 2, price: 350 },
      ],
      cashier: 'Vikram Mehta',
      cardReference: 'CARD987654321',
    },
  },
  {
    id: 'TRX-004',
    date: '2023-11-25T13:10:00Z',
    type: 'sale',
    typeText: 'Sale',
    reference: 'INV-2023-1237',
    amount: 1800,
    method: 'cash',
    methodText: 'Cash',
    details: {
      customer: 'Walk-in Customer',
      items: [
        { name: 'Absolut Vodka', quantity: 1, price: 1800 }
      ],
      cashier: 'Vikram Mehta',
    },
  },
  {
    id: 'TRX-005',
    date: '2023-11-25T14:15:00Z',
    type: 'expense',
    typeText: 'Expense',
    reference: 'EXP-2023-056',
    amount: -500,
    method: 'cash',
    methodText: 'Cash',
    details: {
      category: 'Utilities',
      paidTo: 'Electricity Department',
      notes: 'Monthly electricity bill',
      approvedBy: 'Rajesh Kumar',
    },
  },
  {
    id: 'TRX-006',
    date: '2023-11-25T15:30:00Z',
    type: 'deposit',
    typeText: 'Bank Deposit',
    reference: 'DEP-2023-023',
    amount: -10000,
    method: 'bank_transfer',
    methodText: 'Bank Transfer',
    details: {
      bank: 'HDFC Bank',
      accountNumber: 'XXXX1234',
      notes: 'Daily cash deposit',
      approvedBy: 'Rajesh Kumar',
    },
  },
  {
    id: 'TRX-007',
    date: '2023-11-24T10:45:00Z',
    type: 'sale',
    typeText: 'Sale',
    reference: 'INV-2023-1230',
    amount: 4200,
    method: 'cash',
    methodText: 'Cash',
    details: {
      customer: 'Amit Singh',
      items: [
        { name: 'Chivas Regal 12 Year', quantity: 1, price: 3200 },
        { name: 'Soda Water', quantity: 2, price: 500 },
      ],
      cashier: 'Vikram Mehta',
    },
  },
  {
    id: 'TRX-008',
    date: '2023-11-24T11:30:00Z',
    type: 'sale',
    typeText: 'Sale',
    reference: 'INV-2023-1231',
    amount: 3100,
    method: 'upi',
    methodText: 'UPI',
    details: {
      customer: 'Neha Patel',
      items: [
        { name: 'Bombay Sapphire Gin', quantity: 1, price: 2500 },
        { name: 'Tonic Water', quantity: 2, price: 300 },
      ],
      cashier: 'Vikram Mehta',
      upiReference: 'UPI987654321',
    },
  },
  {
    id: 'TRX-009',
    date: '2023-11-24T12:15:00Z',
    type: 'expense',
    typeText: 'Expense',
    reference: 'EXP-2023-055',
    amount: -800,
    method: 'cash',
    methodText: 'Cash',
    details: {
      category: 'Supplies',
      paidTo: 'Stationery Shop',
      notes: 'Office supplies',
      approvedBy: 'Rajesh Kumar',
    },
  },
  {
    id: 'TRX-010',
    date: '2023-11-24T14:20:00Z',
    type: 'sale',
    typeText: 'Sale',
    reference: 'INV-2023-1232',
    amount: 2500,
    method: 'cash',
    methodText: 'Cash',
    details: {
      customer: 'Walk-in Customer',
      items: [
        { name: 'Jameson Irish Whiskey', quantity: 1, price: 2200 },
        { name: 'Soda Water', quantity: 1, price: 300 },
      ],
      cashier: 'Vikram Mehta',
    },
  },
  {
    id: 'TRX-011',
    date: '2023-11-24T16:30:00Z',
    type: 'deposit',
    typeText: 'Bank Deposit',
    reference: 'DEP-2023-022',
    amount: -8000,
    method: 'bank_transfer',
    methodText: 'Bank Transfer',
    details: {
      bank: 'HDFC Bank',
      accountNumber: 'XXXX1234',
      notes: 'Daily cash deposit',
      approvedBy: 'Rajesh Kumar',
    },
  },
  {
    id: 'TRX-012',
    date: '2023-11-23T11:15:00Z',
    type: 'sale',
    typeText: 'Sale',
    reference: 'INV-2023-1225',
    amount: 6800,
    method: 'card',
    methodText: 'Card',
    details: {
      customer: 'Vikram Mehta',
      items: [
        { name: 'Macallan 12 Year', quantity: 1, price: 6800 },
      ],
      cashier: 'Vikram Mehta',
      cardReference: 'CARD123456789',
    },
  },
  {
    id: 'TRX-013',
    date: '2023-11-23T13:45:00Z',
    type: 'expense',
    typeText: 'Expense',
    reference: 'EXP-2023-054',
    amount: -1200,
    method: 'cash',
    methodText: 'Cash',
    details: {
      category: 'Maintenance',
      paidTo: 'Plumber',
      notes: 'Fixing leaking tap',
      approvedBy: 'Rajesh Kumar',
    },
  },
  {
    id: 'TRX-014',
    date: '2023-11-23T15:30:00Z',
    type: 'sale',
    typeText: 'Sale',
    reference: 'INV-2023-1226',
    amount: 5500,
    method: 'upi',
    methodText: 'UPI',
    details: {
      customer: 'Raj Kumar',
      items: [
        { name: 'Johnnie Walker Black Label', quantity: 1, price: 3500 },
        { name: 'Bacardi White Rum', quantity: 1, price: 1200 },
        { name: 'Soda Water', quantity: 2, price: 400 },
      ],
      cashier: 'Vikram Mehta',
      upiReference: 'UPI567891234',
    },
  },
  {
    id: 'TRX-015',
    date: '2023-11-23T17:00:00Z',
    type: 'deposit',
    typeText: 'Bank Deposit',
    reference: 'DEP-2023-021',
    amount: -12000,
    method: 'bank_transfer',
    methodText: 'Bank Transfer',
    details: {
      bank: 'HDFC Bank',
      accountNumber: 'XXXX1234',
      notes: 'Daily cash deposit',
      approvedBy: 'Rajesh Kumar',
    },
  },
];

// Prepare data for charts
const prepareChartData = (transactions: any[], days: number = 7) => {
  const today = new Date();
  const dates: string[] = [];
  
  // Generate last n days
  for (let i = days - 1; i >= 0; i--) {
    const date = new Date(today);
    date.setDate(today.getDate() - i);
    dates.push(date.toISOString().split('T')[0]);
  }
  
  // Initialize data with zeros
  const chartData = dates.map(date => ({
    date,
    sales: 0,
    expenses: 0,
    deposits: 0,
  }));
  
  // Fill in actual data
  transactions.forEach(transaction => {
    const transactionDate = new Date(transaction.date).toISOString().split('T')[0];
    const dataPoint = chartData.find(item => item.date === transactionDate);
    
    if (dataPoint) {
      if (transaction.type === 'sale') {
        dataPoint.sales += transaction.amount;
      } else if (transaction.type === 'expense') {
        dataPoint.expenses += Math.abs(transaction.amount);
      } else if (transaction.type === 'deposit') {
        dataPoint.deposits += Math.abs(transaction.amount);
      }
    }
  });
  
  // Format dates for display
  return chartData.map(item => ({
    ...item,
    date: new Date(item.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
  }));
};

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`transaction-tabpanel-${index}`}
      aria-labelledby={`transaction-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ pt: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

const CashHistory: React.FC = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedTransaction, setSelectedTransaction] = useState<any | null>(null);
  const [detailsDialogOpen, setDetailsDialogOpen] = useState<boolean>(false);
  const [startDate, setStartDate] = useState<Date | null>(null);
  const [endDate, setEndDate] = useState<Date | null>(null);
  const [tabValue, setTabValue] = useState(0);
  const [transactionType, setTransactionType] = useState<string>('all');
  const [paymentMethod, setPaymentMethod] = useState<string>('all');
  const [transactions] = useState(mockTransactions);
  const [chartData] = useState(prepareChartData(mockTransactions));

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleViewDetails = (transaction: any) => {
    setSelectedTransaction(transaction);
    setDetailsDialogOpen(true);
  };

  const filteredTransactions = transactions.filter(transaction => {
    const matchesSearch = 
      transaction.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      transaction.reference.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (transaction.details.customer && transaction.details.customer.toLowerCase().includes(searchQuery.toLowerCase())) ||
      (transaction.details.paidTo && transaction.details.paidTo.toLowerCase().includes(searchQuery.toLowerCase()));
    
    const transactionDate = new Date(transaction.date);
    const matchesDateRange = 
      (!startDate || transactionDate >= startDate) &&
      (!endDate || transactionDate <= endDate);
    
    const matchesType = 
      transactionType === 'all' || transaction.type === transactionType;
    
    const matchesMethod = 
      paymentMethod === 'all' || transaction.method === paymentMethod;
    
    const matchesTab = 
      (tabValue === 0) || // All
      (tabValue === 1 && transaction.type === 'sale') || // Sales
      (tabValue === 2 && transaction.type === 'expense') || // Expenses
      (tabValue === 3 && transaction.type === 'deposit'); // Deposits
    
    return matchesSearch && matchesDateRange && matchesType && matchesMethod && matchesTab;
  });

  const clearFilters = () => {
    setSearchQuery('');
    setStartDate(null);
    setEndDate(null);
    setTransactionType('all');
    setPaymentMethod('all');
  };

  const getTransactionTypeChip = (type: string) => {
    switch (type) {
      case 'sale':
        return (
          <Chip
            icon={<ReceiptIcon />}
            label="Sale"
            color="primary"
            size="small"
          />
        );
      case 'expense':
        return (
          <Chip
            icon={<ExpenseIcon />}
            label="Expense"
            color="error"
            size="small"
          />
        );
      case 'deposit':
        return (
          <Chip
            icon={<BankIcon />}
            label="Deposit"
            color="info"
            size="small"
          />
        );
      default:
        return null;
    }
  };

  const getPaymentMethodChip = (method: string) => {
    switch (method) {
      case 'cash':
        return (
          <Chip
            icon={<CashIcon />}
            label="Cash"
            color="success"
            size="small"
            variant="outlined"
          />
        );
      case 'upi':
        return (
          <Chip
            label="UPI"
            color="secondary"
            size="small"
            variant="outlined"
          />
        );
      case 'card':
        return (
          <Chip
            label="Card"
            color="primary"
            size="small"
            variant="outlined"
          />
        );
      case 'bank_transfer':
        return (
          <Chip
            icon={<BankIcon />}
            label="Bank Transfer"
            color="info"
            size="small"
            variant="outlined"
          />
        );
      default:
        return null;
    }
  };

  // Calculate totals
  const totalSales = filteredTransactions
    .filter(t => t.type === 'sale')
    .reduce((sum, t) => sum + t.amount, 0);
  
  const totalExpenses = filteredTransactions
    .filter(t => t.type === 'expense')
    .reduce((sum, t) => sum + Math.abs(t.amount), 0);
  
  const totalDeposits = filteredTransactions
    .filter(t => t.type === 'deposit')
    .reduce((sum, t) => sum + Math.abs(t.amount), 0);
  
  const netCashFlow = totalSales - totalExpenses - totalDeposits;

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Box>
        <PageHeader
          title="Cash History"
          subtitle="View and analyze your cash transactions"
        />

        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={12} md={3}>
                <TextField
                  fullWidth
                  placeholder="Search transactions"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <SearchIcon />
                      </InputAdornment>
                    ),
                  }}
                />
              </Grid>
              <Grid item xs={12} md={2}>
                <DatePicker
                  label="From Date"
                  value={startDate}
                  onChange={setStartDate}
                  slotProps={{ textField: { fullWidth: true, size: 'small' } }}
                />
              </Grid>
              <Grid item xs={12} md={2}>
                <DatePicker
                  label="To Date"
                  value={endDate}
                  onChange={setEndDate}
                  slotProps={{ textField: { fullWidth: true, size: 'small' } }}
                />
              </Grid>
              <Grid item xs={6} md={2}>
                <FormControl fullWidth size="small">
                  <InputLabel id="transaction-type-label">Transaction Type</InputLabel>
                  <Select
                    labelId="transaction-type-label"
                    value={transactionType}
                    label="Transaction Type"
                    onChange={(e) => setTransactionType(e.target.value)}
                  >
                    <MenuItem value="all">All Types</MenuItem>
                    <MenuItem value="sale">Sales</MenuItem>
                    <MenuItem value="expense">Expenses</MenuItem>
                    <MenuItem value="deposit">Deposits</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={6} md={2}>
                <FormControl fullWidth size="small">
                  <InputLabel id="payment-method-label">Payment Method</InputLabel>
                  <Select
                    labelId="payment-method-label"
                    value={paymentMethod}
                    label="Payment Method"
                    onChange={(e) => setPaymentMethod(e.target.value)}
                  >
                    <MenuItem value="all">All Methods</MenuItem>
                    <MenuItem value="cash">Cash</MenuItem>
                    <MenuItem value="upi">UPI</MenuItem>
                    <MenuItem value="card">Card</MenuItem>
                    <MenuItem value="bank_transfer">Bank Transfer</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} md={1}>
                <Button
                  variant="outlined"
                  color="primary"
                  onClick={clearFilters}
                  startIcon={<FilterIcon />}
                  fullWidth
                >
                  Clear
                </Button>
              </Grid>
            </Grid>
          </CardContent>
        </Card>

        <Grid container spacing={3} sx={{ mb: 3 }}>
          <Grid item xs={12} md={3}>
            <Card>
              <CardContent>
                <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                  Total Sales
                </Typography>
                <Typography variant="h5" color="primary" sx={{ fontWeight: 'bold' }}>
                  ₹{totalSales.toLocaleString()}
                </Typography>
                <Typography variant="caption" color="textSecondary">
                  {filteredTransactions.filter(t => t.type === 'sale').length} transactions
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={3}>
            <Card>
              <CardContent>
                <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                  Total Expenses
                </Typography>
                <Typography variant="h5" color="error" sx={{ fontWeight: 'bold' }}>
                  ₹{totalExpenses.toLocaleString()}
                </Typography>
                <Typography variant="caption" color="textSecondary">
                  {filteredTransactions.filter(t => t.type === 'expense').length} transactions
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={3}>
            <Card>
              <CardContent>
                <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                  Total Deposits
                </Typography>
                <Typography variant="h5" color="info.main" sx={{ fontWeight: 'bold' }}>
                  ₹{totalDeposits.toLocaleString()}
                </Typography>
                <Typography variant="caption" color="textSecondary">
                  {filteredTransactions.filter(t => t.type === 'deposit').length} transactions
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={3}>
            <Card>
              <CardContent>
                <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                  Net Cash Flow
                </Typography>
                <Typography 
                  variant="h5" 
                  color={netCashFlow >= 0 ? 'success.main' : 'error.main'} 
                  sx={{ fontWeight: 'bold' }}
                >
                  {netCashFlow >= 0 ? '+' : ''}₹{netCashFlow.toLocaleString()}
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  {netCashFlow >= 0 ? (
                    <IncomeIcon fontSize="small" color="success" sx={{ mr: 0.5 }} />
                  ) : (
                    <OutcomeIcon fontSize="small" color="error" sx={{ mr: 0.5 }} />
                  )}
                  <Typography variant="caption" color="textSecondary">
                    {netCashFlow >= 0 ? 'Positive' : 'Negative'} cash flow
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Cash Flow Trend
            </Typography>
            <Box sx={{ height: 300 }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={chartData}
                  margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <RechartsTooltip 
                    formatter={(value: any) => [`₹${value}`, '']}
                    labelFormatter={(label) => `Date: ${label}`}
                  />
                  <Legend />
                  <Bar dataKey="sales" name="Sales" fill="#5E35B1" />
                  <Bar dataKey="expenses" name="Expenses" fill="#D32F2F" />
                  <Bar dataKey="deposits" name="Deposits" fill="#1976D2" />
                </BarChart>
              </ResponsiveContainer>
            </Box>
          </CardContent>
        </Card>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          <Card>
            <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
              <Tabs 
                value={tabValue} 
                onChange={handleTabChange} 
                aria-label="transaction tabs"
                sx={{ px: 2 }}
              >
                <Tab label="All Transactions" />
                <Tab label="Sales" />
                <Tab label="Expenses" />
                <Tab label="Deposits" />
              </Tabs>
            </Box>
            
            <TabPanel value={tabValue} index={0}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h6">
                    All Transactions ({filteredTransactions.length})
                  </Typography>
                  <Box>
                    <Button
                      variant="outlined"
                      color="primary"
                      startIcon={<DownloadIcon />}
                      sx={{ mr: 1 }}
                      onClick={() => {
                        // In a real app, this would download the transactions
                        console.log('Downloading transactions');
                      }}
                    >
                      Export
                    </Button>
                    <Button
                      variant="outlined"
                      color="primary"
                      startIcon={<PrintIcon />}
                      onClick={() => {
                        // In a real app, this would print the transactions
                        console.log('Printing transactions');
                      }}
                    >
                      Print
                    </Button>
                  </Box>
                </Box>

                {renderTransactionsTable(filteredTransactions)}
              </CardContent>
            </TabPanel>
            
            <TabPanel value={tabValue} index={1}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h6">
                    Sales ({filteredTransactions.length})
                  </Typography>
                  <Box>
                    <Button
                      variant="outlined"
                      color="primary"
                      startIcon={<DownloadIcon />}
                      sx={{ mr: 1 }}
                      onClick={() => {
                        // In a real app, this would download the sales
                        console.log('Downloading sales');
                      }}
                    >
                      Export
                    </Button>
                    <Button
                      variant="outlined"
                      color="primary"
                      startIcon={<PrintIcon />}
                      onClick={() => {
                        // In a real app, this would print the sales
                        console.log('Printing sales');
                      }}
                    >
                      Print
                    </Button>
                  </Box>
                </Box>

                {renderTransactionsTable(filteredTransactions)}
              </CardContent>
            </TabPanel>
            
            <TabPanel value={tabValue} index={2}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h6">
                    Expenses ({filteredTransactions.length})
                  </Typography>
                  <Box>
                    <Button
                      variant="outlined"
                      color="primary"
                      startIcon={<DownloadIcon />}
                      sx={{ mr: 1 }}
                      onClick={() => {
                        // In a real app, this would download the expenses
                        console.log('Downloading expenses');
                      }}
                    >
                      Export
                    </Button>
                    <Button
                      variant="outlined"
                      color="primary"
                      startIcon={<PrintIcon />}
                      onClick={() => {
                        // In a real app, this would print the expenses
                        console.log('Printing expenses');
                      }}
                    >
                      Print
                    </Button>
                  </Box>
                </Box>

                {renderTransactionsTable(filteredTransactions)}
              </CardContent>
            </TabPanel>
            
            <TabPanel value={tabValue} index={3}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h6">
                    Deposits ({filteredTransactions.length})
                  </Typography>
                  <Box>
                    <Button
                      variant="outlined"
                      color="primary"
                      startIcon={<DownloadIcon />}
                      sx={{ mr: 1 }}
                      onClick={() => {
                        // In a real app, this would download the deposits
                        console.log('Downloading deposits');
                      }}
                    >
                      Export
                    </Button>
                    <Button
                      variant="outlined"
                      color="primary"
                      startIcon={<PrintIcon />}
                      onClick={() => {
                        // In a real app, this would print the deposits
                        console.log('Printing deposits');
                      }}
                    >
                      Print
                    </Button>
                  </Box>
                </Box>

                {renderTransactionsTable(filteredTransactions)}
              </CardContent>
            </TabPanel>
          </Card>
        </motion.div>

        {/* Details Dialog */}
        <Dialog
          open={detailsDialogOpen}
          onClose={() => setDetailsDialogOpen(false)}
          maxWidth="md"
          fullWidth
        >
          {selectedTransaction && (
            <>
              <DialogTitle>
                Transaction Details - {selectedTransaction.id}
                <Box sx={{ display: 'inline-block', ml: 2 }}>
                  {getTransactionTypeChip(selectedTransaction.type)}
                </Box>
              </DialogTitle>
              <DialogContent>
                <Grid container spacing={2}>
                  <Grid item xs={12} md={6}>
                    <Typography variant="subtitle2" color="textSecondary">
                      Transaction Information
                    </Typography>
                    <Typography variant="body1">
                      <strong>Reference:</strong> {selectedTransaction.reference}
                    </Typography>
                    <Typography variant="body2">
                      <strong>Date:</strong> {new Date(selectedTransaction.date).toLocaleDateString()}
                      {' '}
                      {new Date(selectedTransaction.date).toLocaleTimeString()}
                    </Typography>
                    <Typography variant="body2">
                      <strong>Amount:</strong> {selectedTransaction.amount < 0 ? '-' : ''}
                      ₹{Math.abs(selectedTransaction.amount).toLocaleString()}
                    </Typography>
                    <Box sx={{ mt: 1 }}>
                      {getPaymentMethodChip(selectedTransaction.method)}
                    </Box>
                  </Grid>
                  <Grid item xs={12} md={6}>
                    {selectedTransaction.type === 'sale' && (
                      <>
                        <Typography variant="subtitle2" color="textSecondary">
                          Sale Details
                        </Typography>
                        <Typography variant="body2">
                          <strong>Customer:</strong> {selectedTransaction.details.customer}
                        </Typography>
                        <Typography variant="body2">
                          <strong>Cashier:</strong> {selectedTransaction.details.cashier}
                        </Typography>
                        {selectedTransaction.details.upiReference && (
                          <Typography variant="body2">
                            <strong>UPI Reference:</strong> {selectedTransaction.details.upiReference}
                          </Typography>
                        )}
                        {selectedTransaction.details.cardReference && (
                          <Typography variant="body2">
                            <strong>Card Reference:</strong> {selectedTransaction.details.cardReference}
                          </Typography>
                        )}
                      </>
                    )}
                    {selectedTransaction.type === 'expense' && (
                      <>
                        <Typography variant="subtitle2" color="textSecondary">
                          Expense Details
                        </Typography>
                        <Typography variant="body2">
                          <strong>Category:</strong> {selectedTransaction.details.category}
                        </Typography>
                        <Typography variant="body2">
                          <strong>Paid To:</strong> {selectedTransaction.details.paidTo}
                        </Typography>
                        <Typography variant="body2">
                          <strong>Approved By:</strong> {selectedTransaction.details.approvedBy}
                        </Typography>
                      </>
                    )}
                    {selectedTransaction.type === 'deposit' && (
                      <>
                        <Typography variant="subtitle2" color="textSecondary">
                          Deposit Details
                        </Typography>
                        <Typography variant="body2">
                          <strong>Bank:</strong> {selectedTransaction.details.bank}
                        </Typography>
                        <Typography variant="body2">
                          <strong>Account:</strong> {selectedTransaction.details.accountNumber}
                        </Typography>
                        <Typography variant="body2">
                          <strong>Approved By:</strong> {selectedTransaction.details.approvedBy}
                        </Typography>
                      </>
                    )}
                  </Grid>
                  {selectedTransaction.type === 'sale' && selectedTransaction.details.items && (
                    <Grid item xs={12}>
                      <Divider sx={{ my: 2 }} />
                      <Typography variant="subtitle2" color="textSecondary">
                        Items
                      </Typography>
                      <TableContainer component={Paper} variant="outlined" sx={{ mt: 1 }}>
                        <Table size="small">
                          <TableHead>
                            <TableRow>
                              <TableCell>Product</TableCell>
                              <TableCell align="center">Quantity</TableCell>
                              <TableCell align="right">Price</TableCell>
                              <TableCell align="right">Total</TableCell>
                            </TableRow>
                          </TableHead>
                          <TableBody>
                            {selectedTransaction.details.items.map((item: any, index: number) => (
                              <TableRow key={index}>
                                <TableCell>{item.name}</TableCell>
                                <TableCell align="center">{item.quantity}</TableCell>
                                <TableCell align="right">₹{item.price.toLocaleString()}</TableCell>
                                <TableCell align="right">₹{(item.price * item.quantity).toLocaleString()}</TableCell>
                              </TableRow>
                            ))}
                            <TableRow>
                              <TableCell colSpan={3} align="right" sx={{ fontWeight: 'bold' }}>
                                Total:
                              </TableCell>
                              <TableCell align="right" sx={{ fontWeight: 'bold' }}>
                                ₹{selectedTransaction.amount.toLocaleString()}
                              </TableCell>
                            </TableRow>
                          </TableBody>
                        </Table>
                      </TableContainer>
                    </Grid>
                  )}
                  {selectedTransaction.details.notes && (
                    <Grid item xs={12}>
                      <Typography variant="subtitle2" color="textSecondary" sx={{ mt: 2 }}>
                        Notes
                      </Typography>
                      <Paper variant="outlined" sx={{ p: 2, mt: 1, backgroundColor: 'background.default' }}>
                        <Typography variant="body2">
                          {selectedTransaction.details.notes}
                        </Typography>
                      </Paper>
                    </Grid>
                  )}
                </Grid>
              </DialogContent>
              <DialogActions>
                <Button
                  startIcon={<PrintIcon />}
                  onClick={() => {
                    console.log(`Printing transaction ${selectedTransaction.id}`);
                    // In a real app, this would trigger printing
                  }}
                >
                  Print
                </Button>
                <Button
                  startIcon={<ShareIcon />}
                  onClick={() => {
                    console.log(`Sharing transaction ${selectedTransaction.id}`);
                    // In a real app, this would open sharing options
                  }}
                >
                  Share
                </Button>
                <Button onClick={() => setDetailsDialogOpen(false)}>
                  Close
                </Button>
              </DialogActions>
            </>
          )}
        </Dialog>
      </Box>
    </LocalizationProvider>
  );

  function renderTransactionsTable(transactions: any[]) {
    return transactions.length > 0 ? (
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Date & Time</TableCell>
              <TableCell>Type</TableCell>
              <TableCell>Reference</TableCell>
              <TableCell>Details</TableCell>
              <TableCell align="right">Amount</TableCell>
              <TableCell>Method</TableCell>
              <TableCell align="center">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {transactions.map((transaction) => (
              <TableRow key={transaction.id} hover>
                <TableCell>{transaction.id}</TableCell>
                <TableCell>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <CalendarIcon fontSize="small" sx={{ mr: 1, color: 'text.secondary' }} />
                    <Box>
                      <Typography variant="body2">
                        {new Date(transaction.date).toLocaleDateString()}
                      </Typography>
                      <Typography variant="caption" color="textSecondary">
                        {new Date(transaction.date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </Typography>
                    </Box>
                  </Box>
                </TableCell>
                <TableCell>
                  {getTransactionTypeChip(transaction.type)}
                </TableCell>
                <TableCell>{transaction.reference}</TableCell>
                <TableCell>
                  {transaction.type === 'sale' && (
                    <Typography variant="body2">
                      {transaction.details.customer}
                    </Typography>
                  )}
                  {transaction.type === 'expense' && (
                    <Typography variant="body2">
                      {transaction.details.category} - {transaction.details.paidTo}
                    </Typography>
                  )}
                  {transaction.type === 'deposit' && (
                    <Typography variant="body2">
                      {transaction.details.bank}
                    </Typography>
                  )}
                </TableCell>
                <TableCell align="right">
                  <Typography 
                    variant="body2" 
                    sx={{ 
                      fontWeight: 'medium',
                      color: transaction.amount < 0 ? 'error.main' : 'success.main',
                    }}
                  >
                    {transaction.amount < 0 ? '-' : ''}₹{Math.abs(transaction.amount).toLocaleString()}
                  </Typography>
                </TableCell>
                <TableCell>
                  {getPaymentMethodChip(transaction.method)}
                </TableCell>
                <TableCell align="center">
                  <Tooltip title="View Details">
                    <IconButton
                      size="small"
                      color="primary"
                      onClick={() => handleViewDetails(transaction)}
                    >
                      <ViewIcon fontSize="small" />
                    </IconButton>
                  </Tooltip>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    ) : (
      <Paper
        sx={{
          p: 3,
          textAlign: 'center',
          backgroundColor: 'background.default',
        }}
      >
        <CashIcon sx={{ fontSize: 40, color: 'text.secondary', mb: 1 }} />
        <Typography variant="h6" color="textSecondary">
          No transactions found
        </Typography>
        <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
          {searchQuery || startDate || endDate || transactionType !== 'all' || paymentMethod !== 'all'
            ? 'Try changing your search criteria'
            : 'No transactions available for the selected period'}
        </Typography>
        {(searchQuery || startDate || endDate || transactionType !== 'all' || paymentMethod !== 'all') && (
          <Button
            variant="outlined"
            color="primary"
            onClick={clearFilters}
            startIcon={<FilterIcon />}
          >
            Clear Filters
          </Button>
        )}
      </Paper>
    );
  }
};

export default CashHistory;