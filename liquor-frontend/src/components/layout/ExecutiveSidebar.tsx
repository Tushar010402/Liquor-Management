import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Box,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Collapse,
  Divider,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  ShoppingCart as SalesIcon,
  Inventory as StockIcon,
  AccountBalance as CashIcon,
  BarChart as ReportsIcon,
  ExpandLess,
  ExpandMore,
  AddShoppingCart as NewSaleIcon,
  ShoppingBasket as BatchSaleIcon,
  Receipt as MySalesIcon,
  Save as DraftSalesIcon,
  Branding as BrandSalesIcon,
  InventoryOutlined as SingleAdjustmentIcon,
  Inventory2 as BatchAdjustmentIcon,
  History as MyAdjustmentsIcon,
  AssignmentReturn as CreateReturnIcon,
  Assignment as MyReturnsIcon,
  AccountBalanceWallet as CashBalanceIcon,
  LocalAtm as DepositIcon,
  MonetizationOn as ExpenseIcon,
  CalendarToday as DailySummaryIcon,
  Timeline as CashHistoryIcon,
  PieChart as PaymentBreakdownIcon,
} from '@mui/icons-material';

interface ExecutiveSidebarProps {
  onClose?: () => void;
  open?: boolean;
}

const ExecutiveSidebar: React.FC<ExecutiveSidebarProps> = ({ onClose, open }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const [openMenus, setOpenMenus] = React.useState<Record<string, boolean>>({
    sales: false,
    stock: false,
    cash: false,
    reports: false,
  });

  // Check if the current path matches the given path
  const isActive = (path: string) => {
    return location.pathname === path;
  };

  // Check if any child path is active
  const isMenuActive = (paths: string[]) => {
    return paths.some(path => location.pathname.includes(path));
  };

  // Toggle menu open/closed
  const handleMenuToggle = (menu: string) => {
    setOpenMenus(prev => ({
      ...prev,
      [menu]: !prev[menu],
    }));
  };

  // Navigate to a page and close sidebar on mobile
  const navigateTo = (path: string) => {
    navigate(path);
    if (onClose) {
      onClose();
    }
  };

  // Define menu items
  const menuItems = [
    {
      text: 'Dashboard',
      icon: <DashboardIcon />,
      path: '/executive/dashboard',
    },
    {
      text: 'Sales Management',
      icon: <SalesIcon />,
      menu: 'sales',
      active: isMenuActive(['/executive/new-sale', '/executive/batch-sale', '/executive/my-sales', '/executive/draft-sales', '/executive/brand-sales']),
      children: [
        {
          text: 'New Sale',
          icon: <NewSaleIcon />,
          path: '/executive/new-sale',
        },
        {
          text: 'Batch Sale',
          icon: <BatchSaleIcon />,
          path: '/executive/batch-sale',
        },
        {
          text: 'My Sales',
          icon: <MySalesIcon />,
          path: '/executive/my-sales',
        },
        {
          text: 'Draft Sales',
          icon: <DraftSalesIcon />,
          path: '/executive/draft-sales',
        },
        {
          text: 'Brand Sales',
          icon: <BrandSalesIcon />,
          path: '/executive/brand-sales',
        },
      ],
    },
    {
      text: 'Stock Management',
      icon: <StockIcon />,
      menu: 'stock',
      active: isMenuActive(['/executive/single-adjustment', '/executive/batch-adjustment', '/executive/my-adjustments', '/executive/create-return', '/executive/my-returns']),
      children: [
        {
          text: 'Single Adjustment',
          icon: <SingleAdjustmentIcon />,
          path: '/executive/single-adjustment',
        },
        {
          text: 'Batch Adjustment',
          icon: <BatchAdjustmentIcon />,
          path: '/executive/batch-adjustment',
        },
        {
          text: 'My Adjustments',
          icon: <MyAdjustmentsIcon />,
          path: '/executive/my-adjustments',
        },
        {
          text: 'Create Return',
          icon: <CreateReturnIcon />,
          path: '/executive/create-return',
        },
        {
          text: 'My Returns',
          icon: <MyReturnsIcon />,
          path: '/executive/my-returns',
        },
      ],
    },
    {
      text: 'Cash Management',
      icon: <CashIcon />,
      menu: 'cash',
      active: isMenuActive(['/executive/cash-balance', '/executive/record-deposit', '/executive/record-expense', '/executive/daily-summary', '/executive/cash-history', '/executive/payment-breakdown']),
      children: [
        {
          text: 'Cash Balance',
          icon: <CashBalanceIcon />,
          path: '/executive/cash-balance',
        },
        {
          text: 'Record Deposit',
          icon: <DepositIcon />,
          path: '/executive/record-deposit',
        },
        {
          text: 'Record Expense',
          icon: <ExpenseIcon />,
          path: '/executive/record-expense',
        },
        {
          text: 'Daily Summary',
          icon: <DailySummaryIcon />,
          path: '/executive/daily-summary',
        },
        {
          text: 'Cash History',
          icon: <CashHistoryIcon />,
          path: '/executive/cash-history',
        },
        {
          text: 'Payment Breakdown',
          icon: <PaymentBreakdownIcon />,
          path: '/executive/payment-breakdown',
        },
      ],
    },
    {
      text: 'Reports',
      icon: <ReportsIcon />,
      menu: 'reports',
      active: isMenuActive(['/executive/reports']),
      children: [
        {
          text: 'Sales Reports',
          icon: <BarChart />,
          path: '/executive/reports/sales',
        },
        {
          text: 'Inventory Reports',
          icon: <BarChart />,
          path: '/executive/reports/inventory',
        },
        {
          text: 'Financial Reports',
          icon: <BarChart />,
          path: '/executive/reports/financial',
        },
      ],
    },
  ];

  // Initialize open menus based on active paths
  React.useEffect(() => {
    const newOpenMenus = { ...openMenus };
    
    menuItems.forEach(item => {
      if (item.menu && item.active) {
        newOpenMenus[item.menu] = true;
      }
    });
    
    setOpenMenus(newOpenMenus);
  }, [location.pathname]); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <Box sx={{ overflow: 'auto' }}>
      <List component="nav" sx={{ p: 1 }}>
        {menuItems.map((item, index) => (
          <React.Fragment key={item.text}>
            {item.children ? (
              <>
                <ListItem disablePadding>
                  <ListItemButton
                    onClick={() => handleMenuToggle(item.menu!)}
                    selected={item.active}
                    sx={{
                      borderRadius: 1,
                      mb: 0.5,
                      '&.Mui-selected': {
                        bgcolor: 'primary.light',
                        '&:hover': {
                          bgcolor: 'primary.light',
                        },
                      },
                    }}
                  >
                    <ListItemIcon sx={{ minWidth: 40 }}>
                      {item.icon}
                    </ListItemIcon>
                    <ListItemText primary={item.text} />
                    {openMenus[item.menu!] ? <ExpandLess /> : <ExpandMore />}
                  </ListItemButton>
                </ListItem>
                <Collapse in={openMenus[item.menu!]} timeout="auto" unmountOnExit>
                  <List component="div" disablePadding>
                    {item.children.map((child) => (
                      <ListItem key={child.text} disablePadding>
                        <ListItemButton
                          onClick={() => navigateTo(child.path)}
                          selected={isActive(child.path)}
                          sx={{
                            pl: 4,
                            borderRadius: 1,
                            mb: 0.5,
                            '&.Mui-selected': {
                              bgcolor: 'primary.light',
                              '&:hover': {
                                bgcolor: 'primary.light',
                              },
                            },
                          }}
                        >
                          <ListItemIcon sx={{ minWidth: 40 }}>
                            {child.icon}
                          </ListItemIcon>
                          <ListItemText primary={child.text} />
                        </ListItemButton>
                      </ListItem>
                    ))}
                  </List>
                </Collapse>
              </>
            ) : (
              <ListItem disablePadding>
                <ListItemButton
                  onClick={() => navigateTo(item.path!)}
                  selected={isActive(item.path!)}
                  sx={{
                    borderRadius: 1,
                    mb: 0.5,
                    '&.Mui-selected': {
                      bgcolor: 'primary.light',
                      '&:hover': {
                        bgcolor: 'primary.light',
                      },
                    },
                  }}
                >
                  <ListItemIcon sx={{ minWidth: 40 }}>
                    {item.icon}
                  </ListItemIcon>
                  <ListItemText primary={item.text} />
                </ListItemButton>
              </ListItem>
            )}
            {index === 0 && <Divider sx={{ my: 1 }} />}
          </React.Fragment>
        ))}
      </List>
    </Box>
  );
};

export default ExecutiveSidebar;