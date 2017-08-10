# coding: utf-8

import sys, re, os

from attr_extractor import kbfile_reader, codec

f = open(sys.argv[1]).readline()
m = re.search(r'景点|酒店|餐饮', os.path.basename(f))
t, f = m.group(0), f.rstrip()

for example in kbfile_reader(codec(open(f))):
    pass
