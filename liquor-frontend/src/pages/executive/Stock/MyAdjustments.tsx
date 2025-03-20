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
  Inventory as InventoryIcon,
  FilterList as FilterIcon,
  ArrowUpward as ArrowUpwardIcon,
  ArrowDownward as ArrowDownwardIcon,
  Print as PrintIcon,
  Share as ShareIcon,
  ContentCopy as CopyIcon,
  CheckCircle as CheckCircleIcon,
  Cancel as CancelIcon,
  Pending as PendingIcon,
} from '@mui/icons-material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { PageHeader } from '../../../components/common';

// Mock adjustment data
const mockAdjustments = [
  {
    id: 'ADJ-001',
    date: '2023-11-25T10:30:00Z',
    status: 'approved',
    items: [
      { 
        id: 1, 
        productName: 'Johnnie Walker Black Label', 
        adjustmentType: 'decrease', 
        quantity: 2, 
        reason: 'damaged',
        reasonText: 'Damaged Product',
        notes: 'Bottles broken during delivery' 
      },
      { 
        id: 2, 
        productName: 'Absolut Vodka', 
        adjustmentType: 'decrease', 
        quantity: 1, 
        reason: 'expired',
        reasonText: 'Expired Product',
        notes: 'Past expiry date' 
      },
    ],
    totalItems: 3,
    approvedBy: 'Rajesh Kumar',
    approvedAt: '2023-11-25T14:45:00Z',
    notes: 'Approved with verification',
  },
  {
    id: 'ADJ-002',
    date: '2023-11-24T15:45:00Z',
    status: 'pending',
    items: [
      { 
        id: 3, 
        productName: 'Jack Daniels', 
        adjustmentType: 'increase', 
        quantity: 5, 
        reason: 'received_from_supplier',
        reasonText: 'Received from Supplier',
        notes: 'Additional stock received' 
      },
    ],
    totalItems: 5,
    notes: 'Waiting for verification',
  },
  {
    id: 'ADJ-003',
    date: '2023-11-23T18:20:00Z',
    status: 'rejected',
    items: [
      { 
        id: 4, 
        productName: 'Bacardi White Rum', 
        adjustmentType: 'decrease', 
        quantity: 3, 
        reason: 'theft',
        reasonText: 'Theft/Loss',
        notes: 'Missing from inventory' 
      },
    ],
    totalItems: 3,
    rejectedBy: 'Rajesh Kumar',
    rejectedAt: '2023-11-23T20:10:00Z',
    rejectionReason: 'Insufficient evidence provided',
    notes: 'Please provide CCTV footage',
  },
  {
    id: 'ADJ-004',
    date: '2023-11-22T14:10:00Z',
    status: 'approved',
    items: [
      { 
        id: 5, 
        productName: 'Beefeater Gin', 
        adjustmentType: 'increase', 
        quantity: 10, 
        reason: 'inventory_count',
        reasonText: 'Inventory Count Adjustment',
        notes: 'Found during inventory count' 
      },
      { 
        id: 6, 
        productName: 'Chivas Regal 12 Year', 
        adjustmentType: 'decrease', 
        quantity: 1, 
        reason: 'damaged',
        reasonText: 'Damaged Product',
        notes: 'Seal broken' 
      },
    ],
    totalItems: 11,
    approvedBy: 'Rajesh Kumar',
    approvedAt: '2023-11-22T16:30:00Z',
    notes: 'Approved after physical verification',
  },
  {
    id: 'ADJ-005',
    date: '2023-11-21T11:05:00Z',
    status: 'approved',
    items: [
      { 
        id: 7, 
        productName: 'Grey Goose Vodka', 
        adjustmentType: 'decrease', 
        quantity: 2, 
        reason: 'return_to_supplier',
        reasonText: 'Return to Supplier',
        notes: 'Batch quality issue' 
      },
    ],
    totalItems: 2,
    approvedBy: 'Rajesh Kumar',
    approvedAt: '2023-11-21T13:20:00Z',
    notes: 'Approved with supplier acknowledgment',
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
      id={`adjustment-tabpanel-${index}`}
      aria-labelledby={`adjustment-tab-${index}`}
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

const MyAdjustments: React.FC = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedAdjustment, setSelectedAdjustment] = useState<any | null>(null);
  const [detailsDialogOpen, setDetailsDialogOpen] = useState<boolean>(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState<boolean>(false);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [menuAdjustmentId, setMenuAdjustmentId] = useState<string | null>(null);
  const [startDate, setStartDate] = useState<Date | null>(null);
  const [endDate, setEndDate] = useState<Date | null>(null);
  const [tabValue, setTabValue] = useState(0);
  const [adjustments, setAdjustments] = useState(mockAdjustments);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>, adjustmentId: string) => {
    setAnchorEl(event.currentTarget);
    setMenuAdjustmentId(adjustmentId);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
    setMenuAdjustmentId(null);
  };

  const handleViewDetails = (adjustment: any) => {
    setSelectedAdjustment(adjustment);
    setDetailsDialogOpen(true);
    handleMenuClose();
  };

  const handleDeleteAdjustment = (adjustmentId: string) => {
    setMenuAdjustmentId(adjustmentId);
    setDeleteDialogOpen(true);
    handleMenuClose();
  };

  const confirmDeleteAdjustment = () => {
    if (menuAdjustmentId) {
      // In a real app, this would call an API to delete the adjustment
      setAdjustments(adjustments.filter(adjustment => adjustment.id !== menuAdjustmentId));
      setDeleteDialogOpen(false);
      setMenuAdjustmentId(null);
    }
  };

  const handleDuplicateAdjustment = (adjustmentId: string) => {
    // In a real app, this would navigate to the adjustment page with the data pre-filled
    console.log(`Duplicating adjustment ${adjustmentId}`);
    navigate(`/executive/batch-adjustment?duplicate=${adjustmentId}`);
    handleMenuClose();
  };

  const filteredAdjustments = adjustments.filter(adjustment => {
    const matchesSearch = 
      adjustment.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      adjustment.items.some(item => 
        item.productName.toLowerCase().includes(searchQuery.toLowerCase())
      );
    
    const adjustmentDate = new Date(adjustment.date);
    const matchesDateRange = 
      (!startDate || adjustmentDate >= startDate) &&
      (!endDate || adjustmentDate <= endDate);
    
    const matchesStatus = 
      (tabValue === 0) || // All
      (tabValue === 1 && adjustment.status === 'pending') || // Pending
      (tabValue === 2 && adjustment.status === 'approved') || // Approved
      (tabValue === 3 && adjustment.status === 'rejected'); // Rejected
    
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
          title="My Stock Adjustments"
          subtitle="View and manage your stock adjustment history"
        />

        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={12} md={4}>
                <TextField
                  fullWidth
                  placeholder="Search by ID or product name"
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
                aria-label="adjustment tabs"
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
                    All Adjustments ({filteredAdjustments.length})
                  </Typography>
                  <Button
                    variant="contained"
                    color="primary"
                    startIcon={<InventoryIcon />}
                    onClick={() => navigate('/executive/batch-adjustment')}
                  >
                    New Batch Adjustment
                  </Button>
                </Box>

                {renderAdjustmentsTable(filteredAdjustments)}
              </CardContent>
            </TabPanel>
            
            <TabPanel value={tabValue} index={1}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h6">
                    Pending Adjustments ({filteredAdjustments.length})
                  </Typography>
                  <Button
                    variant="contained"
                    color="primary"
                    startIcon={<InventoryIcon />}
                    onClick={() => navigate('/executive/batch-adjustment')}
                  >
                    New Batch Adjustment
                  </Button>
                </Box>

                {renderAdjustmentsTable(filteredAdjustments)}
              </CardContent>
            </TabPanel>
            
            <TabPanel value={tabValue} index={2}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h6">
                    Approved Adjustments ({filteredAdjustments.length})
                  </Typography>
                  <Button
                    variant="contained"
                    color="primary"
                    startIcon={<InventoryIcon />}
                    onClick={() => navigate('/executive/batch-adjustment')}
                  >
                    New Batch Adjustment
                  </Button>
                </Box>

                {renderAdjustmentsTable(filteredAdjustments)}
              </CardContent>
            </TabPanel>
            
            <TabPanel value={tabValue} index={3}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h6">
                    Rejected Adjustments ({filteredAdjustments.length})
                  </Typography>
                  <Button
                    variant="contained"
                    color="primary"
                    startIcon={<InventoryIcon />}
                    onClick={() => navigate('/executive/batch-adjustment')}
                  >
                    New Batch Adjustment
                  </Button>
                </Box>

                {renderAdjustmentsTable(filteredAdjustments)}
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
          <MenuItem onClick={() => menuAdjustmentId && handleDuplicateAdjustment(menuAdjustmentId)}>
            <ListItemIcon>
              <CopyIcon fontSize="small" />
            </ListItemIcon>
            <ListItemText>Duplicate Adjustment</ListItemText>
          </MenuItem>
          {adjustments.find(a => a.id === menuAdjustmentId)?.status === 'pending' && (
            <MenuItem onClick={() => menuAdjustmentId && handleDeleteAdjustment(menuAdjustmentId)}>
              <ListItemIcon>
                <DeleteIcon fontSize="small" color="error" />
              </ListItemIcon>
              <ListItemText sx={{ color: 'error.main' }}>Delete Adjustment</ListItemText>
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
          {selectedAdjustment && (
            <>
              <DialogTitle>
                Adjustment Details - {selectedAdjustment.id}
                <Box sx={{ display: 'inline-block', ml: 2 }}>
                  {getStatusChip(selectedAdjustment.status)}
                </Box>
              </DialogTitle>
              <DialogContent>
                <Grid container spacing={2}>
                  <Grid item xs={12} md={6}>
                    <Typography variant="subtitle2" color="textSecondary">
                      Adjustment Date
                    </Typography>
                    <Typography variant="body1">
                      {new Date(selectedAdjustment.date).toLocaleDateString()}
                      {' '}
                      {new Date(selectedAdjustment.date).toLocaleTimeString()}
                    </Typography>
                  </Grid>
                  <Grid item xs={12} md={6}>
                    {selectedAdjustment.status === 'approved' && (
                      <>
                        <Typography variant="subtitle2" color="textSecondary">
                          Approved By
                        </Typography>
                        <Typography variant="body1">
                          {selectedAdjustment.approvedBy}
                          {' on '}
                          {new Date(selectedAdjustment.approvedAt).toLocaleDateString()}
                        </Typography>
                      </>
                    )}
                    {selectedAdjustment.status === 'rejected' && (
                      <>
                        <Typography variant="subtitle2" color="textSecondary">
                          Rejected By
                        </Typography>
                        <Typography variant="body1">
                          {selectedAdjustment.rejectedBy}
                          {' on '}
                          {new Date(selectedAdjustment.rejectedAt).toLocaleDateString()}
                        </Typography>
                      </>
                    )}
                  </Grid>
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
                            <TableCell align="center">Type</TableCell>
                            <TableCell align="center">Quantity</TableCell>
                            <TableCell>Reason</TableCell>
                            <TableCell>Notes</TableCell>
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {selectedAdjustment.items.map((item: any) => (
                            <TableRow key={item.id}>
                              <TableCell>{item.productName}</TableCell>
                              <TableCell align="center">
                                {item.adjustmentType === 'increase' ? (
                                  <Chip
                                    icon={<ArrowUpwardIcon />}
                                    label="Increase"
                                    color="success"
                                    size="small"
                                  />
                                ) : (
                                  <Chip
                                    icon={<ArrowDownwardIcon />}
                                    label="Decrease"
                                    color="error"
                                    size="small"
                                  />
                                )}
                              </TableCell>
                              <TableCell align="center">{item.quantity}</TableCell>
                              <TableCell>{item.reasonText}</TableCell>
                              <TableCell>{item.notes || '-'}</TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </TableContainer>
                  </Grid>
                  {selectedAdjustment.notes && (
                    <Grid item xs={12}>
                      <Typography variant="subtitle2" color="textSecondary" sx={{ mt: 2 }}>
                        Notes
                      </Typography>
                      <Paper variant="outlined" sx={{ p: 2, mt: 1, backgroundColor: 'background.default' }}>
                        <Typography variant="body2">
                          {selectedAdjustment.notes}
                        </Typography>
                      </Paper>
                    </Grid>
                  )}
                  {selectedAdjustment.status === 'rejected' && selectedAdjustment.rejectionReason && (
                    <Grid item xs={12}>
                      <Typography variant="subtitle2" color="error" sx={{ mt: 2 }}>
                        Rejection Reason
                      </Typography>
                      <Paper variant="outlined" sx={{ p: 2, mt: 1, backgroundColor: 'error.lightest', borderColor: 'error.light' }}>
                        <Typography variant="body2" color="error.main">
                          {selectedAdjustment.rejectionReason}
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
                    console.log(`Printing adjustment ${selectedAdjustment.id}`);
                    // In a real app, this would trigger printing
                  }}
                >
                  Print
                </Button>
                <Button
                  startIcon={<ShareIcon />}
                  onClick={() => {
                    console.log(`Sharing adjustment ${selectedAdjustment.id}`);
                    // In a real app, this would open sharing options
                  }}
                >
                  Share
                </Button>
                <Button onClick={() => setDetailsDialogOpen(false)}>
                  Close
                </Button>
                {selectedAdjustment.status === 'rejected' && (
                  <Button
                    variant="contained"
                    color="primary"
                    startIcon={<CopyIcon />}
                    onClick={() => {
                      handleDuplicateAdjustment(selectedAdjustment.id);
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
            Delete Adjustment
          </DialogTitle>
          <DialogContent>
            <Typography variant="body1">
              Are you sure you want to delete this adjustment? This action cannot be undone.
            </Typography>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setDeleteDialogOpen(false)}>
              Cancel
            </Button>
            <Button
              variant="contained"
              color="error"
              onClick={confirmDeleteAdjustment}
            >
              Delete
            </Button>
          </DialogActions>
        </Dialog>
      </Box>
    </LocalizationProvider>
  );

  function renderAdjustmentsTable(adjustments: any[]) {
    return adjustments.length > 0 ? (
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Adjustment ID</TableCell>
              <TableCell>Date</TableCell>
              <TableCell align="center">Items</TableCell>
              <TableCell align="center">Status</TableCell>
              <TableCell>Notes</TableCell>
              <TableCell align="center">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {adjustments.map((adjustment) => (
              <TableRow key={adjustment.id} hover>
                <TableCell>{adjustment.id}</TableCell>
                <TableCell>
                  {new Date(adjustment.date).toLocaleDateString()}
                  <Typography variant="caption" display="block" color="textSecondary">
                    {new Date(adjustment.date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </Typography>
                </TableCell>
                <TableCell align="center">{adjustment.totalItems}</TableCell>
                <TableCell align="center">
                  {getStatusChip(adjustment.status)}
                </TableCell>
                <TableCell>
                  <Typography
                    variant="body2"
                    sx={{
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      whiteSpace: 'nowrap',
                      maxWidth: 150,
                    }}
                  >
                    {adjustment.notes || '-'}
                  </Typography>
                </TableCell>
                <TableCell align="center">
                  <Box sx={{ display: 'flex', justifyContent: 'center' }}>
                    <Tooltip title="View Details">
                      <IconButton
                        size="small"
                        color="primary"
                        onClick={() => handleViewDetails(adjustment)}
                      >
                        <ViewIcon fontSize="small" />
                      </IconButton>
                    </Tooltip>
                    <IconButton
                      size="small"
                      onClick={(e) => handleMenuOpen(e, adjustment.id)}
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
        <InventoryIcon sx={{ fontSize: 40, color: 'text.secondary', mb: 1 }} />
        <Typography variant="h6" color="textSecondary">
          No adjustments found
        </Typography>
        <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
          {searchQuery || startDate || endDate
            ? 'Try changing your search criteria'
            : 'Create a new stock adjustment'}
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

export default MyAdjustments;