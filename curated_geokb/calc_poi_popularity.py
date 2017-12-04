# coding: utf-8

from pymongo import MongoClient

import re, json, sys, os.path, itertools

def init_db():
    c = MongoClient()
    return c.review

def init_col_sets():
    colnames = ['cater', 'hotel', 'tour']
    filenames = ['cater.dat', 'hotel.dat', 'tour.dat']

    return colnames, filenames

def calc_popularity(argv):
    review = init_db()

    for colname, filename in itertools.izip(*init_col_sets()):

        col = review.get_collection(colname)

        fout = open(filename, 'w')

        for i, doc in enumerate(col.find({})):
            shopid = doc[u'店铺ID']
            count = len(doc[u'评论列表'])
            fout.write(u'{0}\t{1}\n'.format(shopid, count).encode('utf-8'))

            if i % 5000 == 0:
                print colname, i, 'records processed'
                fout.flush()

        fout.close()


if __name__ == "__main__":
    calc_popularity(sys.argv)


