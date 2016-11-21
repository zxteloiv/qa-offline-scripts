# coding: utf-8

import sys

fout = open(sys.argv[2], 'wb')

for line in open(sys.argv[1], 'rb'):
    line = line.decode('utf-8')
    parts = line.rstrip().split('\t')

    if len(parts) <= 1:
        continue

    entity, categories = parts[0], parts[1:]

    # add filters
    if entity.startswith(' '): continue
    if entity.startswith('!'): continue
    if u'/' in entity or 'talk:' in entity: continue
    if u'User ' in entity: continue
    if any(u'_talk' in c or u'User_' in c
            for c in categories): continue

    categories = [ x for x in categories
            if  u'article' not in x
            and u'ikipedi' not in x
            and u'edirect' not in x
            and u'index' not in x
            and u'/' not in x
            and u'emplate' not in x 
            and u'_talk' not in x
            and u'_page' not in x
            and u'User_' not in x
            and u'索引页面' not in x
            and u'されないページ' not in x
            and u'重定向' not in x
            ]

    if len(categories) == 0: continue

    output = entity + u"\t" + u"\t".join(categories)
    fout.write(output.encode('utf-8') + "\n")


