def transaction_trace(operations):
    if len(operations) > 500:
        raise ValueError("Maximum operation limit exceeded")
    
    state = {}
    reads = []
    snapshots = []
    
    def apply_set(key, value):
        nonlocal state
        state[key] = value
        
    def apply_delete(key):
        nonlocal state
        state.pop(key, None)
    
    for op in operations:
        try:
            cmd = op[0]
            
            if cmd == "set":
                apply_set(op[1], int(op[2]))
                
            elif cmd == "delete":
                apply_delete(op[1])
                
            elif cmd == "get":
                reads.append(state.get(op[1], None))
                
            elif cmd == "begin":
                snapshots.append(dict(state))
                
            elif cmd == "commit":
                if not snapshots:
                    raise ValueError("Commit outside of active transaction")
                state = snapshots.pop()
                
            elif cmd == "rollback":
                if not snapshots:
                    raise ValueError("Rollback outside of active transaction")
                # Сохраняем текущее состояние перед откатом
                prev_state = dict(state)
                state = snapshots.pop()
                # Откатываемся назад, восстанавливая предыдущее состояние
                state.update(prev_state)
                
            else:
                raise ValueError(f"Unknown command: {cmd}")
                
        except IndexError:
            raise ValueError(f"Invalid number of arguments for command: {op}")
    
    return {"state": state, "reads": reads}
