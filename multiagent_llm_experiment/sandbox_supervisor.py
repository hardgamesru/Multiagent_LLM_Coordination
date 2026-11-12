"""Trusted supervisor for the candidate container. Never executes candidate Python."""

import ctypes
import json
import select
import socket
import struct
import subprocess
import sys


MAX_RPC = 64 * 1024
PID_CREDENTIALS = struct.Struct("=iII")
CREDENTIAL_SPACE = socket.CMSG_SPACE(PID_CREDENTIALS.size)
EXCEPTIONS = {"ValueError", "TypeError", "KeyError", "IndexError", "RuntimeError"}


def receive(channel, pid):
    packet, ancillary, flags, _ = channel.recvmsg(MAX_RPC, CREDENTIAL_SPACE, socket.MSG_CMSG_CLOEXEC)
    if not packet or flags & (socket.MSG_TRUNC | socket.MSG_CTRUNC) or len(ancillary) != 1:
        raise ValueError("missing or oversized worker packet")
    level, kind, credentials = ancillary[0]
    if (level, kind) != (socket.SOL_SOCKET, socket.SCM_CREDENTIALS):
        raise ValueError("missing worker credentials")
    sender, _, _ = PID_CREDENTIALS.unpack(credentials)
    if sender != pid:
        raise ValueError("packet from a worker descendant")
    return packet


def send_to_host(message):
    line = json.dumps(message, allow_nan=False, separators=(",", ":")) + "\n"
    if len(line) > MAX_RPC:  # json.dumps escapes non-ASCII by default
        raise ValueError("oversized supervisor reply")
    sys.stdout.write(line)
    sys.stdout.flush()


def supervise(channel, child, payload):
    # Only the supervisor can write the container's attached stdout and stderr.
    print(payload["ready"], file=sys.stderr, flush=True)
    channel.sendall(b"\x00" + payload["code"].encode("utf-8"))
    if receive(channel, child.pid) != b"initialized":
        raise ValueError("worker failed to initialize")
    print(payload["initialized"], file=sys.stderr, flush=True)

    while line := sys.stdin.buffer.readline(MAX_RPC + 1):
        if len(line) > MAX_RPC or not line.endswith(b"\n"):
            raise ValueError("invalid request frame")
        request = json.loads(line)
        if child.poll() is not None or select.select([channel], [], [], 0)[0]:
            raise ValueError("worker exited or sent unsolicited data")
        if request["type"] == "finish":
            send_to_host({"type": "finished"})
            return
        if request["type"] != "call":
            raise ValueError("invalid request")
        channel.sendall(line[:-1])
        response = json.loads(receive(channel, child.pid))
        if type(response) is not dict or type(response.get("ok")) is not bool:
            raise ValueError("invalid worker response")
        if type(response.get("updates")) is not list:
            raise ValueError("missing worker updates")
        if response["ok"]:
            if response.keys() != {"ok", "updates", "value"}:
                raise ValueError("invalid worker result")
        elif (response.keys() != {"ok", "updates", "exception"}
              or type(response["exception"]) is not str or response["exception"] not in EXCEPTIONS):
            raise ValueError("invalid worker exception")
        send_to_host({"type": "reply", "response": response})


def main():
    # Same-UID candidate code must not be able to ptrace the supervisor or
    # reopen its file descriptors through /proc/<pid>/fd.
    if ctypes.CDLL(None, use_errno=True).prctl(4, 0, 0, 0, 0) != 0:  # PR_SET_DUMPABLE
        raise OSError(ctypes.get_errno(), "cannot protect supervisor process")
    payload = json.loads(sys.stdin.buffer.readline())
    channel, endpoint = socket.socketpair(type=socket.SOCK_SEQPACKET)
    with channel, endpoint:
        channel.setsockopt(socket.SOL_SOCKET, socket.SO_PASSCRED, 1)
        child = subprocess.Popen(
            [sys.executable, "-I", "-c", sys.argv[1], str(endpoint.fileno())],
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            pass_fds=(endpoint.fileno(),),
        )
        endpoint.close()
        supervise(channel, child, payload)


if __name__ == "__main__":
    try:
        main()
    except (KeyError, OSError, RecursionError, TypeError, ValueError, struct.error):
        sys.exit(1)
