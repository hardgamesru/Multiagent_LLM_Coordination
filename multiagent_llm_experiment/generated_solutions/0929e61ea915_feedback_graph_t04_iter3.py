def calculate_cart_total(items: list[dict], promo_code: str | None = None) -> float:
    if not items:
        return 0.0
    total = 0.0
    for item in items:
        try:
            price = float(item['price'])
            quantity = int(item['quantity'])
            category = item.get('category')
            if price < 0 or quantity <= 0:
                raise ValueError
            total += price * quantity
        except (KeyError, TypeError, ValueError):
            raise ValueError("Invalid item data")
    
    if promo_code == 'SALE10':
        total *= 0.9
    elif promo_code == 'FOOD5' and any(category == 'food' for item in items):
        total *= 0.95
    
    return round(total, 2)
