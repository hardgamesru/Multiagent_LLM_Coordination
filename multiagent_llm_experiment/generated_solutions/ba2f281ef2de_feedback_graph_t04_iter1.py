def calculate_cart_total(items: list[dict], promo_code: str | None = None) -> float:
    def validate_item(item):
        if item['price'] < 0:
            raise ValueError("Price cannot be negative")
        if item['quantity'] <= 0:
            raise ValueError("Quantity must be positive")
    
    subtotal = 0
    for item in items:
        validate_item(item)
        subtotal += item['price'] * item['quantity']
    
    if promo_code == 'SALE10':
        return round(subtotal * 0.9, 2)
    elif promo_code == 'FOOD5':
        discounted_food_items = [item for item in items if item['category'].lower() == 'food']
        food_subtotal = sum(item['price'] * item['quantity'] for item in discounted_food_items)
        return round((subtotal - food_subtotal + food_subtotal * 0.95), 2)
    else:
        return round(subtotal, 2)
