# coding: utf-8

import sys
import time
import re
import requests

url = "http://www.tripadvisor.cn/Search"

def download_file(filename):
    for line in open(filename):
        query = line.strip()

        params = {
                "geo": 294212,
                "q": query
                }

        response = requests.get(url, params=params)
        print re.sub(r' +', ' ', re.sub(r'\r|\n', ' ', response.text)).encode('utf-8')
        time.sleep(1)

if __name__ == "__main__":
    download_file(sys.argv[1])
