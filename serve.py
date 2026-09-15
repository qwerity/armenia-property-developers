"""Serve web/ on http://localhost:<port> for both IPv4 (127.0.0.1) and IPv6 (::1), local machine only.

Usage: python3 serve.py [port]   (default 5190)
"""
import functools
import http.server
import socket
import sys
import threading
from pathlib import Path

WEB = Path(__file__).resolve().parent / "web"


class V6Server(http.server.ThreadingHTTPServer):
    address_family = socket.AF_INET6


def main() -> int:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5190
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(WEB))
    servers = [http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)]
    try:
        servers.append(V6Server(("::1", port), handler))
    except OSError as e:  # IPv6 loopback unavailable: IPv4 still works
        print(f"IPv6 loopback not available: {e}", file=sys.stderr)
    for s in servers[1:]:
        threading.Thread(target=s.serve_forever, daemon=True).start()
    print(f"Serving {WEB} at http://localhost:{port}", flush=True)
    try:
        servers[0].serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
