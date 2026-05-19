def calculate_cart_total(items: list[dict], promo_code: str | None = None) -> float:
    def validate_item(item):
        if item['price'] < 0 or item['quantity'] <= 0:
            raise ValueError("Invalid item data.")
    
    subtotal = sum(item['price'] * item['quantity'] for item in items)
    
    # Validate all items before proceeding
    for item in items:
        validate_item(item)
        
    if promo_code == 'SALE10':
        return round(subtotal * 0.9, 2)
    elif promo_code == 'FOOD5':
        discounted_food_items_subtotal = sum(
            item['price'] * item['quantity'] 
            for item in items 
            if item.get('category', '').lower() == 'food'
        )
        return round((subtotal - discounted_food_items_subtotal + discounted_food_items_subtotal * 0.95), 2)
    else:
        return round(subtotal, 2)
