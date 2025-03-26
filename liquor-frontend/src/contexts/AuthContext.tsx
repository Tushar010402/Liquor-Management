import React, { createContext, useState, useEffect, ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../services';
import { User, UserRole } from '../types/auth';

// Define auth context interface
interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  error: string | null;
  forgotPassword: (email: string) => Promise<void>;
  resetPassword: (password: string, token: string) => Promise<void>;
}

// Create the auth context
export const AuthContext = createContext<AuthContextType>({
  user: null,
  isAuthenticated: false,
  isLoading: true,
  login: async () => {},
  logout: () => {},
  error: null,
  forgotPassword: async () => {},
  resetPassword: async () => {},
});

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  // Check if user is already logged in
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const token = localStorage.getItem('token');
        if (token) {
          // For development/demo purposes, we'll keep the mock validation
          // In production, this would be replaced with the API call
          
          // Uncomment the following lines to use the real API in production
          // try {
          //   const { user: userData } = await authService.validateToken();
          //   setUser(userData);
          // } catch (err) {
          //   // Token is invalid or expired
          //   localStorage.removeItem('token');
          //   localStorage.removeItem('user');
          //   setUser(null);
          // }
          
          // Mock validation for development/demo
          const userData = localStorage.getItem('user');
          if (userData) {
            setUser(JSON.parse(userData));
          }
        }
      } catch (error) {
        console.error('Authentication error:', error);
        localStorage.removeItem('token');
        localStorage.removeItem('user');
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, []);

  // Login function
  const login = async (email: string, password: string) => {
    setIsLoading(true);
    setError(null);
    
    try {
      // For development/demo purposes, we'll keep the mock login
      // In production, this would be replaced with the API call
      
      // Uncomment the following line to use the real API in production
      // const { user: userData, token } = await authService.login({ email, password });
      
      // Mock login for development/demo
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
        };
      } else if (email.startsWith('tenant')) {
        mockUser = {
          id: '2',
          email,
          full_name: 'Tenant Admin User',
          role: 'tenant_admin',
          tenant_id: '550e8400-e29b-41d4-a716-446655441111',
          permissions: ['tenant_all'],
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
          navigate('/manager/dashboard');
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
    } catch (err: any) {
      console.error('Login error:', err);
      setError(err.response?.data?.message || 'Invalid email or password');
    } finally {
      setIsLoading(false);
    }
  };

  // Logout function
  const logout = async () => {
    try {
      // For development/demo purposes, we'll keep the mock logout
      // In production, this would be replaced with the API call
      
      // Uncomment the following line to use the real API in production
      // await authService.logout();
      
      // Clear local storage and state
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      setUser(null);
      navigate('/login');
    } catch (err) {
      console.error('Logout error:', err);
      // Even if the API call fails, we still want to log out locally
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      setUser(null);
      navigate('/login');
    }
  };

  // Add forgotPassword and resetPassword methods
  const forgotPassword = async (email: string) => {
    setIsLoading(true);
    setError(null);
    
    try {
      // For demo purposes, simulate API call
      // In production, replace with actual API call
      console.log('Password reset requested for:', email);
      await new Promise(resolve => setTimeout(resolve, 1000));
    } catch (err: any) {
      console.error('Password reset request error:', err);
      setError(err.response?.data?.message || 'Failed to process password reset request');
    } finally {
      setIsLoading(false);
    }
  };

  const resetPassword = async (password: string, token: string) => {
    setIsLoading(true);
    setError(null);
    
    try {
      // For demo purposes, simulate API call
      // In production, replace with actual API call
      console.log('Resetting password with token:', token);
      await new Promise(resolve => setTimeout(resolve, 1000));
    } catch (err: any) {
      console.error('Password reset error:', err);
      setError(err.response?.data?.message || 'Failed to reset password');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        logout,
        error,
        forgotPassword,
        resetPassword
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;