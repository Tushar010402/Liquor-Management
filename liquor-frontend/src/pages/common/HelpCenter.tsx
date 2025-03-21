import React, { useState } from 'react';
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  TextField,
  InputAdornment,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Button,
  Paper,
  Chip,
  useTheme,
} from '@mui/material';
import {
  Help as HelpIcon,
  Search as SearchIcon,
  ExpandMore as ExpandMoreIcon,
  Book as BookIcon,
  VideoLibrary as VideoIcon,
  QuestionAnswer as FAQIcon,
  ContactSupport as ContactIcon,
  ShoppingCart as SalesIcon,
  Inventory as InventoryIcon,
  AttachMoney as CashIcon,
  Dashboard as DashboardIcon,
  Settings as SettingsIcon,
  People as PeopleIcon,
  Store as StoreIcon,
} from '@mui/icons-material';
import { PageHeader } from '../../components/common';
import { useTranslations } from '../../hooks';
import { useAuth } from '../../hooks';

// FAQ data
const faqData = [
  {
    category: 'General',
    icon: <HelpIcon />,
    questions: [
      {
        question: 'What is Liquor Management System?',
        answer: 'Liquor Management System is a comprehensive solution designed to help liquor shops manage inventory, sales, cash flow, and reporting in a single integrated platform.',
      },
      {
        question: 'How do I get started with the system?',
        answer: 'After logging in, you\'ll be directed to your role-specific dashboard. From there, you can navigate to different sections using the sidebar menu. We recommend starting with setting up your inventory and then proceeding to sales management.',
      },
      {
        question: 'Can I use this system on mobile devices?',
        answer: 'Yes, the Liquor Management System is fully responsive and can be used on desktops, tablets, and mobile phones. However, for the best experience, we recommend using a tablet or desktop for complex operations like inventory management.',
      },
      {
        question: 'How secure is my data?',
        answer: 'We take security very seriously. All data is encrypted both in transit and at rest. We implement role-based access control to ensure users can only access the information they need for their specific role.',
      },
    ],
  },
  {
    category: 'Sales',
    icon: <SalesIcon />,
    questions: [
      {
        question: 'How do I create a new sale?',
        answer: 'Navigate to the Point of Sale or Sales Management section, click on "New Sale", search for products by name or barcode, add them to the cart, adjust quantities if needed, and then finalize the sale by selecting a payment method.',
      },
      {
        question: 'Can I offer discounts on sales?',
        answer: 'Yes, you can apply discounts at both the product level and the entire sale. When adding items to a sale, you can specify a discount percentage or amount for individual products. Before finalizing the sale, you can also apply a discount to the entire transaction.',
      },
      {
        question: 'How do I handle returns?',
        answer: 'To process a return, go to the Sales Management section, find the original sale using the search function, click on "Process Return", select the items being returned, specify the reason for the return, and complete the process. The inventory will be automatically updated.',
      },
      {
        question: 'Can I save a sale as a draft?',
        answer: 'Yes, if a customer wants to hold items or if you need to pause a transaction, you can save it as a draft by clicking the "Save as Draft" button during the sale process. You can retrieve and complete draft sales from the Draft Sales section.',
      },
    ],
  },
  {
    category: 'Inventory',
    icon: <InventoryIcon />,
    questions: [
      {
        question: 'How do I add new products to inventory?',
        answer: 'Go to Inventory Management, click "Add Product", fill in the required details including name, category, price, cost, and initial stock quantity. You can also add optional information like description, barcode, and supplier details.',
      },
      {
        question: 'How do I update stock quantities?',
        answer: 'You can update stock in several ways: through Stock Adjustment (for corrections), Receiving Stock (for new deliveries), or Stock Transfer (for moving inventory between locations). Each process is available in the Inventory Management section.',
      },
      {
        question: 'What is the low stock threshold?',
        answer: 'The low stock threshold is the minimum quantity at which you want to be alerted that a product needs to be restocked. You can set this value when creating or editing a product. Products below this threshold will appear in the Low Stock reports.',
      },
      {
        question: 'How do I track product expiry dates?',
        answer: 'When adding or receiving stock, you can specify batch numbers and expiry dates. The system will track these dates and alert you when products are approaching expiration. You can view expiring products in the Inventory Management section under "Expiry Tracking".',
      },
    ],
  },
  {
    category: 'Cash Management',
    icon: <CashIcon />,
    questions: [
      {
        question: 'How do I record cash deposits?',
        answer: 'Navigate to the Cash Management section, select "Record Deposit", enter the amount, specify the deposit method (cash, bank transfer, etc.), add any notes, and submit the form. This will update your cash balance accordingly.',
      },
      {
        question: 'How do I record expenses?',
        answer: 'Go to Cash Management, click on "Record Expense", select the expense category, enter the amount and description, attach any receipts if needed, and submit. This will deduct the amount from your cash balance.',
      },
      {
        question: 'How do I view my daily cash summary?',
        answer: 'In the Cash Management section, click on "Daily Summary". This will show you the opening balance, total sales, expenses, deposits, and closing balance for the selected day. You can also view payment method breakdowns.',
      },
      {
        question: 'What should I do if the cash count doesn\'t match the system?',
        answer: 'If there\'s a discrepancy, you should record a cash adjustment. Go to Cash Management, select "Cash Adjustment", enter the actual cash amount, and the system will calculate the difference. Add notes explaining the discrepancy for auditing purposes.',
      },
    ],
  },
  {
    category: 'Reports',
    icon: <DashboardIcon />,
    questions: [
      {
        question: 'What reports are available in the system?',
        answer: 'The system offers various reports including Sales Reports (daily, weekly, monthly), Inventory Reports (stock levels, movements), Financial Reports (profit/loss, expenses), and Performance Reports (top-selling products, sales by staff).',
      },
      {
        question: 'Can I export reports?',
        answer: 'Yes, most reports can be exported to PDF or Excel formats. Look for the export button (usually in the top-right corner of the report) and select your preferred format.',
      },
      {
        question: 'How do I create a custom report?',
        answer: 'In the Reports section, click on "Custom Report", select the data points you want to include, specify the date range and any filters, then generate the report. You can save custom report configurations for future use.',
      },
      {
        question: 'How often are reports updated?',
        answer: 'Dashboard statistics and reports are updated in real-time as transactions occur. Historical reports are generated based on the data available at the time of the request.',
      },
    ],
  },
];

// User guide categories
const userGuideCategories = [
  {
    title: 'Getting Started',
    icon: <BookIcon />,
    description: 'Learn the basics of the Liquor Management System',
    articles: [
      'System Overview',
      'Logging In and Navigation',
      'Understanding Your Dashboard',
      'User Roles and Permissions',
    ],
  },
  {
    title: 'Sales Management',
    icon: <SalesIcon />,
    description: 'Learn how to manage sales and transactions',
    articles: [
      'Creating a New Sale',
      'Processing Returns',
      'Managing Draft Sales',
      'Applying Discounts',
    ],
  },
  {
    title: 'Inventory Management',
    icon: <InventoryIcon />,
    description: 'Learn how to manage your product inventory',
    articles: [
      'Adding New Products',
      'Stock Adjustments',
      'Low Stock Alerts',
      'Expiry Tracking',
    ],
  },
  {
    title: 'Cash Management',
    icon: <CashIcon />,
    description: 'Learn how to track cash flow and expenses',
    articles: [
      'Recording Deposits',
      'Managing Expenses',
      'Daily Cash Summary',
      'Cash Reconciliation',
    ],
  },
  {
    title: 'Reporting',
    icon: <DashboardIcon />,
    description: 'Learn how to generate and analyze reports',
    articles: [
      'Sales Reports',
      'Inventory Reports',
      'Financial Reports',
      'Custom Reports',
    ],
  },
  {
    title: 'Admin Functions',
    icon: <SettingsIcon />,
    description: 'Learn about administrative features',
    articles: [
      'User Management',
      'Shop Configuration',
      'System Settings',
      'Data Backup and Restore',
    ],
  },
];

// Video tutorials
const videoTutorials = [
  {
    title: 'Getting Started with Liquor Management System',
    duration: '5:32',
    thumbnail: '/assets/images/video-thumbnail-1.jpg',
    category: 'Basics',
  },
  {
    title: 'How to Process Sales Quickly',
    duration: '4:18',
    thumbnail: '/assets/images/video-thumbnail-2.jpg',
    category: 'Sales',
  },
  {
    title: 'Inventory Management Best Practices',
    duration: '7:45',
    thumbnail: '/assets/images/video-thumbnail-3.jpg',
    category: 'Inventory',
  },
  {
    title: 'Daily Cash Reconciliation',
    duration: '6:10',
    thumbnail: '/assets/images/video-thumbnail-4.jpg',
    category: 'Cash',
  },
  {
    title: 'Generating and Analyzing Reports',
    duration: '8:22',
    thumbnail: '/assets/images/video-thumbnail-5.jpg',
    category: 'Reports',
  },
  {
    title: 'User and Permission Management',
    duration: '5:55',
    thumbnail: '/assets/images/video-thumbnail-6.jpg',
    category: 'Admin',
  },
];

/**
 * Help Center component
 */
const HelpCenter: React.FC = () => {
  const { common } = useTranslations();
  const theme = useTheme();
  const { user } = useAuth();
  const [searchQuery, setSearchQuery] = useState('');
  const [expandedFaq, setExpandedFaq] = useState<string | false>(false);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  // Handle FAQ expansion
  const handleFaqChange = (panel: string) => (event: React.SyntheticEvent, isExpanded: boolean) => {
    setExpandedFaq(isExpanded ? panel : false);
  };

  // Filter FAQs based on search query and selected category
  const filteredFaqs = faqData.filter(category => 
    !selectedCategory || category.category === selectedCategory
  ).flatMap(category => 
    category.questions.filter(q => 
      q.question.toLowerCase().includes(searchQuery.toLowerCase()) || 
      q.answer.toLowerCase().includes(searchQuery.toLowerCase())
    ).map(q => ({ ...q, category: category.category, icon: category.icon }))
  );

  // Get role-specific help content
  const getRoleSpecificHelp = () => {
    if (!user) return null;
    
    switch (user.role) {
      case 'saas_admin':
        return (
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                SaaS Admin Resources
              </Typography>
              <Typography variant="body2" paragraph>
                As a SaaS Administrator, you have access to system-wide settings and tenant management.
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <Paper variant="outlined" sx={{ p: 2 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <PeopleIcon color="primary" sx={{ mr: 1 }} />
                      <Typography variant="subtitle1">Tenant Management</Typography>
                    </Box>
                    <Typography variant="body2">
                      Learn how to create, configure, and manage tenants in the system.
                    </Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Paper variant="outlined" sx={{ p: 2 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <SettingsIcon color="primary" sx={{ mr: 1 }} />
                      <Typography variant="subtitle1">System Configuration</Typography>
                    </Box>
                    <Typography variant="body2">
                      Learn about global system settings and configuration options.
                    </Typography>
                  </Paper>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        );
      case 'tenant_admin':
        return (
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Tenant Admin Resources
              </Typography>
              <Typography variant="body2" paragraph>
                As a Tenant Administrator, you manage shops and staff within your organization.
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <Paper variant="outlined" sx={{ p: 2 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <StoreIcon color="primary" sx={{ mr: 1 }} />
                      <Typography variant="subtitle1">Shop Management</Typography>
                    </Box>
                    <Typography variant="body2">
                      Learn how to create and configure shops for your organization.
                    </Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Paper variant="outlined" sx={{ p: 2 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <PeopleIcon color="primary" sx={{ mr: 1 }} />
                      <Typography variant="subtitle1">Staff Management</Typography>
                    </Box>
                    <Typography variant="body2">
                      Learn how to add, edit, and manage staff accounts and permissions.
                    </Typography>
                  </Paper>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        );
      case 'shop_manager':
        return (
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Shop Manager Resources
              </Typography>
              <Typography variant="body2" paragraph>
                As a Shop Manager, you oversee all operations of your assigned shop.
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <Paper variant="outlined" sx={{ p: 2 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <DashboardIcon color="primary" sx={{ mr: 1 }} />
                      <Typography variant="subtitle1">Performance Monitoring</Typography>
                    </Box>
                    <Typography variant="body2">
                      Learn how to track and analyze shop performance metrics.
                    </Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Paper variant="outlined" sx={{ p: 2 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <InventoryIcon color="primary" sx={{ mr: 1 }} />
                      <Typography variant="subtitle1">Inventory Planning</Typography>
                    </Box>
                    <Typography variant="body2">
                      Learn strategies for effective inventory management and planning.
                    </Typography>
                  </Paper>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        );
      default:
        return null;
    }
  };

  return (
    <Container maxWidth="xl">
      <PageHeader
        title="Help Center"
        subtitle="Find answers, tutorials, and support resources"
        icon={<HelpIcon fontSize="large" />}
      />

      <Card sx={{ mb: 3 }}>
        <CardContent sx={{ textAlign: 'center', py: 5 }}>
          <Typography variant="h4" gutterBottom>
            How can we help you today?
          </Typography>
          <Typography variant="body1" color="textSecondary" paragraph>
            Search for answers or browse our help resources
          </Typography>
          <Box sx={{ maxWidth: 600, mx: 'auto', mt: 3 }}>
            <TextField
              fullWidth
              placeholder="Search for help topics..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon />
                  </InputAdornment>
                ),
              }}
              variant="outlined"
              size="large"
            />
          </Box>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: 1, mt: 3 }}>
            <Chip 
              label="All Topics" 
              onClick={() => setSelectedCategory(null)}
              color={selectedCategory === null ? 'primary' : 'default'}
              variant={selectedCategory === null ? 'filled' : 'outlined'}
            />
            {faqData.map((category) => (
              <Chip 
                key={category.category}
                label={category.category}
                icon={React.cloneElement(category.icon, { fontSize: 'small' })}
                onClick={() => setSelectedCategory(category.category)}
                color={selectedCategory === category.category ? 'primary' : 'default'}
                variant={selectedCategory === category.category ? 'filled' : 'outlined'}
              />
            ))}
          </Box>
        </CardContent>
      </Card>

      {getRoleSpecificHelp()}

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Frequently Asked Questions
              </Typography>
              
              {searchQuery && filteredFaqs.length === 0 ? (
                <Box sx={{ textAlign: 'center', py: 4 }}>
                  <Typography variant="body1" color="textSecondary">
                    No results found for "{searchQuery}"
                  </Typography>
                  <Button 
                    variant="text" 
                    color="primary" 
                    onClick={() => setSearchQuery('')}
                    sx={{ mt: 1 }}
                  >
                    Clear search
                  </Button>
                </Box>
              ) : (
                filteredFaqs.map((faq, index) => (
                  <Accordion
                    key={index}
                    expanded={expandedFaq === `faq-${index}`}
                    onChange={handleFaqChange(`faq-${index}`)}
                    sx={{ mb: 1 }}
                  >
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Box sx={{ mr: 2, color: 'primary.main' }}>
                          {faq.icon}
                        </Box>
                        <Box>
                          <Typography variant="subtitle1">{faq.question}</Typography>
                          <Typography variant="caption" color="textSecondary">
                            Category: {faq.category}
                          </Typography>
                        </Box>
                      </Box>
                    </AccordionSummary>
                    <AccordionDetails>
                      <Typography variant="body1">{faq.answer}</Typography>
                    </AccordionDetails>
                  </Accordion>
                ))
              )}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                User Guides
              </Typography>
              <List>
                {userGuideCategories.map((category, index) => (
                  <React.Fragment key={index}>
                    <ListItem button>
                      <ListItemIcon>
                        {category.icon}
                      </ListItemIcon>
                      <ListItemText 
                        primary={category.title} 
                        secondary={category.description}
                      />
                    </ListItem>
                    {index < userGuideCategories.length - 1 && <Divider />}
                  </React.Fragment>
                ))}
              </List>
            </CardContent>
          </Card>

          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">
                  Video Tutorials
                </Typography>
                <Button variant="text" endIcon={<VideoIcon />}>
                  View All
                </Button>
              </Box>
              <Grid container spacing={2}>
                {videoTutorials.slice(0, 4).map((video, index) => (
                  <Grid item xs={12} key={index}>
                    <Paper variant="outlined" sx={{ p: 1 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Box 
                          sx={{ 
                            width: 80, 
                            height: 45, 
                            bgcolor: 'grey.300', 
                            mr: 2,
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                          }}
                        >
                          <VideoIcon />
                        </Box>
                        <Box>
                          <Typography variant="body2" noWrap>
                            {video.title}
                          </Typography>
                          <Box sx={{ display: 'flex', alignItems: 'center', mt: 0.5 }}>
                            <Chip 
                              label={video.category} 
                              size="small" 
                              sx={{ mr: 1, fontSize: '0.7rem' }}
                            />
                            <Typography variant="caption" color="textSecondary">
                              {video.duration}
                            </Typography>
                          </Box>
                        </Box>
                      </Box>
                    </Paper>
                  </Grid>
                ))}
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Card sx={{ mt: 3 }}>
        <CardContent sx={{ textAlign: 'center', py: 4 }}>
          <Typography variant="h6" gutterBottom>
            Need more help?
          </Typography>
          <Typography variant="body1" paragraph>
            If you couldn't find what you're looking for, our support team is here to help.
          </Typography>
          <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2, mt: 2 }}>
            <Button variant="outlined" startIcon={<FAQIcon />}>
              Browse All FAQs
            </Button>
            <Button variant="contained" color="primary" startIcon={<ContactIcon />}>
              Contact Support
            </Button>
          </Box>
        </CardContent>
      </Card>
    </Container>
  );
};

export default HelpCenter;