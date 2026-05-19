def calculate_cart_total(items: list[dict], promo_code: str | None = None) -> float:
    # Validate input items
    for item in items:
        if item['price'] < 0:
            raise ValueError("Item price cannot be negative")
        if item['quantity'] <= 0:
            raise ValueError("Item quantity must be positive")
    
    # Calculate initial subtotal
    subtotal = sum(item['price'] * item['quantity'] for item in items)
    
    # Apply discounts based on promo code
    if promo_code == 'SALE10':
        discounted_subtotal = subtotal * 0.9  # 10% off everything
    elif promo_code == 'FOOD5':
        # Only apply 5% discount to food items
        food_discount = sum(
            item['price'] * item['quantity'] * 0.05 
            for item in items if item['category'].lower() == 'food'
        )
        discounted_subtotal = subtotal - food_discount
    else:
        discounted_subtotal = subtotal  # No discount applied
        
    return round(discounted_subtotal, 2)
