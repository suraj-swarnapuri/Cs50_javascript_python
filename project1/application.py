import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
goodreads_api_key = "J0pNS5TU42DPCAd79w"

@app.route("/")
def index():
    return render_template('login.html')

@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("user")
    passw = request.form.get("pass")
    session['name'] = name
    return render_template('home.html',name=name)

@app.route("/search", methods=["GET","POST"])
def search():
    option = request.form.get("selectpicker")
    value = request.form.get("search")
    books=[]
    if option == "ISBN":
       books = db.execute("SELECT * FROM books WHERE isbn LIKE '%"+value+"%'").fetchall()
    elif option == "Title":
       books = db.execute("SELECT * FROM books WHERE title LIKE '%"+value+"%'").fetchall()
    elif option == "Author" :
        books = db.execute("SELECT * FROM books WHERE author LIKE '%"+value+"%'").fetchall()
    return render_template("home.html",name=session["name"],books=books)

@app.route("/books/<string:book_isbn>")
def book(book_isbn):
    book = db.execute("SELECT * from books where isbn=:isbn",{"isbn":book_isbn}).fetchone()
    print(book)
    return render_template("book.html",book=book, reviews=[])

