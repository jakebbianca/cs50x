import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import time
import copy

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():

    # Query for cash holdings of current user
    cash = float(db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session.get("user_id"))[0]['cash'])

    sharestotal = 0

    # Select total shares purchased and sold by current user by stock
    transactions = db.execute("SELECT symbol, company, sum(CASE WHEN buy_sell = 'Buy' THEN shares ELSE 0 END) AS purchased_shares, sum(CASE WHEN buy_sell = 'Sell' THEN shares ELSE 0 END) AS sold_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol",
                            user_id=session.get("user_id"))

    if not transactions:
        return render_template("index.html", cash=usd(float(cash)), total=usd(float(cash)))

    # Create list to fill with stock information as dicts to pass through to index.html
    stocks = []

    for row in transactions:

        quoteDict = lookup(row['symbol'])
        price = quoteDict['price']

        # Calculate current held shares by calculating difference of purchased shares less sold shares
        shares = row['purchased_shares'] - row['sold_shares']

        # Calculate total value of held shares for this stock
        line = float(price) * float(shares)
        sharestotal += line
        line = line
        price = price

        # Append values for row stock to pass through to index.html
        stocks.append({'symbol': row['symbol'], 'company': row['company'], 'price': usd(price), 'shares': shares, 'line': usd(line)})

    total = float(cash) + sharestotal

    return render_template("index.html", stocks=stocks, sharestotal=usd(float(sharestotal)), cash=usd(float(cash)), total=usd(float(total)))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():

    if request.method == "POST":

        # Ensure that some symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide a stock symbol", 403)

        # Ensure that some amount of shares was submitted
        if not request.form.get("shares"):
            return apology("must provide a number of shares you want to purchase", 403)

        # Ensure that the amount of shares is positive
        if not int(request.form.get("shares")) >= 1:
            return apology("must buy a positive integer of shares")

        # Ensure that the amount of shares is an integer
        if not int(request.form.get("shares")) % 1 == 0:
            return apology("must buy a positive integer of shares")

        symbol = request.form.get("symbol")
        nshares = request.form.get("shares")

        # Check that the stock symbol provided is valid
        if not lookup(symbol):
            return apology("must provide a valid symbol", 403)

        # Save the current stock info in a dict
        quoteDict = lookup(symbol)

        # Before purchase takes place, query the cash balance for the current user
        startBalance = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session.get("user_id"))

        # Calculate cost of the total desired stock purchase
        buyCost = quoteDict['price'] * float(nshares)

        # Calculate the difference of the user's cash less the total cost of the desired purchase
        endBalance = float(startBalance[0]['cash']) - float(buyCost)

        # Ensure that the current user can afford to make their desired purchase
        if endBalance < 0:
            return apology("insufficient funds to make purchase", 403)

        # Update 'transactions' table with new purchase
        db.execute("INSERT INTO transactions (symbol, company, shares, price, total, buy_sell, date, time, user_id) VALUES (:symbol, :company, :shares, :price, :total, :buy_sell, :date, :time, :user_id)",
                    symbol=quoteDict['symbol'], company=quoteDict['name'], shares=int(nshares), price=quoteDict['price'], total=float(nshares)*quoteDict['price'],
                    buy_sell='Buy', date=datetime.now().date(), time=datetime.now().time(), user_id=session.get("user_id"))

        # Update user's cash balance
        db.execute("UPDATE users SET cash = :newBalance WHERE id = :user_id", newBalance=endBalance, user_id=session.get("user_id"))

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():

    transactions = db.execute("SELECT * FROM transactions WHERE user_id = :user_id", user_id = session.get("user_id"))

    for row in transactions:

        row['price'] = usd(row['price'])

    return render_template("history.html", transactions=transactions)


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
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

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


@app.route("/changepass", methods=["GET", "POST"])
@login_required
def changepass():

    if request.method == "POST":

        # Check inputs for validity, make sure current pass is correct
        if not request.form.get("current-password"):
            return apology("must provide current password", 403)

        if not request.form.get("new-password"):
            return apology("must provide new password", 403)

        rows = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session.get("user_id"))


        # Check that password hashes match
        if not check_password_hash(rows[0]["hash"], request.form.get("current-password")):
            return apology("current password entered was incorrect", 403)

        if request.form.get("current-password") == request.form.get("new-password"):
            return apology("new password cannot be current password", 403)

        # Update password
        db.execute("UPDATE users SET hash = :hashed WHERE id = :user_id", hashed=generate_password_hash(request.form.get("new-password")), user_id=session.get("user_id"))

        return redirect("/")
    else:
        return render_template("changepass.html")

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure that some symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide a stock symbol", 403)

        symbol = request.form.get("symbol")

        if not lookup(symbol):
            return apology("must provide a valid symbol", 403)

        quoteDict = lookup(symbol)

        return render_template("quoted.html", companyName=quoteDict['name'], symbol=quoteDict['symbol'], price=quoteDict['price'])

    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure that the password confirmation matches the password entry
        elif not request.form.get("confirm-password") == request.form.get("password"):
            return apology("password and password confirmation entries must match", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        if len(rows) != 0:
            return apology("username is already in use", 403)


        db.execute("INSERT INTO users (username, hash) VALUES (:username, :passhash)",
                                    username=request.form.get("username"),
                                    passhash=generate_password_hash(request.form.get("password")))

        return redirect("/login")

    else:

        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

    if request.method == "POST":

        # Ensure that some symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide a stock symbol", 403)

        # Ensure that some amount of shares was submitted
        if not request.form.get("shares"):
            return apology("must provide a number of shares you want to purchase", 403)

        # Ensure that the amount of shares is positive
        if not int(request.form.get("shares")) >= 1:
            return apology("must buy a positive integer of shares")

        # Ensure that the amount of shares is an integer
        if not int(request.form.get("shares")) % 1 == 0:
            return apology("must buy a positive integer of shares")

        # Select total shares purchased and sold by current user by stock
        transactions = db.execute("SELECT symbol, company, sum(CASE WHEN buy_sell = 'Buy' THEN shares ELSE 0 END) AS purchased_shares, sum(CASE WHEN buy_sell = 'Sell' THEN shares ELSE 0 END) AS sold_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol",
                                    user_id=session.get("user_id"))

        # If there are no transactions, user must not own any stock, so prevent sale
        if not transactions:
            return apology("You don't have any shares to sell", 403)


        for row in transactions:

            # Compare symbol given in form to symbols for stocks user has purchased and/or sold
            if request.form.get("symbol") != row['symbol']:
                continue

            # Calculate currently held shares for user-provided stock
            shares = int(row['purchased_shares']) - int(row['sold_shares'])

            # If user tries to sell more shares than they own, prevent sale
            if int(request.form.get("shares")) > shares:
                return apology("Not enough shares of this stock to sell desired quantity", 403)

        # Once passing all validation, complete sale of stock and update cash balance
        quoteDict = lookup(request.form.get('symbol'))

        # Calculate cash balance after completion of sale
        precash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session.get("user_id"))[0]['cash']
        salevalue = float(request.form.get('shares')) * quoteDict['price']
        postcash = precash + salevalue


        # Update 'transactions' table with new sale
        db.execute("INSERT INTO transactions (symbol, company, shares, price, total, buy_sell, date, time, user_id) VALUES (:symbol, :company, :shares, :price, :total, :buy_sell, :date, :time, :user_id)",
                    symbol=quoteDict['symbol'], company=quoteDict['name'], shares=int(request.form.get('shares')), price=quoteDict['price'], total=float(request.form.get('shares'))*quoteDict['price'],
                    buy_sell='Sell', date=datetime.now().date(), time=datetime.now().time(), user_id=session.get("user_id"))


        # Update cash balance
        db.execute("UPDATE users SET cash = :cash WHERE id = :user_id", cash=postcash, user_id=session.get("user_id"))

        return redirect("/")

    else:

        # Select total shares purchased and sold by current user by stock
        transactions = db.execute("SELECT symbol, company, sum(CASE WHEN buy_sell = 'Buy' THEN shares ELSE 0 END) AS purchased_shares, sum(CASE WHEN buy_sell = 'Sell' THEN shares ELSE 0 END) AS sold_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol",
                                    user_id=session.get("user_id"))

        if not transactions:
            return apology("You don't have any shares to sell", 403)

        stocks = []

        for row in transactions:

            quoteDict = lookup(row['symbol'])
            symbol = quoteDict['symbol']

            shares = row['purchased_shares'] - row['sold_shares']

            if shares < 1:
                continue

            stocks.append({'symbol': symbol, 'shares': shares})

        return render_template("sell.html", stocks=stocks)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
