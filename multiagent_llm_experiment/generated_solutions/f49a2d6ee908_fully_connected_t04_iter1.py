def calculate_cart_total(items: list[dict], promo_code: str | None = None) -> float:
    if not all('price' in i and 'quantity' in i and 'category' in i for i in items):
        raise ValueError("Invalid item data")
    
    total = sum(item['price'] * item['quantity'] for item in items)
    
    if promo_code == 'SALE10':
        total *= 0.9
    elif promo_code == 'FOOD5':
        food_items = [item for item in items if item['category'] == 'food']
        food_total = sum(item['price'] * item['quantity'] for item in food_items)
        total -= food_total * 0.05
    
    return round(total, 2)
