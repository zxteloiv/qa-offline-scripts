# coding: utf-8

import sys
import cPickle

from merge_category import normalized_entity_name

def build_rev_index(filename):
    rev_index = {"en":{}, "zh":{}, "ja":{}}
    for line in open(filename):
        parts = line.decode('utf-8').split('\t')
        ent_id, en, zh, ja = parts[0], parts[1], parts[2], parts[3]

        ja = ja.rstrip()

        if en.strip(): rev_index['en'][normalized_entity_name(en)] = ent_id
        if zh.strip(): rev_index['zh'][normalized_entity_name(zh)] = ent_id
        if ja.strip(): rev_index['ja'][normalized_entity_name(ja)] = ent_id

    return rev_index

def align_infobox_triples(filenames, rev_index):
    for f in filenames:
        print "processing %s..." % f
        fout = open(f + '.aligned', 'wb')
        if 'enwiki' in f:
            lang = 'en'
        elif 'zhwiki' in f:
            lang = 'zh'
        elif 'jawiki' in f:
            lang = 'ja'
        else:
            continue

        for line in open(f):
            parts = line.decode('utf-8').split('\t')
            if len(parts) < 3: continue

            h, r, t = parts[0], parts[1], parts[2]

            ent_id = rev_index[lang].get(normalized_entity_name(h))

            if not ent_id: continue

            out = u"\t".join((ent_id, h, r, t))
            fout.write(out.encode('utf-8')) # newline \n is already in t
            fout.flush()
        fout.close()

if __name__ == "__main__":
    #rev_index = build_rev_index(sys.argv[1])
    #cPickle.dump(rev_index, open("__rev__index.dat", 'wb'))
    print "loading rev index...."
    rev_index = cPickle.load(open('__rev__index.dat'))
    align_infobox_triples(sys.argv[2:], rev_index)

