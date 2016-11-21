# coding: utf-8

import json, sys

def main():
    print "reload base %s...." % sys.argv[1]
    ent_base = dict()
    rev_ent_idx = {"en":{}, "zh":{}, "ja":{}}
    for line in open(sys.argv[1]):
        line = line.rstrip().split('\t')
        if len(line) <= 1: continue
        ent_id, jsonstr = int(line[0]), line[1]
        ent = json.loads(jsonstr)
        ent_base[ent_id] = ent

        for lang in rev_ent_idx:
            if ent[lang]:
                rev_ent_idx[lang][ent[lang].lower().replace('_', ' ')] = ent_id

    for f in sys.argv[2:-1]:
        print "read wiki file %s..." % f
        lang = "en" if "enwiki" in f else ("zh" if "zhwiki" in f else "ja")

        for line in open(f):
            line = line.decode('utf-8').rstrip().split('\t')
            if len(line) <= 1: continue
            ent_name, triples = line[0].lower().replace('_', ' '), json.loads(line[1])

            if ent_name not in rev_ent_idx[lang]: continue

            ent_id = rev_ent_idx[lang][ent_name]
            ent = ent_base[ent_id]
            ent[lang + 'info'] = {}

            for triple in triples:
                r, t = triple[0], triple[1]
                ent[lang + 'info'][r] = t

    fout = open(sys.argv[-1], 'wb')
    for ent_id, ent in ent_base.iteritems():
        out = str(ent_id) + "\t" + json.dumps(ent)
        fout.write(out + "\n")
        fout.flush()

    fout.close()

if __name__ == "__main__":
    main()
