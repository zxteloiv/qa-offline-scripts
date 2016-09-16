# coding: utf-8

from __future__ import absolute_import

import sys
import os.path
import json, datetime
import urlparse

from bs4 import BeautifulSoup

from insert_db.bd_search import get_mongo_col

def parse_dianping_file(filename, baidu_id=None, shopid=None, ctime=None):
    soup = BeautifulSoup(open(filename).read(), 'lxml')
    main = soup.find(class_='main')

    obj = {u'description': []}
    obj[u'baiduid'] = baidu_id
    obj[u'shopid'] = shopid
    obj[u'create_time'] = ctime

    # essential fields, any missing value will raise an exception
    obj[u'name'] = unicode(main.find(class_='shop-name').find(text=True, recursive=False).strip())
    obj[u'addr'] = main.find('span', itemprop='street-address').get_text(strip=True)

    # optional fields
    obj[u'phone'] = u' '.join(t.get_text(strip=True).replace(' ', '') for t in main.find_all(itemprop='tel'))

    for info in main.find_all(class_='info info-indent'):
        info_name = info.find(class_='info-name')
        info_item = info.find(class_='item') 
        info_text = info.find(text=True, recursive=False).strip()
        if not info_name: continue
        if info_item:
            text = info_item.get_text(strip=False)
        elif info_text: # text can be in the tag rather than in another child tag
            text = unicode(info_text)
        else:
            continue
        obj[u'description'].append(u' '.join((info_name.get_text(strip=True), text)))

    return obj

def insert_file(filename, prefix):
    col = get_mongo_col(col='dianping')
    for line in open(filename):
        parts = line.rstrip().split(' ')

        ctime = parts[0] + " " + parts[1][:8] # 2016-09-07 14:48:08.386197
        baiduid = parts[2]
        localid = parts[-1]

        fout_name = urlparse.urlparse(parts[4]).netloc.replace('.', '_') + '_' + baiduid
        fout_name = os.path.join(prefix, baiduid[-1], fout_name)

        try:
            obj = parse_dianping_file(fout_name, baiduid, localid, ctime)
        except:
            print >> sys.stderr, line.rstrip()
            sys.stderr.flush()
            continue

        col.insert(obj)

        print datetime.datetime.now(), baiduid, localid
        sys.stdout.flush()

if __name__ == "__main__":
    insert_file(sys.argv[1], sys.argv[2])

