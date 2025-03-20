import React from 'react';
import { render, screen } from '../../test-utils';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import ProtectedRoute from '../../../components/auth/ProtectedRoute';
import * as authHook from '../../../hooks/useAuth';

// Mock the useAuth hook
jest.mock('../../../hooks/useAuth', () => ({
  __esModule: true,
  default: jest.fn(),
}));

// Mock components for testing
const MockDashboard = () => <div>Dashboard Content</div>;
const MockLogin = () => <div>Login Page</div>;

describe('ProtectedRoute', () => {
  const mockNavigate = jest.fn();
  
  // Mock useNavigate
  jest.mock('react-router-dom', () => ({
    ...jest.requireActual('react-router-dom'),
    useNavigate: () => mockNavigate,
  }));
  
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('shows loading spinner when authentication is being checked', () => {
    // Mock the hook to return loading state
    (authHook.default as jest.Mock).mockReturnValue({
      isAuthenticated: false,
      isLoading: true,
      user: null,
    });
    
    render(
      <MemoryRouter initialEntries={['/dashboard']}>
        <Routes>
          <Route path="/login" element={<MockLogin />} />
          <Route element={<ProtectedRoute />}>
            <Route path="/dashboard" element={<MockDashboard />} />
          </Route>
        </Routes>
      </MemoryRouter>
    );
    
    // Check if loading spinner is displayed
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
    expect(screen.queryByText('Dashboard Content')).not.toBeInTheDocument();
    expect(screen.queryByText('Login Page')).not.toBeInTheDocument();
  });

  it('redirects to login page when user is not authenticated', () => {
    // Mock the hook to return unauthenticated state
    (authHook.default as jest.Mock).mockReturnValue({
      isAuthenticated: false,
      isLoading: false,
      user: null,
    });
    
    render(
      <MemoryRouter initialEntries={['/dashboard']}>
        <Routes>
          <Route path="/login" element={<MockLogin />} />
          <Route element={<ProtectedRoute />}>
            <Route path="/dashboard" element={<MockDashboard />} />
          </Route>
        </Routes>
      </MemoryRouter>
    );
    
    // Check if redirected to login page
    expect(screen.queryByText('Dashboard Content')).not.toBeInTheDocument();
    expect(screen.getByText('Login Page')).toBeInTheDocument();
  });

  it('renders protected content when user is authenticated', () => {
    // Mock the hook to return authenticated state
    (authHook.default as jest.Mock).mockReturnValue({
      isAuthenticated: true,
      isLoading: false,
      user: { role: 'executive' },
    });
    
    render(
      <MemoryRouter initialEntries={['/dashboard']}>
        <Routes>
          <Route path="/login" element={<MockLogin />} />
          <Route element={<ProtectedRoute />}>
            <Route path="/dashboard" element={<MockDashboard />} />
          </Route>
        </Routes>
      </MemoryRouter>
    );
    
    // Check if protected content is rendered
    expect(screen.getByText('Dashboard Content')).toBeInTheDocument();
    expect(screen.queryByText('Login Page')).not.toBeInTheDocument();
  });

  it('redirects to appropriate dashboard when user role does not match allowed roles', () => {
    // Mock the hook to return authenticated state with executive role
    (authHook.default as jest.Mock).mockReturnValue({
      isAuthenticated: true,
      isLoading: false,
      user: { role: 'executive' },
    });
    
    render(
      <MemoryRouter initialEntries={['/admin-dashboard']}>
        <Routes>
          <Route path="/login" element={<MockLogin />} />
          <Route path="/executive/dashboard" element={<div>Executive Dashboard</div>} />
          <Route element={<ProtectedRoute allowedRoles={['manager', 'tenant_admin']} />}>
            <Route path="/admin-dashboard" element={<div>Admin Dashboard</div>} />
          </Route>
        </Routes>
      </MemoryRouter>
    );
    
    // Check if redirected to executive dashboard
    expect(screen.queryByText('Admin Dashboard')).not.toBeInTheDocument();
    expect(screen.getByText('Executive Dashboard')).toBeInTheDocument();
  });
});