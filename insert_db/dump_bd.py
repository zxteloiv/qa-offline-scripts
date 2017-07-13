# coding: utf-8

import sys
import pymongo

def main():
    client = pymongo.MongoClient()
    for item in client.poi_db.bd_search.find():
        try:
            oid = item['_id']
            name = item['name']
            uid = item['localid']

            print str(oid), name.encode('utf-8'), uid.encode('utf-8')
        except:
            print >> sys.stderr, repr(item)

if __name__ == "__main__":
    main()
