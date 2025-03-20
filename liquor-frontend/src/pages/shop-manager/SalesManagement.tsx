import React, { useState } from 'react';
import {
  Box,
  Container,
  Typography,
  Button,
  Card,
  CardContent,
  Grid,
  TextField,
  InputAdornment,
  IconButton,
  Chip,
  Menu,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  FormHelperText,
  Tabs,
  Tab,
  Divider,
  Avatar,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  useTheme,
} from '@mui/material';
import {
  Search as SearchIcon,
  Add as AddIcon,
  FilterList as FilterListIcon,
  MoreVert as MoreVertIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  ShoppingCart as ShoppingCartIcon,
  Receipt as ReceiptIcon,
  Print as PrintIcon,
  Visibility as VisibilityIcon,
  Cancel as CancelIcon,
  Person as PersonIcon,
  CalendarToday as CalendarTodayIcon,
  AttachMoney as AttachMoneyIcon,
  LocalShipping as LocalShippingIcon,
  Download as DownloadIcon,
} from '@mui/icons-material';
import { DataTable, PageHeader } from '../../components/common';
import { useTranslations, useFormValidation, useGlobalConfirmDialog } from '../../hooks';
import * as Yup from 'yup';
import { format } from 'date-fns';

// Mock data for sales
const mockSales = [
  {
    id: 1,
    invoice_number: 'INV-2023-0001',
    customer_name: 'John Doe',
    customer_phone: '9876543210',
    date: '2023-06-15',
    time: '14:30',
    items: 3,
    total: 2500,
    payment_method: 'cash',
    status: 'completed',
    created_by: 'Robert Johnson',
  },
  {
    id: 2,
    invoice_number: 'INV-2023-0002',
    customer_name: 'Jane Smith',
    customer_phone: '9876543211',
    date: '2023-06-15',
    time: '15:45',
    items: 2,
    total: 1800,
    payment_method: 'card',
    status: 'completed',
    created_by: 'Robert Johnson',
  },
  {
    id: 3,
    invoice_number: 'INV-2023-0003',
    customer_name: 'Michael Wilson',
    customer_phone: '9876543212',
    date: '2023-06-15',
    time: '16:20',
    items: 5,
    total: 4200,
    payment_method: 'upi',
    status: 'completed',
    created_by: 'Emily Davis',
  },
  {
    id: 4,
    invoice_number: 'INV-2023-0004',
    customer_name: 'Emily Davis',
    customer_phone: '9876543213',
    date: '2023-06-15',
    time: '17:10',
    items: 1,
    total: 950,
    payment_method: 'cash',
    status: 'completed',
    created_by: 'Emily Davis',
  },
  {
    id: 5,
    invoice_number: 'INV-2023-0005',
    customer_name: 'Robert Johnson',
    customer_phone: '9876543214',
    date: '2023-06-15',
    time: '18:05',
    items: 4,
    total: 3100,
    payment_method: 'card',
    status: 'completed',
    created_by: 'Robert Johnson',
  },
  {
    id: 6,
    invoice_number: 'INV-2023-0006',
    customer_name: 'Sarah Brown',
    customer_phone: '9876543215',
    date: '2023-06-16',
    time: '10:15',
    items: 2,
    total: 1500,
    payment_method: 'cash',
    status: 'completed',
    created_by: 'Robert Johnson',
  },
  {
    id: 7,
    invoice_number: 'INV-2023-0007',
    customer_name: 'David Miller',
    customer_phone: '9876543216',
    date: '2023-06-16',
    time: '11:30',
    items: 3,
    total: 2200,
    payment_method: 'upi',
    status: 'completed',
    created_by: 'Emily Davis',
  },
  {
    id: 8,
    invoice_number: 'INV-2023-0008',
    customer_name: 'Jennifer Lee',
    customer_phone: '9876543217',
    date: '2023-06-16',
    time: '12:45',
    items: 1,
    total: 800,
    payment_method: 'cash',
    status: 'cancelled',
    created_by: 'Robert Johnson',
  },
  {
    id: 9,
    invoice_number: 'INV-2023-0009',
    customer_name: 'William Taylor',
    customer_phone: '9876543218',
    date: '2023-06-16',
    time: '14:00',
    items: 6,
    total: 5500,
    payment_method: 'card',
    status: 'completed',
    created_by: 'Emily Davis',
  },
  {
    id: 10,
    invoice_number: 'INV-2023-0010',
    customer_name: 'Jessica Anderson',
    customer_phone: '9876543219',
    date: '2023-06-16',
    time: '15:20',
    items: 2,
    total: 1700,
    payment_method: 'upi',
    status: 'completed',
    created_by: 'Robert Johnson',
  },
];

// Mock data for sale items
const mockSaleItems = {
  1: [
    { id: 1, product: 'Jack Daniels Whiskey', quantity: 1, price: 1500, total: 1500 },
    { id: 2, product: 'Corona Beer (6-pack)', quantity: 1, price: 600, total: 600 },
    { id: 3, product: 'Absolut Vodka', quantity: 1, price: 400, total: 400 },
  ],
  2: [
    { id: 1, product: 'Johnnie Walker Black Label', quantity: 1, price: 1500, total: 1500 },
    { id: 2, product: 'Kingfisher Beer (6-pack)', quantity: 1, price: 300, total: 300 },
  ],
  3: [
    { id: 1, product: 'Bacardi Rum', quantity: 1, price: 800, total: 800 },
    { id: 2, product: 'Smirnoff Vodka', quantity: 2, price: 350, total: 700 },
    { id: 3, product: 'Bira White Beer (6-pack)', quantity: 2, price: 350, total: 700 },
    { id: 4, product: 'Old Monk Rum', quantity: 1, price: 500, total: 500 },
    { id: 5, product: 'Blenders Pride Whiskey', quantity: 1, price: 1500, total: 1500 },
  ],
};

// Mock data for customers
const mockCustomers = [
  { id: 1, name: 'John Doe', phone: '9876543210', email: 'john.doe@example.com' },
  { id: 2, name: 'Jane Smith', phone: '9876543211', email: 'jane.smith@example.com' },
  { id: 3, name: 'Michael Wilson', phone: '9876543212', email: 'michael.wilson@example.com' },
  { id: 4, name: 'Emily Davis', phone: '9876543213', email: 'emily.davis@example.com' },
  { id: 5, name: 'Robert Johnson', phone: '9876543214', email: 'robert.johnson@example.com' },
];

/**
 * Sales Management component for Shop Manager
 */
const SalesManagement: React.FC = () => {
  const { common, sales } = useTranslations();
  const theme = useTheme();
  const { confirm } = useGlobalConfirmDialog();
  const [searchQuery, setSearchQuery] = useState('');
  const [filterAnchorEl, setFilterAnchorEl] = useState<null | HTMLElement>(null);
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [paymentMethodFilter, setPaymentMethodFilter] = useState<string>('all');
  const [dateFilter, setDateFilter] = useState<string>('all');
  const [openSaleDetailsDialog, setOpenSaleDetailsDialog] = useState(false);
  const [selectedSale, setSelectedSale] = useState<any | null>(null);
  const [actionAnchorEl, setActionAnchorEl] = useState<{ [key: number]: HTMLElement | null }>({});
  const [tabValue, setTabValue] = useState(0);

  // Handle opening the filter menu
  const handleFilterClick = (event: React.MouseEvent<HTMLElement>) => {
    setFilterAnchorEl(event.currentTarget);
  };

  // Handle closing the filter menu
  const handleFilterClose = () => {
    setFilterAnchorEl(null);
  };

  // Handle opening the action menu for a sale
  const handleActionClick = (event: React.MouseEvent<HTMLElement>, saleId: number) => {
    setActionAnchorEl({ ...actionAnchorEl, [saleId]: event.currentTarget });
  };

  // Handle closing the action menu for a sale
  const handleActionClose = (saleId: number) => {
    setActionAnchorEl({ ...actionAnchorEl, [saleId]: null });
  };

  // Handle opening the sale details dialog
  const handleOpenSaleDetailsDialog = (sale: any) => {
    setSelectedSale(sale);
    setOpenSaleDetailsDialog(true);
    if (actionAnchorEl[sale.id]) {
      handleActionClose(sale.id);
    }
  };

  // Handle closing the sale details dialog
  const handleCloseSaleDetailsDialog = () => {
    setOpenSaleDetailsDialog(false);
  };

  // Handle printing an invoice
  const handlePrintInvoice = (sale: any) => {
    console.log('Printing invoice for sale:', sale);
    // In a real app, you would generate and print the invoice
    handleActionClose(sale.id);
  };

  // Handle cancelling a sale
  const handleCancelSale = async (sale: any) => {
    const confirmed = await confirm({
      title: sales('cancelSale'),
      message: `${sales('confirmCancelSale')} "${sale.invoice_number}"?`,
      confirmButtonColor: 'error',
      confirmText: common('cancel'),
      cancelText: common('no'),
    });

    if (confirmed) {
      console.log('Cancelling sale:', sale);
      // In a real app, you would make an API call to cancel the sale
    }

    handleActionClose(sale.id);
  };

  // Handle tab change
  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  // Get unique dates for filter
  const uniqueDates = Array.from(new Set(mockSales.map(sale => sale.date)));

  // Filter sales based on search query and filters
  const filteredSales = mockSales.filter((sale) => {
    const matchesSearch = sale.invoice_number.toLowerCase().includes(searchQuery.toLowerCase()) ||
      sale.customer_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      sale.customer_phone.includes(searchQuery);
    
    const matchesStatus = statusFilter === 'all' || sale.status === statusFilter;
    const matchesPaymentMethod = paymentMethodFilter === 'all' || sale.payment_method === paymentMethodFilter;
    const matchesDate = dateFilter === 'all' || sale.date === dateFilter;
    
    return matchesSearch && matchesStatus && matchesPaymentMethod && matchesDate;
  });

  // Define columns for the data table
  const columns = [
    {
      field: 'invoice_number',
      headerName: sales('invoiceNumber'),
      flex: 1,
      renderCell: (params: any) => (
        <Box>
          <Typography variant="body1" fontWeight={500}>
            {params.invoice_number}
          </Typography>
          <Typography variant="body2" color="textSecondary">
            {`${params.date} ${params.time}`}
          </Typography>
        </Box>
      ),
    },
    {
      field: 'customer_name',
      headerName: common('customer'),
      flex: 1,
      renderCell: (params: any) => (
        <Box>
          <Typography variant="body1">
            {params.customer_name}
          </Typography>
          <Typography variant="body2" color="textSecondary">
            {params.customer_phone}
          </Typography>
        </Box>
      ),
    },
    {
      field: 'items',
      headerName: common('items'),
      flex: 0.5,
      align: 'center',
    },
    {
      field: 'total',
      headerName: common('total'),
      flex: 0.7,
      renderCell: (params: any) => (
        <Typography variant="body2" fontWeight={500}>
          ₹{params.total.toLocaleString()}
        </Typography>
      ),
    },
    {
      field: 'payment_method',
      headerName: sales('paymentMethod'),
      flex: 0.7,
      renderCell: (params: any) => (
        <Chip
          label={
            params.payment_method === 'cash'
              ? common('cash')
              : params.payment_method === 'card'
              ? common('card')
              : params.payment_method === 'upi'
              ? common('upi')
              : params.payment_method
          }
          color={
            params.payment_method === 'cash'
              ? 'success'
              : params.payment_method === 'card'
              ? 'primary'
              : 'secondary'
          }
          size="small"
          variant="outlined"
        />
      ),
    },
    {
      field: 'status',
      headerName: common('status'),
      flex: 0.7,
      renderCell: (params: any) => (
        <Chip
          label={
            params.status === 'completed'
              ? sales('completed')
              : params.status === 'cancelled'
              ? sales('cancelled')
              : params.status
          }
          color={params.status === 'completed' ? 'success' : 'error'}
          size="small"
        />
      ),
    },
    {
      field: 'created_by',
      headerName: sales('createdBy'),
      flex: 0.7,
    },
    {
      field: 'actions',
      headerName: common('actions'),
      flex: 0.5,
      renderCell: (params: any) => (
        <>
          <IconButton
            size="small"
            onClick={(e) => handleActionClick(e, params.id)}
            aria-label="actions"
          >
            <MoreVertIcon fontSize="small" />
          </IconButton>
          <Menu
            anchorEl={actionAnchorEl[params.id]}
            open={Boolean(actionAnchorEl[params.id])}
            onClose={() => handleActionClose(params.id)}
          >
            <MenuItem onClick={() => handleOpenSaleDetailsDialog(params)}>
              <VisibilityIcon fontSize="small" sx={{ mr: 1 }} />
              {common('view')}
            </MenuItem>
            <MenuItem onClick={() => handlePrintInvoice(params)}>
              <PrintIcon fontSize="small" sx={{ mr: 1 }} />
              {sales('printInvoice')}
            </MenuItem>
            {params.status !== 'cancelled' && (
              <MenuItem onClick={() => handleCancelSale(params)} sx={{ color: 'error.main' }}>
                <CancelIcon fontSize="small" sx={{ mr: 1 }} />
                {common('cancel')}
              </MenuItem>
            )}
          </Menu>
        </>
      ),
    },
  ];

  return (
    <Container maxWidth="xl">
      <PageHeader
        title={sales('sales')}
        subtitle={sales('manageSales')}
        icon={<ShoppingCartIcon fontSize="large" />}
      />

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Tabs
            value={tabValue}
            onChange={handleTabChange}
            indicatorColor="primary"
            textColor="primary"
            variant="fullWidth"
            aria-label="sales tabs"
          >
            <Tab label={common('all')} />
            <Tab label={sales('completed')} />
            <Tab label={sales('cancelled')} />
          </Tabs>
          <Divider sx={{ my: 2 }} />
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} sm={6} md={4}>
              <TextField
                fullWidth
                placeholder={common('search')}
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <SearchIcon />
                    </InputAdornment>
                  ),
                }}
                size="small"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={4}>
              <Box sx={{ display: 'flex', gap: 1 }}>
                <Button
                  variant="outlined"
                  startIcon={<FilterListIcon />}
                  onClick={handleFilterClick}
                  size="small"
                >
                  {common('filter')}
                </Button>
                <Menu
                  anchorEl={filterAnchorEl}
                  open={Boolean(filterAnchorEl)}
                  onClose={handleFilterClose}
                >
                  <MenuItem sx={{ pointerEvents: 'none' }}>
                    <Typography variant="subtitle2">{common('status')}</Typography>
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setStatusFilter('all');
                      handleFilterClose();
                    }}
                    selected={statusFilter === 'all'}
                  >
                    {common('all')}
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setStatusFilter('completed');
                      handleFilterClose();
                    }}
                    selected={statusFilter === 'completed'}
                  >
                    {sales('completed')}
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setStatusFilter('cancelled');
                      handleFilterClose();
                    }}
                    selected={statusFilter === 'cancelled'}
                  >
                    {sales('cancelled')}
                  </MenuItem>
                  <Divider />
                  <MenuItem sx={{ pointerEvents: 'none' }}>
                    <Typography variant="subtitle2">{sales('paymentMethod')}</Typography>
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setPaymentMethodFilter('all');
                      handleFilterClose();
                    }}
                    selected={paymentMethodFilter === 'all'}
                  >
                    {common('all')}
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setPaymentMethodFilter('cash');
                      handleFilterClose();
                    }}
                    selected={paymentMethodFilter === 'cash'}
                  >
                    {common('cash')}
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setPaymentMethodFilter('card');
                      handleFilterClose();
                    }}
                    selected={paymentMethodFilter === 'card'}
                  >
                    {common('card')}
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setPaymentMethodFilter('upi');
                      handleFilterClose();
                    }}
                    selected={paymentMethodFilter === 'upi'}
                  >
                    {common('upi')}
                  </MenuItem>
                  <Divider />
                  <MenuItem sx={{ pointerEvents: 'none' }}>
                    <Typography variant="subtitle2">{common('date')}</Typography>
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      setDateFilter('all');
                      handleFilterClose();
                    }}
                    selected={dateFilter === 'all'}
                  >
                    {common('all')}
                  </MenuItem>
                  {uniqueDates.map((date) => (
                    <MenuItem
                      key={date}
                      onClick={() => {
                        setDateFilter(date);
                        handleFilterClose();
                      }}
                      selected={dateFilter === date}
                    >
                      {date}
                    </MenuItem>
                  ))}
                </Menu>
              </Box>
            </Grid>
            <Grid item xs={12} sm={12} md={4} sx={{ display: 'flex', justifyContent: 'flex-end', gap: 1 }}>
              <Button
                variant="outlined"
                color="primary"
                startIcon={<DownloadIcon />}
                onClick={() => console.log('Export sales')}
              >
                {common('export')}
              </Button>
              <Button
                variant="contained"
                color="primary"
                startIcon={<AddIcon />}
                onClick={() => console.log('New sale')}
              >
                {sales('newSale')}
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <DataTable
        columns={columns}
        data={filteredSales}
        keyField="id"
        pagination
        paginationPerPage={10}
        paginationTotalRows={filteredSales.length}
      />

      {/* Sale Details Dialog */}
      <Dialog open={openSaleDetailsDialog} onClose={handleCloseSaleDetailsDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          {sales('saleDetails')}
        </DialogTitle>
        <DialogContent>
          {selectedSale && (
            <Box>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <Card variant="outlined" sx={{ mb: 2 }}>
                    <CardContent>
                      <Grid container spacing={2}>
                        <Grid item xs={12} sm={6}>
                          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                            <ReceiptIcon sx={{ mr: 1, color: 'primary.main' }} />
                            <Typography variant="subtitle1" fontWeight={600}>
                              {selectedSale.invoice_number}
                            </Typography>
                          </Box>
                          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                            <CalendarTodayIcon sx={{ mr: 1, color: 'text.secondary', fontSize: '1rem' }} />
                            <Typography variant="body2" color="textSecondary">
                              {`${selectedSale.date} ${selectedSale.time}`}
                            </Typography>
                          </Box>
                          <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            <PersonIcon sx={{ mr: 1, color: 'text.secondary', fontSize: '1rem' }} />
                            <Typography variant="body2" color="textSecondary">
                              {`Created by: ${selectedSale.created_by}`}
                            </Typography>
                          </Box>
                        </Grid>
                        <Grid item xs={12} sm={6}>
                          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                            <PersonIcon sx={{ mr: 1, color: 'primary.main' }} />
                            <Typography variant="subtitle1" fontWeight={600}>
                              {selectedSale.customer_name}
                            </Typography>
                          </Box>
                          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                            <Typography variant="body2" color="textSecondary">
                              {`Phone: ${selectedSale.customer_phone}`}
                            </Typography>
                          </Box>
                          <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            <Chip
                              label={
                                selectedSale.status === 'completed'
                                  ? sales('completed')
                                  : selectedSale.status === 'cancelled'
                                  ? sales('cancelled')
                                  : selectedSale.status
                              }
                              color={selectedSale.status === 'completed' ? 'success' : 'error'}
                              size="small"
                            />
                          </Box>
                        </Grid>
                      </Grid>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="subtitle1" gutterBottom>
                    {sales('items')}
                  </Typography>
                  <TableContainer component={Paper} variant="outlined">
                    <Table>
                      <TableHead>
                        <TableRow>
                          <TableCell>{common('product')}</TableCell>
                          <TableCell align="center">{common('quantity')}</TableCell>
                          <TableCell align="right">{common('price')}</TableCell>
                          <TableCell align="right">{common('total')}</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {mockSaleItems[selectedSale.id]?.map((item) => (
                          <TableRow key={item.id}>
                            <TableCell>{item.product}</TableCell>
                            <TableCell align="center">{item.quantity}</TableCell>
                            <TableCell align="right">₹{item.price.toLocaleString()}</TableCell>
                            <TableCell align="right">₹{item.total.toLocaleString()}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </Grid>
                <Grid item xs={12}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 2 }}>
                    <Typography variant="subtitle1">
                      {sales('paymentMethod')}:
                    </Typography>
                    <Chip
                      label={
                        selectedSale.payment_method === 'cash'
                          ? common('cash')
                          : selectedSale.payment_method === 'card'
                          ? common('card')
                          : selectedSale.payment_method === 'upi'
                          ? common('upi')
                          : selectedSale.payment_method
                      }
                      color={
                        selectedSale.payment_method === 'cash'
                          ? 'success'
                          : selectedSale.payment_method === 'card'
                          ? 'primary'
                          : 'secondary'
                      }
                      size="small"
                      variant="outlined"
                    />
                  </Box>
                  <Divider sx={{ my: 2 }} />
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography variant="subtitle1" fontWeight={600}>
                      {common('total')}:
                    </Typography>
                    <Typography variant="subtitle1" fontWeight={600}>
                      ₹{selectedSale.total.toLocaleString()}
                    </Typography>
                  </Box>
                </Grid>
              </Grid>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseSaleDetailsDialog}>{common('close')}</Button>
          <Button
            variant="outlined"
            color="primary"
            startIcon={<PrintIcon />}
            onClick={() => handlePrintInvoice(selectedSale)}
          >
            {sales('printInvoice')}
          </Button>
          {selectedSale && selectedSale.status !== 'cancelled' && (
            <Button
              variant="outlined"
              color="error"
              startIcon={<CancelIcon />}
              onClick={() => {
                handleCloseSaleDetailsDialog();
                handleCancelSale(selectedSale);
              }}
            >
              {common('cancel')}
            </Button>
          )}
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default SalesManagement;