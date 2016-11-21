# coding: utf-8

import sys, json

def extract_id_name(filename):
    fout_name = open("ent_id_name.dat", 'wb')
    fout_cate = open("ent_id_cate.dat", 'wb')
    for line in open(filename):
        parts = line.rstrip().split('\t')
        if len(parts) != 2: continue

        ent_id, json_str = parts[0], parts[1]

        ent = json.loads(json_str)

        ent_name_obj = {'ent_id':ent_id,
                'en':ent['en'], 'zh':ent['zh'], 'ja':ent['ja']}
        fout_name.write(json.dumps(ent_name_obj) + '\n')

        for cate in ent['categories']:
            ent_cate_obj = {'ent_id':ent_id, 'category':cate}
            fout_cate.write(json.dumps(ent_cate_obj) + '\n')

        fout_name.flush()
        fout_cate.flush()

    fout_name.close()
    fout_cate.close()

if __name__ == "__main__":
    extract_id_name(sys.argv[1])
