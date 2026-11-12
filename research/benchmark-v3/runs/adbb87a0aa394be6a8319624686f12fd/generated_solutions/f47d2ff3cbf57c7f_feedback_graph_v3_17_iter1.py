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
        
    def apply_get(key):
        nonlocal reads
        reads.append(state.get(key))
    
    def apply_begin():
        snapshots.append(dict(state))
    
    def apply_commit():
        if not snapshots:
            raise ValueError("No active transaction to commit")
        state = snapshots.pop()
    
    def apply_rollback():
        if not snapshots:
            raise ValueError("No active transaction to roll back")
        prev_state = snapshots[-1]
        # Restore previous state but keep reads from current transaction
        state.update(prev_state)
        # Remove read values from current transaction
        reads[:] = []
    
    commands_map = {
        "set": apply_set,
        "delete": apply_delete,
        "get": apply_get,
        "begin": apply_begin,
        "commit": apply_commit,
        "rollback": apply_rollback
    }
    
    for op in operations:
        cmd = op[0]
        try:
            func = commands_map[cmd]
        except KeyError:
            raise ValueError(f"Invalid command: {cmd}")
            
        # Check for valid transaction context before applying command
        if cmd in ("commit", "rollback"):
            if not snapshots:
                raise ValueError(f"{cmd} called outside of transaction")
                
        func(*op[1:])
    
    return {"state": state, "reads": reads}
