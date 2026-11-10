"""Untrusted-side worker. Runs only inside its own isolated container."""
import contextlib
import json
import sys


def decode(value, references):
    if not isinstance(value, dict) or "t" not in value:
        return value
    kind = value["t"]
    if kind == "ref":
        return references[value["id"]]
    if kind == "list":
        result = []
        references[value["id"]] = result
        result.extend(decode(item, references) for item in value["v"])
        return result
    if kind == "dict":
        result = {}
        references[value["id"]] = result
        result.update((decode(k, references), decode(v, references)) for k, v in value["v"])
        return result
    if kind == "tuple":
        result = tuple(decode(item, references) for item in value["v"])
        references[value["id"]] = result
        return result
    raise ValueError("unsupported input type")


def encode(value, reverse, depth=0):
    if depth > 64:
        raise ValueError("result nesting too deep")
    if value is None or type(value) in (bool, int, float, str):
        return value
    if id(value) in reverse:
        return {"t": "ref", "id": reverse[id(value)]}
    if type(value) in (list, tuple):
        return {"t": "list" if type(value) is list else "tuple",
                "v": [encode(item, reverse, depth + 1) for item in value]}
    if type(value) is dict:
        return {"t": "dict", "v": [[encode(k, reverse, depth + 1), encode(v, reverse, depth + 1)]
                                   for k, v in value.items()]}
    raise ValueError("unsupported result type")


def collect_updates(references, reverse):
    updates = []
    for key, value in references.items():
        if type(value) is list:
            updates.append({"id": key, "t": "list", "v": [encode(item, reverse) for item in value]})
        elif type(value) is dict:
            updates.append({"id": key, "t": "dict", "v": [[encode(k, reverse), encode(v, reverse)]
                                                            for k, v in value.items()]})
    return updates


payload = json.loads(sys.stdin.readline())
sys.stderr.write(payload["ready"] + "\n")
sys.stderr.flush()
namespace = {"__name__": "__candidate__"}
try:
    with contextlib.redirect_stdout(sys.stderr):
        exec(compile(payload["code"], "<candidate>", "exec"), namespace)
except BaseException:
    sys.exit(1)

sys.stderr.write(payload["initialized"] + "\n")
sys.stderr.flush()

for line in sys.stdin:
    references = {}
    reverse = {}
    try:
        request = json.loads(line)
        args = decode(request["args"], references)
        kwargs = decode(request["kwargs"], references)
        reverse = {id(value): key for key, value in references.items()}
        with contextlib.redirect_stdout(sys.stderr):
            result = namespace[request["name"]](*args, **kwargs)
        reply = {"ok": True, "value": encode(result, reverse), "updates": collect_updates(references, reverse)}
    except BaseException as exc:
        # Exception text is untrusted and is never forwarded to the evaluator.
        exception = type(exc).__name__ if type(exc) in (ValueError, TypeError, KeyError, IndexError) else "RuntimeError"
        reply = {"ok": False, "exception": exception}
        try:
            reply["updates"] = collect_updates(references, reverse)
        except BaseException:
            reply = {"ok": False, "exception": "RuntimeError"}
    sys.stdout.write(json.dumps(reply, allow_nan=False, separators=(",", ":")) + "\n")
    sys.stdout.flush()
