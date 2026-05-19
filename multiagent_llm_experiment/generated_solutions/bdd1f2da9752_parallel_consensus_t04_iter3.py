def calculate_cart_total(items: list[dict], promo_code: str | None = None) -> float:
    def validate_item(item):
        if item['price'] < 0:
            raise ValueError("Item price cannot be negative")
        if item['quantity'] <= 0:
            raise ValueError("Item quantity must be positive")
    
    # Validate all items first
    for item in items:
        validate_item(item)
        
    subtotal = sum(item['price'] * item['quantity'] for item in items)
    
    if promo_code == 'SALE10':
        return round(subtotal * 0.9, 2)
    elif promo_code == 'FOOD5':
        discounted_food_items = [item for item in items if item['category'].lower() == 'food']
        food_discount = sum(item['price'] * item['quantity'] for item in discounted_food_items) * 0.05
        return round(subtotal - food_discount, 2)
    else:
        return round(subtotal, 2)
