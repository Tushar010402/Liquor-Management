import apiClient from './apiClient';

/**
 * User role type
 */
export type UserRole = 'saas_admin' | 'tenant_admin' | 'shop_manager' | 'assistant_manager' | 'executive';

/**
 * User status type
 */
export type UserStatus = 'active' | 'inactive' | 'pending';

/**
 * User interface
 */
export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  phone?: string;
  role: UserRole;
  status: UserStatus;
  tenant_id?: number;
  assigned_shops?: { id: string; name: string }[];
  created_at: string;
  updated_at: string;
  last_login?: string;
}

/**
 * Create user request interface
 */
export interface CreateUserRequest {
  username: string;
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  phone?: string;
  role: UserRole;
  tenant_id?: number;
  shop_ids?: number[];
}

/**
 * Update user request interface
 */
export interface UpdateUserRequest {
  email?: string;
  first_name?: string;
  last_name?: string;
  phone?: string;
  role?: UserRole;
  status?: UserStatus;
  tenant_id?: number;
  shop_ids?: number[];
}

/**
 * Change password request interface
 */
export interface ChangePasswordRequest {
  current_password: string;
  new_password: string;
  confirm_password: string;
}

/**
 * User service
 */
const userService = {
  /**
   * Get all users
   * @param tenantId - Tenant ID (optional)
   * @returns Promise with users
   */
  getUsers: (tenantId?: number): Promise<User[]> => {
    return apiClient.get('/users', tenantId ? { tenant_id: tenantId } : undefined);
  },

  /**
   * Get user by ID
   * @param userId - User ID
   * @returns Promise with user
   */
  getUserById: (userId: number): Promise<User> => {
    return apiClient.get(`/users/${userId}`);
  },

  /**
   * Create user
   * @param userData - User data
   * @returns Promise with created user
   */
  createUser: (userData: CreateUserRequest): Promise<User> => {
    return apiClient.post('/users', userData);
  },

  /**
   * Update user
   * @param userId - User ID
   * @param userData - User data
   * @returns Promise with updated user
   */
  updateUser: (userId: number, userData: UpdateUserRequest): Promise<User> => {
    return apiClient.put(`/users/${userId}`, userData);
  },

  /**
   * Delete user
   * @param userId - User ID
   * @returns Promise with success message
   */
  deleteUser: (userId: number): Promise<{ message: string }> => {
    return apiClient.delete(`/users/${userId}`);
  },

  /**
   * Change password
   * @param userId - User ID
   * @param passwordData - Password data
   * @returns Promise with success message
   */
  changePassword: (userId: number, passwordData: ChangePasswordRequest): Promise<{ message: string }> => {
    return apiClient.post(`/users/${userId}/change-password`, passwordData);
  },

  /**
   * Get user profile
   * @returns Promise with user profile
   */
  getProfile: (): Promise<User> => {
    return apiClient.get('/users/profile');
  },

  /**
   * Update user profile
   * @param profileData - Profile data
   * @returns Promise with updated user profile
   */
  updateProfile: (profileData: Partial<User>): Promise<User> => {
    return apiClient.put('/users/profile', profileData);
  },
};

export default userService;