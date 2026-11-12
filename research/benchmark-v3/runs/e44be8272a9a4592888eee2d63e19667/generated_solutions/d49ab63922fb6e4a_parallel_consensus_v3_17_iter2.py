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
        if len(snapshots) == 0 and op[:2] != ["begin"]:
            # Non-transactional read
            reads.append(None)
            continue
            
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
                raise ValueError("Commit outside of transaction")
            state = snapshots.pop()
        elif cmd == "rollback":
            if not snapshots:
                raise ValueError("Rollback outside of transaction")
            # Restore previous state
            state = snapshots.pop()
            # Rollback committed changes if outer rollback
            if snapshots:
                state.update(snapshots[-1])
                
    return {"state": state, "reads": reads}
