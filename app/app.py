from flask import Flask, render_template, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

db_config = {
    "host": os.getenv("MYSQL_HOST", "db"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "root"),
    "database": os.getenv("MYSQL_DB", "registration")
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            password VARCHAR(100)
        )
    """)

    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
        (name, email, password)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Registration successful!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
