from flask import Flask, render_template, request, session
import sqlite3

app = Flask(__name__)
app.secret_key = "autopartspro_secret_key"


def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?",
            (email, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            return "Login successful! Welcome " + user[1]

        return "Invalid email or password"

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, password)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return "Email already registered"

        conn.close()
        return "Registration successful! You can login now."

    return render_template("register.html")


@app.route("/shop")
def shop():
    return render_template("shop.html")


@app.route("/add-to-cart/<path:product>")
def add_to_cart(product):
    if "cart" not in session:
        session["cart"] = []

    session["cart"].append(product)
    session.modified = True

    return render_template("cart.html", cart=session["cart"])

    return render_template("cart.html", cart=cart)


@app.route("/cart")
def cart():
    cart = session.get("cart", [])
    return render_template("cart.html", cart=cart)


@app.route("/product")
def product():
    return render_template("product.html")


@app.route("/sell")
def sell():
    return render_template("sell.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


init_db()

if __name__ == "__main__":
    app.run(debug=True)