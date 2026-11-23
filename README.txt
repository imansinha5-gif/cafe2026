BEAN & BLOOM CAFE - STARTER PROJECT

Project structure:
  app.py                    Flask application / API routes
  backend/cafe_backend.py   Menu, order processing and SQLite database logic
  backend/__init__.py
  frontend/index.html       Cafe website (HTML, CSS and JavaScript)
  cafe.db                   Created automatically on first run

SETUP (Windows PowerShell)
1. Open PowerShell in this project folder.
2. Create a virtual environment (optional but recommended):
      py -m venv .venv
      .venv\Scripts\Activate.ps1
3. Install Flask:
      py -m pip install flask
4. Start the app:
      py app.py
5. Open this address in your browser:
      http://127.0.0.1:5000

FEATURES
- Cafe menu with categories and prices
- Add items and update quantities in cart
- Automatic total calculation in INR
- Place customer orders
- Orders saved in a local SQLite database
- GET /api/orders returns saved orders (useful for a future staff dashboard)

NOTE
This is a learning/demo project. It does not process real online payments.
For production, add authentication, input/output hardening, CSRF protection,
HTTPS, backups, and a payment provider's official checkout integration.
