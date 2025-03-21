import apiClient from './apiClient';

/**
 * Interface for dashboard statistics
 */
export interface DashboardStats {
  today_sales: number;
  total_items: number;
  total_orders: number;
  total_customers: number;
  low_stock_count: number;
  sales_growth: number;
  orders_growth: number;
  customers_growth: number;
}

/**
 * Interface for sales over time
 */
export interface SalesOverTime {
  labels: string[];
  data: number[];
}

/**
 * Interface for sales by category
 */
export interface SalesByCategory {
  labels: string[];
  data: number[];
}

/**
 * Interface for recent sale
 */
export interface RecentSale {
  id: number;
  invoice_number: string;
  customer_name: string | null;
  items_count: number;
  total_amount: number;
  created_at: string;
  time_ago: string;
}

/**
 * Interface for low stock item
 */
export interface LowStockItem {
  id: number;
  name: string;
  stock: number;
  threshold: number;
  category: string;
}

/**
 * Dashboard service
 */
const dashboardService = {
  /**
   * Get dashboard statistics
   * @param shopId - Shop ID (optional)
   * @returns Promise with dashboard statistics
   */
  getStats: (shopId?: number): Promise<DashboardStats> => {
    return apiClient.get('/dashboard/stats', shopId ? { shop_id: shopId } : undefined);
  },

  /**
   * Get sales over time
   * @param shopId - Shop ID (optional)
   * @param period - Period (day, week, month, year)
   * @returns Promise with sales over time
   */
  getSalesOverTime: (
    shopId?: number,
    period: 'day' | 'week' | 'month' | 'year' = 'day'
  ): Promise<SalesOverTime> => {
    return apiClient.get('/dashboard/sales-over-time', { shop_id: shopId, period });
  },

  /**
   * Get sales by category
   * @param shopId - Shop ID (optional)
   * @param period - Period (day, week, month, year)
   * @returns Promise with sales by category
   */
  getSalesByCategory: (
    shopId?: number,
    period: 'day' | 'week' | 'month' | 'year' = 'day'
  ): Promise<SalesByCategory> => {
    return apiClient.get('/dashboard/sales-by-category', { shop_id: shopId, period });
  },

  /**
   * Get recent sales
   * @param shopId - Shop ID (optional)
   * @param limit - Limit (default: 5)
   * @returns Promise with recent sales
   */
  getRecentSales: (shopId?: number, limit: number = 5): Promise<RecentSale[]> => {
    return apiClient.get('/dashboard/recent-sales', { shop_id: shopId, limit });
  },

  /**
   * Get low stock items
   * @param shopId - Shop ID (optional)
   * @param limit - Limit (default: 5)
   * @returns Promise with low stock items
   */
  getLowStockItems: (shopId?: number, limit: number = 5): Promise<LowStockItem[]> => {
    return apiClient.get('/dashboard/low-stock', { shop_id: shopId, limit });
  },
};

export default dashboardService;