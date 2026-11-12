def calculate_cart_total(items: list[dict], promo_code: str | None = None) -> float:
    if not all('price' in i and 'quantity' in i and 'category' in i for i in items):
        raise ValueError("Invalid item data")
    
    total = sum(i['price'] * i['quantity'] for i in items)
    
    if promo_code == 'SALE10':
        total *= 0.9
    elif promo_code == 'FOOD5':
        food_total = sum(i['price'] * i['quantity'] for i in items if i['category'] == 'food')
        total -= food_total * 0.05
    
    return round(total, 2)
