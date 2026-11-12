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
        
    def apply_delete(key):
        nonlocal state
        state.pop(key, None)
        
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
                    raise ValueError("No active transaction")
                    
            elif cmd == "get":
                reads.append(state.get(params[0]))
                
            elif cmd == "set":
                apply_set(*params)
                
            elif cmd == "delete":
                apply_delete(*params)
                
        except IndexError:
            # Skip invalid commands with wrong number of parameters
            pass
    
    if snapshots:
        raise ValueError("Open transactions at end")
    
    return {"state": dict(state), "reads": reads}
