def transaction_trace(operations: list[list]) -> dict:
    state: dict[str, int] = {}
    reads: list[int | None] = []
    snapshots: list[dict[str, int | None]] = []

    for op in operations:
        cmd = op[0]
        if cmd == "set":
            key, value = op[1], op[2]
            if snapshots:
                if op[1] not in snapshots[-1]:
                    snapshots[-1][key] = state.get(key)
            state[key] = value
        elif cmd == "delete":
            key = op[1]
            if snapshots:
                if key not in snapshots[-1]:
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
            changes = snapshots.pop()
            if snapshots:
                snapshots[-1].update(changes)
        elif cmd == "rollback":
            if not snapshots:
                raise ValueError
            changes = snapshots.pop()
            for k, v in changes.items():
                if v is None:
                    state.pop(k, None)
                else:
                    state[k] = v
        else:
            raise ValueError

    if snapshots:
        raise ValueError

    return {"state": state, "reads": reads}
