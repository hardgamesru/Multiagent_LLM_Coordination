def calculate_cart_total(items: list[dict], promo_code: str | None = None) -> float:
    total = 0.0
    
    for item in items:
        try:
            price = float(item.get('price', 0))
            quantity = int(item.get('quantity', 0))
            
            if price < 0 or quantity <= 0:
                raise ValueError("Invalid item data")
                
            total += price * quantity
        
        except (KeyError, ValueError):
            raise ValueError("Invalid item data")
    
    if promo_code == 'SALE10':
        total *= 0.9
    elif promo_code == 'FOOD5':
        discounted_food_items = [item for item in items if item.get('category') == 'food']
        food_total = sum(float(item.get('price')) * int(item.get('quantity')) for item in discounted_food_items)
        total -= food_total * 0.05
    
    return round(total, 2)
