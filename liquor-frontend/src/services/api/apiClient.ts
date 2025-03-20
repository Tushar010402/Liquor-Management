import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';
import { getToken, refreshToken, clearTokens } from '../../utils/auth';

// API base URL from environment variables
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

/**
 * Create an Axios instance with default configuration
 */
const axiosInstance: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
});

/**
 * Request interceptor to add auth token to requests
 */
axiosInstance.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    const token = getToken();
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

/**
 * Response interceptor to handle common errors and token refresh
 */
axiosInstance.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  async (error: AxiosError) => {
    const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean };
    
    // Handle 401 Unauthorized errors (token expired)
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        // Try to refresh the token
        const newToken = await refreshToken();
        
        // If token refresh successful, retry the original request
        if (newToken && originalRequest.headers) {
          originalRequest.headers.Authorization = `Bearer ${newToken}`;
          return axiosInstance(originalRequest);
        }
      } catch (refreshError) {
        // If token refresh fails, clear tokens and redirect to login
        clearTokens();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    // Handle other errors
    return Promise.reject(error);
  }
);

/**
 * API client for making HTTP requests
 */
const apiClient = {
  /**
   * Make a GET request
   * @param url - The URL to request
   * @param params - Query parameters
   * @param config - Additional Axios config
   * @returns Promise with the response data
   */
  get: <T>(url: string, params?: any, config?: AxiosRequestConfig): Promise<T> => {
    return axiosInstance
      .get(url, { params, ...config })
      .then((response: AxiosResponse<T>) => response.data);
  },

  /**
   * Make a POST request
   * @param url - The URL to request
   * @param data - The data to send
   * @param config - Additional Axios config
   * @returns Promise with the response data
   */
  post: <T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
    return axiosInstance
      .post(url, data, config)
      .then((response: AxiosResponse<T>) => response.data);
  },

  /**
   * Make a PUT request
   * @param url - The URL to request
   * @param data - The data to send
   * @param config - Additional Axios config
   * @returns Promise with the response data
   */
  put: <T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
    return axiosInstance
      .put(url, data, config)
      .then((response: AxiosResponse<T>) => response.data);
  },

  /**
   * Make a PATCH request
   * @param url - The URL to request
   * @param data - The data to send
   * @param config - Additional Axios config
   * @returns Promise with the response data
   */
  patch: <T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
    return axiosInstance
      .patch(url, data, config)
      .then((response: AxiosResponse<T>) => response.data);
  },

  /**
   * Make a DELETE request
   * @param url - The URL to request
   * @param config - Additional Axios config
   * @returns Promise with the response data
   */
  delete: <T>(url: string, config?: AxiosRequestConfig): Promise<T> => {
    return axiosInstance
      .delete(url, config)
      .then((response: AxiosResponse<T>) => response.data);
  },
};

export default apiClient;