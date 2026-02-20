from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # потрібний для сесій (логін)

# Дані товарів
products = [
    {"id": 1, "name": "Собача іграшка", "price": 150, "image": "product1.jpg"},
    {"id": 2, "name": "Корм для котів", "price": 200, "image": "product1.jpg"}
]

cart = []

# Логін кабінету продавця
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"  # зміни на свій пароль

# Головна сторінка
@app.route("/")
def home():
    return render_template("index.html", products=products)

# Сторінка товару
@app.route("/product/<int:product_id>")
def product(product_id):
    product_item = next((p for p in products if p["id"] == product_id), None)
    return render_template("product.html", product=product_item)

# Додати у кошик
@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    product_item = next((p for p in products if p["id"] == product_id), None)
    if product_item:
        cart.append(product_item)
    return redirect(url_for("cart_page"))

# Кошик
@app.route("/cart")
def cart_page():
    total = sum(item["price"] for item in cart)
    return render_template("cart.html", cart=cart, total=total)

# Логін у кабінет продавця
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin"))
        else:
            return render_template("login.html", error="Невірний логін або пароль")
    return render_template("login.html")

# Кабінет продавця
@app.route("/admin")
def admin():
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))
    return render_template("admin.html", products=products)

# Додати товар
@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))
    if request.method == "POST":
        new_id = max([p["id"] for p in products] + [0]) + 1
        name = request.form.get("name")
        price = float(request.form.get("price"))
        image = request.form.get("image")  # назва файлу у static/images/
        products.append({"id": new_id, "name": name, "price": price, "image": image})
        return redirect(url_for("admin"))
    return render_template("add_product.html")

# Вихід з кабінету
@app.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
