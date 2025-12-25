from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import requests

import sqlite3

import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def get_db():
    conn = sqlite3.connect("booktrack.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        db = get_db()
        cursor = db.cursor()

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return render_template("register.html", error="All fields are required")
        if password != confirmation:
            return render_template("register.html", error="Must be the same password")
        
        cursor.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        )

        user = cursor.fetchone()

        if user:
            db.close()
            return render_template("register.html", error="Username already in use.")
        
        passwordHashed = generate_password_hash(password)

        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES(?, ?)", (username, passwordHashed)
        )

        db.commit()
        db.close()

        return redirect("/login")
        
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if(request.method == "POST"):
        db = get_db()
        cursor = db.cursor()

        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return render_template("login.html", error="All fields are required")
        
        cursor.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        )

        user = cursor.fetchone()

        if user == None or not check_password_hash(user["password_hash"], password):
            db.close()
            return render_template("login.html", error="Username or password incorrects")
        
        session["user_id"] = user["id"]
        db.close()
        return redirect("/profile")

    else:
        return render_template("login.html")


@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect("/login")
    
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT username FROM users where id = ?", (session["user_id"],)
    )

    user = cursor.fetchone()

    cursor.execute(
        "SELECT title, authors, thumbnail, description, status FROM books WHERE user_id = ?", (session["user_id"],)
    )

    books = cursor.fetchall()

    cursor.execute(
        "SELECT * FROM books WHERE status = 'finished' AND user_id = ?", (session["user_id"],)
    )

    finished_books = cursor.fetchall()

    cursor.execute(
        "SELECT * FROM books WHERE status = 'to_read' AND user_id = ?", (session["user_id"],)
    )

    to_read_books = cursor.fetchall()

    cursor.execute(
        "SELECT * FROM books WHERE status = 'reading' AND user_id = ?", (session["user_id"],)
    )

    reading_books = cursor.fetchall()

    db.close()

    return render_template("profile.html", username=user["username"], books=books, finished_books=finished_books, to_read_books=to_read_books, reading_books=reading_books)

@app.route("/add", methods=["GET", "POST"])
def add():
    if "user_id" not in session:
        return redirect("/login")
    
    if request.method == "POST":
            db = get_db()
            cursor = db.cursor()

            google_id = request.form.get("google_id")
            title = request.form.get("title")
            authors = request.form.get("authors") or "Unknown author."
            thumbnail = request.form.get("thumbnail")
            description = request.form.get("description") or "Unknown description."
            status = request.form.get("status")

            if not google_id or not title:
                db.close()
                return render_template("add.html")
            
            if not thumbnail or thumbnail == "undefined":
                thumbnail = None
            
            cursor.execute(
                "SELECT id FROM books WHERE user_id = ? AND google_id = ?", (session["user_id"], google_id)
            )

            bookOwned = cursor.fetchone()

            if bookOwned:
                db.close()
                return redirect("/profile")

            cursor.execute(
                "INSERT INTO books (user_id, google_id, title, authors, thumbnail, description, status) VALUES (?, ?, ?, ?, ?, ?, ?)", (session["user_id"], google_id, title, authors, thumbnail, description, status)
            )

            db.commit()
            db.close()

            return redirect("/profile")
    else:
        query = request.args.get("search")
        results = []

        if query:
            url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={GOOGLE_BOOKS_API_KEY}"
            response = requests.get(url)
            data = response.json()
                
            results = []
            if "items" in data:
                for item in data["items"]:
                    volume_info = item.get("volumeInfo", {})
                    imageLinks = volume_info.get("imageLinks", {})
                    book_data = {
                        "google_id": item.get("id"),
                        "title": volume_info.get("title", "Unknown title"),
                        "authors": volume_info.get("authors", ["Unknown author"]),
                        "description": volume_info.get("description", "Unknown description"),
                        "thumbnail": imageLinks.get("thumbnail"),
                        "ratingsCount": volume_info.get("ratingsCount", 0)
                    }
                    results.append(book_data)
                
                results.sort(key=lambda b: b["ratingsCount"], reverse=True)
        
        return render_template("add.html", results=results)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/books/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    if "user_id" not in session:
        return redirect("/login")
    
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM books WHERE id = ? AND user_id = ?", (book_id, session["user_id"])
    )

    db.commit()
    db.close()

    return redirect("/profile")

@app.route("/books/<int:book_id>/update", methods=["POST"])
def update_book(book_id):
    db = get_db()
    cursor = db.cursor()

    if "user_id" not in session:
        return redirect("/login")
    
    new_status = request.form.get("status")

    if new_status not in ["finished", "reading", "to_read"]:
        return redirect("/profile")
    
    cursor.execute(
        "UPDATE books SET status = ? WHERE id = ? AND user_id = ?", (new_status, book_id, session["user_id"])
    )

    db.commit()
    db.close()

    return redirect("/profile")
    

if __name__ == "__main__":
    app.run(debug=True) 