from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = "secret123"   # required for flash messages

# ----------------------------
# MySQL Configuration
# ----------------------------
db_config = {
    "host": os.getenv("MYSQL_HOST", "mysql"),     # service name in docker-compose
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "root"),
    "database": os.getenv("MYSQL_DB", "registration")
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# ----------------------------
# Routes
# ----------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    if not name or not email or not password:
        flash("All fields are required!", "error")
        return redirect(url_for("index"))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
        """)

        # Insert data
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password)
        )

        conn.commit()
        cursor.close()
        conn.close()

        flash("Registration successful!", "success")

    except mysql.connector.Error as err:
        flash(f"Database error: {err}", "error")

    return redirect(url_for("index"))

# ----------------------------
# App Runner
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
