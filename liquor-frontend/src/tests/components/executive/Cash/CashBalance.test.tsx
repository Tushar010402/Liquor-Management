import React from 'react';
import { render, screen, fireEvent, waitFor } from '../../../test-utils';
import CashBalance from '../../../../pages/executive/Cash/CashBalance';

// Mock navigate function
const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));

describe('CashBalance', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders cash balance information correctly', () => {
    render(<CashBalance />);
    
    // Check if the page title is rendered
    expect(screen.getByText('Cash Balance')).toBeInTheDocument();
    
    // Check if the cash balance card is rendered
    expect(screen.getByText('Current Cash Balance')).toBeInTheDocument();
    
    // Check if the transaction history section is rendered
    expect(screen.getByText('Recent Transactions')).toBeInTheDocument();
  });

  it('navigates to record deposit page when deposit button is clicked', () => {
    render(<CashBalance />);
    
    // Find and click the Record Deposit button
    const depositButton = screen.getByText('Record Deposit');
    fireEvent.click(depositButton);
    
    // Check if navigate was called with the correct path
    expect(mockNavigate).toHaveBeenCalledWith('/executive/record-deposit');
  });

  it('navigates to record expense page when expense button is clicked', () => {
    render(<CashBalance />);
    
    // Find and click the Record Expense button
    const expenseButton = screen.getByText('Record Expense');
    fireEvent.click(expenseButton);
    
    // Check if navigate was called with the correct path
    expect(mockNavigate).toHaveBeenCalledWith('/executive/record-expense');
  });

  it('displays transaction details when a transaction is clicked', async () => {
    render(<CashBalance />);
    
    // Find and click a transaction in the list
    const transactions = screen.getAllByRole('row');
    // Skip the header row
    if (transactions.length > 1) {
      fireEvent.click(transactions[1]);
      
      // Check if transaction details dialog is displayed
      await waitFor(() => {
        expect(screen.getByText('Transaction Details')).toBeInTheDocument();
      });
    }
  });

  it('closes transaction details dialog when close button is clicked', async () => {
    render(<CashBalance />);
    
    // Find and click a transaction in the list
    const transactions = screen.getAllByRole('row');
    // Skip the header row
    if (transactions.length > 1) {
      fireEvent.click(transactions[1]);
      
      // Wait for dialog to appear
      await waitFor(() => {
        expect(screen.getByText('Transaction Details')).toBeInTheDocument();
      });
      
      // Find and click the close button
      const closeButton = screen.getByText('Close');
      fireEvent.click(closeButton);
      
      // Check if dialog is closed
      await waitFor(() => {
        expect(screen.queryByText('Transaction Details')).not.toBeInTheDocument();
      });
    }
  });

  it('displays cash flow chart', () => {
    render(<CashBalance />);
    
    // Check if the cash flow chart is rendered
    expect(screen.getByText('Cash Flow')).toBeInTheDocument();
  });

  it('displays transaction breakdown by type', () => {
    render(<CashBalance />);
    
    // Check if the transaction breakdown section is rendered
    expect(screen.getByText('Transaction Breakdown')).toBeInTheDocument();
  });
});