# coding: utf-8

import sys
import pymysql.cursors
import json
import datetime

connection = pymysql.connect(host="localhost",
        user="root",
        password="AptX4869",
        db="wiki_entities",
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()

sql = '''insert into `ent_name` (`ent_id`, `en_name`, `zh_name`, `ja_name`)
values (%s, %s, %s, %s)'''

counter = 0
for line in open(sys.argv[1]):
    data = json.loads(line)
    try:
        cursor.execute(sql, (data['ent_id'], data['en'], data['zh'], data['ja']))
        connection.commit()

        counter += 1
        if counter % 100000 == 0:
            print (datetime.datetime.now(),
                    'written %d records, last %s' % (counter, line.rstrip()))
    except:
        print >> sys.stderr, (datetime.datetime.now(),
                "error insert ent_id=%s" % data['ent_id'])
        continue

