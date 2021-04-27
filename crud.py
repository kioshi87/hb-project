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


def create_coupon(title, description, reward_type, code, offer, offer_value, store, url,
                  image, categories, start_date, end_date, status):
    """Create and return a coupon"""


    coupon = Coupon(title=title,
                    description=    description,
                    reward_type=reward_type,
                    code=code,
                    offer=offer,
                    offer_value=offer_value,
                    store=store,
                    url=url,
                    image=image,
                    categories=categories,
                    start_date=start_date,
                    end_date=end_date,
                    status=status)

    db.session.add(coupon)
    db.session.commit()

    return coupon

def create_user_account(user, lmd):
    """Create and return a user account."""
    
    account = userAccount(user=user, lmd=lmd)

    db.session.add(account)
    db.session.commit()

    return account


if __name__ == '__main__':
    from server import app
    connect_to_db(app)