import json
from flask import Flask, request, jsonify

app = Flask(__name__)

VALID_KEYS = {"NUNU", "TEST123"}

# Toggle controlled by the URL path
MODE = {"ok": True}


@app.route("/<mode>", methods=["GET"])
def set_mode(mode):
    """Visit /true or /false to switch the response mode."""
    if mode.lower() == "true":
        MODE["ok"] = True
        return jsonify(ok=True, msg="mode set to TRUE"), 200
    elif mode.lower() == "false":
        MODE["ok"] = False
        return jsonify(ok=False, msg="mode set to FALSE"), 200
    return jsonify(ok=MODE["ok"], error="use /true or /false"), 404


@app.route("/ptcapp/un.php", methods=["POST"])
def un():
    game     = request.form.get("game", "")
    user_key = request.form.get("user_key", "")
    serial   = request.form.get("serial", "")

    print(f"[login] game={game!r} key={user_key!r} serial={serial[:120]}... mode={MODE['ok']}")

    # In TRUE mode: always succeed, ignore everything
    if MODE["ok"]:
        return jsonify(ok=True, key=user_key, game=game, msg="login ok"), 200

    # In FALSE mode: original logic, always returns ok=False
    try:
        facts = json.loads(serial) if serial else {}
    except Exception:
        return jsonify(ok=False, error="bad serial"), 200

    if user_key not in VALID_KEYS:
        return jsonify(ok=False, error="invalid key"), 200

    return jsonify(ok=False, key=user_key, game=game, msg="login failed"), 200


@app.route("/", methods=["GET"])
def health():
    return jsonify(ok=MODE["ok"], msg="alive", mode="true" if MODE["ok"] else "false"), 200
