def aggregate_orders(customers: list[dict], orders: list[dict]) -> list[dict]:
    customer_set = set(d['id'] for d in customers)
    
    result = {}
    for order in orders:
        if order['customer'] not in customer_set:
            raise ValueError("Unknown customer")
        
        if order['amount'] < 0:
            raise ValueError("Negative amount")
            
        result[order['customer']] = result.get(order['customer'], 0) + order['amount']
    
    # Add missing customers with total=0
    for cust_id in customer_set:
        if cust_id not in result:
            result[cust_id] = 0
    
    return [{"id": k, "total": v} for k, v in result.items()]
