# coding: utf-8

import sys
import time
import re, random
import requests

url = "http://www.tripadvisor.cn/Search"

def download_file(filename):
    for line in open(filename):
        query = line.strip()

        # http://www.tripadvisor.cn/Search?geo=&pid=3826&typeaheadRedirect=true&redirect=&startTime=1472010738265&uiOrigin=MASTHEAD&q=故宫&returnTo=__2F__&searchSessionId=64BFC6592AE1B2BBDCC2D3775FF7C3811472039535386ssid
        params = {
                "geo": 294212,
                "pid": 3826,
                "typeaheadRedirect": True,
                "startTime": int((time.time() - 8 * 3600 - 10) * 1000 + random.random() * 900),
                "uiOrigin": "MASTHEAD",
                "returnTo": "__2F__",
                "searchSessionId": "64BFC6592AE1B2BBDCC2D3775FF7C381147" + str(int(random.random() * 3039535386)) + "ssid",
                "q": query
                }

        response = requests.get(url, params=params)
        print re.sub(r' +', ' ', re.sub(r'\r|\n', ' ', response.text)).encode('utf-8')
        time.sleep(10)

if __name__ == "__main__":
    download_file(sys.argv[1])
