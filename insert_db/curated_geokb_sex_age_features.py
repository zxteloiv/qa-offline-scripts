# coding: utf-8

from __future__ import absolute_import

import sys, datetime, itertools
import json

import pymongo

from curated_geokb.calc_poi_popularity import init_col_sets, init_db

def build_feature_dict():
    features = {}
    for domain, filename in itertools.izip(*init_col_sets()):
        features[domain] = {}
        for l in open(filename):
            parts = l.rstrip().split('\t')
            shopid = parts[0]
            scores = dict((feature, int(score)) for score, feature in itertools.izip(parts[1:], get_feature_names()))

            features[domain][shopid] = scores
    return features
            
def get_col_tuples():
    return list(itertools.product(['beijing', 'guangzhou', 'shanghai'], ['cater', 'hotel', 'tour']))

def get_feature_names():
    return ['popularity', 'male', 'female', 'young', 'adult', 'elder']

def update_features():
    conn = pymongo.MongoClient()
    db = conn.geokb

    features = build_feature_dict()
    for city, domain in get_col_tuples():
        col = db.get_collection('_'.join((city, domain)))
        
        for i, doc in enumerate(col.find()):
            shopid = doc[u'ID']
            scores = features[domain].get(shopid)
            if scores is None:
                scores = dict((f, 0) for f in get_feature_names())

            res = col.update_one({'_id': doc['_id']}, {'$set': {'_sys_ranks': scores}})
            print res.acknowledged, doc['_id'], shopid, str(scores)


if __name__ == "__main__":
    update_features()

