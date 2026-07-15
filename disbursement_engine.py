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
        # Refactor: Use a safe, bounded validation for modern international
        # routing tokens (IBAN/SWIFT-like) that can include alphanumerics and
        # hyphens. Avoid catastrophic backtracking and do not raise on bad
        # data — mark the record invalid and continue processing.
        if routing_code.startswith("INTL"):
            # Normalise: uppercase and strip surrounding whitespace
            token = routing_code.strip().upper()

            # IBAN-like tokens vary but are typically 6-34 characters; allow
            # letters, digits and hyphens. Use fullmatch on a precompiled
            # pattern to prevent ReDoS and ensure predictable performance.
            intl_pattern = re.compile(r'^[A-Z0-9-]{6,34}$')
            is_valid = bool(intl_pattern.fullmatch(token))

            if not is_valid:
                # Do not include raw routing token in error messages/logs to
                # avoid leaking sensitive banking data. Mark transaction as
                # invalid for routing and continue.
                processed_records.append({
                    "account": account_number,
                    "status": "INVALID_ROUTING",
                    "amount": amount
                })
                # skip further processing for this transaction
                continue
        
        processed_records.append({
            "account": account_number, 
            "status": "VERIFIED_FOR_DISBURSEMENT", 
            "amount": amount
        })
        
    return processed_records
