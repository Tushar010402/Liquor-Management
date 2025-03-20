import { get, post, put, del } from '../utils/api';
import { PaginatedResponse } from './salesService';

// Types
export interface CashTransaction {
  id: number;
  transaction_type: 'sale' | 'expense' | 'deposit' | 'other';
  amount: number;
  payment_method: string;
  payment_details?: any;
  reference_id?: string;
  reference_type?: string;
  notes?: string;
  created_by: number;
  created_at: string;
  updated_at: string;
}

export interface CashExpense {
  id: number;
  category: string;
  amount: number;
  payment_method: string;
  payment_details?: any;
  recipient: string;
  receipt_number?: string;
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

export interface CashDeposit {
  id: number;
  amount: number;
  deposit_method: string;
  deposit_details?: any;
  bank_name: string;
  account_number: string;
  reference_number?: string;
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

export interface CreateExpenseRequest {
  category: string;
  amount: number;
  payment_method: string;
  payment_details?: any;
  recipient: string;
  receipt_number?: string;
  notes?: string;
}

export interface UpdateExpenseRequest {
  category?: string;
  amount?: number;
  payment_method?: string;
  payment_details?: any;
  recipient?: string;
  receipt_number?: string;
  notes?: string;
}

export interface CreateDepositRequest {
  amount: number;
  deposit_method: string;
  deposit_details?: any;
  bank_name: string;
  account_number: string;
  reference_number?: string;
  notes?: string;
}

export interface UpdateDepositRequest {
  amount?: number;
  deposit_method?: string;
  deposit_details?: any;
  bank_name?: string;
  account_number?: string;
  reference_number?: string;
  notes?: string;
}

export interface CashFilter {
  start_date?: string;
  end_date?: string;
  transaction_type?: string;
  payment_method?: string;
  min_amount?: number;
  max_amount?: number;
  status?: string;
  search?: string;
  page?: number;
  limit?: number;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}

export interface CashBalance {
  total_cash: number;
  total_sales: number;
  total_expenses: number;
  total_deposits: number;
  last_updated: string;
}

export interface DailySummary {
  date: string;
  opening_balance: number;
  closing_balance: number;
  total_sales: number;
  total_expenses: number;
  total_deposits: number;
  cash_sales: number;
  card_sales: number;
  upi_sales: number;
  other_sales: number;
}

/**
 * Service for cash-related API calls
 */
export const cashService = {
  /**
   * Get cash balance
   * @returns Cash balance data
   */
  getCashBalance: () => {
    return get<CashBalance>('/cash/balance', undefined, 'Loading cash balance...');
  },

  /**
   * Get daily summary
   * @param date Date for summary (defaults to today)
   * @returns Daily summary data
   */
  getDailySummary: (date?: string) => {
    return get<DailySummary>('/cash/daily-summary', { date }, 'Loading daily summary...');
  },

  /**
   * Get all cash transactions with optional filtering
   * @param filters Optional filters
   * @returns Paginated cash transactions data
   */
  getCashTransactions: (filters?: CashFilter) => {
    return get<PaginatedResponse<CashTransaction>>(
      '/cash/transactions',
      filters,
      'Loading transactions...'
    );
  },

  /**
   * Get all expenses with optional filtering
   * @param filters Optional filters
   * @returns Paginated expenses data
   */
  getExpenses: (filters?: CashFilter) => {
    return get<PaginatedResponse<CashExpense>>(
      '/cash/expenses',
      filters,
      'Loading expenses...'
    );
  },

  /**
   * Get a single expense by ID
   * @param id Expense ID
   * @returns Expense data
   */
  getExpense: (id: number) => {
    return get<CashExpense>(`/cash/expenses/${id}`, undefined, 'Loading expense details...');
  },

  /**
   * Create a new expense
   * @param data Expense data
   * @returns Created expense
   */
  createExpense: (data: CreateExpenseRequest) => {
    return post<CashExpense>('/cash/expenses', data, 'Creating expense...');
  },

  /**
   * Update an existing expense
   * @param id Expense ID
   * @param data Updated expense data
   * @returns Updated expense
   */
  updateExpense: (id: number, data: UpdateExpenseRequest) => {
    return put<CashExpense>(`/cash/expenses/${id}`, data, 'Updating expense...');
  },

  /**
   * Delete an expense
   * @param id Expense ID
   */
  deleteExpense: (id: number) => {
    return del<void>(`/cash/expenses/${id}`, 'Deleting expense...');
  },

  /**
   * Get all deposits with optional filtering
   * @param filters Optional filters
   * @returns Paginated deposits data
   */
  getDeposits: (filters?: CashFilter) => {
    return get<PaginatedResponse<CashDeposit>>(
      '/cash/deposits',
      filters,
      'Loading deposits...'
    );
  },

  /**
   * Get a single deposit by ID
   * @param id Deposit ID
   * @returns Deposit data
   */
  getDeposit: (id: number) => {
    return get<CashDeposit>(`/cash/deposits/${id}`, undefined, 'Loading deposit details...');
  },

  /**
   * Create a new deposit
   * @param data Deposit data
   * @returns Created deposit
   */
  createDeposit: (data: CreateDepositRequest) => {
    return post<CashDeposit>('/cash/deposits', data, 'Creating deposit...');
  },

  /**
   * Update an existing deposit
   * @param id Deposit ID
   * @param data Updated deposit data
   * @returns Updated deposit
   */
  updateDeposit: (id: number, data: UpdateDepositRequest) => {
    return put<CashDeposit>(`/cash/deposits/${id}`, data, 'Updating deposit...');
  },

  /**
   * Delete a deposit
   * @param id Deposit ID
   */
  deleteDeposit: (id: number) => {
    return del<void>(`/cash/deposits/${id}`, 'Deleting deposit...');
  },

  /**
   * Get payment breakdown
   * @param start_date Start date
   * @param end_date End date
   * @returns Payment breakdown data
   */
  getPaymentBreakdown: (start_date?: string, end_date?: string) => {
    return get<any>('/cash/payment-breakdown', { start_date, end_date }, 'Loading payment breakdown...');
  },
};

export default cashService;