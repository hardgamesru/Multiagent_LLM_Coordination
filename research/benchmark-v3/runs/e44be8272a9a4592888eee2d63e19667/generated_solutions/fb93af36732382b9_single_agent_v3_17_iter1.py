def transaction_trace(operations):
    state = {}
    reads = []
    snapshots = []
    
    def apply_op(op):
        if op[0] == 'set':
            state[op[1]] = int(op[2])
        elif op[0] == 'delete':
            state.pop(op[1], None)
        elif op[0] == 'get':
            reads.append(state.get(op[1]))
    
    for op in operations:
        if op == ['begin']:
            snapshots.append(dict(state))
        elif op == ['commit']:
            if not snapshots:
                raise ValueError("Commit outside of transaction")
            state = snapshots.pop()
        elif op == ['rollback']:
            if not snapshots:
                raise ValueError("Rollback outside of transaction")
            # Restore state but keep committed changes
            state.update(snapshots[-1])
            snapshots.pop()
        else:
            try:
                apply_op(op)
            except KeyError:
                pass  # Missing operation is ignored
    
    if snapshots:
        raise ValueError("Open transactions at end")
    
    return {'state': state, 'reads': reads}
