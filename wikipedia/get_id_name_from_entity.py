# coding: utf-8

import sys, json

def extract_id_name(filename):
    for line in open(filename):
        parts = line.rstrip().split('\t')
        if len(parts) != 2: continue

        ent_id, json_str = parts[0], parts[1]

        ent = json.loads(json_str)

        out = "\t".join((ent_id, ent['en'], ent['zh'], ent['ja']))

        print out.encode('utf-8')
        sys.stdout.flush()

if __name__ == "__main__":
    extract_id_name(sys.argv[1])
