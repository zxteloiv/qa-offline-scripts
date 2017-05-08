# coding: utf-8

import sys, re, pymongo

def cleanup(word):
    word = re.sub('\[\[.*\|(.*)\]\]', r'\1', word) # replace the link with the anchor text: [[something|anchor]] -> anchor
    word = re.sub('\[\[([^\|]*)\|?$', r'\1', word) # left part of a link: [[something -> something
    word = re.sub('\[\[[^\|]*\|([^\]]*)$', r'\1', word) # left and right part of a link: [[something|anchor -> anchor
    word = re.sub('[^\|]*\|(.*)\]\]', r'\1', word) # right part of a link: something|anchor]] -> anchor
    word = re.sub('.*\|(.*)$', r'\1', word) # middle part of a link: something|anchor -> anchor
    word = re.sub('[\[\]\|]', '', word) # remove all [, ] and |
    return word

def cleanup_predicate_match(filename):
    for line in open(filename):
        parts = line.rstrip().split('\t')
        try:
            src, dest, score = cleanup(parts[0]), cleanup(parts[1]), int(parts[2])
        except:
            continue

        if not src or not dest: continue
        yield (src, dest, score)

def insert_mongo(triple, client):
    t = {"src":triple[0], "dest":triple[1], "score":triple[2]}
    client.poi_db.predicate_mapper.insert_one(t)

def miao():
    client = pymongo.MongoClient()
    for t in cleanup_predicate_match(sys.argv[1]):
        insert_mongo(t, client)

if __name__ == "__main__":
    miao()

