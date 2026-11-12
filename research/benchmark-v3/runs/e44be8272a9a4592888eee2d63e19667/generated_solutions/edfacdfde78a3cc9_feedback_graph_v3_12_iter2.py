def aggregate_orders(customers: list[dict], orders: list[dict]) -> list[dict]:
    # Создаем словарь для хранения итоговой суммы заказов каждого клиента
    result = {c["id"]: 0 for c in customers}
    
    # Проверяем наличие неизвестных клиентов в заказах
    unknown_customers = set(order.get("customer") for order in orders if order.get("customer") not in result)
    if unknown_customers:
        raise ValueError(f"Unknown customers: {unknown_customers}")
    
    # Обрабатываем каждый заказ
    for order in orders:
        customer_id = order.get("customer")
        
        # Проверяем валидность клиента и отрицательные суммы
        if customer_id not in result or order.get("amount") is None or order["amount"] < 0:
            raise ValueError(f"Invalid order for customer '{customer_id}'")
            
        # Добавляем сумму заказа к общей сумме клиента
        result[customer_id] += order["amount"]
    
    # Формируем результат в нужном формате
    return [{"id": k, "total": v} for k, v in result.items()]
