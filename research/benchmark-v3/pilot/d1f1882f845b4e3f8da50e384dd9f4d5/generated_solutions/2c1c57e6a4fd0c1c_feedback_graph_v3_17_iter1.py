def transaction_trace(operations: list[list]) -> dict:
    state = {}
    reads = []
    snapshots = []

    for op in operations:
        cmd = op[0]
        if cmd == "set":
            key, val = op[1], op[2]
            if snapshots:
                snapshots[-1].setdefault("_writes", {})[key] = val
            else:
                state[key] = val
        elif cmd == "delete":
            key = op[1]
            if snapshots:
                snapshots[-1].setdefault("_writes", {})[key] = None
            else:
                state.pop(key, None)
        elif cmd == "get":
            key = op[1]
            if snapshots:
                writes = snapshots[-1].get("_writes", {})
                if key in writes:
                    reads.append(writes[key])
                else:
                    reads.append(state.get(key))
            else:
                reads.append(state.get(key))
        elif cmd == "begin":
            snapshots.append({})
        elif cmd == "commit":
            if not snapshots:
                raise ValueError
            top = snapshots.pop()
            writes = top.get("_writes", {})
            if snapshots:
                parent = snapshots[-1].setdefault("_writes", {})
                for k, v in writes.items():
                    parent[k] = v
            else:
                for k, v in writes.items():
                    if v is None:
                        state.pop(k, None)
                    else:
                        state[k] = v
        elif cmd == "rollback":
            if not snapshots:
                raise ValueError
            snapshots.pop()

    if snapshots:
        raise ValueError

    return {"state": state, "reads": reads}
