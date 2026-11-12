def transaction_trace(operations: list[list]) -> dict:
    state = {}
    reads = []
    snapshots = []

    def get_value(k):
        for snap in reversed(snapshots):
            if k in snap:
                return snap[k]
        return state.get(k, None)

    for op in operations:
        cmd = op[0]
        if cmd == "set":
            _, k, v = op
            if snapshots:
                snapshots[-1][k] = v
            else:
                state[k] = v
        elif cmd == "delete":
            _, k = op
            if snapshots:
                snapshots[-1][k] = None
            else:
                state.pop(k, None)
        elif cmd == "get":
            _, k = op
            reads.append(get_value(k))
        elif cmd == "begin":
            snapshots.append({})
        elif cmd == "commit":
            if not snapshots:
                raise ValueError("No transaction to commit")
            changes = snapshots.pop()
            if snapshots:
                snapshots[-1].update(changes)
            else:
                for k, v in changes.items():
                    if v is None:
                        state.pop(k, None)
                    else:
                        state[k] = v
        elif cmd == "rollback":
            if not snapshots:
                raise ValueError("No transaction to rollback")
            snapshots.pop()

    if snapshots:
        raise ValueError("Uncommitted transactions remain")

    return {"state": state, "reads": reads}
