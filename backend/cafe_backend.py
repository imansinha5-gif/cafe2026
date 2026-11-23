import sqlite3
from pathlib import Path

DEFAULT_MENU = [
    {"id": 1, "name": "Cappuccino", "category": "Coffee", "price": 140, "description": "Espresso with steamed milk foam"},
    {"id": 2, "name": "Cold Coffee", "category": "Coffee", "price": 160, "description": "Chilled creamy coffee"},
    {"id": 3, "name": "Masala Tea", "category": "Tea", "price": 60, "description": "Indian tea with warming spices"},
    {"id": 4, "name": "Veg Sandwich", "category": "Snacks", "price": 120, "description": "Toasted sandwich with fresh vegetables"},
    {"id": 5, "name": "French Fries", "category": "Snacks", "price": 100, "description": "Crispy salted potato fries"},
    {"id": 6, "name": "Chocolate Brownie", "category": "Dessert", "price": 110, "description": "Rich chocolate brownie"},
]

class CafeBackend:
    def __init__(self, db_path):
        self.db_path = Path(db_path)
        self._initialize()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _initialize(self):
        with self._connect() as con:
            con.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_name TEXT NOT NULL,
                    items TEXT NOT NULL,
                    total REAL NOT NULL,
                    status TEXT NOT NULL DEFAULT 'Received',
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def get_menu(self):
        return DEFAULT_MENU

    def create_order(self, items, customer_name):
        if not isinstance(items, list) or not items:
            raise ValueError("Please add at least one item to your cart.")

        menu_by_id = {item["id"]: item for item in DEFAULT_MENU}
        order_lines = []
        total = 0

        for entry in items:
            try:
                item_id = int(entry["id"])
                quantity = int(entry["quantity"])
            except (KeyError, TypeError, ValueError):
                raise ValueError("Each cart item needs a valid id and quantity.")
            if item_id not in menu_by_id or quantity < 1 or quantity > 50:
                raise ValueError("An item or quantity in your cart is invalid.")
            product = menu_by_id[item_id]
            line_total = product["price"] * quantity
            total += line_total
            order_lines.append({
                "name": product["name"],
                "quantity": quantity,
                "unit_price": product["price"],
                "line_total": line_total
            })

        customer_name = str(customer_name).strip()[:80] or "Guest"
        import json
        with self._connect() as con:
            cur = con.execute(
                "INSERT INTO orders (customer_name, items, total) VALUES (?, ?, ?)",
                (customer_name, json.dumps(order_lines), total)
            )
            order_id = cur.lastrowid

        return {"id": order_id, "customer_name": customer_name,
                "items": order_lines, "total": total, "status": "Received"}

    def get_orders(self):
        import json
        with self._connect() as con:
            rows = con.execute(
                "SELECT id, customer_name, items, total, status, created_at "
                "FROM orders ORDER BY id DESC"
            ).fetchall()
        return [
            {"id": row[0], "customer_name": row[1], "items": json.loads(row[2]),
             "total": row[3], "status": row[4], "created_at": row[5]}
            for row in rows
        ]
