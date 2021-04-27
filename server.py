"""Server for copoun account app."""

from flask import Flask, render_template, request, flash, session,redirect

from model import connect_to_db
from pprint import pformat
import os
import crud

from jinja2 import StrictUndefined
import keyword
from pip._vendor import requests

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.secret_key = "secret"


API_KEY = os.environ['COUPON_KEY']


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

@app.route('/account_creation')
def account_creation_page():
    """Take user to account creation page"""

    return render_template('account-form.html')

@app.route('/coupon_search')
def coupon_search_page():
    """load coupon search page"""

    return render_template('coupon-search.html')

@app.route('/coupon')
def coupon_search():
    """ Search coupons """

    keyword = request.args.get('keyword', '')

    url = 'http://feed.linkmydeals.com/getOffers'
    payload = {'apikey': API_KEY,
                'keyword': keyword}

    response = requests.get(url, params=payload)

    data = response.json()
    copouns = data['_embedded']['copouns']

    #coupon = crud.create_coupon()

    return render_template('coupon-results.html',
                            pformat=pformat,
                            data=data,
                            results=copouns)


@app.route('/user_account')
def get_account_data():
    """GET user account data"""

    username = crud.get_user_by_username()
    
    return render_template('account-results.html', username=username)


@app.route('/useraccounts', methods=['POST'])
def create_account():
    """ Create user account"""

    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    if user:
        flash('Cannot create an account with that email. Try again.')
    else:
        crud.create_user(username, email, password)
        flash('Account created!')

    return redirect('/coupon_search') #redirect cto another app-route to get to an html use render_template


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if not user:
        flash("No such email address.")
        return redirect('/login')

    if user.password != password:
        flash("Incorrect password.")
        return redirect("/login")

    session["logged_in_user_id"] = user.id
    flash("Logged in.")
    return redirect("/user_account")


@app.route("/logout")
def process_logout():
    """Log user out."""

    del session["logged_in_user_id"]
    flash("Logged out.")
    return redirect("/")

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
 