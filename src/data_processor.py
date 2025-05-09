from datetime import datetime
from typing import List, Dict, Any
from loguru import logger

class InvoiceDataProcessor:
    def __init__(self):
        """Initialize the invoice data processor."""
        logger.info("Invoice Data Processor initialized")

    def calculate_total_balance(self, invoices: List[Dict[str, Any]]) -> float:
        """
        Calculate total balance from all invoices.
        
        Args:
            invoices (List[Dict]): List of invoice dictionaries
            
        Returns:
            float: Total balance due
        """
        try:
            total = sum(float(invoice['balance_due']) for invoice in invoices)
            logger.info(f"Calculated total balance: {total}")
            return total
        except Exception as e:
            logger.error(f"Error calculating total balance: {str(e)}")
            raise

    def format_date(self, date_str: str) -> str:
        """
        Format date string to DD/MM/YYYY format.
        
        Args:
            date_str (str): Date string in any format
            
        Returns:
            str: Formatted date string
        """
        try:
            # Parse the date string
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            # Format to DD/MM/YYYY
            formatted_date = date_obj.strftime("%d/%m/%Y")
            return formatted_date
        except Exception as e:
            logger.error(f"Error formatting date {date_str}: {str(e)}")
            raise

    def get_current_date(self) -> str:
        """
        Get current date in DD/MM/YYYY format.
        
        Returns:
            str: Current date string
        """
        return datetime.now().strftime("%d/%m/%Y")

    def get_row_class(self, due_by: int) -> str:
        """
        Determine CSS class for table row based on due_by days.
        
        Args:
            due_by (int): Number of days until due
            
        Returns:
            str: CSS class name
        """
        if due_by > 30:
            return "row-red"
        elif due_by > 15:
            return "row-yellow"
        else:
            return "row-green"

    def process_invoices(self, invoices: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process invoice data and prepare template data.
        
        Args:
            invoices (List[Dict]): List of invoice dictionaries
            
        Returns:
            Dict: Processed data for template
        """
        try:
            logger.info("Processing invoice data")
            
            # Calculate total balance
            total_balance = self.calculate_total_balance(invoices)
            
            # Get current date
            current_date = self.get_current_date()
            
            # Process invoice rows
            invoice_rows = []
            for invoice in invoices:
                row = {
                    'date': self.format_date(invoice['invoice_date']),
                    'number': invoice['invoice_number'],
                    'amount': f"₹ {float(invoice['balance_due']):,.2f}",
                    'due_by': f"{invoice['due_by']} days",
                    'class': self.get_row_class(invoice['due_by'])
                }
                invoice_rows.append(row)
            
            # Prepare template data
            template_data = {
                'total_balance': f"₹ {total_balance:,.2f}",
                'current_date': current_date,
                'invoices': invoice_rows
            }
            
            logger.info("Invoice data processing completed")
            return template_data
            
        except Exception as e:
            logger.error(f"Error processing invoice data: {str(e)}")
            raise 