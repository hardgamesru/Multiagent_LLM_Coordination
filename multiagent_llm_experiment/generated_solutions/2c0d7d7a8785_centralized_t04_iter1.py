def calculate_cart_total(items: list[dict], promo_code: str | None = None) -> float:
    if any(item.get('price', 0) < 0 or item.get('quantity', 0) <= 0 for item in items):
        raise ValueError("Invalid item data")
    
    subtotal = sum(item['price'] * item['quantity'] for item in items)
    
    if promo_code == "SALE10":
        final_total = subtotal * 0.9
    elif promo_code == "FOOD5":
        food_subtotal = sum(item['price'] * item['quantity'] for item in items if item['category'] == 'food')
        final_total = subtotal - (food_subtotal * 0.05)
    else:
        final_total = subtotal
    
    return round(final_total, 2)
