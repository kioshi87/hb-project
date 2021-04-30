"""Server for copoun account app."""

from flask import Flask, render_template, request, flash, session,redirect

from model import User, connect_to_db
from pprint import pformat
import os
import crud

from jinja2 import StrictUndefined
import requests
import json

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

@app.route('/account_login')
def account_landing_page():
    """Displays page after successfully logging into account"""

    return render_template('account-results.html')

@app.route('/coupon')
def coupon_search_page():
    """load coupon search page"""

    return render_template('coupon-search.html')

@app.route('/coupon/search')
def coupon_search():
    """ Search coupons """

    catergories = request.args.get('categories', '')
    title = request.args.get('title', '')
    description = request.args.get('description', '')
    code = request.args.get('code', '')
    source = request.args.get('source', '')
    store = request.args.get('store', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')

    url = 'https://couponapi.org/api/getFeed'
    payload = {'apikey': API_KEY,
                'categories' : catergories,
                'title': title,
                'description' : description,
                'code' : code,
                'source' : source,
                'store' : store,
                'start_date': start_date,
                'end_date' : end_date}

    response = requests.get(url, params=payload)

    print(response.text)
    data = response.json()
    copoun = data['_embedded']['copoun']

    #coupon = crud.create_coupon()

    return redirect('/coupon_results',
                    pformat=pformat,
                    data=data,
                    results=copoun)


@app.route('/coupon_results')
def get_coupoun_search_results():
    """Display coupon results"""

    return render_template('coupon-results.html')


#@app.route('/user_account')
#def get_account_data():
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

    return redirect('/coupon') #redirect cto another app-route to get to an html use render_template


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
 
