import apiClient from './apiClient';
import productService, { Product, StockAdjustmentRequest } from './productService';

/**
 * Interface for stock transfer
 */
export interface StockTransferRequest {
  product_id: number;
  from_shop_id: number;
  to_shop_id: number;
  quantity: number;
  notes?: string;
}

/**
 * Interface for stock transfer response
 */
export interface StockTransfer {
  id: number;
  product_id: number;
  product_name: string;
  from_shop_id: number;
  from_shop_name: string;
  to_shop_id: number;
  to_shop_name: string;
  quantity: number;
  status: 'pending' | 'approved' | 'rejected' | 'completed';
  notes?: string;
  created_by: string;
  created_at: string;
  updated_at: string;
}

/**
 * Interface for stock adjustment response
 */
export interface StockAdjustment {
  id: number;
  product_id: number;
  product_name: string;
  shop_id: number;
  shop_name: string;
  adjustment_type: 'increase' | 'decrease';
  quantity: number;
  reason: string;
  notes?: string;
  status: 'pending' | 'approved' | 'rejected';
  created_by: string;
  created_at: string;
  updated_at: string;
}

/**
 * Interface for expiry tracking
 */
export interface ExpiryTracking {
  id: number;
  product_id: number;
  product_name: string;
  shop_id: number;
  shop_name: string;
  batch_number: string;
  quantity: number;
  expiry_date: string;
  status: 'active' | 'expired' | 'disposed';
  created_at: string;
  updated_at: string;
}

/**
 * Interface for expiry tracking request
 */
export interface ExpiryTrackingRequest {
  product_id: number;
  batch_number: string;
  quantity: number;
  expiry_date: string;
  shop_id?: number;
}

/**
 * Interface for inventory statistics
 */
export interface InventoryStatistics {
  total_products: number;
  total_stock_value: number;
  low_stock_count: number;
  out_of_stock_count: number;
  expiring_soon_count: number;
  expired_count: number;
}

/**
 * Inventory service
 */
const inventoryService = {
  /**
   * Get all products (alias for productService.getProducts)
   * @param shopId - Shop ID (optional)
   * @returns Promise with products
   */
  getProducts: (shopId?: number): Promise<Product[]> => {
    return productService.getProducts(shopId);
  },

  /**
   * Get low stock products (alias for productService.getLowStockProducts)
   * @param shopId - Shop ID (optional)
   * @returns Promise with low stock products
   */
  getLowStockProducts: (shopId?: number): Promise<Product[]> => {
    return productService.getLowStockProducts(shopId);
  },

  /**
   * Get out of stock products (alias for productService.getOutOfStockProducts)
   * @param shopId - Shop ID (optional)
   * @returns Promise with out of stock products
   */
  getOutOfStockProducts: (shopId?: number): Promise<Product[]> => {
    return productService.getOutOfStockProducts(shopId);
  },

  /**
   * Adjust product stock (alias for productService.adjustStock)
   * @param data - Stock adjustment data
   * @returns Promise with updated product
   */
  adjustStock: (data: StockAdjustmentRequest): Promise<Product> => {
    return productService.adjustStock(data);
  },

  /**
   * Get stock adjustments
   * @param shopId - Shop ID (optional)
   * @param status - Status filter (optional)
   * @returns Promise with stock adjustments
   */
  getStockAdjustments: (shopId?: number, status?: string): Promise<StockAdjustment[]> => {
    const params: any = {};
    if (shopId) params.shop_id = shopId;
    if (status) params.status = status;
    
    return apiClient.get('/inventory/adjustments', params);
  },

  /**
   * Get stock adjustment by ID
   * @param id - Adjustment ID
   * @returns Promise with stock adjustment
   */
  getStockAdjustment: (id: number): Promise<StockAdjustment> => {
    return apiClient.get(`/inventory/adjustments/${id}`);
  },

  /**
   * Approve stock adjustment
   * @param id - Adjustment ID
   * @param notes - Approval notes (optional)
   * @returns Promise with approved stock adjustment
   */
  approveStockAdjustment: (id: number, notes?: string): Promise<StockAdjustment> => {
    return apiClient.post(`/inventory/adjustments/${id}/approve`, { notes });
  },

  /**
   * Reject stock adjustment
   * @param id - Adjustment ID
   * @param notes - Rejection notes (optional)
   * @returns Promise with rejected stock adjustment
   */
  rejectStockAdjustment: (id: number, notes?: string): Promise<StockAdjustment> => {
    return apiClient.post(`/inventory/adjustments/${id}/reject`, { notes });
  },

  /**
   * Transfer stock between shops
   * @param data - Stock transfer data
   * @returns Promise with stock transfer
   */
  transferStock: (data: StockTransferRequest): Promise<StockTransfer> => {
    return apiClient.post('/inventory/transfers', data);
  },

  /**
   * Get stock transfers
   * @param shopId - Shop ID (optional)
   * @param status - Status filter (optional)
   * @returns Promise with stock transfers
   */
  getStockTransfers: (shopId?: number, status?: string): Promise<StockTransfer[]> => {
    const params: any = {};
    if (shopId) params.shop_id = shopId;
    if (status) params.status = status;
    
    return apiClient.get('/inventory/transfers', params);
  },

  /**
   * Get stock transfer by ID
   * @param id - Transfer ID
   * @returns Promise with stock transfer
   */
  getStockTransfer: (id: number): Promise<StockTransfer> => {
    return apiClient.get(`/inventory/transfers/${id}`);
  },

  /**
   * Approve stock transfer
   * @param id - Transfer ID
   * @param notes - Approval notes (optional)
   * @returns Promise with approved stock transfer
   */
  approveStockTransfer: (id: number, notes?: string): Promise<StockTransfer> => {
    return apiClient.post(`/inventory/transfers/${id}/approve`, { notes });
  },

  /**
   * Reject stock transfer
   * @param id - Transfer ID
   * @param notes - Rejection notes (optional)
   * @returns Promise with rejected stock transfer
   */
  rejectStockTransfer: (id: number, notes?: string): Promise<StockTransfer> => {
    return apiClient.post(`/inventory/transfers/${id}/reject`, { notes });
  },

  /**
   * Complete stock transfer
   * @param id - Transfer ID
   * @param notes - Completion notes (optional)
   * @returns Promise with completed stock transfer
   */
  completeStockTransfer: (id: number, notes?: string): Promise<StockTransfer> => {
    return apiClient.post(`/inventory/transfers/${id}/complete`, { notes });
  },

  /**
   * Track product expiry
   * @param data - Expiry tracking data
   * @returns Promise with expiry tracking
   */
  trackExpiry: (data: ExpiryTrackingRequest): Promise<ExpiryTracking> => {
    return apiClient.post('/inventory/expiry', data);
  },

  /**
   * Get expiry tracking
   * @param shopId - Shop ID (optional)
   * @param status - Status filter (optional)
   * @returns Promise with expiry tracking
   */
  getExpiryTracking: (shopId?: number, status?: string): Promise<ExpiryTracking[]> => {
    const params: any = {};
    if (shopId) params.shop_id = shopId;
    if (status) params.status = status;
    
    return apiClient.get('/inventory/expiry', params);
  },

  /**
   * Get expiring soon products
   * @param shopId - Shop ID (optional)
   * @param days - Days until expiry (default: 30)
   * @returns Promise with expiring soon products
   */
  getExpiringSoonProducts: (shopId?: number, days: number = 30): Promise<ExpiryTracking[]> => {
    const params: any = { days };
    if (shopId) params.shop_id = shopId;
    
    return apiClient.get('/inventory/expiry/expiring-soon', params);
  },

  /**
   * Get expired products
   * @param shopId - Shop ID (optional)
   * @returns Promise with expired products
   */
  getExpiredProducts: (shopId?: number): Promise<ExpiryTracking[]> => {
    const params: any = {};
    if (shopId) params.shop_id = shopId;
    
    return apiClient.get('/inventory/expiry/expired', params);
  },

  /**
   * Mark product as disposed
   * @param id - Expiry tracking ID
   * @param notes - Disposal notes (optional)
   * @returns Promise with disposed expiry tracking
   */
  markAsDisposed: (id: number, notes?: string): Promise<ExpiryTracking> => {
    return apiClient.post(`/inventory/expiry/${id}/dispose`, { notes });
  },

  /**
   * Get inventory statistics
   * @param shopId - Shop ID (optional)
   * @returns Promise with inventory statistics
   */
  getInventoryStatistics: (shopId?: number): Promise<InventoryStatistics> => {
    const params: any = {};
    if (shopId) params.shop_id = shopId;
    
    return apiClient.get('/inventory/statistics', params);
  },
};

export default inventoryService;