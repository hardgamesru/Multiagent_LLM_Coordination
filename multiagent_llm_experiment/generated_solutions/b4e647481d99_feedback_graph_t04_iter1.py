def calculate_cart_total(items: list[dict], promo_code: str | None = None) -> float:
    if not all('price' in i and 'quantity' in i and 'category' in i for i in items):
        raise ValueError("Each item must contain 'price', 'quantity', and 'category'")
    
    # Validate prices and quantities
    for item in items:
        if item['price'] < 0:
            raise ValueError(f"Price {item['price']} is negative")
        if item['quantity'] <= 0:
            raise ValueError(f"Quantity {item['quantity']} is not positive")
    
    subtotal = sum(item['price'] * item['quantity'] for item in items)
    
    # Apply discount if valid promo code exists
    if promo_code == 'SALE10':
        return round(subtotal * 0.9, 2)
    elif promo_code == 'FOOD5':
        discounted_food_items = [i for i in items if i['category'].lower() == 'food']
        food_subtotal = sum(i['price'] * i['quantity'] for i in discounted_food_items)
        discount_amount = food_subtotal * 0.05
        return round(subtotal - discount_amount, 2)
    else:
        return round(subtotal, 2)
