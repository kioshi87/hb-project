"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server
import csv

os.system('dropdb user_accounts')
os.system('createdb user_accounts')

model.connect_to_db(server.app)
model.db.create_all()

#Load coupon data from CSV file, create coupon objects, load into db
with open('data/full_coupon_database.tsv') as tsv_f:
	f = csv.reader(tsv_f, delimiter="\t")
	count = 1

	for line in f:
		print('*******************************')
		print(count)
		print(line)
		print('*******************************')
		offer_id, title, description, code, source, affiliate_link, url, image_url, store, categories, start_date, end_date, status = line

		if start_date:
			start_date = datetime.strptime(start_date, '%Y-%m-%d')
		else: 
			start_date = None

		if end_date:
			end_date = datetime.strptime(end_date, '%Y-%m-%d')
		else:
			end_date = None

		coupon = crud.create_coupon(offer_id, title, description, code, source, url, affiliate_link,
                              image_url, store, categories, start_date, end_date, status)    
		count += 1

print('*******************************')
print('COUPON LOADING COMPLETE')
print('*******************************')


# Create 5 users, then a coupon and creates a user account
for n in range(5):
	username = f'user{n}'
	email = f'user{n}@test.com'
	password = 'test'

	user = crud.create_user(username, email, password)
	print('*******************************')
	print(user)
	print('*******************************')

	coupons_in_db = model.Coupon.query.all()
	for i in range(5):
		random_coupon = choice(coupons_in_db)
		crud.create_user_account(user, random_coupon)
print('*******************************')
print('DB SEEDED')
print('*******************************')