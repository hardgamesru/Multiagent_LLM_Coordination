def calculate_cart_total(items: list[dict], promo_code: str | None = None) -> float:
    total = 0.0
    food_total = 0.0
    for item in items:
        price = item.get('price')
        quantity = item.get('quantity')
        category = item.get('category')
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError('Invalid price')
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError('Invalid quantity')
        if not isinstance(category, str):
            raise ValueError('Invalid category')
        line_total = price * quantity
        total += line_total
        if category.lower() == 'food':
            food_total += line_total
    if promo_code == 'SALE10':
        total *= 0.9
    elif promo_code == 'FOOD5':
        total -= food_total * 0.05
    return round(total, 2)
