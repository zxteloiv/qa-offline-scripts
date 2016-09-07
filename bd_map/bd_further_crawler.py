# coding: utf-8

import requests
import sys
import datetime
import time
import os.path
import urlparse

def download_file(filename, output_dir):
    for line in open(filename):
        uid, url = line.strip().split()
        fout_name = urlparse.urlparse(url).netloc.replace('.', '_') + '_' + uid
        f = open(os.path.join(output_dir, uid[-1], fout_name), 'w')

        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for retry in xrange(5):
            try:
                response = requests.get(url, timeout=10, headers=headers) # 10s timeout
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
        print datetime.datetime.now(), uid, len(data), url
        sys.stdout.flush()
        time.sleep(1)

if __name__ == "__main__":
    download_file(sys.argv[1], sys.argv[2])


