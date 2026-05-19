def calculate_cart_total(items: list[dict], promo_code: str | None = None) -> float:
    total = 0.0
    for item in items:
        price = item.get('price', -1)
        quantity = item.get('quantity', -1)
        
        # Validate item data
        if price < 0 or quantity <= 0:
            raise ValueError("Invalid item data")
            
        total += price * quantity
    
    # Apply promos
    if promo_code == 'SALE10':
        total *= 0.9
    elif promo_code == 'FOOD5':
        food_total = sum(item['price'] * item['quantity'] 
                         for item in items if item['category'].lower() == 'food')
        total -= (food_total * 0.05)
    
    return round(total, 2)
