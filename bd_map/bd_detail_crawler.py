# coding: utf-8

import requests
import sys
import datetime
import time
import os.path

def download_file(filename, output_dir):
    for line in open(filename):
        uid, url = line.strip().split()
        f = open(os.path.join(output_dir, uid[-1], uid), 'w')

        for retry in xrange(3):
            try:
                response = requests.get(url, timeout=60) # 60s timeout
                break
            except:
                time.sleep(1)
                continue
        else:
            print datetime.datetime.now(), uid, "error", url
            continue

        response.encoding = 'utf-8'
        data = response.text
        data = data.encode('utf-8')
        f.write(data)
        f.close()
        print datetime.datetime.now(), uid, len(data)
        sys.stdout.flush()
        time.sleep(1)

if __name__ == "__main__":
    download_file(sys.argv[1], sys.argv[2])


