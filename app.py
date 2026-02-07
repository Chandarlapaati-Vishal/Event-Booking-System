from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "tcs_secret_key"

def get_db():
    return sqlite3.connect("database.db")

@app.route("/")
def index():
    db = get_db()
    events = db.execute("SELECT * FROM events").fetchall()
    return render_template("index.html", events=events)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        db = get_db()
        db.execute(
            "INSERT INTO users VALUES (NULL, ?, ?, ?, ?)",
            (name, email, password, role)
        )
        db.commit()
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        ).fetchone()

        if user:
            session["user_id"] = user[0]
            session["role"] = user[4]
            return redirect("/")
    return render_template("login.html")

@app.route("/event/<int:event_id>")
def event_detail(event_id):
    db = get_db()
    event = db.execute(
        "SELECT * FROM events WHERE id=?",
        (event_id,)
    ).fetchone()
    return render_template("event_detail.html", event=event)

@app.route("/book/<int:event_id>")
def book_event(event_id):
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    ticket_id = f"TKT{event_id}{user_id}"

    db = get_db()
    db.execute(
        "INSERT INTO bookings VALUES (NULL, ?, ?, ?)",
        (user_id, event_id, ticket_id)
    )
    db.commit()

    return f"Booking Confirmed! Ticket ID: {ticket_id}"

@app.route("/admin")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect("/login")

    db = get_db()
    events = db.execute("SELECT * FROM events").fetchall()
    return render_template("admin_dashboard.html", events=events)

app.run(debug=True)
