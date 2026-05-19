def calculate_cart_total(items: list[dict], promo_code: str | None = None) -> float:
    if any(item['price'] < 0 or item['quantity'] <= 0 for item in items):
        raise ValueError("Invalid item data")
    
    subtotal = sum(item['price'] * item['quantity'] for item in items)
    
    if promo_code == "SALE10":
        return round(subtotal * 0.9, 2)
    elif promo_code == "FOOD5":
        food_items_subtotal = sum(
            item['price'] * item['quantity'] 
            for item in items 
            if item['category'].lower() == 'food'
        )
        discounted_food_subtotal = food_items_subtotal * 0.95
        non_food_subtotal = subtotal - food_items_subtotal
        return round(discounted_food_subtotal + non_food_subtotal, 2)
    else:
        return round(subtotal, 2)
