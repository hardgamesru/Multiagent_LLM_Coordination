def calculate_cart_total(items: list[dict], promo_code: str | None = None) -> float:  
   total = 0.0  
   for item in items:  
      if 'price' not in item or 'quantity' not in item or 'category' not in item:  
         raise ValueError("Invalid item data")  
      if item['price'] < 0 or item['quantity'] <= 0:  
         raise ValueError("Invalid item data")  
      total += item['price'] * item['quantity']  
   
   if promo_code == 'SALE10':  
      total *= 0.9  
   elif promo_code == 'FOOD5':  
      food_total = sum(i['price']*i['quantity'] for i in items if i['category']=='food')  
      total -= food_total * 0.05  
   
   return round(total, 2)
