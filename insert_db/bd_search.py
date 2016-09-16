# coding: utf-8

import sys, datetime
import json

import pymongo

def get_mongo_col(db="poi_db", col="bd_search"):
    client = pymongo.MongoClient()
    db = client.poi_db
    col = db.get_collection(col)
    return col

def parse_result(result):
    obj = {}
    # essential fields
    try:
        obj[u'name'] = result['name']
        obj[u'addr'] = result['address']
        obj[u'lng'] = result['location']['lng']
        obj[u'lat'] = result['location']['lat']
        obj[u'localid'] = result['uid']
        obj[u'src'] = 'baidu'
    except:
        return None

    # optional fields
    if u'detail_info' in result:
        for key in (u'overall_rating', u'shop_hours', u'tag', u'comment_num', u'detail_url'):
            if key in result['detail_info']:
                obj[key] = result['detail_info'][key]

    return obj

def insert_file(filename):
    dbcol = get_mongo_col()
    for line in open(filename):
        try:
            data = json.loads(line.rstrip())
        except:
            print >> sys.stderr, line.rstrip()

        if data['status'] != 0:
            continue

        for result in data['results']:
            obj = parse_result(result)

            if obj:
                objid = dbcol.insert(obj)
                print datetime.datetime.now(), objid, obj['src'], obj['localid']
                sys.stdout.flush()

if __name__ == "__main__":
    insert_file(sys.argv[1])

