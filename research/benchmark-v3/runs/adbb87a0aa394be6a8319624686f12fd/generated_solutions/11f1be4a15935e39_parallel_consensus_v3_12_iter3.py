def aggregate_orders(customers: list[dict], orders: list[dict]) -> list[dict]:
    customer_map = {c['id']: 0 for c in customers}
    
    for order in orders:
        if order['customer'] not in customer_map:
            raise ValueError(f"Unknown customer: {order['customer']}")
        
        if order['amount'] < 0:
            raise ValueError("Negative amount")
            
        customer_map[order['customer']] += order['amount']
    
    # Add missing customers with total=0
    result = [{**{"id": cid}, **{"total": total}} for cid, total in customer_map.items()]
    
    return result
