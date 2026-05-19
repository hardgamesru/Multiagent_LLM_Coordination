def calculate_cart_total(items: list[dict], promo_code: str | None = None) -> float:
    if any(item.get('price', 0) < 0 or item.get('quantity', 0) <= 0 for item in items):
        raise ValueError("Invalid item data")
    
    subtotal = sum(item['price'] * item['quantity'] for item in items)
    
    # Apply promo code discounts
    if promo_code == "SALE10":
        discounted_subtotal = subtotal * 0.9
    elif promo_code == "FOOD5":
        food_items_cost = sum(
            item['price'] * item['quantity'] 
            for item in items 
            if item.get('category') == 'food'
        )
        non_food_items_cost = subtotal - food_items_cost
        discounted_subtotal = (food_items_cost * 0.95) + non_food_items_cost
    else:
        discounted_subtotal = subtotal
        
    return round(discounted_subtotal, 2)
