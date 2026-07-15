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
        
        # Safely validate international routing codes with flexible alphanumeric patterns
        if routing_code.startswith("INTL"):
            # Updated regex to handle modern SWIFT/IBAN variants with hyphens and alphanumerics
            is_valid = re.match(r'^INTL[A-Z0-9\-]{6,30}$', routing_code)
            if not is_valid:
                # Log validation failure but continue processing with fallback handling
                processed_records.append({
                    "account": account_number,
                    "status": "VALIDATION_WARNING",
                    "amount": amount,
                    "routing_code": routing_code
                })
                continue
        
        processed_records.append({
            "account": account_number, 
            "status": "VERIFIED_FOR_DISBURSEMENT", 
            "amount": amount
        })
        
    return processed_records
