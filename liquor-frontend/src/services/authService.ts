import { post } from '../utils/api';
import { User } from '../types/auth';

interface LoginRequest {
  email: string;
  password: string;
}

interface LoginResponse {
  user: User;
  token: string;
}

interface ForgotPasswordRequest {
  email: string;
}

interface ResetPasswordRequest {
  token: string;
  password: string;
}

/**
 * Service for authentication-related API calls
 */
export const authService = {
  /**
   * Login user
   * @param data Login credentials
   * @returns User data and token
   */
  login: (data: LoginRequest) => {
    return post<LoginResponse>('/auth/login', data, 'Logging in...');
  },

  /**
   * Send forgot password email
   * @param data Email address
   */
  forgotPassword: (data: ForgotPasswordRequest) => {
    return post<void>('/auth/forgot-password', data, 'Sending reset link...');
  },

  /**
   * Reset password
   * @param data Reset password data
   */
  resetPassword: (data: ResetPasswordRequest) => {
    return post<void>('/auth/reset-password', data, 'Resetting password...');
  },

  /**
   * Logout user
   */
  logout: () => {
    return post<void>('/auth/logout', {}, 'Logging out...', false);
  },

  /**
   * Validate token
   * @returns User data
   */
  validateToken: () => {
    return post<{ user: User }>('/auth/validate-token', {}, undefined, false);
  },
};

export default authService;