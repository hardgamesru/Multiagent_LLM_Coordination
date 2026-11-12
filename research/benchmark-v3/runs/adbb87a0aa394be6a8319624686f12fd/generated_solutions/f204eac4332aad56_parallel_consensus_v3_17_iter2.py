def transaction_trace(operations):
    state = {}
    reads = []
    snapshots = []
    
    def apply_op(op):
        nonlocal state, reads
        if op[0] == 'set':
            state[op[1]] = op[2]
        elif op[0] == 'get':
            reads.append(state.get(op[1]))
        elif op[0] == 'begin':
            snapshots.append(dict(state))
        elif op[0] == 'commit':
            if not snapshots:
                raise ValueError("Commit outside of transaction")
            state = snapshots.pop()
        elif op[0] == 'rollback':
            if not snapshots:
                return
            # Rollback to previous snapshot
            state = snapshots[-1]
            # If there's another outer transaction, undo its commits too
            while snapshots and len(snapshots[-1]) != len(state):
                snapshots.pop()
    
    for op in operations:
        try:
            apply_op(op)
        except KeyError:
            # Missing delete operation is ignored
            pass
    
    return {"state": state, "reads": reads}
