import apiClient from './apiClient';

/**
 * Interface for product
 */
export interface Product {
  id: number;
  name: string;
  category: string;
  brand: string;
  price: number;
  cost_price: number;
  stock: number;
  threshold: number;
  barcode: string;
  status: string;
  description?: string;
  image?: string;
  created_at: string;
  updated_at: string;
}

/**
 * Interface for creating a product
 */
export interface CreateProductRequest {
  name: string;
  category_id: number;
  brand_id: number;
  price: number;
  cost_price: number;
  stock: number;
  threshold: number;
  barcode: string;
  description?: string;
  image?: File;
  status?: string;
}

/**
 * Interface for updating a product
 */
export interface UpdateProductRequest {
  name?: string;
  category_id?: number;
  brand_id?: number;
  price?: number;
  cost_price?: number;
  stock?: number;
  threshold?: number;
  barcode?: string;
  description?: string;
  image?: File;
  status?: string;
}

/**
 * Interface for stock adjustment
 */
export interface StockAdjustmentRequest {
  product_id: number;
  adjustment_type: 'increase' | 'decrease';
  quantity: number;
  reason: string;
  notes?: string;
}

/**
 * Product service
 */
const productService = {
  /**
   * Get all products
   * @param shopId - Shop ID (optional)
   * @returns Promise with products
   */
  getProducts: (shopId?: number): Promise<Product[]> => {
    return apiClient.get('/products', shopId ? { shop_id: shopId } : undefined);
  },

  /**
   * Get product by ID
   * @param id - Product ID
   * @returns Promise with product
   */
  getProduct: (id: number): Promise<Product> => {
    return apiClient.get(`/products/${id}`);
  },

  /**
   * Create a new product
   * @param data - Product data
   * @returns Promise with created product
   */
  createProduct: (data: CreateProductRequest): Promise<Product> => {
    // Use FormData for file uploads
    const formData = new FormData();
    Object.entries(data).forEach(([key, value]) => {
      if (value !== undefined) {
        formData.append(key, value);
      }
    });

    return apiClient.post('/products', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  /**
   * Update a product
   * @param id - Product ID
   * @param data - Product data to update
   * @returns Promise with updated product
   */
  updateProduct: (id: number, data: UpdateProductRequest): Promise<Product> => {
    // Use FormData for file uploads
    const formData = new FormData();
    Object.entries(data).forEach(([key, value]) => {
      if (value !== undefined) {
        formData.append(key, value);
      }
    });

    return apiClient.put(`/products/${id}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  /**
   * Delete a product
   * @param id - Product ID
   * @returns Promise
   */
  deleteProduct: (id: number): Promise<void> => {
    return apiClient.delete(`/products/${id}`);
  },

  /**
   * Adjust product stock
   * @param data - Stock adjustment data
   * @returns Promise with updated product
   */
  adjustStock: (data: StockAdjustmentRequest): Promise<Product> => {
    return apiClient.post('/products/adjust-stock', data);
  },

  /**
   * Get low stock products
   * @param shopId - Shop ID (optional)
   * @returns Promise with low stock products
   */
  getLowStockProducts: (shopId?: number): Promise<Product[]> => {
    return apiClient.get('/products/low-stock', shopId ? { shop_id: shopId } : undefined);
  },

  /**
   * Get out of stock products
   * @param shopId - Shop ID (optional)
   * @returns Promise with out of stock products
   */
  getOutOfStockProducts: (shopId?: number): Promise<Product[]> => {
    return apiClient.get('/products/out-of-stock', shopId ? { shop_id: shopId } : undefined);
  },

  /**
   * Search products by barcode
   * @param barcode - Product barcode
   * @returns Promise with product
   */
  searchByBarcode: (barcode: string): Promise<Product> => {
    return apiClient.get(`/products/barcode/${barcode}`);
  },

  /**
   * Import products from CSV
   * @param file - CSV file
   * @param shopId - Shop ID (optional)
   * @returns Promise with import results
   */
  importProducts: (file: File, shopId?: number): Promise<{ imported: number; errors: any[] }> => {
    const formData = new FormData();
    formData.append('file', file);
    if (shopId) {
      formData.append('shop_id', shopId.toString());
    }

    return apiClient.post('/products/import', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  /**
   * Export products to CSV
   * @param shopId - Shop ID (optional)
   * @returns Promise with file URL
   */
  exportProducts: (shopId?: number): Promise<string> => {
    return apiClient.get('/products/export', shopId ? { shop_id: shopId } : undefined);
  },
};

export default productService;