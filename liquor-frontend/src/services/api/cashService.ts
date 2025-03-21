import apiClient from './apiClient';

/**
 * Interface for cash transaction
 */
export interface CashTransaction {
  id: number;
  shop_id: number;
  shop_name: string;
  transaction_type: 'deposit' | 'expense' | 'upi' | 'collection';
  amount: number;
  reference_number?: string;
  payment_method: string;
  notes?: string;
  receipt_url?: string;
  status: 'pending' | 'approved' | 'rejected';
  created_by: string;
  created_at: string;
  updated_at: string;
}

/**
 * Interface for cash deposit request
 */
export interface CashDepositRequest {
  amount: number;
  reference_number?: string;
  notes?: string;
  receipt?: File;
  shop_id?: number;
}

/**
 * Interface for UPI transaction request
 */
export interface UpiTransactionRequest {
  amount: number;
  reference_number: string;
  notes?: string;
  screenshot?: File;
  shop_id?: number;
}

/**
 * Interface for expense request
 */
export interface ExpenseRequest {
  amount: number;
  category: string;
  reason: string;
  notes?: string;
  receipt?: File;
  shop_id?: number;
}

/**
 * Interface for cash collection request
 */
export interface CashCollectionRequest {
  amount: number;
  notes?: string;
  shop_id?: number;
}

/**
 * Interface for cash balance
 */
export interface CashBalance {
  shop_id: number;
  shop_name: string;
  opening_balance: number;
  closing_balance: number;
  total_deposits: number;
  total_expenses: number;
  total_upi: number;
  total_collections: number;
  last_updated: string;
}

/**
 * Interface for daily summary
 */
export interface DailySummary {
  date: string;
  shop_id: number;
  shop_name: string;
  total_sales: number;
  cash_sales: number;
  upi_sales: number;
  card_sales: number;
  other_sales: number;
  expenses: number;
  deposits: number;
  opening_balance: number;
  closing_balance: number;
  status: 'pending' | 'completed' | 'reconciled';
  created_by: string;
  created_at: string;
  updated_at: string;
}

/**
 * Interface for daily summary request
 */
export interface DailySummaryRequest {
  date: string;
  cash_sales: number;
  upi_sales: number;
  card_sales: number;
  other_sales: number;
  expenses: number;
  deposits: number;
  notes?: string;
  shop_id?: number;
}

/**
 * Cash service
 */
const cashService = {
  /**
   * Get cash transactions
   * @param shopId - Shop ID (optional)
   * @param params - Query parameters
   * @returns Promise with cash transactions
   */
  getCashTransactions: (
    shopId?: number,
    params?: {
      start_date?: string;
      end_date?: string;
      type?: string;
      status?: string;
    }
  ): Promise<CashTransaction[]> => {
    return apiClient.get('/cash/transactions', { shop_id: shopId, ...params });
  },

  /**
   * Get cash transaction by ID
   * @param id - Transaction ID
   * @returns Promise with cash transaction
   */
  getCashTransaction: (id: number): Promise<CashTransaction> => {
    return apiClient.get(`/cash/transactions/${id}`);
  },

  /**
   * Record cash deposit
   * @param data - Deposit data
   * @returns Promise with cash transaction
   */
  recordDeposit: (data: CashDepositRequest): Promise<CashTransaction> => {
    // Use FormData for file uploads
    const formData = new FormData();
    Object.entries(data).forEach(([key, value]) => {
      if (value !== undefined) {
        formData.append(key, value);
      }
    });

    return apiClient.post('/cash/deposits', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  /**
   * Record UPI transaction
   * @param data - UPI transaction data
   * @returns Promise with cash transaction
   */
  recordUpiTransaction: (data: UpiTransactionRequest): Promise<CashTransaction> => {
    // Use FormData for file uploads
    const formData = new FormData();
    Object.entries(data).forEach(([key, value]) => {
      if (value !== undefined) {
        formData.append(key, value);
      }
    });

    return apiClient.post('/cash/upi', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  /**
   * Record expense
   * @param data - Expense data
   * @returns Promise with cash transaction
   */
  recordExpense: (data: ExpenseRequest): Promise<CashTransaction> => {
    // Use FormData for file uploads
    const formData = new FormData();
    Object.entries(data).forEach(([key, value]) => {
      if (value !== undefined) {
        formData.append(key, value);
      }
    });

    return apiClient.post('/cash/expenses', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  /**
   * Record cash collection
   * @param data - Cash collection data
   * @returns Promise with cash transaction
   */
  recordCashCollection: (data: CashCollectionRequest): Promise<CashTransaction> => {
    return apiClient.post('/cash/collections', data);
  },

  /**
   * Approve cash transaction
   * @param id - Transaction ID
   * @param notes - Approval notes (optional)
   * @returns Promise with approved cash transaction
   */
  approveTransaction: (id: number, notes?: string): Promise<CashTransaction> => {
    return apiClient.post(`/cash/transactions/${id}/approve`, { notes });
  },

  /**
   * Reject cash transaction
   * @param id - Transaction ID
   * @param reason - Rejection reason
   * @returns Promise with rejected cash transaction
   */
  rejectTransaction: (id: number, reason: string): Promise<CashTransaction> => {
    return apiClient.post(`/cash/transactions/${id}/reject`, { reason });
  },

  /**
   * Get cash balance
   * @param shopId - Shop ID (optional)
   * @returns Promise with cash balance
   */
  getCashBalance: (shopId?: number): Promise<CashBalance> => {
    return apiClient.get('/cash/balance', shopId ? { shop_id: shopId } : undefined);
  },

  /**
   * Get daily summary
   * @param date - Date (YYYY-MM-DD)
   * @param shopId - Shop ID (optional)
   * @returns Promise with daily summary
   */
  getDailySummary: (date: string, shopId?: number): Promise<DailySummary> => {
    return apiClient.get('/cash/daily-summary', { date, shop_id: shopId });
  },

  /**
   * Submit daily summary
   * @param data - Daily summary data
   * @returns Promise with daily summary
   */
  submitDailySummary: (data: DailySummaryRequest): Promise<DailySummary> => {
    return apiClient.post('/cash/daily-summary', data);
  },

  /**
   * Get daily summaries
   * @param shopId - Shop ID (optional)
   * @param params - Query parameters
   * @returns Promise with daily summaries
   */
  getDailySummaries: (
    shopId?: number,
    params?: {
      start_date?: string;
      end_date?: string;
      status?: string;
    }
  ): Promise<DailySummary[]> => {
    return apiClient.get('/cash/daily-summaries', { shop_id: shopId, ...params });
  },

  /**
   * Reconcile daily summary
   * @param id - Daily summary ID
   * @param notes - Reconciliation notes (optional)
   * @returns Promise with reconciled daily summary
   */
  reconcileDailySummary: (id: number, notes?: string): Promise<DailySummary> => {
    return apiClient.post(`/cash/daily-summaries/${id}/reconcile`, { notes });
  },

  /**
   * Export cash transactions to CSV
   * @param shopId - Shop ID (optional)
   * @param params - Query parameters
   * @returns Promise with file URL
   */
  exportCashTransactions: (
    shopId?: number,
    params?: {
      start_date?: string;
      end_date?: string;
      type?: string;
      status?: string;
    }
  ): Promise<string> => {
    return apiClient.get('/cash/transactions/export', { shop_id: shopId, ...params });
  },

  /**
   * Export daily summaries to CSV
   * @param shopId - Shop ID (optional)
   * @param params - Query parameters
   * @returns Promise with file URL
   */
  exportDailySummaries: (
    shopId?: number,
    params?: {
      start_date?: string;
      end_date?: string;
      status?: string;
    }
  ): Promise<string> => {
    return apiClient.get('/cash/daily-summaries/export', { shop_id: shopId, ...params });
  },
};

export default cashService;