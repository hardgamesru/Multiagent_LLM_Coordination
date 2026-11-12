def transaction_trace(operations):
    state = {}
    reads = []
    snapshots = []
    
    def apply_op(op):
        nonlocal state, reads
        if op[0] == 'set':
            state[op[1]] = int(op[2])
        elif op[0] == 'get':
            reads.append(state.get(op[1]))
        elif op[0] == 'begin':
            snapshots.append(dict(state))
        elif op[0] == 'commit':
            if not snapshots:
                raise ValueError("No active transaction")
            state = snapshots.pop()
        elif op[0] == 'rollback':
            if not snapshots:
                return
            # Сохранить текущие чтения перед откатом
            reads.extend(state.get(k) for k in state)
            # Откатываемся к предыдущему состоянию
            state = snapshots.pop()
            
    for op in operations:
        try:
            apply_op(op)
        except KeyError:
            # Пропускаем команды с отсутствующими ключами
            pass
    
    return {"state": state, "reads": reads}
