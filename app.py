
from flask import Flask, request, jsonify, render_template
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config["SECRET_KEY"] = "lab_secret_key"

# Demo users
users = {
    "admin": {"password": "admin123", "role": "ADMIN"},
    "seller": {"password": "seller123", "role": "SELLER"},
    "customer": {"password": "customer123", "role": "CUSTOMER"}
}

products = [
    {"id": 1, "name": "Laptop", "seller": "seller"},
    {"id": 2, "name": "Mobile", "seller": "seller"}
]

orders = [
    {"id": 101, "customer": "customer", "seller": "seller", "product": "Laptop"}
]

# JWT Login
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")

    user = users.get(username)

    if not user or user["password"] != password:
        return jsonify({"message": "Invalid credentials"}), 401

    token = jwt.encode({
        "sub": username,
        "role": user["role"],
        "exp": datetime.datetime.now(
            datetime.timezone.utc
        ) + datetime.timedelta(hours=1)
    }, app.config["SECRET_KEY"], algorithm="HS256")

    return jsonify({
        "message": "Login successful",
        "role": user["role"],
        "token": token
    })


# JWT Authentication + RBAC
def authorize(roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            header = request.headers.get("Authorization", "")

            if not header.startswith("Bearer "):
                return jsonify({"message": "Token missing"}), 401

            try:
                payload = jwt.decode(
                    header[7:],
                    app.config["SECRET_KEY"],
                    algorithms=["HS256"]
                )
            except jwt.ExpiredSignatureError:
                return jsonify({"message": "Token expired"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"message": "Invalid token"}), 401

            if payload.get("role") not in roles:
                return jsonify({"message": "Access Denied"}), 403

            request.user = payload
            return func(*args, **kwargs)
        return wrapper
    return decorator


# Homepage
@app.route("/")
def home():
    return render_template("index.html")


# Product Microservice
@app.route("/products", methods=["GET"])
@authorize(["ADMIN", "SELLER", "CUSTOMER"])
def get_products():
    return jsonify({"products": products})


@app.route("/products/add", methods=["POST"])
@authorize(["ADMIN", "SELLER"])
def add_product():
    data = request.get_json(silent=True) or {}
    name = data.get("name", "New Product")

    product = {
        "id": len(products) + 1,
        "name": name,
        "seller": request.user["sub"]
    }
    products.append(product)

    return jsonify({
        "message": "Product added successfully",
        "product": product
    })


@app.route("/products/<int:product_id>", methods=["DELETE"])
@authorize(["ADMIN", "SELLER"])
def delete_product(product_id):
    for product in products:
        if product["id"] == product_id:
            if (request.user["role"] != "ADMIN"
                    and product["seller"] != request.user["sub"]):
                return jsonify({"message": "Not your product"}), 403

            products.remove(product)
            return jsonify({"message": "Product deleted"})

    return jsonify({"message": "Product not found"}), 404


# Order Microservice
@app.route("/orders", methods=["GET"])
@authorize(["ADMIN", "SELLER", "CUSTOMER"])
def get_orders():
    role = request.user["role"]
    username = request.user["sub"]

    if role == "ADMIN":
        result = orders
    elif role == "SELLER":
        result = [o for o in orders if o["seller"] == username]
    else:
        result = [o for o in orders if o["customer"] == username]

    return jsonify({"orders": result})


# Payment Microservice
@app.route("/payment", methods=["POST"])
@authorize(["CUSTOMER"])
def payment():
    return jsonify({
        "message": "Payment processed successfully",
        "customer": request.user["sub"]
    })


# Customer Microservice - Admin Only
@app.route("/admin/users", methods=["GET"])
@authorize(["ADMIN"])
def manage_users():
    return jsonify({
        "message": "Admin access granted",
        "users": [
            {"username": name, "role": info["role"]}
            for name, info in users.items()
        ]
    })


if __name__ == "__main__":
    app.run(debug=True)
