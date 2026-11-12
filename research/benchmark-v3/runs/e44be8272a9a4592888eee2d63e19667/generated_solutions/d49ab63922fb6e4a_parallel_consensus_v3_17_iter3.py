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
        if len(snapshots) == 0 and op[:2] != ["begin", ""]:
            # Read outside of transaction
            reads.append(None)
        elif op == ["begin"]:
            snapshots.append(dict(state))
        elif op == ["commit"]:
            if not snapshots:
                raise ValueError("Commit without begin")
            state = snapshots.pop()
        elif op == ["rollback"]:
            if not snapshots:
                raise ValueError("Rollback without begin")
            state = snapshots.pop()
        elif op[:2] == ["set", ""]:
            apply_set(op[2], int(op[3]))
        elif op[:2] == ["delete", ""]:
            apply_delete(op[1])
        elif op[:2] == ["get", ""]:
            reads.append(state.get(op[1], None))
            
    return {"state": state, "reads": reads}
