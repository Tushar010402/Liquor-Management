import axios, { AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';
import { store } from '../store';
import { addNotification } from '../store/slices/notificationSlice';
import { startLoading, stopLoading } from '../store/slices/loadingSlice';

// Create axios instance with default config
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor
api.interceptors.request.use(
  (config) => {
    // Get token from localStorage
    const token = localStorage.getItem('token');
    
    // If token exists, add it to request headers
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error: AxiosError) => {
    // Handle response errors
    const { response } = error;
    
    if (response) {
      // Handle different status codes
      switch (response.status) {
        case 401:
          // Unauthorized - clear token and redirect to login
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          window.location.href = '/login';
          break;
        case 403:
          // Forbidden
          store.dispatch(
            addNotification({
              message: 'You do not have permission to perform this action',
              type: 'error',
            })
          );
          break;
        case 404:
          // Not found
          store.dispatch(
            addNotification({
              message: 'The requested resource was not found',
              type: 'error',
            })
          );
          break;
        case 500:
          // Server error
          store.dispatch(
            addNotification({
              message: 'An unexpected error occurred. Please try again later',
              type: 'error',
            })
          );
          break;
        default:
          // Other errors
          const responseData = response.data as { message?: string };
          const errorMessage = responseData?.message || 'An error occurred';
          store.dispatch(
            addNotification({
              message: errorMessage,
              type: 'error',
            })
          );
      }
    } else {
      // Network error
      store.dispatch(
        addNotification({
          message: 'Network error. Please check your internet connection',
          type: 'error',
        })
      );
    }
    
    return Promise.reject(error);
  }
);

// Generic request function with loading state
export const request = async <T>(
  config: AxiosRequestConfig,
  loadingText?: string,
  showLoading: boolean = true
): Promise<T> => {
  if (showLoading) {
    store.dispatch(startLoading(loadingText));
  }
  
  try {
    const response: AxiosResponse<T> = await api(config);
    return response.data;
  } finally {
    if (showLoading) {
      store.dispatch(stopLoading());
    }
  }
};

// Helper methods for common HTTP methods
export const get = <T>(
  url: string,
  params?: any,
  loadingText?: string,
  showLoading: boolean = true
): Promise<T> => {
  return request<T>(
    {
      method: 'GET',
      url,
      params,
    },
    loadingText,
    showLoading
  );
};

export const post = <T>(
  url: string,
  data?: any,
  loadingText?: string,
  showLoading: boolean = true
): Promise<T> => {
  return request<T>(
    {
      method: 'POST',
      url,
      data,
    },
    loadingText,
    showLoading
  );
};

export const put = <T>(
  url: string,
  data?: any,
  loadingText?: string,
  showLoading: boolean = true
): Promise<T> => {
  return request<T>(
    {
      method: 'PUT',
      url,
      data,
    },
    loadingText,
    showLoading
  );
};

export const patch = <T>(
  url: string,
  data?: any,
  loadingText?: string,
  showLoading: boolean = true
): Promise<T> => {
  return request<T>(
    {
      method: 'PATCH',
      url,
      data,
    },
    loadingText,
    showLoading
  );
};

export const del = <T>(
  url: string,
  loadingText?: string,
  showLoading: boolean = true
): Promise<T> => {
  return request<T>(
    {
      method: 'DELETE',
      url,
    },
    loadingText,
    showLoading
  );
};

export default api;