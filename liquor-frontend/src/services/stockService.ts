import { get, post, put, del } from '../utils/api';
import { Product, PaginatedResponse } from './salesService';

// Types
export interface Supplier {
  id: number;
  name: string;
  contact_person: string;
  phone: string;
  email?: string;
  address?: string;
  created_at: string;
  updated_at: string;
}

export interface StockAdjustment {
  id: number;
  product_id: number;
  product?: Product;
  adjustment_type: 'increase' | 'decrease';
  quantity: number;
  reason: string;
  notes?: string;
  status: 'pending' | 'approved' | 'rejected';
  approved_by?: number;
  approved_at?: string;
  rejected_by?: number;
  rejected_at?: string;
  rejection_reason?: string;
  created_by: number;
  created_at: string;
  updated_at: string;
}

export interface CreateStockAdjustmentRequest {
  product_id: number;
  adjustment_type: 'increase' | 'decrease';
  quantity: number;
  reason: string;
  notes?: string;
}

export interface UpdateStockAdjustmentRequest {
  product_id?: number;
  adjustment_type?: 'increase' | 'decrease';
  quantity?: number;
  reason?: string;
  notes?: string;
}

export interface StockReturn {
  id: number;
  supplier_id: number;
  supplier?: Supplier;
  reference_number?: string;
  items: StockReturnItem[];
  total_amount: number;
  status: 'pending' | 'approved' | 'rejected';
  approved_by?: number;
  approved_at?: string;
  rejected_by?: number;
  rejected_at?: string;
  rejection_reason?: string;
  notes?: string;
  created_by: number;
  created_at: string;
  updated_at: string;
}

export interface StockReturnItem {
  id: number;
  product_id: number;
  product?: Product;
  quantity: number;
  price: number;
  reason: string;
  notes?: string;
}

export interface CreateStockReturnRequest {
  supplier_id: number;
  reference_number?: string;
  items: {
    product_id: number;
    quantity: number;
    price: number;
    reason: string;
    notes?: string;
  }[];
  notes?: string;
}

export interface UpdateStockReturnRequest {
  supplier_id?: number;
  reference_number?: string;
  items?: {
    product_id: number;
    quantity: number;
    price: number;
    reason: string;
    notes?: string;
  }[];
  notes?: string;
}

export interface StockFilter {
  start_date?: string;
  end_date?: string;
  status?: string;
  adjustment_type?: string;
  product_id?: number;
  search?: string;
  page?: number;
  limit?: number;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}

/**
 * Service for stock-related API calls
 */
export const stockService = {
  /**
   * Get all stock adjustments with optional filtering
   * @param filters Optional filters
   * @returns Paginated stock adjustments data
   */
  getStockAdjustments: (filters?: StockFilter) => {
    return get<PaginatedResponse<StockAdjustment>>(
      '/stock/adjustments',
      filters,
      'Loading adjustments...'
    );
  },

  /**
   * Get a single stock adjustment by ID
   * @param id Adjustment ID
   * @returns Stock adjustment data
   */
  getStockAdjustment: (id: number) => {
    return get<StockAdjustment>(`/stock/adjustments/${id}`, undefined, 'Loading adjustment details...');
  },

  /**
   * Create a new stock adjustment
   * @param data Adjustment data
   * @returns Created adjustment
   */
  createStockAdjustment: (data: CreateStockAdjustmentRequest) => {
    return post<StockAdjustment>('/stock/adjustments', data, 'Creating adjustment...');
  },

  /**
   * Create multiple stock adjustments in a batch
   * @param data Array of adjustment data
   * @returns Created adjustments
   */
  createBatchAdjustment: (data: CreateStockAdjustmentRequest[]) => {
    return post<StockAdjustment[]>('/stock/adjustments/batch', { adjustments: data }, 'Creating batch adjustment...');
  },

  /**
   * Update an existing stock adjustment
   * @param id Adjustment ID
   * @param data Updated adjustment data
   * @returns Updated adjustment
   */
  updateStockAdjustment: (id: number, data: UpdateStockAdjustmentRequest) => {
    return put<StockAdjustment>(`/stock/adjustments/${id}`, data, 'Updating adjustment...');
  },

  /**
   * Delete a stock adjustment
   * @param id Adjustment ID
   */
  deleteStockAdjustment: (id: number) => {
    return del<void>(`/stock/adjustments/${id}`, 'Deleting adjustment...');
  },

  /**
   * Get all stock returns with optional filtering
   * @param filters Optional filters
   * @returns Paginated stock returns data
   */
  getStockReturns: (filters?: StockFilter) => {
    return get<PaginatedResponse<StockReturn>>(
      '/stock/returns',
      filters,
      'Loading returns...'
    );
  },

  /**
   * Get a single stock return by ID
   * @param id Return ID
   * @returns Stock return data
   */
  getStockReturn: (id: number) => {
    return get<StockReturn>(`/stock/returns/${id}`, undefined, 'Loading return details...');
  },

  /**
   * Create a new stock return
   * @param data Return data
   * @returns Created return
   */
  createStockReturn: (data: CreateStockReturnRequest) => {
    return post<StockReturn>('/stock/returns', data, 'Creating return...');
  },

  /**
   * Update an existing stock return
   * @param id Return ID
   * @param data Updated return data
   * @returns Updated return
   */
  updateStockReturn: (id: number, data: UpdateStockReturnRequest) => {
    return put<StockReturn>(`/stock/returns/${id}`, data, 'Updating return...');
  },

  /**
   * Delete a stock return
   * @param id Return ID
   */
  deleteStockReturn: (id: number) => {
    return del<void>(`/stock/returns/${id}`, 'Deleting return...');
  },

  /**
   * Get all suppliers
   * @returns List of suppliers
   */
  getSuppliers: () => {
    return get<Supplier[]>('/suppliers', undefined, 'Loading suppliers...');
  },

  /**
   * Get stock levels
   * @returns Stock levels data
   */
  getStockLevels: () => {
    return get<any>('/stock/levels', undefined, 'Loading stock levels...');
  },
};

export default stockService;