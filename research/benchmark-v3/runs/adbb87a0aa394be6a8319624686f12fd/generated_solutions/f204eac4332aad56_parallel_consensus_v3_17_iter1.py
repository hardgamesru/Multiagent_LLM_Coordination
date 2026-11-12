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
        snapshots.append(dict(state))
    
    def commit():
        if not snapshots:
            raise ValueError("No active transaction")
        # Remove last snapshot but keep its changes
        state.update(snapshots.pop())
    
    def rollback():
        if not snapshots:
            return
        # Restore previous state, undoing committed changes
        state = snapshots[-1].copy()
    
    commands = {
        "set": lambda k,v: apply_set(k,v),
        "delete": lambda k: apply_delete(k),
        "get": lambda k: reads.append(state.get(k)),
        "begin": begin,
        "commit": commit,
        "rollback": rollback
    }
    
    for op in operations:
        cmd = op[0]
        try:
            fn = commands[cmd]
        except KeyError:
            continue
        args = op[1:] if len(op)>1 else []
        fn(*args)
    
    return {"state": state, "reads": reads}
