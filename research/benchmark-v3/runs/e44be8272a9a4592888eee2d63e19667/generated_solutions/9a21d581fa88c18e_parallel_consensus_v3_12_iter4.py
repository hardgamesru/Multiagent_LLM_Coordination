def aggregate_orders(customers: list[dict], orders: list[dict]) -> list[dict]:
    if len(set(c["id"] for c in customers)) != len(customers):
        raise ValueError("Duplicate customer IDs")
    
    result = {c["id"]: 0 for c in customers}
    
    for order in orders:
        customer_id = order.get("customer")
        amount = order.get("amount")
        
        if customer_id is None or amount is None or amount < 0:
            raise ValueError("Invalid order data")
        
        if customer_id not in result:
            raise ValueError(f"Unknown customer '{customer_id}'")
        
        result[customer_id] += amount
    
    return [{"id": k, "total": v} for k, v in result.items()]
