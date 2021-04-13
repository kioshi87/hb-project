from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Replace this with your code!
class Users(dm.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True,
                        nullable=False)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)


class Coupons(db.Model):
    """Coupon Codes"""

    __tablename__ = 'coupons'

    lmd_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True,
                        nullable=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    reward_type = db.Column(db.String)
    code = db.Column(db.String)
    offer = db.Column(db.String)
    offer_value = db.Column(db.String)
    store = db.Column(db.String)
    url = db.Column(db.url)
    image = db.Column(db.url)
    categories = db.Column(db.String)
    start_date = db.Column(db.date)
    end_date = db.Column(db.date)
    status = db.Column(db.String)


class userAccounts(db.Model):
    """A user_account"""

    __tablename__ = 'user_accounts'
    
    
    account_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True,
                            nullable=True)
    user_id = db.Column(db.Integer)
    lmd_id = db.Column(db.Integer)


def connect_to_db(flask_app, db_uri='postgresql:///ratings', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
