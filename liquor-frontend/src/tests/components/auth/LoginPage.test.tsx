import React from 'react';
import { render, screen, fireEvent, waitFor } from '../../test-utils';
import LoginPage from '../../../pages/auth/LoginPage';
import * as authHook from '../../../hooks/useAuth';

// Mock the useAuth hook
jest.mock('../../../hooks/useAuth', () => ({
  __esModule: true,
  default: jest.fn(),
}));

describe('LoginPage', () => {
  const mockLogin = jest.fn();
  
  beforeEach(() => {
    jest.clearAllMocks();
    (authHook.default as jest.Mock).mockReturnValue({
      login: mockLogin,
      error: null,
      isLoading: false,
    });
  });

  it('renders login form correctly', () => {
    render(<LoginPage />);
    
    // Check if important elements are rendered
    expect(screen.getByText(/Sign In/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Email Address/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Sign In/i })).toBeInTheDocument();
  });

  it('shows validation errors for empty fields', async () => {
    render(<LoginPage />);
    
    // Submit the form without filling in any fields
    fireEvent.click(screen.getByRole('button', { name: /Sign In/i }));
    
    // Check for validation errors
    await waitFor(() => {
      expect(screen.getByText(/Email is required/i)).toBeInTheDocument();
      expect(screen.getByText(/Password is required/i)).toBeInTheDocument();
    });
    
    // Verify login was not called
    expect(mockLogin).not.toHaveBeenCalled();
  });

  it('calls login function with correct credentials', async () => {
    render(<LoginPage />);
    
    // Fill in the form
    fireEvent.change(screen.getByLabelText(/Email Address/i), {
      target: { value: 'test@example.com' },
    });
    
    fireEvent.change(screen.getByLabelText(/Password/i), {
      target: { value: 'password123' },
    });
    
    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: /Sign In/i }));
    
    // Verify login was called with correct credentials
    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith('test@example.com', 'password123');
    });
  });

  it('displays error message when login fails', async () => {
    // Mock the hook to return an error
    (authHook.default as jest.Mock).mockReturnValue({
      login: mockLogin,
      error: 'Invalid email or password',
      isLoading: false,
    });
    
    render(<LoginPage />);
    
    // Check if error message is displayed
    expect(screen.getByText(/Invalid email or password/i)).toBeInTheDocument();
  });

  it('disables submit button during loading state', async () => {
    // Mock the hook to return loading state
    (authHook.default as jest.Mock).mockReturnValue({
      login: mockLogin,
      error: null,
      isLoading: true,
    });
    
    render(<LoginPage />);
    
    // Check if button is disabled and shows loading text
    const submitButton = screen.getByRole('button', { name: /Signing in/i });
    expect(submitButton).toBeDisabled();
    expect(submitButton).toHaveTextContent('Signing in...');
  });
});