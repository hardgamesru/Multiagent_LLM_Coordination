def calculate_cart_total(items: list[dict], promo_code: str | None = None) -> float:
    if any(item.get('price', 0) < 0 or item.get('quantity', 0) <= 0 for item in items):
        raise ValueError("Invalid item data")
    
    subtotal = sum(item['price'] * item['quantity'] for item in items)
    
    # Apply discounts based on promo code
    if promo_code == "SALE10":
        discount = subtotal * 0.10
    elif promo_code == "FOOD5":
        food_items_subtotal = sum(
            item['price'] * item['quantity'] 
            for item in items 
            if item.get('category') == 'food'
        )
        discount = food_items_subtotal * 0.05
    else:
        discount = 0
        
    return round(subtotal - discount, 2)
