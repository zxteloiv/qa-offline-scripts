# coding: utf-8

import sys, json
import os.path
from bs4 import BeautifulSoup
import urlparse

def filename_gen(uidfile, path_prefix):
    for line in open(uidfile):
        uid = line.strip()
        yield uid, os.path.join(path_prefix, uid[-1], uid)

def parse_html(uid, filename):
    soup = BeautifulSoup(open(filename), 'lxml')

    resource = soup.find(id='resourceList')

    if resource is None: return

    links = resource.find_all('a')
    hrefs = (x.get('href') for x in links)
    parses = (urlparse.parse_qs(h) for h in hrefs)
    bd_redirect_urls = [p['url'] for p in parses if 'url' in p]
    further = [u[0] for u in bd_redirect_urls if len(u) > 0]

    for url in further:
        print uid, url

    sys.stdout.flush() 


def main(argv):
    for uid, filename in filename_gen(argv[1], argv[2]):
        parse_html(uid, filename)

if __name__ == "__main__":
    main(sys.argv)
