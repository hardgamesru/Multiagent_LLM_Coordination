def transaction_trace(operations):
    state = {}
    reads = []
    snapshots = []
    
    def apply_command(cmd):
        nonlocal state, reads
        if cmd == ['begin']:
            snapshots.append(dict(state))
        elif cmd == ['commit']:
            if not snapshots:
                raise ValueError('No active transaction')
            # Сохраняем текущее состояние
            state = snapshots.pop()
        elif cmd == ['rollback']:
            if not snapshots:
                raise ValueError('No active transaction')
            # Восстанавливаем предыдущее состояние
            state = snapshots.pop()
        else:
            k, v = cmd[1], cmd[2]
            if cmd[0] == 'set':
                state[k] = v
            elif cmd[0] == 'get':
                reads.append(state.get(k, None))
            elif cmd[0] == 'delete':
                state.pop(k, None)
    
    for op in operations:
        try:
            apply_command(op)
        except Exception:
            # Пропускаем недопустимые команды
            continue
    
    return {"state": state, "reads": reads}
