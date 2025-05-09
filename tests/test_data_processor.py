import pytest
from datetime import datetime
from src.data_processor import InvoiceDataProcessor

@pytest.fixture
def processor():
    return InvoiceDataProcessor()

@pytest.fixture
def sample_invoices():
    return [
        {
            "invoice_id": 454,
            "invoice_number": "4006",
            "invoice_date": "2025-03-03",
            "balance_due": "496.00",
            "due_by": 8
        },
        {
            "invoice_id": 461,
            "invoice_number": "104640",
            "invoice_date": "2025-03-13",
            "balance_due": "10400.00",
            "due_by": 18
        },
        {
            "invoice_id": 467,
            "invoice_number": "105008",
            "invoice_date": "2025-03-20",
            "balance_due": "2000.00",
            "due_by": 25
        }
    ]

def test_calculate_total_balance(processor, sample_invoices):
    total = processor.calculate_total_balance(sample_invoices)
    assert total == 12896.00  # 496.00 + 10400.00 + 2000.00

def test_format_date(processor):
    date_str = "2025-03-03"
    formatted = processor.format_date(date_str)
    assert formatted == "03/03/2025"

def test_get_current_date(processor):
    current_date = processor.get_current_date()
    # Verify format
    datetime.strptime(current_date, "%d/%m/%Y")
    # Verify it's today's date
    today = datetime.now().strftime("%d/%m/%Y")
    assert current_date == today

def test_get_row_class(processor):
    assert processor.get_row_class(35) == "row-red"
    assert processor.get_row_class(20) == "row-yellow"
    assert processor.get_row_class(10) == "row-green"

def test_process_invoices(processor, sample_invoices):
    result = processor.process_invoices(sample_invoices)
    
    # Check total balance
    assert result['total_balance'] == "₹ 12,896.00"
    
    # Check current date format
    datetime.strptime(result['current_date'], "%d/%m/%Y")
    
    # Check invoice rows
    assert len(result['invoices']) == 3
    
    # Check first invoice
    first_invoice = result['invoices'][0]
    assert first_invoice['date'] == "03/03/2025"
    assert first_invoice['number'] == "4006"
    assert first_invoice['amount'] == "₹ 496.00"
    assert first_invoice['due_by'] == "8 days"
    assert first_invoice['class'] == "row-green"

def test_process_invoices_empty_list(processor):
    result = processor.process_invoices([])
    assert result['total_balance'] == "₹ 0.00"
    assert len(result['invoices']) == 0

def test_process_invoices_invalid_data(processor):
    invalid_invoices = [
        {
            "invoice_id": 454,
            "invoice_number": "4006",
            "invoice_date": "invalid-date",
            "balance_due": "invalid-amount",
            "due_by": "invalid-days"
        }
    ]
    
    with pytest.raises(Exception):
        processor.process_invoices(invalid_invoices) 