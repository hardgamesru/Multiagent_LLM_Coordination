def aggregate_orders(customers: list[dict], orders: list[dict]) -> list[dict]:
    if not all('id' in c for c in customers):
        raise ValueError("Each customer must have an 'id'")
    
    customer_ids = set(c['id'] for c in customers)
    
    result = [{ 'id': c['id'], 'total': 0 } for c in customers]
    
    for order in orders:
        if 'customer' not in order or 'amount' not in order:
            continue
        
        if order['customer'] not in customer_ids or order['amount'] < 0:
            raise ValueError(f"Invalid customer '{order['customer']}' or negative amount")
        
        # Find corresponding customer record
        found = next((r for r in result if r['id'] == order['customer']), None)
        if found is None:
            raise ValueError(f"Unknown customer '{order['customer']}'")
            
        found['total'] += order['amount']
    
    return result
