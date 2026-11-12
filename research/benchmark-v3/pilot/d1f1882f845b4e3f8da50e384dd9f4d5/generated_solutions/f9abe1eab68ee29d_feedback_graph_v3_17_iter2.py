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
        # Remove last snapshot but keep its changes
        state.update(snapshots.pop())
    
    def rollback():
        if not snapshots:
            raise ValueError("Rollback outside of a transaction")
        # Restore previous state
        state = snapshots[-1].copy()
    
    commands = {
        "set": lambda k,v: apply_set(k,v),
        "delete": apply_delete,
        "get": lambda k: (reads.append(state.get(k)), state.get(k)),
        "begin": begin,
        "commit": commit,
        "rollback": rollback
    }
    
    for op in operations:
        cmd = op[0]
        params = op[1:]
        try:
            commands[cmd](*params)
        except KeyError:
            pass  # Missing command is ignored
    
    return {"state": state, "reads": reads}
