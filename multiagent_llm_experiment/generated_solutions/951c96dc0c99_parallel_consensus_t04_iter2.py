def calculate_cart_total(items: list[dict], promo_code: str | None = None) -> float:
    def validate_item(item):
        if item['price'] < 0:
            raise ValueError("Price cannot be negative")
        if item['quantity'] <= 0:
            raise ValueError("Quantity must be positive")
    
    subtotal = sum((item['price'] * item['quantity']) for item in items)
    if len(items) == 0:
        return round(subtotal, 2)
        
    # Validate all items first before applying any promotions
    for item in items:
        validate_item(item)
    
    if promo_code == 'SALE10':
        discounted_subtotal = subtotal - (subtotal * 0.1)
    elif promo_code == 'FOOD5':
        food_items_total = sum((item['price'] * item['quantity']) 
                               for item in items if item.get('category', '') == 'food')
        discounted_food_total = food_items_total - (food_items_total * 0.05)
        other_items_total = subtotal - food_items_total
        discounted_subtotal = other_items_total + discounted_food_total
    else:
        discounted_subtotal = subtotal
    
    return round(discounted_subtotal, 2)
