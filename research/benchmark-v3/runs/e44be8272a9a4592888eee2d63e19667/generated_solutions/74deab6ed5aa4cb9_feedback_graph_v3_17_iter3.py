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
        if len(snapshots) > 0:
            # Create a new snapshot when needed
            if op[0] == 'begin':
                snapshots.append(dict(state))
            elif op[0] == 'commit':
                # Remove last snapshot and keep changes
                snapshots.pop()
            elif op[0] == 'rollback':
                # Restore previous snapshot
                if len(snapshots) > 0:
                    state = snapshots[-1]
                else:
                    raise ValueError("No active transaction to roll back")
                
        try:
            if op[0] == 'set':
                apply_set(op[1], int(op[2]))
            elif op[0] == 'get':
                # Store read values
                reads.append(state.get(op[1], None))
            elif op[0] == 'delete':
                apply_delete(op[1])
        except IndexError:
            # Skip invalid commands
            pass
            
    # Check for unclosed transactions
    if len(snapshots) != 0:
        raise ValueError("Uncommitted transactions detected")
    
    return {"state": state, "reads": reads}
