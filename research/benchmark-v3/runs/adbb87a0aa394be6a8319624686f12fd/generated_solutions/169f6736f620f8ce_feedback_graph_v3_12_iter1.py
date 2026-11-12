def aggregate_orders(customers: list[dict], orders: list[dict]) -> list[dict]:
    # Создаем словарь для хранения суммы заказов каждого клиента
    result = {c['id']: 0 for c in customers}
    
    # Проверяем каждый заказ
    for order in orders:
        # Получаем ID клиента из заказа
        customer_id = order.get('customer')
        
        # Проверка наличия и валидности ID клиента
        if customer_id is None or customer_id not in result:
            raise ValueError(f"Unknown customer '{customer_id}'")
            
        # Получаем сумму заказа
        amount = order.get('amount')
        
        # Проверка валидности суммы
        if amount is None or amount < 0:
            raise ValueError(f"Invalid amount {amount}")
            
        # Добавляем сумму к общей сумме клиента
        result[customer_id] += amount
    
    # Формируем результат в нужном формате
    return [{"id": k, "total": v} for k, v in result.items()]
