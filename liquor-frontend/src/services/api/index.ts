import apiClient from './apiClient';
import authService from './authService';
import tenantService from './tenantService';
import productService from './productService';
import saleService from './saleService';
import inventoryService from './inventoryService';
import cashService from './cashService';
import dashboardService from './dashboardService';
import userService from './userService';

export {
  apiClient,
  authService,
  tenantService,
  productService,
  saleService,
  inventoryService,
  cashService,
  dashboardService,
  userService,
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
export type {
  DashboardStats,
  SalesOverTime,
  SalesByCategory,
  RecentSale,
  LowStockItem
} from './dashboardService';
export type {
  User,
  UserRole,
  UserStatus,
  CreateUserRequest,
  UpdateUserRequest,
  ChangePasswordRequest
} from './userService';