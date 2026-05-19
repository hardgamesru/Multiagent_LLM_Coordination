def calculate_cart_total(items: list[dict], promo_code: str | None = None) -> float:
    total_cost = 0.0
    
    # Validate input items
    for item in items:
        if 'price' not in item or 'quantity' not in item or 'category' not in item:
            raise ValueError("Item is missing necessary fields")
        
        price = item['price']
        quantity = item['quantity']
        
        if price < 0:
            raise ValueError(f"Invalid price {price} for item {item}")
            
        if quantity <= 0:
            raise ValueError(f"Invalid quantity {quantity} for item {item}")
            
        total_cost += price * quantity
    
    # Apply promotions
    if promo_code == 'SALE10':
        total_cost *= 0.9  # 10% discount
    elif promo_code == 'FOOD5':
        discounted_food_cost = sum(item['price'] * item['quantity'] 
                                   for item in items if item['category'].lower() == 'food')
        total_cost -= discounted_food_cost * 0.05  # 5% discount on food items
    
    return round(total_cost, 2)
