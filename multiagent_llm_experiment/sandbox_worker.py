"""Candidate-side adapter. Its private IPC replies are untrusted data."""
import json
import socket
import sys


MAX_INPUT = 128 * 1024
MAX_RPC = 64 * 1024


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


def main(channel):
    # Exec'd descendants inherit only the ordinary, discarded standard streams.
    channel.set_inheritable(False)
    source = channel.recv(MAX_INPUT + 2)
    if not source.startswith(b"\x00") or len(source) > MAX_INPUT + 1:
        raise ValueError("invalid candidate source frame")
    namespace = {"__name__": "__candidate__"}
    exec(compile(source[1:].decode("utf-8"), "<candidate>", "exec"), namespace)
    channel.sendall(b"initialized")

    while packet := channel.recv(MAX_RPC + 1):
        if len(packet) > MAX_RPC:
            raise ValueError("oversized call")
        request = json.loads(packet)
        references = {}
        args = decode(request["args"], references)
        kwargs = decode(request["kwargs"], references)
        reverse = {id(value): key for key, value in references.items()}
        try:
            result = namespace[request["name"]](*args, **kwargs)
        except BaseException as exc:
            exc_type = type(exc)
            exception = exc_type.__name__ if exc_type in (ValueError, TypeError, KeyError, IndexError) else "RuntimeError"
            reply = {"ok": False, "exception": exception}
        else:
            reply = {"ok": True, "value": encode(result, reverse)}
        reply["updates"] = collect_updates(references, reverse)
        data = json.dumps(reply, allow_nan=False, separators=(",", ":")).encode("ascii")
        if len(data) > MAX_RPC:
            raise ValueError("oversized candidate result")
        channel.sendall(data)


if __name__ == "__main__":
    with socket.socket(fileno=int(sys.argv[1])) as endpoint:
        main(endpoint)
