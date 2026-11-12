from collections import defaultdict

def transaction_trace(operations):
    if not operations:
        return {"state": {}, "reads": []}
    
    state = defaultdict(int)
    reads = []
    snapshots = []
    
    def apply_set(key, value):
        nonlocal state
        state[key] = value
        
    for op in operations:
        try:
            cmd, *params = op
            
            if cmd == "begin":
                snapshots.append(dict(state))
                
            elif cmd == "commit" and snapshots:
                state = snapshots.pop()
                
            elif cmd == "rollback":
                if snapshots:
                    state = snapshots.pop()
                else:
                    raise ValueError("No active transaction to roll back")
                    
            elif cmd == "get":
                reads.append(state.get(params[0]))
                
            elif cmd == "set":
                apply_set(*params)
                
            elif cmd == "delete":
                key = params[0]
                state.pop(key, None)
                
        except Exception as e:
            # Пропускаем недопустимые операции
            continue
    
    return {"state": dict(state), "reads": reads}
