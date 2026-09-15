import json
from flask import Flask, request, jsonify

app = Flask(__name__)

VALID_KEYS = {"NUNU", "TEST123"}

EXPECTED = {
    # "cert":  "<sha256 of signing cert>",
    # "hash0": "<sha256 of classes.dex>",
    # ...
}

@app.route("/ptcapp/un.php", methods=["POST"])
def un():
    game     = request.form.get("game", "")
    user_key = request.form.get("user_key", "")
    serial   = request.form.get("serial", "")

    print(f"[login] game={game!r} key={user_key!r} serial={serial[:120]}...")

    try:
        facts = json.loads(serial) if serial else {}
    except Exception:
        return jsonify(ok=False, error="bad serial"), 200

    if user_key not in VALID_KEYS:
        return jsonify(ok=False, error="invalid key"), 200

    for k, expected in EXPECTED.items():
        if facts.get(k) != expected:
            return jsonify(ok=False, error=f"bad {k}"), 200

    return jsonify(ok=True, key=user_key, game=game, msg="login ok"), 200


@app.route("/", methods=["GET"])
def health():
    return jsonify(ok=True, msg="auth endpoint alive"), 200        print(f"[login] game={game!r} key={user_key!r} serial={serial[:120]}...")

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
