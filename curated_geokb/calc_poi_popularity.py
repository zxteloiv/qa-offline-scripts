# coding: utf-8

from pymongo import MongoClient

import re, json, sys, os.path, itertools, datetime

def init_db():
    c = MongoClient()
    return c.review

def init_col_sets():
    colnames = ['cater', 'hotel', 'tour']
    filenames = ['cater.dat', 'hotel.dat', 'tour.dat']

    return colnames, filenames

def calc_popularity(argv):
    reviewdb = init_db()

    for colname, filename in itertools.izip(*init_col_sets()):

        col = reviewdb.get_collection(colname)

        fout = open(filename, 'w')

        for i, doc in enumerate(col.find({})):
            shopid = doc[u'店铺ID']
            count = len(doc[u'评论列表'])
            male = 0
            female = 0
            young = 0
            adult = 0
            elder = 0

            for review in doc[u'评论列表']:
                male += 1 if "man" == review[u'用户性别'] else 0
                female += 1 if "woman" == review[u'用户性别'] else 0

                birth = review[u'用户生日']
                adulthood_start = datetime.datetime.strptime('1997-1-1', '%Y-%m-%d')
                elder_start = datetime.datetime.strptime('1977-1-1', '%Y-%m-%d')
                try:
                    dt_birth = datetime.datetime.strptime(birth, '%Y-%m-%d')
                    if dt_birth < adulthood_start:
                        young += 1
                    elif dt_birth < elder_start:
                        adult += 1
                    else:
                        elder += 1

                except:
                    pass
                    
            
            fout.write(u'{shopid}\t{count}\t{male}\t{female}\t{young}\t{adult}\t{elder}\n'.format(
                shopid=shopid, count=count, male=male, female=female, young=young, adult=adult, elder=elder
                ).encode('utf-8'))

            if i % 5000 == 0:
                print colname, i, 'records processed'
                fout.flush()

        fout.close()


if __name__ == "__main__":
    calc_popularity(sys.argv)


