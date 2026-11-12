def transaction_trace(operations: list[list]) -> dict:
    state = {}
    reads = []
    snapshots = []

    for op in operations:
        cmd = op[0]
        if cmd == "set":
            key, val = op[1], op[2]
            if snapshots:
                snapshots[-1].setdefault("set", {})[key] = state.get(key, None)
                snapshots[-1].setdefault("delete", set()).discard(key)
            state[key] = val
        elif cmd == "delete":
            key = op[1]
            if key in state:
                if snapshots:
                    snapshots[-1].setdefault("delete", set()).add(key)
                    snapshots[-1].setdefault("set", {})[key] = state.get(key, None)
                del state[key]
        elif cmd == "get":
            key = op[1]
            reads.append(state.get(key, None))
        elif cmd == "begin":
            snapshots.append({})
        elif cmd == "commit":
            if not snapshots:
                raise ValueError
            top = snapshots.pop()
            if snapshots:
                parent = snapshots[-1]
                for k, v in top.get("set", {}).items():
                    parent.setdefault("set", {})[k] = v
                parent.setdefault("delete", set()).update(top.get("delete", set()))
        elif cmd == "rollback":
            if not snapshots:
                raise ValueError
            top = snapshots.pop()
            for k in top.get("delete", set()):
                state[k] = top["set"][k]
            for k, v in top.get("set", {}).items():
                if v is None:
                    state.pop(k, None)
                else:
                    state[k] = v

    if snapshots:
        raise ValueError
    return {"state": state, "reads": reads}
