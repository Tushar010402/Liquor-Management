import axios from 'axios';
import jwtDecode from 'jwt-decode';

// Token storage keys
const ACCESS_TOKEN_KEY = 'access_token';
const REFRESH_TOKEN_KEY = 'refresh_token';

// API base URL from environment variables
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

/**
 * Interface for JWT token payload
 */
interface TokenPayload {
  sub: string; // User ID
  role: string; // User role
  exp: number; // Expiration timestamp
  iat: number; // Issued at timestamp
}

/**
 * Get the access token from localStorage
 * @returns The access token or null if not found
 */
export const getToken = (): string | null => {
  return localStorage.getItem(ACCESS_TOKEN_KEY);
};

/**
 * Get the refresh token from localStorage
 * @returns The refresh token or null if not found
 */
export const getRefreshToken = (): string | null => {
  return localStorage.getItem(REFRESH_TOKEN_KEY);
};

/**
 * Set the access token in localStorage
 * @param token - The access token to store
 */
export const setToken = (token: string): void => {
  localStorage.setItem(ACCESS_TOKEN_KEY, token);
};

/**
 * Set the refresh token in localStorage
 * @param token - The refresh token to store
 */
export const setRefreshToken = (token: string): void => {
  localStorage.setItem(REFRESH_TOKEN_KEY, token);
};

/**
 * Clear all tokens from localStorage
 */
export const clearTokens = (): void => {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
};

/**
 * Check if the access token is valid (not expired)
 * @returns True if the token is valid, false otherwise
 */
export const isTokenValid = (): boolean => {
  const token = getToken();
  if (!token) return false;

  try {
    const decoded = jwtDecode<TokenPayload>(token);
    const currentTime = Date.now() / 1000;
    return decoded.exp > currentTime;
  } catch (error) {
    return false;
  }
};

/**
 * Get user information from the token
 * @returns User information or null if token is invalid
 */
export const getUserFromToken = (): { id: string; role: string } | null => {
  const token = getToken();
  if (!token) return null;

  try {
    const decoded = jwtDecode<TokenPayload>(token);
    return {
      id: decoded.sub,
      role: decoded.role,
    };
  } catch (error) {
    return null;
  }
};

/**
 * Refresh the access token using the refresh token
 * @returns Promise with the new access token
 */
export const refreshToken = async (): Promise<string> => {
  const refreshToken = getRefreshToken();
  if (!refreshToken) {
    throw new Error('No refresh token available');
  }

  try {
    const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
      refresh_token: refreshToken,
    });

    const { access_token } = response.data;
    setToken(access_token);
    return access_token;
  } catch (error) {
    clearTokens();
    throw error;
  }
};

/**
 * Login user with credentials
 * @param email - User email
 * @param password - User password
 * @returns Promise with user data
 */
export const login = async (email: string, password: string): Promise<any> => {
  try {
    const response = await axios.post(`${API_BASE_URL}/auth/login`, {
      email,
      password,
    });

    const { access_token, refresh_token, user } = response.data;
    setToken(access_token);
    setRefreshToken(refresh_token);
    return user;
  } catch (error) {
    throw error;
  }
};

/**
 * Logout user
 */
export const logout = async (): Promise<void> => {
  try {
    const token = getToken();
    if (token) {
      await axios.post(
        `${API_BASE_URL}/auth/logout`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
    }
  } catch (error) {
    console.error('Logout error:', error);
  } finally {
    clearTokens();
  }
};