from flask import Flask
import csv
import json
import time

app = Flask(__name__)

@app.route("/", methods=['GET'])
def getJSON():

	startTime = time.time()

	table = {}
	with open('accounts.csv', mode='r', encoding='utf-8-sig') as csvf:
		csvReader = csv.DictReader(csvf)

		for row in csvReader:
			key = row['id']
			table[key] = row

		jsonDict = json.dumps(table)


	print(time.time() - startTime)	#2.8 milliseconds

	return jsonDict

if __name__ == '__main__':
    app.run(debug=True)