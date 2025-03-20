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
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Tabs,
  Tab,
  Divider,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  useTheme,
} from '@mui/material';
import {
  Search as SearchIcon,
  FilterList as FilterListIcon,
  Visibility as VisibilityIcon,
  CheckCircle as CheckCircleIcon,
  Cancel as CancelIcon,
  ShoppingCart as ShoppingCartIcon,
  Inventory as InventoryIcon,
  LocalShipping as LocalShippingIcon,
  Approval as ApprovalIcon,
  AttachMoney as AttachMoneyIcon,
  Person as PersonIcon,
  CalendarToday as CalendarTodayIcon,
} from '@mui/icons-material';
import { DataTable, PageHeader } from '../../components/common';
import { useTranslations, useFormValidation, useGlobalConfirmDialog } from '../../hooks';
import * as Yup from 'yup';

// Mock data for pending approvals
const mockPendingApprovals = [
  {
    id: 1,
    type: 'sale',
    title: 'Sale #INV-2023-0045',
    amount: 3500,
    items: 5,
    submitted_by: 'John Doe',
    submitted_at: '2023-06-15 14:30',
    status: 'pending',
    details: {
      customer_name: 'Michael Brown',
      customer_phone: '9876543210',
      payment_method: 'cash',
      products: [
        { name: 'Jack Daniels Whiskey', quantity: 1, price: 2500, total: 2500 },
        { name: 'Corona Beer (6-pack)', quantity: 1, price: 600, total: 600 },
        { name: 'Smirnoff Vodka', quantity: 1, price: 400, total: 400 },
      ],
    },
  },
  {
    id: 2,
    type: 'adjustment',
    title: 'Stock Adjustment #ADJ-2023-0032',
    items: 5,
    submitted_by: 'Jane Smith',
    submitted_at: '2023-06-15 15:45',
    status: 'pending',
    details: {
      reason: 'damaged',
      notes: 'Bottles damaged during delivery',
      products: [
        { name: 'Jack Daniels Whiskey', quantity: -2, current_stock: 15 },
        { name: 'Absolut Vodka', quantity: -1, current_stock: 8 },
        { name: 'Corona Beer (6-pack)', quantity: -2, current_stock: 24 },
      ],
    },
  },
  {
    id: 3,
    type: 'return',
    title: 'Return #RET-2023-0012',
    amount: 1200,
    items: 1,
    submitted_by: 'Michael Wilson',
    submitted_at: '2023-06-15 16:20',
    status: 'pending',
    details: {
      customer_name: 'David Miller',
      customer_phone: '9876543211',
      reason: 'defective',
      notes: 'Seal was broken',
      products: [
        { name: 'Johnnie Walker Black Label', quantity: 1, price: 1200, total: 1200 },
      ],
    },
  },
  {
    id: 4,
    type: 'sale',
    title: 'Sale #INV-2023-0046',
    amount: 4800,
    items: 3,
    submitted_by: 'Emily Davis',
    submitted_at: '2023-06-15 17:10',
    status: 'pending',
    details: {
      customer_name: 'Sarah Johnson',
      customer_phone: '9876543212',
      payment_method: 'card',
      products: [
        { name: 'Johnnie Walker Black Label', quantity: 1, price: 3500, total: 3500 },
        { name: 'Bira White Beer (6-pack)', quantity: 1, price: 700, total: 700 },
        { name: 'Old Monk Rum', quantity: 1, price: 600, total: 600 },
      ],
    },
  },
  {
    id: 5,
    type: 'adjustment',
    title: 'Stock Adjustment #ADJ-2023-0033',
    items: 2,
    submitted_by: 'Robert Johnson',
    submitted_at: '2023-06-15 18:05',
    status: 'pending',
    details: {
      reason: 'correction',
      notes: 'Correcting inventory count after audit',
      products: [
        { name: 'Blenders Pride Whiskey', quantity: 2, current_stock: 10 },
        { name: 'Kingfisher Beer (6-pack)', quantity: -3, current_stock: 36 },
      ],
    },
  },
];

// Validation schema for approval/rejection
const approvalSchema = Yup.object({
  notes: Yup.string().required('Notes are required'),
});

/**
 * Pending Approvals component for Assistant Manager
 */
const PendingApprovals: React.FC = () => {
  const { common, approvals } = useTranslations();
  const theme = useTheme();
  const { confirm } = useGlobalConfirmDialog();
  const [searchQuery, setSearchQuery] = useState('');
  const [typeFilter, setTypeFilter] = useState<string>('all');
  const [openDetailsDialog, setOpenDetailsDialog] = useState(false);
  const [selectedApproval, setSelectedApproval] = useState<any | null>(null);
  const [openApproveDialog, setOpenApproveDialog] = useState(false);
  const [openRejectDialog, setOpenRejectDialog] = useState(false);
  const [tabValue, setTabValue] = useState(0);

  // Form validation for approval/rejection
  const approvalForm = useFormValidation({
    initialValues: {
      notes: '',
    },
    validationSchema: approvalSchema,
    onSubmit: (values) => {
      if (openApproveDialog) {
        handleApprove(selectedApproval, values.notes);
      } else if (openRejectDialog) {
        handleReject(selectedApproval, values.notes);
      }
    },
  });

  // Handle tab change
  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
    
    // Set type filter based on tab
    switch (newValue) {
      case 0:
        setTypeFilter('all');
        break;
      case 1:
        setTypeFilter('sale');
        break;
      case 2:
        setTypeFilter('adjustment');
        break;
      case 3:
        setTypeFilter('return');
        break;
      default:
        setTypeFilter('all');
    }
  };

  // Handle opening the details dialog
  const handleOpenDetailsDialog = (approval: any) => {
    setSelectedApproval(approval);
    setOpenDetailsDialog(true);
  };

  // Handle closing the details dialog
  const handleCloseDetailsDialog = () => {
    setOpenDetailsDialog(false);
  };

  // Handle opening the approve dialog
  const handleOpenApproveDialog = (approval: any) => {
    setSelectedApproval(approval);
    setOpenApproveDialog(true);
    approvalForm.formik.resetForm();
  };

  // Handle closing the approve dialog
  const handleCloseApproveDialog = () => {
    setOpenApproveDialog(false);
  };

  // Handle opening the reject dialog
  const handleOpenRejectDialog = (approval: any) => {
    setSelectedApproval(approval);
    setOpenRejectDialog(true);
    approvalForm.formik.resetForm();
  };

  // Handle closing the reject dialog
  const handleCloseRejectDialog = () => {
    setOpenRejectDialog(false);
  };

  // Handle approving an approval
  const handleApprove = (approval: any, notes: string) => {
    console.log('Approving:', approval, 'Notes:', notes);
    // In a real app, you would make an API call to approve the approval
    handleCloseApproveDialog();
  };

  // Handle rejecting an approval
  const handleReject = (approval: any, notes: string) => {
    console.log('Rejecting:', approval, 'Notes:', notes);
    // In a real app, you would make an API call to reject the approval
    handleCloseRejectDialog();
  };

  // Filter approvals based on search query and type filter
  const filteredApprovals = mockPendingApprovals.filter((approval) => {
    const matchesSearch = approval.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      approval.submitted_by.toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesType = typeFilter === 'all' || approval.type === typeFilter;
    
    return matchesSearch && matchesType;
  });

  // Define columns for the data table
  const columns = [
    {
      field: 'title',
      headerName: approvals('title'),
      flex: 1.5,
      renderCell: (params: any) => (
        <Box>
          <Typography variant="body1" fontWeight={500}>
            {params.title}
          </Typography>
          <Typography variant="body2" color="textSecondary">
            {params.submitted_at}
          </Typography>
        </Box>
      ),
    },
    {
      field: 'type',
      headerName: common('type'),
      flex: 0.8,
      renderCell: (params: any) => (
        <Chip
          label={
            params.type === 'sale'
              ? approvals('sale')
              : params.type === 'adjustment'
              ? approvals('adjustment')
              : approvals('return')
          }
          color={
            params.type === 'sale'
              ? 'success'
              : params.type === 'adjustment'
              ? 'warning'
              : 'error'
          }
          size="small"
        />
      ),
    },
    {
      field: 'submitted_by',
      headerName: approvals('submittedBy'),
      flex: 1,
    },
    {
      field: 'details',
      headerName: approvals('details'),
      flex: 1,
      renderCell: (params: any) => (
        <Box>
          {params.type === 'sale' && (
            <>
              <Typography variant="body2">
                {params.details.customer_name}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                {params.items} {common('items')} • ₹{params.amount.toLocaleString()}
              </Typography>
            </>
          )}
          {params.type === 'adjustment' && (
            <>
              <Typography variant="body2">
                {params.details.reason}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                {params.items} {common('items')}
              </Typography>
            </>
          )}
          {params.type === 'return' && (
            <>
              <Typography variant="body2">
                {params.details.customer_name}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                {params.items} {common('items')} • ₹{params.amount.toLocaleString()}
              </Typography>
            </>
          )}
        </Box>
      ),
    },
    {
      field: 'actions',
      headerName: common('actions'),
      flex: 1,
      renderCell: (params: any) => (
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            variant="outlined"
            size="small"
            startIcon={<VisibilityIcon />}
            onClick={() => handleOpenDetailsDialog(params)}
          >
            {common('view')}
          </Button>
          <Button
            variant="contained"
            color="success"
            size="small"
            startIcon={<CheckCircleIcon />}
            onClick={() => handleOpenApproveDialog(params)}
          >
            {common('approve')}
          </Button>
          <Button
            variant="contained"
            color="error"
            size="small"
            startIcon={<CancelIcon />}
            onClick={() => handleOpenRejectDialog(params)}
          >
            {common('reject')}
          </Button>
        </Box>
      ),
    },
  ];

  return (
    <Container maxWidth="xl">
      <PageHeader
        title={approvals('pendingApprovals')}
        subtitle={approvals('manageApprovals')}
        icon={<ApprovalIcon fontSize="large" />}
      />

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Tabs
            value={tabValue}
            onChange={handleTabChange}
            indicatorColor="primary"
            textColor="primary"
            variant="fullWidth"
            aria-label="approval tabs"
          >
            <Tab label={common('all')} />
            <Tab label={approvals('sales')} />
            <Tab label={approvals('adjustments')} />
            <Tab label={approvals('returns')} />
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
            <Grid item xs={12} sm={6} md={8} sx={{ display: 'flex', justifyContent: 'flex-end' }}>
              <Typography variant="body2" color="textSecondary" sx={{ mr: 1, alignSelf: 'center' }}>
                {approvals('totalPending')}: {filteredApprovals.length}
              </Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <DataTable
        columns={columns}
        data={filteredApprovals}
        keyField="id"
        pagination
        paginationPerPage={10}
        paginationTotalRows={filteredApprovals.length}
      />

      {/* Details Dialog */}
      <Dialog open={openDetailsDialog} onClose={handleCloseDetailsDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          {selectedApproval?.title}
        </DialogTitle>
        <DialogContent>
          {selectedApproval && (
            <Box>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <Card variant="outlined" sx={{ mb: 2 }}>
                    <CardContent>
                      <Grid container spacing={2}>
                        <Grid item xs={12} sm={6}>
                          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                            {selectedApproval.type === 'sale' ? (
                              <ShoppingCartIcon sx={{ mr: 1, color: 'success.main' }} />
                            ) : selectedApproval.type === 'adjustment' ? (
                              <InventoryIcon sx={{ mr: 1, color: 'warning.main' }} />
                            ) : (
                              <LocalShippingIcon sx={{ mr: 1, color: 'error.main' }} />
                            )}
                            <Typography variant="subtitle1" fontWeight={600}>
                              {selectedApproval.title}
                            </Typography>
                          </Box>
                          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                            <CalendarTodayIcon sx={{ mr: 1, color: 'text.secondary', fontSize: '1rem' }} />
                            <Typography variant="body2" color="textSecondary">
                              {selectedApproval.submitted_at}
                            </Typography>
                          </Box>
                          <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            <PersonIcon sx={{ mr: 1, color: 'text.secondary', fontSize: '1rem' }} />
                            <Typography variant="body2" color="textSecondary">
                              {approvals('submittedBy')}: {selectedApproval.submitted_by}
                            </Typography>
                          </Box>
                        </Grid>
                        <Grid item xs={12} sm={6}>
                          {selectedApproval.type === 'sale' && (
                            <>
                              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                                <PersonIcon sx={{ mr: 1, color: 'primary.main' }} />
                                <Typography variant="subtitle1" fontWeight={600}>
                                  {selectedApproval.details.customer_name}
                                </Typography>
                              </Box>
                              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                                <Typography variant="body2" color="textSecondary">
                                  {common('phone')}: {selectedApproval.details.customer_phone}
                                </Typography>
                              </Box>
                              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                <AttachMoneyIcon sx={{ mr: 1, color: 'text.secondary', fontSize: '1rem' }} />
                                <Typography variant="body2" color="textSecondary">
                                  {approvals('paymentMethod')}: {selectedApproval.details.payment_method}
                                </Typography>
                              </Box>
                            </>
                          )}
                          {selectedApproval.type === 'adjustment' && (
                            <>
                              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                                <Typography variant="subtitle1" fontWeight={600}>
                                  {approvals('reason')}: {selectedApproval.details.reason}
                                </Typography>
                              </Box>
                              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                <Typography variant="body2" color="textSecondary">
                                  {common('notes')}: {selectedApproval.details.notes}
                                </Typography>
                              </Box>
                            </>
                          )}
                          {selectedApproval.type === 'return' && (
                            <>
                              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                                <PersonIcon sx={{ mr: 1, color: 'primary.main' }} />
                                <Typography variant="subtitle1" fontWeight={600}>
                                  {selectedApproval.details.customer_name}
                                </Typography>
                              </Box>
                              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                                <Typography variant="body2" color="textSecondary">
                                  {common('phone')}: {selectedApproval.details.customer_phone}
                                </Typography>
                              </Box>
                              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                <Typography variant="body2" color="textSecondary">
                                  {approvals('reason')}: {selectedApproval.details.reason}
                                </Typography>
                              </Box>
                            </>
                          )}
                        </Grid>
                      </Grid>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="subtitle1" gutterBottom>
                    {common('items')}
                  </Typography>
                  <TableContainer component={Paper} variant="outlined">
                    <Table>
                      <TableHead>
                        <TableRow>
                          <TableCell>{common('product')}</TableCell>
                          <TableCell align="center">{common('quantity')}</TableCell>
                          {(selectedApproval.type === 'sale' || selectedApproval.type === 'return') && (
                            <>
                              <TableCell align="right">{common('price')}</TableCell>
                              <TableCell align="right">{common('total')}</TableCell>
                            </>
                          )}
                          {selectedApproval.type === 'adjustment' && (
                            <TableCell align="right">{common('currentStock')}</TableCell>
                          )}
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {selectedApproval.details.products.map((product: any, index: number) => (
                          <TableRow key={index}>
                            <TableCell>{product.name}</TableCell>
                            <TableCell align="center">
                              {selectedApproval.type === 'adjustment' ? (
                                <Typography
                                  color={product.quantity < 0 ? 'error.main' : 'success.main'}
                                >
                                  {product.quantity > 0 ? `+${product.quantity}` : product.quantity}
                                </Typography>
                              ) : (
                                product.quantity
                              )}
                            </TableCell>
                            {(selectedApproval.type === 'sale' || selectedApproval.type === 'return') && (
                              <>
                                <TableCell align="right">₹{product.price.toLocaleString()}</TableCell>
                                <TableCell align="right">₹{product.total.toLocaleString()}</TableCell>
                              </>
                            )}
                            {selectedApproval.type === 'adjustment' && (
                              <TableCell align="right">{product.current_stock}</TableCell>
                            )}
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </Grid>
                {(selectedApproval.type === 'sale' || selectedApproval.type === 'return') && (
                  <Grid item xs={12}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 2 }}>
                      <Typography variant="subtitle1" fontWeight={600}>
                        {common('total')}:
                      </Typography>
                      <Typography variant="subtitle1" fontWeight={600}>
                        ₹{selectedApproval.amount.toLocaleString()}
                      </Typography>
                    </Box>
                  </Grid>
                )}
                {selectedApproval.details.notes && (
                  <Grid item xs={12}>
                    <Box sx={{ mt: 2 }}>
                      <Typography variant="subtitle1" gutterBottom>
                        {common('notes')}
                      </Typography>
                      <Paper variant="outlined" sx={{ p: 2 }}>
                        <Typography variant="body2">
                          {selectedApproval.details.notes}
                        </Typography>
                      </Paper>
                    </Box>
                  </Grid>
                )}
              </Grid>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDetailsDialog}>{common('close')}</Button>
          <Button
            variant="contained"
            color="success"
            startIcon={<CheckCircleIcon />}
            onClick={() => {
              handleCloseDetailsDialog();
              handleOpenApproveDialog(selectedApproval);
            }}
          >
            {common('approve')}
          </Button>
          <Button
            variant="contained"
            color="error"
            startIcon={<CancelIcon />}
            onClick={() => {
              handleCloseDetailsDialog();
              handleOpenRejectDialog(selectedApproval);
            }}
          >
            {common('reject')}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Approve Dialog */}
      <Dialog open={openApproveDialog} onClose={handleCloseApproveDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {approvals('approveTitle')}
        </DialogTitle>
        <form onSubmit={approvalForm.formik.handleSubmit}>
          <DialogContent>
            <Typography variant="body1" gutterBottom>
              {approvals('approveConfirmation')} <strong>{selectedApproval?.title}</strong>?
            </Typography>
            <TextField
              fullWidth
              id="notes"
              name="notes"
              label={common('notes')}
              multiline
              rows={4}
              value={approvalForm.formik.values.notes}
              onChange={approvalForm.formik.handleChange}
              error={approvalForm.formik.touched.notes && Boolean(approvalForm.formik.errors.notes)}
              helperText={approvalForm.formik.touched.notes && approvalForm.formik.errors.notes}
              margin="normal"
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseApproveDialog}>{common('cancel')}</Button>
            <Button type="submit" variant="contained" color="success">
              {common('approve')}
            </Button>
          </DialogActions>
        </form>
      </Dialog>

      {/* Reject Dialog */}
      <Dialog open={openRejectDialog} onClose={handleCloseRejectDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {approvals('rejectTitle')}
        </DialogTitle>
        <form onSubmit={approvalForm.formik.handleSubmit}>
          <DialogContent>
            <Typography variant="body1" gutterBottom>
              {approvals('rejectConfirmation')} <strong>{selectedApproval?.title}</strong>?
            </Typography>
            <TextField
              fullWidth
              id="notes"
              name="notes"
              label={common('notes')}
              multiline
              rows={4}
              value={approvalForm.formik.values.notes}
              onChange={approvalForm.formik.handleChange}
              error={approvalForm.formik.touched.notes && Boolean(approvalForm.formik.errors.notes)}
              helperText={approvalForm.formik.touched.notes && approvalForm.formik.errors.notes}
              margin="normal"
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseRejectDialog}>{common('cancel')}</Button>
            <Button type="submit" variant="contained" color="error">
              {common('reject')}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Container>
  );
};

export default PendingApprovals;