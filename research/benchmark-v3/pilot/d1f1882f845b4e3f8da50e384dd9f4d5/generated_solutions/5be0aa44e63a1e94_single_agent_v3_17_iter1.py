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
        snapshots.append(dict(state))
    
    def commit():
        if not snapshots:
            raise ValueError("No active transaction")
        state = snapshots.pop()
    
    def rollback():
        if not snapshots:
            return
        # Restore previous state even if it was committed
        state = snapshots[-1]
    
    commands = {
        "set": lambda k,v: apply_set(k,v),
        "delete": apply_delete,
        "get": lambda k: reads.append(state.get(k)),
        "begin": begin,
        "commit": commit,
        "rollback": rollback
    }
    
    for op in operations:
        cmd, *args = op
        try:
            commands[cmd](*args)
        except KeyError:
            pass  # Missing command is ignored
    
    return {"state": state, "reads": reads}
