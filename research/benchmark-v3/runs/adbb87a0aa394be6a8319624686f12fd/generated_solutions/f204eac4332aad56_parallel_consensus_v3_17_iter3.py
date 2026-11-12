def transaction_trace(operations):
    state = {}
    reads = []
    snapshots = []
    
    def apply_op(op):
        if op[0] == 'set':
            state[op[1]] = op[2]
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
            # Rollback reads from last get operation
            if reads:
                reads.pop()
            state = snapshots.pop()
        else:
            apply_op(op)
            
    return {"state": state, "reads": reads}
