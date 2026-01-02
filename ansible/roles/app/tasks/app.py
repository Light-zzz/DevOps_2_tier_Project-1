from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="db",
    user="root",
    password="root",
    database="users"
)

cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS login (username VARCHAR(50), password VARCHAR(50))")

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        cursor.execute("INSERT INTO login VALUES (%s,%s)", (u,p))
        db.commit()
        return "Login stored in DB"
    return render_template("login.html")

app.run(host="0.0.0.0")
