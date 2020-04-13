import datetime
import subprocess
import json
from alert import check_result
from pymongo import MongoClient

client = MongoClient()
db = client['speedcheck']
collection = db['testdata']

print("\nStarting speedtest...")
data = subprocess.check_output('speedtest -f json', shell=True)
data = data.decode("utf-8")
data = json.loads(data)
print("Finished speedtest")

result = {
        "_id" : datetime.datetime.now(),
        "ping" : data['ping']['latency'],
        "download" : (data['download']['bytes']*8) / (data['download']['elapsed']*1000),
        "upload" : (data['upload']['bytes']*8) / (data['upload']['elapsed']*1000),
        }

collection.insert_one(result)
print("Added results into database:\nPing - {0}\nDownload - {1}\nUpload - {2}\nAt time {3}".format(result['ping'], result['download'], result['upload'], result['_id']))
with open('/tmp/dmapi.log', 'a+') as logfile:
    logfile.write("Successfully recorded test at " + str(result['_id'])+"\n")

if check_result(result):
    print("Alert sent")
else:
    print("No alert sent")
