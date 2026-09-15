import json
from flask import Flask, request, jsonify

app = Flask(__name__)

VALID_KEYS = {"NUNU", "TEST123"}

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

    return jsonify(ok=True, key=user_key, game=game, msg="login ok"), 200

@app.route("/", methods=["GET"])
def health():
    return jsonify(ok=True, msg="alive"), 200
