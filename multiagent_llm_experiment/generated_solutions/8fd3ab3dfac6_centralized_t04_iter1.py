def calculate_cart_total(items: list[dict], promo_code: str | None = None) -> float:
    total = 0.0
    food_total = 0.0
    for item in items:
        if "price" not in item or "quantity" not in item or "category" not in item:
            raise ValueError("item must contain price, quantity, and category")
        price = item["price"]
        quantity = item["quantity"]
        category = item["category"]
        if price < 0 or quantity <= 0:
            raise ValueError("invalid price or quantity")
        line_total = price * quantity
        total += line_total
        if category == "food":
            food_total += line_total
    if promo_code == "SALE10":
        total *= 0.9
    elif promo_code == "FOOD5":
        total -= food_total * 0.05
    return round(total, 2)
