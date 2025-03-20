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
} from '@mui/material';
import {
  Search as SearchIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  MoreVert as MoreVertIcon,
  ShoppingCart as CartIcon,
  Save as SaveIcon,
  Visibility as ViewIcon,
  Print as PrintIcon,
  Share as ShareIcon,
  FilterList as FilterIcon,
} from '@mui/icons-material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { PageHeader } from '../../../components/common';

// Mock draft sales data
const mockDraftSales = [
  {
    id: 'DFT-001',
    customerName: 'Raj Kumar',
    customerPhone: '9876543210',
    items: [
      { id: 1, name: 'Johnnie Walker Black Label', quantity: 2, price: 3500, total: 7000 },
      { id: 2, name: 'Absolut Vodka', quantity: 1, price: 1800, total: 1800 },
    ],
    totalItems: 3,
    totalAmount: 8800,
    createdAt: '2023-11-25T10:30:00Z',
    createdBy: 'Vikram Mehta',
    notes: 'Customer will pick up tomorrow',
  },
  {
    id: 'DFT-002',
    customerName: 'Priya Sharma',
    customerPhone: '8765432109',
    items: [
      { id: 3, name: 'Jack Daniels', quantity: 1, price: 2800, total: 2800 },
      { id: 4, name: 'Bacardi White Rum', quantity: 2, price: 1200, total: 2400 },
      { id: 5, name: 'Beefeater Gin', quantity: 1, price: 2200, total: 2200 },
    ],
    totalItems: 4,
    totalAmount: 7400,
    createdAt: '2023-11-24T15:45:00Z',
    createdBy: 'Vikram Mehta',
    notes: 'Regular customer, special pricing applied',
  },
  {
    id: 'DFT-003',
    customerName: 'Amit Singh',
    customerPhone: '7654321098',
    items: [
      { id: 6, name: 'Chivas Regal 12 Year', quantity: 1, price: 3200, total: 3200 },
    ],
    totalItems: 1,
    totalAmount: 3200,
    createdAt: '2023-11-23T18:20:00Z',
    createdBy: 'Vikram Mehta',
    notes: '',
  },
  {
    id: 'DFT-004',
    customerName: 'Neha Patel',
    customerPhone: '6543210987',
    items: [
      { id: 7, name: 'Grey Goose Vodka', quantity: 1, price: 4500, total: 4500 },
      { id: 8, name: 'Bombay Sapphire Gin', quantity: 1, price: 2500, total: 2500 },
    ],
    totalItems: 2,
    totalAmount: 7000,
    createdAt: '2023-11-22T14:10:00Z',
    createdBy: 'Vikram Mehta',
    notes: 'For birthday party',
  },
  {
    id: 'DFT-005',
    customerName: 'Vikram Mehta',
    customerPhone: '5432109876',
    items: [
      { id: 9, name: 'Captain Morgan Spiced Rum', quantity: 2, price: 1400, total: 2800 },
      { id: 10, name: 'Jameson Irish Whiskey', quantity: 1, price: 2200, total: 2200 },
    ],
    totalItems: 3,
    totalAmount: 5000,
    createdAt: '2023-11-21T11:05:00Z',
    createdBy: 'Vikram Mehta',
    notes: 'Will confirm final order by evening',
  },
];

const DraftSales: React.FC = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedDraft, setSelectedDraft] = useState<any | null>(null);
  const [detailsDialogOpen, setDetailsDialogOpen] = useState<boolean>(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState<boolean>(false);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [menuDraftId, setMenuDraftId] = useState<string | null>(null);
  const [startDate, setStartDate] = useState<Date | null>(null);
  const [endDate, setEndDate] = useState<Date | null>(null);
  const [draftSales, setDraftSales] = useState(mockDraftSales);

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>, draftId: string) => {
    setAnchorEl(event.currentTarget);
    setMenuDraftId(draftId);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
    setMenuDraftId(null);
  };

  const handleViewDetails = (draft: any) => {
    setSelectedDraft(draft);
    setDetailsDialogOpen(true);
    handleMenuClose();
  };

  const handleEditDraft = (draftId: string) => {
    // In a real app, this would navigate to the edit page with the draft ID
    console.log(`Editing draft ${draftId}`);
    navigate(`/executive/edit-sale/${draftId}`);
    handleMenuClose();
  };

  const handleDeleteDraft = (draftId: string) => {
    setMenuDraftId(draftId);
    setDeleteDialogOpen(true);
    handleMenuClose();
  };

  const confirmDeleteDraft = () => {
    if (menuDraftId) {
      // In a real app, this would call an API to delete the draft
      setDraftSales(draftSales.filter(draft => draft.id !== menuDraftId));
      setDeleteDialogOpen(false);
      setMenuDraftId(null);
    }
  };

  const handleConvertToSale = (draftId: string) => {
    // In a real app, this would navigate to the sale page with the draft data pre-filled
    console.log(`Converting draft ${draftId} to sale`);
    navigate(`/executive/new-sale?draft=${draftId}`);
    handleMenuClose();
  };

  const filteredDrafts = draftSales.filter(draft => {
    const matchesSearch = 
      draft.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      draft.customerName.toLowerCase().includes(searchQuery.toLowerCase()) ||
      draft.customerPhone.includes(searchQuery);
    
    const draftDate = new Date(draft.createdAt);
    const matchesDateRange = 
      (!startDate || draftDate >= startDate) &&
      (!endDate || draftDate <= endDate);
    
    return matchesSearch && matchesDateRange;
  });

  const clearFilters = () => {
    setSearchQuery('');
    setStartDate(null);
    setEndDate(null);
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Box>
        <PageHeader
          title="Draft Sales"
          subtitle="Manage your saved draft sales"
        />

        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={12} md={4}>
                <TextField
                  fullWidth
                  placeholder="Search by ID, customer name or phone"
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
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">
                  Draft Sales ({filteredDrafts.length})
                </Typography>
                <Button
                  variant="contained"
                  color="primary"
                  startIcon={<CartIcon />}
                  onClick={() => navigate('/executive/new-sale')}
                >
                  Create New Sale
                </Button>
              </Box>

              {filteredDrafts.length > 0 ? (
                <TableContainer>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Draft ID</TableCell>
                        <TableCell>Customer</TableCell>
                        <TableCell align="center">Items</TableCell>
                        <TableCell align="right">Amount</TableCell>
                        <TableCell>Created On</TableCell>
                        <TableCell>Notes</TableCell>
                        <TableCell align="center">Actions</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {filteredDrafts.map((draft) => (
                        <TableRow key={draft.id} hover>
                          <TableCell>{draft.id}</TableCell>
                          <TableCell>
                            <Typography variant="body2">{draft.customerName}</Typography>
                            <Typography variant="caption" color="textSecondary">
                              {draft.customerPhone}
                            </Typography>
                          </TableCell>
                          <TableCell align="center">{draft.totalItems}</TableCell>
                          <TableCell align="right">₹{draft.totalAmount.toLocaleString()}</TableCell>
                          <TableCell>
                            {new Date(draft.createdAt).toLocaleDateString()}
                            <Typography variant="caption" display="block" color="textSecondary">
                              {new Date(draft.createdAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                            </Typography>
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
                              {draft.notes || '-'}
                            </Typography>
                          </TableCell>
                          <TableCell align="center">
                            <Box sx={{ display: 'flex', justifyContent: 'center' }}>
                              <Tooltip title="View Details">
                                <IconButton
                                  size="small"
                                  color="primary"
                                  onClick={() => handleViewDetails(draft)}
                                >
                                  <ViewIcon fontSize="small" />
                                </IconButton>
                              </Tooltip>
                              <Tooltip title="Edit Draft">
                                <IconButton
                                  size="small"
                                  color="info"
                                  onClick={() => handleEditDraft(draft.id)}
                                >
                                  <EditIcon fontSize="small" />
                                </IconButton>
                              </Tooltip>
                              <IconButton
                                size="small"
                                onClick={(e) => handleMenuOpen(e, draft.id)}
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
                  <SaveIcon sx={{ fontSize: 40, color: 'text.secondary', mb: 1 }} />
                  <Typography variant="h6" color="textSecondary">
                    No draft sales found
                  </Typography>
                  <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
                    {searchQuery || startDate || endDate
                      ? 'Try changing your search criteria'
                      : 'Create a new sale and save it as draft'}
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
              )}
            </CardContent>
          </Card>
        </motion.div>

        {/* Action Menu */}
        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={handleMenuClose}
        >
          <MenuItem onClick={() => menuDraftId && handleConvertToSale(menuDraftId)}>
            <ListItemIcon>
              <CartIcon fontSize="small" />
            </ListItemIcon>
            <ListItemText>Convert to Sale</ListItemText>
          </MenuItem>
          <MenuItem onClick={() => menuDraftId && handleEditDraft(menuDraftId)}>
            <ListItemIcon>
              <EditIcon fontSize="small" />
            </ListItemIcon>
            <ListItemText>Edit Draft</ListItemText>
          </MenuItem>
          <MenuItem onClick={() => menuDraftId && handleDeleteDraft(menuDraftId)}>
            <ListItemIcon>
              <DeleteIcon fontSize="small" color="error" />
            </ListItemIcon>
            <ListItemText sx={{ color: 'error.main' }}>Delete Draft</ListItemText>
          </MenuItem>
        </Menu>

        {/* Details Dialog */}
        <Dialog
          open={detailsDialogOpen}
          onClose={() => setDetailsDialogOpen(false)}
          maxWidth="md"
          fullWidth
        >
          {selectedDraft && (
            <>
              <DialogTitle>
                Draft Sale Details - {selectedDraft.id}
              </DialogTitle>
              <DialogContent>
                <Grid container spacing={2}>
                  <Grid item xs={12} md={6}>
                    <Typography variant="subtitle2" color="textSecondary">
                      Customer Information
                    </Typography>
                    <Typography variant="body1">
                      {selectedDraft.customerName}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      {selectedDraft.customerPhone}
                    </Typography>
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <Typography variant="subtitle2" color="textSecondary">
                      Draft Created
                    </Typography>
                    <Typography variant="body1">
                      {new Date(selectedDraft.createdAt).toLocaleDateString()}
                      {' '}
                      {new Date(selectedDraft.createdAt).toLocaleTimeString()}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      By: {selectedDraft.createdBy}
                    </Typography>
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
                            <TableCell align="center">Quantity</TableCell>
                            <TableCell align="right">Price</TableCell>
                            <TableCell align="right">Total</TableCell>
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {selectedDraft.items.map((item: any) => (
                            <TableRow key={item.id}>
                              <TableCell>{item.name}</TableCell>
                              <TableCell align="center">{item.quantity}</TableCell>
                              <TableCell align="right">₹{item.price.toLocaleString()}</TableCell>
                              <TableCell align="right">₹{item.total.toLocaleString()}</TableCell>
                            </TableRow>
                          ))}
                          <TableRow>
                            <TableCell colSpan={3} align="right" sx={{ fontWeight: 'bold' }}>
                              Total Amount:
                            </TableCell>
                            <TableCell align="right" sx={{ fontWeight: 'bold' }}>
                              ₹{selectedDraft.totalAmount.toLocaleString()}
                            </TableCell>
                          </TableRow>
                        </TableBody>
                      </Table>
                    </TableContainer>
                  </Grid>
                  {selectedDraft.notes && (
                    <Grid item xs={12}>
                      <Typography variant="subtitle2" color="textSecondary" sx={{ mt: 2 }}>
                        Notes
                      </Typography>
                      <Paper variant="outlined" sx={{ p: 2, mt: 1, backgroundColor: 'background.default' }}>
                        <Typography variant="body2">
                          {selectedDraft.notes}
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
                    console.log(`Printing draft ${selectedDraft.id}`);
                    // In a real app, this would trigger printing
                  }}
                >
                  Print
                </Button>
                <Button
                  startIcon={<ShareIcon />}
                  onClick={() => {
                    console.log(`Sharing draft ${selectedDraft.id}`);
                    // In a real app, this would open sharing options
                  }}
                >
                  Share
                </Button>
                <Button onClick={() => setDetailsDialogOpen(false)}>
                  Close
                </Button>
                <Button
                  variant="contained"
                  color="primary"
                  startIcon={<CartIcon />}
                  onClick={() => {
                    handleConvertToSale(selectedDraft.id);
                    setDetailsDialogOpen(false);
                  }}
                >
                  Convert to Sale
                </Button>
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
            Delete Draft Sale
          </DialogTitle>
          <DialogContent>
            <Typography variant="body1">
              Are you sure you want to delete this draft sale? This action cannot be undone.
            </Typography>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setDeleteDialogOpen(false)}>
              Cancel
            </Button>
            <Button
              variant="contained"
              color="error"
              onClick={confirmDeleteDraft}
            >
              Delete
            </Button>
          </DialogActions>
        </Dialog>
      </Box>
    </LocalizationProvider>
  );
};

export default DraftSales;