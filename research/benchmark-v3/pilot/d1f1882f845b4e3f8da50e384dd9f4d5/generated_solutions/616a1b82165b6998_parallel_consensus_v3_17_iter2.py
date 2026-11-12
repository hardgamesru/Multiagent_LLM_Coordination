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
                snapshots[-1].setdefault("del", set()).discard(key)
            state[key] = val
        elif cmd == "delete":
            key = op[1]
            if key in state:
                if snapshots:
                    snapshots[-1].setdefault("del", set()).add(key)
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
            changes = snapshots.pop()
            if snapshots:
                parent_set = snapshots[-1].setdefault("set", {})
                parent_del = snapshots[-1].setdefault("del", set())
                for k, v in changes.get("set", {}).items():
                    parent_set[k] = v
                for k in changes.get("del", set()):
                    parent_del.add(k)
        elif cmd == "rollback":
            if not snapshots:
                raise ValueError
            changes = snapshots.pop()
            for k in changes.get("del", set()):
                state[k] = changes["set"][k]
            for k, v in changes.get("set", {}).items():
                if v is None:
                    state.pop(k, None)
                else:
                    state[k] = v
    if snapshots:
        raise ValueError
    return {"state": state, "reads": reads}
