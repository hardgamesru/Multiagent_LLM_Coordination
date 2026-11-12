from collections import defaultdict

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
        nonlocal snapshots
        snapshots.append(dict(state))
        
    def commit():
        nonlocal snapshots, state
        if not snapshots:
            raise ValueError("No active transaction")
        state = snapshots.pop()
            
    def rollback():
        nonlocal snapshots, state
        if not snapshots:
            return
        # Restore previous state even if it was committed
        state = snapshots[-1]
        
    commands = {
        "set": lambda k,v: apply_set(k, v),
        "delete": apply_delete,
        "get": lambda k: reads.append(state.get(k)),
        "begin": begin,
        "commit": commit,
        "rollback": rollback
    }
    
    for op in operations:
        cmd = op[0]
        args = op[1:]
        try:
            commands[cmd](*args)
        except KeyError:
            pass  # Missing command is ignored
    
    # Ensure all transactions closed properly
    if snapshots:
        raise ValueError("Uncommitted transactions exist")
    
    return {"state": state, "reads": reads}
