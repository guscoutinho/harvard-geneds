#
# CS50 Final Project
# Harvard Geneds
# Developed by Beatriz Marinho, Gustavo Coutinho and Marcia Lagesse
#

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///courses50.db")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    return render_template("homepage.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure passwords match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match", 400)

        # Hash password to increase protection
        hash = generate_password_hash(request.form.get("password"))

        # Query database for username
        rows = db.execute("INSERT INTO users (username, password) VALUES(:username, :password)",
                          username=request.form.get("username"), password=hash)

        # Return if user is taken
        if not rows:
            return apology("username is already taken")

        # Store their id session
        session["user_id"] = rows

        # Redirect user to home page
        return redirect("/")

    # If method is GET
    else:
        return render_template("register.html")


@app.route("/homepage", methods=["GET", "POST"])
def homepage():
    # Create a list
    ids = list(request.form.keys())

    # Create a dictionary
    columns = {}

    # Iterates over each category (geneds) selected by the user (ids list)
    for cat in ids:

        # SQL query to join the two tables we have on course id and select all the classes (with their Q scores) in the categories chosen by the user
        rows = db.execute(
            "SELECT * FROM geneds AS g INNER JOIN Qcourses AS q ON g.Course_ID = q.course_id WHERE g.GenEd1=:cat OR g.GenEd2 = :cat OR g.GenEd3 = :cat", cat=cat)

        # Create a dictionary of dictionaries
        columns[cat] = {}

        # Iterates over the rows in the SQL table
        for row in rows:

            # Select the Class Name and Q score of the class
            columns[cat][row["Class_Name"]] = row["CourseOverall"]

    # Return html page with the classes the user can take to fulfill his or her gened requirements
    return render_template("ahvah.html", columns=columns)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
