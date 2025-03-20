import React from 'react';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { AuthProvider, AuthContext } from '../../contexts/AuthContext';

// Mock component to test the context
const TestComponent = () => {
  const { user, isAuthenticated, login, logout } = React.useContext(AuthContext);
  
  return (
    <div>
      <div data-testid="auth-status">{isAuthenticated ? 'Authenticated' : 'Not Authenticated'}</div>
      {user && <div data-testid="user-role">{user.role}</div>}
      <button onClick={() => login('test@example.com', 'password')}>Login</button>
      <button onClick={logout}>Logout</button>
    </div>
  );
};

// Mock navigate function
const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));

describe('AuthContext', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    localStorage.clear();
    jest.useFakeTimers();
  });
  
  afterEach(() => {
    jest.useRealTimers();
  });

  it('provides initial unauthenticated state', () => {
    render(
      <MemoryRouter>
        <AuthProvider>
          <TestComponent />
        </AuthProvider>
      </MemoryRouter>
    );
    
    expect(screen.getByTestId('auth-status')).toHaveTextContent('Not Authenticated');
    expect(screen.queryByTestId('user-role')).not.toBeInTheDocument();
  });

  it('updates state and redirects after successful login', async () => {
    render(
      <MemoryRouter>
        <AuthProvider>
          <TestComponent />
        </AuthProvider>
      </MemoryRouter>
    );
    
    // Click login button
    fireEvent.click(screen.getByText('Login'));
    
    // Fast-forward timers to simulate API call
    act(() => {
      jest.advanceTimersByTime(1000);
    });
    
    // Check if state is updated
    await waitFor(() => {
      expect(screen.getByTestId('auth-status')).toHaveTextContent('Authenticated');
    });
    
    // Check if user data is stored in localStorage
    expect(localStorage.getItem('token')).toBeTruthy();
    expect(localStorage.getItem('user')).toBeTruthy();
    
    // Check if redirected based on user role
    // The exact path depends on the email used, but it should be called
    expect(mockNavigate).toHaveBeenCalled();
  });

  it('clears state and redirects to login after logout', async () => {
    // Setup authenticated state
    localStorage.setItem('token', 'mock-token');
    localStorage.setItem('user', JSON.stringify({
      id: '1',
      email: 'test@example.com',
      full_name: 'Test User',
      role: 'executive',
    }));
    
    render(
      <MemoryRouter>
        <AuthProvider>
          <TestComponent />
        </AuthProvider>
      </MemoryRouter>
    );
    
    // Verify authenticated state
    await waitFor(() => {
      expect(screen.getByTestId('auth-status')).toHaveTextContent('Authenticated');
      expect(screen.getByTestId('user-role')).toHaveTextContent('executive');
    });
    
    // Click logout button
    fireEvent.click(screen.getByText('Logout'));
    
    // Check if state is updated
    await waitFor(() => {
      expect(screen.getByTestId('auth-status')).toHaveTextContent('Not Authenticated');
    });
    
    // Check if user data is removed from localStorage
    expect(localStorage.getItem('token')).toBeNull();
    expect(localStorage.getItem('user')).toBeNull();
    
    // Check if redirected to login page
    expect(mockNavigate).toHaveBeenCalledWith('/login');
  });

  it('loads user from localStorage on initial render', async () => {
    // Setup authenticated state in localStorage
    localStorage.setItem('token', 'mock-token');
    localStorage.setItem('user', JSON.stringify({
      id: '1',
      email: 'test@example.com',
      full_name: 'Test User',
      role: 'manager',
    }));
    
    render(
      <MemoryRouter>
        <AuthProvider>
          <TestComponent />
        </AuthProvider>
      </MemoryRouter>
    );
    
    // Check if state is loaded from localStorage
    await waitFor(() => {
      expect(screen.getByTestId('auth-status')).toHaveTextContent('Authenticated');
      expect(screen.getByTestId('user-role')).toHaveTextContent('manager');
    });
  });
});