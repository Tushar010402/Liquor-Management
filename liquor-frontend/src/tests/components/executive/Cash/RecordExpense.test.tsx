import React from 'react';
import { render, screen, fireEvent, waitFor } from '../../../test-utils';
import RecordExpense from '../../../../pages/executive/Cash/RecordExpense';

// Mock navigate function
const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));

describe('RecordExpense', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    // Mock window.alert
    jest.spyOn(window, 'alert').mockImplementation(() => {});
  });

  it('renders expense form correctly', () => {
    render(<RecordExpense />);
    
    // Check if the page title is rendered
    expect(screen.getByText('Record Expense')).toBeInTheDocument();
    
    // Check if form fields are rendered
    expect(screen.getByLabelText(/Amount/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Expense Category/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Paid To/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Notes/i)).toBeInTheDocument();
  });

  it('shows validation errors for empty required fields', async () => {
    render(<RecordExpense />);
    
    // Submit the form without filling in required fields
    const nextButton = screen.getByRole('button', { name: /Next/i });
    fireEvent.click(nextButton);
    
    // Check for validation errors
    await waitFor(() => {
      expect(screen.getByText(/Amount is required/i)).toBeInTheDocument();
      expect(screen.getByText(/Category is required/i)).toBeInTheDocument();
      expect(screen.getByText(/Recipient name is required/i)).toBeInTheDocument();
    });
  });

  it('shows validation error for invalid amount', async () => {
    render(<RecordExpense />);
    
    // Enter an invalid amount (negative)
    const amountInput = screen.getByLabelText(/Amount/i);
    fireEvent.change(amountInput, { target: { value: '-100' } });
    
    // Fill other required fields
    const categorySelect = screen.getByLabelText(/Expense Category/i);
    fireEvent.mouseDown(categorySelect);
    const categoryOptions = screen.getAllByRole('option');
    fireEvent.click(categoryOptions[0]);
    
    const paidToInput = screen.getByLabelText(/Paid To/i);
    fireEvent.change(paidToInput, { target: { value: 'Supplier Name' } });
    
    // Submit the form
    const nextButton = screen.getByRole('button', { name: /Next/i });
    fireEvent.click(nextButton);
    
    // Check for validation error
    await waitFor(() => {
      expect(screen.getByText(/Amount must be positive/i)).toBeInTheDocument();
    });
  });

  it('proceeds through form steps when valid data is entered', async () => {
    render(<RecordExpense />);
    
    // Step 1: Fill in expense details
    const amountInput = screen.getByLabelText(/Amount/i);
    fireEvent.change(amountInput, { target: { value: '500' } });
    
    const categorySelect = screen.getByLabelText(/Expense Category/i);
    fireEvent.mouseDown(categorySelect);
    const categoryOptions = screen.getAllByRole('option');
    fireEvent.click(categoryOptions[0]);
    
    const paidToInput = screen.getByLabelText(/Paid To/i);
    fireEvent.change(paidToInput, { target: { value: 'Supplier Name' } });
    
    const notesInput = screen.getByLabelText(/Notes/i);
    fireEvent.change(notesInput, { target: { value: 'Monthly utility payment' } });
    
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
      expect(screen.getByText(/Review Expense Details/i)).toBeInTheDocument();
    });
    
    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: /Submit for Approval/i }));
    
    // Check if confirmation dialog is shown
    await waitFor(() => {
      expect(screen.getByText(/Confirm Expense Submission/i)).toBeInTheDocument();
    });
    
    // Confirm submission
    fireEvent.click(screen.getByRole('button', { name: /Confirm/i }));
    
    // Check if alert is shown and navigation occurs
    expect(window.alert).toHaveBeenCalled();
    expect(mockNavigate).toHaveBeenCalledWith('/executive/cash-balance');
  });

  it('allows navigation back to previous steps', async () => {
    render(<RecordExpense />);
    
    // Fill in required fields for step 1
    const amountInput = screen.getByLabelText(/Amount/i);
    fireEvent.change(amountInput, { target: { value: '500' } });
    
    const categorySelect = screen.getByLabelText(/Expense Category/i);
    fireEvent.mouseDown(categorySelect);
    const categoryOptions = screen.getAllByRole('option');
    fireEvent.click(categoryOptions[0]);
    
    const paidToInput = screen.getByLabelText(/Paid To/i);
    fireEvent.change(paidToInput, { target: { value: 'Supplier Name' } });
    
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
      expect(screen.getByLabelText(/Expense Category/i)).toBeInTheDocument();
    });
  });

  it('cancels confirmation dialog when Cancel button is clicked', async () => {
    render(<RecordExpense />);
    
    // Fill in required fields for step 1
    const amountInput = screen.getByLabelText(/Amount/i);
    fireEvent.change(amountInput, { target: { value: '500' } });
    
    const categorySelect = screen.getByLabelText(/Expense Category/i);
    fireEvent.mouseDown(categorySelect);
    const categoryOptions = screen.getAllByRole('option');
    fireEvent.click(categoryOptions[0]);
    
    const paidToInput = screen.getByLabelText(/Paid To/i);
    fireEvent.change(paidToInput, { target: { value: 'Supplier Name' } });
    
    // Move through steps
    fireEvent.click(screen.getByRole('button', { name: /Next/i }));
    await waitFor(() => {
      expect(screen.getByText(/Upload Receipt/i)).toBeInTheDocument();
    });
    
    fireEvent.click(screen.getByRole('button', { name: /Next/i }));
    await waitFor(() => {
      expect(screen.getByText(/Review Expense Details/i)).toBeInTheDocument();
    });
    
    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: /Submit for Approval/i }));
    
    // Check if confirmation dialog is shown
    await waitFor(() => {
      expect(screen.getByText(/Confirm Expense Submission/i)).toBeInTheDocument();
    });
    
    // Click Cancel button
    fireEvent.click(screen.getByRole('button', { name: /Cancel/i }));
    
    // Check if dialog is closed
    await waitFor(() => {
      expect(screen.queryByText(/Confirm Expense Submission/i)).not.toBeInTheDocument();
    });
  });
});