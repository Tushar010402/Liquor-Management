import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  IconButton,
  Chip,
  Grid,
  Divider,
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
  Paper,
  InputAdornment,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Tab,
  Tabs,
} from '@mui/material';
import {
  Search,
  FilterList,
  Visibility,
  Print,
  Receipt,
  LocalAtm,
  CreditCard,
  AccountBalance,
  CalendarToday,
} from '@mui/icons-material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { useNavigate } from 'react-router-dom';
import { PageHeader, DataTable } from '../../../components/common';

// Mock data for sales
const salesData = [
  { 
    id: 1, 
    invoice: 'INV-2023-1234', 
    date: '2023-11-25', 
    time: '14:30',
    customer: 'John Doe', 
    items: 5, 
    total: 3500, 
    payment: 'Cash', 
    status: 'Completed' 
  },
  { 
    id: 2, 
    invoice: 'INV-2023-1235', 
    date: '2023-11-25', 
    time: '15:45',
    customer: 'Jane Smith', 
    items: 3, 
    total: 2800, 
    payment: 'UPI', 
    status: 'Completed' 
  },
  { 
    id: 3, 
    invoice: 'INV-2023-1236', 
    date: '2023-11-25', 
    time: '16:20',
    customer: 'Mike Johnson', 
    items: 7, 
    total: 5200, 
    payment: 'Card', 
    status: 'Completed' 
  },
  { 
    id: 4, 
    invoice: 'INV-2023-1237', 
    date: '2023-11-25', 
    time: '17:10',
    customer: 'Sarah Williams', 
    items: 2, 
    total: 1800, 
    payment: 'Cash', 
    status: 'Completed' 
  },
  { 
    id: 5, 
    invoice: 'INV-2023-1238', 
    date: '2023-11-24', 
    time: '11:15',
    customer: 'David Brown', 
    items: 4, 
    total: 3200, 
    payment: 'UPI', 
    status: 'Completed' 
  },
  { 
    id: 6, 
    invoice: 'INV-2023-1239', 
    date: '2023-11-24', 
    time: '12:45',
    customer: 'Emily Davis', 
    items: 6, 
    total: 4500, 
    payment: 'Cash', 
    status: 'Completed' 
  },
  { 
    id: 7, 
    invoice: 'INV-2023-1240', 
    date: '2023-11-24', 
    time: '14:20',
    customer: 'Robert Wilson', 
    items: 3, 
    total: 2200, 
    payment: 'Card', 
    status: 'Completed' 
  },
  { 
    id: 8, 
    invoice: 'INV-2023-1241', 
    date: '2023-11-23', 
    time: '10:30',
    customer: 'Jennifer Taylor', 
    items: 5, 
    total: 3800, 
    payment: 'Cash', 
    status: 'Completed' 
  },
  { 
    id: 9, 
    invoice: 'INV-2023-1242', 
    date: '2023-11-23', 
    time: '16:15',
    customer: 'Michael Anderson', 
    items: 8, 
    total: 6200, 
    payment: 'UPI', 
    status: 'Completed' 
  },
  { 
    id: 10, 
    invoice: 'INV-2023-1243', 
    date: '2023-11-22', 
    time: '18:45',
    customer: 'Lisa Thomas', 
    items: 4, 
    total: 3500, 
    payment: 'Cash', 
    status: 'Completed' 
  },
];

// Mock data for sale details
const saleDetailsData = {
  id: 1,
  invoice: 'INV-2023-1234',
  date: '2023-11-25',
  time: '14:30',
  customer: {
    name: 'John Doe',
    phone: '9876543210',
  },
  items: [
    { id: 1, name: 'Johnnie Walker Black Label', category: 'Whisky', price: 3500, quantity: 1, total: 3500 },
    { id: 2, name: 'Absolut Vodka', category: 'Vodka', price: 1800, quantity: 2, total: 3600 },
    { id: 3, name: 'Jack Daniels', category: 'Whisky', price: 2800, quantity: 1, total: 2800 },
  ],
  subtotal: 9900,
  discount: 400,
  total: 9500,
  payment: {
    method: 'Cash',
    amount: 10000,
    change: 500,
  },
  status: 'Completed',
  createdBy: 'Executive User',
};

interface SaleDetailsDialogProps {
  open: boolean;
  onClose: () => void;
  saleData: any;
}

const SaleDetailsDialog: React.FC<SaleDetailsDialogProps> = ({ open, onClose, saleData }) => {
  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h6">Sale Details</Typography>
          <Chip 
            label={saleData.status} 
            color="success" 
            size="small" 
          />
        </Box>
      </DialogTitle>
      <DialogContent>
        <Grid container spacing={2} sx={{ mb: 3 }}>
          <Grid item xs={12} sm={6}>
            <Typography variant="body2" color="textSecondary">Invoice Number</Typography>
            <Typography variant="body1" sx={{ fontWeight: 500 }}>{saleData.invoice}</Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Typography variant="body2" color="textSecondary">Date & Time</Typography>
            <Typography variant="body1">{saleData.date} {saleData.time}</Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Typography variant="body2" color="textSecondary">Customer</Typography>
            <Typography variant="body1">{saleData.customer.name}</Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Typography variant="body2" color="textSecondary">Phone</Typography>
            <Typography variant="body1">{saleData.customer.phone}</Typography>
          </Grid>
        </Grid>

        <Typography variant="subtitle1" gutterBottom>Items</Typography>
        <TableContainer component={Paper} variant="outlined" sx={{ mb: 3 }}>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Product</TableCell>
                <TableCell align="right">Price</TableCell>
                <TableCell align="center">Quantity</TableCell>
                <TableCell align="right">Total</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {saleData.items.map((item: any) => (
                <TableRow key={item.id}>
                  <TableCell>
                    <Typography variant="body2" sx={{ fontWeight: 500 }}>
                      {item.name}
                    </Typography>
                    <Typography variant="caption" color="textSecondary">
                      {item.category}
                    </Typography>
                  </TableCell>
                  <TableCell align="right">₹{item.price}</TableCell>
                  <TableCell align="center">{item.quantity}</TableCell>
                  <TableCell align="right">₹{item.total}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>

        <Grid container spacing={2} sx={{ mb: 3 }}>
          <Grid item xs={12} sm={6}>
            <Typography variant="body2" color="textSecondary">Payment Method</Typography>
            <Typography variant="body1">{saleData.payment.method}</Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Typography variant="body2" color="textSecondary">Created By</Typography>
            <Typography variant="body1">{saleData.createdBy}</Typography>
          </Grid>
        </Grid>

        <Divider sx={{ my: 2 }} />

        <Grid container spacing={2}>
          <Grid item xs={6}>
            <Typography variant="body1">Subtotal:</Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography variant="body1" align="right">₹{saleData.subtotal}</Typography>
          </Grid>
          
          <Grid item xs={6}>
            <Typography variant="body1">Discount:</Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography variant="body1" align="right">₹{saleData.discount}</Typography>
          </Grid>
          
          <Grid item xs={6}>
            <Typography variant="h6">Total:</Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography variant="h6" align="right">₹{saleData.total}</Typography>
          </Grid>

          {saleData.payment.method === 'Cash' && (
            <>
              <Grid item xs={6}>
                <Typography variant="body1">Amount Received:</Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography variant="body1" align="right">₹{saleData.payment.amount}</Typography>
              </Grid>
              
              <Grid item xs={6}>
                <Typography variant="body1">Change:</Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography variant="body1" align="right">₹{saleData.payment.change}</Typography>
              </Grid>
            </>
          )}
        </Grid>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Close</Button>
        <Button 
          variant="contained" 
          color="primary"
          startIcon={<Print />}
        >
          Print Receipt
        </Button>
      </DialogActions>
    </Dialog>
  );
};

const MySales: React.FC = () => {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [filterAnchorEl, setFilterAnchorEl] = useState<null | HTMLElement>(null);
  const [tabValue, setTabValue] = useState(0);
  const [startDate, setStartDate] = useState<Date | null>(null);
  const [endDate, setEndDate] = useState<Date | null>(null);
  const [paymentMethod, setPaymentMethod] = useState('all');
  const [detailsDialogOpen, setDetailsDialogOpen] = useState(false);
  const [selectedSale, setSelectedSale] = useState<any>(null);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleViewDetails = (sale: any) => {
    setSelectedSale(saleDetailsData);
    setDetailsDialogOpen(true);
  };

  const handleCloseDetailsDialog = () => {
    setDetailsDialogOpen(false);
  };

  const columns = [
    { 
      field: 'invoice', 
      headerName: 'Invoice', 
      width: 150,
      renderCell: (params: any) => (
        <Typography variant="body2" sx={{ fontWeight: 500 }}>
          {params.value}
        </Typography>
      ),
    },
    { 
      field: 'date', 
      headerName: 'Date & Time', 
      width: 180,
      renderCell: (params: any) => (
        <Typography variant="body2">
          {params.row.date} {params.row.time}
        </Typography>
      ),
    },
    { 
      field: 'customer', 
      headerName: 'Customer', 
      width: 180,
    },
    { 
      field: 'items', 
      headerName: 'Items', 
      width: 100,
      align: 'center',
    },
    { 
      field: 'total', 
      headerName: 'Total', 
      width: 120,
      renderCell: (params: any) => (
        <Typography variant="body2" sx={{ fontWeight: 500 }}>
          ₹{params.value}
        </Typography>
      ),
    },
    { 
      field: 'payment', 
      headerName: 'Payment', 
      width: 120,
      renderCell: (params: any) => (
        <Chip 
          label={params.value} 
          size="small" 
          color={
            params.value === 'Cash' ? 'success' : 
            params.value === 'UPI' ? 'primary' : 
            'secondary'
          }
        />
      ),
    },
    { 
      field: 'status', 
      headerName: 'Status', 
      width: 120,
      renderCell: (params: any) => (
        <Chip 
          label={params.value} 
          size="small" 
          color={
            params.value === 'Completed' ? 'success' : 
            params.value === 'Pending' ? 'warning' : 
            'error'
          }
        />
      ),
    },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 120,
      renderCell: (params: any) => (
        <Box>
          <IconButton 
            size="small" 
            onClick={() => handleViewDetails(params.row)}
            color="primary"
          >
            <Visibility fontSize="small" />
          </IconButton>
          <IconButton 
            size="small" 
            color="secondary"
          >
            <Print fontSize="small" />
          </IconButton>
        </Box>
      ),
    },
  ];

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Box>
        <PageHeader
          title="My Sales"
          subtitle="View and manage your sales transactions"
          actionText="New Sale"
          actionIcon={<Receipt />}
          onActionClick={() => navigate('/executive/new-sale')}
        />

        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={12} md={4}>
                <TextField
                  fullWidth
                  placeholder="Search by invoice, customer..."
                  variant="outlined"
                  size="small"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <Search fontSize="small" />
                      </InputAdornment>
                    ),
                  }}
                />
              </Grid>
              <Grid item xs={12} md={8}>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={4}>
                    <DatePicker
                      label="From Date"
                      value={startDate}
                      onChange={(newValue) => setStartDate(newValue)}
                      slotProps={{ textField: { size: 'small', fullWidth: true } }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={4}>
                    <DatePicker
                      label="To Date"
                      value={endDate}
                      onChange={(newValue) => setEndDate(newValue)}
                      slotProps={{ textField: { size: 'small', fullWidth: true } }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={4}>
                    <FormControl fullWidth size="small">
                      <InputLabel id="payment-method-filter-label">Payment Method</InputLabel>
                      <Select
                        labelId="payment-method-filter-label"
                        id="payment-method-filter"
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
                </Grid>
              </Grid>
            </Grid>
          </CardContent>
        </Card>

        <Box sx={{ mb: 3 }}>
          <Tabs 
            value={tabValue} 
            onChange={handleTabChange}
            variant="scrollable"
            scrollButtons="auto"
          >
            <Tab label="All Sales" />
            <Tab label="Today" />
            <Tab label="Yesterday" />
            <Tab label="This Week" />
            <Tab label="This Month" />
          </Tabs>
        </Box>

        <DataTable
          title="Sales Transactions"
          rows={salesData}
          columns={columns}
          loading={false}
          height={600}
        />

        {selectedSale && (
          <SaleDetailsDialog
            open={detailsDialogOpen}
            onClose={handleCloseDetailsDialog}
            saleData={selectedSale}
          />
        )}
      </Box>
    </LocalizationProvider>
  );
};

export default MySales;