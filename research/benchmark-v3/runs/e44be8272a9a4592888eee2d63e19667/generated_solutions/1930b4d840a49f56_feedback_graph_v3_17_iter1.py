def transaction_trace(operations: list[list]) -> dict:
    state = {}
    reads = []
    snapshots = []

    for op in operations:
        cmd = op[0]
        if cmd == "set":
            key, val = op[1], op[2]
            if snapshots:
                if key not in snapshots[-1]:
                    snapshots[-1][key] = state.get(key, None)
            state[key] = val
        elif cmd == "delete":
            key = op[1]
            if snapshots:
                if key not in snapshots[-1]:
                    snapshots[-1][key] = state.get(key, None)
            state.pop(key, None)
        elif cmd == "get":
            key = op[1]
            reads.append(state.get(key, None))
        elif cmd == "begin":
            snapshots.append({})
        elif cmd == "commit":
            if not snapshots:
                raise ValueError
            snapshots.pop()
        elif cmd == "rollback":
            if not snapshots:
                raise ValueError
            snap = snapshots.pop()
            for k, v in snap.items():
                if v is None:
                    state.pop(k, None)
                else:
                    state[k] = v
        else:
            raise ValueError

    if snapshots:
        raise ValueError

    return {"state": state, "reads": reads}
