# coding: utf-8

from pymongo import MongoClient

import re, json, sys, os.path, itertools

def init_db():
    c = MongoClient()
    return c.geokb

def main(argv):
    kb = init_db()
    colnames = list(itertools.product(['beijing', 'guangzhou', 'shanghai'], ['cater', 'hotel', 'tour']))

    for name in colnames:
        col = kb.get_collection('_'.join(name))

        for doc in col.find({}):
            k = u'名称'
            if k in doc:
                print u'\t'.join((name[1].decode('utf-8'), k, doc[k].strip())).encode('utf-8')

            for k in (u'推荐菜品', u'酒店设施', u'酒店服务', u'房间设施'):
                if k in doc:
                    for d in doc[k]:
                        for _, v in d.iteritems():
                            print u'\t'.join((name[1].decode('utf-8'), k, v.strip())).encode('utf-8')

if __name__ == "__main__":
    main(sys.argv)
