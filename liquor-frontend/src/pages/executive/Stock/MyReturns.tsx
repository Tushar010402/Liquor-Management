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
} from '@mui/material';
import {
  Search as SearchIcon,
  Visibility as ViewIcon,
  Delete as DeleteIcon,
  MoreVert as MoreVertIcon,
  AssignmentReturn as ReturnIcon,
  FilterList as FilterIcon,
  Print as PrintIcon,
  Share as ShareIcon,
  ContentCopy as CopyIcon,
  CheckCircle as CheckCircleIcon,
  Cancel as CancelIcon,
  Pending as PendingIcon,
  LocalShipping as SupplierIcon,
} from '@mui/icons-material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { PageHeader } from '../../../components/common';

// Mock return data
const mockReturns = [
  {
    id: 'RTN-001',
    date: '2023-11-25T10:30:00Z',
    status: 'approved',
    supplier: {
      id: 1,
      name: 'ABC Distributors',
      contact: 'Rajesh Kumar',
      phone: '9876543210',
      email: 'rajesh@abcdist.com',
    },
    items: [
      { 
        id: 1, 
        productName: 'Johnnie Walker Black Label', 
        price: 3500,
        quantity: 2, 
        total: 7000,
        reason: 'damaged',
        reasonText: 'Damaged Product',
        notes: 'Bottles broken during delivery' 
      },
      { 
        id: 2, 
        productName: 'Absolut Vodka', 
        price: 1800,
        quantity: 1, 
        total: 1800,
        reason: 'expired',
        reasonText: 'Expired Product',
        notes: 'Past expiry date' 
      },
    ],
    totalItems: 3,
    totalAmount: 8800,
    referenceNumber: 'INV-12345',
    approvedBy: 'Rajesh Kumar',
    approvedAt: '2023-11-25T14:45:00Z',
    notes: 'Approved with verification',
    documentUrl: 'https://example.com/document1.pdf',
  },
  {
    id: 'RTN-002',
    date: '2023-11-24T15:45:00Z',
    status: 'pending',
    supplier: {
      id: 2,
      name: 'XYZ Beverages',
      contact: 'Priya Sharma',
      phone: '8765432109',
      email: 'priya@xyzbev.com',
    },
    items: [
      { 
        id: 3, 
        productName: 'Jack Daniels', 
        price: 2800,
        quantity: 5, 
        total: 14000,
        reason: 'quality_issue',
        reasonText: 'Quality Issue',
        notes: 'Seal broken' 
      },
    ],
    totalItems: 5,
    totalAmount: 14000,
    referenceNumber: 'PO-67890',
    notes: 'Waiting for verification',
    documentUrl: null,
  },
  {
    id: 'RTN-003',
    date: '2023-11-23T18:20:00Z',
    status: 'rejected',
    supplier: {
      id: 3,
      name: 'Premium Spirits',
      contact: 'Amit Singh',
      phone: '7654321098',
      email: 'amit@premiumspirits.com',
    },
    items: [
      { 
        id: 4, 
        productName: 'Bacardi White Rum', 
        price: 1200,
        quantity: 3, 
        total: 3600,
        reason: 'wrong_delivery',
        reasonText: 'Wrong Product Delivered',
        notes: 'Ordered dark rum' 
      },
    ],
    totalItems: 3,
    totalAmount: 3600,
    referenceNumber: 'INV-54321',
    rejectedBy: 'Rajesh Kumar',
    rejectedAt: '2023-11-23T20:10:00Z',
    rejectionReason: 'Insufficient evidence provided',
    notes: 'Please provide delivery receipt',
    documentUrl: 'https://example.com/document2.pdf',
  },
  {
    id: 'RTN-004',
    date: '2023-11-22T14:10:00Z',
    status: 'approved',
    supplier: {
      id: 4,
      name: 'Global Wines & Spirits',
      contact: 'Neha Patel',
      phone: '6543210987',
      email: 'neha@globalws.com',
    },
    items: [
      { 
        id: 5, 
        productName: 'Beefeater Gin', 
        price: 2200,
        quantity: 10, 
        total: 22000,
        reason: 'excess_inventory',
        reasonText: 'Excess Inventory',
        notes: 'Ordered too many' 
      },
      { 
        id: 6, 
        productName: 'Chivas Regal 12 Year', 
        price: 3200,
        quantity: 1, 
        total: 3200,
        reason: 'damaged',
        reasonText: 'Damaged Product',
        notes: 'Seal broken' 
      },
    ],
    totalItems: 11,
    totalAmount: 25200,
    referenceNumber: 'PO-09876',
    approvedBy: 'Rajesh Kumar',
    approvedAt: '2023-11-22T16:30:00Z',
    notes: 'Approved after physical verification',
    documentUrl: 'https://example.com/document3.pdf',
  },
  {
    id: 'RTN-005',
    date: '2023-11-21T11:05:00Z',
    status: 'approved',
    supplier: {
      id: 5,
      name: 'Metro Liquors',
      contact: 'Vikram Mehta',
      phone: '5432109876',
      email: 'vikram@metroliquors.com',
    },
    items: [
      { 
        id: 7, 
        productName: 'Grey Goose Vodka', 
        price: 4500,
        quantity: 2, 
        total: 9000,
        reason: 'recall',
        reasonText: 'Product Recall',
        notes: 'Manufacturer recall' 
      },
    ],
    totalItems: 2,
    totalAmount: 9000,
    referenceNumber: 'INV-13579',
    approvedBy: 'Rajesh Kumar',
    approvedAt: '2023-11-21T13:20:00Z',
    notes: 'Approved with supplier acknowledgment',
    documentUrl: 'https://example.com/document4.pdf',
  },
];

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
      id={`return-tabpanel-${index}`}
      aria-labelledby={`return-tab-${index}`}
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

const MyReturns: React.FC = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedReturn, setSelectedReturn] = useState<any | null>(null);
  const [detailsDialogOpen, setDetailsDialogOpen] = useState<boolean>(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState<boolean>(false);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [menuReturnId, setMenuReturnId] = useState<string | null>(null);
  const [startDate, setStartDate] = useState<Date | null>(null);
  const [endDate, setEndDate] = useState<Date | null>(null);
  const [tabValue, setTabValue] = useState(0);
  const [returns, setReturns] = useState(mockReturns);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>, returnId: string) => {
    setAnchorEl(event.currentTarget);
    setMenuReturnId(returnId);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
    setMenuReturnId(null);
  };

  const handleViewDetails = (returnData: any) => {
    setSelectedReturn(returnData);
    setDetailsDialogOpen(true);
    handleMenuClose();
  };

  const handleDeleteReturn = (returnId: string) => {
    setMenuReturnId(returnId);
    setDeleteDialogOpen(true);
    handleMenuClose();
  };

  const confirmDeleteReturn = () => {
    if (menuReturnId) {
      // In a real app, this would call an API to delete the return
      setReturns(returns.filter(returnData => returnData.id !== menuReturnId));
      setDeleteDialogOpen(false);
      setMenuReturnId(null);
    }
  };

  const handleDuplicateReturn = (returnId: string) => {
    // In a real app, this would navigate to the return page with the data pre-filled
    console.log(`Duplicating return ${returnId}`);
    navigate(`/executive/create-return?duplicate=${returnId}`);
    handleMenuClose();
  };

  const filteredReturns = returns.filter(returnData => {
    const matchesSearch = 
      returnData.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      returnData.supplier.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      returnData.items.some(item => 
        item.productName.toLowerCase().includes(searchQuery.toLowerCase())
      );
    
    const returnDate = new Date(returnData.date);
    const matchesDateRange = 
      (!startDate || returnDate >= startDate) &&
      (!endDate || returnDate <= endDate);
    
    const matchesStatus = 
      (tabValue === 0) || // All
      (tabValue === 1 && returnData.status === 'pending') || // Pending
      (tabValue === 2 && returnData.status === 'approved') || // Approved
      (tabValue === 3 && returnData.status === 'rejected'); // Rejected
    
    return matchesSearch && matchesDateRange && matchesStatus;
  });

  const clearFilters = () => {
    setSearchQuery('');
    setStartDate(null);
    setEndDate(null);
  };

  const getStatusChip = (status: string) => {
    switch (status) {
      case 'approved':
        return (
          <Chip
            icon={<CheckCircleIcon />}
            label="Approved"
            color="success"
            size="small"
          />
        );
      case 'rejected':
        return (
          <Chip
            icon={<CancelIcon />}
            label="Rejected"
            color="error"
            size="small"
          />
        );
      case 'pending':
        return (
          <Chip
            icon={<PendingIcon />}
            label="Pending"
            color="warning"
            size="small"
          />
        );
      default:
        return null;
    }
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Box>
        <PageHeader
          title="My Returns"
          subtitle="View and manage your supplier returns"
        />

        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={12} md={4}>
                <TextField
                  fullWidth
                  placeholder="Search by ID, supplier or product"
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
              <Grid item xs={12} md={2}>
                <Button
                  variant="outlined"
                  color="primary"
                  onClick={clearFilters}
                  startIcon={<FilterIcon />}
                  fullWidth
                >
                  Clear Filters
                </Button>
              </Grid>
            </Grid>
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
                aria-label="return tabs"
                sx={{ px: 2 }}
              >
                <Tab label="All" />
                <Tab label="Pending" />
                <Tab label="Approved" />
                <Tab label="Rejected" />
              </Tabs>
            </Box>
            
            <TabPanel value={tabValue} index={0}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h6">
                    All Returns ({filteredReturns.length})
                  </Typography>
                  <Button
                    variant="contained"
                    color="primary"
                    startIcon={<ReturnIcon />}
                    onClick={() => navigate('/executive/create-return')}
                  >
                    Create New Return
                  </Button>
                </Box>

                {renderReturnsTable(filteredReturns)}
              </CardContent>
            </TabPanel>
            
            <TabPanel value={tabValue} index={1}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h6">
                    Pending Returns ({filteredReturns.length})
                  </Typography>
                  <Button
                    variant="contained"
                    color="primary"
                    startIcon={<ReturnIcon />}
                    onClick={() => navigate('/executive/create-return')}
                  >
                    Create New Return
                  </Button>
                </Box>

                {renderReturnsTable(filteredReturns)}
              </CardContent>
            </TabPanel>
            
            <TabPanel value={tabValue} index={2}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h6">
                    Approved Returns ({filteredReturns.length})
                  </Typography>
                  <Button
                    variant="contained"
                    color="primary"
                    startIcon={<ReturnIcon />}
                    onClick={() => navigate('/executive/create-return')}
                  >
                    Create New Return
                  </Button>
                </Box>

                {renderReturnsTable(filteredReturns)}
              </CardContent>
            </TabPanel>
            
            <TabPanel value={tabValue} index={3}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h6">
                    Rejected Returns ({filteredReturns.length})
                  </Typography>
                  <Button
                    variant="contained"
                    color="primary"
                    startIcon={<ReturnIcon />}
                    onClick={() => navigate('/executive/create-return')}
                  >
                    Create New Return
                  </Button>
                </Box>

                {renderReturnsTable(filteredReturns)}
              </CardContent>
            </TabPanel>
          </Card>
        </motion.div>

        {/* Action Menu */}
        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={handleMenuClose}
        >
          <MenuItem onClick={() => menuReturnId && handleDuplicateReturn(menuReturnId)}>
            <ListItemIcon>
              <CopyIcon fontSize="small" />
            </ListItemIcon>
            <ListItemText>Duplicate Return</ListItemText>
          </MenuItem>
          {returns.find(r => r.id === menuReturnId)?.status === 'pending' && (
            <MenuItem onClick={() => menuReturnId && handleDeleteReturn(menuReturnId)}>
              <ListItemIcon>
                <DeleteIcon fontSize="small" color="error" />
              </ListItemIcon>
              <ListItemText sx={{ color: 'error.main' }}>Delete Return</ListItemText>
            </MenuItem>
          )}
        </Menu>

        {/* Details Dialog */}
        <Dialog
          open={detailsDialogOpen}
          onClose={() => setDetailsDialogOpen(false)}
          maxWidth="md"
          fullWidth
        >
          {selectedReturn && (
            <>
              <DialogTitle>
                Return Details - {selectedReturn.id}
                <Box sx={{ display: 'inline-block', ml: 2 }}>
                  {getStatusChip(selectedReturn.status)}
                </Box>
              </DialogTitle>
              <DialogContent>
                <Grid container spacing={2}>
                  <Grid item xs={12} md={6}>
                    <Typography variant="subtitle2" color="textSecondary">
                      Supplier Information
                    </Typography>
                    <Typography variant="body1">
                      {selectedReturn.supplier.name}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Contact: {selectedReturn.supplier.contact}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Phone: {selectedReturn.supplier.phone}
                    </Typography>
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <Typography variant="subtitle2" color="textSecondary">
                      Return Details
                    </Typography>
                    <Typography variant="body2">
                      <strong>Date:</strong> {new Date(selectedReturn.date).toLocaleDateString()}
                    </Typography>
                    {selectedReturn.referenceNumber && (
                      <Typography variant="body2">
                        <strong>Reference:</strong> {selectedReturn.referenceNumber}
                      </Typography>
                    )}
                    <Typography variant="body2">
                      <strong>Total Value:</strong> ₹{selectedReturn.totalAmount}
                    </Typography>
                    {selectedReturn.status === 'approved' && (
                      <Typography variant="body2" color="success.main">
                        <strong>Approved By:</strong> {selectedReturn.approvedBy} on {new Date(selectedReturn.approvedAt).toLocaleDateString()}
                      </Typography>
                    )}
                    {selectedReturn.status === 'rejected' && (
                      <Typography variant="body2" color="error.main">
                        <strong>Rejected By:</strong> {selectedReturn.rejectedBy} on {new Date(selectedReturn.rejectedAt).toLocaleDateString()}
                      </Typography>
                    )}
                  </Grid>
                  <Grid item xs={12}>
                    <Divider sx={{ my: 2 }} />
                    <Typography variant="subtitle2" color="textSecondary">
                      Return Items
                    </Typography>
                    <TableContainer component={Paper} variant="outlined" sx={{ mt: 1 }}>
                      <Table size="small">
                        <TableHead>
                          <TableRow>
                            <TableCell>Product</TableCell>
                            <TableCell align="right">Price</TableCell>
                            <TableCell align="center">Quantity</TableCell>
                            <TableCell align="right">Total</TableCell>
                            <TableCell>Reason</TableCell>
                            <TableCell>Notes</TableCell>
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {selectedReturn.items.map((item: any) => (
                            <TableRow key={item.id}>
                              <TableCell>{item.productName}</TableCell>
                              <TableCell align="right">₹{item.price}</TableCell>
                              <TableCell align="center">{item.quantity}</TableCell>
                              <TableCell align="right">₹{item.total}</TableCell>
                              <TableCell>{item.reasonText}</TableCell>
                              <TableCell>{item.notes || '-'}</TableCell>
                            </TableRow>
                          ))}
                          <TableRow>
                            <TableCell colSpan={3} align="right" sx={{ fontWeight: 'bold' }}>
                              Total Return Value:
                            </TableCell>
                            <TableCell align="right" sx={{ fontWeight: 'bold' }}>
                              ₹{selectedReturn.totalAmount}
                            </TableCell>
                            <TableCell colSpan={2}></TableCell>
                          </TableRow>
                        </TableBody>
                      </Table>
                    </TableContainer>
                  </Grid>
                  {selectedReturn.notes && (
                    <Grid item xs={12}>
                      <Typography variant="subtitle2" color="textSecondary" sx={{ mt: 2 }}>
                        Notes
                      </Typography>
                      <Paper variant="outlined" sx={{ p: 2, mt: 1, backgroundColor: 'background.default' }}>
                        <Typography variant="body2">
                          {selectedReturn.notes}
                        </Typography>
                      </Paper>
                    </Grid>
                  )}
                  {selectedReturn.status === 'rejected' && selectedReturn.rejectionReason && (
                    <Grid item xs={12}>
                      <Typography variant="subtitle2" color="error" sx={{ mt: 2 }}>
                        Rejection Reason
                      </Typography>
                      <Paper variant="outlined" sx={{ p: 2, mt: 1, backgroundColor: 'error.lightest', borderColor: 'error.light' }}>
                        <Typography variant="body2" color="error.main">
                          {selectedReturn.rejectionReason}
                        </Typography>
                      </Paper>
                    </Grid>
                  )}
                  {selectedReturn.documentUrl && (
                    <Grid item xs={12}>
                      <Typography variant="subtitle2" color="textSecondary" sx={{ mt: 2 }}>
                        Supporting Document
                      </Typography>
                      <Button
                        variant="outlined"
                        startIcon={<ViewIcon />}
                        sx={{ mt: 1 }}
                        onClick={() => {
                          // In a real app, this would open the document
                          window.open(selectedReturn.documentUrl, '_blank');
                        }}
                      >
                        View Document
                      </Button>
                    </Grid>
                  )}
                </Grid>
              </DialogContent>
              <DialogActions>
                <Button
                  startIcon={<PrintIcon />}
                  onClick={() => {
                    console.log(`Printing return ${selectedReturn.id}`);
                    // In a real app, this would trigger printing
                  }}
                >
                  Print
                </Button>
                <Button
                  startIcon={<ShareIcon />}
                  onClick={() => {
                    console.log(`Sharing return ${selectedReturn.id}`);
                    // In a real app, this would open sharing options
                  }}
                >
                  Share
                </Button>
                <Button onClick={() => setDetailsDialogOpen(false)}>
                  Close
                </Button>
                {selectedReturn.status === 'rejected' && (
                  <Button
                    variant="contained"
                    color="primary"
                    startIcon={<CopyIcon />}
                    onClick={() => {
                      handleDuplicateReturn(selectedReturn.id);
                      setDetailsDialogOpen(false);
                    }}
                  >
                    Duplicate & Edit
                  </Button>
                )}
              </DialogActions>
            </>
          )}
        </Dialog>

        {/* Delete Confirmation Dialog */}
        <Dialog
          open={deleteDialogOpen}
          onClose={() => setDeleteDialogOpen(false)}
        >
          <DialogTitle>
            Delete Return
          </DialogTitle>
          <DialogContent>
            <Typography variant="body1">
              Are you sure you want to delete this return? This action cannot be undone.
            </Typography>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setDeleteDialogOpen(false)}>
              Cancel
            </Button>
            <Button
              variant="contained"
              color="error"
              onClick={confirmDeleteReturn}
            >
              Delete
            </Button>
          </DialogActions>
        </Dialog>
      </Box>
    </LocalizationProvider>
  );

  function renderReturnsTable(returns: any[]) {
    return returns.length > 0 ? (
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Return ID</TableCell>
              <TableCell>Date</TableCell>
              <TableCell>Supplier</TableCell>
              <TableCell align="center">Items</TableCell>
              <TableCell align="right">Amount</TableCell>
              <TableCell align="center">Status</TableCell>
              <TableCell align="center">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {returns.map((returnData) => (
              <TableRow key={returnData.id} hover>
                <TableCell>{returnData.id}</TableCell>
                <TableCell>
                  {new Date(returnData.date).toLocaleDateString()}
                  <Typography variant="caption" display="block" color="textSecondary">
                    {new Date(returnData.date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Typography variant="body2">{returnData.supplier.name}</Typography>
                  <Typography variant="caption" color="textSecondary">
                    {returnData.referenceNumber || 'No reference'}
                  </Typography>
                </TableCell>
                <TableCell align="center">{returnData.totalItems}</TableCell>
                <TableCell align="right">₹{returnData.totalAmount.toLocaleString()}</TableCell>
                <TableCell align="center">
                  {getStatusChip(returnData.status)}
                </TableCell>
                <TableCell align="center">
                  <Box sx={{ display: 'flex', justifyContent: 'center' }}>
                    <Tooltip title="View Details">
                      <IconButton
                        size="small"
                        color="primary"
                        onClick={() => handleViewDetails(returnData)}
                      >
                        <ViewIcon fontSize="small" />
                      </IconButton>
                    </Tooltip>
                    <IconButton
                      size="small"
                      onClick={(e) => handleMenuOpen(e, returnData.id)}
                    >
                      <MoreVertIcon fontSize="small" />
                    </IconButton>
                  </Box>
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
        <ReturnIcon sx={{ fontSize: 40, color: 'text.secondary', mb: 1 }} />
        <Typography variant="h6" color="textSecondary">
          No returns found
        </Typography>
        <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
          {searchQuery || startDate || endDate
            ? 'Try changing your search criteria'
            : 'Create a new return to supplier'}
        </Typography>
        {(searchQuery || startDate || endDate) && (
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

export default MyReturns;