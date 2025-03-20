import React, { createContext, useState, useEffect, ReactNode, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../services/api';
import { getToken, isTokenValid, clearTokens, getUserFromToken } from '../utils/auth';
import { useNotification } from '../hooks';

// Define user roles
export type UserRole = 'saas_admin' | 'tenant_admin' | 'manager' | 'assistant_manager' | 'executive';

// Define user interface
export interface User {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
  tenant_id?: string;
  assigned_shops?: { id: string; name: string }[];
  permissions?: string[];
  avatar?: string;
}

// Define auth context interface
interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  updateUser: (userData: Partial<User>) => void;
  error: string | null;
}

// Create the auth context
export const AuthContext = createContext<AuthContextType>({
  user: null,
  isAuthenticated: false,
  isLoading: true,
  login: async () => {},
  logout: async () => {},
  updateUser: () => {},
  error: null,
});

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();
  const { showNotification } = useNotification();

  // Check if the user is authenticated
  const isAuthenticated = Boolean(user) && isTokenValid();

  // Initialize auth state from token
  useEffect(() => {
    const initAuth = async () => {
      try {
        if (isTokenValid()) {
          // Get user info from token
          const tokenUser = getUserFromToken();
          
          if (tokenUser) {
            try {
              // Fetch full user profile from API
              const userProfile = await authService.getProfile();
              setUser(userProfile);
            } catch (error) {
              console.error('Error fetching user profile:', error);
              clearTokens();
              setUser(null);
            }
          } else {
            clearTokens();
          }
        }
      } catch (error) {
        console.error('Error initializing auth:', error);
        clearTokens();
      } finally {
        setIsLoading(false);
      }
    };

    initAuth();
  }, []);

  /**
   * Login function
   * @param email - User email
   * @param password - User password
   */
  const login = useCallback(async (email: string, password: string) => {
    setIsLoading(true);
    setError(null);
    
    try {
      // In production environment
      if (process.env.NODE_ENV === 'production') {
        const userData = await authService.login({ email, password });
        setUser(userData);
        
        // Redirect based on user role
        if (userData.role === 'saas_admin') {
          navigate('/saas-admin/dashboard');
        } else if (userData.role === 'tenant_admin') {
          navigate('/tenant-admin/dashboard');
        } else if (userData.role === 'manager') {
          navigate('/shop-manager/dashboard');
        } else if (userData.role === 'assistant_manager') {
          navigate('/assistant-manager/dashboard');
        } else if (userData.role === 'executive') {
          navigate('/executive/dashboard');
        } else {
          navigate('/dashboard');
        }
      } else {
        // For development/demo purposes, we'll use mock login
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Mock different user roles based on email prefix
        let mockUser: User;
        
        if (email.startsWith('saas')) {
          mockUser = {
            id: '1',
            email,
            full_name: 'SaaS Admin User',
            role: 'saas_admin',
            permissions: ['all'],
            avatar: '',
          };
        } else if (email.startsWith('tenant')) {
          mockUser = {
            id: '2',
            email,
            full_name: 'Tenant Admin User',
            role: 'tenant_admin',
            tenant_id: '550e8400-e29b-41d4-a716-446655441111',
            permissions: ['tenant_all'],
            avatar: '',
          };
        } else if (email.startsWith('manager')) {
          mockUser = {
            id: '3',
            email,
            full_name: 'Manager User',
            role: 'manager',
            tenant_id: '550e8400-e29b-41d4-a716-446655441111',
            assigned_shops: [
              { id: '550e8400-e29b-41d4-a716-446655442222', name: 'Downtown Shop' },
              { id: '550e8400-e29b-41d4-a716-446655442223', name: 'Uptown Shop' },
            ],
            permissions: ['manager_permissions'],
            avatar: '',
          };
        } else if (email.startsWith('assistant')) {
          mockUser = {
            id: '4',
            email,
            full_name: 'Assistant Manager User',
            role: 'assistant_manager',
            tenant_id: '550e8400-e29b-41d4-a716-446655441111',
            assigned_shops: [
              { id: '550e8400-e29b-41d4-a716-446655442222', name: 'Downtown Shop' },
            ],
            permissions: ['assistant_permissions'],
            avatar: '',
          };
        } else {
          mockUser = {
            id: '5',
            email,
            full_name: 'Executive User',
            role: 'executive',
            tenant_id: '550e8400-e29b-41d4-a716-446655441111',
            assigned_shops: [
              { id: '550e8400-e29b-41d4-a716-446655442222', name: 'Downtown Shop' },
            ],
            permissions: ['executive_permissions'],
            avatar: '',
          };
        }
        
        // Store token and user data
        const mockToken = 'mock-jwt-token-' + Math.random().toString(36).substring(2);
        localStorage.setItem('token', mockToken);
        localStorage.setItem('user', JSON.stringify(mockUser));
        
        setUser(mockUser);
        
        // Redirect based on user role
        switch (mockUser.role) {
          case 'saas_admin':
            navigate('/saas-admin/dashboard');
            break;
          case 'tenant_admin':
            navigate('/tenant-admin/dashboard');
            break;
          case 'manager':
            navigate('/shop-manager/dashboard');
            break;
          case 'assistant_manager':
            navigate('/assistant-manager/dashboard');
            break;
          case 'executive':
            navigate('/executive/dashboard');
            break;
          default:
            navigate('/dashboard');
        }
      }
    } catch (err: any) {
      console.error('Login error:', err);
      const errorMessage = err.response?.data?.message || 'Invalid email or password';
      setError(errorMessage);
      showNotification({
        message: errorMessage,
        variant: 'error',
      });
    } finally {
      setIsLoading(false);
    }
  }, [navigate, showNotification]);

  /**
   * Logout function
   */
  const logout = useCallback(async () => {
    try {
      if (process.env.NODE_ENV === 'production') {
        await authService.logout();
      }
      
      // Clear tokens and state
      clearTokens();
      setUser(null);
      navigate('/login');
    } catch (err) {
      console.error('Logout error:', err);
      // Even if the API call fails, we still want to log out locally
      clearTokens();
      setUser(null);
      navigate('/login');
    }
  }, [navigate]);

  /**
   * Update user data
   * @param userData - Partial user data to update
   */
  const updateUser = useCallback((userData: Partial<User>) => {
    setUser((prevUser) => {
      if (!prevUser) return null;
      return { ...prevUser, ...userData };
    });
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated,
        isLoading,
        login,
        logout,
        updateUser,
        error,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;