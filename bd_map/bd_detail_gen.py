# coding: utf-8

import sys, json

def process_file(filenames):
    for f in filenames:
        for line in open(f):
            if not line.strip(): continue
            data = json.loads(line)
            process_data(data)

def process_data(data):
    if u"results" not in data:
        return

    for poi in data[u"results"]:
        if poi.get("detail_info") and poi["detail_info"].get("detail_url"):
            uid = poi[u"uid"]
            url = poi[u"detail_info"][u"detail_url"]

            print uid, url

if __name__ == "__main__":
    process_file(sys.argv[1:])
