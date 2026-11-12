"""Trusted-side evaluator. Never receives or executes candidate source."""
import json
import math
import sys
import traceback


EXCEPTIONS = {exc.__name__: exc for exc in (ValueError, TypeError, KeyError, IndexError, RuntimeError)}
protocol_failed = False


class CandidateProtocolError(BaseException):
    pass


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
    if type(value) is not dict:
        if value is None or type(value) in (bool, int, str) or (type(value) is float and math.isfinite(value)):
            return value
        raise ValueError("invalid result")
    kind = value.get("t")
    if kind == "ref" and value.keys() == {"t", "id"} and type(value["id"]) is int:
        return references[value["id"]]
    if value.keys() != {"t", "v"}:
        raise ValueError("invalid result fields")
    return decode_container(kind, value["v"], references, depth)


def decode_container(kind, values, references, depth=0):
    if type(values) is not list:
        raise ValueError("invalid container payload")
    if kind == "list":
        return [decode(item, references, depth + 1) for item in values]
    if kind == "tuple":
        return tuple(decode(item, references, depth + 1) for item in values)
    if kind == "dict":
        entries = {}
        for pair in values:
            if type(pair) is not list or len(pair) != 2:
                raise ValueError("invalid dictionary entry")
            key, item = pair
            entries[decode(key, references, depth + 1)] = decode(item, references, depth + 1)
        return entries
    raise ValueError("invalid result type")


def read_response(references):
    line = sys.stdin.readline(65537)
    if not line.endswith("\n") or len(line) > 65536:
        raise ValueError("candidate response unavailable")
    envelope = json.loads(line)
    if envelope["type"] != "reply":
        raise ValueError("invalid supervisor reply")
    response = envelope["response"]
    mutable = {key: value for key, value in references.items() if type(value) in (list, dict)}
    updates = []
    for update in response["updates"]:
        if update.keys() != {"id", "t", "v"} or type(update["id"]) is not int:
            raise ValueError("invalid candidate update")
        target = mutable.pop(update["id"])
        if update["t"] != type(target).__name__:
            raise ValueError("invalid candidate update type")
        updates.append((target, decode_container(update["t"], update["v"], references)))
    if mutable:
        raise ValueError("missing candidate updates")
    if response["ok"]:
        value, exception = decode(response["value"], references), None
    else:
        value, exception = None, EXCEPTIONS[response["exception"]]
    # Validate the entire graph before changing any evaluator-side object.
    for target, replacement in updates:
        if type(target) is list:
            target[:] = replacement
        else:
            target.clear()
            target.update(replacement)
    return value, exception


def make_proxy(name):
    def call(*args, **kwargs):
        global protocol_failed
        references, identities = {}, {}
        try:
            request = {"type": "call", "name": name, "args": encode(args, references, identities),
                       "kwargs": encode(kwargs, references, identities)}
            print(json.dumps(request, allow_nan=False, separators=(",", ":")), flush=True)
            value, exception = read_response(references)
        except Exception as exc:
            protocol_failed = True
            raise CandidateProtocolError("candidate transport failed") from exc
        if exception is not None:
            raise exception("candidate raised an exception")
        return value
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
    status = "failed_tests" if protocol_failed else "passed"
print(json.dumps({"type": "final", "status": status, "diagnostic": diagnostic}), flush=True)
