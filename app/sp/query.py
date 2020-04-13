import datetime
from pymongo import MongoClient
from dateutil.relativedelta import relativedelta

client = MongoClient()
db = client['speedcheck']
collection = db['testdata']

def time_query(starttime, endtime="NOW"):
    if endtime == "NOW":
        endtime = datetime.datetime.now()
    if starttime == "hour":
        s = relativedelta(hours=-1)
        starttime = endtime + s
    elif starttime == "day":
        s = relativedelta(days=-1)
        starttime = endtime + s
    elif starttime == "month":
        s = relativedelta(months=-1)
        starttime = endtime + s
    elif starttime == "alltime":
        s = relativedelta(years=-1)
        starttime = endtime + s
    results=[]
    query = collection.find({'_id': {'$gte': starttime, '$lt': endtime}}).sort("_id")
    for r in query:
        results.append(r)
    print("Found {0} results between {1} and {2}.".format(len(results), starttime, endtime))
    return results
