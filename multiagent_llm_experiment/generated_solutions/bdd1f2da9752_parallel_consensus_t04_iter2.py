def calculate_cart_total(items: list[dict], promo_code: str | None = None) -> float:
    def validate_item(item):
        if item['price'] < 0:
            raise ValueError("Item price cannot be negative")
        if item['quantity'] <= 0:
            raise ValueError("Item quantity must be positive")
    
    subtotal = 0
    # Validate input items and compute subtotal
    for item in items:
        validate_item(item)
        subtotal += item['price'] * item['quantity']
        
    # Apply promotions
    if promo_code == 'SALE10':
        return round(subtotal * 0.9, 2)
    elif promo_code == 'FOOD5':
        food_discount = sum(
            item['price'] * item['quantity'] * 0.05 
            for item in items if item['category'].lower() == 'food'
        )
        return round(subtotal - food_discount, 2)
    else:
        return round(subtotal, 2)
