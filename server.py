"""Server for copoun account app."""

from flask import Flask, render_template, request, flash, session, redirect

from model import User, connect_to_db
from pprint import pformat
import os
import crud
from model import Coupon

from jinja2 import StrictUndefined
import requests
import json
import csv
from setuptools._vendor.pyparsing import col

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.secret_key = "secret"


API_KEY = os.environ['API_KEY']


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')


@app.route('/account_creation')
def account_creation_page():
    """Take user to account creation page"""

    return render_template('account-form.html')


@app.route('/account_login')
def account_landing_page():
    """Displays page after successfully logging into account"""

    return render_template('account-results.html')


@app.route('/coupon')
def coupon_search_page():
    """load coupon search page"""

    return render_template('coupon-search.html')


@app.route('/coupon_search')
def coupon_search():
    """ Search coupons """

    category = request.args.get('categories')
    coupons = []
    failure = 'No coupon could be found matching that category. Please try again.'


    with open('data/full_coupon_database.tsv') as tsv_f:
        f = csv.reader(tsv_f, delimiter="\t",)
        row  = [line for line in f]

        for rows in f:
            if row.data == str(category):
                coupons.append(row)

                print(coupons)
            else:
                return failure

    return render_template('coupon-results.html', coupons=coupons)


@app.route('/coupon_results')
def get_coupoun_search_results():
    """Display coupon results"""

    return render_template('coupon-results.html')


# @app.route('/user_account')
# def get_account_data():
    """GET user account data"""

    #username = crud.get_user_by_username()

 #   return render_template('account-results.html')


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    #user_id = User.query.filter_by(user_id=user_id).first()

    if not user:
        flash("No such user.")
        return redirect('/login')

    if user.password != password:
        flash("Incorrect password.")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in.")
    return redirect(F"/account_login/{user.user_id}")



@app.route('/coupon-accounts', methods=['POST'])
def show_saved_coupons():
    """Get user account data"""

    # I updated the form value to be the offer_id of each coupon
    offer_id = request.form.get('coupon-choice')

    categories = request.args.get('categories', '')
    title = request.args.get('title', '')
    description = request.args.get('description', '')
    code = request.args.get('code', '')
    source = request.args.get('source', '')
    store = request.args.get('store', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    image_url = request.args.get('image_url', '')
    url = request.args.get('url', '')
    affiliate_link = request.args.get('affiliate_link', '')
    status = request.args.get('status', '')

    # Grab user id from session because we need it to make an account
    user_id = session['user_id']


    # now create your new coupon and add to the db; and create your new user account and add to db
    new_coupon = crud.create_coupon(offer_id, title, description, code, source, url, affiliate_link,
                                    image_url, store, categories, start_date, end_date, status)
    new_user_account = crud.create_user_account(user_id, offer_id)

    # now query your user accounts table for all existing coupons for that user and pass that as a list to the template
    all_user_accounts = crud.get_user_accounts(user_id)

    return render_template('account-results.html', all_user_accounts=all_user_accounts)

@app.route("/logout")
def process_logout():
    """Log user out."""

    del session["user_id"]
    flash("Logged out.")
    return redirect("/")


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

    # redirect cto another app-route to get to an html use render_template
    return redirect('/coupon')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
