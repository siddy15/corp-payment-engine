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
        
        # INTENTIONAL BUG / AUDIT BLOCK:
        # Legacy regex engine fails to safely parse modern international SWIFT/IBAN variants.
        # This causes parsing failures or processing time-outs under production volumes.
        if routing_code.startswith("INTL"):
            # Flawed strict format verification pattern
            is_valid = re.match(r'^[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}$', routing_code)
            if not is_valid:
                raise ValueError(
                    f"CRITICAL PLATFORM FAULT: Invalid routing token '{routing_code}'. "
                    f"Execution aborted to safeguard corporate fund delivery."
                )
        
        processed_records.append({
            "account": account_number, 
            "status": "VERIFIED_FOR_DISBURSEMENT", 
            "amount": amount
        })
        
    return processed_records
