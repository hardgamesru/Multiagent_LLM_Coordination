def aggregate_orders(customers: list[dict], orders: list[dict]) -> list[dict]:
    if len({c['id'] for c in customers}) != len(customers):
        raise ValueError("Duplicate customer IDs")
    
    result = {c['id']: 0 for c in customers}
    
    for order in orders:
        customer_id = order.get('customer')
        
        if customer_id is None:
            continue
            
        amount = order.get('amount')
        
        if amount is None or amount < 0:
            raise ValueError("Negative or missing order amount")
            
        if customer_id not in result:
            raise ValueError(f"Unknown customer '{customer_id}'")
            
        result[customer_id] += amount
    
    return [{"id": k, "total": v} for k, v in result.items()]
