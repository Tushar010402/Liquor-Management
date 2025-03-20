import apiClient from './apiClient';

/**
 * Interface for tenant
 */
export interface Tenant {
  id: number;
  name: string;
  email: string;
  plan: string;
  status: string;
  shops: number;
  users: number;
  created_at: string;
  subscription_ends: string;
}

/**
 * Interface for creating a tenant
 */
export interface CreateTenantRequest {
  name: string;
  email: string;
  plan: string;
  max_shops: number;
  max_users: number;
  subscription_period: number;
}

/**
 * Interface for updating a tenant
 */
export interface UpdateTenantRequest {
  name?: string;
  email?: string;
  plan?: string;
  max_shops?: number;
  max_users?: number;
  subscription_period?: number;
  status?: string;
}

/**
 * Tenant service
 */
const tenantService = {
  /**
   * Get all tenants
   * @returns Promise with tenants
   */
  getTenants: (): Promise<Tenant[]> => {
    return apiClient.get('/tenants');
  },

  /**
   * Get tenant by ID
   * @param id - Tenant ID
   * @returns Promise with tenant
   */
  getTenant: (id: number): Promise<Tenant> => {
    return apiClient.get(`/tenants/${id}`);
  },

  /**
   * Create a new tenant
   * @param data - Tenant data
   * @returns Promise with created tenant
   */
  createTenant: (data: CreateTenantRequest): Promise<Tenant> => {
    return apiClient.post('/tenants', data);
  },

  /**
   * Update a tenant
   * @param id - Tenant ID
   * @param data - Tenant data to update
   * @returns Promise with updated tenant
   */
  updateTenant: (id: number, data: UpdateTenantRequest): Promise<Tenant> => {
    return apiClient.put(`/tenants/${id}`, data);
  },

  /**
   * Delete a tenant
   * @param id - Tenant ID
   * @returns Promise
   */
  deleteTenant: (id: number): Promise<void> => {
    return apiClient.delete(`/tenants/${id}`);
  },

  /**
   * Activate a tenant
   * @param id - Tenant ID
   * @returns Promise with activated tenant
   */
  activateTenant: (id: number): Promise<Tenant> => {
    return apiClient.patch(`/tenants/${id}/activate`);
  },

  /**
   * Deactivate a tenant
   * @param id - Tenant ID
   * @returns Promise with deactivated tenant
   */
  deactivateTenant: (id: number): Promise<Tenant> => {
    return apiClient.patch(`/tenants/${id}/deactivate`);
  },

  /**
   * Get tenant statistics
   * @returns Promise with tenant statistics
   */
  getTenantStats: (): Promise<{
    total: number;
    active: number;
    inactive: number;
    growth: number;
  }> => {
    return apiClient.get('/tenants/stats');
  },
};

export default tenantService;