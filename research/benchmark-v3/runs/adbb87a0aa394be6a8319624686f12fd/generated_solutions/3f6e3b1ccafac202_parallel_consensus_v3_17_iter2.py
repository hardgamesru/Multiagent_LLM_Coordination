def transaction_trace(operations: list[list]) -> dict:
    state: dict[str, int] = {}
    reads: list[int | None] = []
    snapshots: list[dict[str, int | None]] = []

    for op in operations:
        cmd = op[0]
        if cmd == "set":
            key, val = op[1], op[2]
            if snapshots:
                if snapshots[-1].get(key, object()) is None:
                    snapshots[-1][key] = val
                elif key not in snapshots[-1]:
                    snapshots[-1][key] = state.get(key)
            state[key] = val
        elif cmd == "delete":
            key = op[1]
            if snapshots:
                if snapshots[-1].get(key, object()) is None:
                    snapshots[-1][key] = None
                elif key not in snapshots[-1]:
                    snapshots[-1][key] = state.get(key)
            state.pop(key, None)
        elif cmd == "get":
            key = op[1]
            reads.append(state.get(key))
        elif cmd == "begin":
            snapshots.append({})
        elif cmd == "commit":
            if not snapshots:
                raise ValueError
            parent = snapshots.pop()
            if snapshots:
                for k, v in parent.items():
                    if k not in snapshots[-1]:
                        snapshots[-1][k] = v
            else:
                for k, v in parent.items():
                    if v is None:
                        state.pop(k, None)
                    else:
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
