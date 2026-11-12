def transaction_trace(operations: list[list]) -> dict:
    state: dict[str, int] = {}
    reads: list[int | None] = []
    snapshots: list[dict[str, int | None]] = []

    for op in operations:
        cmd = op[0]
        if cmd == "set":
            _, key, value = op
            state[key] = value
        elif cmd == "delete":
            _, key = op
            state.pop(key, None)
        elif cmd == "get":
            _, key = op
            reads.append(state.get(key))
        elif cmd == "begin":
            snapshots.append(state.copy())
        elif cmd == "commit":
            if not snapshots:
                raise ValueError
            snapshots.pop()
        elif cmd == "rollback":
            if not snapshots:
                raise ValueError
            state = snapshots.pop()

    if snapshots:
        raise ValueError

    return {"state": state, "reads": reads}
