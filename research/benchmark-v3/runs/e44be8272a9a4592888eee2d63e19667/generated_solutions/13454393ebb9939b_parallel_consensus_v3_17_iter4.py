def transaction_trace(operations: list[list]) -> dict:
    state = {}
    reads = []
    snapshots = []

    for op in operations:
        cmd = op[0]
        if cmd == "set":
            key, val = op[1], op[2]
            if snapshots:
                snapshots[-1].setdefault("_w", {})[key] = val
            else:
                state[key] = val
        elif cmd == "delete":
            key = op[1]
            if snapshots:
                snapshots[-1].setdefault("_w", {})[key] = None
            else:
                state.pop(key, None)
        elif cmd == "get":
            key = op[1]
            if snapshots:
                w = snapshots[-1].get("_w", {})
                if key in w:
                    reads.append(w[key])
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
            if not snapshots:
                for k, v in top.get("_w", {}).items():
                    if v is None:
                        state.pop(k, None)
                    else:
                        state[k] = v
            else:
                parent = snapshots[-1].setdefault("_w", {})
                for k, v in top.get("_w", {}).items():
                    parent[k] = v
        elif cmd == "rollback":
            if not snapshots:
                raise ValueError
            snapshots.pop()

    if snapshots:
        raise ValueError

    return {"state": state, "reads": reads}
