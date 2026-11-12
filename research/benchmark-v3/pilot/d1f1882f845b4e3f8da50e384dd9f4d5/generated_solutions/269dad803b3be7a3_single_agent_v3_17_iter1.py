def transaction_trace(operations: list[list]) -> dict:
    state = {}
    reads = []
    snapshots = []

    for op in operations:
        cmd = op[0]
        if cmd == "set":
            key, val = op[1], op[2]
            if snapshots:
                snapshots[-1].setdefault("writes", {})[key] = state.get(key, None)
            state[key] = val
        elif cmd == "delete":
            key = op[1]
            if key in state:
                if snapshots:
                    snapshots[-1].setdefault("writes", {})[key] = state.get(key, None)
                del state[key]
        elif cmd == "get":
            key = op[1]
            reads.append(state.get(key, None))
        elif cmd == "begin":
            snapshots.append({})
        elif cmd == "rollback":
            if not snapshots:
                raise ValueError
            snap = snapshots.pop()
            writes = snap.get("writes", {})
            for k, v in writes.items():
                if v is None:
                    state.pop(k, None)
                else:
                    state[k] = v
        elif cmd == "commit":
            if not snapshots:
                raise ValueError
            snapshots.pop()

    if snapshots:
        raise ValueError

    return {"state": state, "reads": reads}
