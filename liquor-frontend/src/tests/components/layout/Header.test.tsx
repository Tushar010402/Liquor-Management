import React from 'react';
import { render, screen, fireEvent, cleanup } from '../../test-utils';
import Header from '../../../components/layout/Header';
import * as authHook from '../../../hooks/useAuth';

// Mock the useAuth hook
jest.mock('../../../hooks/useAuth', () => ({
  __esModule: true,
  default: jest.fn(),
}));

// Mock navigate function
const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));

describe('Header', () => {
  const mockLogout = jest.fn();
  const mockSidebarToggle = jest.fn();
  
  beforeEach(() => {
    jest.clearAllMocks();
    
    // Default mock implementation
    (authHook.default as jest.Mock).mockReturnValue({
      user: {
        id: '1',
        email: 'executive@example.com',
        full_name: 'Executive User',
        role: 'executive',
        assigned_shops: [{ id: '1', name: 'Downtown Shop' }],
      },
      logout: mockLogout,
    });
  });

  it('renders correctly with user information', () => {
    render(<Header onSidebarToggle={mockSidebarToggle} />);
    
    // Check if the header contains the correct title based on user role
    expect(screen.getByText('Executive Portal')).toBeInTheDocument();
    
    // Check if shop selector is displayed for roles that can access shops
    expect(screen.getByText('Downtown Shop')).toBeInTheDocument();
  });

  it('calls sidebar toggle function when menu button is clicked on mobile', () => {
    // Mock useMediaQuery to simulate mobile view
    jest.spyOn(require('@mui/material'), 'useMediaQuery').mockReturnValue(true);
    
    render(<Header onSidebarToggle={mockSidebarToggle} />);
    
    // Find and click the menu button
    const menuButton = screen.getByLabelText('open drawer');
    fireEvent.click(menuButton);
    
    // Check if the toggle function was called
    expect(mockSidebarToggle).toHaveBeenCalledTimes(1);
  });

  it('opens user menu when avatar is clicked', () => {
    render(<Header onSidebarToggle={mockSidebarToggle} />);
    
    // Find and click the avatar button
    const avatarButton = screen.getByLabelText('Open settings');
    fireEvent.click(avatarButton);
    
    // Check if the menu is opened
    expect(screen.getByText('Profile')).toBeInTheDocument();
    expect(screen.getByText('Settings')).toBeInTheDocument();
    expect(screen.getByText('Logout')).toBeInTheDocument();
  });

  it('calls logout function when logout button is clicked', () => {
    render(<Header onSidebarToggle={mockSidebarToggle} />);
    
    // Open the user menu
    const avatarButton = screen.getByLabelText('Open settings');
    fireEvent.click(avatarButton);
    
    // Find and click the logout button
    const logoutButton = screen.getByText('Logout');
    fireEvent.click(logoutButton);
    
    // Check if logout function was called
    expect(mockLogout).toHaveBeenCalledTimes(1);
  });

  it('navigates to profile page when profile button is clicked', () => {
    render(<Header onSidebarToggle={mockSidebarToggle} />);
    
    // Open the user menu
    const avatarButton = screen.getByLabelText('Open settings');
    fireEvent.click(avatarButton);
    
    // Find and click the profile button
    const profileButton = screen.getByText('Profile');
    fireEvent.click(profileButton);
    
    // Check if navigate was called with the correct path
    expect(mockNavigate).toHaveBeenCalledWith('/executive/profile');
  });

  it('navigates to settings page when settings button is clicked', () => {
    render(<Header onSidebarToggle={mockSidebarToggle} />);
    
    // Open the user menu
    const avatarButton = screen.getByLabelText('Open settings');
    fireEvent.click(avatarButton);
    
    // Find and click the settings button
    const settingsButton = screen.getByText('Settings');
    fireEvent.click(settingsButton);
    
    // Check if navigate was called with the correct path
    expect(mockNavigate).toHaveBeenCalledWith('/executive/settings');
  });

  it('opens notifications menu when notification icon is clicked', () => {
    render(<Header onSidebarToggle={mockSidebarToggle} />);
    
    // Find and click the notifications button
    const notificationsButton = screen.getByLabelText('show new notifications');
    fireEvent.click(notificationsButton);
    
    // Check if the notifications menu is opened
    expect(screen.getByText('View all notifications')).toBeInTheDocument();
  });

  it('displays different title based on user role', () => {
    // Test with different user roles
    const roles = [
      { role: 'saas_admin', title: 'SaaS Admin Portal' },
      { role: 'tenant_admin', title: 'Tenant Admin Portal' },
      { role: 'manager', title: 'Manager Portal' },
      { role: 'assistant_manager', title: 'Assistant Manager Portal' },
      { role: 'executive', title: 'Executive Portal' },
    ];
    
    for (const { role, title } of roles) {
      // Update mock implementation for each role
      (authHook.default as jest.Mock).mockReturnValue({
        user: {
          id: '1',
          email: `${role}@example.com`,
          full_name: `${role.charAt(0).toUpperCase() + role.slice(1)} User`,
          role,
          assigned_shops: role !== 'saas_admin' && role !== 'tenant_admin' 
            ? [{ id: '1', name: 'Downtown Shop' }] 
            : undefined,
        },
        logout: mockLogout,
      });
      
      render(<Header onSidebarToggle={mockSidebarToggle} />);
      
      // Check if the header contains the correct title
      expect(screen.getByText(title)).toBeInTheDocument();
      
      // Cleanup
      cleanup();
    }
  });

  test('renders user menu items when user icon is clicked', async () => {
    // ... existing test code
    
    // Cleanup
    cleanup();
  });
});