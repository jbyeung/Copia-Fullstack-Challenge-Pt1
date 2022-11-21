from flask import Flask
import csv
import json
import time
import phonenumbers
import sqlite3


app = Flask(__name__)
connection = sqlite3.connect("copia.sqlite")
cursor = connection.cursor()


@app.route("/getAllUsers", methods=['GET'])
def getJSON():
	#GET endpoint, returns parsed CSV as JSON

	# start = time.time()
	with sqlite3.connect('copia.sqlite') as conn:
		cursor = conn.cursor()

		sql = "SELECT json_object('id', id, 'firstName', firstName, 'lastName', lastName, 'street', street, 'city', city, 'state', state, 'postal', postal, 'country', country, 'email', email, 'phone', phone) AS json_result FROM (SELECT * FROM users);"

		# sql = "SELECT * FROM users"
		cursor.execute(sql)
		jsonData = json.dumps(cursor.fetchall())
		# print(time.time() - start)			#4.2 milliseconds
		return jsonData



#--------------------------------------------------------------------------------
#helper functions
def reformat_e164(phone, country):
	#reformats phone number 123-456-7890 into e164 format, +X1234567890

	country_code = phonenumbers.country_code_for_region(country)
	return "+" + str(country_code) + phone.replace('-', '')

def init_db(connection):
	#creates empty table, then injects data from CSV file

	query = """
	CREATE TABLE IF NOT EXISTS users (
		id INTEGER, 
		firstName TEXT,
		lastName TEXT,
		street TEXT,
		city TEXT,
		state TEXT,
		postal TEXT,
		country TEXT,
		email TEXT, 
		phone TEXT
	);
	"""

	#run query to create table
	try:
		cursor.execute(query)
		connection.commit()
		print("Query executed successfully")
	except sqlite3.Error as e:
		print(f"The error '{e}' occurred")
		return

	#inject CSV data
	insertData()


#SQLite functions
def create_connection(path):
	# creates sql connection
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred")

    return connection

def insertData():
	# reads CSV file and attempts to insert into table

	with open('accounts.csv', mode='r', encoding='utf-8-sig') as csvf:
		csvReader = csv.DictReader(csvf)
		data = []

		for row in csvReader:
			row['phone'] = reformat_e164(row['phone'], row['country'])
			entry = [row['id'], row['firstName'], row['lastName'], row['street'], row['city'], row['state'], row['postal'], row['country'], row['email'], row['phone']]
			data.append(entry)

		keys = ', '.join(row.keys())
		valholders = ', '.join('?' * len(row))
		q = 'INSERT INTO users ({}) VALUES ({})'.format(keys, valholders)
		try:
			cursor.executemany(q, data)
			connection.commit()
			print("Query executed successfully")
		except sqlite3.Error as e:
			print(f"The error '{e}' occurred")
			return

if __name__ == '__main__':
	init_db(connection)
	app.run(debug=True)