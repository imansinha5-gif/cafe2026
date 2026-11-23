
from flask import Flask, jsonify, request
from pathlib import Path
from backend.cafe_backend import CafeBackend

# Project directory
ROOT = Path(__file__).resolve().parent
FRONTEND = ROOT / "frontend"

# Flask application
app = Flask(
    __name__,
    static_folder=str(FRONTEND),
    static_url_path="/static"
)

# Initialize cafe database
cafe = CafeBackend(ROOT / "cafe.db")


# Home page - Frontend
@app.route("/")
def home():
    return app.send_static_file("index.html")


# Get cafe menu
@app.route("/api/menu", methods=["GET"])
def menu():
    return jsonify(cafe.get_menu())


# Place customer order
@app.route("/api/orders", methods=["POST"])
def create_order():
    data = request.get_json(silent=True) or {}

    try:
        order = cafe.create_order(
            data.get("items", []),
            data.get("customer_name", "Guest")
        )

        return jsonify({
            "message": "Order placed successfully",
            "order": order
        }), 201

    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


# Get all customer orders
@app.route("/api/orders", methods=["GET"])
def orders():
    return jsonify(cafe.get_orders())


# Health check
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "Cafe application is running"})


# Local development
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
