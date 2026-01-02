from flask import Flask, render_template, request, redirect
import mysql.connector
import time

app = Flask(__name__)

# Wait for MySQL to be ready
time.sleep(10)

db = mysql.connector.connect(
    host="mysql",        # Docker service name
    user="root",
    password="root",
    database="login_db"
)

cursor = db.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    password VARCHAR(100)
)
""")
db.commit()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password)
        )
        db.commit()

        return "Login data stored successfully!"

    return render_template("login.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
