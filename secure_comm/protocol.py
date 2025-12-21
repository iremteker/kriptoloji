import json
import struct
from typing import Any, Dict

HEADER_STRUCT = struct.Struct("!I")  # 4 byte uzunluk


def send_frame(sock, obj: Dict[str, Any]) -> None:
    data = json.dumps(obj, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    sock.sendall(HEADER_STRUCT.pack(len(data)) + data)


def recv_exact(sock, n: int) -> bytes:
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("Socket closed")
        buf += chunk
    return buf


def recv_frame(sock) -> Dict[str, Any]:
    header = recv_exact(sock, HEADER_STRUCT.size)
    (length,) = HEADER_STRUCT.unpack(header)
    payload = recv_exact(sock, length)
    return json.loads(payload.decode("utf-8"))
