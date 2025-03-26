import { useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext';
import { User, UserRegistrationData } from '../types/auth';

export interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  signup: (userData: UserRegistrationData) => Promise<void>;
  updateUser: (userData: Partial<User>) => void;
  loading: boolean;
  error: string | null;
  forgotPassword: (email: string) => Promise<void>;
  resetPassword: (password: string, token: string) => Promise<void>;
}

const useAuth = () => {
  const context = useContext(AuthContext);
  
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  
  return context;
};

export default useAuth;