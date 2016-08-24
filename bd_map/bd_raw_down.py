#coding: utf-8
from __future__ import absolute_import

import requests
import sys
import re
import config

bd_place_url = "http://api.map.baidu.com/place/v2/search"
ak = config.ak

def down(filename):
    for line in open(filename):
        poi_name = line.rstrip()

        # only POI in Beijing now
        params = {
                "ak": ak,
                "page_num": 0,
                "scope": 2,
                "output": "json",
                "region": "北京",
                "city_limit": True,
                "query": poi_name
                }

        response = requests.get(bd_place_url, params=params)

        # remove new line and substitute two or more consecutive spaces with one
        print re.sub(r' +', ' ', re.sub(r'\r|\n', ' ', response.text)).encode('utf-8')

if __name__ == "__main__":
    down(sys.argv[1])

