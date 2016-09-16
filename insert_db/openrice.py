# coding: utf-8

from __future__ import absolute_import

import sys
import os.path
import json, datetime
import urlparse

from bs4 import BeautifulSoup

from insert_db.bd_search import get_mongo_col

def parse_general_info(general_info, obj):
    # essential fields, any missing value will raise an exception
    obj[u'addr'] = general_info.find('div', 'address-info-section').get_text(strip=True)

    # optional fields
    for tag in general_info.find_all(class_='sr2-overview-container'):
        if tag.find(class_='address-info-section'):
            continue
        elif 'phone-section' in tag.get('class'):
            obj[u'phone'] = u' '.join(p.get_text(strip=True).replace(' ', '') for p in tag.find_all('span'))
        elif tag.find(itemprop='priceRange'):
            obj[u'price'] = tag.get_text(strip=True)
        else:
            obj[u'description'].append(tag.get_text(strip=True))

def parse_openrice_file(filename, baidu_id=None, shopid=None, ctime=None):
    soup = BeautifulSoup(open(filename).read(), 'lxml')
    detail = soup.find('div', 'pois-detail-body')

    obj = {u'description': []}
    obj[u'baiduid'] = baidu_id
    obj[u'shopid'] = shopid
    obj[u'locale'] = u'zh'
    obj[u'create_time'] = ctime
    obj[u'name'] = soup.find(itemprop='name').get_text(strip=True)

    for section in detail.find_all(class_='or-section'):
        if 'general-info' in section.get('class'):
            parse_general_info(section, obj)

        elif section.find(class_='signature-dishes-container'): # 招牌菜
            obj[u'dishes'] = [ y
                    for y in (x.get_text(strip=True) for x in section.find_all('span'))
                    if y ] # extracted text must not be empty

        elif section.find_all(class_='sr2-overview-container'):
            for tag in section.find_all(class_='sr2-overview-container'):
                obj[u'description'].extend( y
                        for y in (x.get_text(strip=True) for x in tag.find_all(class_='text'))
                        if y ) # extracted text must not be empty

        else:
            pass

    return obj


def insert_file(filename, prefix):
    col = get_mongo_col(col='openrice')
    for line in open(filename):
        parts = line.rstrip().split(' ')

        ctime = parts[0] + " " + parts[1][:8] # 2016-09-07 14:48:08.386197
        baiduid = parts[2]
        localid = parts[-1]

        fout_name = urlparse.urlparse(parts[4]).netloc.replace('.', '_') + '_' + baiduid
        fout_name = os.path.join(prefix, baiduid[-1], fout_name)

        try:
            obj = parse_openrice_file(fout_name, baiduid, localid, ctime)
        except:
            print >> sys.stderr, datetime.datetime.now(), fout_name, line.rstrip()
            sys.stderr.flush()
            continue

        col.insert(obj)

        print datetime.datetime.now(), baiduid, localid
        sys.stdout.flush()

if __name__ == "__main__":
    insert_file(sys.argv[1], sys.argv[2])

