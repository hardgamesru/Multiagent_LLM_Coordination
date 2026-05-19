def calculate_cart_total(items: list[dict], promo_code: str | None = None) -> float:
    if not items:
        return 0.0
    total = sum(item['price'] * item['quantity'] for item in items)
    if promo_code == 'SALE10':
        total *= 0.9
    elif promo_code == 'FOOD5' and any(item.get('category', '') == 'food' for item in items):
        total *= 0.95
    if total < 0:
        raise ValueError("Invalid item data")
    return round(total, 2)
