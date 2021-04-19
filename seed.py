"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system('dropdb user_accounts')
os.system('createdb user_accounts')

model.connect_to_db(server.app)
model.db.create_all()

# Load coupon data from JSON file
with open('data/coupons.json') as f:
	coupon_data = json.loads(f.read())

#Create coupon and store in a list
coupons_in_db =[]
for coupon in coupon_data:
	store, title, description, reward_type, code, offer, offer_value,url = (coupon['store'],
																			coupon['title'],
																			coupon['description'],
																			coupon['reward_type'],
																			coupon['code'],
																			coupon['offer'],
																			coupon['offer_value'],
																			coupon['url'])
	image_url, smartLink, categories, status =  (coupon['image_url'],
												 coupon['smartLink'],
												 coupon['categories'],
												 coupon['status'])
	start_date = datetime.strptime(coupon['start_date'], '%Y-%m-%d')
	end_date = datetime.strptime(coupon['end_date'], '%Y-%m-%d')


	db_coupon = crud.create_coupon(store,
								   title,
								   description,
								   reward_type,
								   code,
								   offer,
								   offer_value,
								   url,
								   image_url,
								   smartLink,
								   categories,
								   status,
								   start_date,
								   end_date)
	coupons_in_db.append(db_coupon)


# Create 5 users, then a coupon and creates a user account
for n in range(5):
	username = f'user{n}'
	email = f'user{n}@test.com'
	password = 'test'

	user = crud.create_user(username, email, password)

	for _ in range(5):
		random_coupon = choice(coupons_in_db)

		crud.create_user_account(user, random_coupon)