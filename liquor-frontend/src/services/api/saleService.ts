import apiClient from './apiClient';

/**
 * Interface for sale item
 */
export interface SaleItem {
  id: number;
  product_id: number;
  product_name: string;
  quantity: number;
  price: number;
  total: number;
}

/**
 * Interface for sale
 */
export interface Sale {
  id: number;
  invoice_number: string;
  customer_id?: number;
  customer_name?: string;
  customer_phone?: string;
  date: string;
  time: string;
  items_count: number;
  total_amount: number;
  payment_method: string;
  status: string;
  created_by: string;
  created_at: string;
  updated_at: string;
  items?: SaleItem[];
}

/**
 * Interface for sale item request
 */
export interface SaleItemRequest {
  product_id: number;
  quantity: number;
  price: number;
}

/**
 * Interface for creating a sale
 */
export interface CreateSaleRequest {
  customer_id?: number;
  customer_name?: string;
  customer_phone?: string;
  payment_method: string;
  items: SaleItemRequest[];
  discount_type?: 'percentage' | 'fixed';
  discount_value?: number;
  notes?: string;
}

/**
 * Sale service
 */
const saleService = {
  /**
   * Get all sales
   * @param shopId - Shop ID (optional)
   * @param params - Query parameters
   * @returns Promise with sales
   */
  getSales: (
    shopId?: number,
    params?: {
      start_date?: string;
      end_date?: string;
      status?: string;
      payment_method?: string;
    }
  ): Promise<Sale[]> => {
    return apiClient.get('/sales', { shop_id: shopId, ...params });
  },

  /**
   * Get sale by ID
   * @param id - Sale ID
   * @returns Promise with sale
   */
  getSale: (id: number): Promise<Sale> => {
    return apiClient.get(`/sales/${id}`);
  },

  /**
   * Create a new sale
   * @param data - Sale data
   * @param shopId - Shop ID (optional)
   * @returns Promise with created sale
   */
  createSale: (data: CreateSaleRequest, shopId?: number): Promise<Sale> => {
    return apiClient.post('/sales', { ...data, shop_id: shopId });
  },

  /**
   * Cancel a sale
   * @param id - Sale ID
   * @param reason - Cancellation reason
   * @returns Promise with cancelled sale
   */
  cancelSale: (id: number, reason: string): Promise<Sale> => {
    return apiClient.patch(`/sales/${id}/cancel`, { reason });
  },

  /**
   * Get sale items
   * @param saleId - Sale ID
   * @returns Promise with sale items
   */
  getSaleItems: (saleId: number): Promise<SaleItem[]> => {
    return apiClient.get(`/sales/${saleId}/items`);
  },

  /**
   * Get sales statistics
   * @param shopId - Shop ID (optional)
   * @param params - Query parameters
   * @returns Promise with sales statistics
   */
  getSalesStats: (
    shopId?: number,
    params?: {
      start_date?: string;
      end_date?: string;
    }
  ): Promise<{
    total_sales: number;
    total_orders: number;
    average_order_value: number;
    sales_by_category: { category: string; percentage: number }[];
    sales_by_payment_method: { method: string; percentage: number }[];
  }> => {
    return apiClient.get('/sales/stats', { shop_id: shopId, ...params });
  },

  /**
   * Get top selling products
   * @param shopId - Shop ID (optional)
   * @param params - Query parameters
   * @returns Promise with top selling products
   */
  getTopSellingProducts: (
    shopId?: number,
    params?: {
      start_date?: string;
      end_date?: string;
      limit?: number;
    }
  ): Promise<{
    id: number;
    name: string;
    category: string;
    quantity: number;
    revenue: number;
  }[]> => {
    return apiClient.get('/sales/top-products', { shop_id: shopId, ...params });
  },

  /**
   * Get top customers
   * @param shopId - Shop ID (optional)
   * @param params - Query parameters
   * @returns Promise with top customers
   */
  getTopCustomers: (
    shopId?: number,
    params?: {
      start_date?: string;
      end_date?: string;
      limit?: number;
    }
  ): Promise<{
    id: number;
    name: string;
    purchases: number;
    revenue: number;
  }[]> => {
    return apiClient.get('/sales/top-customers', { shop_id: shopId, ...params });
  },

  /**
   * Export sales to CSV
   * @param shopId - Shop ID (optional)
   * @param params - Query parameters
   * @returns Promise with file URL
   */
  exportSales: (
    shopId?: number,
    params?: {
      start_date?: string;
      end_date?: string;
      status?: string;
      payment_method?: string;
    }
  ): Promise<string> => {
    return apiClient.get('/sales/export', { shop_id: shopId, ...params });
  },

  /**
   * Generate invoice PDF
   * @param id - Sale ID
   * @returns Promise with PDF URL
   */
  generateInvoice: (id: number): Promise<string> => {
    return apiClient.get(`/sales/${id}/invoice`);
  },
};

export default saleService;