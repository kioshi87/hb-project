"""CRUD operations."""

from model import db, User, Coupon, userAccount, connect_to_db


def create_user(user_id, username, email, password):
    """Create and return a new user."""

    user = User(user_id=user_id, username=username, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user
    

def get_user_by_username(username):
    """Return a user by username"""

    return User.query.filter(User.username == username).first()


def get_user_by_email(email):
    """Return a user by email"""

    return User.query.filter(User.email == email).first()
    

def get_user_by_email_and_user_id(email, user_id):
    """Return a user by email"""

    return User.query.filter(User.email == email, User.user_id == user_id).first()



def create_coupon(offer_id, title, description, code, source, url, affiliate_link,
                  image_url, store, categories, start_date, end_date, status):
    """Create and return a coupon"""


    coupon = Coupon(offer_id=offer_id,
                    title=title,
                    description=description,
                    code=code,
                    source=source,
                    url=url,
                    affiliate_link =affiliate_link,
                    image_url=image_url,
                    store = store,
                    categories=categories,
                    start_date=start_date,
                    end_date=end_date,
                    status=status)

    db.session.add(coupon)
    db.session.commit()

    return coupon

def create_user_account(user_id, coupon):
    """Create and return a user account."""
    
    account = userAccount(user_id=user_id, offer_id=coupon.offer_id)

    db.session.add(account)
    db.session.commit()

    return account

def get_user_accounts(user_id):
    """ Returns list of all user accounts. """
    
    return userAccount.query.filter_by(user_id).all()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)