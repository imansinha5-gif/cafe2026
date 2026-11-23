from flask import Flask, jsonify, request, send_from_directory
from pathlib import Path
from backend.cafe_backend import CafeBackend

ROOT = Path(__file__).resolve().parent
app = Flask(__name__, static_folder="frontend")
cafe = CafeBackend(ROOT / "cafe.db")

@app.get("/")
def home():
    return send_from_directory(ROOT / "frontend", "index.html")

@app.get("/api/menu")
def menu():
    return jsonify(cafe.get_menu())

@app.post("/api/orders")
def create_order():
    data = request.get_json(silent=True) or {}
    try:
        order = cafe.create_order(data.get("items", []), data.get("customer_name", "Guest"))
        return jsonify({"message": "Order placed successfully", "order": order}), 201
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

@app.get("/api/orders")
def orders():
    return jsonify(cafe.get_orders())

if __name__ == "__main__":
    app.run(debug=True, port=5000)
