def aggregate_orders(customers: list[dict], orders: list[dict]) -> list[dict]:
    customer_set = set(customer['id'] for customer in customers)
    
    result = {}
    
    for order in orders:
        if order['customer'] not in customer_set:
            raise ValueError("Unknown customer")
        
        if order['amount'] < 0:
            raise ValueError("Negative amount")
            
        result.setdefault(order['customer'], 0)
        result[order['customer']] += order['amount']
    
    # Add missing customers with total=0
    for customer_id in customer_set:
        if customer_id not in result:
            result[customer_id] = 0
    
    return [{"id": k, "total": v} for k, v in result.items()]
