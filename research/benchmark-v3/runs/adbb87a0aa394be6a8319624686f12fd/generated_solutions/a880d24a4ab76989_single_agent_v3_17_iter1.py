def transaction_trace(operations: list[list]) -> dict:
    state = {}
    reads = []
    snapshots = []

    for op in operations:
        cmd = op[0]
        if cmd == "set":
            key, val = op[1], op[2]
            if snapshots:
                snapshots[-1].setdefault(key, state.get(key, None))
            state[key] = val
        elif cmd == "delete":
            key = op[1]
            if snapshots:
                snapshots[-1].setdefault(key, state.get(key, None))
            if key in state:
                del state[key]
        elif cmd == "get":
            key = op[1]
            reads.append(state.get(key, None))
        elif cmd == "begin":
            snapshots.append({})
        elif cmd == "commit":
            if not snapshots:
                raise ValueError
            changes = snapshots.pop()
            for k, v in changes.items():
                if v is None and k in state:
                    del state[k]
                elif v is not None:
                    state[k] = v
        elif cmd == "rollback":
            if not snapshots:
                raise ValueError
            changes = snapshots.pop()
            for k, v in changes.items():
                if v is None:
                    state.pop(k, None)
                else:
                    state[k] = v

    if snapshots:
        raise ValueError
    return {"state": state, "reads": reads}
