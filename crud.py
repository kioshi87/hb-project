"""CRUD operations."""

from model import db, Users, Coupons, userAccounts, connect_to_db


def create_user(username, email, password):
    """Create and return a new user."""

    user = Users(username=username, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user


def create_coupon(title, description, reward_type, code, offer, offer_value, store, url,
                  image, categories, start_date, end_date, status):
    """Create and return a coupon"""


    coupon = Coupons(title=title,
                    description=description,
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
    
    account = userAccounts(user=user, lmd=lmd)

    db.session.add(account)
    db.session.commit()

    return account


if __name__ == '__main__':
    from server import app
    connect_to_db(app)