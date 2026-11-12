def transaction_trace(operations):
    state = {}
    reads = []
    snapshots = []
    
    def apply_set(key, value):
        nonlocal state
        state[key] = value
        
    def apply_delete(key):
        nonlocal state
        state.pop(key, None)
        
    def begin():
        if snapshots:
            raise ValueError("Begin inside an active transaction")
        snapshots.append(dict(state))
            
    def commit():
        if not snapshots:
            raise ValueError("Commit outside of a transaction")
        state = snapshots.pop()
        
    def rollback():
        if not snapshots:
            raise ValueError("Rollback outside of a transaction")
        # Сохраняем текущее чтение перед восстановлением состояния
        reads.append(state.get(read_key, None))
        state = snapshots.pop()
        
    for op in operations:
        try:
            cmd, *params = op
            if cmd == "set":
                apply_set(params[0], int(params[1]))
            elif cmd == "delete":
                apply_delete(params[0])
            elif cmd == "get":
                read_key = params[0]
                # Читаем значение только при первой команде get в транзакции
                if not snapshots:
                    reads.append(state.get(read_key, None))
                else:
                    reads.append(None)
            elif cmd == "begin":
                begin()
            elif cmd == "commit":
                commit()
            elif cmd == "rollback":
                rollback()
        except KeyError:
            pass  # Пропускаем отсутствующие команды
    
    return {"state": state, "reads": reads}
