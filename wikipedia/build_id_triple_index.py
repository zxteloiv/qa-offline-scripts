# coding: utf-8

import sys, json

def build_triple_index(fin, fout):
    fout = open(fout, 'wb')
    for line in open(fin):
        parts = line.rstrip().split('\t')
        if len(parts) != 4: continue
        ent_id, ent_name, relation, value = parts

        triple_obj = {"ent_id": ent_id,
                "name": ent_name, "relation": relation, "value":value }

        fout.write(json.dumps(triple_obj) + '\n')
        fout.flush()
    fout.close()

if __name__ == "__main__":
    build_triple_index(sys.argv[1], sys.argv[2])

