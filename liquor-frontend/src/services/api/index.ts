import apiClient from './apiClient';
import authService from './authService';
import tenantService from './tenantService';
import productService from './productService';
import saleService from './saleService';
import inventoryService from './inventoryService';
import cashService from './cashService';

export {
  apiClient,
  authService,
  tenantService,
  productService,
  saleService,
  inventoryService,
  cashService,
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
export type {
  CashTransaction,
  CashDepositRequest,
  UpiTransactionRequest,
  ExpenseRequest,
  CashCollectionRequest,
  CashBalance,
  DailySummary,
  DailySummaryRequest
} from './cashService';