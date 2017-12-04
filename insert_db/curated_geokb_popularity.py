# coding: utf-8

from __future__ import absolute_import

import sys, datetime, itertools
import json

import pymongo

from curated_geokb.calc_poi_popularity import init_col_sets, init_db

def build_popularity_dict():
    popularities = {}
    for domain, filename in itertools.izip(*init_col_sets()):
        popularities[domain] = {}
        for l in open(filename):
            shopid, score = l.rstrip().split('\t')
            score = int(score)

            popularities[domain][shopid] = score
    return popularities
            
def get_col_tuples():
    return list(itertools.product(['beijing', 'guangzhou', 'shanghai'], ['cater', 'hotel', 'tour']))

def update_popularity():
    conn = pymongo.MongoClient()
    db = conn.geokb

    popularities = build_popularity_dict()
    for city, domain in get_col_tuples():
        col = db.get_collection('_'.join((city, domain)))
        
        for i, doc in enumerate(col.find()):
            shopid = doc[u'ID']
            score = popularities[domain].get(shopid)
            if score is None:
                score = 0
            res = col.update_one({'_id': doc['_id']}, {'$set': {'popularity': score}})

            print res.acknowledged, doc['_id'], shopid, score


if __name__ == "__main__":
    update_popularity()

