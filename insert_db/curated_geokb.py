# coding: utf-8

import sys, datetime
import json

import pymongo

def get_mongo_col(db="poi_db", col="bd_search"):
    client = pymongo.MongoClient()
    db = client.get_database(db)
    col = db.get_collection(col)
    return col

def insert_file(filename, dbname, colname):
    print "get_mongo_col", dbname, colname
    dbcol = get_mongo_col(dbname, colname)
    for i, line in enumerate(open(filename)):
        try:
            data = json.loads(line.rstrip())
        except:
            print >> sys.stderr, line.rstrip()

        objid = dbcol.insert(data)
        print datetime.datetime.now(), i, objid #, data[u'ID']
        sys.stdout.flush()

if __name__ == "__main__":
    insert_file(sys.argv[1], sys.argv[2], sys.argv[3])

