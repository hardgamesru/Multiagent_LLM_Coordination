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
        
    for op in operations:
        if len(snapshots) == 0 and op[0] in ("begin", "commit", "rollback"):
            raise ValueError("Invalid operation outside of transaction")
            
        if op[0] == "set":
            apply_set(op[1], int(op[2]))
        elif op[0] == "delete":
            apply_delete(op[1])
        elif op[0] == "get":
            reads.append(state.get(op[1], None))
        elif op[0] == "begin":
            snapshots.append(dict(state))
        elif op[0] == "commit":
            if not snapshots:
                continue
            state = snapshots.pop()
        elif op[0] == "rollback":
            if not snapshots:
                continue
            state = snapshots[-1]
        else:
            # ignore unknown commands
            pass
    
    return {"state": state, "reads": reads}
