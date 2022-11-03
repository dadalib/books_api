import os
from flask import Flask, render_template,jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

app = Flask(__name__)

# Check for environement variable
if not os.getenv("DATA_BASE_URL"):
    raise RuntimeError("DATA_BASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
uri = os.getenv("DATA_BASE_URL")
print(uri)
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://","postgresql://",1)
    print("Uri changed")

# Link SQL service
engine = create_engine(uri)
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template('index.html',logged_in=False)

@app.route("/api/<isbn>")
def book_api(isbn):
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn",{"isbn":isbn}).fetchone()
    db.commit()
    if book is None:
        print("Not Found")
        return jsonify({"error":"Not found"}),404

    return jsonify({
        "title": book["title"],
        "author": book["author"],
        "year": book["year"],
    })

