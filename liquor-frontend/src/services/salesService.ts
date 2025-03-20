import { get, post, put, del } from '../utils/api';

// Types
export interface Product {
  id: number;
  name: string;
  category: string;
  price: number;
  stock: number;
  brand?: string;
  description?: string;
  image_url?: string;
  barcode?: string;
  created_at: string;
  updated_at: string;
}

export interface Customer {
  id: number;
  name: string;
  phone: string;
  email?: string;
  address?: string;
  created_at: string;
  updated_at: string;
}

export interface SaleItem {
  product_id: number;
  quantity: number;
  price: number;
  discount?: number;
  total: number;
}

export interface Sale {
  id: number;
  invoice_number: string;
  customer_id?: number;
  customer?: Customer;
  items: SaleItem[];
  subtotal: number;
  discount?: number;
  tax?: number;
  total: number;
  payment_method: string;
  payment_details?: any;
  status: 'draft' | 'pending' | 'completed' | 'cancelled';
  notes?: string;
  created_by: number;
  created_at: string;
  updated_at: string;
}

export interface CreateSaleRequest {
  customer_id?: number;
  items: Omit<SaleItem, 'total'>[];
  discount?: number;
  tax?: number;
  payment_method: string;
  payment_details?: any;
  status: 'draft' | 'completed';
  notes?: string;
}

export interface UpdateSaleRequest {
  customer_id?: number;
  items?: Omit<SaleItem, 'total'>[];
  discount?: number;
  tax?: number;
  payment_method?: string;
  payment_details?: any;
  status?: 'draft' | 'completed' | 'cancelled';
  notes?: string;
}

export interface SalesFilter {
  start_date?: string;
  end_date?: string;
  status?: string;
  payment_method?: string;
  customer_id?: number;
  min_amount?: number;
  max_amount?: number;
  search?: string;
  page?: number;
  limit?: number;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}

export interface PaginatedResponse<T> {
  data: T[];
  meta: {
    current_page: number;
    from: number;
    last_page: number;
    path: string;
    per_page: number;
    to: number;
    total: number;
  };
}

/**
 * Service for sales-related API calls
 */
export const salesService = {
  /**
   * Get all sales with optional filtering
   * @param filters Optional filters
   * @returns Paginated sales data
   */
  getSales: (filters?: SalesFilter) => {
    return get<PaginatedResponse<Sale>>('/sales', filters, 'Loading sales...');
  },

  /**
   * Get a single sale by ID
   * @param id Sale ID
   * @returns Sale data
   */
  getSale: (id: number) => {
    return get<Sale>(`/sales/${id}`, undefined, 'Loading sale details...');
  },

  /**
   * Create a new sale
   * @param data Sale data
   * @returns Created sale
   */
  createSale: (data: CreateSaleRequest) => {
    return post<Sale>('/sales', data, 'Creating sale...');
  },

  /**
   * Update an existing sale
   * @param id Sale ID
   * @param data Updated sale data
   * @returns Updated sale
   */
  updateSale: (id: number, data: UpdateSaleRequest) => {
    return put<Sale>(`/sales/${id}`, data, 'Updating sale...');
  },

  /**
   * Delete a sale
   * @param id Sale ID
   */
  deleteSale: (id: number) => {
    return del<void>(`/sales/${id}`, 'Deleting sale...');
  },

  /**
   * Get all products
   * @returns List of products
   */
  getProducts: () => {
    return get<Product[]>('/products', undefined, 'Loading products...');
  },

  /**
   * Get all customers
   * @returns List of customers
   */
  getCustomers: () => {
    return get<Customer[]>('/customers', undefined, 'Loading customers...');
  },

  /**
   * Get sales statistics
   * @param start_date Start date
   * @param end_date End date
   * @returns Sales statistics
   */
  getSalesStatistics: (start_date?: string, end_date?: string) => {
    return get<any>('/sales/statistics', { start_date, end_date }, 'Loading statistics...');
  },

  /**
   * Get brand sales
   * @param start_date Start date
   * @param end_date End date
   * @returns Brand sales data
   */
  getBrandSales: (start_date?: string, end_date?: string) => {
    return get<any>('/sales/brands', { start_date, end_date }, 'Loading brand sales...');
  },
};

export default salesService;