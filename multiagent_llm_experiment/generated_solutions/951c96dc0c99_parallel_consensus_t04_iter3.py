def calculate_cart_total(items: list[dict], promo_code: str | None = None) -> float:
    def validate_item(item):
        if item['price'] < 0:
            raise ValueError("Price cannot be negative")
        if item['quantity'] <= 0:
            raise ValueError("Quantity must be positive")
    
    subtotal = sum(item['price'] * item['quantity'] for item in items)
    
    # Validate all items first before applying any promotions
    for item in items:
        validate_item(item)
        
    # Apply promotional discounts
    if promo_code == 'SALE10':
        return round(subtotal * 0.9, 2)
    elif promo_code == 'FOOD5':
        discounted_food_subtotal = sum(
            (item['price'] * item['quantity']) * 0.95 
            if item['category'].lower() == 'food' else 
            item['price'] * item['quantity']
            for item in items
        )
        return round(discounted_food_subtotal, 2)
    else:
        return round(subtotal, 2)
