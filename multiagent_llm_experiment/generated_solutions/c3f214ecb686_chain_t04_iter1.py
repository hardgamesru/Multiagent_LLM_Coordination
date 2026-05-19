def calculate_cart_total(items: list[dict], promo_code: str | None = None) -> float:
    if not items:
        return 0.0
    
    total = sum(item['price'] * item['quantity'] for item in items)
    
    if promo_code == 'SALE10':
        total *= 0.9
    elif promo_code == 'FOOD5':
        food_items = [item for item in items if item.get('category', '') == 'food']
        food_total = sum(item['price'] * item['quantity'] for item in food_items)
        total -= food_total * 0.05
    
    return round(total, 2)
