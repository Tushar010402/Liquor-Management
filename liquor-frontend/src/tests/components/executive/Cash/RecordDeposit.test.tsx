import React from 'react';
import { render, screen, fireEvent, waitFor } from '../../../test-utils';
import RecordDeposit from '../../../../pages/executive/Cash/RecordDeposit';

// Mock navigate function
const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));

describe('RecordDeposit', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    // Mock window.alert
    jest.spyOn(window, 'alert').mockImplementation(() => {});
  });

  it('renders deposit form correctly', () => {
    render(<RecordDeposit />);
    
    // Check if the page title is rendered
    expect(screen.getByText('Record Bank Deposit')).toBeInTheDocument();
    
    // Check if form fields are rendered
    expect(screen.getByLabelText(/Amount/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Bank Account/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Reference Number/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Notes/i)).toBeInTheDocument();
  });

  it('shows validation errors for empty required fields', async () => {
    render(<RecordDeposit />);
    
    // Submit the form without filling in required fields
    const submitButton = screen.getByRole('button', { name: /Submit for Approval/i });
    fireEvent.click(submitButton);
    
    // Check for validation errors
    await waitFor(() => {
      expect(screen.getByText(/Amount is required/i)).toBeInTheDocument();
      expect(screen.getByText(/Bank account is required/i)).toBeInTheDocument();
    });
  });

  it('shows validation error for invalid amount', async () => {
    render(<RecordDeposit />);
    
    // Enter an invalid amount (negative)
    const amountInput = screen.getByLabelText(/Amount/i);
    fireEvent.change(amountInput, { target: { value: '-100' } });
    
    // Submit the form
    const submitButton = screen.getByRole('button', { name: /Submit for Approval/i });
    fireEvent.click(submitButton);
    
    // Check for validation error
    await waitFor(() => {
      expect(screen.getByText(/Amount must be positive/i)).toBeInTheDocument();
    });
  });

  it('proceeds through form steps when valid data is entered', async () => {
    render(<RecordDeposit />);
    
    // Step 1: Fill in deposit details
    const amountInput = screen.getByLabelText(/Amount/i);
    fireEvent.change(amountInput, { target: { value: '5000' } });
    
    const bankAccountSelect = screen.getByLabelText(/Bank Account/i);
    fireEvent.mouseDown(bankAccountSelect);
    
    // Select a bank account option
    const bankOptions = screen.getAllByRole('option');
    fireEvent.click(bankOptions[0]);
    
    const referenceInput = screen.getByLabelText(/Reference Number/i);
    fireEvent.change(referenceInput, { target: { value: 'DEP-12345' } });
    
    // Click Next button
    const nextButton = screen.getByRole('button', { name: /Next/i });
    fireEvent.click(nextButton);
    
    // Check if moved to step 2 (Upload Receipt)
    await waitFor(() => {
      expect(screen.getByText(/Upload Receipt/i)).toBeInTheDocument();
    });
    
    // Click Next button again to move to step 3
    fireEvent.click(screen.getByRole('button', { name: /Next/i }));
    
    // Check if moved to step 3 (Review)
    await waitFor(() => {
      expect(screen.getByText(/Review Deposit Details/i)).toBeInTheDocument();
    });
    
    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: /Submit for Approval/i }));
    
    // Check if confirmation dialog is shown
    await waitFor(() => {
      expect(screen.getByText(/Confirm Deposit Submission/i)).toBeInTheDocument();
    });
    
    // Confirm submission
    fireEvent.click(screen.getByRole('button', { name: /Confirm/i }));
    
    // Check if alert is shown and navigation occurs
    expect(window.alert).toHaveBeenCalled();
    expect(mockNavigate).toHaveBeenCalledWith('/executive/cash-balance');
  });

  it('allows navigation back to previous steps', async () => {
    render(<RecordDeposit />);
    
    // Fill in required fields for step 1
    const amountInput = screen.getByLabelText(/Amount/i);
    fireEvent.change(amountInput, { target: { value: '5000' } });
    
    const bankAccountSelect = screen.getByLabelText(/Bank Account/i);
    fireEvent.mouseDown(bankAccountSelect);
    
    // Select a bank account option
    const bankOptions = screen.getAllByRole('option');
    fireEvent.click(bankOptions[0]);
    
    // Move to step 2
    fireEvent.click(screen.getByRole('button', { name: /Next/i }));
    
    // Check if moved to step 2
    await waitFor(() => {
      expect(screen.getByText(/Upload Receipt/i)).toBeInTheDocument();
    });
    
    // Click Back button
    fireEvent.click(screen.getByRole('button', { name: /Back/i }));
    
    // Check if returned to step 1
    await waitFor(() => {
      expect(screen.getByLabelText(/Amount/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/Bank Account/i)).toBeInTheDocument();
    });
  });

  it('cancels confirmation dialog when Cancel button is clicked', async () => {
    render(<RecordDeposit />);
    
    // Fill in required fields for step 1
    const amountInput = screen.getByLabelText(/Amount/i);
    fireEvent.change(amountInput, { target: { value: '5000' } });
    
    const bankAccountSelect = screen.getByLabelText(/Bank Account/i);
    fireEvent.mouseDown(bankAccountSelect);
    
    // Select a bank account option
    const bankOptions = screen.getAllByRole('option');
    fireEvent.click(bankOptions[0]);
    
    // Move through steps
    fireEvent.click(screen.getByRole('button', { name: /Next/i }));
    await waitFor(() => {
      expect(screen.getByText(/Upload Receipt/i)).toBeInTheDocument();
    });
    
    fireEvent.click(screen.getByRole('button', { name: /Next/i }));
    await waitFor(() => {
      expect(screen.getByText(/Review Deposit Details/i)).toBeInTheDocument();
    });
    
    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: /Submit for Approval/i }));
    
    // Check if confirmation dialog is shown
    await waitFor(() => {
      expect(screen.getByText(/Confirm Deposit Submission/i)).toBeInTheDocument();
    });
    
    // Click Cancel button
    fireEvent.click(screen.getByRole('button', { name: /Cancel/i }));
    
    // Check if dialog is closed
    await waitFor(() => {
      expect(screen.queryByText(/Confirm Deposit Submission/i)).not.toBeInTheDocument();
    });
  });
});