import React from 'react';
import { RouteObject } from 'react-router-dom';
import ProtectedRoute from '../components/auth/ProtectedRoute';
import ShopManagerLayout from '../layouts/ShopManagerLayout';
import Dashboard from '../pages/shop-manager/Dashboard';
import InventoryManagement from '../pages/shop-manager/InventoryManagement';
import SalesManagement from '../pages/shop-manager/SalesManagement';
import PointOfSale from '../pages/shop-manager/PointOfSale';
import Reports from '../pages/shop-manager/Reports';
import NotFoundPage from '../pages/NotFoundPage';

const shopManagerRoutes: RouteObject[] = [
  {
    path: '/shop-manager',
    element: (
      <ProtectedRoute allowedRoles={['shop_manager', 'manager']}>
        <ShopManagerLayout />
      </ProtectedRoute>
    ),
    children: [
      {
        path: '',
        element: <Dashboard />,
      },
      {
        path: 'dashboard',
        element: <Dashboard />,
      },
      {
        path: 'inventory',
        element: <InventoryManagement />,
      },
      {
        path: 'sales',
        element: <SalesManagement />,
      },
      {
        path: 'pos',
        element: <PointOfSale />,
      },
      {
        path: 'reports',
        element: <Reports />,
      },
      {
        path: '*',
        element: <NotFoundPage />,
      },
    ],
  },
];

export default shopManagerRoutes;