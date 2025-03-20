import apiClient from './apiClient';
import authService from './authService';
import tenantService from './tenantService';
import productService from './productService';
import saleService from './saleService';
import inventoryService from './inventoryService';

export {
  apiClient,
  authService,
  tenantService,
  productService,
  saleService,
  inventoryService,
};

// Export types
export type { LoginRequest, LoginResponse } from './authService';
export type { Tenant, CreateTenantRequest, UpdateTenantRequest } from './tenantService';
export type { Product, CreateProductRequest, UpdateProductRequest, StockAdjustmentRequest } from './productService';
export type { Sale, SaleItem, CreateSaleRequest, SaleItemRequest } from './saleService';
export type { 
  StockTransferRequest, 
  StockTransfer, 
  StockAdjustment, 
  ExpiryTracking, 
  ExpiryTrackingRequest, 
  InventoryStatistics 
} from './inventoryService';