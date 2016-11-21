# coding: utf-8

import sys, re, json
import re

def load_infobox_data(filename):
    ent, info = None, {}
    for line in open(filename):
        line = line.decode('utf-8').rstrip()
        if line == u"<page>":
            ent, info = None, {}
        elif u"<title>" in line and u"</title>" in line:
            m = re.match("<title>(.*)</title>", line)
            if m:
                ent = m.group(1).lower()
        elif u"<infobox>" == line:
            info = {}
        elif u"<==>" in line:
            parts = line.split('\t')
            key, val = parts[0], parts[-1]
            if not key or not val: continue
            info[key] = val
        elif u"</page>":
            if ent:
                yield ent.lower(), info
            ent, info = None, {}

def process(s):
    # remove hyperlinks to files
    s = re.sub(r'\[\[File[^\]]+\]\]', '', s)
    # remove hyperlinks with anchor text only
    s = re.sub(r'\[\[([^\|]*)\|([^\]]+)\]\]', r'\2', s)
    # remove links
    s = re.sub('\[|\]', '', s)
    # remove new line
    s = re.sub(r'<br */?>', ' ', s)
    # remove special chars
    s = re.sub(r'-_|-_-|_-|•', ' ', s)
    # remove continuous space
    s = re.sub('[ \t][ \t]*', ' ', s)
    # trim
    s = s.strip()

    return s

def main():
    for ent, info in load_infobox_data(sys.argv[1]):
        for k, v in info.iteritems():
            k = process(k)
            v = process(v)
            if not k or not v: continue
            out = u"\t".join((ent, k, v))
            print out.encode('utf-8')
            sys.stdout.flush()

if __name__ == "__main__":
    main()

