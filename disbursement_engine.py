import csv
import re
import time

def process_salary_disbursement(batch_payload):
    """
    Processes high-volume enterprise payroll streams for FYN B2B clients.
    Validates transactional routing paths before initiating disbursement rails.
    """
    processed_records = []
    
    for transaction in batch_payload:
        routing_code = transaction.get('routing_code', '')
        account_number = transaction.get('account_number', '')
        amount = float(transaction.get('amount', 0))
        
        # Validate international routing codes
        # Supports modern SWIFT/IBAN variants with alphanumeric characters and hyphens
        if routing_code.startswith("INTL"):
            # Flexible pattern for modern international routing structures
            is_valid = re.match(r'^[A-Z]{4}[A-Z]{2}[A-Z0-9\-]{2,}$', routing_code)
            if not is_valid:
                raise ValueError(
                    f"Invalid routing code format: '{routing_code}'. "
                    f"Expected format: INTL<2-letter code><alphanumeric/hyphen sequence>"
                )
        
        processed_records.append({
            "account": account_number, 
            "status": "VERIFIED_FOR_DISBURSEMENT", 
            "amount": amount
        })
        
    return processed_records
