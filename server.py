"""Server for copoun account app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
#app.secret_key = ""
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

@app.route('/coupons')
def coupon_search():
    """ Search coupons """

    coupon = crud.create_coupon()

    return render_template('coupons.html', coupon)


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
        flash('Account created! Please log in.')

    #user_account = crud.create_user_account()

    return redirect('/')



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
