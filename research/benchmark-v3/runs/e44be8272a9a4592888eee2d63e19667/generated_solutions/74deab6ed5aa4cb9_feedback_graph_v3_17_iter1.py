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
        
    def apply_get(key):
        nonlocal reads
        reads.append(state.get(key))
        
    def start_snapshot():
        snapshots.append(dict(state))
    
    def commit():
        if not snapshots:
            raise ValueError("No active transaction")
        state = snapshots.pop()
    
    def rollback():
        if not snapshots:
            raise ValueError("No active transaction")
        prev_state = snapshots.pop()
        # Restore previous state but keep reads from current one
        for k, v in state.items():
            if k not in prev_state:
                del state[k]
            else:
                state[k] = prev_state[k]
    
    commands_map = {
        "set": apply_set,
        "delete": apply_delete,
        "get": apply_get,
        "begin": start_snapshot,
        "commit": commit,
        "rollback": rollback
    }
    
    for op in operations:
        try:
            cmd, *params = op
            func = commands_map.get(cmd)
            if func:
                func(*params)
        except Exception:
            pass  # Invalid command ignored
    
    return {"state": state, "reads": reads}
