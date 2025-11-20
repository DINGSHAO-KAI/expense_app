mport os
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# 建立資料庫
def init_db():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    records = cursor.fetchall()
    conn.close()
    return render_template("index.html", records=records)

@app.route("/add", methods=["GET"])
def add_page():
    return render_template("add.html")

@app.route("/add", methods=["POST"])
def add_expense():
    title = request.form["title"]
    amount = request.form["amount"]
    date = request.form["date"]

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (title, amount, date) VALUES (?, ?, ?)",
        (title, amount, date)
    )
    conn.commit()
    conn.close()

    return redirect("/")

# Render 需要監聽 0.0.0.0 + PORT
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
