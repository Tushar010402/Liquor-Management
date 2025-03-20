import React from 'react';
import { render, screen, fireEvent, waitFor } from '../../../test-utils';
import DailySummary from '../../../../pages/executive/Cash/DailySummary';

// Mock navigate function
const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));

// Mock window.alert
jest.spyOn(window, 'alert').mockImplementation(() => {});

describe('DailySummary', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders daily summary information correctly', () => {
    render(<DailySummary />);
    
    // Check if the page title is rendered
    expect(screen.getByText('Daily Summary')).toBeInTheDocument();
    
    // Check if the date picker is rendered
    expect(screen.getByLabelText('Select Date')).toBeInTheDocument();
    
    // Check if summary sections are rendered
    expect(screen.getByText('Total Sales')).toBeInTheDocument();
    expect(screen.getByText('Cash Sales')).toBeInTheDocument();
    expect(screen.getByText('UPI Sales')).toBeInTheDocument();
    expect(screen.getByText('Card Sales')).toBeInTheDocument();
    
    // Check if charts are rendered
    expect(screen.getByText('Sales by Hour')).toBeInTheDocument();
    expect(screen.getByText('Payment Methods')).toBeInTheDocument();
    
    // Check if tables are rendered
    expect(screen.getByText('Top Selling Items')).toBeInTheDocument();
    expect(screen.getByText('Cash Summary')).toBeInTheDocument();
    expect(screen.getByText('Transactions')).toBeInTheDocument();
    expect(screen.getByText('Stock Adjustments')).toBeInTheDocument();
  });

  it('opens print dialog when print button is clicked', async () => {
    render(<DailySummary />);
    
    // Find and click the Print button
    const printButton = screen.getByRole('button', { name: /Print/i });
    fireEvent.click(printButton);
    
    // Check if print dialog is displayed
    await waitFor(() => {
      expect(screen.getByText('Print Daily Summary')).toBeInTheDocument();
    });
  });

  it('closes print dialog when cancel button is clicked', async () => {
    render(<DailySummary />);
    
    // Open print dialog
    const printButton = screen.getByRole('button', { name: /Print/i });
    fireEvent.click(printButton);
    
    // Wait for dialog to appear
    await waitFor(() => {
      expect(screen.getByText('Print Daily Summary')).toBeInTheDocument();
    });
    
    // Find and click the Cancel button
    const cancelButton = screen.getByRole('button', { name: /Cancel/i });
    fireEvent.click(cancelButton);
    
    // Check if dialog is closed
    await waitFor(() => {
      expect(screen.queryByText('Print Daily Summary')).not.toBeInTheDocument();
    });
  });

  it('prints summary when print button in dialog is clicked', async () => {
    render(<DailySummary />);
    
    // Open print dialog
    const printButton = screen.getByRole('button', { name: /Print/i });
    fireEvent.click(printButton);
    
    // Wait for dialog to appear
    await waitFor(() => {
      expect(screen.getByText('Print Daily Summary')).toBeInTheDocument();
    });
    
    // Find and click the Print Summary button
    const printSummaryButton = screen.getByRole('button', { name: /Print Summary/i });
    fireEvent.click(printSummaryButton);
    
    // Check if alert is shown
    expect(window.alert).toHaveBeenCalledWith('Summary sent to printer!');
    
    // Check if dialog is closed
    await waitFor(() => {
      expect(screen.queryByText('Print Daily Summary')).not.toBeInTheDocument();
    });
  });

  it('updates data when date is changed', async () => {
    render(<DailySummary />);
    
    // Find the date picker
    const datePicker = screen.getByLabelText('Select Date');
    
    // Change the date
    // Note: This is a simplified test as the actual date picker interaction is complex
    // In a real test, we would use a more sophisticated approach to interact with the date picker
    fireEvent.change(datePicker, { target: { value: '2023-11-24' } });
    
    // In a real app, this would trigger an API call to fetch data for the selected date
    // For this test, we're just checking that the component doesn't crash
    expect(screen.getByText('Daily Summary')).toBeInTheDocument();
  });

  it('displays transaction details in the transactions table', () => {
    render(<DailySummary />);
    
    // Check if the transactions table is rendered with data
    expect(screen.getByText('Transactions')).toBeInTheDocument();
    
    // Check for transaction types
    expect(screen.getAllByText('Sale').length).toBeGreaterThan(0);
    expect(screen.getAllByText('Expense').length).toBeGreaterThan(0);
    expect(screen.getAllByText('Deposit').length).toBeGreaterThan(0);
  });

  it('displays stock adjustments in the stock adjustments table', () => {
    render(<DailySummary />);
    
    // Check if the stock adjustments table is rendered
    expect(screen.getByText('Stock Adjustments')).toBeInTheDocument();
    
    // Check for adjustment types
    expect(screen.getByText('Increase')).toBeInTheDocument();
    expect(screen.getByText('Decrease')).toBeInTheDocument();
  });
});