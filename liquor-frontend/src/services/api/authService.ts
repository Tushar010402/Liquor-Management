import apiClient from './apiClient';
import { login as authLogin, logout as authLogout } from '../../utils/auth';

/**
 * Interface for login request
 */
export interface LoginRequest {
  email: string;
  password: string;
}

/**
 * Interface for login response
 */
export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  user: {
    id: string;
    name: string;
    email: string;
    role: string;
    avatar?: string;
  };
}

/**
 * Interface for forgot password request
 */
export interface ForgotPasswordRequest {
  email: string;
}

/**
 * Interface for reset password request
 */
export interface ResetPasswordRequest {
  token: string;
  password: string;
  password_confirmation: string;
}

/**
 * Authentication service
 */
const authService = {
  /**
   * Login user
   * @param credentials - User credentials
   * @returns Promise with login response
   */
  login: (credentials: LoginRequest): Promise<LoginResponse['user']> => {
    return authLogin(credentials.email, credentials.password);
  },

  /**
   * Logout user
   * @returns Promise
   */
  logout: (): Promise<void> => {
    return authLogout();
  },

  /**
   * Send forgot password email
   * @param data - Forgot password request data
   * @returns Promise
   */
  forgotPassword: (data: ForgotPasswordRequest): Promise<void> => {
    return apiClient.post('/auth/forgot-password', data);
  },

  /**
   * Reset password
   * @param data - Reset password request data
   * @returns Promise
   */
  resetPassword: (data: ResetPasswordRequest): Promise<void> => {
    return apiClient.post('/auth/reset-password', data);
  },

  /**
   * Get current user profile
   * @returns Promise with user data
   */
  getProfile: (): Promise<LoginResponse['user']> => {
    return apiClient.get('/auth/profile');
  },

  /**
   * Update user profile
   * @param data - User profile data
   * @returns Promise with updated user data
   */
  updateProfile: (data: Partial<LoginResponse['user']>): Promise<LoginResponse['user']> => {
    return apiClient.put('/auth/profile', data);
  },

  /**
   * Change password
   * @param data - Change password data
   * @returns Promise
   */
  changePassword: (data: { current_password: string; password: string; password_confirmation: string }): Promise<void> => {
    return apiClient.post('/auth/change-password', data);
  },
};

export default authService;