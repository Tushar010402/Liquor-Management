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
  Chip,
  Avatar,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  Search as SearchIcon,
  FilterList as FilterIcon,
  FileDownload as DownloadIcon,
  Print as PrintIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  TrendingFlat as TrendingFlatIcon,
  Visibility as VisibilityIcon,
  LocalBar as BottleIcon,
} from '@mui/icons-material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { motion } from 'framer-motion';
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
  PieChart,
  Pie,
  Cell,
} from 'recharts';

// Mock brand sales data
const mockBrandSales = [
  {
    id: 1,
    brand: 'Johnnie Walker',
    category: 'Whisky',
    logoUrl: 'https://example.com/logos/johnnie-walker.png',
    sales: 125000,
    units: 35,
    avgPrice: 3571,
    trend: 'up',
    trendPercentage: 12,
    products: [
      { name: 'Johnnie Walker Black Label', sales: 75000, units: 20 },
      { name: 'Johnnie Walker Red Label', sales: 35000, units: 10 },
      { name: 'Johnnie Walker Blue Label', sales: 15000, units: 5 },
    ],
  },
  {
    id: 2,
    brand: 'Absolut',
    category: 'Vodka',
    logoUrl: 'https://example.com/logos/absolut.png',
    sales: 98000,
    units: 50,
    avgPrice: 1960,
    trend: 'up',
    trendPercentage: 8,
    products: [
      { name: 'Absolut Original', sales: 60000, units: 30 },
      { name: 'Absolut Citron', sales: 20000, units: 10 },
      { name: 'Absolut Elyx', sales: 18000, units: 10 },
    ],
  },
  {
    id: 3,
    brand: 'Jack Daniels',
    category: 'Whisky',
    logoUrl: 'https://example.com/logos/jack-daniels.png',
    sales: 85000,
    units: 30,
    avgPrice: 2833,
    trend: 'down',
    trendPercentage: 5,
    products: [
      { name: 'Jack Daniels Old No. 7', sales: 65000, units: 25 },
      { name: 'Jack Daniels Honey', sales: 20000, units: 5 },
    ],
  },
  {
    id: 4,
    brand: 'Bacardi',
    category: 'Rum',
    logoUrl: 'https://example.com/logos/bacardi.png',
    sales: 72000,
    units: 60,
    avgPrice: 1200,
    trend: 'flat',
    trendPercentage: 0,
    products: [
      { name: 'Bacardi Superior', sales: 40000, units: 35 },
      { name: 'Bacardi Gold', sales: 32000, units: 25 },
    ],
  },
  {
    id: 5,
    brand: 'Beefeater',
    category: 'Gin',
    logoUrl: 'https://example.com/logos/beefeater.png',
    sales: 65000,
    units: 30,
    avgPrice: 2167,
    trend: 'up',
    trendPercentage: 15,
    products: [
      { name: 'Beefeater London Dry Gin', sales: 45000, units: 20 },
      { name: 'Beefeater Pink', sales: 20000, units: 10 },
    ],
  },
  {
    id: 6,
    brand: 'Chivas Regal',
    category: 'Whisky',
    logoUrl: 'https://example.com/logos/chivas.png',
    sales: 60000,
    units: 20,
    avgPrice: 3000,
    trend: 'down',
    trendPercentage: 3,
    products: [
      { name: 'Chivas Regal 12 Year', sales: 40000, units: 15 },
      { name: 'Chivas Regal 18 Year', sales: 20000, units: 5 },
    ],
  },
  {
    id: 7,
    brand: 'Grey Goose',
    category: 'Vodka',
    logoUrl: 'https://example.com/logos/grey-goose.png',
    sales: 55000,
    units: 12,
    avgPrice: 4583,
    trend: 'up',
    trendPercentage: 10,
    products: [
      { name: 'Grey Goose Original', sales: 40000, units: 9 },
      { name: 'Grey Goose La Poire', sales: 15000, units: 3 },
    ],
  },
  {
    id: 8,
    brand: 'Bombay Sapphire',
    category: 'Gin',
    logoUrl: 'https://example.com/logos/bombay.png',
    sales: 50000,
    units: 20,
    avgPrice: 2500,
    trend: 'up',
    trendPercentage: 18,
    products: [
      { name: 'Bombay Sapphire', sales: 50000, units: 20 },
    ],
  },
  {
    id: 9,
    brand: 'Captain Morgan',
    category: 'Rum',
    logoUrl: 'https://example.com/logos/captain-morgan.png',
    sales: 45000,
    units: 30,
    avgPrice: 1500,
    trend: 'down',
    trendPercentage: 2,
    products: [
      { name: 'Captain Morgan Spiced Rum', sales: 30000, units: 20 },
      { name: 'Captain Morgan White Rum', sales: 15000, units: 10 },
    ],
  },
  {
    id: 10,
    brand: 'Jameson',
    category: 'Whisky',
    logoUrl: 'https://example.com/logos/jameson.png',
    sales: 40000,
    units: 18,
    avgPrice: 2222,
    trend: 'up',
    trendPercentage: 7,
    products: [
      { name: 'Jameson Irish Whiskey', sales: 40000, units: 18 },
    ],
  },
];

// Colors for charts
const COLORS = ['#4CAF50', '#9C27B0', '#2196F3', '#FF9800', '#F44336', '#3F51B5', '#009688', '#E91E63', '#CDDC39', '#795548'];

// Categories
const categories = ['Whisky', 'Vodka', 'Rum', 'Gin', 'Tequila', 'Brandy', 'Liqueur'];

const BrandSales: React.FC = () => {
  const [startDate, setStartDate] = useState<Date | null>(null);
  const [endDate, setEndDate] = useState<Date | null>(null);
  const [category, setCategory] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [sortBy, setSortBy] = useState<string>('sales');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const [selectedBrand, setSelectedBrand] = useState<any | null>(null);
  const [brandDetailsOpen, setBrandDetailsOpen] = useState<boolean>(false);
  const [brandSales] = useState(mockBrandSales);

  // Calculate totals
  const totalSales = brandSales.reduce((sum, brand) => sum + brand.sales, 0);
  const totalUnits = brandSales.reduce((sum, brand) => sum + brand.units, 0);

  // Prepare data for category pie chart
  const categoryData = categories.map(cat => ({
    name: cat,
    value: brandSales
      .filter(brand => brand.category === cat)
      .reduce((sum, brand) => sum + brand.sales, 0),
  })).filter(item => item.value > 0);

  // Prepare data for top brands bar chart
  const topBrandsData = [...brandSales]
    .sort((a, b) => b.sales - a.sales)
    .slice(0, 5)
    .map(brand => ({
      name: brand.brand,
      sales: brand.sales,
    }));

  const clearFilters = () => {
    setStartDate(null);
    setEndDate(null);
    setCategory('all');
    setSearchQuery('');
  };

  const handleViewBrandDetails = (brand: any) => {
    setSelectedBrand(brand);
    setBrandDetailsOpen(true);
  };

  const filteredBrands = brandSales.filter(brand => {
    const matchesSearch = 
      brand.brand.toLowerCase().includes(searchQuery.toLowerCase()) ||
      brand.category.toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesCategory = 
      category === 'all' || brand.category === category;
    
    return matchesSearch && matchesCategory;
  });

  const sortedBrands = [...filteredBrands].sort((a, b) => {
    let comparison = 0;
    
    switch (sortBy) {
      case 'brand':
        comparison = a.brand.localeCompare(b.brand);
        break;
      case 'category':
        comparison = a.category.localeCompare(b.category);
        break;
      case 'sales':
        comparison = a.sales - b.sales;
        break;
      case 'units':
        comparison = a.units - b.units;
        break;
      case 'avgPrice':
        comparison = a.avgPrice - b.avgPrice;
        break;
      case 'trend':
        comparison = a.trendPercentage - b.trendPercentage;
        break;
      default:
        comparison = 0;
    }
    
    return sortOrder === 'asc' ? comparison : -comparison;
  });

  const getTrendIcon = (trend: string, percentage: number) => {
    switch (trend) {
      case 'up':
        return (
          <Box sx={{ display: 'flex', alignItems: 'center', color: 'success.main' }}>
            <TrendingUpIcon fontSize="small" sx={{ mr: 0.5 }} />
            <Typography variant="body2" sx={{ fontWeight: 'medium' }}>
              +{percentage}%
            </Typography>
          </Box>
        );
      case 'down':
        return (
          <Box sx={{ display: 'flex', alignItems: 'center', color: 'error.main' }}>
            <TrendingDownIcon fontSize="small" sx={{ mr: 0.5 }} />
            <Typography variant="body2" sx={{ fontWeight: 'medium' }}>
              -{percentage}%
            </Typography>
          </Box>
        );
      case 'flat':
        return (
          <Box sx={{ display: 'flex', alignItems: 'center', color: 'text.secondary' }}>
            <TrendingFlatIcon fontSize="small" sx={{ mr: 0.5 }} />
            <Typography variant="body2" sx={{ fontWeight: 'medium' }}>
              {percentage}%
            </Typography>
          </Box>
        );
      default:
        return null;
    }
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Box>
        <PageHeader
          title="Brand Sales Analysis"
          subtitle="Analyze sales performance by brand"
        />

        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={12} md={3}>
                <TextField
                  fullWidth
                  placeholder="Search brands"
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
                  <InputLabel id="category-label">Category</InputLabel>
                  <Select
                    labelId="category-label"
                    value={category}
                    label="Category"
                    onChange={(e) => setCategory(e.target.value)}
                  >
                    <MenuItem value="all">All Categories</MenuItem>
                    {categories.map((cat) => (
                      <MenuItem key={cat} value={cat}>{cat}</MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={6} md={2}>
                <FormControl fullWidth size="small">
                  <InputLabel id="sort-by-label">Sort By</InputLabel>
                  <Select
                    labelId="sort-by-label"
                    value={sortBy}
                    label="Sort By"
                    onChange={(e) => setSortBy(e.target.value)}
                  >
                    <MenuItem value="sales">Sales Amount</MenuItem>
                    <MenuItem value="units">Units Sold</MenuItem>
                    <MenuItem value="avgPrice">Average Price</MenuItem>
                    <MenuItem value="brand">Brand Name</MenuItem>
                    <MenuItem value="category">Category</MenuItem>
                    <MenuItem value="trend">Trend</MenuItem>
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
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                  Total Brand Sales
                </Typography>
                <Typography variant="h5" color="primary" sx={{ fontWeight: 'bold' }}>
                  ₹{totalSales.toLocaleString()}
                </Typography>
                <Typography variant="caption" color="textSecondary">
                  {brandSales.length} brands
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                  Total Units Sold
                </Typography>
                <Typography variant="h5" color="success.main" sx={{ fontWeight: 'bold' }}>
                  {totalUnits.toLocaleString()}
                </Typography>
                <Typography variant="caption" color="textSecondary">
                  Across all brands
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                  Average Price Per Unit
                </Typography>
                <Typography variant="h5" sx={{ fontWeight: 'bold', color: '#9C27B0' }}>
                  ₹{(totalSales / totalUnits).toFixed(2)}
                </Typography>
                <Typography variant="caption" color="textSecondary">
                  Overall average
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
                    Sales by Category
                  </Typography>
                  <Box sx={{ height: 300 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={categoryData}
                          cx="50%"
                          cy="50%"
                          labelLine={false}
                          outerRadius={80}
                          fill="#8884d8"
                          dataKey="value"
                          label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(1)}%`}
                        >
                          {categoryData.map((entry, index) => (
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
                    Top 5 Brands by Sales
                  </Typography>
                  <Box sx={{ height: 300 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart
                        data={topBrandsData}
                        margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                      >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="name" />
                        <YAxis />
                        <RechartsTooltip 
                          formatter={(value: any) => [`₹${value.toLocaleString()}`, '']}
                        />
                        <Legend />
                        <Bar dataKey="sales" name="Sales Amount" fill="#4CAF50" />
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
              transition={{ duration: 0.3, delay: 0.2 }}
            >
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                    <Typography variant="h6">
                      Brand Sales Analysis
                    </Typography>
                    <Button
                      variant="outlined"
                      color="primary"
                      startIcon={<DownloadIcon />}
                      onClick={() => {
                        // In a real app, this would download the report
                        console.log('Downloading report');
                      }}
                    >
                      Export Report
                    </Button>
                  </Box>
                  <TableContainer>
                    <Table>
                      <TableHead>
                        <TableRow>
                          <TableCell>Brand</TableCell>
                          <TableCell>Category</TableCell>
                          <TableCell align="right">Sales Amount</TableCell>
                          <TableCell align="right">Units Sold</TableCell>
                          <TableCell align="right">Avg. Price</TableCell>
                          <TableCell align="center">Trend</TableCell>
                          <TableCell align="center">Actions</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {sortedBrands.map((brand) => (
                          <TableRow key={brand.id} hover>
                            <TableCell>
                              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                <Avatar 
                                  sx={{ 
                                    width: 30, 
                                    height: 30, 
                                    mr: 1,
                                    bgcolor: 'background.paper',
                                    border: '1px solid',
                                    borderColor: 'divider',
                                  }}
                                >
                                  <BottleIcon fontSize="small" />
                                </Avatar>
                                <Typography variant="body2" sx={{ fontWeight: 'medium' }}>
                                  {brand.brand}
                                </Typography>
                              </Box>
                            </TableCell>
                            <TableCell>
                              <Chip 
                                label={brand.category} 
                                size="small" 
                                variant="outlined"
                              />
                            </TableCell>
                            <TableCell align="right">
                              <Typography variant="body2" sx={{ fontWeight: 'medium' }}>
                                ₹{brand.sales.toLocaleString()}
                              </Typography>
                              <Typography variant="caption" color="textSecondary">
                                {((brand.sales / totalSales) * 100).toFixed(1)}% of total
                              </Typography>
                            </TableCell>
                            <TableCell align="right">
                              <Typography variant="body2">
                                {brand.units.toLocaleString()}
                              </Typography>
                              <Typography variant="caption" color="textSecondary">
                                {((brand.units / totalUnits) * 100).toFixed(1)}% of total
                              </Typography>
                            </TableCell>
                            <TableCell align="right">
                              <Typography variant="body2">
                                ₹{brand.avgPrice.toLocaleString()}
                              </Typography>
                            </TableCell>
                            <TableCell align="center">
                              {getTrendIcon(brand.trend, brand.trendPercentage)}
                            </TableCell>
                            <TableCell align="center">
                              <Tooltip title="View Details">
                                <IconButton
                                  size="small"
                                  color="primary"
                                  onClick={() => handleViewBrandDetails(brand)}
                                >
                                  <VisibilityIcon fontSize="small" />
                                </IconButton>
                              </Tooltip>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </CardContent>
              </Card>
            </motion.div>
          </Grid>
        </Grid>

        {/* Brand Details Dialog */}
        {selectedBrand && (
          <Paper
            sx={{
              position: 'fixed',
              bottom: 0,
              right: 0,
              width: '100%',
              maxWidth: 600,
              maxHeight: '80vh',
              overflowY: 'auto',
              zIndex: 1300,
              boxShadow: 5,
              display: brandDetailsOpen ? 'block' : 'none',
            }}
          >
            <Box sx={{ p: 2, bgcolor: 'primary.main', color: 'primary.contrastText' }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="h6">
                  {selectedBrand.brand} - Brand Details
                </Typography>
                <Button 
                  variant="text" 
                  color="inherit" 
                  onClick={() => setBrandDetailsOpen(false)}
                >
                  Close
                </Button>
              </Box>
            </Box>
            <Box sx={{ p: 3 }}>
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                    Brand Information
                  </Typography>
                  <Typography variant="body1">
                    <strong>Category:</strong> {selectedBrand.category}
                  </Typography>
                  <Typography variant="body1">
                    <strong>Total Sales:</strong> ₹{selectedBrand.sales.toLocaleString()}
                  </Typography>
                  <Typography variant="body1">
                    <strong>Units Sold:</strong> {selectedBrand.units.toLocaleString()}
                  </Typography>
                  <Typography variant="body1">
                    <strong>Average Price:</strong> ₹{selectedBrand.avgPrice.toLocaleString()}
                  </Typography>
                  <Box sx={{ mt: 1 }}>
                    <Typography variant="body1">
                      <strong>Trend:</strong> {getTrendIcon(selectedBrand.trend, selectedBrand.trendPercentage)}
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                    Sales Distribution
                  </Typography>
                  <Box sx={{ height: 200 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={selectedBrand.products}
                          cx="50%"
                          cy="50%"
                          labelLine={false}
                          outerRadius={60}
                          fill="#8884d8"
                          dataKey="sales"
                          nameKey="name"
                          label={({ name, percent }) => `${(percent * 100).toFixed(0)}%`}
                        >
                          {selectedBrand.products.map((entry: any, index: number) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                          ))}
                        </Pie>
                        <RechartsTooltip 
                          formatter={(value: any) => [`₹${value.toLocaleString()}`, '']}
                        />
                      </PieChart>
                    </ResponsiveContainer>
                  </Box>
                </Grid>
                <Grid item xs={12}>
                  <Divider sx={{ my: 2 }} />
                  <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                    Products
                  </Typography>
                  <TableContainer component={Paper} variant="outlined">
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>Product</TableCell>
                          <TableCell align="right">Sales Amount</TableCell>
                          <TableCell align="right">Units Sold</TableCell>
                          <TableCell align="right">Avg. Price</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {selectedBrand.products.map((product: any, index: number) => (
                          <TableRow key={index}>
                            <TableCell>{product.name}</TableCell>
                            <TableCell align="right">₹{product.sales.toLocaleString()}</TableCell>
                            <TableCell align="right">{product.units}</TableCell>
                            <TableCell align="right">₹{(product.sales / product.units).toFixed(2)}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </Grid>
                <Grid item xs={12}>
                  <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 2 }}>
                    <Button
                      variant="outlined"
                      color="primary"
                      startIcon={<PrintIcon />}
                      onClick={() => {
                        // In a real app, this would print the brand report
                        console.log(`Printing report for ${selectedBrand.brand}`);
                      }}
                      sx={{ mr: 1 }}
                    >
                      Print Report
                    </Button>
                    <Button
                      variant="contained"
                      color="primary"
                      onClick={() => setBrandDetailsOpen(false)}
                    >
                      Close
                    </Button>
                  </Box>
                </Grid>
              </Grid>
            </Box>
          </Paper>
        )}
      </Box>
    </LocalizationProvider>
  );
};

export default BrandSales;