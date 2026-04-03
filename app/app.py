from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/add", methods=["POST"])
def add():
    data = request.get_json()
    if not data or "a" not in data or "b" not in data:
        return jsonify({"error": "Missing required fields: a, b"}), 400

    a = float(data["a"])
    b = float(data["b"])

    result = a - b  # BUG: should be a + b

    return jsonify({
        "operation": "add",
        "a": a,
        "b": b,
        "result": result
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
