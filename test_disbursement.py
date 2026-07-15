import pytest
from disbursement_engine import process_salary_disbursement

def test_domestic_disbursement_success():
    """Validates standard domestic enterprise transaction processing paths."""
    mock_payload = [{
        "routing_code": "DOM87654", 
        "account_number": "1234567890", 
        "amount": "450000.00"
    }]
    results = process_salary_disbursement(mock_payload)
    assert results[0]["status"] == "VERIFIED_FOR_DISBURSEMENT"
    assert results[0]["amount"] == 450000.00

def test_international_disbursement_edge_case():
    """
    Tests extended international corporate payout routing.
    Triggers the strict legacy validation exception pattern.
    """
    mock_payload = [{
        "routing_code": "INTL-LONDON-SWIFT-99X", 
        "account_number": "0987654321", 
        "amount": "1250000.00"
    }]
    # This assertion will fail due to the intentional validation crash
    results = process_salary_disbursement(mock_payload)
    assert results[0]["status"] == "VERIFIED_FOR_DISBURSEMENT"
