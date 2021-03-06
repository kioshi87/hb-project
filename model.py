from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Replace this with your code!
class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True,
                        nullable=False)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)


class Coupon(db.Model):
    """Coupon Codes"""

    __tablename__ = 'coupons'

    offer_id = db.Column(db.Integer,
                        primary_key=True,
                        nullable=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    code = db.Column(db.String)
    source = db.Column(db.String)
    url = db.Column(db.String)
    affiliate_link = db.Column(db.String)
    image_url = db.Column(db.String)
    store = db.Column(db.String)
    categories = db.Column(db.String)
    start_date = db.Column(db.Integer)
    end_date = db.Column(db.Integer)
    status = db.Column(db.String)

    def __init__(self, offer_id, title, description, code, source,
                 url, affiliate_link, image_url, store, categories,
                 start_date, end_date, status):

        self.offer_id = offer_id
        self.title = title
        self.description = description
        self.code = code
        self.source = source
        self.url = url
        self.affiliate_link = affiliate_link
        self.image_url = image_url
        self.store = store
        self.categories = categories
        self.start_date = start_date
        self.end_date = end_date
        self.status = status


class userAccount(db.Model):
    """A user_account"""

    __tablename__ = 'user_accounts'
    
    
    account_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True,
                            nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    offer_id = db.Column(db.Integer, db.ForeignKey('coupons.offer_id'))



def connect_to_db(flask_app, db_uri='postgresql:///user_accounts', echo=True):  #instance of a flask, what is called from server (db_uri specifies what database to actually call)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri   
    flask_app.config['SQLALCHEMY_ECHO'] = echo          #accepts Boolean, defaulted to true, allows you to SQL command being ran
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
