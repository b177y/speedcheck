import datetime
import subprocess
import json
from alert import check_result
from pymongo import MongoClient

client = MongoClient()
db = client['speedcheck']
collection = db['testdata']

print("\nStarting speedtest...")
data = subprocess.check_output('speedtest --csv', shell=True)
data = data.decode("utf-8")
data = data.split(",")
print("Finished speedtest")

result = {
        "_id" : datetime.datetime.now(),
        "ping" : float(data[5]),
        "download" : float(data[6]) / 10 ** 6,
        "upload" : float(data[7]) / 10 ** 6
        }

collection.insert_one(result)
print("Added results into database:\nPing - {0}\nDownload - {1}\nUpload - {2}\nAt time {3}".format(result['ping'], result['download'], result['upload'], result['_id']))

if check_result(result):
    print("Alert sent")
else:
    print("No alert sent")
