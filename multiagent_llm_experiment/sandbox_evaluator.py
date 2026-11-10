"""Trusted-side evaluator. Never receives or executes candidate source."""
import json
import sys
import traceback


def encode(value, references, identities, depth=0):
    if depth > 64:
        raise ValueError("input nesting too deep")
    if value is None or type(value) in (bool, int, float, str):
        return value
    if type(value) not in (list, tuple, dict):
        raise ValueError("unsupported input type")
    identity = id(value)
    if identity in identities:
        return {"t": "ref", "id": identities[identity]}
    index = len(references)
    identities[identity] = index
    references[index] = value
    if type(value) is dict:
        data = [[encode(k, references, identities, depth + 1), encode(v, references, identities, depth + 1)]
                for k, v in value.items()]
        kind = "dict"
    else:
        data = [encode(item, references, identities, depth + 1) for item in value]
        kind = "tuple" if type(value) is tuple else "list"
    return {"t": kind, "id": index, "v": data}


def decode(value, references, depth=0):
    if depth > 64:
        raise ValueError("result nesting too deep")
    if not isinstance(value, dict):
        if value is None or type(value) in (bool, int, float, str):
            return value
        raise ValueError("invalid result")
    kind = value.get("t")
    if kind == "ref":
        return references[value["id"]]
    if kind == "list":
        return [decode(item, references, depth + 1) for item in value["v"]]
    if kind == "tuple":
        return tuple(decode(item, references, depth + 1) for item in value["v"])
    if kind == "dict":
        return {decode(k, references, depth + 1): decode(v, references, depth + 1) for k, v in value["v"]}
    raise ValueError("invalid result type")


def make_proxy(name):
    def call(*args, **kwargs):
        references, identities = {}, {}
        request = {"type": "call", "name": name, "args": encode(args, references, identities),
                   "kwargs": encode(kwargs, references, identities)}
        print(json.dumps(request, allow_nan=False, separators=(",", ":")), flush=True)
        line = sys.stdin.readline(65537)
        if not line or len(line) > 65536:
            raise RuntimeError("candidate response unavailable")
        response = json.loads(line)
        if not isinstance(response, dict) or type(response.get("ok")) is not bool:
            raise RuntimeError("invalid candidate response")
        updates = response.get("updates", [])
        if not isinstance(updates, list) or len(updates) > len(references):
            raise RuntimeError("invalid candidate updates")
        for update in updates:
            target = references[update["id"]]
            if update["t"] == "list" and type(target) is list:
                target[:] = [decode(item, references) for item in update["v"]]
            elif update["t"] == "dict" and type(target) is dict:
                entries = [(decode(k, references), decode(v, references)) for k, v in update["v"]]
                target.clear()
                target.update(entries)
            else:
                raise RuntimeError("invalid candidate update type")
        if not response["ok"]:
            exc = {"ValueError": ValueError, "TypeError": TypeError, "KeyError": KeyError,
                   "IndexError": IndexError}.get(response.get("exception"), RuntimeError)
            raise exc("candidate raised an exception")
        return decode(response["value"], references)
    return call


payload = json.loads(sys.stdin.readline())
sys.stderr.write(payload["ready"] + "\n")
sys.stderr.flush()
namespace = {name: make_proxy(name) for name in payload["functions"]}
diagnostic = ""
try:
    exec(compile(payload["tests"], "<tests>", "exec"), namespace)
except BaseException as exc:
    status = "failed_tests"
    if payload["diagnostics"]:
        frame = next((f for f in reversed(traceback.extract_tb(exc.__traceback__)) if f.filename == "<tests>"), None)
        if frame:
            lines = payload["tests"].splitlines()
            line = lines[frame.lineno - 1].strip() if 0 < frame.lineno <= len(lines) else ""
            diagnostic = (type(exc).__name__ + " at development test line " + str(frame.lineno) + ": " + line)[:512]
else:
    status = "passed"
print(json.dumps({"type": "final", "status": status, "diagnostic": diagnostic}), flush=True)
