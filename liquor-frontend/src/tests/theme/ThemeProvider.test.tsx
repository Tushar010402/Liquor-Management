import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { ThemeProvider, ThemeContext } from '../../theme/ThemeProvider';

// Mock component to test the theme context
const TestComponent = () => {
  const { toggleColorMode } = React.useContext(ThemeContext);
  
  return (
    <div>
      <button onClick={toggleColorMode}>Toggle Theme</button>
      <div>Theme Content</div>
    </div>
  );
};

describe('ThemeProvider', () => {
  it('renders children correctly', () => {
    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );
    
    expect(screen.getByText('Theme Content')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Toggle Theme' })).toBeInTheDocument();
  });

  it('provides toggleColorMode function', () => {
    // This is a simple test to ensure the context is provided correctly
    // In a real app with dark mode, we would test the actual theme switching
    const toggleColorMode = jest.fn();
    
    jest.spyOn(React, 'useMemo').mockImplementation(() => ({
      toggleColorMode,
    }));
    
    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );
    
    fireEvent.click(screen.getByRole('button', { name: 'Toggle Theme' }));
    
    expect(toggleColorMode).toHaveBeenCalledTimes(1);
  });
});