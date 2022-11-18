from flask import Flask
import csv
import json
import time
import phonenumbers

app = Flask(__name__)

@app.route("/", methods=['GET'])
def getJSON():
#GET endpoint, returns parsed CSV as JSON

	startTime = time.time()

	table = {}
	with open('accounts.csv', mode='r', encoding='utf-8-sig') as csvf:
		csvReader = csv.DictReader(csvf)

		for row in csvReader:
			key = row['id']
			row['phone'] = reformat_e164(row['phone'], row['country'])
			table[key] = row

		jsonDict = json.dumps(table)


	print(time.time() - startTime)	# ~3 milliseconds

	return jsonDict



#--------------------------------------------------------------------------------
def reformat_e164(phone, country):
#reformats phone number 123-456-7890 into e164 format, +X1234567890

	country_code = phonenumbers.country_code_for_region(country)
	return "+" + str(country_code) + phone.replace('-', '')


if __name__ == '__main__':
    app.run(debug=True)