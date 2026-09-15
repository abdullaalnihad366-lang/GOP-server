import json
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs

VALID_KEYS = {"NUNU", "TEST123"}

# Optional: expected hashes from a legit build. Leave empty to skip checks.
EXPECTED = {
    # "cert":  "<sha256 of signing cert>",
    # "hash0": "<sha256 of classes.dex>",
    # "hash1": "<sha256 of classes2.dex>",
    # "hash2": "<sha256 of lib/arm64-v8a/libdripclient.so>",
    # "hash3": "<sha256 of AndroidManifest.xml>",
    # "hash4": "<sha256 of resources.arsc>",
}


class handler(BaseHTTPRequestHandler):
    def _send(self, code, body):
        payload = json.dumps(body).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0") or "0")
        raw = self.rfile.read(length).decode("utf-8", errors="replace")
        form = {k: v[0] for k, v in parse_qs(raw, keep_blank_values=True).items()}

        game     = form.get("game", "")
        user_key = form.get("user_key", "")
        serial   = form.get("serial", "")

        print(f"[login] game={game!r} key={user_key!r} serial={serial[:120]}...")

        try:
            facts = json.loads(serial)
        except Exception:
            return self._send(200, {"ok": False, "error": "bad serial"})

        if user_key not in VALID_KEYS:
            return self._send(200, {"ok": False, "error": "invalid key"})

        # Optional integrity check
        for k, expected in EXPECTED.items():
            if facts.get(k) != expected:
                return self._send(200, {"ok": False, "error": f"bad {k}"})

        return self._send(200, {
            "ok": True,
            "key": user_key,
            "game": game,
            "msg": "login ok",
        })

    def do_GET(self):
        return self._send(200, {"ok": True, "msg": "auth endpoint alive"})
