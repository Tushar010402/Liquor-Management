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
  TextField,
  InputAdornment,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import {
  Search as SearchIcon,
  FilterList as FilterIcon,
  FileDownload as DownloadIcon,
  Print as PrintIcon,
  LocalAtm as CashIcon,
  AccountBalance as BankIcon,
  CreditCard as CardIcon,
  PhoneAndroid as UpiIcon,
  CalendarToday as CalendarIcon,
} from '@mui/icons-material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { motion } from 'framer-motion';
import { PageHeader } from '../../../components/common';
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Legend,
  Tooltip as RechartsTooltip,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  LineChart,
  Line,
} from 'recharts';

// Mock payment data
const mockPaymentData = [
  {
    date: '2023-11-25',
    cash: 12500,
    upi: 8200,
    card: 5500,
    total: 26200,
    transactions: 15,
  },
  {
    date: '2023-11-24',
    cash: 10800,
    upi: 7500,
    card: 6200,
    total: 24500,
    transactions: 14,
  },
  {
    date: '2023-11-23',
    cash: 11200,
    upi: 9100,
    card: 4800,
    total: 25100,
    transactions: 16,
  },
  {
    date: '2023-11-22',
    cash: 9800,
    upi: 6800,
    card: 7200,
    total: 23800,
    transactions: 13,
  },
  {
    date: '2023-11-21',
    cash: 13500,
    upi: 7900,
    card: 5100,
    total: 26500,
    transactions: 17,
  },
  {
    date: '2023-11-20',
    cash: 10200,
    upi: 8500,
    card: 6800,
    total: 25500,
    transactions: 15,
  },
  {
    date: '2023-11-19',
    cash: 9500,
    upi: 7200,
    card: 5800,
    total: 22500,
    transactions: 12,
  },
];

// Mock daily payment breakdown
const mockDailyBreakdown = [
  { time: '9-10 AM', cash: 1200, upi: 800, card: 500 },
  { time: '10-11 AM', cash: 1500, upi: 1200, card: 700 },
  { time: '11-12 PM', cash: 1800, upi: 1500, card: 900 },
  { time: '12-1 PM', cash: 2200, upi: 1800, card: 1100 },
  { time: '1-2 PM', cash: 1900, upi: 1600, card: 800 },
  { time: '2-3 PM', cash: 1600, upi: 1300, card: 600 },
  { time: '3-4 PM', cash: 1400, upi: 1100, card: 500 },
  { time: '4-5 PM', cash: 1700, upi: 1400, card: 700 },
  { time: '5-6 PM', cash: 2000, upi: 1700, card: 900 },
  { time: '6-7 PM', cash: 2300, upi: 2000, card: 1200 },
  { time: '7-8 PM', cash: 2500, upi: 2200, card: 1300 },
  { time: '8-9 PM', cash: 2100, upi: 1900, card: 1000 },
];

// Colors for charts
const COLORS = ['#4CAF50', '#9C27B0', '#2196F3'];

const PaymentBreakdown: React.FC = () => {
  const [startDate, setStartDate] = useState<Date | null>(null);
  const [endDate, setEndDate] = useState<Date | null>(null);
  const [paymentMethod, setPaymentMethod] = useState<string>('all');
  const [timeFrame, setTimeFrame] = useState<string>('daily');
  const [paymentData] = useState(mockPaymentData);
  const [dailyBreakdown] = useState(mockDailyBreakdown);

  // Calculate totals
  const totalCash = paymentData.reduce((sum, day) => sum + day.cash, 0);
  const totalUpi = paymentData.reduce((sum, day) => sum + day.upi, 0);
  const totalCard = paymentData.reduce((sum, day) => sum + day.card, 0);
  const grandTotal = totalCash + totalUpi + totalCard;
  const totalTransactions = paymentData.reduce((sum, day) => sum + day.transactions, 0);

  // Prepare data for pie chart
  const pieChartData = [
    { name: 'Cash', value: totalCash },
    { name: 'UPI', value: totalUpi },
    { name: 'Card', value: totalCard },
  ];

  // Prepare data for trend chart
  const trendChartData = paymentData.map(day => ({
    date: new Date(day.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    cash: day.cash,
    upi: day.upi,
    card: day.card,
  }));

  const clearFilters = () => {
    setStartDate(null);
    setEndDate(null);
    setPaymentMethod('all');
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Box>
        <PageHeader
          title="Payment Breakdown"
          subtitle="Analyze payment methods and trends"
        />

        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={12} md={3}>
                <DatePicker
                  label="From Date"
                  value={startDate}
                  onChange={setStartDate}
                  slotProps={{ textField: { fullWidth: true, size: 'small' } }}
                />
              </Grid>
              <Grid item xs={12} md={3}>
                <DatePicker
                  label="To Date"
                  value={endDate}
                  onChange={setEndDate}
                  slotProps={{ textField: { fullWidth: true, size: 'small' } }}
                />
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
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={6} md={2}>
                <FormControl fullWidth size="small">
                  <InputLabel id="timeframe-label">Time Frame</InputLabel>
                  <Select
                    labelId="timeframe-label"
                    value={timeFrame}
                    label="Time Frame"
                    onChange={(e) => setTimeFrame(e.target.value)}
                  >
                    <MenuItem value="daily">Daily</MenuItem>
                    <MenuItem value="weekly">Weekly</MenuItem>
                    <MenuItem value="monthly">Monthly</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} md={2}>
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <Button
                    variant="outlined"
                    color="primary"
                    onClick={clearFilters}
                    startIcon={<FilterIcon />}
                    fullWidth
                  >
                    Clear
                  </Button>
                  <Button
                    variant="outlined"
                    color="primary"
                    startIcon={<DownloadIcon />}
                    fullWidth
                    onClick={() => {
                      // In a real app, this would download the report
                      console.log('Downloading report');
                    }}
                  >
                    Export
                  </Button>
                </Box>
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
                  ₹{grandTotal.toLocaleString()}
                </Typography>
                <Typography variant="caption" color="textSecondary">
                  {totalTransactions} transactions
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={3}>
            <Card>
              <CardContent>
                <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                  Cash Payments
                </Typography>
                <Typography variant="h5" color="success.main" sx={{ fontWeight: 'bold' }}>
                  ₹{totalCash.toLocaleString()}
                </Typography>
                <Typography variant="caption" color="textSecondary">
                  {((totalCash / grandTotal) * 100).toFixed(1)}% of total
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={3}>
            <Card>
              <CardContent>
                <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                  UPI Payments
                </Typography>
                <Typography variant="h5" sx={{ fontWeight: 'bold', color: '#9C27B0' }}>
                  ₹{totalUpi.toLocaleString()}
                </Typography>
                <Typography variant="caption" color="textSecondary">
                  {((totalUpi / grandTotal) * 100).toFixed(1)}% of total
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={3}>
            <Card>
              <CardContent>
                <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                  Card Payments
                </Typography>
                <Typography variant="h5" color="info.main" sx={{ fontWeight: 'bold' }}>
                  ₹{totalCard.toLocaleString()}
                </Typography>
                <Typography variant="caption" color="textSecondary">
                  {((totalCard / grandTotal) * 100).toFixed(1)}% of total
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        <Grid container spacing={3}>
          <Grid item xs={12} md={5}>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <Card sx={{ height: '100%' }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Payment Method Distribution
                  </Typography>
                  <Box sx={{ height: 300 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={pieChartData}
                          cx="50%"
                          cy="50%"
                          labelLine={false}
                          outerRadius={80}
                          fill="#8884d8"
                          dataKey="value"
                          label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(1)}%`}
                        >
                          {pieChartData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                          ))}
                        </Pie>
                        <Legend />
                        <RechartsTooltip 
                          formatter={(value: any) => [`₹${value.toLocaleString()}`, '']}
                        />
                      </PieChart>
                    </ResponsiveContainer>
                  </Box>
                  <Divider sx={{ my: 2 }} />
                  <Grid container spacing={2}>
                    <Grid item xs={4}>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <CashIcon sx={{ color: COLORS[0], mr: 1 }} />
                        <Box>
                          <Typography variant="body2">Cash</Typography>
                          <Typography variant="body1" sx={{ fontWeight: 'medium' }}>
                            {((totalCash / grandTotal) * 100).toFixed(1)}%
                          </Typography>
                        </Box>
                      </Box>
                    </Grid>
                    <Grid item xs={4}>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <UpiIcon sx={{ color: COLORS[1], mr: 1 }} />
                        <Box>
                          <Typography variant="body2">UPI</Typography>
                          <Typography variant="body1" sx={{ fontWeight: 'medium' }}>
                            {((totalUpi / grandTotal) * 100).toFixed(1)}%
                          </Typography>
                        </Box>
                      </Box>
                    </Grid>
                    <Grid item xs={4}>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <CardIcon sx={{ color: COLORS[2], mr: 1 }} />
                        <Box>
                          <Typography variant="body2">Card</Typography>
                          <Typography variant="body1" sx={{ fontWeight: 'medium' }}>
                            {((totalCard / grandTotal) * 100).toFixed(1)}%
                          </Typography>
                        </Box>
                      </Box>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            </motion.div>
          </Grid>
          <Grid item xs={12} md={7}>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: 0.1 }}
            >
              <Card sx={{ height: '100%' }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Payment Method Trends
                  </Typography>
                  <Box sx={{ height: 300 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart
                        data={trendChartData}
                        margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                      >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="date" />
                        <YAxis />
                        <RechartsTooltip 
                          formatter={(value: any) => [`₹${value.toLocaleString()}`, '']}
                        />
                        <Legend />
                        <Line type="monotone" dataKey="cash" name="Cash" stroke={COLORS[0]} activeDot={{ r: 8 }} />
                        <Line type="monotone" dataKey="upi" name="UPI" stroke={COLORS[1]} />
                        <Line type="monotone" dataKey="card" name="Card" stroke={COLORS[2]} />
                      </LineChart>
                    </ResponsiveContainer>
                  </Box>
                </CardContent>
              </Card>
            </motion.div>
          </Grid>
          <Grid item xs={12}>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: 0.2 }}
            >
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Hourly Payment Breakdown (Today)
                  </Typography>
                  <Box sx={{ height: 300 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart
                        data={dailyBreakdown}
                        margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                      >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="time" />
                        <YAxis />
                        <RechartsTooltip 
                          formatter={(value: any) => [`₹${value.toLocaleString()}`, '']}
                        />
                        <Legend />
                        <Bar dataKey="cash" name="Cash" fill={COLORS[0]} />
                        <Bar dataKey="upi" name="UPI" fill={COLORS[1]} />
                        <Bar dataKey="card" name="Card" fill={COLORS[2]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </Box>
                </CardContent>
              </Card>
            </motion.div>
          </Grid>
          <Grid item xs={12}>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: 0.3 }}
            >
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                    <Typography variant="h6">
                      Daily Payment Breakdown
                    </Typography>
                    <Button
                      variant="outlined"
                      color="primary"
                      startIcon={<PrintIcon />}
                      onClick={() => {
                        // In a real app, this would print the report
                        console.log('Printing report');
                      }}
                    >
                      Print Report
                    </Button>
                  </Box>
                  <TableContainer>
                    <Table>
                      <TableHead>
                        <TableRow>
                          <TableCell>Date</TableCell>
                          <TableCell align="right">Cash</TableCell>
                          <TableCell align="right">UPI</TableCell>
                          <TableCell align="right">Card</TableCell>
                          <TableCell align="right">Total</TableCell>
                          <TableCell align="center">Transactions</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {paymentData.map((day) => (
                          <TableRow key={day.date} hover>
                            <TableCell>
                              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                <CalendarIcon fontSize="small" sx={{ mr: 1, color: 'text.secondary' }} />
                                {new Date(day.date).toLocaleDateString()}
                              </Box>
                            </TableCell>
                            <TableCell align="right">
                              <Typography 
                                variant="body2" 
                                sx={{ 
                                  fontWeight: 'medium',
                                  color: 'success.main',
                                }}
                              >
                                ₹{day.cash.toLocaleString()}
                              </Typography>
                              <Typography variant="caption" color="textSecondary">
                                {((day.cash / day.total) * 100).toFixed(1)}%
                              </Typography>
                            </TableCell>
                            <TableCell align="right">
                              <Typography 
                                variant="body2" 
                                sx={{ 
                                  fontWeight: 'medium',
                                  color: '#9C27B0',
                                }}
                              >
                                ₹{day.upi.toLocaleString()}
                              </Typography>
                              <Typography variant="caption" color="textSecondary">
                                {((day.upi / day.total) * 100).toFixed(1)}%
                              </Typography>
                            </TableCell>
                            <TableCell align="right">
                              <Typography 
                                variant="body2" 
                                sx={{ 
                                  fontWeight: 'medium',
                                  color: 'info.main',
                                }}
                              >
                                ₹{day.card.toLocaleString()}
                              </Typography>
                              <Typography variant="caption" color="textSecondary">
                                {((day.card / day.total) * 100).toFixed(1)}%
                              </Typography>
                            </TableCell>
                            <TableCell align="right">
                              <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                                ₹{day.total.toLocaleString()}
                              </Typography>
                            </TableCell>
                            <TableCell align="center">
                              {day.transactions}
                            </TableCell>
                          </TableRow>
                        ))}
                        <TableRow>
                          <TableCell sx={{ fontWeight: 'bold' }}>Total</TableCell>
                          <TableCell align="right" sx={{ fontWeight: 'bold', color: 'success.main' }}>
                            ₹{totalCash.toLocaleString()}
                          </TableCell>
                          <TableCell align="right" sx={{ fontWeight: 'bold', color: '#9C27B0' }}>
                            ₹{totalUpi.toLocaleString()}
                          </TableCell>
                          <TableCell align="right" sx={{ fontWeight: 'bold', color: 'info.main' }}>
                            ₹{totalCard.toLocaleString()}
                          </TableCell>
                          <TableCell align="right" sx={{ fontWeight: 'bold' }}>
                            ₹{grandTotal.toLocaleString()}
                          </TableCell>
                          <TableCell align="center" sx={{ fontWeight: 'bold' }}>
                            {totalTransactions}
                          </TableCell>
                        </TableRow>
                      </TableBody>
                    </Table>
                  </TableContainer>
                </CardContent>
              </Card>
            </motion.div>
          </Grid>
        </Grid>
      </Box>
    </LocalizationProvider>
  );
};

export default PaymentBreakdown;