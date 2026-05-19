def calculate_cart_total(items: list[dict], promo_code: str | None = None) -> float:
    if not all('price' in i and 'quantity' in i and 'category' in i for i in items):
        raise ValueError("Invalid item data")
    
    total_price = sum(i['price'] * i['quantity'] for i in items)
    
    if promo_code == 'SALE10':
        total_price *= 0.9
    elif promo_code == 'FOOD5':
        food_items = [i for i in items if i['category'] == 'food']
        food_total = sum(i['price'] * i['quantity'] for i in food_items)
        total_price -= food_total * 0.05
    
    return round(total_price, 2)
