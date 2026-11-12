def aggregate_orders(customers: list[dict], orders: list[dict]) -> list[dict]:
    if not isinstance(customers, list) or not isinstance(orders, list):
        raise TypeError("Both arguments must be lists")
    
    customer_ids = set(c['id'] for c in customers)
    
    result = [{ 'id': cid, 'total': 0 } for cid in customer_ids]
    
    for order in orders:
        try:
            customer_id = order['customer']
            amount_cents = int(order['amount'])
            
            if customer_id not in customer_ids:
                raise ValueError(f"Unknown customer: {customer_id}")
                
            if amount_cents < 0:
                raise ValueError("Negative amount is not allowed")
        
            # Find corresponding customer record
            target = next(x for x in result if x['id'] == customer_id)
            target['total'] += amount_cents
        
        except KeyError as e:
            raise ValueError(f"Missing key in order: {e}") from None
    
    return result
