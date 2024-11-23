from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory "database" for products
products = [
    {"id": 1, "name": "Laptop", "price": 1200},
    {"id": 2, "name": "Headphones", "price": 200},
    {"id": 3, "name": "Mouse", "price": 50},
]

# Utility Functions
def calculate_cart_value(cart_items):
    total = 0
    for item in cart_items:
        product = next((p for p in products if p["id"] == item["id"]), None)
        if product:
            total += product["price"] * item["quantity"]
    return total

def validate_cart_items(cart_items):
    for item in cart_items:
        if not isinstance(item.get("id"), int) or not isinstance(item.get("quantity"), int):
            raise ValueError("Invalid cart item format.")
    return True

# Routes
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the E-commerce API!"}), 200

@app.route("/api/products", methods=["GET"])
def get_products():
    return jsonify(products), 200

@app.route("/api/cart", methods=["POST"])
def calculate_cart():
    data = request.get_json()
    try:
        validate_cart_items(data)
        total = calculate_cart_value(data)
        return jsonify({"total_value": total}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Main entry point
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
